"""Tests for llm_clients provider selection functionality."""
from __future__ import annotations

import json
import os
from unittest.mock import MagicMock, patch

import pytest

from agents.llm_clients import LLMError, call_groq, call_provider, cheap_mix


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


class TestGroqModelPool:
    """Test configurable model pool for call_groq fallback."""

    def test_default_model_pool(self):
        """Test that call_groq uses default model pool when no config is provided."""
        with patch.dict(os.environ, {"GROQ_API_KEY": "test_key"}):
            with patch("agents.llm_clients._post_json") as mock_post:
                mock_post.return_value = {
                    "choices": [{"message": {"content": "test response"}}]
                }
                response = call_groq("test prompt")
                assert response == "test response"
                # Should use the first model from default pool
                assert mock_post.call_args[1]["payload"]["model"] == "openai/gpt-oss-120b"

    def test_single_model_parameter(self):
        """Test that providing a single model parameter uses only that model."""
        with patch.dict(os.environ, {"GROQ_API_KEY": "test_key"}):
            with patch("agents.llm_clients._post_json") as mock_post:
                mock_post.return_value = {
                    "choices": [{"message": {"content": "test response"}}]
                }
                response = call_groq("test prompt", model="custom-model")
                assert response == "test response"
                assert mock_post.call_args[1]["payload"]["model"] == "custom-model"

    def test_model_pool_parameter(self):
        """Test that providing a model_pool parameter uses those models in sequence."""
        with patch.dict(os.environ, {"GROQ_API_KEY": "test_key"}):
            with patch("agents.llm_clients._post_json") as mock_post:
                # First model fails, second succeeds
                mock_post.side_effect = [
                    LLMError("Model 1 failed"),
                    LLMError("Model 1 failed"),
                    LLMError("Model 1 failed"),
                    {"choices": [{"message": {"content": "model 2 response"}}]},
                ]
                response = call_groq("test prompt", model_pool=["model-1", "model-2"])
                assert response == "model 2 response"
                # Verify model-1 was tried 3 times, then model-2
                calls = [call[1]["payload"]["model"] for call in mock_post.call_args_list]
                assert calls == ["model-1", "model-1", "model-1", "model-2"]

    def test_env_var_model_pool(self):
        """Test that GROQ_MODEL_POOL env var configures the model pool."""
        model_pool = ["custom-1", "custom-2", "custom-3"]
        with patch.dict(
            os.environ,
            {
                "GROQ_API_KEY": "test_key",
                "GROQ_MODEL_POOL": json.dumps(model_pool),
            },
        ):
            with patch("agents.llm_clients._post_json") as mock_post:
                mock_post.return_value = {
                    "choices": [{"message": {"content": "test response"}}]
                }
                response = call_groq("test prompt")
                assert response == "test response"
                assert mock_post.call_args[1]["payload"]["model"] == "custom-1"

    def test_fallback_to_second_model(self):
        """Test that call_groq falls back to second model when first fails."""
        with patch.dict(os.environ, {"GROQ_API_KEY": "test_key"}):
            with patch("agents.llm_clients._post_json") as mock_post:
                # First model fails all retries, second succeeds
                mock_post.side_effect = [
                    LLMError("Failed"),
                    LLMError("Failed"),
                    LLMError("Failed"),
                    {"choices": [{"message": {"content": "success from model 2"}}]},
                ]
                response = call_groq("test prompt")
                assert response == "success from model 2"
                # Verify we tried first model 3 times, then second model once
                calls = [call[1]["payload"]["model"] for call in mock_post.call_args_list]
                assert calls[:3] == ["openai/gpt-oss-120b"] * 3
                assert calls[3] == "openai/gpt-oss-20b"

    def test_fallback_to_third_model(self):
        """Test that call_groq falls back to third model when first two fail."""
        with patch.dict(os.environ, {"GROQ_API_KEY": "test_key"}):
            with patch("agents.llm_clients._post_json") as mock_post:
                # First two models fail all retries, third succeeds
                mock_post.side_effect = [
                    # Model 1 fails 3 times
                    LLMError("Failed"),
                    LLMError("Failed"),
                    LLMError("Failed"),
                    # Model 2 fails 3 times
                    LLMError("Failed"),
                    LLMError("Failed"),
                    LLMError("Failed"),
                    # Model 3 succeeds
                    {"choices": [{"message": {"content": "success from model 3"}}]},
                ]
                response = call_groq("test prompt")
                assert response == "success from model 3"
                # Verify we tried all three models
                calls = [call[1]["payload"]["model"] for call in mock_post.call_args_list]
                assert calls[:3] == ["openai/gpt-oss-120b"] * 3
                assert calls[3:6] == ["openai/gpt-oss-20b"] * 3
                assert calls[6] == "qwen/qwen3-32b"

    def test_all_models_fail(self):
        """Test that call_groq raises LLMError when all models fail."""
        with patch.dict(os.environ, {"GROQ_API_KEY": "test_key"}):
            with patch("agents.llm_clients._post_json") as mock_post:
                mock_post.side_effect = LLMError("All failed")
                with pytest.raises(LLMError) as exc_info:
                    call_groq("test prompt")
                assert "All Groq models failed" in str(exc_info.value)
                # Should have tried all 3 models with 3 retries each
                assert mock_post.call_count == 9

    def test_invalid_env_var_format(self):
        """Test that invalid GROQ_MODEL_POOL format raises LLMError."""
        with patch.dict(
            os.environ,
            {
                "GROQ_API_KEY": "test_key",
                "GROQ_MODEL_POOL": "not valid json",
            },
        ):
            with pytest.raises(LLMError) as exc_info:
                call_groq("test prompt")
            assert "Invalid GROQ_MODEL_POOL format" in str(exc_info.value)

    def test_env_var_non_array(self):
        """Test that GROQ_MODEL_POOL must be a JSON array."""
        with patch.dict(
            os.environ,
            {
                "GROQ_API_KEY": "test_key",
                "GROQ_MODEL_POOL": json.dumps({"key": "value"}),
            },
        ):
            with pytest.raises(LLMError) as exc_info:
                call_groq("test prompt")
            assert "GROQ_MODEL_POOL must be a JSON array" in str(exc_info.value)

    def test_model_parameter_takes_precedence(self):
        """Test that model parameter takes precedence over env var and default."""
        with patch.dict(
            os.environ,
            {
                "GROQ_API_KEY": "test_key",
                "GROQ_MODEL_POOL": json.dumps(["env-model"]),
            },
        ):
            with patch("agents.llm_clients._post_json") as mock_post:
                mock_post.return_value = {
                    "choices": [{"message": {"content": "test response"}}]
                }
                response = call_groq("test prompt", model="param-model")
                assert response == "test response"
                assert mock_post.call_args[1]["payload"]["model"] == "param-model"

    def test_model_pool_parameter_takes_precedence_over_env(self):
        """Test that model_pool parameter takes precedence over env var."""
        with patch.dict(
            os.environ,
            {
                "GROQ_API_KEY": "test_key",
                "GROQ_MODEL_POOL": json.dumps(["env-model"]),
            },
        ):
            with patch("agents.llm_clients._post_json") as mock_post:
                mock_post.return_value = {
                    "choices": [{"message": {"content": "test response"}}]
                }
                response = call_groq("test prompt", model_pool=["param-model"])
                assert response == "test response"
                assert mock_post.call_args[1]["payload"]["model"] == "param-model"
