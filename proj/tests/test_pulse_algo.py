import unittest
from functools import partial

from proj.pulse import pulse
from proj.tests.graph_helper import get_simple_graph

class TestPulseAlgorithm(unittest.TestCase):
  def setUp(self):
    self.graph = get_simple_graph()
    self.constraints = dict(time=9, emission=330)
    self.source = 's'
    self.target = 't'

  def get_pulse_generator(self):
    return pulse(
      self.graph, self.source, self.target,
      weight='cost', constraints=self.constraints, primal_bound=20,
    )

  def test_runs_ok(self):
    exception = None

    try:
      next(self.get_pulse_generator())
    except Exception as e:
      exception = e
    
    self.assertIsNone(exception)

  def test_yields_path(self):
    pulse_gen = self.get_pulse_generator()

    path, _ = next(pulse_gen)

    self.assertTrue(path)
    self.assertGreater(len(path), 1)

  def test_all_results_found(self):
    results = [r for r in self.get_pulse_generator()]

    # 2 is the known number of paths from s to t
    self.assertEqual(len(results), 2)
