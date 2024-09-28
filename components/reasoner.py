# components/reasoner.py

import groq
from typing import List, Dict, Any


class Reasoner:
    def __init__(self, api_key: str):
        self.client = groq.Client(api_key=api_key)

    def analyze_step(
        self, step: Dict[str, str], context: Dict[str, Any]
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

        response = self.client.chat.completions.create(
            model="llama3-1-small",
            messages=[
                {
                    "role": "system",
                    "content": "You are an AI reasoner. Your job is to analyze steps in a plan and provide insights.",
                },
                {"role": "user", "content": prompt},
            ],
        )

        analysis = eval(response.choices[0].message.content)
        return analysis

    def make_decision(
        self, options: List[str], criteria: Dict[str, float], context: Dict[str, Any]
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

        response = self.client.chat.completions.create(
            model="llama3-1-small",
            messages=[
                {
                    "role": "system",
                    "content": "You are an AI reasoner. Your job is to make decisions based on given criteria and context.",
                },
                {"role": "user", "content": prompt},
            ],
        )

        decision = eval(response.choices[0].message.content)
        return decision

    def solve_problem(
        self, problem: str, constraints: List[str], context: Dict[str, Any]
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

        response = self.client.chat.completions.create(
            model="llama3-1-small",
            messages=[
                {
                    "role": "system",
                    "content": "You are an AI reasoner. Your job is to solve problems creatively while adhering to given constraints.",
                },
                {"role": "user", "content": prompt},
            ],
        )

        solution = eval(response.choices[0].message.content)
        return solution
