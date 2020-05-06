
class Pulse(object):
  def __init__(self, node, weights, edge=None):
    self.edge = edge
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
    
    # all weights from self are greater or equal and there exists
    # one that is greater
    return all(map(lambda x: x[0] <= x[1], to_compare)) and \
           any(map(lambda x: x[0] < x[1], to_compare))

  def to_path(self):
    curr = self
    path = []

    while curr:
      if curr.edge:
        path.append(curr.edge)
      curr = curr.prev_pulse

    path.reverse()

    return path

  @classmethod
  def from_pulse(cls, pulse, node, weights, edge=None):
    ret = Pulse(node, {}, edge=edge)
    ret.prev_pulse = pulse

    for key, value in weights.items():
      ret.weights[key] = pulse.weights[key] + value

    return ret

  def __repr__(self):
    return f'<Pulse node={self.node} weights={self.weights}>'
