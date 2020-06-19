from functools import partial

import networkx as nx
from .pulse import Pulse
from .pulse_context import PulseContext
from proj import logger, configuration


def _log_stats(context, current=None):
  """
  Log pulse stats
  """
  stats = context.stats()

  if current:
    logger.debug(f'Pulse: current {current}, stack len: {len(context.pulses)}')

  logger.debug(
    'Pruned by cost: {cost_pruned}, dominance: {dominance_pruned}, infeasibility: {inf_pruned}'.format(**stats)
  )
  logger.debug(
    'Active pulses: {total_pulses}, nodes reached: {nodes_reached}, total nodes: {total_nodes}'.format(**stats)
  )


def _pulse(
  graph, source, target, weight,
  constraints=None,
  primal_bound=None,
  pulse_key_fn=None
):
  """
  Compute shortest path using pulse algorithm

  Args:
    graph: networkx graph instance
    source: source node
    target: target node
    weight: edge weight to minimize
    constraints: dict of constraints, default None
    primal_bound: path cost between source and target used to bound branches.
    pulse_key_fn: callable that returns the sorting key of pulses

  Returns:
    generator that yields path, path_weights
  """
  if not graph:
    raise Exception('Graph is empty')

  context = PulseContext(
    source=source,
    target=target,
    weight=weight,
    graph=graph,
    best_cost=primal_bound,
    constraints=constraints or {},
    pulse_key_fn=pulse_key_fn,
  )

  iteration = 0
  while True:
    current = context.pop_pulse()

    if not current:
      return

    iteration += 1

    if iteration % 10000 == 0:
      _log_stats(context, current)

    if graph.is_multigraph():
      out_edges = graph.edges(current.node, keys=True)
    else:
      out_edges = graph.edges(current.node)

    adjacency = [(edge[1], edge) for edge in out_edges]

    for adjacent, edge in adjacency:
      if adjacent == current.node:
        # Ignore self loops
        continue

      if configuration.pulse_discard_faraway_nodes \
        and (context.get_cost_bound(adjacent) - context.get_cost_bound(current.node) >= \
          configuration.pulse_discard_faraway_delta):
        # Ignore adjacent whose lower bound cost plus delta is greater than current
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
        _log_stats(context)
        yield candidate_pulse.to_path(), dict(candidate_pulse.weights)


def pulse(*args, **kwargs):
  """
  Calls pulse algorithm.

  If return best only is enabled, then returns the best.
  """
  weight_key = kwargs.get('weight')

  pulses_generator = _pulse(*args, **kwargs)

  best = None
  best_cost = None

  iter = 0
  for pulse, weights in pulses_generator:
    iter += 1

    # Update local best
    if best is None or best_cost > weights.get(weight_key):
      best_cost = weights.get(weight_key)
      best = pulse, weights

    if not configuration.pulse_return_best and iter % configuration.pulse_return_best_every == 0:
      yield best
      best = best_cost = None

  if best:
    yield best

