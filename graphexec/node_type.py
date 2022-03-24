import importlib
import logging
import sys
from typing import Any, Callable, Dict, List, Sequence

from graphexec.model import NodeTypeModel, PropertyModel


logger = logging.getLogger(__name__)


def collect_node_types(module_names: List[str], *, discover_installed: bool) -> Dict[str, Any]:
    def dictify(funcs: Sequence[Callable]):
        return {func._node_type_model.type_name: func for func in funcs}

    node_types = {}

    if discover_installed:
        if sys.version_info < (3, 10):
            from importlib_metadata import entry_points
        else:
            # We *must not* attempt this pre-3.10, as the built-in package has an incompatible API
            from importlib.metadata import entry_points

        discovered = entry_points(group="graphexec.node_types")

        for entry_point in discovered:
            logger.debug("Discovered %s", entry_point)
            module = entry_point.load()
            additional_node_types = dictify(module.NODE_TYPES)

            intersection = node_types.keys() & additional_node_types

            if len(intersection) != 0:
                raise Exception(
                    f"Node name collision in module {module_name}: {', '.join(intersection)}"
                )

            node_types |= additional_node_types

    for module_name in module_names:
        module = importlib.import_module(module_name)
        additional_node_types = dictify(module.NODE_TYPES)

        intersection = node_types.keys() & additional_node_types

        if len(intersection) != 0:
            raise Exception(
                f"Node name collision in module {module_name}: {', '.join(intersection)}"
            )

        node_types |= additional_node_types

    return node_types


def _get_model(func) -> NodeTypeModel:
    if not hasattr(func, "_node_type_model"):
        func._node_type_model = NodeTypeModel(
            type_name="UNKNOWN", label="Unknown", inputs={}, outputs={}, properties={}
        )

    return func._node_type_model


def define(type_name, label, **kwargs):
    def wrap(func):
        m = _get_model(func)
        m.type_name = type_name
        m.label = label
        for attr, value in kwargs.items():
            setattr(m, attr, value)
        return func

    return wrap


def input(name: str, type_name: str):
    def wrap(func):
        m = _get_model(func)
        assert name not in m.inputs
        m.inputs = {name: type_name} | m.inputs  # slow?
        return func

    return wrap


def output(name: str, type_name: str):
    def wrap(func):
        m = _get_model(func)
        assert name not in m.outputs
        m.outputs = {name: type_name} | m.outputs  # slow?
        return func

    return wrap


def property(name: str, default_value, **kwargs):
    def wrap(func):
        m = _get_model(func)
        assert name not in m.outputs
        m.properties = {
            name: PropertyModel(**kwargs, default_value=default_value)
        } | m.properties  # slow?
        return func

    return wrap
