# main.py

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Any
import uvicorn
import os

# Import our AI agent components
from components.planner import Planner
from components.reasoner import Reasoner
from components.executor import Executor
from components.evaluator import Evaluator
from components.memory import Memory
from components.optimizer import Optimizer

app = FastAPI()

# Load API key from environment variable
groq_api_key = os.getenv('GROQ_API_KEY')

# Initialize the components
planner = Planner(groq_api_key)
reasoner = Reasoner(groq_api_key)
executor = Executor(groq_api_key)
evaluator = Evaluator(groq_api_key)
memory = Memory(groq_api_key)
optimizer = Optimizer(groq_api_key)

class TaskInput(BaseModel):
    task: str
    context: Dict[str, Any]

class TaskOutput(BaseModel):
    task: str
    plan: List[Dict[str, str]]
    results: List[Dict[str, Any]]
    evaluation: Dict[str, Any]

task_history = []

@app.post("/run_task", response_model=TaskOutput)
async def run_task(task_input: TaskInput):
    global task_history

    task = task_input.task
    context = task_input.context

    # Optimize based on past performance
    if task_history:
        analysis = optimizer.analyze_performance(task_history)
        suggestions = optimizer.generate_optimization_suggestions(analysis, task)
        
        # Apply optimizations to each component
        for component, component_suggestions in suggestions.items():
            optimizations = optimizer.apply_optimizations(component, component_suggestions, context)
            # In a real-world scenario, you would apply these optimizations to the components

    # Retrieve relevant information from memory
    relevant_info = memory.retrieve_relevant_info(task, context)
    context.update(relevant_info)

    # Create a plan
    initial_plan = planner.create_plan(task)

    # Execute the plan
    results = executor.execute_plan(initial_plan, context)

    # Evaluate the plan execution
    evaluation = evaluator.evaluate_plan(initial_plan, results, context)

    # Store learnings in memory
    memory.summarize_and_store({
        'task': task,
        'plan': initial_plan,
        'results': results,
        'evaluation': evaluation
    }, context)

    # Clear short-term memory for the next task
    memory.clear_short_term_memory()

    task_result = {
        'task': task,
        'evaluation': evaluation,
        'context': context
    }
    task_history.append(task_result)

    return TaskOutput(task=task, plan=initial_plan, results=results, evaluation=evaluation)

@app.get("/task_history")
async def get_task_history():
    return {"task_history": task_history}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)