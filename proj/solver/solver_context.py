import logging
import networkx as nx

from proj import configuration
from proj.context import Context
from proj.cache import cached_property
from proj.constants import infinite
from .solution import Solution
from .functions import astar_path_length, get_zero_weight_subgraph
from .graph import construct_multigraph

class SolverContext(Context):
  def __init__(self, graph, infrastructures, demand, budget, **kwargs):
    self.graph = graph
    self.demand = demand
    self.infrastructures = infrastructures
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

    result_graph = get_zero_weight_subgraph(
      self.current_graph, configuration.arc_cost_key
    )

    for od, demand_amount in self.demand.items():
      ac += demand_amount * astar_path_length(
        result_graph, *od, configuration.arc_weight_key
      )

    if ac < self.best_solution.value:
      logging.debug('Best objective {}'.format(ac))

      self.best_solution = Solution(ac, self.modifications)

    return ac

  @cached_property
  def total_demand(self):
    return sum(self.demand.values())

  @cached_property
  def modifications(self):
    return { od: {} for od in self.odpairs }

  def apply_path(self, od, path):
    """
    Applies the path to the current_graph, meaning that its arcs won't have a
    construction cost
    """
    path_weights = {}

    logging.debug('Applying path {} from {}'.format(path, od))

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
    logging.debug('Disapplying path {} from {}'.format(path, od))

    for arc, infra_cost in self.modifications[od].items():
      self.available_budget += infra_cost
      self.current_graph.edges[arc][configuration.arc_cost_key] = infra_cost

    self.modifications[od] = {}

  def get_budget(self, od):
    """
    Returns the budget for a given od.
    """
    p = self.demand[od] / self.total_demand

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
      ret[od] = astar_path_length(self.graph, *od, configuration.arc_weight_key)

    return ret
