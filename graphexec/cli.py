import logging
from pathlib import Path

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

    process_graph(args.path.read_text(), collect_node_types(args.modules))


if __name__ == "__main__":
    main()
