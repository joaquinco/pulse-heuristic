from functools import partial
import math
import networkx as nx
from proj.networkx import astar_path as proj_astar_path
from proj import configuration
from proj.geo import plane_distance

def astar_heuristic(graph, u, v):
  """
  Heuristic is the euclidean distance between nodes
  """
  return configuration.astar_heuristic_factor * plane_distance(
    graph, u, v, key=configuration.node_location_key
  )


def get_heuristic(graph):
  """
  Returns the astar heuristic function if enabled
  """
  if configuration.use_astar_heuristic:
    return partial(astar_heuristic, graph)
  return None


def astar_path(graph, source, target, weight):
  return proj_astar_path(
    graph, source, target, heuristic=get_heuristic(graph), weight=weight
  )


def astar_path_length(graph, source, target, weight):
  _, length = astar_path(
    graph, source, target, weight,
  )

  return length


def get_zero_weight_subgraph(graph, cost_weight):
  """
  Return view of graph with edges whose cost is zero
  """
  def filter_edge(n1, n2, k):
    return graph.edges[n1, n2, k][cost_weight] == 0

  return nx.subgraph_view(graph, filter_edge=filter_edge)


def normalize(arr):
  """
  Normalizes array values to 1
  """

  total = sum(arr)

  return list(map(lambda x: x / total, arr))
