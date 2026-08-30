"""Pytest fixtures and configuration."""

import pytest


@pytest.fixture
def sample_recipient() -> str:
    """Provide a sample recipient name for tests."""
    return "Antigravity"
