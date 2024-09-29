# components/optimizer.py

import groq
from typing import Dict, Any, List


class Optimizer:
    def __init__(self, api_key: str):
        self.client = groq.Client(api_key=GROQ_API_KEY)

    def analyze_performance(self, task_history: List[Dict[str, Any]]) -> Dict[str, Any]:
        prompt = f"""
        Task History: {task_history}

        Analyze the performance across these tasks and provide:
        1. Common patterns in successful strategies
        2. Recurring issues or bottlenecks
        3. Trends in performance over time
        4. Potential areas for improvement in planning and reasoning

        Format the output as a Python dictionary with keys: 'success_patterns', 'issues', 'trends', and 'improvement_areas'.
        """

        response = self.client.chat.completions.create(
            model="llama3-1-small",
            messages=[
                {
                    "role": "system",
                    "content": "You are an AI performance analyst. Your job is to identify patterns and suggest improvements based on historical task performance.",
                },
                {"role": "user", "content": prompt},
            ],
        )

        analysis = eval(response.choices[0].message.content)
        return analysis

    def generate_optimization_suggestions(
        self, analysis: Dict[str, Any], current_task: str
    ) -> Dict[str, Any]:
        prompt = f"""
        Performance Analysis: {analysis}
        Current Task: {current_task}

        Based on the performance analysis and the current task, generate suggestions for optimizing:
        1. Planning strategies
        2. Reasoning approaches
        3. Execution methods
        4. Evaluation criteria

        For each suggestion, provide a brief explanation of its potential impact.

        Format the output as a Python dictionary with keys: 'planning_suggestions', 'reasoning_suggestions', 
        'execution_suggestions', and 'evaluation_suggestions'. Each value should be a list of tuples, 
        where each tuple contains (suggestion, explanation).
        """

        response = self.client.chat.completions.create(
            model="llama3-1-small",
            messages=[
                {
                    "role": "system",
                    "content": "You are an AI optimization expert. Your job is to suggest improvements to an AI agent's strategies based on past performance and the current task.",
                },
                {"role": "user", "content": prompt},
            ],
        )

        suggestions = eval(response.choices[0].message.content)
        return suggestions

    def apply_optimizations(
        self, component: str, suggestions: List[tuple], context: Dict[str, Any]
    ) -> Dict[str, Any]:
        prompt = f"""
        Component: {component}
        Optimization Suggestions: {suggestions}
        Current Context: {context}

        For each suggestion, determine how to best implement it in the given component. Provide:
        1. A description of the change to be made
        2. The expected impact of the change
        3. Any potential risks or trade-offs

        Format the output as a Python dictionary with keys matching the suggestions, where each value is 
        another dictionary containing 'implementation', 'impact', and 'risks'.
        """

        response = self.client.chat.completions.create(
            model="llama3-1-small",
            messages=[
                {
                    "role": "system",
                    "content": "You are an AI system architect. Your job is to determine how to implement optimization suggestions in specific components of an AI agent.",
                },
                {"role": "user", "content": prompt},
            ],
        )

        optimizations = eval(response.choices[0].message.content)
        return optimizations
