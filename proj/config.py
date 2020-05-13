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
  # Factor of euclidean distance to be used as heuristic function
  astar_heuristic_factor=1,
  # Multiply factor of best cost path on base graph, from which pulse algorithm will yield paths
  pulse_primal_bound_factor=1,
  # On each Pulse iteration, ignore adjacents whose cost_bound is higher that current node.
  pulse_discard_faraway_nodes=True,
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
  # Random initial seed
  seed=129,
)

class Config(Context):
  def __init__(self, **kwargs):
    super().__init__(**{**defaults, **kwargs})


configuration = Config()


def recreate_configuration(**kwargs):
  global configuration

  configuration = Config(**kwargs)
