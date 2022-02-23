from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, Optional
import jinja2
from pydantic import BaseModel

import yaml


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
    parser.add_argument("path", type=Path)
    parser.add_argument("-o", dest="output_path", type=Path, required=True)
    args = parser.parse_args()

    env = jinja2.Environment(
        loader=jinja2.FileSystemLoader(Path(__file__).parent / "templates"),
        trim_blocks=True,
        lstrip_blocks=True,
    )

    template = env.get_template("node_types.js")

    with open(args.path, "rt") as f:
        model = yaml.safe_load(f)
        node_types = {
            name: NodeTypeModel(**node_type_model)
            for name, node_type_model in model.items()
        }

    print(node_types)

    with open(args.output_path, "wt") as f:
        f.write(template.render(node_types=node_types))


if __name__ == "__main__":
    main()
