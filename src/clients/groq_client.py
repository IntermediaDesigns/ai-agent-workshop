from groq import Groq
from config.config import GROQ_API_KEY, GROQ_MODELS

client = Groq(api_key=GROQ_API_KEY)

def get_groq_response(prompt: str, json_mode: bool = False) -> str:
    for model in GROQ_MODELS:
        try:
            kwargs = {
                "model": model,
                "messages": [{"role": "user", "content": prompt}]
            }
            if json_mode:
                kwargs["response_format"] = {"type": "json_object"}

            response = client.chat.completions.create(**kwargs)
            return response.choices[0].message.content
        except Exception as e:
            print(f"Error with model {model}: {e}")
    
    raise Exception("All Groq models failed")