import networkx as nx


def get_simple_graph():
  """
  Returns a networkx.DiGraph
  """
  nodes = ['s', '1', '2', '3', '4', '5', 't']

  raw_arcs = {
      ('s', '1'): (5, 2, 90),
      ('s', '2'): (3, 3, 130),
      ('1', '2'): (3, 1, 90),
      ('1', '3'): (4, 2, 80),
      ('1', '4'): (1, 6, 120),
      ('2', '3'): (1, 1, 120),
      ('2', '5'): (3, 2, 110),
      ('3', '4'): (4, 3, 80),
      ('3', '5'): (3, 1, 140),
      ('4', '5'): (1, 4, 60),
      ('4', 't'): (2, 1, 80),
      ('5', 't'): (6, 2, 100),
  }

  arcs = {k: dict(cost=v[0], time=v[1], emission=v[2]) for k, v in raw_arcs.items()}

  graph = nx.DiGraph()
  graph.add_nodes_from(nodes)

  for edge, edge_data in arcs.items():
    graph.add_edge(*edge, **edge_data)

  return graph


def get_simple_multigraph():
  """
  Builds simple multigraph
  """
  g = nx.MultiDiGraph()

  g.add_nodes_from([1, 2, 3, 4])
  edges = {
    (1, 2): 2, (2, 3): 3, (3, 4): 3, (2, 4): 5,
  }

  infra_count = 4
  infra_factors = [1 / i for i in range(1, infra_count + 1)]

  for edge, weight in edges.items():
    for index in range(infra_count):
      n1, n2 = edge
      g.add_edge(n1, n2, cost=weight * infra_factors[index])

  return g
