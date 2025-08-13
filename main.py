import argparse

from tabulate import tabulate

from log_processor.filters import DateFilter
from log_processor.parser import LogParser
from log_processor.reporter import ReporterFactory


def main():
    parser = argparse.ArgumentParser(description="Лог-процессор для анализа эндпоинтов")
    parser.add_argument(
        "--files", nargs="+", required=True, help="Список файлов для обработки"
    )
    parser.add_argument(
        "--report", required=True, help="Тип отчета (например, average)"
    )
    parser.add_argument(
        "--date", default=None, help="Фильтрация по дате в формате YYYY-MM-DD"
    )
    args = parser.parse_args()

    try:
        # Парсинг логов
        log_parser = LogParser(args.files)
        entries = log_parser.parse()
        # # Применение фильтров
        if args.date:
            date_filter = DateFilter(args.date)
            entries = date_filter.apply(entries)
        # Генерация отчета
        reporter = ReporterFactory.get_reporter(args.report)
        report_data = reporter.generate(entries)
        # Форматирование вывода
        table = [
            [rd.endpoint, rd.request_count, f"{rd.average_response_time:.2f} мс"]
            for rd in report_data
        ]
        headers = ["Эндпоинт", "Количество запросов", "Среднее время ответа"]
        print(tabulate(table, headers=headers, tablefmt="grid"))

    except Exception as e:
        print(f"Произошла ошибка: {str(e)}")
        exit(1)


if __name__ == "__main__":
    main()
