from dataclasses import dataclass


@dataclass
class GraphDeps:
    id: str
    query: str


@dataclass
class GraphState:
    intent: str
