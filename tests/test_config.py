"""
Unit tests for environment-based configuration behavior.
"""

import importlib

from src import pipeline


def test_db_config_uses_default_host(monkeypatch):
    """Verify DB_HOST defaults to localhost when not explicitly set."""

    monkeypatch.delenv("DB_HOST", raising=False)

    importlib.reload(pipeline)

    assert pipeline.DB_CONFIG["host"] == "localhost"
