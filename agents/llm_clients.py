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


def call_openrouter(prompt: str, model: str = "google/gemini-2.5-flash-8b") -> str:
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


def call_groq(prompt: str, model: str = "openai/gpt-oss-120b") -> str:
    api_key = _require_env("GROQ_API_KEY")
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }
    payload = {
        "model": model,
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
    raise LLMError(f"Groq call failed: {last_error}")


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


def cheap_mix(prompt: str, models: Optional[Dict[str, str]] = None) -> str:
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
                return func(prompt, model_override)
            return func(prompt)  # type: ignore[arg-type]
        except LLMError as exc:
            errors[name] = str(exc)
            continue
    detail = "; ".join(f"{name}: {message}" for name, message in errors.items())
    raise LLMError(f"All providers failed ({detail})")
