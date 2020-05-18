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


def _find_lower(node):
  """
  Returns lower valued node, the most on the left
  """
  if not node:
    return None

  current = node
  while current.left:
    current = current.left

  return current


def _insert_node(root, node):
  """
  Iterative inserts a node in the tree
  """
  curr = root

  while True:
    if node.key <= curr.key:
      if curr.left:
        curr = curr.left
        continue
      curr.left = node
    else:
      if curr.right:
        curr = curr.right
        continue
      curr.right = node

    node.parent = curr
    break

class Node(object):
  def __init__(self, elem, key, left=None, right=None):
    self.elem = elem
    self.key = key
    self.left = left
    self.right = right
    self.parent = None
  
  def remove(self):
    if self.left:
      raise Exception('Can\'t remove intermediate element')

    ret = None

    if self.right:
      ret = self.right
      if self.parent:
        self.parent.left = self.right
        self.right.parent = self.parent
      else:
        self.right.parent = None
    elif self.parent:
      ret = self.parent
      self.parent.left = None

    self.parent = None
    self.right = None
    self.elem = None
    self.key = None

    return ret

  def __repr__(self):
    return f'<Node key={self.key} elem={self.elem}>'

  def print(self, depth):
    padding = ' ' * depth
    print(padding, self)
    if self.left:
      print(padding, 'Left')
      self.left.print(depth + 1)
    if self.right:
      print(padding, 'Right')
      self.right.print(depth + 1)

class BinaryTree(object):
  def __init__(self, iterable=None, key=None):
    self.root = None
    self.first = None
    self.length = 0
    self.get_key = partial(_get_key, key)

    for elem in iterable or []:
      self.add(elem)

  def add(self, *args):
    for elem in args:
      self._add_elem(elem)
  
  def _add_elem(self, elem):
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

    _insert_node(self.root, node)
    # TODO: Balance tree

    if node.key <= self.first.key:
      self.first = node

  def pop(self):
    """
    Pops the lower element from the tree
    """
    if not self.first:
      raise IndexError

    ret = self.first.elem

    reassign_root = self.root == self.first
    self.first = _find_lower(self.first.remove())

    if reassign_root:
      self.root = self.first

    self.length -= 1

    return ret

  def __len__(self):
    return self.length

  def __repr__(self):
    return f'<BinaryTree len={len(self)} first={self.first}>'

