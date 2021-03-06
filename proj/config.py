from .context import Context

defaults = dict(
  # If use astar heuristic to compute objective function
  use_astar_heuristic=True,
  # Key to use as location information on each node for node distance computation
  node_location_key='pos',
  # arc weigth key
  arc_weight_key='weight',
  # construction arc cost key
  arc_cost_key='construction_cost',
  # Constant factor to multiply cost, which is also multiplied by edge weight
  construction_coefficient=1,
  # How to calculate od pair budget, based on demand ('demand'), based on path length ('path_length'), or base on both ('both').
  budget_assignment_approach='demand',
  # Factor of euclidean distance to be used as heuristic function
  astar_heuristic_factor=1,
  # Multiply factor of best cost path on base graph, from which pulse algorithm will yield paths
  pulse_primal_bound_factor=1,
  # On each Pulse iteration, ignore adjacents whose cost_bound is higher that current node.
  pulse_discard_faraway_nodes=False,
  # Difference from which to discard faraway nodes
  pulse_discard_faraway_delta=0,
  # Pulse queue key es computed as cost_bound(node) * pulse_queue_key_factor + pulse_current_cost
  pulse_queue_key_factor=1,
  # If pulse returns the best pulse, or just the first found. Note that how good is the first found approach can be tunned with pulse_primal_bound_factor.
  pulse_return_best=False,
  # Number of times to run the recursive search
  max_iter=10,
  # Per od paths to consider, each recursive search will generate at most solutions_per_od ** od_count paths
  solutions_per_od=1,
  # Per od budget modifier. Each od will be restricted by a fraction of the total budget
  # relative to its demand, if than number is P, then the od budget will be:
  # od_budget_factor * P + od_budget_epsilon
  od_budget_factor=1,
  od_budget_epsilon=0,
  # Minimum raw infrastructure length, except for base infrastructure
  # TODO: minimum_infra_length=3,
  # Random initializer seed
  seed=129,
)

class Config(Context):
  def __init__(self, **kwargs):
    super().__init__(**{**defaults, **kwargs})


configuration = Config()


def update_configuration(**kwargs):
  global configuration

  configuration.update(**kwargs)
