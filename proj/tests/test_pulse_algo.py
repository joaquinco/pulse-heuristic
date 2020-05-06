import unittest
from functools import partial

import networkx as nx

from proj.pulse import pulse
from proj.tests.graph_helper import get_simple_graph, get_simple_multigraph

class TestPulseAlgorithm(unittest.TestCase):
  def get_simple_pulse(self, **kwargs):
    graph = get_simple_graph()
    constraints = dict(time=9, emission=330)
    
    source = 's'
    target = 't'
    
    return pulse(
      graph, source, target,
      **{
        **dict(weight='cost', constraints=constraints, primal_bound=20),
        **kwargs,
      }
    )

  def get_multigraph_pulse(self, **kwargs):
    graph = get_simple_multigraph()

    source = 1
    target = 4
    
    return pulse(
      graph, source, target,
      **{
        **dict(weight='cost', constraints=None),
        **kwargs,
      }
    )

  def test_runs_ok(self):
    exception = None

    try:
      next(self.get_simple_pulse())
    except Exception as e:
      exception = e
    
    self.assertIsNone(exception)

  def test_yields_path(self):
    pulse_gen = self.get_simple_pulse()

    path, _ = next(pulse_gen)

    self.assertTrue(path)
    self.assertGreater(len(path), 1)

  def test_all_results_found(self):
    results = [r for r in self.get_simple_pulse()]

    # 2 is the known number of paths from s to t
    self.assertEqual(len(results), 2)

  def test_best_results_found(self):
    # 8 is the known shortest path cost and is satisfied by a single path
    results = [r for r in self.get_simple_pulse(primal_bound=8)]

    self.assertEqual(len(results), 1)

  def test_multigraph(self):
    self.graph = get_simple_multigraph()
    results = [r for r in self.get_multigraph_pulse()]

    self.assertGreater(len(results), 1)



