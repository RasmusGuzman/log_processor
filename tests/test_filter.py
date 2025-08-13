# tests/test_filters.py
from log_processor.filters import DateFilter
from log_processor.models import LogEntry


def test_date_filter(log_entries):
    entries = [LogEntry.from_dict(entry) for entry in log_entries]
    filter = DateFilter("2025-22-06")  # формат YYYY-DD-MM

    filtered = filter.apply(entries)
    assert len(filtered) == 2
    assert all(
        entry.timestamp.strftime("%Y-%d-%m") == "2025-22-06" for entry in filtered
    )


def test_date_filter_no_matches(log_entries):
    entries = [LogEntry.from_dict(entry) for entry in log_entries]
    filter = DateFilter("2025-23-06")  # другая дата

    filtered = filter.apply(entries)
    assert len(filtered) == 0
