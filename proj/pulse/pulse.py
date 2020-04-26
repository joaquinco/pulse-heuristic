
class Pulse(object):
  def __init__(self, node, weights):
    self.node = node
    self.weights = dict(weights)
    self.prev_pulse = None

  def dominates(self, other_pulse):
    """
    Returns True if self dominates other_pulse
    """
    keys = self.weights.keys()
    to_compare = zip(
        [self.weights[k] for k in keys],
        [other_pulse.weights[k] for k in keys]
    )
    
    # self is strictly better, or it's no better no worse
    return all(map(lambda x: x[0] <= x[1], to_compare)) or \
           not (any(map(lambda x: x[0] > x[1], to_compare)) and \
           any(map(lambda x: x[0] < x[1], to_compare)))

  @classmethod
  def from_pulse(cls, pulse, node, weights):
    ret = Pulse(node, {})
    ret.prev_pulse = pulse

    for key, value in weights.items():
      ret.weights = pulse.weights[key] + value

    return ret
