"""Unit tests for WaterWise AI service integration.

Uses mocked Gemini client to verify SDK calls, safety pre-flight blocking,
credential handling, model configuration, and graceful exception management.
"""

from __future__ import annotations

from unittest.mock import MagicMock, patch
import pytest

from waterwise.ai_service import GeminiExplainerService, MAX_HISTORY_MESSAGES
from waterwise import config


class MockGenAIResponse:
    """Mock for google.genai response structure."""
    def __init__(self, text: str):
        self.text = text


class TestGeminiExplainerService:
    """Test AI service interactions, safety intercepts, and mock generation."""

    def test_missing_credentials_handling(self):
        """Should return configuration notice without crashing when key is absent."""
        with patch.object(config, "get_api_key", return_value=None):
            service = GeminiExplainerService(api_key=None, from_config_if_none=False)
            resp = service.explain("Explain the water treatment process.")
            assert resp.is_live_ai is False
            assert "API Configuration Notice" in resp.content
            assert resp.error_detail == "API credentials missing."

    def test_safety_check_blocks_before_invoking_gemini(self):
        """Prohibited prompt must be rejected before Gemini client is invoked."""
        mock_client = MagicMock()
        service = GeminiExplainerService(api_key="fake-test-key-12345")
        service._client = mock_client

        # Submit prohibited arrival query
        resp = service.explain("When will the water supply arrive in my area?")
        assert resp.is_refusal is True
        assert resp.is_live_ai is False
        assert "cannot predict or verify the arrival time" in resp.content

        # Verify client.models.generate_content was NEVER called
        mock_client.models.generate_content.assert_not_called()

    def test_successful_mocked_generation(self):
        """Allowed prompt successfully invokes mocked Gemini model."""
        mock_client = MagicMock()
        mock_client.models.generate_content.return_value = MockGenAIResponse(
            "Water treatment consists of screening, coagulation, sedimentation, filtration, and disinfection."
        )

        service = GeminiExplainerService(api_key="fake-test-key-12345", model_name="gemini-3.6-flash")
        service._client = mock_client

        resp = service.explain("Explain the water treatment process.")
        assert resp.is_live_ai is True
        assert resp.is_refusal is False
        assert resp.model_used == "gemini-3.6-flash"
        assert "Water treatment consists of" in resp.content

        # Verify SDK was called once
        mock_client.models.generate_content.assert_called_once()

    def test_model_configuration_respected(self):
        """Service should use explicitly configured model (e.g. gemini-3.8-flash)."""
        mock_client = MagicMock()
        mock_client.models.generate_content.return_value = MockGenAIResponse("Distribution explanation.")

        service = GeminiExplainerService(api_key="fake-test-key-12345", model_name="gemini-3.8-flash")
        service._client = mock_client

        resp = service.explain("How does water distribution work?")
        assert resp.model_used == "gemini-3.8-flash"
        
        # Verify model argument passed to generate_content
        call_kwargs = mock_client.models.generate_content.call_args.kwargs
        assert call_kwargs["model"] == "gemini-3.8-flash"

    def test_conversation_history_bounded(self):
        """Service must bound conversation history to MAX_HISTORY_MESSAGES."""
        mock_client = MagicMock()
        mock_client.models.generate_content.return_value = MockGenAIResponse("Answer.")
        service = GeminiExplainerService(api_key="fake-test-key-12345")
        service._client = mock_client

        # Create 20 historical messages
        history = [{"role": "user" if i % 2 == 0 else "assistant", "content": f"Message {i}"} for i in range(20)]

        service.explain("What causes low water pressure?", chat_history=history)

        call_kwargs = mock_client.models.generate_content.call_args.kwargs
        contents = call_kwargs["contents"]
        # History messages + 1 current prompt = MAX_HISTORY_MESSAGES + 1
        assert len(contents) <= MAX_HISTORY_MESSAGES + 1

    def test_model_not_found_actionable_error(self):
        """404 / NotFound error should explain model access and suggest alternative."""
        mock_client = MagicMock()
        mock_client.models.generate_content.side_effect = Exception("404 Model not found: models/gemini-3.8-flash")

        service = GeminiExplainerService(api_key="fake-test-key-12345", model_name="gemini-3.8-flash")
        service._client = mock_client

        resp = service.explain("What are some water conservation tips?")
        assert resp.is_live_ai is False
        assert "Configured Model Inaccessible" in resp.content
        assert "GEMINI_MODEL=gemini-3.6-flash" in resp.content

    def test_invalid_api_key_handled(self):
        """401/403 should display authentication notice without leaking key."""
        mock_client = MagicMock()
        secret_key = "AIzaSySecretTestingKeyThatShouldNeverLeak"
        mock_client.models.generate_content.side_effect = Exception(f"403 API key {secret_key} is invalid.")

        service = GeminiExplainerService(api_key=secret_key)
        service._client = mock_client

        resp = service.explain("Explain the water treatment process.")
        assert resp.is_live_ai is False
        assert "Authentication Failed" in resp.content
        # Ensure raw secret is not leaked in user content
        assert secret_key not in resp.content

    def test_rate_limit_quota_exceeded_handled(self):
        """429 Resource Exhausted should return friendly quota notice."""
        mock_client = MagicMock()
        mock_client.models.generate_content.side_effect = Exception("429 RESOURCE_EXHAUSTED: Quota exceeded")

        service = GeminiExplainerService(api_key="fake-test-key-12345")
        service._client = mock_client

        resp = service.explain("Explain the water treatment process.")
        assert resp.is_live_ai is False
        assert "Rate Limit / Quota Exceeded" in resp.content

    def test_network_timeout_handled(self):
        """Timeout errors should return connection guidance without crashing."""
        mock_client = MagicMock()
        mock_client.models.generate_content.side_effect = Exception("Connection timed out after 30 seconds")

        service = GeminiExplainerService(api_key="fake-test-key-12345")
        service._client = mock_client

        resp = service.explain("Explain the water treatment process.")
        assert resp.is_live_ai is False
        assert "Network Connection Issue" in resp.content

    def test_empty_response_handled_gracefully(self):
        """Provider returning empty text should produce a clean notice."""
        mock_client = MagicMock()
        mock_client.models.generate_content.return_value = MockGenAIResponse("   ")

        service = GeminiExplainerService(api_key="fake-test-key-12345")
        service._client = mock_client

        resp = service.explain("Explain the water treatment process.")
        assert resp.is_live_ai is False
        assert "empty response" in resp.content.lower()


class TestConfigModule:
    """Test environment configuration priorities and safe masking."""

    def test_masked_api_key_short(self):
        with patch.object(config, "get_api_key", return_value="12345"):
            assert config.get_masked_api_key() == "****"

    def test_masked_api_key_normal(self):
        with patch.object(config, "get_api_key", return_value="AIzaSyDummyKeyForTesting"):
            masked = config.get_masked_api_key()
            assert masked.startswith("AIza")
            assert masked.endswith("ting")
            assert "Dummy" not in masked

    def test_masked_api_key_none(self):
        with patch.object(config, "get_api_key", return_value=None):
            assert config.get_masked_api_key() == "Not Configured"
