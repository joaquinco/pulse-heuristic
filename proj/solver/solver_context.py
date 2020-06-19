import networkx as nx

from proj import configuration, logger
from proj.context import Context
from proj.cache import cached_property
from proj.constants import infinite
from .solution import Solution
from .functions import astar_path, astar_path_length, get_zero_weight_subgraph, normalize
from .graph import construct_multigraph
from proj import logger


class SolverContext(Context):
  def __init__(self, graph, infrastructures, demand, budget, **kwargs):
    self.graph = graph
    self.demand = demand
    self.infrastructures = Context(infrastructures)
    self.budget = budget
    self.available_budget = budget
    self.best_solution = Solution(infinite, {})
    self.current_graph = construct_multigraph(graph, infrastructures)

    super().__init__(**kwargs)

  def recompute_objective(self):
    """
    Compute objective function:
    
    Find shortest path between every origin-destination pair and then multiply
    the each by demand amount.
    """
    ac = 0
    paths = {}

    result_graph = get_zero_weight_subgraph(
      self.current_graph, configuration.arc_cost_key
    )

    for od, demand_amount in self.demand.items():
      shortest_path, path_length = astar_path(
        result_graph, *od, configuration.arc_weight_key
      )
      paths[od] = dict(path=shortest_path, length=path_length)
      ac += demand_amount * path_length

    if ac < self.best_solution.value:
      logger.debug('Best objective {}'.format(ac))

      self.best_solution = Solution(ac, self.modifications, shortest_paths=paths)

    return ac

  @cached_property
  def budget_percentage_per_od(self):
    """
    Calculates budget percentage per od
    """
    normalized_base_costs = normalize([self.base_primal_bound[od] for od in self.odpairs])
    if configuration.budget_assignment_approach == 'path_length':
      percentages = normalized_base_costs

    normalized_demand = normalize([self.demand[od] for od in self.odpairs])
    if configuration.budget_assignment_approach == 'demand':
      percentages = normalized_demand
    else:
      percentages = normalize([
        normalized_base_costs[i] * normalized_demand[i] for i in range(len(self.odpairs))
      ])

    ret = {od: percentages[i] for i, od in enumerate(self.odpairs)}
    logger.debug(f'Budget assignment {ret}')

    return ret

  @cached_property
  def modifications(self):
    return { od: {} for od in self.odpairs }

  def apply_path(self, od, path):
    """
    Applies the path to the current_graph, meaning that its arcs won't have a
    construction cost
    """
    path_weights = {}

    logger.debug('Applying path {} from {}'.format(path, od))

    for arc in path:
      infra_cost = self.current_graph.edges[arc][configuration.arc_cost_key]
      self.available_budget -= infra_cost
      path_weights[arc] = infra_cost
      self.current_graph.edges[arc][configuration.arc_cost_key] = 0

    self.modifications[od] = path_weights

  def disapply_path(self, od, path):
    """
    Dismantle path, meaning that its arcs will have a cost again
    """
    logger.debug('Disapplying path {} from {}'.format(path, od))

    for arc, infra_cost in self.modifications[od].items():
      self.available_budget += infra_cost
      self.current_graph.edges[arc][configuration.arc_cost_key] = infra_cost

    self.modifications[od] = {}

  def get_budget(self, od):
    """
    Returns the budget for a given od.
    """
    p = self.budget_percentage_per_od[od]

    return min(
      configuration.od_budget_factor * p * self.budget + configuration.od_budget_epsilon,
      self.available_budget
    )

  @cached_property
  def base_primal_bound(self):
    """
    Returns best path cost per OD in base graph.
    """
    ret = {}

    for od in self.demand.keys():
      path, ret[od] = astar_path(self.graph, *od, configuration.arc_weight_key)
      logger.debug(f'Base shortest path for {od}: {path}')

    return ret

  def pulse_key_fn(self, pulse, ctx):
    """
    Returns the key that sorts pulses in pulse algorithm. Meant to override
    the default
    """
    if configuration.solver_pulse_key_approach == 'naive':
      return pulse.weights[ctx.cost_weight] + ctx.get_cost_bound(pulse.node)

    bp = ctx.constraints['construction_cost'] - pulse.weights['construction_cost']
    bp_factor = pulse.weights['construction_cost'] / ctx.constraints['construction_cost']
    qp, ip = self.agg_infra_factors
    lp = bp / qp
    cp = ctx.get_cost_bound(pulse.node) / self.min_infra_cost

    projected_cost = cp - lp + lp * ip * qp
  
    return (pulse.weights[ctx.cost_weight] + projected_cost) * (1 + bp_factor)

  @cached_property
  def agg_infra_factors(self):
    """
    Return (construction_cost_factor, cost_factor) used to estimate projected cost of pulse
    """
    if configuration.solver_pulse_key_approach == 'max_cost':
      qp = max(self.infrastructures.construction_cost_factors)
      ip = min(self.infrastructures.cost_factors)
    elif configuration.solver_pulse_key_approach == 'min_cost':
      qp = max(self.infrastructures.construction_cost_factors)
      ip = min(self.infrastructures.cost_factors)
    elif configuration.solver_pulse_key_approach == 'avg_cost':
      qp = sum(self.infrastructures.construction_cost_factors) / len(self.infrastructures.construction_cost_factors)
      ip = sum(self.infrastructures.cost_factors) / len(self.infrastructures.cost_factors)
    else:
      indexes = range(len(self.infrastructures.cost_factors))
      utility_fn = lambda i: self.infrastructures.cost_factors[i] / self.infrastructures.construction_cost_factors[i]

      if configuration.solver_pulse_key_approach == 'avg_utility':
        index = sorted(indexes, key=utility_fn)[int(len(indexes) / 2)]
      else:
        fun = max if configuration.solver_pulse_key_approach == 'max_utility' else min
        index = fun(indexes, key=utility_fn)

      qp = self.infrastructures.cost_factors[index]
      ip = self.infrastructures.construction_cost_factors[index]

    return qp, ip

  @cached_property
  def agg_cost_factor(self):
    """
    Returns cost factor, used to estimate projected cost of pulse
    """

  @cached_property
  def min_infra_cost(self):
    """
    Returns minimun infra cost
    """
    return min(self.infrastructures.cost_factors)
