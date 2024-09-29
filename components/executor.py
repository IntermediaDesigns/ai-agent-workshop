# components/executor.py

import groq
from typing import Dict, Any, List
import time
import random


class Executor:
    def __init__(self, api_key: str):
        self.client = groq.Client(api_key=GROQ_API_KEY)

    def execute_action(
        self, action: Dict[str, str], context: Dict[str, Any]
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

        response = self.client.chat.completions.create(
            model="llama3-1-small",
            messages=[
                {
                    "role": "system",
                    "content": "You are an AI executor. Your job is to simulate the execution of actions and provide realistic outcomes.",
                },
                {"role": "user", "content": prompt},
            ],
        )

        execution_result = eval(response.choices[0].message.content)
        return execution_result

    def execute_plan(
        self, plan: List[Dict[str, str]], context: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        results = []
        for step in plan:
            result = self.execute_action(step, context)
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
        self, error: Dict[str, Any], context: Dict[str, Any]
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

        response = self.client.chat.completions.create(
            model="llama3-1-small",
            messages=[
                {
                    "role": "system",
                    "content": "You are an AI error handler. Your job is to analyze errors and propose solutions.",
                },
                {"role": "user", "content": prompt},
            ],
        )

        error_handling = eval(response.choices[0].message.content)
        return error_handling
