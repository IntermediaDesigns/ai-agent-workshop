from openai import OpenAI
from config.config import OPENAI_API_KEY, OPENAI_MODEL

client = OpenAI(api_key=OPENAI_API_KEY)

def get_openai_response(prompt: str, json_mode: bool = False) -> str:
    kwargs = {
        "model": OPENAI_MODEL,
        "messages": [{"role": "user", "content": prompt}]
    }

    if json_mode:
        kwargs["response_format"] = {"type": "json_object"}

    response = client.chat.completions.create(**kwargs)
    return response.choices[0].message.content