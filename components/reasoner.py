from typing import List, Dict, Any
from openai import OpenAI
from groq import Groq
from config.config import GROQ_MODELS, OPENAI_MODEL, OPENROUTER_MODEL



class Reasoner:
    def __init__(self, groq_client: Groq, openai_client: OpenAI, openrouter_client: OpenAI, default_groq_model: str):
        self.groq_client = groq_client
        self.openai_client = openai_client
        self.openrouter_client = openrouter_client
        self.default_groq_model = default_groq_model

    def analyze_step(
        self, step: Dict[str, str], context: Dict[str, Any], api: str = "groq"
    ) -> Dict[str, Any]:
        prompt = f"""
        Step to analyze: {step}
        Context: {context}

        Analyze this step and provide:
        1. Potential challenges or obstacles
        2. Required resources or information
        3. Alternative approaches
        4. Success criteria

        Format the output as a Python dictionary with keys: 'challenges', 'resources', 'alternatives', and 'success_criteria'.
        """

        if api == "groq":
            response = self.groq_client.chat.completions.create(
                model="llama3-1-small",
                messages=[
                    {
                        "role": "system",
                        "content": "You are an AI reasoner. Your job is to analyze steps in a plan and provide insights.",
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
                        "content": "You are an AI reasoner. Your job is to analyze steps in a plan and provide insights.",
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
                        "content": "You are an AI reasoner. Your job is to analyze steps in a plan and provide insights.",
                    },
                    {"role": "user", "content": prompt},
                ],
            )
        else:
            raise ValueError(f"Invalid API: {api}")

        analysis = eval(response.choices[0].message.content)
        return analysis

    def make_decision(
        self,
        options: List[str],
        criteria: Dict[str, float],
        context: Dict[str, Any],
        api: str = "groq",
    ) -> str:
        options_str = "\n".join(f"- {option}" for option in options)
        criteria_str = "\n".join(
            f"- {criterion}: {weight}" for criterion, weight in criteria.items()
        )

        prompt = f"""
        Options:
        {options_str}

        Decision Criteria (with weights):
        {criteria_str}

        Context: {context}

        Based on the given options, decision criteria (with their relative importance as weights), and context, 
        choose the best option. Explain your reasoning, showing how you weighted each criterion for each option.
        
        Format your response as a Python dictionary with keys 'decision' (the chosen option) and 'reasoning' (explanation for the decision).
        """

        if api == "groq":
            response = self.groq_client.chat.completions.create(
                model="llama3-1-small",
                messages=[
                    {
                        "role": "system",
                        "content": "You are an AI reasoner. Your job is to make decisions based on given criteria and context.",
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
                        "content": "You are an AI reasoner. Your job is to make decisions based on given criteria and context.",
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
                        "content": "You are an AI reasoner. Your job is to make decisions based on given criteria and context.",
                    },
                    {"role": "user", "content": prompt},
                ],
            )
        else:
            raise ValueError(f"Invalid API: {api}")

        decision = eval(response.choices[0].message.content)
        return decision

    def solve_problem(
        self,
        problem: str,
        constraints: List[str],
        context: Dict[str, Any],
        api: str = "groq",
    ) -> Dict[str, Any]:
        constraints_str = "\n".join(f"- {constraint}" for constraint in constraints)

        prompt = f"""
        Problem: {problem}
        
        Constraints:
        {constraints_str}

        Context: {context}

        Propose a solution to this problem, taking into account the given constraints and context. 
        Your solution should be creative yet practical.

        Format your response as a Python dictionary with keys 'solution' (a brief description of your proposed solution) 
        and 'steps' (a list of steps to implement the solution).
        """

        if api == "groq":
            response = self.groq_client.chat.completions.create(
                model="llama3-1-small",
                messages=[
                    {
                        "role": "system",
                        "content": "You are an AI reasoner. Your job is to solve problems creatively while adhering to given constraints.",
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
                        "content": "You are an AI reasoner. Your job is to solve problems creatively while adhering to given constraints.",
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
                        "content": "You are an AI reasoner. Your job is to solve problems creatively while adhering to given constraints.",
                    },
                    {"role": "user", "content": prompt},
                ],
            )
        else:
            raise ValueError(f"Invalid API: {api}")

        solution = eval(response.choices[0].message.content)
        return solution
