import networkx as nx

from proj.constants import infinite
from proj.context import Context
from proj.cache import cached_property
from proj.timer import timed
from .pulse import Pulse
from ..sorted import BinaryTree

class PulseContext(Context):
  def __init__(
        self,
        source=None,
        target=None,
        weight=None,
        graph=None,
        constraints=None,
        best_cost=None,
        **kwargs
      ):
    super().__init__(**kwargs)
    
    self.source = source
    self.target = target
    self.cost_weight = weight
    self.graph = graph
    self.constraints = constraints
    self.best_cost = best_cost or infinite
    self.pulses_by_node = {}
    self.nodes_reached = set()
    self.total_pulses = 0
    self.cost_pruned = 0
    self.dominance_pruned = 0
    self.inf_pruned = 0

    self._init_pulses()

  def _init_pulses(self):
    if self.graph.is_multigraph():
      some_edges = self.graph.edges(self.source, keys=True)
    else:
      some_edges = self.graph.edges(self.source)

    some_edge = list(some_edges)[0]
    empty_weights = { k: 0 for k in self.graph.edges[some_edge].keys() }
    
    # Pulses over which we'll iterate
    self.pulses = BinaryTree(
      [Pulse(self.source, empty_weights)], key=self.projected_weight
    )

  def projected_weight(self, pulse):
    """
    Key by which pulses are sorted. It will determinate which pulse to consider in
    each
    """
    return self.get_cost_bound(pulse.node) + pulse.weights[self.cost_weight]

  def get_cost_bound(self, node):
    # If target is unreachable from pulse.node, then infinite
    return self.cost_bound.get(node, infinite)

  def dissatisfies_constraints(self, pulse):
    """
    Returns if should prune by infeasibility
    """
    for name, value in self.constraints.items():
      if name == self.cost_weight:
        continue
      if pulse.weights[name] + self.resource_bounds[name][pulse.node] > value:
        self.inf_pruned += 1
        return True
    
    return False

  def satisfies_cost(self, pulse):
    """
    Returns if pulse should not be pruned by cost bound
    """
    if self.projected_weight(pulse) > self.best_cost:
      self.cost_pruned += 1
      return False
    
    return True

  def is_dominated(self, pulse):
    for other_pulse in self.pulses_by_node.get(pulse.node, []):
      if other_pulse.dominates(pulse):
        self.dominance_pruned += 1
        return True
    
    return False

  def save_pulse(self, pulse):
    """
    Remove pulses that are dominated by the new one and add the pulse
    to the queue.
    """
    self.nodes_reached.add(pulse.node)

    node_pulses = self.pulses_by_node.get(pulse.node, set())
    to_remove = set()
    for other_pulse in node_pulses:
      if pulse.dominates(other_pulse):
        to_remove.add(other_pulse)
        other_pulse.dominated = True

    node_pulses -= to_remove
    node_pulses.add(pulse)

    self.total_pulses -= len(to_remove) - 1

    self.pulses_by_node[pulse.node] = node_pulses
    self.pulses.add(pulse)

    # Update best cost if needed
    is_target = self.target == pulse.node
    pulse_cost = pulse.weights[self.cost_weight]
    if is_target and pulse_cost < self.best_cost:
      self.best_cost = pulse_cost


  @cached_property
  def cost_bound(self):
    """For infeasability pruning"""
    dijkstra = timed('cost bound dijkstra')(nx.single_source_dijkstra_path_length)
    ret = dijkstra(
      self.reverse_graph, self.target, weight=self.cost_weight
    )

    if ret.get(self.source) is None:
      raise Exception(f'{self.target} is not reachable from {self.source}')

    return ret

  @cached_property
  def resource_bounds(self):
    """For infeasibility pruning"""
    resource_bounds = {}

    for key in self.constraints.keys():
      dijkstra = timed(f'{key} bound dijkstra')(nx.single_source_dijkstra_path_length)
      resource_bounds[key] = dijkstra(
        self.reverse_graph, self.target, weight=key
      )

    return resource_bounds

  @cached_property
  def reverse_graph(self):
    return nx.reverse_view(self.graph)

  def pop_pulse(self):
    """
    Pop a pulse from the queue. Also removes it from the node.
    """
    while True:
      pulse = self.pulses.pop()

      if not pulse:
        return None

      if pulse.dominated:
        continue

      node_pulses = self.pulses_by_node.get(pulse.node)
      if node_pulses:
        node_pulses.remove(pulse)

      return pulse

  def stats(self):
    """
    Return current stats
    """

    return dict(
      total_pulses=self.total_pulses,
      nodes_reached=len(self.nodes_reached),
      total_nodes=self.graph.number_of_nodes(),
      cost_pruned=self.cost_pruned,
      dominance_pruned=self.dominance_pruned,
      inf_pruned=self.inf_pruned
    )
