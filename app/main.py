from fastapi import FastAPI, HTTPException, BackgroundTasks
from uuid import uuid4
from typing import Dict
from app.engine import GraphEngine
from app.models import GraphCreateRequest, GraphRunRequest
from app.workflows import NODE_REGISTRY, quality_gate

app = FastAPI(title="Mini Agent Engine")

# In-memory storage
graphs: Dict[str, GraphEngine] = {}
runs: Dict[str, Dict] = {}

@app.get("/")
def home():
    return {"message": "Agent Engine is Running. Available nodes:", "nodes": list(NODE_REGISTRY.keys())}

@app.post("/graph/create")
def create_graph(payload: GraphCreateRequest):
    """
    Dynamically assembles a graph from registered nodes.
    """
    graph_id = str(uuid4())[:8]
    engine = GraphEngine()
    
    # 1. Register Nodes
    for node_def in payload.nodes:
        if node_def.function_name not in NODE_REGISTRY:
            raise HTTPException(status_code=400, detail=f"Function {node_def.function_name} not found.")
        engine.add_node(node_def.name, NODE_REGISTRY[node_def.function_name])

    # 2. Register Linear Edges
    for edge in payload.edges:
        engine.add_edge(edge.from_node, edge.to_node)

    # 3. Register Entry Point
    engine.set_entry_point(payload.entry_point)
    
    # 4. Hardcoded conditional edge for the assignment Demo (Looping logic)
    # In a full system, we would parse this from JSON too.
    if "check_complexity" in engine.nodes:
        # We override the linear edge to add the loop for the demo workflow
        engine.add_conditional_edge("detect_issues", quality_gate)
        # Ensure the loop connects back
        engine.add_edge("suggest_improvements", "detect_issues")

    graphs[graph_id] = engine
    return {"graph_id": graph_id, "message": "Graph created successfully"}

@app.post("/graph/run")
async def run_graph(payload: GraphRunRequest, background_tasks: BackgroundTasks):
    """
    Runs the graph. Uses async await.
    """
    if payload.graph_id not in graphs:
        raise HTTPException(status_code=404, detail="Graph ID not found")
    
    engine = graphs[payload.graph_id]
    
    # Execute
    try:
        result = await engine.run(payload.initial_state)
        
        # Store result
        run_id = str(uuid4())[:8]
        runs[run_id] = result
        
        return {
            "run_id": run_id,
            "status": "completed",
            "final_state": result["final_state"],
            "logs": result["logs"]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/graph/state/{run_id}")
def get_run_state(run_id: str):
    if run_id not in runs:
        raise HTTPException(status_code=404, detail="Run ID not found")
    return runs[run_id]