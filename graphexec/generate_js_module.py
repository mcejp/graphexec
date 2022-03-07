from os import getcwd
from pathlib import Path
import sys

import jinja2

from .node_type import collect_node_types


def main():
    from argparse import ArgumentParser

    parser = ArgumentParser()
    parser.add_argument("module")
    parser.add_argument("-o", dest="output_path", type=Path, required=True)
    args = parser.parse_args()

    sys.path.insert(0, getcwd())
    node_types = collect_node_types([args.module], include_builtins=False)

    node_type_models = {}

    for name, function in node_types.items():
        if hasattr(function, "_node_type_model"):
            node_type_models[name] = function._node_type_model
        else:
            print(f"Warning: no doc for node type {name}", file=sys.stderr)

    env = jinja2.Environment(
        loader=jinja2.FileSystemLoader(Path(__file__).parent / "templates"),
        trim_blocks=True,
        lstrip_blocks=True,
    )

    template = env.get_template("node_types.js")

    with open(args.output_path, "wt") as f:
        f.write(template.render(node_types=node_type_models, source_module=args.module))


if __name__ == "__main__":
    main()
