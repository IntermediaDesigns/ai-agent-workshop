from src.utils.response_handler import get_llm_response

def evaluate_responses(prompt: str, reasoning_prompt: str = None):
    if reasoning_prompt:
        prompt = f"{prompt}\n\n{reasoning_prompt}"

    openai_response = get_llm_response("openai", prompt)
    groq_response = get_llm_response("groq", prompt)
    openrouter_response = get_llm_response("openrouter", prompt)

    print(f"OpenAI Response: {openai_response}")
    print(f"\nGroq Response: {groq_response}")
    print(f"\nOpenRouter Response: {openrouter_response}")