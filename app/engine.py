import asyncio
from typing import Dict, Any, Callable, Optional, List

class WorkflowContext:
    """Holds the state of the workflow execution."""
    def __init__(self, state: Dict[str, Any]):
        self.state = state
        self.logs: List[str] = []
        self.status: str = "running"

    def update(self, key: str, value: Any):
        self.state[key] = value

    def log(self, message: str):
        self.logs.append(message)

# Type alias for a node function
NodeFunction = Callable[[WorkflowContext], Any]

class GraphEngine:
    def __init__(self):
        self.nodes: Dict[str, NodeFunction] = {}
        self.edges: Dict[str, str] = {}  # Simple: node_a -> node_b
        self.conditional_edges: Dict[str, Callable[[WorkflowContext], str]] = {} # node_a -> logic_func -> node_b
        self.entry_point: Optional[str] = None
        self.end_point: str = "END"

    def add_node(self, name: str, func: NodeFunction):
        self.nodes[name] = func

    def set_entry_point(self, name: str):
        self.entry_point = name

    def add_edge(self, from_node: str, to_node: str):
        self.edges[from_node] = to_node

    def add_conditional_edge(self, from_node: str, condition_func: Callable[[WorkflowContext], str]):
        """
        condition_func should return the name of the next node.
        """
        self.conditional_edges[from_node] = condition_func

    async def run(self, initial_state: Dict[str, Any]):
        if not self.entry_point:
            raise ValueError("No entry point defined.")

        context = WorkflowContext(initial_state)
        current_node_name = self.entry_point
        context.log(f"Starting workflow at {current_node_name}")

        # Safety valve for infinite loops
        steps_count = 0
        max_steps = 20

        while current_node_name != self.end_point and steps_count < max_steps:
            if current_node_name not in self.nodes:
                raise ValueError(f"Node {current_node_name} not found in registry.")

            # 1. Execute the node
            node_func = self.nodes[current_node_name]
            context.log(f"Executing: {current_node_name}")
            
            # Support both async and sync nodes
            if asyncio.iscoroutinefunction(node_func):
                await node_func(context)
            else:
                node_func(context)

            steps_count += 1

            # 2. Determine next node
            if current_node_name in self.conditional_edges:
                # Dynamic branching
                condition_func = self.conditional_edges[current_node_name]
                next_node = condition_func(context)
                context.log(f"Condition met. Routing to: {next_node}")
                current_node_name = next_node
            elif current_node_name in self.edges:
                # Linear transition
                current_node_name = self.edges[current_node_name]
            else:
                # No outgoing edge implies end
                current_node_name = self.end_point

        context.status = "completed"
        return {
            "final_state": context.state,
            "logs": context.logs,
            "steps_executed": steps_count
        }