from proj.cache import cached_property

class Solution(object):
  def __init__(self, value, modifications, shortest_paths=None):
    self.value = value
    self.modifications = dict(modifications)
    self.shortest_paths = shortest_paths

  @cached_property
  def budget_used(self):
    ac = 0
    for path in self.modifications.values():
      ac += sum(path.values())

    return ac

  def print(self):
    print(
      f"""
      Solution:
      {self.value}\n
      Budget used: {self.budget_used}
      Modifications:
      {self.modifications}
      Shortest Paths:
      {self.shortest_paths}
      """
    )
