from os import path
import logging

import networkx as nx

from proj.solver import solve, export
from proj.config import configuration
from proj.timer import timed

logging.basicConfig(
  level=logging.DEBUG,
  format='%(asctime)-15s %(message)s'
)

def run_comparison():
  configuration.arc_weight_key = 'weight'
  configuration.max_iter = 1
  configuration.pulse_primal_bound_factor = 0.95

  file_path_prefix = path.join(path.dirname(__file__), '..', 'data/mdeo_med')
  graph = nx.read_yaml(f'{file_path_prefix}.yml')

  infrastructures = {
    'cost_factors': [0.9, 0.5, 0.4],
    'construction_cost_factors': [1, 4, 8],
  }

  demand = {
    ('14880', '87'): 500,
    ('6933', '16825'): 50,
    ('6988', '11437'): 100,
    ('16108', '6987'): 350,
  }
  budget = 15000

  timed_export = timed('Export to mathprog')(export)
  with open(f'{file_path_prefix}.dat', 'w') as data_file:
    timed_export(data_file, graph, infrastructures, demand, budget)

  timed_solve = timed('Main problem solve')(solve)
  timed_solve(graph, infrastructures, demand, budget)

