import os
import openai
from typing import Optional

def get_client():
    """Return a singleton OpenAI client with the right org & key."""
    key = os.getenv("OPENAI_API_KEY")
    if not key or key.startswith("sk-your-api-key-here"):
        raise RuntimeError("OPENAI_API_KEY not set")
    
    # Use the older API format for compatibility
    openai.api_key = key
    return openai

def get_client_or_none() -> Optional[OpenAI]:
    """Return OpenAI client if available, None otherwise."""
    try:
        return get_client()
    except RuntimeError:
        return None 