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
    ('15384', '6763'): 500,
    ('1160', '103'): 50,
    ('15384', '16611'): 100,
    ('15507', '6428'): 150,
    ('15384', '15507'): 300,
  }

  budget = 15000

  timed_solve = timed(solve)

  timed_solve(graph, infrastructures, demand, budget)

  with open(f'{file_path_prefix}.dat', 'w') as data_file:
    export(data_file, graph, infrastructures, demand, budget)
