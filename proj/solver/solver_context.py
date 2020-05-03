from proj.context import Context
from .functions import astar_path_length


class SolverContext(Context):
  def __init__(self, graph, demand, infras, budget, **kwargs):
    self.graph = graph
    self.demand = demand
    self.infrastructures = infras
    self.budget = budget
    self.best_objective = None
    self.best_solution = None
    self.current_objective = None
    self.current_graph = None

    super().__init__(**kwargs)

  def compute_objective(self):
    """
    Compute objective function:
    
    Find shortest path between every origin-destination pair and then multiply
    the each by demand amount.
    """
    ac = 0

    for od, demand_amount in self.demand.keys():
      ac += demand_amount * astar_path_length(self.current_graph, *od)

    self.current_objective = ac

    return ac




