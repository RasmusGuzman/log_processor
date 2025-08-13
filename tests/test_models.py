from datetime import datetime

import pytest

from log_processor.models import LogEntry


def test_log_entry_creation(sample_log_entry):
    entry = LogEntry.from_dict(sample_log_entry)
    assert entry.timestamp == datetime.fromisoformat("2025-06-22T13:57:32")
    assert entry.status == 200
    assert entry.url == "/api/context/..."
    assert entry.response_time == 0.024
    assert entry.http_user_agent == "Mozilla/5.0"


def test_invalid_log_entry():
    invalid_entry = {
        "@timestamp": "invalid-date",
        "status": 200,
        "url": "/api/context/...",
    }
    with pytest.raises(ValueError):
        LogEntry.from_dict(invalid_entry)
