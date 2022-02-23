from dataclasses import dataclass
from typing import List, Optional, Tuple, Dict

from pydantic import BaseModel


class GraphInput(BaseModel):
    name: str
    type: str
    link: Optional[int]  # null if unconnected


class GraphOutput(BaseModel):
    name: str
    type: str
    links: Optional[List[int]]  # null if none
    slot_index: Optional[int]


class GraphNode(BaseModel):
    id: int
    type: str
    title: Optional[str] = None  # omitted if default
    inputs: List[GraphInput] = []  # omitted if none
    outputs: List[GraphOutput] = []  # omitted if none
    properties: dict

    @property
    def outputs_by_slot_id(self):
        return {output.slot_index: output for output in self.outputs}


@dataclass
class GraphLink:
    id: int
    in_node_id: int
    in_slot_id: int
    out_node_id: int
    out_slot_id: int
    type: str


class Graph(BaseModel):
    last_node_id: int
    last_link_id: int
    nodes: List[GraphNode]
    links: List[Tuple[int, int, int, int, int, str]]
    version: float

    links_by_id: Dict[int, GraphLink]
    nodes_by_id: Dict[int, GraphNode]

    def __init__(self, **kwargs):
        super().__init__(**kwargs, links_by_id={}, nodes_by_id={})

        self.links_by_id = {link[0]: GraphLink(*link) for link in self.links}
        self.nodes_by_id = {node.id: node for node in self.nodes}
