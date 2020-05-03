from functools import partial
import math
import networkx as nx
from proj import configuration


def astar_heuristic(graph, u, v):
  """
  Heuristic is the euclidean distance between nodes
  """
  x1, y1 = graph.nodes[u][configuration.node_location_key]
  x2, y2 = graph.nodes[v][configuration.node_location_key]

  return configuration.astar_heuristic_factor * math.sqrt(
    (x1 - x2) ** 2 + (y1 - y2) ** 2
  )


def get_heuristic(graph):
  """
  Returns the astar heuristic function if enabled
  """
  if configuration.astar_heuristic_enabled:
    return partial(astar_heuristic, graph)
  return None


def astar_path_length(graph, source, target):
  return nx.astar_path_length(graph, source, target, heuristic=get_heuristic(graph))
