from main import filter_rows, aggregate_rows, process_csv, find_comparison_operator
from tests.conftest import csv_reader, sample_csv_file
import pytest

def test_filter_rows(csv_reader):
    """Тестируем фильтр по возрасту"""
    rows = csv_reader
    filtered = filter_rows(rows, 'age', '=', '25')
    assert len(filtered) == 2  # Осталось две строки: одна заголовочная и одна с Alice
    assert filtered[1][1] == 'Alice'  # Убедимся, что осталась запись про Алису

def test_comparison_operator(csv_reader):
    """Тестируем функцию find_comparison_operator"""
    rows = csv_reader
    with pytest.raises(ValueError):
        filter_rows(rows, 'age', '>=', '25')

def test_aggregate_rows(csv_reader):
    """Проверяем функциональность агрегирования"""
    rows = csv_reader
    avg_age = aggregate_rows(rows, 'age', 'avg')
    expected_avg = sum(map(int, ['25', '30', '20'])) / 3
    assert round(avg_age, 2) == round(expected_avg, 2)

def test_unsupported_operator(csv_reader):
    """Тестируем обработку неподдерживаемого оператора сравнения"""
    rows = csv_reader
    with pytest.raises(ValueError, match="Unsupported operator"):
        filter_rows(rows, 'age', '%', '25')

def test_unknown_column(csv_reader):
    """Тестируем обработку неизвестной колонки"""
    rows = csv_reader
    with pytest.raises(ValueError, match="'unknown_column' is not in list"):
        filter_rows(rows, 'unknown_column', '=', '25')

def test_aggregate_on_non_numeric_column(csv_reader):
    """Тестируем обработку попытки агрегирования по неконтроллируемым данным"""
    rows = csv_reader
    with pytest.raises(ValueError, match="could not convert string to float"):
        aggregate_rows(rows, 'name', 'avg')


def test_find_comparison_operator():
    """Тестируем извлечение оператора сравнения"""
    operator = find_comparison_operator("age>25")
    assert operator == ">"
    with pytest.raises(ValueError):
        find_comparison_operator("ageX25")

def test_filter_rows_text_comparison(csv_reader):
    """Тестируем фильтрацию по текстовому полю"""
    rows = csv_reader
    filtered = filter_rows(rows, 'name', '=', 'Alice')
    assert len(filtered) == 2  # Одна заголовочная строка и одна строка с Alice
    assert filtered[1][1] == 'Alice'


def test_process_csv_no_errors(sample_csv_file):
    """Простой тест для проверки фильтрации и агрегирования в process_csv без ошибок"""
    process_csv(sample_csv_file, where='age>25', aggregate='age=avg')
    assert True
