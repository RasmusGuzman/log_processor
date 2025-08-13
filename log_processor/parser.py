import json
from typing import List

from log_processor.models import LogEntry


class LogParser:
    def __init__(self, file_paths: List[str]):
        self.file_paths = file_paths
        self.entries: List[LogEntry] = []

    def parse(self) -> List[LogEntry]:
        for path in self.file_paths:
            with open(path, "r") as f:
                for line in f:
                    try:
                        data = json.loads(line)
                        # Используем фабричный метод для создания объекта
                        self.entries.append(LogEntry.from_dict(data))
                    except (json.JSONDecodeError, ValueError) as e:
                        print(f"Ошибка парсинга строки: {str(e)}")
        return self.entries
