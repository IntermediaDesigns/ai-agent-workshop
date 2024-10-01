# main.py

from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict, Any
import uvicorn
import os
from dotenv import load_dotenv
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import jwt

# Import our AI agent components
from components.planner import Planner
from components.reasoner import Reasoner
from components.executor import Executor
from components.evaluator import Evaluator
from components.memory import Memory
from components.optimizer import Optimizer

# Import API clients
from openai import OpenAI
from groq import Groq

# Import configuration
from config.config import (
    OPENAI_API_KEY,
    GROQ_API_KEY,
    OPENROUTER_API_KEY,
    OPENAI_MODEL,
    GROQ_MODELS,
    OPENROUTER_MODEL,
)

security = HTTPBearer()


security = HTTPBearer(auto_error=False)


async def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    if credentials is None:
        return {
            "id": "anonymous"
        }  # or handle as you see fit for unauthenticated requests

    token = credentials.credentials
    try:
        payload = jwt.decode(token, options={"verify_signature": False})
        return payload
    except jwt.PyJWTError:
        raise HTTPException(
            status_code=401, detail="Invalid authentication credentials"
        )


app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://ai-agent-workshop.vercel.app/", "http://localhost:5173"],  # Add your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load environment variables
load_dotenv()

# Load API keys from environment variables
groq_api_key = os.getenv("GROQ_API_KEY")
openai_api_key = os.getenv("OPENAI_API_KEY")
openrouter_api_key = os.getenv("OPENROUTER_API_KEY")

# Initialize API clients
groq_client = Groq(api_key=groq_api_key)
openai_client = OpenAI(api_key=openai_api_key)
openrouter_client = OpenAI(
    base_url="https://openrouter.ai/api/v1", api_key=openrouter_api_key
)

# Use the first Groq model in the list as the default
DEFAULT_GROQ_MODEL = GROQ_MODELS[0]



# Initialize the components with all API clients
planner = Planner(groq_client, openai_client, openrouter_client, DEFAULT_GROQ_MODEL)
reasoner = Reasoner(groq_client, openai_client, openrouter_client, DEFAULT_GROQ_MODEL)
executor = Executor(groq_client, openai_client, openrouter_client, DEFAULT_GROQ_MODEL)
evaluator = Evaluator(groq_client, openai_client, openrouter_client, DEFAULT_GROQ_MODEL)
memory = Memory(groq_client, openai_client, openrouter_client, DEFAULT_GROQ_MODEL)
optimizer = Optimizer(groq_client, openai_client, openrouter_client, DEFAULT_GROQ_MODEL)

# This is important for Vercel serverless function
app = app


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
async def run_task(task_input: TaskInput, user: dict = Depends(verify_token)):
    global task_history

    task = task_input.task
    context = task_input.context
    api = context.get("api", "groq")

    # Select the appropriate model based on the API
    if api == "groq":
        model = context.get("model", DEFAULT_GROQ_MODEL)
        if model not in GROQ_MODELS:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid Groq model. Available models are: {', '.join(GROQ_MODELS)}",
            )
    elif api == "openai":
        model = OPENAI_MODEL
    elif api == "openrouter":
        model = OPENROUTER_MODEL
    else:
        raise HTTPException(status_code=400, detail="Invalid API specified")

    try:
        # Optimize based on past performance
        if task_history:
            optimizations = optimizer.optimize_all_components(
                task_history, task, context, api
            )
            # TODO: Apply optimizations to components

        # Retrieve relevant information from memory
        relevant_info = memory.retrieve_relevant_info(task, context, api)
        context.update(relevant_info)

        # Use the selected model in your components
        initial_plan = planner.create_plan(task, api=api, model=model)
        results = executor.execute_plan(initial_plan, context, api=api, model=model)
        evaluation = evaluator.evaluate_plan(initial_plan, results, context, api=api, model=model)

        # Store learnings in memory
        memory.summarize_and_store(
            {
                "task": task,
                "plan": initial_plan,
                "results": results,
                "evaluation": evaluation,
            },
            context,
            api,
        )

        # Clear short-term memory for the next task
        memory.clear_short_term_memory()

        task_result = {"task": task, "evaluation": evaluation, "context": context}
        task_history.append(task_result)

        return TaskOutput(
            task=task, plan=initial_plan, results=results, evaluation=evaluation
        )

        return TaskOutput(
            task=task, plan=initial_plan, results=results, evaluation=evaluation
        )
    except Exception as e:
        print(f"Error in run_task: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/task_history")
async def get_task_history():
    return {"task_history": task_history}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
