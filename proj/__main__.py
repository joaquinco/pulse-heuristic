import argparse
import logging
import pprint as pp
import sys

from proj.solver import solve, export
from proj.inputfile import parse_config_file
from proj.config import update_configuration, configuration


def parse_args(argv):
  parser = argparse.ArgumentParser()
  parser.add_argument('config_file')
  parser.add_argument('-l', '--log-level', choices=['debug', 'info', 'error'], default='debug')
  parser.add_argument('-a', '--action', choices=['solve', 'export'], default='solve')

  return parser.parse_args(argv)


def main():
  args = parse_args(sys.argv[1:])

  logging.basicConfig(
    level=getattr(logging, args.log_level.upper()),
    format='%(asctime)-15s %(message)s'
  )

  data = parse_config_file(args.config_file)
  update_configuration(**data.config)

  arguments = [data.graph, data.infrastructures, data.demand, data.budget]

  if args.action in ['export']:
    export(sys.stdout, *arguments)
  else:
    logging.info(
      f"""\n
  Running params:
  input: {args.config_file}
  demand: \n{pp.pformat(data.demand, indent=4)}
  infras: \n{pp.pformat(data.infrastructures, indent=5)}
  budget: {data.budget}
  nodes: {data.graph.number_of_nodes()}
  edges: {data.graph.number_of_edges()}
  config: \n{pp.pformat(configuration, indent=4)}
      """
    )
    solution = solve(*arguments)
    solution.print()


main()
