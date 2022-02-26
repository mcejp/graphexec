from dataclasses import dataclass
from typing import Any, Dict, Optional


@dataclass
class Result:
    outputs: Dict[str, Any]
    extra_outputs: Dict[str, Any]


@dataclass
class PropertyModel:
    default_value: Any
    widget_type: Optional[str]
    label: Optional[str]
    additional_options: dict

    def __init__(self, default_value, widget_type=None, label=None, **kwargs):
        self.default_value = default_value
        self.widget_type = widget_type
        self.label = label
        self.additional_options = kwargs

    def format_additional_options_js(self) -> str:
        if self.additional_options is None:
            return ""

        return ", ".join(
            f"{name}: {value}" for name, value in self.additional_options.items()
        )


@dataclass
class NodeTypeModel:
    label: str
    inputs: Dict[str, str]
    outputs: Dict[str, str]
    properties: Dict[str, PropertyModel]
    feedback_type: Optional[str] = None
