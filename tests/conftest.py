import json

import pytest


@pytest.fixture
def sample_log_entry():
    return {
        "@timestamp": "2025-06-22T13:57:32Z",
        "status": 200,
        "url": "/api/context/...",
        "request_method": "GET",
        "response_time": 0.024,
        "http_user_agent": "Mozilla/5.0",
    }


@pytest.fixture
def log_entries():
    return [
        {
            "@timestamp": "2025-06-22T13:57:32Z",
            "status": 200,
            "url": "/api/context/1",
            "request_method": "GET",
            "response_time": 0.024,
            "http_user_agent": "Mozilla/5.0",
        },
        {
            "@timestamp": "2025-06-22T13:58:32Z",
            "status": 200,
            "url": "/api/context/2",
            "request_method": "GET",
            "response_time": 0.028,
            "http_user_agent": "Mozilla/5.0",
        },
    ]


@pytest.fixture
def temp_log_file(tmpdir, log_entries):
    file_path = tmpdir.join("test.log")
    with open(file_path, "w") as f:
        for entry in log_entries:
            f.write(json.dumps(entry) + "\n")
    return str(file_path)
