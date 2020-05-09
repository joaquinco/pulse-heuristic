import networkx as nx

from proj.constants import infinite
from proj.context import Context
from proj.cache import cached_property
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
    self.best_cost_fixed = bool(best_cost)
    self.pulses_by_node = {}

  def dissatisfies_constraints(self, pulse):
    """
    Returns if should prune by infeasibility
    """

    for name, value in self.constraints.items():
      if name == self.cost_weight:
        continue
      if pulse.weights[name] + self.resource_bounds[name][pulse.node] > value:
        return True
    
    return False

  def satisfies_cost(self, pulse):
    """
    Returns if pulse should not be pruned by cost bound
    """
    # If target is unreachable from pulse.node, then infinite
    estimated_target_cost = self.cost_bound.get(pulse.node, infinite)

    if estimated_target_cost + pulse.weights[self.cost_weight] > self.best_cost:
      return False
    
    return True

  def is_dominated(self, pulse):
    for other_pulse in self.pulses_by_node.get(pulse.node, []):
      if other_pulse.dominates(pulse):
        return True
    
    return False

  def save_pulse(self, pulse):
    node_pulses = self.pulses_by_node.get(pulse.node, set())

    to_remove = set()
    for other_pulse in node_pulses:
      if pulse.dominates(other_pulse):
        to_remove.add(other_pulse)

    node_pulses -= to_remove
    node_pulses.add(pulse)

    # Update best cost if needed
    is_target = self.target == pulse.node
    pulse_cost = pulse.weights[self.cost_weight]
    if is_target and pulse_cost < self.best_cost and not self.best_cost_fixed:
      self.best_cost = pulse_cost

    self.pulses_by_node[pulse.node] = node_pulses

  @cached_property
  def cost_bound(self):
    """For infeasability pruning"""
    ret = nx.single_source_dijkstra_path_length(
      self.reverse_graph, self.target, weight=self.weight
    )

    return ret

  @cached_property
  def resource_bounds(self):
    """For infeasibility pruning"""
    resource_bounds = {}

    for key in self.constraints.keys():
      resource_bounds[key] = nx.single_source_dijkstra_path_length(
        self.reverse_graph, self.target, weight=key
      )

    return resource_bounds

  @cached_property
  def reverse_graph(self):
    return nx.reverse_view(self.graph)
