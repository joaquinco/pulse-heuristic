from functools import partial

def _get_key(key, elem):
  """
  Return the sorting key of elem
  """
  if key is None:
    return elem

  if isinstance(key, str):
    return getattr(elem, key)
  
  if hasattr(key, '__call__'):
    return key(elem)


class Node(object):
  def __init__(self, elem, key, left=None, right=None):
    self.elem = elem
    self.key = key
    self.left = left
    self.right = right
    self.parent = None

  def insert(self, node):
    if self.key <= node.key:
      if self.left:
        return self.left.insert(node)
      self.left = node
      node.parent = self
    else:
      if self.right:
        return self.right.insert(node)
      self.right = node
      node.parent = self
  
  def remove(self):
    if self.left:
      raise Exception('Can\'t remove intermediate element')

    if self.right:
      self.parent.left = self.right

    self.parent = None
    self.right = None
    self.elem = None
    self.key = None


class BinaryTree(object):
  def __init__(self, iterable, key=None):
    self.root = None
    self.first = None
    self.length = 0
    self.get_key = partial(_get_key, key)

    for elem in iterable:
      self.add(elem)

  def add(self, elem):
    node = Node(elem, self.get_key(elem))
    self._perform_insertion(node)
    self.length += 1

  def _perform_insertion(self, node):
    """
    Perform sorted insertion of node in the sorted tree.
    """

    if not self.root:
      self.root = node
      self.first = node
      return

    self.root.insert(node)
    # TODO: Balance tree

    if node.key <= self.first.key:
      self.first = node

    return self

  def pop(self):
    """
    Pops the lower element from the tree
    """
    ret = self.first.elem

    if self.root == self.first:
      self.root = None
      self.first = None
    else:
      self.first.remove()

    self.length -= 1

    return ret

  def __len__(self):
    return self.length




