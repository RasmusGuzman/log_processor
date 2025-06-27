import pytest
import os
import tempfile
import csv

@pytest.fixture(scope="function")
def sample_csv_file():
    """Фикстура создает временный CSV файл для тестов"""
    temp_dir = tempfile.mkdtemp()
    filename = os.path.join(temp_dir, "test_data.csv")
    rows = [
        ['id', 'name', 'age'],  # Включаем заголовочную строку
        ['1', 'Alice', '25'],
        ['2', 'Bob', '30'],
        ['3', 'Charlie', '20']
    ]
    with open(filename, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(rows)
    yield filename
    os.remove(filename)
    os.rmdir(temp_dir)

@pytest.fixture(scope="function")
def csv_reader(sample_csv_file):
    """Читает содержимое CSV файла в память"""
    with open(sample_csv_file, 'r') as f:
        reader = csv.reader(f)
        rows = list(reader)  # Получаем все строки вместе с заголовочной
    return rows
