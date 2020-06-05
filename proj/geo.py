import math


def normalize_osm(g):
  """
  Put coordinates x, y into pos attribute for each node.
  """
  for node in g.nodes():
    data = g.nodes[node]
    g.nodes[node]['pos'] = (data['x'], data['y'])

  return g


def plane_distance(g, n1, n2):
  x, y = g.nodes[n1]['pos']
  x1, y1 = g.nodes[n2]['pos']

  return math.sqrt(
    (x - x1) ** 2 + (y - y1) ** 2
  )
