import networkx as nx
from proj.config import configuration

from proj.context import Context


def construct_multigraph(graph, infrastructures):
  """
  Given a simple graph and infrastructures information, constructs a multigraph
  that includes the merged information.
  """
  infras = InfrastructureContext(**infrastructures)

  ret = nx.MultiDiGraph()
  
  # Add base graph nodes and edges
  ret.add_nodes_from(graph.nodes())
  ret.add_edges_from(graph.edges(), **{
    configuration.arc_cost_key: 0
  })

  for infra_index in range(len(infras.cost_factors)):
    for edge in graph.edges():
      n1, n2 = edge
      data = graph.edges[edge]
      ret.add_edge(
        n1, n2,
        **data,
        **infras.get_edge_weights(infra_index, edge, data)
      )
  
  return ret


class InfrastructureContext(Context):
  def __init__(self, **kwargs):
    super().__init__(self, **kwargs)
    self._validate()

  def get_edge_weights(self, infra, edge, edge_attrs):
    if edge in self.costs:
      cost = self.costs.get(edge)
    else:
      cost = edge_attrs[configuration.arc_weight_key] * self.cost_factors[infra]

    if edge in self.construction_costs:
      construction_cost = self.construction_costs.get(edge)
    else:
      construction_cost = edge_attrs[configuration.arc_cost_key] * self.construction_cost_factors[infra]
    
    return {
      configuration.arc_weight_key: cost,
      configuration.arc_cost_key: construction_cost,
    }

  def _validate(self):
    """
    Dictionary with information about costs and construction costs:
    For example, for three infrastructures, without the base:
    {
      cost_factors: [x1, x2, x3],
      construction_cost_factors: [y1, y2, y3],
      costs: [ # One dict per infrastructure
        { (n1, n2): 123, (n4, n3): 12312 },
        {},
        {},
      ],
      construction_costs: [
        ...
        same format as costs
        ...
      ],
    }
    """
    infras = self

    infra_keys = ['cost_factors', 'construction_cost_factors', 'costs', 'construction_costs']

    for key in infra_keys:
      value = infras.get('key')
      if not value:
        raise Exception(f'Missing infrastructures {key}')
      
    for key in infra_keys[:2]:
      if not isinstance(value, list):
        raise Exception(f'{key} must be an list')

    if len(infras.cost_factors) != len(infras.construction_cost_factors):
      raise Exception('cost_factors and construction_cost_factors have different length')

    for key in infra_keys[2:]:
      value = infras.get(key)

      if value and not isinstance(value, list):
        raise Exception(f'{key} must be an list')

      if any(map(lambda x: not isinstance(x, dict)), value):
        raise Exception(f'{key} must be an list of dicts')
