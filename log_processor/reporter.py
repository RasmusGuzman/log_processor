from collections import defaultdict
from typing import List, Dict, DefaultDict

from log_processor.models import LogEntry, ReportData


class BaseReporter:
    def generate(self, entries: List[LogEntry]) -> List[ReportData]:
        raise NotImplementedError


class AverageReport(BaseReporter):
    def generate(self, entries: List[LogEntry]) -> List[ReportData]:
        data: DefaultDict[str, Dict] = defaultdict(lambda: {"count": 0, "total_time": 0.0})

        for entry in entries:
            data[entry.url]["count"] += 1
            data[entry.url]["total_time"] += entry.response_time

        return [
            ReportData(
                endpoint=endpoint,
                request_count=stats["count"],
                average_response_time=stats["total_time"] / stats["count"],
            )
            for endpoint, stats in data.items()
        ]


class ReporterFactory:
    @staticmethod
    def get_reporter(report_type: str) -> BaseReporter:
        if report_type == "average":
            return AverageReport()
        raise ValueError(f"Неизвестный тип отчета: {report_type}")
