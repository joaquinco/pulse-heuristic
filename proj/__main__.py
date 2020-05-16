import argparse
import logging
import sys

from proj.solver import solve, export
from proj.inputfile import parse_config_file
from proj.config import recreate_configuration


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
  recreate_configuration(**data.config)

  arguments = [data.graph, data.infrastructures, data.demand, data.budget]
  print(data.graph)
  if args.action in ['export']:
    export(sys.stdout, *arguments)
  else:
    logging.info(
      f"""\n
      Running params:
      input: {args.config_file}
      demand: {data.demand}
      budget: {data.budget}
      nodes: {data.graph.number_of_nodes()}
      edges: {data.graph.number_of_edges()}
      """
    )
    solve(*arguments)


main()
