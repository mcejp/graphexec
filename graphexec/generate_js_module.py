from dataclasses import dataclass
from os import getcwd
from pathlib import Path
import sys
from typing import Any, Dict, Optional

import jinja2
from pydantic import BaseModel
import yaml

from .node_type import collect_node_types


@dataclass
class PropertyModel:
    default_value: Any
    widget_type: Optional[str]
    label: Optional[str]
    additional_options: dict

    def __init__(self, value, widget_type=None, label=None, **kwargs):
        self.default_value = value
        self.widget_type = widget_type
        self.label = label
        self.additional_options = kwargs

    def format_additional_options_js(self) -> str:
        if self.additional_options is None:
            return ""

        return ", ".join(
            f"{name}: {value}" for name, value in self.additional_options.items()
        )

    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if isinstance(v, dict):
            return PropertyModel(**v)
        elif isinstance(v, float) or isinstance(v, int):
            return PropertyModel(value=v)
        else:
            raise TypeError("number or dict required")


class NodeTypeModel(BaseModel):
    label: str
    inputs: Dict[str, str] = {}
    outputs: Dict[str, str] = {}
    properties: Dict[str, PropertyModel] = {}
    feedback_type: Optional[str] = None


def main():
    from argparse import ArgumentParser

    parser = ArgumentParser()
    parser.add_argument("module")
    parser.add_argument("-o", dest="output_path", type=Path, required=True)
    args = parser.parse_args()

    sys.path.insert(0, getcwd())
    node_types = collect_node_types([args.module])

    node_type_models = {}

    for name, function in node_types.items():
        if function.__doc__ is None:
            print(f"Warning: no doc for node type {name}", file=sys.stderr)
        else:
            node_type_models[name] = NodeTypeModel(**yaml.safe_load(function.__doc__))

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
