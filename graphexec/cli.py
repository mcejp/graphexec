import logging
from os import getcwd
from pathlib import Path
import sys

from graphexec.node_type import collect_node_types

from .litegraph_processor import process_graph


def main():
    from argparse import ArgumentParser

    parser = ArgumentParser()
    parser.add_argument("path", type=Path)
    parser.add_argument("-m", dest="modules", action="append", default=[])
    parser.add_argument("-v", dest="verbose", action="store_true")

    args = parser.parse_args()

    logging.basicConfig(level=logging.INFO if args.verbose else logging.WARNING)

    sys.path.insert(0, getcwd())
    process_graph(args.path.read_text(), collect_node_types(args.modules, include_builtins=True))


if __name__ == "__main__":
    main()
