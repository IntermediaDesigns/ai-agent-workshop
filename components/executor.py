from typing import Dict, Any, List
from openai import OpenAI
from groq import Groq
import time
import random
from config.config import GROQ_MODELS, OPENAI_MODEL, OPENROUTER_MODEL



class Executor:
    def __init__(self, groq_client: Groq, openai_client: OpenAI, openrouter_client: OpenAI, default_groq_model: str):
        self.groq_client = groq_client
        self.openai_client = openai_client
        self.openrouter_client = openrouter_client
        self.default_groq_model = default_groq_model

    def execute_action(
        self, action: Dict[str, str], context: Dict[str, Any], api: str = "groq"
    ) -> Dict[str, Any]:
        # Simulate action execution
        time.sleep(random.uniform(0.5, 2.0))  # Simulate varying execution times

        prompt = f"""
        Action to execute: {action}
        Context: {context}

        Simulate the execution of this action and provide:
        1. The result of the action
        2. Any side effects or unexpected outcomes
        3. Resources used during execution
        4. Time taken to complete (in minutes)

        Format the output as a Python dictionary with keys: 'result', 'side_effects', 'resources_used', and 'time_taken'.
        """

        if api == "groq":
            response = self.groq_client.chat.completions.create(
                model=GROQ_MODELS[0],
                messages=[
                    {
                        "role": "system",
                        "content": "You are an AI executor. Your job is to simulate the execution of actions and provide realistic outcomes.",
                    },
                    {"role": "user", "content": prompt},
                ],
            )
        elif api == "openai":
            response = self.openai_client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {
                        "role": "system",
                        "content": "You are an AI executor. Your job is to simulate the execution of actions and provide realistic outcomes.",
                    },
                    {"role": "user", "content": prompt},
                ],
            )
        elif api == "openrouter":
            response = self.openrouter_client.chat.completions.create(
                model="meta-llama/llama-3.1-8b-instruct:free",
                messages=[
                    {
                        "role": "system",
                        "content": "You are an AI executor. Your job is to simulate the execution of actions and provide realistic outcomes.",
                    },
                    {"role": "user", "content": prompt},
                ],
            )
        else:
            raise ValueError(f"Invalid API: {api}")

        execution_result = eval(response.choices[0].message.content)
        return execution_result

    def execute_plan(
        self, plan: List[Dict[str, str]], context: Dict[str, Any], api: str = "groq"
    ) -> List[Dict[str, Any]]:
        results = []
        for step in plan:
            result = self.execute_action(step, context, api)
            results.append(result)

            # Update context based on the result
            context.update(
                {
                    "last_action": step["action"],
                    "last_result": result["result"],
                    "resources_used": result["resources_used"],
                    "total_time": context.get("total_time", 0) + result["time_taken"],
                }
            )

        return results

    def handle_error(
        self, error: Dict[str, Any], context: Dict[str, Any], api: str = "groq"
    ) -> Dict[str, Any]:
        prompt = f"""
        Error encountered: {error}
        Context: {context}

        Propose a solution to handle this error. Consider:
        1. The nature of the error
        2. Possible causes
        3. Potential fixes or workarounds
        4. Steps to implement the solution

        Format the output as a Python dictionary with keys: 'analysis', 'solution', and 'implementation_steps'.
        """

        if api == "groq":
            response = self.groq_client.chat.completions.create(
                model=GROQ_MODELS[0],
                messages=[
                    {
                        "role": "system",
                        "content": "You are an AI error handler. Your job is to analyze errors and propose solutions.",
                    },
                    {"role": "user", "content": prompt},
                ],
            )
        elif api == "openai":
            response = self.openai_client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {
                        "role": "system",
                        "content": "You are an AI error handler. Your job is to analyze errors and propose solutions.",
                    },
                    {"role": "user", "content": prompt},
                ],
            )
        elif api == "openrouter":
            response = self.openrouter_client.chat.completions.create(
                model="meta-llama/llama-3.1-8b-instruct:free",
                messages=[
                    {
                        "role": "system",
                        "content": "You are an AI error handler. Your job is to analyze errors and propose solutions.",
                    },
                    {"role": "user", "content": prompt},
                ],
            )
        else:
            raise ValueError(f"Invalid API: {api}")

        error_handling = eval(response.choices[0].message.content)
        return error_handling
