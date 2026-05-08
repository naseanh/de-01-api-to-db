"""
Unit tests for API extraction behavior.
"""

from unittest.mock import Mock, patch

import requests

from src.pipeline import extract


@patch("src.pipeline.time.sleep")
@patch("src.pipeline.requests.get")
def test_extract_retries_after_timeout(mock_get, mock_sleep):
    """Verify extract() retries after a timeout and succeeds on a later attempt."""

    successful_response = Mock()
    successful_response.raise_for_status.return_value = None
    successful_response.json.return_value = {"current_weather": {}}

    mock_get.side_effect = [
        requests.exceptions.Timeout,
        successful_response,
    ]

    result = extract()

    assert result == {"current_weather": {}}
    assert mock_get.call_count == 2
    mock_sleep.assert_called_once()
