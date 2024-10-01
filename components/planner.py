from typing import List, Dict
from openai import OpenAI
from groq import Groq
from config.config import GROQ_MODELS, OPENAI_MODEL, OPENROUTER_MODEL



class Planner:
    def __init__(
        self,
        groq_client: Groq,
        openai_client: OpenAI,
        openrouter_client: OpenAI,
        groq_model: str,
    ):
        self.groq_client = groq_client
        self.openai_client = openai_client
        self.openrouter_client = openrouter_client
        self.groq_model = groq_model

    def create_plan(self, task: str, api: str = "groq") -> List[Dict[str, str]]:
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

        if api == "groq":
            response = self.groq_client.chat.completions.create(
                model=self.groq_model,
                messages=[
                    {
                        "role": "system",
                        "content": "You are an AI planner. Your job is to break down tasks into clear, actionable steps.",
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
                        "content": "You are an AI planner. Your job is to break down tasks into clear, actionable steps.",
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
                        "content": "You are an AI planner. Your job is to break down tasks into clear, actionable steps.",
                    },
                    {"role": "user", "content": prompt},
                ],
            )
        else:
            raise ValueError(f"Invalid API: {api}")

        plan = eval(response.choices[0].message.content)
        return plan

    def refine_plan(
        self, plan: List[Dict[str, str]], feedback: str, api: str = "groq"
    ) -> List[Dict[str, str]]:
        plan_str = str(plan)
        prompt = f"""
        Current plan: {plan_str}
        
        Feedback: {feedback}
        
        Please refine the plan based on the given feedback. Maintain the same format as the original plan.
        """

        if api == "groq":
            response = self.groq_client.chat.completions.create(
                model=GROQ_MODELS[0],
                messages=[
                    {
                        "role": "system",
                        "content": "You are an AI planner. Your job is to refine existing plans based on feedback.",
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
                        "content": "You are an AI planner. Your job is to refine existing plans based on feedback.",
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
                        "content": "You are an AI planner. Your job is to refine existing plans based on feedback.",
                    },
                    {"role": "user", "content": prompt},
                ],
            )
        else:
            raise ValueError(f"Invalid API: {api}")

        refined_plan = eval(response.choices[0].message.content)
        return refined_plan
