"""Unit tests for UI styling, formatters, and Streamlit components."""

from __future__ import annotations

from waterwise import ui
from waterwise import config
from waterwise import prompts


def test_custom_css_tokens_defined():
    """Verify custom CSS has required color and structural styling."""
    assert "ww-hero-container" in ui.CUSTOM_CSS
    assert "ww-card" in ui.CUSTOM_CSS
    assert "#0284c7" in ui.CUSTOM_CSS  # Teal/Blue primary
    assert "#f8fafc" in ui.CUSTOM_CSS  # Clean surface background


def test_required_questions_count_and_content():
    """Verify official required questions are present."""
    assert len(prompts.REQUIRED_ASSIGNMENT_QUESTIONS) == 4
    assert any("treatment" in q.lower() for q in prompts.REQUIRED_ASSIGNMENT_QUESTIONS)
    assert any("distribution" in q.lower() for q in prompts.REQUIRED_ASSIGNMENT_QUESTIONS)
    assert any("pressure" in q.lower() for q in prompts.REQUIRED_ASSIGNMENT_QUESTIONS)
    assert any("conservation" in q.lower() for q in prompts.REQUIRED_ASSIGNMENT_QUESTIONS)


def test_system_prompt_bounds():
    """Verify system instruction contains clear educational instructions and disclaimers."""
    assert "WaterWise AI" in prompts.SYSTEM_INSTRUCTION
    assert "Simple Explanation" in prompts.SYSTEM_INSTRUCTION
    assert "How It Works" in prompts.SYSTEM_INSTRUCTION
    assert "Why It Matters" in prompts.SYSTEM_INSTRUCTION
    assert "Key Takeaway" in prompts.SYSTEM_INSTRUCTION
    assert "DO NOT have access to live municipal SCADA" in prompts.SYSTEM_INSTRUCTION


def test_config_summary_keys():
    """Ensure config summary dictionary contains safe diagnostic keys."""
    summary = config.get_config_summary()
    assert "model" in summary
    assert "api_configured" in summary
    assert "key_preview" in summary
    # Raw API key must never be the value of key_preview
    assert "AIza" not in summary["key_preview"] or "..." in summary["key_preview"]
