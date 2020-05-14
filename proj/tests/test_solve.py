import unittest
from proj import solve
from proj.solver import export
from proj.solver.graph import construct_multigraph
from proj.config import configuration
from proj.constants import infinite
from .graph_helper import get_simple_graph


class SolveTestCase(unittest.TestCase):
  def setUp(self):
    self.graph = get_simple_graph()
    self.infras = {
      'cost_factors': [0.9, 0.5, 0.4],
      'construction_cost_factors': [1, 4, 8],
    }

    self.demand = {
      ('s', 't'):  100,
      ('s', '5'): 50,
      ('2', '4'): 50,
    }
    self.budget = 30

    configuration.arc_weight_key = 'cost'
    configuration.max_iter = 1
    configuration.pulse_primal_bound_factor = 0.95

  def test_create_multigraph(self):
    graph = construct_multigraph(self.graph, self.infras)

    self.assertTrue(graph.is_multigraph())

    for _, _, cost in graph.edges.data('cost'):
      self.assertIsNotNone(cost)
      self.assertGreater(cost, 0)

    for _, _, construction_cost in graph.edges.data('construction_cost'):
      self.assertIsNotNone(construction_cost)
      self.assertGreaterEqual(construction_cost, 0)

  def test_solve_basic(self):
    solution = solve(self.graph, self.infras, self.demand, self.budget)

    self.assertIsNotNone(solution)
    self.assertLess(solution.value, infinite)

  def test_export_basic(self):
    data_path = '/tmp/proj_solve_data.dat'
    with open(data_path, 'w') as output:
      export(output, self.graph, self.infras, self.demand, self.budget)

    with open(data_path, 'r') as input:
      data = input.read()

    self.assertTrue(data)
    self.assertGreater(len(data), 1500)
