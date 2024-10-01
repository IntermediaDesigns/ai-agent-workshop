from typing import Literal
from src.clients.openai_client import get_openai_response
from src.clients.groq_client import get_groq_response
from src.clients.openrouter_client import get_openrouter_response

ClientType = Literal["openai", "groq", "openrouter"]

def get_llm_response(client: ClientType, prompt: str, json_mode: bool = False) -> str:
    if client == "openai":
        return get_openai_response(prompt, json_mode)
    elif client == "groq":
        return get_groq_response(prompt, json_mode)
    elif client == "openrouter":
        return get_openrouter_response(prompt, json_mode)
    else:
        raise ValueError(f"Invalid client: {client}")