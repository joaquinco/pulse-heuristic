import unittest

from proj.sorted import BinaryTree

class TestAVL(unittest.TestCase):
  def setUp(self):
    self.instance = BinaryTree()

  def test_add(self):
    self.instance.add(42)

    self.assertEqual(len(self.instance), 1)

  def test_pop(self):
    self.instance.add(42)
    elem = self.instance.pop()

    self.assertFalse(self.instance)
    self.assertEqual(elem, 42)

  def test_order(self):
    elements = [10, 20, 4, 5, 30, 110, 1]
    sorted_elements = sorted(elements)

    self.instance.add(*elements)

    for i in range(len(elements)):
      self.assertEqual(sorted_elements[i], self.instance.pop())


