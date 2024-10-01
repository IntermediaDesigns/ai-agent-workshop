from typing import Dict, Any, List
from openai import OpenAI
from groq import Groq
from config.config import GROQ_MODELS, OPENAI_MODEL, OPENROUTER_MODEL



class Optimizer:
    def __init__(self, groq_client: Groq, openai_client: OpenAI, openrouter_client: OpenAI, default_groq_model: str):
        self.groq_client = groq_client
        self.openai_client = openai_client
        self.openrouter_client = openrouter_client
        self.default_groq_model = default_groq_model

    def analyze_performance(
        self, task_history: List[Dict[str, Any]], api: str = "groq"
    ) -> Dict[str, Any]:
        prompt = f"""
        Task History: {task_history}

        Analyze the performance across these tasks and provide:
        1. Common patterns in successful strategies
        2. Recurring issues or bottlenecks
        3. Trends in performance over time
        4. Potential areas for improvement in planning and reasoning

        Format the output as a Python dictionary with keys: 'success_patterns', 'issues', 'trends', and 'improvement_areas'.
        """

        if api == "groq":
            response = self.groq_client.chat.completions.create(
                model="llama3-1-small",
                messages=[
                    {
                        "role": "system",
                        "content": "You are an AI performance analyst. Your job is to identify patterns and suggest improvements based on historical task performance.",
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
                        "content": "You are an AI performance analyst. Your job is to identify patterns and suggest improvements based on historical task performance.",
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
                        "content": "You are an AI performance analyst. Your job is to identify patterns and suggest improvements based on historical task performance.",
                    },
                    {"role": "user", "content": prompt},
                ],
            )
        else:
            raise ValueError(f"Invalid API: {api}")

        analysis = eval(response.choices[0].message.content)
        return analysis

    def generate_optimization_suggestions(
        self, analysis: Dict[str, Any], current_task: str, api: str = "groq"
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

        if api == "groq":
            response = self.groq_client.chat.completions.create(
                model="llama3-1-small",
                messages=[
                    {
                        "role": "system",
                        "content": "You are an AI optimization expert. Your job is to suggest improvements to an AI agent's strategies based on past performance and the current task.",
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
                        "content": "You are an AI optimization expert. Your job is to suggest improvements to an AI agent's strategies based on past performance and the current task.",
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
                        "content": "You are an AI optimization expert. Your job is to suggest improvements to an AI agent's strategies based on past performance and the current task.",
                    },
                    {"role": "user", "content": prompt},
                ],
            )
        else:
            raise ValueError(f"Invalid API: {api}")

        suggestions = eval(response.choices[0].message.content)
        return suggestions

    def apply_optimizations(
        self,
        component: str,
        suggestions: List[tuple],
        context: Dict[str, Any],
        api: str = "groq",
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

        if api == "groq":
            response = self.groq_client.chat.completions.create(
                model="llama3-1-small",
                messages=[
                    {
                        "role": "system",
                        "content": "You are an AI system architect. Your job is to determine how to implement optimization suggestions in specific components of an AI agent.",
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
                        "content": "You are an AI system architect. Your job is to determine how to implement optimization suggestions in specific components of an AI agent.",
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
                        "content": "You are an AI system architect. Your job is to determine how to implement optimization suggestions in specific components of an AI agent.",
                    },
                    {"role": "user", "content": prompt},
                ],
            )
        else:
            raise ValueError(f"Invalid API: {api}")

        optimizations = eval(response.choices[0].message.content)
        return optimizations

    def optimize_component(
        self,
        component: str,
        task_history: List[Dict[str, Any]],
        current_task: str,
        context: Dict[str, Any],
        api: str = "groq",
    ) -> Dict[str, Any]:
        analysis = self.analyze_performance(task_history, api)
        suggestions = self.generate_optimization_suggestions(
            analysis, current_task, api
        )
        component_suggestions = suggestions.get(f"{component}_suggestions", [])
        optimizations = self.apply_optimizations(
            component, component_suggestions, context, api
        )
        return optimizations

    def optimize_all_components(
        self,
        task_history: List[Dict[str, Any]],
        current_task: str,
        context: Dict[str, Any],
        api: str = "groq",
    ) -> Dict[str, Dict[str, Any]]:
        components = ["planning", "reasoning", "execution", "evaluation"]
        optimizations = {}
        for component in components:
            optimizations[component] = self.optimize_component(
                component, task_history, current_task, context, api
            )
        return optimizations
