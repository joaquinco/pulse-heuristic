from proj.constants import infinite
from ..context import Context

class PulseContext(Context):
  def __init__(
        self,
        source=None,
        target=None,
        weight=None,
        constraints=None,
        resource_bounds=None,
        best_cost=None,
        cost_bound=None,
        **kwargs
      ):
    super().__init__(**kwargs)
    
    self.source = source
    self.target = target
    self.cost_weight = weight
    self.constraints = constraints
    self.resource_bounds = resource_bounds
    self.best_cost = best_cost or infinite
    self.best_cost_fixed = bool(best_cost)
    self.cost_bound = cost_bound
    self.pulses_by_node = {}

  def dissatisfies_constraints(self, pulse):
    """
    Returns if should prune by infeasibility
    """

    for name, value in self.constraints.items():
      if name == self.cost_weight:
        continue
      if pulse.weights[name] + self.resource_bounds[name][pulse.node] > value:
        return True
    
    return False

  def satisfies_cost(self, pulse):
    """
    Returns if pulse should not be pruned by cost bound
    """
    if self.cost_bound[pulse.node] + pulse.weights[self.cost_weight] > self.best_cost:
      return False
    
    return True

  def is_dominated(self, pulse):
    for other_pulse in self.pulses_by_node.get(pulse.node, []):
      if other_pulse.dominates(pulse):
        return True
    
    return False

  def save_pulse(self, pulse):
    node_pulses = self.pulses_by_node.get(pulse.node, set())

    to_remove = set()
    for other_pulse in node_pulses:
      if pulse.dominates(other_pulse):
        to_remove.add(other_pulse)

    node_pulses -= to_remove
    node_pulses.add(pulse)

    # Update best cost if needed
    is_target = self.target == pulse.node
    pulse_cost = pulse.weights[self.cost_weight]
    if is_target and pulse_cost < self.best_cost and not self.best_cost_fixed:
      self.best_cost = pulse_cost

    self.pulses_by_node[pulse.node] = node_pulses

