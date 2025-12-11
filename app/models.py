from pydantic import BaseModel
from typing import List, Dict, Any, Optional

class NodeDef(BaseModel):
    name: str
    function_name: str # Must match a key in NODE_REGISTRY

class EdgeDef(BaseModel):
    from_node: str
    to_node: str

class GraphCreateRequest(BaseModel):
    nodes: List[NodeDef]
    edges: List[EdgeDef]
    entry_point: str

class GraphRunRequest(BaseModel):
    graph_id: str
    initial_state: Dict[str, Any]