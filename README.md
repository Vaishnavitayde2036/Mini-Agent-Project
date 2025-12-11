# Mini Agent Workflow Engine

A lightweight, async workflow engine built with FastAPI. It supports defining nodes, linear transitions, and conditional loops to simulate agentic behaviors.

## Setup
1. `pip install -r requirements.txt`
2. Run server: `uvicorn app.main:app --reload`

## How to Test (Option A: Code Review)

**1. Create the Graph**
POST `/graph/create`
```json
{
  "nodes": [
    {"name": "extract", "function_name": "extract_functions"},
    {"name": "complexity", "function_name": "check_complexity"},
    {"name": "detect_issues", "function_name": "detect_issues"},
    {"name": "suggest_improvements", "function_name": "suggest_improvements"}
  ],
  "edges": [
    {"from_node": "extract", "to_node": "complexity"},
    {"from_node": "complexity", "to_node": "detect_issues"}
  ],
  "entry_point": "extract"
}