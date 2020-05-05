

class cached_property(object):
  def __init__(self, fn):
    self.fn = fn

  def __call__(self):
    ret = self.fn()
    setattr(self, self.fn.__name__, ret)

    return ret
