import math

def plane_distance(g, n1, n2):
  x, y = g.nodes[n1]['pos']
  x1, y1 = g.nodes[n2]['pos']

  return math.sqrt(
    (x - x1) ** 2 + (y - y1) ** 2
  )
