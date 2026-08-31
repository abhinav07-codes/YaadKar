"""Configuration helpers for YaadKar."""

import os
from pathlib import Path

from dotenv import load_dotenv

DEFAULT_MODEL_NAME = "qwen/qwen3.8-27b"
DEFAULT_API_BASE_URL = "https://api.groq.com"
MODEL_NAME_ALIASES = {
    "llama-3.7b-versatile": DEFAULT_MODEL_NAME,
    "llama-3.7b": DEFAULT_MODEL_NAME,
    "llama-3.3-70b-versatile": DEFAULT_MODEL_NAME,
    "llama-3.3-70b": DEFAULT_MODEL_NAME,
    "llama-3.1-70b-versatile": DEFAULT_MODEL_NAME,
    "mixtral-8x7b-32768": DEFAULT_MODEL_NAME,
    "meta-llama/llama-3.3-70b-versatile": DEFAULT_MODEL_NAME,
    "openai/gpt-oss-20b": DEFAULT_MODEL_NAME,
    "qwen/qwen3.8-27b": DEFAULT_MODEL_NAME,
    "qwen/qwen3.6-27b": DEFAULT_MODEL_NAME,
}


def normalize_model_name(model_name: str | None) -> str:
    """Normalize common Groq model typos to a known working value."""
    if not model_name:
        return DEFAULT_MODEL_NAME

    normalized = model_name.strip()
    if not normalized:
        return DEFAULT_MODEL_NAME

    lowercase = normalized.lower()
    return MODEL_NAME_ALIASES.get(lowercase, normalized)


def normalize_groq_base_url(base_url: str | None) -> str:
    """Return the Groq API root; the SDK appends /openai/v1 automatically."""
    normalized = (base_url or DEFAULT_API_BASE_URL).strip().rstrip("/")
    if not normalized:
        return DEFAULT_API_BASE_URL

    for suffix in ("/openai/v1", "/openai"):
        if normalized.lower().endswith(suffix):
            normalized = normalized[: -len(suffix)]
            break

    return normalized or DEFAULT_API_BASE_URL


BASE_DIR = Path(__file__).resolve().parent.parent
ENV_PATH = BASE_DIR / ".env"
load_dotenv(ENV_PATH, override=False)

GROQ_API_KEY = os.getenv("GROQ_API_KEY", "").strip()
MODEL_NAME = normalize_model_name(os.getenv("MODEL_NAME", DEFAULT_MODEL_NAME))
API_BASE_URL = normalize_groq_base_url(os.getenv("GROQ_API_BASE", DEFAULT_API_BASE_URL))
