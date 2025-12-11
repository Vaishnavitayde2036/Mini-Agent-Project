import random
from app.engine import WorkflowContext

# Global Registry for the API to look up functions
NODE_REGISTRY = {}

def register_node(name):
    def decorator(func):
        NODE_REGISTRY[name] = func
        return func
    return decorator

# --- OPTION A: Code Review Workflow Implementation ---

@register_node("extract_functions")
def extract_functions(ctx: WorkflowContext):
    code = ctx.state.get("code", "")
    # Mock logic: split by 'def '
    func_count = code.count("def ")
    ctx.update("function_count", func_count)
    ctx.log(f"Extracted {func_count} functions.")

@register_node("check_complexity")
def check_complexity(ctx: WorkflowContext):
    code = ctx.state.get("code", "")
    # Mock logic: length of code acts as complexity
    complexity = len(code) / 10
    ctx.update("complexity_score", complexity)
    ctx.log(f"Calculated complexity: {complexity}")

@register_node("detect_issues")
def detect_issues(ctx: WorkflowContext):
    # Mock logic: Randomly find issues if quality is low
    if ctx.state.get("quality_score", 0) < 80:
        ctx.update("issues_found", True)
        ctx.log("Issues detected in code structure.")
    else:
        ctx.update("issues_found", False)
        ctx.log("No major issues found.")

@register_node("suggest_improvements")
def suggest_improvements(ctx: WorkflowContext):
    # Mock logic: "Fix" the code by increasing quality score
    current_quality = ctx.state.get("quality_score", 50)
    improvement = random.randint(10, 20)
    new_quality = min(100, current_quality + improvement)
    
    ctx.update("quality_score", new_quality)
    ctx.log(f"Applied fixes. Quality improved from {current_quality} to {new_quality}.")

def quality_gate(ctx: WorkflowContext) -> str:
    """Conditional Edge Logic"""
    score = ctx.state.get("quality_score", 0)
    if score >= 90:
        return "END" # Special keyword for engine to stop
    else:
        return "suggest_improvements" # Loop back