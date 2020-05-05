import logging
import networkx as nx

from proj import configuration
from proj.context import Context
from proj.cache import cached_property
from proj.constants import infinite
from .solution import Solution
from .functions import astar_path_length

class SolverContext(Context):
  def __init__(self, graph, demand, infras, budget, **kwargs):
    self.graph = graph
    self.demand = demand
    self.infrastructures = infras
    self.budget = budget
    self.available_budget = budget
    self.best_objective = infinite
    self.best_solution = Solution(infinite, {})
    self.current_graph = None

    super().__init__(**kwargs)

  def recompute_objective(self):
    """
    Compute objective function:
    
    Find shortest path between every origin-destination pair and then multiply
    the each by demand amount.
    """
    ac = 0

    for od, demand_amount in self.demand.keys():
      ac += demand_amount * astar_path_length(self.current_graph, *od)

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

    for arc in zip(path[:-1], path[1:]):
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
      configuration.od_budget_factor * p + configuration.od_budget_epsilon,
      self.available_budget
    )
