"""Unit tests for WaterWise AI knowledge base and offline educational modules.

Verifies completeness of educational content, process diagrams, offline answers,
and terminology glossary.
"""

from __future__ import annotations

import pytest
from waterwise import knowledge
from waterwise import prompts


class TestKnowledgeBaseCompleteness:
    """Verify that all core learning pillars and topics exist."""

    def test_four_core_topics_present(self):
        topic_ids = [t.id for t in knowledge.TOPICS]
        assert "treatment" in topic_ids
        assert "distribution" in topic_ids
        assert "pressure" in topic_ids
        assert "conservation" in topic_ids
        assert len(knowledge.TOPICS) == 4

    def test_topic_details_and_diagrams_populated(self):
        for topic in knowledge.TOPICS:
            assert topic.title
            assert topic.subtitle
            assert len(topic.summary) > 30
            assert "│" in topic.diagram_ascii or "\n" in topic.diagram_ascii
            assert len(topic.key_stages) >= 4
            assert len(topic.faq) >= 2
            assert topic.sample_prompt

    def test_treatment_stages_sequence(self):
        treatment = knowledge.TOPIC_TREATMENT
        stage_names = " ".join([s["name"] for s in treatment.key_stages]).lower()
        assert "screening" in stage_names
        assert "coagulation" in stage_names
        assert "flocculation" in stage_names
        assert "sedimentation" in stage_names
        assert "filtration" in stage_names
        assert "disinfection" in stage_names

    def test_distribution_stages(self):
        distribution = knowledge.TOPIC_DISTRIBUTION
        stage_names = " ".join([s["name"] for s in distribution.key_stages]).lower()
        assert "pump" in stage_names
        assert "transmission" in stage_names
        assert "storage" in stage_names or "towers" in stage_names
        assert "distribution" in stage_names

    def test_pressure_stages(self):
        pressure = knowledge.TOPIC_PRESSURE
        stage_names = " ".join([s["name"] for s in pressure.key_stages]).lower()
        assert "elevation" in stage_names
        assert "demand" in stage_names or "peak" in stage_names
        assert "valve" in stage_names or "pipe" in stage_names

    def test_conservation_stages(self):
        conservation = knowledge.TOPIC_CONSERVATION
        stage_names = " ".join([s["name"] for s in conservation.key_stages]).lower()
        assert "leak" in stage_names
        assert "aerator" in stage_names or "fixture" in stage_names
        assert "rainwater" in stage_names or "landscaping" in stage_names

    def test_curated_offline_answers_cover_required_questions(self):
        """All 4 required assignment demonstration questions must have curated offline answers."""
        for req_q in prompts.REQUIRED_ASSIGNMENT_QUESTIONS:
            ans = knowledge.get_curated_answer(req_q)
            assert ans is not None, f"Missing curated answer for: {req_q}"
            assert len(ans) > 100
            assert "Simple Explanation" in ans
            assert "Why It Matters" in ans

    def test_glossary_entries(self):
        """Verify glossary has essential municipal terminology."""
        assert len(knowledge.GLOSSARY) >= 8
        terms = [item["term"].lower() for item in knowledge.GLOSSARY]
        assert any("potable" in t for t in terms)
        assert any("turbidity" in t for t in terms)
        assert any("coagulation" in t for t in terms)
        assert any("flocculation" in t for t in terms)
        assert any("head" in t for t in terms)
        assert any("prv" in t or "valve" in t for t in terms)
