

class Solution(object):
  def __init__(self, value, paths):
    self.value = value
    self.paths = dict(paths)

  def print(self):
    print(
      f"""
      Solution:
      {self.value}\n
      Paths:
      {self.paths}
      """
    )
