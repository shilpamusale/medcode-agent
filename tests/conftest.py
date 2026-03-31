"""
Shared pytest fixtures — stubs out all external API calls.
Unit tests never hit live endpoints.
"""
from unittest.mock import AsyncMock, MagicMock

import pytest


@pytest.fixture
def mock_anthropic_client():
    client = MagicMock()
    client.messages.create = AsyncMock(return_value=MagicMock(
        content=[MagicMock(text='{"codes": [], "confidence": 0.9}')]
    ))
    return client


@pytest.fixture
def mock_umls_client():
    client = MagicMock()
    client.lookup = AsyncMock(return_value={
        "cui": "C0020538",
        "name": "Hypertension",
        "semanticTypes": ["T047"]
    })
    return client


@pytest.fixture
def sample_clinical_note() -> str:
    """Minimal synthetic note — no real PHI."""
    return (
        "Patient presents with essential hypertension and type 2 diabetes mellitus. "
        "Blood pressure 145/92. HbA1c 8.1%. Started on metformin 500mg BID. "
        "Follow-up in 3 months."
    )
