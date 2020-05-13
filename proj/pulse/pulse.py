
class Pulse(object):
  def __init__(self, node, weights, edge=None):
    self.edge = edge
    self.node = node
    self.weights = dict(weights)
    self.prev_path = []
    self.dominated = False

  def dominates(self, other_pulse):
    """
    Returns True if self dominates other_pulse
    """
    has_strict_lt = False

    for k, v in self.weights.items():
      other = other_pulse.weights[k]
      if v > other:
        return False

      has_strict_lt = v < other
    
    return has_strict_lt

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
    return f'<Pulse node={self.node} len={len(self.prev_path)} weights={self.weights}>'
