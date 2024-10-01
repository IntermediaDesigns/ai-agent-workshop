from typing import Dict, Any, List
from openai import OpenAI
from groq import Groq
import json
import os
from config.config import GROQ_MODELS, OPENAI_MODEL, OPENROUTER_MODEL


class Memory:
    def __init__(
        self,
        groq_client: Groq,
        openai_client: OpenAI,
        openrouter_client: OpenAI,
        default_groq_model: str,
        storage_file: str = "memory_storage.json",
    ):
        self.groq_client = groq_client
        self.openai_client = openai_client
        self.openrouter_client = openrouter_client
        self.default_groq_model = default_groq_model
        self.storage_file = storage_file
        self.short_term_memory = {}
        self.long_term_memory = self.load_long_term_memory()

    def load_long_term_memory(self) -> Dict[str, Any]:
        if os.path.exists(self.storage_file):
            with open(self.storage_file, "r") as f:
                return json.load(f)
        return {}

    def save_long_term_memory(self):
        with open(self.storage_file, "w") as f:
            json.dump(self.long_term_memory, f)

    def add_to_short_term_memory(self, key: str, value: Any):
        self.short_term_memory[key] = value

    def add_to_long_term_memory(self, key: str, value: Any):
        self.long_term_memory[key] = value
        self.save_long_term_memory()

    def get_from_short_term_memory(self, key: str) -> Any:
        return self.short_term_memory.get(key)

    def get_from_long_term_memory(self, key: str) -> Any:
        return self.long_term_memory.get(key)

    def summarize_and_store(
        self,
        data: Dict[str, Any],
        context: Dict[str, Any],
        api: str = "groq",
        model: str = None,
    ):
        prompt = f"""
        Data: {data}
        Context: {context}

        Summarize the key information from this data that should be remembered for future tasks. 
        Consider:
        1. Important insights or lessons learned
        2. Successful strategies or approaches
        3. Common pitfalls or errors to avoid
        4. Relevant statistics or metrics

        Format the output as a Python dictionary with keys representing categories of information 
        and values containing the summarized insights.
        """

        if api == "groq":
            model = model or self.default_groq_model
            if model not in GROQ_MODELS:
                raise ValueError(
                    f"Invalid Groq model. Available models are: {', '.join(GROQ_MODELS)}"
                )
            response = self.groq_client.chat.completions.create(
                model=model,
                messages=[
                    {
                        "role": "system",
                        "content": "You are an AI memory manager. Your job is to extract and summarize key information for long-term storage.",
                    },
                    {"role": "user", "content": prompt},
                ],
            )
        elif api == "openai":
            response = self.openai_client.chat.completions.create(
                model=OPENAI_MODEL,
                messages=[
                    {
                        "role": "system",
                        "content": "You are an AI memory manager. Your job is to extract and summarize key information for long-term storage.",
                    },
                    {"role": "user", "content": prompt},
                ],
            )
        elif api == "openrouter":
            response = self.openrouter_client.chat.completions.create(
                model=OPENROUTER_MODEL,
                messages=[
                    {
                        "role": "system",
                        "content": "You are an AI memory manager. Your job is to extract and summarize key information for long-term storage.",
                    },
                    {"role": "user", "content": prompt},
                ],
            )
        else:
            raise ValueError(f"Invalid API: {api}")

        summary = eval(response.choices[0].message.content)

        for category, insights in summary.items():
            self.add_to_long_term_memory(category, insights)

    def retrieve_relevant_info(
        self, query: str, context: Dict[str, Any], api: str = "groq", model: str = None
    ) -> Dict[str, Any]:
        prompt = f"""
        Query: {query}
        Context: {context}
        Long-term memory: {self.long_term_memory}
        Short-term memory: {self.short_term_memory}

        Retrieve and synthesize relevant information from the provided memories that could be useful 
        for addressing the query. Consider both long-term and short-term memories.

        Format the output as a Python dictionary with keys 'relevant_info' (a list of relevant pieces of information) 
        and 'synthesis' (a brief summary of how this information relates to the query).
        """

        if api == "groq":
            model = model or self.default_groq_model
            if model not in GROQ_MODELS:
                raise ValueError(
                    f"Invalid Groq model. Available models are: {', '.join(GROQ_MODELS)}"
                )
            response = self.groq_client.chat.completions.create(
                model=model,
                messages=[
                    {
                        "role": "system",
                        "content": "You are an AI memory retrieval system. Your job is to find and synthesize relevant information from stored memories.",
                    },
                    {"role": "user", "content": prompt},
                ],
            )
        elif api == "openai":
            response = self.openai_client.chat.completions.create(
                model=OPENAI_MODEL,
                messages=[
                    {
                        "role": "system",
                        "content": "You are an AI memory retrieval system. Your job is to find and synthesize relevant information from stored memories.",
                    },
                    {"role": "user", "content": prompt},
                ],
            )
        elif api == "openrouter":
            response = self.openrouter_client.chat.completions.create(
                model=OPENROUTER_MODEL,
                messages=[
                    {
                        "role": "system",
                        "content": "You are an AI memory retrieval system. Your job is to find and synthesize relevant information from stored memories.",
                    },
                    {"role": "user", "content": prompt},
                ],
            )
        else:
            raise ValueError(f"Invalid API: {api}")

        retrieval_result = eval(response.choices[0].message.content)
        return retrieval_result

    def retrieve_relevant_info(
        self, query: str, context: Dict[str, Any], api: str = "groq"
    ) -> Dict[str, Any]:
        prompt = f"""
        Query: {query}
        Context: {context}
        Long-term memory: {self.long_term_memory}
        Short-term memory: {self.short_term_memory}

        Retrieve and synthesize relevant information from the provided memories that could be useful 
        for addressing the query. Consider both long-term and short-term memories.

        Format the output as a Python dictionary with keys 'relevant_info' (a list of relevant pieces of information) 
        and 'synthesis' (a brief summary of how this information relates to the query).
        """

        if api == "groq":
            response = self.groq_client.chat.completions.create(
                model="llama3-1-small",
                messages=[
                    {
                        "role": "system",
                        "content": "You are an AI memory retrieval system. Your job is to find and synthesize relevant information from stored memories.",
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
                        "content": "You are an AI memory retrieval system. Your job is to find and synthesize relevant information from stored memories.",
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
                        "content": "You are an AI memory retrieval system. Your job is to find and synthesize relevant information from stored memories.",
                    },
                    {"role": "user", "content": prompt},
                ],
            )
        else:
            raise ValueError(f"Invalid API: {api}")

        retrieval_result = eval(response.choices[0].message.content)
        return retrieval_result

    def clear_short_term_memory(self):
        self.short_term_memory.clear()
