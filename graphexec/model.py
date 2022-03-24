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


@dataclass
class NodeTypeModel:
    type_name: str
    label: str
    inputs: Dict[str, str]
    outputs: Dict[str, str]
    properties: Dict[str, PropertyModel]
    feedback_type: Optional[str] = None
