"""Pytest fixtures and configuration."""

import os

import pytest

# Ensure Qt runs headlessly in test environments
os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")


@pytest.fixture
def sample_recipient() -> str:
    """Provide a sample recipient name for tests."""
    return "Antigravity"
