import sys
from functools import partial

import networkx as nx
from .solver_context import SolverContext
from proj.config import configuration


def write(output, value='', line_break=True):
  output.write(value)
  if line_break:
    output.write('\n')


def fl(values, sep=' '):
  return sep.join(values)


def edge_name(e):
  return ''.join(e)


def export(output, graph, infrastructures, demand, budget):
  """
  Export the solver data in mathprog data format.
  """
  w = partial(write, output)
  w('data;\n')

  ctx = SolverContext(graph, infrastructures, demand, budget)
  reverse_graph = nx.reverse_view(graph)

  nodes = graph.nodes()
  edges = list(map(edge_name, graph.edges()))
  w(f'set nodes := {fl(nodes)};')
  w(f'set edges := {fl(edges)};')
  w()

  for n in nodes:
    adjs = reverse_graph.adj[n]
    adj_edges = map(edge_name, [(a, n) for a in adjs])
    val = fl(adj_edges) if adjs else '{}'
    w(f'set inbound[{n}] := {val};')
  w()
  
  for n in nodes:
    adjs = graph.adj[n]
    adj_edges = map(edge_name, [(n, a) for a in adjs])
    val = fl(adj_edges) if adjs else '{}'
    w(f'set outbound[{n}] := {val};')
  w()
  
  infras_count = len(infrastructures.get('cost_factors')) + 1
  w(f'set infras := {fl(map(str, range(infras_count)))};')
  w()

  ods = fl([f'({o}, {d})' for o, d in demand.keys()])
  w(f'set ods := {ods};')
  w()

  w(f'param demand := ', line_break=False)
  for od, value in demand.items():
    o, d = od
    w()
    w(f'  [{o}, {d}] {value}', line_break=False)
  w(';\n')

  w(f'param budget := {budget};')

  w(f'param weights :=', line_break=False)
  for edge in ctx.current_graph.edges(keys=True):
    n1, n2, infra = edge
    weight = ctx.current_graph.edges[edge][configuration.arc_weight_key]
    w()
    w(f'  [{edge_name([n1, n2])}, {infra}] {weight}', line_break=False)
  w(';\n')

  w(f'param construction_cost :=', line_break=False)
  for edge in ctx.current_graph.edges(keys=True):
    n1, n2, infra = edge
    construction_cost = ctx.current_graph.edges[edge][configuration.arc_cost_key]
    w()
    w(f'  [{edge_name([n1, n2])}, {infra}] {construction_cost}', line_break=False)
  w(';\n')

  w('end;')
