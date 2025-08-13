from datetime import datetime

import pytest

from log_processor.models import LogEntry
from log_processor.reporter import AverageReport, ReporterFactory


def test_average_report(log_entries):
    entries = [LogEntry.from_dict(entry) for entry in log_entries]
    reporter = AverageReport()
    report = reporter.generate(entries)

    assert len(report) == 2
    assert report[0].endpoint == "/api/context/1"
    assert report[0].request_count == 1
    assert report[0].average_response_time == 0.024

    assert report[1].endpoint == "/api/context/2"
    assert report[1].request_count == 1
    assert report[1].average_response_time == 0.028


def test_average_report_multiple_requests():
    entries = [
        LogEntry(
            timestamp=datetime.now(),
            status=200,
            url="/api/test",
            request_method="GET",
            response_time=0.02,
            http_user_agent="Test",
        ),
        LogEntry(
            timestamp=datetime.now(),
            status=200,
            url="/api/test",
            request_method="GET",
            response_time=0.03,
            http_user_agent="Test",
        ),
    ]

    reporter = AverageReport()
    report = reporter.generate(entries)

    assert len(report) == 1
    assert report[0].endpoint == "/api/test"
    assert report[0].request_count == 2
    assert report[0].average_response_time == 0.025


def test_reporter_factory():
    reporter = ReporterFactory.get_reporter("average")
    assert isinstance(reporter, AverageReport)

    with pytest.raises(ValueError):
        ReporterFactory.get_reporter("unknown_type")
