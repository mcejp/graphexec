import importlib
from typing import Any, Dict, List

from . import litegraph_builtins


def collect_node_types(module_names: List[str]) -> Dict[str, Any]:
    node_types = {} | litegraph_builtins.NODE_TYPES

    for module_name in module_names:
        module = importlib.import_module(module_name)
        additional_node_types = module.NODE_TYPES

        intersection = node_types.keys() & additional_node_types

        if len(intersection) != 0:
            raise Exception(
                f"Node name collision in module {module_name}: {', '.join(intersection)}"
            )

        node_types |= additional_node_types

    return node_types
