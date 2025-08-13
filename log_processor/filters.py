from typing import List

from log_processor.models import LogEntry


class BaseFilter:
    def apply(self, entries: List[LogEntry]) -> List[LogEntry]:
        raise NotImplementedError


class DateFilter(BaseFilter):
    def __init__(self, date: str):
        self.target_date = date

    def apply(self, entries: List[LogEntry]) -> List[LogEntry]:
        return [
            entry
            for entry in entries
            if entry.timestamp.strftime("%Y-%d-%m") == self.target_date
        ]
