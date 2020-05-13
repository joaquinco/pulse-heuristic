from functools import partial
import logging

import networkx as nx
from .pulse import Pulse
from .pulse_context import PulseContext

def _initialize_pulse(
  graph, source, target, weight='weight', constraints=None, primal_bound=None):
  """
  Initialization phase of pulse algorithm
  """
  constraints = constraints or {}

  context = PulseContext(
    source=source,
    target=target,
    weight=weight,
    graph=graph,
    best_cost=primal_bound,
    constraints=constraints,
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

  iteration = 0
  while True:
    if not context.pulses:
      return

    current = context.pop_pulse()
    iteration += 1

    if iteration % 10000 == 0:
      logging.debug(f'Pulse: current {current}, stack: {context.pulses}')

    if graph.is_multigraph():
      out_edges = graph.edges(current.node, keys=True)
    else:
      out_edges = graph.edges(current.node)

    adjacency = [(edge[1], edge) for edge in out_edges]

    for adjacent, edge in adjacency:
      if adjacent == current.node:
        # Ignore self loops
        continue

      edge_weights = graph.edges[edge]

      candidate_pulse = Pulse.from_pulse(current, adjacent, edge_weights, edge)

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

      if adjacent == context.target:
        # TODO: since yielding every path can end up in exponential space search,
        # it might be better to just return the best.
        # TODO: this can be also enforced buy giving a primal_bound that is low
        # enough
        yield candidate_pulse.to_path(), dict(candidate_pulse.weights)

