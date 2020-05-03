from .context import Context

defaults = dict(
  # If use astar heuristic to compute objective function
  use_astar_heuristic=True,
  # Key to use as location information on each node for node distance computation
  node_location_key='pos',
  # Factor of euclidean distance to be used as heuristic function
  astar_heuristic_factor=1,
  # Multiply factor of best cost path on base graph from which pulse algorithm will yield paths
  pulse_primal_bound_factor=1,
  # Number of times to run the recursive search
  max_iter=10,
  # Per od paths to consider, each recursive search will generate at most solutions_per_od ** od_count paths
  solutions_per_od=2,
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
