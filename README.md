Log Processor
Описание
Log Processor — это инструмент для обработки и анализа логов веб-приложений. Проект позволяет парсить файлы с логами, 
фильтровать записи по различным критериям и генерировать отчеты.

Установка
git clone https://github.com/your-repo/log-processor.git
cd log-processor
pip install -r requirements.txt
Основные компоненты
Модели данных:

LogEntry — структура для хранения одной записи лога

ReportData — структура для хранения данных отчета

Парсер:

LogParser — основной класс для парсинга логов

Фильтры:

BaseFilter — базовый класс для фильтров

DateFilter — фильтр по дате

Отчеты:

BaseReporter — базовый класс для отчетов

AverageReport — отчет со средними значениями

ReporterFactory — фабрика отчетов

Использование
from log_processor.parsers import LogParser
from log_processor.filters import DateFilter
from log_processor.reports import ReporterFactory

# Парсинг логов
parser = LogParser(['path/to/logs.log'])
entries = parser.parse()

# Фильтрация по дате
filtered_entries = DateFilter('2025-22-06').apply(entries)

# Генерация отчета
reporter = ReporterFactory.get_reporter('average')
report = reporter.generate(filtered_entries)
Требования
Python 3.8+

flake8 для проверки стиля кода

isort для сортировки импортов

black для форматирования кода

mypy для проверки типов

pytest для тестирования

Тестирование
Для запуска тестов выполните:

pytest

CI/CD
Проект настроен с автоматическим тестированием и линтингом через GitHub Actions. При каждом пуше проверяются:

Стиль кода

Форматирование

Типизация

Тесты

Контактная информация
Email: rasim_giseinov@mail.ru

GitHub: https://github.com/RasmusGuzman