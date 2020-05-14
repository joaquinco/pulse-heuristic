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

@timed('Mdeo Large')
def run_comparison_med():
  configuration.arc_weight_key = 'weight'
  configuration.max_iter = 1
  configuration.pulse_primal_bound_factor = 1

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

  logging.info(
    f"""\n
    Running params:
    demand: {demand}
    budget: {budget}
    graph_file: {file_path_prefix}
    """
  )

  with open(f'{file_path_prefix}.dat', 'w') as data_file:
    export(data_file, graph, infrastructures, demand, budget)

  solution = solve(graph, infrastructures, demand, budget)
  solution.print()


@timed('Mdeo Large')
def run_comparison_large():
  configuration.arc_weight_key = 'weight'
  configuration.max_iter = 1
  configuration.pulse_primal_bound_factor = 1

  file_path_prefix = path.join(path.dirname(__file__), '..', 'data/mdeo_large')
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

  logging.info(
    f"""\n
    Running params:
    demand: {demand}
    budget: {budget}
    graph_file: {file_path_prefix}
    """
  )

  with open(f'{file_path_prefix}.dat', 'w') as data_file:
    export(data_file, graph, infrastructures, demand, budget)

  solution = solve(graph, infrastructures, demand, budget)
  solution.print()


def run_comparison():
  run_comparison_large()
