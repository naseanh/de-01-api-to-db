"""
Unit tests for API extraction behavior.
"""

from unittest.mock import patch

import pytest
import requests

from src.pipeline import extract


@patch("src.pipeline.requests.get")
def test_extract_raises_runtime_error_on_timeout(mock_get):
    """
    Verify extract() raises RuntimeError when API request times out.
    """

    mock_get.side_effect = requests.exceptions.Timeout

    with pytest.raises(RuntimeError) as exc_info:
        extract()

    assert "timed out" in str(exc_info.value)
