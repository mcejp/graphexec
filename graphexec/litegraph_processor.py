import graphlib
import json
import logging
import time
from typing import Dict

from .litegraph_model import Graph, GraphNode
from .model import Result


logger = logging.getLogger(__name__)


def evaluate_node(
    graph: Graph,
    node: GraphNode,
    node_results: Dict[int, Result],
    handlers,
) -> Result:
    try:
        handler = handlers[node.type]
    except KeyError:
        raise RuntimeError(f"Unknown node type '{node.type}'") from None

    kwargs = {**node.properties}

    # resolve inputs
    for input in node.inputs:
        if input.link is not None:
            # resolve link
            link = graph.links_by_id[input.link]
            node = graph.nodes_by_id[link.in_node_id]
            # node results are keyed by output name, but the link contains slot_id; need to resolve the output name
            output_name = node.outputs_by_slot_id[link.in_slot_id].name
            value = node_results[link.in_node_id].outputs[output_name]
            kwargs[input.name] = value
        else:
            # If unconnected, it may still be set via a property with a matching name.
            # (related discussion: https://github.com/jagenjo/litegraph.js/issues/278)
            #
            # Otherwise, the argument will remain unset.
            pass

    res = handler(**kwargs)

    if isinstance(res, dict):
        res = Result(outputs=res, extra_outputs={})
    else:
        assert isinstance(res, Result)

    return res


def process_graph(model: str, handlers) -> str:
    graph = Graph(**json.loads(model))

    # determine ordering of nodes so that output-input relationships can be satisfied
    graph_model = {}

    for node in graph.nodes:
        graph_model[node.id] = [
            graph.links_by_id[input.link].in_node_id
            for input in node.inputs
            if input.link is not None
        ]

    sorter = graphlib.TopologicalSorter(graph_model)
    order = list(sorter.static_order())

    # evaluate nodes in the determined order
    node_results: Dict[int, Result] = {}

    for node_id in order:
        node = graph.nodes_by_id[node_id]

        start = time.time()
        try:
            res = evaluate_node(graph, node, node_results, handlers)
        except Exception as ex:
            raise Exception(f"Error in evaluation of node: {str(node)}") from ex

        end = time.time()
        logger.info("%s: took %.2f secs", node, end - start)
        node_results[node.id] = res

    # extract additional outputs (e.g., visual preview)
    return_dict = dict(
        nodes={
            node_id: dict(extraOutputs=res.extra_outputs)
            for node_id, res in node_results.items()
        }
    )

    return json.dumps(return_dict)
