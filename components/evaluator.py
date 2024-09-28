# components/evaluator.py

import groq
from typing import Dict, Any, List

class Evaluator:
    def __init__(self, api_key: str):
        self.client = groq.Client(api_key=api_key)

    def evaluate_action(self, action: Dict[str, str], result: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
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

        response = self.client.chat.completions.create(
            model="llama3-1-small",
            messages=[
                {"role": "system", "content": "You are an AI evaluator. Your job is to assess the outcomes of actions and provide constructive feedback."},
                {"role": "user", "content": prompt}
            ]
        )

        evaluation = eval(response.choices[0].message.content)
        return evaluation

    def evaluate_plan(self, plan: List[Dict[str, str]], results: List[Dict[str, Any]], context: Dict[str, Any]) -> Dict[str, Any]:
        evaluations = [self.evaluate_action(action, result, context) for action, result in zip(plan, results)]
        
        overall_score = sum(eval['score'] for eval in evaluations) / len(evaluations)
        
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

        response = self.client.chat.completions.create(
            model="llama3-1-small",
            messages=[
                {"role": "system", "content": "You are an AI evaluator. Your job is to provide an overall assessment of plan execution and offer strategic insights."},
                {"role": "user", "content": prompt}
            ]
        )

        overall_evaluation = eval(response.choices[0].message.content)
        overall_evaluation['score'] = overall_score
        overall_evaluation['action_evaluations'] = evaluations
        
        return overall_evaluation

    def generate_report(self, evaluation: Dict[str, Any]) -> str:
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

        response = self.client.chat.completions.create(
            model="llama3-1-small",
            messages=[
                {"role": "system", "content": "You are an AI report generator. Your job is to create clear, insightful reports based on evaluation data."},
                {"role": "user", "content": prompt}
            ]
        )

        report = response.choices[0].message.content
        return report