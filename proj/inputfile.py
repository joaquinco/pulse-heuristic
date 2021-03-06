import json

import networkx as nx
from proj.context import Context


def as_tuples_dict(data):
  """
  Parses a list of { source:, target:, value:} and return a dict
  of {(source,target): value, ...}
  """
  ret = {}
  for entry in data:
    key = (entry['source'], entry['target'])
    value = entry['value']
    ret[key] = value

  return ret


def parse_config_file(file_path):
  """
  config file is a json file with the following data:

  {
    graph: 'path/to/graph.yml',
    infrastructures: {
      cost_factors: [...],
      construction_cost_factors: [...],
      costs: [
        { source: ..., target: ..., value: ... },
        ...
      ],
      construction_costs: [
        { source: ..., target: ..., value: ... },
        ...
      ],
    },
    budget: ..,
    demand: [
      { source: ..., target: ..., value: ... },
      ...
    ],
    config: {
      ...configs key value
    }
  }
  """

  with open(file_path, 'r') as f:
    data = json.loads(f.read())

  graph = nx.read_yaml(data['graph'])
  infrastructures = data['infrastructures']

  for key in ['costs', 'construction_costs']:
    if key in infrastructures:
      infrastructures[key] = as_tuples_dict(infrastructures[key])

  budget = data['budget']

  demand = as_tuples_dict(data['demand'])

  config = data.get('config', {})

  return Context(
    graph=graph,
    demand=demand,
    infrastructures=infrastructures,
    budget=budget,
    config=config
  )
