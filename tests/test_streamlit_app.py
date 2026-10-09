"""End-to-end component tests using Streamlit AppTest framework.

Verifies page rendering, widgets, topic button triggers, and state management.
"""

from __future__ import annotations

import pytest
from streamlit.testing.v1 import AppTest


def test_app_startup_rendering():
    """Verify Streamlit app initializes without errors in zero-credential mode."""
    at = AppTest.from_file("../app.py", default_timeout=10)
    at.run()
    assert not at.exception, f"App raised an exception on startup: {at.exception}"

    # Verify title and sidebar elements
    assert "WaterWise AI" in at.sidebar.caption[0].value
    # Verify tabs exist
    assert len(at.tabs) >= 3


def test_app_click_suggested_question():
    """Verify clicking a suggested question triggers question processing."""
    at = AppTest.from_file("../app.py", default_timeout=10)
    at.run()

    # Find and click the 'Explain the water treatment process.' button
    treatment_btn = None
    for btn in at.button:
        if "treatment" in btn.label.lower():
            treatment_btn = btn
            break

    assert treatment_btn is not None, "Treatment question button not found"
    treatment_btn.click().run()
    assert not at.exception

    # Conversation history should now contain the question and response
    messages = at.session_state["messages"]
    assert len(messages) >= 2
    assert messages[0]["role"] == "user"
    assert "treatment" in messages[0]["content"].lower()
    assert messages[1]["role"] == "assistant"


def test_app_clear_conversation():
    """Verify clear conversation button resets history."""
    at = AppTest.from_file("../app.py", default_timeout=10)
    at.run()

    # Add dummy message to session state
    at.session_state["messages"] = [{"role": "user", "content": "Hello"}]
    at.run()
    assert len(at.session_state["messages"]) == 1

    # Find Clear Conversation button
    clear_btn = None
    for btn in at.sidebar.button:
        if "Clear" in btn.label:
            clear_btn = btn
            break

    assert clear_btn is not None
    clear_btn.click().run()
    assert len(at.session_state["messages"]) == 0
