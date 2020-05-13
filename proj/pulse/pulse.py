
class Pulse(object):
  def __init__(self, node, weights, edge=None):
    self.edge = edge
    self.node = node
    self.weights = dict(weights)
    self.prev_path = []

  def dominates(self, other_pulse):
    """
    Returns True if self dominates other_pulse
    """
    keys = self.weights.keys()
    to_compare = zip(
        [self.weights[k] for k in keys],
        [other_pulse.weights[k] for k in keys]
    )
    
    # all weights from self are greater or equal and there exists
    # one that is greater
    return all(map(lambda x: x[0] <= x[1], to_compare)) and \
           any(map(lambda x: x[0] < x[1], to_compare))

  def to_path(self):
    return self.prev_path[:]

  @classmethod
  def from_pulse(cls, pulse, node, weights, edge):
    ret = Pulse(node, {}, edge=edge)
    ret.prev_path = pulse.prev_path + [edge]

    for key, value in weights.items():
      ret.weights[key] = pulse.weights[key] + value

    return ret

  def __repr__(self):
    return f'<Pulse node={self.node} weights={self.weights}>'
