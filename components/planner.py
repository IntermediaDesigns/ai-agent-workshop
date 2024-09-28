# components/planner.py

import groq
from typing import List, Dict


class Planner:
    def __init__(self, api_key: str):
        self.client = groq.Client(api_key=api_key)

    def create_plan(self, task: str) -> List[Dict[str, str]]:
        prompt = f"""
        Task: {task}
        
        Create a detailed step-by-step plan to accomplish this task. Each step should be concise but clear.
        Format the output as a Python list of dictionaries, where each dictionary represents a step with 'action' and 'description' keys.
        
        Example format:
        [
            {{"action": "Step 1", "description": "Description of step 1"}},
            {{"action": "Step 2", "description": "Description of step 2"}},
            ...
        ]
        """

        response = self.client.chat.completions.create(
            model="llama3-1-small",  # Specify the Llama 3.1 model you're using
            messages=[
                {
                    "role": "system",
                    "content": "You are an AI planner. Your job is to break down tasks into clear, actionable steps.",
                },
                {"role": "user", "content": prompt},
            ],
        )

        # Parse the response and convert it to the expected format
        plan = eval(response.choices[0].message.content)
        return plan

    def refine_plan(
        self, plan: List[Dict[str, str]], feedback: str
    ) -> List[Dict[str, str]]:
        plan_str = str(plan)
        prompt = f"""
        Current plan: {plan_str}
        
        Feedback: {feedback}
        
        Please refine the plan based on the given feedback. Maintain the same format as the original plan.
        """

        response = self.client.chat.completions.create(
            model="llama3-1-small",
            messages=[
                {
                    "role": "system",
                    "content": "You are an AI planner. Your job is to refine existing plans based on feedback.",
                },
                {"role": "user", "content": prompt},
            ],
        )

        refined_plan = eval(response.choices[0].message.content)
        return refined_plan
