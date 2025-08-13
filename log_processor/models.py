from dataclasses import dataclass
from datetime import datetime
from typing import Any


@dataclass
class LogEntry:
    timestamp: datetime
    status: int
    url: str
    request_method: str
    response_time: float
    http_user_agent: str

    @classmethod
    def from_dict(cls, data: Any) -> "LogEntry":
        try:
            timestamp = datetime.fromisoformat(data["@timestamp"].rstrip("Z"))
            return cls(
                timestamp=timestamp,
                status=data["status"],
                url=data["url"],
                request_method=data["request_method"],
                response_time=data["response_time"],
                http_user_agent=data["http_user_agent"],
            )
        except (KeyError, ValueError) as e:
            raise ValueError(f"Ошибка при парсинге записи: {str(e)}")


@dataclass
class ReportData:
    endpoint: str
    request_count: int
    average_response_time: float
