
import logging
import random

from proj import pulse, configuration
from .solver_context import SolverContext


def print_report(ctx):
  """
  Print results of the solve algorithm
  """
  
  if ctx.current_solution:
    ctx.current_solution.print()
  else:
    logging.info('No solution found')


def run_solve_search(ctx, od_index):
  """
  Run recursive algorithm saving best results on the leafs.
  """
  od = ctx.odpairs[od_index]
  source, target = od

  paths = pulse(
    ctx.current_graph, source, target, weight='weight',
    primal_bound=ctx.base_primal_bound[od] * configuration.pulse_primal_bound_factor
  )

  for path in paths:
    ctx.apply_path(path)
    if od_index == len(ctx.odpairs) - 1:
      ctx.compute_objective()
    else:
      run_solve_search(ctx, od_index + 1)
    ctx.remove_path(path)

def run_solve(ctx):
  """
  Run metaheristic
  """
  odpairs = list(ctx.demand)

  for iter in range(1, configuration.max_iter + 1):
    ctx.odpairs = odpairs
    ctx.modifications = { k: {} for k in odpairs }

    run_solve_search(ctx, 0)


def solve(graph, infrastructures, demand, budget):
  """
  Runs the algorithm to solve the multi-commodity multi-facility problem

  Args:
    graph: networkx graph instance
    infrastructures:
    demand: mapping from (o, d) pair to demand amount
    budget: number
  """
  g = SolverContext(
    graph, demand, infrastructures, budget,
  )

  try:
    run_solve(g)
  except InterruptedError:
    logging.info('Exporting solution')
    print_report(g)
