from typing import Any, List
from config import settings


def openai_available() -> bool:
    return bool(settings.openai_api_key) and not settings.mock_mode


def call_openai_chat(messages: List[dict], max_tokens: int = 400) -> str:
    """Call OpenAI in a way compatible with openai<1.0 and openai>=1.0.
    Returns the assistant text or raises the underlying exception.
    """
    try:
        import openai
    except Exception:
        raise

    # new client API (openai>=1.0.0)
    if hasattr(openai, "OpenAI"):
        client = openai.OpenAI(api_key=settings.openai_api_key) if settings.openai_api_key else openai.OpenAI()
        resp = client.chat.completions.create(model=settings.openai_model, messages=messages, max_tokens=max_tokens)
        # new API returns choices[0].message.content
        return resp.choices[0].message.content

    # older API
    openai.api_key = settings.openai_api_key
    resp = openai.ChatCompletion.create(model=settings.openai_model, messages=messages, max_tokens=max_tokens)
    return resp.choices[0].message.content
