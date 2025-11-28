"""Tests for llm_clients provider selection functionality."""
from __future__ import annotations

import os
from unittest.mock import MagicMock, patch

import pytest

from agents.llm_clients import LLMError, call_provider, cheap_mix


class TestProviderSelection:
    """Test provider-specific call behavior."""

    def test_call_provider_uses_specified_provider(self):
        """Test that call_provider uses the provider from APOCALYPSAI_PROVIDER env var."""
        with patch.dict(os.environ, {"APOCALYPSAI_PROVIDER": "gemini"}):
            with patch("agents.llm_clients.call_gemini") as mock_gemini:
                mock_gemini.return_value = "test response"
                response, provider = call_provider("test prompt")
                assert response == "test response"
                assert provider == "gemini"
                mock_gemini.assert_called_once()

    def test_call_provider_groq(self):
        """Test that call_provider uses Groq when specified."""
        with patch.dict(os.environ, {"APOCALYPSAI_PROVIDER": "groq"}):
            with patch("agents.llm_clients.call_groq") as mock_groq:
                mock_groq.return_value = "groq response"
                response, provider = call_provider("test prompt")
                assert response == "groq response"
                assert provider == "groq"
                mock_groq.assert_called_once()

    def test_call_provider_openrouter(self):
        """Test that call_provider uses OpenRouter when specified."""
        with patch.dict(os.environ, {"APOCALYPSAI_PROVIDER": "openrouter"}):
            with patch("agents.llm_clients.call_openrouter") as mock_or:
                mock_or.return_value = "openrouter response"
                response, provider = call_provider("test prompt")
                assert response == "openrouter response"
                assert provider == "openrouter"
                mock_or.assert_called_once()

    def test_call_provider_fails_when_specified_provider_fails(self):
        """Test that call_provider raises error when specified provider fails."""
        with patch.dict(os.environ, {"APOCALYPSAI_PROVIDER": "gemini"}):
            with patch("agents.llm_clients.call_gemini") as mock_gemini:
                mock_gemini.side_effect = LLMError("Gemini API error")
                with pytest.raises(LLMError) as exc_info:
                    call_provider("test prompt")
                assert "Provider 'gemini' failed" in str(exc_info.value)

    def test_call_provider_no_fallback_on_specified_provider(self):
        """Test that call_provider doesn't fall back when a specific provider is set."""
        with patch.dict(os.environ, {"APOCALYPSAI_PROVIDER": "groq"}):
            with patch("agents.llm_clients.call_groq") as mock_groq:
                with patch("agents.llm_clients.call_gemini") as mock_gemini:
                    mock_groq.side_effect = LLMError("Groq API error")
                    with pytest.raises(LLMError):
                        call_provider("test prompt")
                    # Gemini should not be called
                    mock_gemini.assert_not_called()

    def test_call_provider_falls_back_when_no_provider_specified(self):
        """Test that call_provider uses cheap_mix when no provider is specified."""
        with patch.dict(os.environ, {}, clear=True):
            with patch("agents.llm_clients.call_groq") as mock_groq:
                with patch("agents.llm_clients.call_gemini") as mock_gemini:
                    mock_groq.side_effect = LLMError("Groq failed")
                    mock_gemini.return_value = "gemini response"
                    response, provider = call_provider("test prompt")
                    assert response == "gemini response"
                    assert provider == "gemini"
                    mock_groq.assert_called_once()
                    mock_gemini.assert_called_once()

    def test_call_provider_cheap_mix_mode(self):
        """Test that call_provider uses fallback when provider is 'cheap_mix'."""
        with patch.dict(os.environ, {"APOCALYPSAI_PROVIDER": "cheap_mix"}):
            with patch("agents.llm_clients.call_groq") as mock_groq:
                mock_groq.return_value = "groq response"
                response, provider = call_provider("test prompt")
                assert response == "groq response"
                assert provider == "groq"

    def test_call_provider_with_model_override(self):
        """Test that call_provider passes model overrides to the provider."""
        with patch.dict(os.environ, {"APOCALYPSAI_PROVIDER": "gemini"}):
            with patch("agents.llm_clients.call_gemini") as mock_gemini:
                mock_gemini.return_value = "test response"
                models = {"gemini": "custom-model"}
                response, provider = call_provider("test prompt", models)
                assert response == "test response"
                assert provider == "gemini"
                mock_gemini.assert_called_once_with("test prompt", "custom-model")

    def test_cheap_mix_backward_compatibility(self):
        """Test that cheap_mix still works for backward compatibility."""
        with patch("agents.llm_clients.call_groq") as mock_groq:
            mock_groq.return_value = "groq response"
            response = cheap_mix("test prompt")
            assert response == "groq response"
            mock_groq.assert_called_once()
