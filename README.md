
Mini Agent Workflow Engine

A lightweight, async backend for AI agent workflows built with **FastAPI**. It allows you to define nodes, connect them with edges, and support conditional looping (e.g., a "Code Review" agent that loops until quality improves).

Features
- Graph Engine: Dynamic execution of nodes and edges.
- State Management: A shared dictionary (`state`) that flows between steps.
- Conditional Branching: Support for loops and logic-based routing.
- Async Execution: Built on Python's `asyncio` for non-blocking operations.
- REST API: Clean endpoints to create and run workflows.

Setup & Installation

1. Clone the repository
   
   git clone (https://github.com/Vaishnavitayde2036/mini-agent-engine.git)
   cd mini-agent-engine


2.  Create a Virtual Environment

   
    python -m venv venv
    # Windows:
    .\venv\Scripts\activate
    # Mac/Linux:
    source venv/bin/activate
    

3.  Install Dependencies

    pip install fastapi uvicorn pydantic
   

4.  Run the Server

    
    uvicorn app.main:app --reload
   

    The API will be available at: `http://127.0.0.1:8000`

📖 How to Use

The easiest way to test is via the interactive API docs at `http://127.0.0.1:8000/docs`.

1. Create a Workflow Graph

Send a POST request to `/graph/create` with your node definitions.

Example Payload:


{
  "nodes": [
    {"name": "extract", "function_name": "extract_functions"},
    {"name": "complexity", "function_name": "check_complexity"},
    {"name": "detect", "function_name": "detect_issues"},
    {"name": "improve", "function_name": "suggest_improvements"}
  ],
  "edges": [
    {"from_node": "extract", "to_node": "complexity"},
    {"from_node": "complexity", "to_node": "detect"}
  ],
  "entry_point": "extract"
}


Copy the `graph_id` returned in the response.

2. Run the Agent

Send a POST request to `/graph/run`.

Example Payload:


{
  "graph_id": "YOUR_GRAPH_ID_HERE",
  "initial_state": {
    "code": "def hello(): print('world')",
    "quality_score": 50
  }
}

3. View Results

The response will contain the execution logs, showing the agent looping through the "improve" step until the quality score meets the threshold.

📂 Project Structure
/app
  ├── main.py       # FastAPI entry point
  ├── engine.py     # Core Graph Workflow Logic
  ├── models.py     # Pydantic data models
  └── workflows.py  # "Option A" Code Review Agent Logic

