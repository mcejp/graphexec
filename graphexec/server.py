import logging
from os import getcwd
from pathlib import Path
import sys
from typing import Any, Dict, List

from flask import Flask, redirect, request, send_from_directory

from .litegraph_processor import process_graph
from .node_type import collect_node_types


def create_app(node_types: List[Dict[str, Any]], www_root: Path):
    logger = logging.getLogger("graphexec")
    logger.addHandler(logging.StreamHandler())
    logger.level = logging.INFO

    # send_from_directory doesn't interpret paths relative to cwd
    www_root = www_root.absolute()

    app = Flask(__name__)

    @app.route("/")
    def index():
        return redirect("/editor/index.html")

    @app.route("/graph", methods=["POST"])
    def handle_graph():
        res = process_graph(request.get_data().decode(), node_types)
        return res

    @app.route("/<path:path>")
    def send_js(path):
        print("TEST", www_root, path)
        return send_from_directory(www_root, path)

    return app


def main():
    from argparse import ArgumentParser

    parser = ArgumentParser()
    parser.add_argument("-m", dest="modules", action="append", default=[])
    parser.add_argument("--wwwroot", type=Path, required=True)

    args = parser.parse_args()

    sys.path.insert(0, getcwd())
    node_types = collect_node_types(args.modules)

    app = create_app(node_types=node_types, www_root=args.wwwroot)
    app.run(debug=True)


if __name__ == "__main__":
    main()
