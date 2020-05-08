

class cached_property(object):
  def __init__(self, fn):
    self.fn = fn

  def __get__(self, instance, cls=None):
    ret = self.fn(instance)

    setattr(instance, self.fn.__name__, ret)

    return ret

