# app/services/openai_client.py
from __future__ import annotations

import os
from typing import Optional, Any

# Try the modern client first (openai>=1.x)
_HAVING_V1 = False
OpenAI = None  # type: ignore[assignment]

try:
    from openai import OpenAI as _OpenAI  # modern SDK
    OpenAI = _OpenAI                      # expose name for type checkers
    _HAVING_V1 = True
except Exception:
    # Fall back to legacy module (openai==0.x)
    import openai as _openai              # legacy SDK
    _openai  # keep for lints


def get_client_or_none() -> Optional[Any]:
    """
    Return an OpenAI client object if API key is set; otherwise None.

    - If modern SDK is installed (openai>=1.x), returns OpenAI(...)
    - If legacy SDK (openai==0.x), returns the legacy 'openai' module after setting api_key
    """
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        return None

    # Optional: allow overriding base URL / org if you use a proxy or Azure
    base_url = os.getenv("OPENAI_BASE_URL")  # e.g., "https://api.openai.com/v1"
    organization = os.getenv("OPENAI_ORG")

    if _HAVING_V1:
        kwargs = {"api_key": api_key}
        if base_url:
            kwargs["base_url"] = base_url
        if organization:
            kwargs["organization"] = organization
        return OpenAI(**kwargs)

    # Legacy path
    import openai as _openai  # type: ignore[no-redef]
    _openai.api_key = api_key
    if organization:
        _openai.organization = organization
    # Legacy SDK doesn't support base_url in the same way; skip unless you've customized a proxy.
    return _openai


def get_client():
    """Return a singleton OpenAI client with the right org & key."""
    key = os.getenv("OPENAI_API_KEY")
    if not key or key.startswith("sk-your-api-key-here"):
        raise RuntimeError("OPENAI_API_KEY not set")
    
    # Use the older API format for compatibility
    import openai as _openai
    _openai.api_key = key
    return _openai