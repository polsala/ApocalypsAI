from __future__ import annotations

import json
import os
import random
import re
import time
from typing import Dict, Optional

import requests


class LLMError(RuntimeError):
    """Raised when no LLM provider returns a usable response."""


_ANSI_RE = re.compile(r"\x1b\[[0-9;]*[A-Za-z]")


def _strip_ansi(text: str) -> str:
    return _ANSI_RE.sub("", text)


def _strip_code_fences(text: str) -> str:
    cleaned = text.strip()
    if cleaned.startswith("```") and cleaned.endswith("```"):
        lines = cleaned.splitlines()
        if len(lines) >= 2:
            lines = lines[1:-1]
            cleaned = "\n".join(lines).strip()
    return cleaned


def _clean_response_text(text: str) -> str:
    return _strip_code_fences(_strip_ansi(text)).strip()


def _sleep_with_jitter(attempt: int) -> None:
    base = 0.5 * (2 ** attempt)
    wait = min(base + random.uniform(0, 0.5), 4.0)
    time.sleep(wait)


def _require_env(name: str) -> str:
    value = os.environ.get(name)
    if not value:
        raise LLMError(f"Provider unavailable: missing environment variable {name}")
    return value


def _post_json(
    url: str,
    *,
    headers: Dict[str, str],
    payload: Dict[str, object],
    timeout: float = 60.0,
) -> Dict[str, object]:
    response = requests.post(url, headers=headers, json=payload, timeout=timeout)
    if response.status_code >= 400:
        raise LLMError(f"HTTP {response.status_code}: {response.text.strip()}")
    try:
        return response.json()
    except json.JSONDecodeError as exc:
        raise LLMError(f"Failed to decode JSON response: {exc}") from exc


def call_openrouter(prompt: str, model: str = "kwaipilot/kat-coder-pro:free") -> str:
    api_key = _require_env("OPENROUTER_API_KEY")
    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }
    payload = {
        "model": model,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.2,
    }
    last_error: Optional[Exception] = None
    for attempt in range(3):
        try:
            data = _post_json(url, headers=headers, payload=payload)
            choices = data.get("choices")
            if not choices:
                raise LLMError("OpenRouter response missing choices")
            message = choices[0].get("message") or {}
            content = message.get("content")
            if not isinstance(content, str):
                raise LLMError("OpenRouter message missing text content")
            return _clean_response_text(content)
        except (LLMError, requests.RequestException) as exc:
            last_error = exc
            if attempt == 2:
                break
            _sleep_with_jitter(attempt)
    raise LLMError(f"OpenRouter call failed: {last_error}")


def call_groq(
    prompt: str,
    model: Optional[str] = None,
    model_pool: Optional[list[str]] = None,
) -> str:
    """
    Call Groq API with configurable model fallback.
    
    Args:
        prompt: The prompt to send to the model
        model: Single model to use (overrides pool if provided)
        model_pool: List of models to try in sequence. If not provided,
                   reads from GROQ_MODEL_POOL env var (JSON format),
                   or uses default pool.
    
    Default pool: ["openai/gpt-oss-120b", "openai/gpt-oss-20b", "qwen/qwen3-32b"]
    
    Returns:
        The model's response text
        
    Raises:
        LLMError: If all models in the pool fail
    """
    api_key = _require_env("GROQ_API_KEY")
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }
    
    # Determine the model pool to use
    if model is not None:
        # Single model provided - use it with retries
        models_to_try = [model]
    elif model_pool is not None:
        # Model pool provided as argument
        models_to_try = model_pool
    else:
        # Check environment variable for custom pool
        pool_env = os.environ.get("GROQ_MODEL_POOL")
        if pool_env:
            try:
                models_to_try = json.loads(pool_env)
                if not isinstance(models_to_try, list):
                    raise ValueError("GROQ_MODEL_POOL must be a JSON array")
            except (json.JSONDecodeError, ValueError) as exc:
                raise LLMError(f"Invalid GROQ_MODEL_POOL format: {exc}") from exc
        else:
            # Use default fallback pool
            models_to_try = [
                "openai/gpt-oss-120b",
                "openai/gpt-oss-20b",
                "qwen/qwen3-32b",
            ]
    
    # Try each model in the pool
    all_errors: Dict[str, str] = {}
    for model_name in models_to_try:
        payload = {
            "model": model_name,
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.1,
        }
        last_error: Optional[Exception] = None
        for attempt in range(3):
            try:
                data = _post_json(url, headers=headers, payload=payload)
                choices = data.get("choices")
                if not choices:
                    raise LLMError("Groq response missing choices")
                message = choices[0].get("message") or {}
                content = message.get("content")
                if not isinstance(content, str):
                    raise LLMError("Groq message missing text content")
                return _clean_response_text(content)
            except (LLMError, requests.RequestException) as exc:
                last_error = exc
                if attempt == 2:
                    break
                _sleep_with_jitter(attempt)
        # Record the error for this model and try the next one
        all_errors[model_name] = str(last_error)
    
    # All models failed
    error_details = "; ".join(f"{model}: {error}" for model, error in all_errors.items())
    raise LLMError(f"All Groq models failed ({error_details})")


def call_gemini(prompt: str, model: str = "gemini-2.5-flash") -> str:
    api_key = _require_env("GOOGLE_API_KEY")
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent"
    params = {"key": api_key}
    headers = {"Content-Type": "application/json"}
    payload = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {"temperature": 0.2},
    }
    last_error: Optional[Exception] = None
    for attempt in range(3):
        try:
            response = requests.post(url, params=params, headers=headers, json=payload, timeout=60.0)
            if response.status_code >= 400:
                raise LLMError(f"HTTP {response.status_code}: {response.text.strip()}")
            data = response.json()
            candidates = data.get("candidates")
            if not candidates:
                raise LLMError("Gemini response missing candidates")
            parts = candidates[0].get("content", {}).get("parts", [])
            if not parts:
                raise LLMError("Gemini candidate missing content parts")
            text = parts[0].get("text")
            if not isinstance(text, str):
                raise LLMError("Gemini content missing text")
            return _clean_response_text(text)
        except (LLMError, requests.RequestException) as exc:
            last_error = exc
            if attempt == 2:
                break
            _sleep_with_jitter(attempt)
    raise LLMError(f"Gemini call failed: {last_error}")


def call_provider(prompt: str, models: Optional[Dict[str, str]] = None) -> tuple[str, str]:
    """
    Call the LLM provider specified by APOCALYPSAI_PROVIDER env var.
    Returns tuple of (response_text, provider_name).
    Raises LLMError if the specified provider fails.
    
    If APOCALYPSAI_PROVIDER is not set or is set to an unknown value,
    falls back to cheap_mix behavior (tries providers in order).
    """
    provider = os.environ.get("APOCALYPSAI_PROVIDER", "").lower()
    
    provider_map = {
        "groq": call_groq,
        "gemini": call_gemini,
        "openrouter": call_openrouter,
    }
    
    # If a specific provider is requested, use only that one
    if provider and provider in provider_map:
        func = provider_map[provider]
        model_override = (models or {}).get(provider)
        try:
            if model_override:
                response = func(prompt, model_override)
            else:
                response = func(prompt)  # type: ignore[arg-type]
            return (response, provider)
        except LLMError as exc:
            raise LLMError(f"Provider '{provider}' failed: {exc}") from exc
    
    # If no provider specified, provider is unknown, or explicitly set to "cheap_mix",
    # use fallback behavior
    return _cheap_mix_impl(prompt, models)


def _cheap_mix_impl(prompt: str, models: Optional[Dict[str, str]] = None) -> tuple[str, str]:
    """Internal implementation of cheap_mix with provider fallback."""
    providers = [
        ("groq", call_groq),
        ("gemini", call_gemini),
        ("openrouter", call_openrouter),
    ]
    errors = {}
    for name, func in providers:
        model_override = (models or {}).get(name)
        try:
            if model_override:
                response = func(prompt, model_override)
            else:
                response = func(prompt)  # type: ignore[arg-type]
            return (response, name)
        except LLMError as exc:
            errors[name] = str(exc)
            continue
    detail = "; ".join(f"{name}: {message}" for name, message in errors.items())
    raise LLMError(f"All providers failed ({detail})")


def cheap_mix(prompt: str, models: Optional[Dict[str, str]] = None) -> str:
    """
    Legacy function for backward compatibility.
    Try providers in order: Groq -> Gemini -> OpenRouter.
    Return first successful text response.
    Raise LLMError if all fail.
    """
    response, _ = _cheap_mix_impl(prompt, models)
    return response
