import networkx as nx

serializable_types = [int, float, bool, str]

def _is_serializable(value):
  if isinstance(value, list):
    return all(map(_is_serializable, value))
  
  return any(map(lambda t: isinstance(value, t), serializable_types))

def as_serializable(graph):
  """
  Return an osm graph but just including serializable attributes.
  """
  ret = graph.copy()

  for n in ret.nodes():
    for k, v in list(ret.nodes[n].items()):
      if not _is_serializable(v):
        del ret.nodes[n][k]

  if ret.is_multigraph():
    edges = ret.edges(keys=True)
  else:
    edges = ret.edges()

  for e in edges:
    for k, v in list(ret.edges[e].items()):
      if not _is_serializable(v):
        del ret.edges[e][k]

  return ret


def normalize_osm(g):
  """
  Put coordinates x, y into pos attribute for each node.
  Transform node ids to string
  """
  nodes = list(g.nodes())
  for node in nodes:
    data = g.nodes[node]
    g.nodes[node]['pos'] = [data['x'], data['y']]

  mapping = { n:str(n) for n in nodes }

  return nx.relabel_nodes(g, mapping)
