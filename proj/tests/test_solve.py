import unittest
from proj import solve
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

    configuration.arc_weight_key = 'cost'

  def test_create_multigraph(self):
    graph = construct_multigraph(self.graph, self.infras)

    self.assertTrue(graph.is_multigraph())

    for (n1, n2, cost) in graph.edges.data('cost'):
      self.assertIsNotNone(cost)
      self.assertGreaterEqual(cost, 0)

  def test_solve_basic(self):
    demand = {
      ('s', 't'):  100,
      ('s', '5'): 50,
      ('2', '5'): 50,
    }
    budget = 10

    solution = solve(self.graph, self.infras, demand, budget)

    self.assertIsNotNone(solution)
    self.assertLess(solution.value, infinite)
