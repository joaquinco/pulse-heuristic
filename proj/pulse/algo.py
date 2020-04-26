from functools import partial

import networkx as nx
from .pulse import Pulse
from ..sorted import BinaryTree
from .pulse_context import PulseContext


def _initialize_pulse(
  graph, source, target, weight='weight', constraints=None, primal_bound=None):
  """
  Initialization phase of pulse algorithm
  """

  empty_weights = { k: 0 for k, _ in graph.nodes(source).values() }
  
  # Pulses over which we'll iterate
  pulses = BinaryTree([Pulse(source, empty_weights)], key=lambda p: p.weights[weight])

  # For cost pruning
  reverse_graph = graph.reverse_view()
  cost_bound_by_node = nx.single_source_dijkstra_path_length(
    reverse_graph, target, weight=weight
  )

  # For infeasibility pruning
  resource_bounds = {}
  for key in (constraints or {}).keys():
    resource_bounds[key] = nx.single_source_dijkstra_path_length(
      reverse_graph, target, weight=key
    )

  context = PulseContext(
    weight=weight,
    pulses=pulses,
    cost_bound_by_node=cost_bound_by_node,
    best_cost=primal_bound,
    constraints=constraints,
    resource_bounds=resource_bounds,
  )

  return context



def pulse(graph, *args, **kwargs):
  """
  Computes shortest path using pulse algorithm
  """

  if not graph:
    raise Exception('Graph is empty')

  context = _initialize_pulse(graph, *args, **kwargs)

  while True:
    if not context.pulses:
      return

    current = context.pulses.pop()

    for adjacent in graph.adj[current.node]:
      candidate_pulse = Pulse.from_pulse(current, adjacent, graph.nodes[adjacent])

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

      # TODO: if adjacent is target node then yield the full path.





