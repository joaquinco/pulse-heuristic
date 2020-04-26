

class Context(dict):
  def __getattribute__(self, name):
    return self.get(name, None)

