from proj.cache import cached_property

class Solution(object):
  def __init__(self, value, paths):
    self.value = value
    self.paths = dict(paths)

  @cached_property
  def budget_used(self):
    ac = 0
    for path in self.paths.values():
      ac += sum(path.values())

    return ac

  def print(self):
    print(
      f"""
      Solution:
      {self.value}\n
      Budget used: {self.budget_used}
      Paths:
      {self.paths}
      """
    )
