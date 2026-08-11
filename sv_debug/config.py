"""Environment/config helpers. Never commit real API keys."""

from __future__ import annotations

import os
from pathlib import Path

from dotenv import load_dotenv

_ENV_LOADED = False
_PLACEHOLDER_KEYS = {
    "",
    "your_gemini_api_key_here",
    "your_api_key_here",
}


def load_env() -> None:
    """Load repo-root .env once (safe to call repeatedly)."""
    global _ENV_LOADED
    if _ENV_LOADED:
        return
    env_path = Path(__file__).resolve().parent.parent / ".env"
    load_dotenv(env_path)
    _ENV_LOADED = True


def _api_key() -> str | None:
    load_env()
    return os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")


def has_api_key() -> bool:
    """Return True when a non-placeholder Gemini API key is configured."""
    key = _api_key()
    return bool(key and key.strip() not in _PLACEHOLDER_KEYS)


def demo_mode_enabled() -> bool:
    """Return True when DEMO_MODE is on (default: on when no real API key is set)."""
    load_env()
    raw = os.getenv("DEMO_MODE")
    if raw is not None:
        return raw.strip().lower() in {"1", "true", "yes", "on"}
    return not has_api_key()


def require_api_key() -> str:
    """Return a real API key or raise a clear setup error."""
    key = _api_key()
    if not key or key.strip() in _PLACEHOLDER_KEYS:
        raise ValueError(
            "Missing Gemini API key. Open the .env file in this project and replace "
            "your_gemini_api_key_here with a real key from https://aistudio.google.com/apikey "
            "or keep DEMO_MODE=true to try the app without a key."
        )
    return key.strip()
