from fastapi import FastAPI, Depends, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict, Any
import uvicorn
import os
from dotenv import load_dotenv
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import jwt
import logging

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


logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://ai-agent-workshop.vercel.app/",
        "http://localhost:5173",
    ],  # Add your frontend URL
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


@app.post("/run_task")
async def run_task(request: Request):
    try:
        # Log the incoming request payload
        payload = await request.json()
        logging.info(f"Received payload: {payload}")

        # Process the payload
        task = payload.get("task")
        context = payload.get("context")
        api = context.get("api", "groq")

        logging.info(f"Received task: {task}, context: {context}, api: {api}")

        # Select the appropriate model based on the API
        if api == "groq":
            model = context.get("model", DEFAULT_GROQ_MODEL)
            if model not in GROQ_MODELS:
                logging.error(f"Invalid Groq model: {model}")
                raise HTTPException(
                    status_code=400,
                    detail=f"Invalid Groq model. Available models are: {', '.join(GROQ_MODELS)}",
                )
        elif api == "openai":
            model = OPENAI_MODEL
        elif api == "openrouter":
            model = OPENROUTER_MODEL
        else:
            logging.error(f"Invalid API specified: {api}")
            raise HTTPException(status_code=400, detail="Invalid API specified")

        logging.info(f"Selected model: {model}")

        try:
            # Optimize based on past performance
            if task_history:
                logging.info(f"Optimizing with task history: {task_history}")
                optimizations = optimizer.optimize_all_components(
                    task_history, task, context, api
                )
                logging.info(f"Optimizations: {optimizations}")
            else:
                logging.info("No task history available for optimization")
        except Exception as e:
            logging.error(f"Error during optimization: {e}")
            raise

    except Exception as e:
        logging.error(f"Unhandled exception: {e}")
        raise


@app.get("/task_history")
async def get_task_history():
    return {"task_history": task_history}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
