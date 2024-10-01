from typing import Dict, Any, List
from openai import OpenAI
from groq import Groq


class Evaluator:
    def __init__(
        self, groq_client: Groq, openai_client: OpenAI, openrouter_client: OpenAI
    ):
        self.groq_client = groq_client
        self.openai_client = openai_client
        self.openrouter_client = openrouter_client

    def evaluate_action(
        self,
        action: Dict[str, str],
        result: Dict[str, Any],
        context: Dict[str, Any],
        api: str = "groq",
    ) -> Dict[str, Any]:
        prompt = f"""
        Action: {action}
        Result: {result}
        Context: {context}

        Evaluate the outcome of this action and provide:
        1. A success score (0-100)
        2. Key achievements
        3. Areas for improvement
        4. Unexpected outcomes or surprises
        5. Recommendations for future actions

        Format the output as a Python dictionary with keys: 'score', 'achievements', 'improvements', 'surprises', and 'recommendations'.
        """

        if api == "groq":
            response = self.groq_client.chat.completions.create(
                model="llama3-1-small",
                messages=[
                    {
                        "role": "system",
                        "content": "You are an AI evaluator. Your job is to assess the outcomes of actions and provide constructive feedback.",
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
                        "content": "You are an AI evaluator. Your job is to assess the outcomes of actions and provide constructive feedback.",
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
                        "content": "You are an AI evaluator. Your job is to assess the outcomes of actions and provide constructive feedback.",
                    },
                    {"role": "user", "content": prompt},
                ],
            )
        else:
            raise ValueError(f"Invalid API: {api}")

        evaluation = eval(response.choices[0].message.content)
        return evaluation

    def evaluate_plan(
        self,
        plan: List[Dict[str, str]],
        results: List[Dict[str, Any]],
        context: Dict[str, Any],
        api: str = "groq",
    ) -> Dict[str, Any]:
        evaluations = [
            self.evaluate_action(action, result, context, api)
            for action, result in zip(plan, results)
        ]

        overall_score = sum(eval["score"] for eval in evaluations) / len(evaluations)

        prompt = f"""
        Plan: {plan}
        Results: {results}
        Individual Evaluations: {evaluations}
        Overall Score: {overall_score}
        Context: {context}

        Provide an overall evaluation of the plan execution:
        1. Summary of key achievements
        2. Major areas for improvement
        3. Lessons learned
        4. Recommendations for future planning and execution

        Format the output as a Python dictionary with keys: 'summary', 'improvements', 'lessons', and 'recommendations'.
        """

        if api == "groq":
            response = self.groq_client.chat.completions.create(
                model="llama3-1-small",
                messages=[
                    {
                        "role": "system",
                        "content": "You are an AI evaluator. Your job is to provide an overall assessment of plan execution and offer strategic insights.",
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
                        "content": "You are an AI evaluator. Your job is to provide an overall assessment of plan execution and offer strategic insights.",
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
                        "content": "You are an AI evaluator. Your job is to provide an overall assessment of plan execution and offer strategic insights.",
                    },
                    {"role": "user", "content": prompt},
                ],
            )
        else:
            raise ValueError(f"Invalid API: {api}")

        overall_evaluation = eval(response.choices[0].message.content)
        overall_evaluation["score"] = overall_score
        overall_evaluation["action_evaluations"] = evaluations

        return overall_evaluation

    def generate_report(self, evaluation: Dict[str, Any], api: str = "groq") -> str:
        prompt = f"""
        Evaluation: {evaluation}

        Generate a detailed report based on this evaluation. The report should include:
        1. An executive summary
        2. Detailed analysis of each action and its outcome
        3. Overall performance assessment
        4. Key lessons learned
        5. Specific recommendations for improvement
        6. Next steps

        Format the report in Markdown.
        """

        if api == "groq":
            response = self.groq_client.chat.completions.create(
                model="llama3-1-small",
                messages=[
                    {
                        "role": "system",
                        "content": "You are an AI report generator. Your job is to create clear, insightful reports based on evaluation data.",
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
                        "content": "You are an AI report generator. Your job is to create clear, insightful reports based on evaluation data.",
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
                        "content": "You are an AI report generator. Your job is to create clear, insightful reports based on evaluation data.",
                    },
                    {"role": "user", "content": prompt},
                ],
            )
        else:
            raise ValueError(f"Invalid API: {api}")

        report = response.choices[0].message.content
        return report
