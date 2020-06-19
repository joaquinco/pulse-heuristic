
import random

from proj import pulse, configuration, logger
from proj.timer import timed
from .solver_context import SolverContext


def print_report(ctx):
  """
  Print results of the solve algorithm
  """
  
  if ctx.current_solution:
    ctx.current_solution.print()
  else:
    logger.info('No solution found')


def run_solve_search(ctx, od_index):
  """
  Run recursive algorithm computing solution score on the leafs.
  """
  if od_index >= len(ctx.odpairs):
    ctx.recompute_objective()
    return

  od = ctx.odpairs[od_index]
  source, target = od

  constraints = { configuration.arc_cost_key: ctx.get_budget(od) }
  primal_bound = ctx.base_primal_bound[od] * configuration.pulse_primal_bound_factor

  logger.debug(
    'Running od {}, constraints: {}, primal_bound: {}'.format(
      od, constraints, primal_bound
    )
  )

  paths = pulse(
    ctx.current_graph, source, target,
    weight=configuration.arc_weight_key, constraints=constraints,
    primal_bound=primal_bound, pulse_key_fn=ctx.pulse_key_fn
  )

  found = False

  for num, path_info in enumerate(paths):
    found = True
    path, path_weights = path_info

    logger.debug('Found path for {}: {}, {}'.format(od, path, path_weights))

    ctx.apply_path(od, path)
    run_solve_search(ctx, od_index + 1)
    ctx.disapply_path(od, path)

    if num >= configuration.solutions_per_od - 1:
      return

  if not found:
    logger.warning(f'Path not found for {od}')


def run_solve(ctx):
  """
  Run metaheristic
  """
  odpairs = list(ctx.demand)
  logger.info(f'Base primal bound per od {ctx.base_primal_bound}')

  for iter in range(1, configuration.max_iter + 1):
    random.shuffle(odpairs)
    logger.debug('Main iteration {}, ods: {}'.format(iter, odpairs))

    ctx.odpairs = odpairs
    run_solve_search(ctx, 0)

  return ctx.best_solution


@timed('Solve')
def solve(graph, infrastructures, demand, budget):
  """
  Runs the algorithm to solve the multi-commodity multi-facility problem

  Args:
    graph: networkx graph instance
    infrastructures: dict with infrastructure data
    demand: mapping from (o, d) pair to demand amount
    budget: number
  """
  random.seed(configuration.seed)

  g = SolverContext(
    graph, infrastructures, demand, budget,
  )

  try:
    return run_solve(g)
  except InterruptedError:
    logger.info('Exporting solution')
    print_report(g)
