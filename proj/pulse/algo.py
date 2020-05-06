from functools import partial

import pdb

import networkx as nx
from .pulse import Pulse
from ..sorted import BinaryTree
from .pulse_context import PulseContext


def _initialize_pulse(
  graph, source, target, weight='weight', constraints=None, primal_bound=None):
  """
  Initialization phase of pulse algorithm
  """
  if graph.is_multigraph():
    some_edges = graph.edges(source, keys=True)
  else:
    some_edges = graph.edges(source)

  some_edge = list(some_edges)[0]
  empty_weights = { k: 0 for k in graph.edges[some_edge].keys() }
  
  # Pulses over which we'll iterate
  pulses = BinaryTree([Pulse(source, empty_weights)], key=lambda p: p.weights[weight])

  # For cost pruning
  reverse_graph = nx.reverse_view(graph)
  cost_bound_by_node = nx.single_source_dijkstra_path_length(
    reverse_graph, target, weight=weight
  )

  constraints = constraints or {}

  # For infeasibility pruning
  resource_bounds = {}
  for key in constraints.keys():
    resource_bounds[key] = nx.single_source_dijkstra_path_length(
      reverse_graph, target, weight=key
    )

  context = PulseContext(
    source=source,
    target=target,
    weight=weight,
    pulses=pulses,
    cost_bound=cost_bound_by_node,
    best_cost=primal_bound,
    constraints=constraints,
    resource_bounds=resource_bounds,
  )

  return context


def pulse(graph, *args, **kwargs):
  """
  Compute shortest path using pulse algorithm

  Args:
    graph: networkx graph instance
    source: source node
    target: target node
    weight: edge weight to minimize, default 'weight'
    constraints: dict of constraints, default None
    primal_bound: path cost between source and target used to bound branches.

  Returns:
    generator that yields path, path_weights
  """
  if not graph:
    raise Exception('Graph is empty')

  context = _initialize_pulse(graph, *args, **kwargs)

  while True:
    if not context.pulses:
      return

    current = context.pulses.pop()

    if graph.is_multigraph():
      out_edges = graph.edges(current.node, keys=True)
    else:
      out_edges = graph.edges(current.node)

    adjacency = [(edge[1], edge) for edge in out_edges]

    for adjacent, edge in adjacency:
      edge_weights = graph.edges[edge]

      candidate_pulse = Pulse.from_pulse(current, adjacent, edge_weights, edge=edge)

      # Cost pruning
      if not context.satisfies_cost(candidate_pulse):
        continue
      
      # Infeasibility pruning
      if context.dissatisfies_constraints(candidate_pulse):
        continue
      
      # Dominance pruning
      if context.is_dominated(candidate_pulse):
        continue

      context.save_pulse(candidate_pulse)
      context.pulses.add(candidate_pulse)

      if adjacent == context.target:
        # TODO: since yielding every path can end up in exponential space search,
        # it might be better to just return the best.
        # TODO: this can be also enforced buy giving a primal_bound that is low
        # enough
        yield candidate_pulse.to_path(), dict(candidate_pulse.weights)

