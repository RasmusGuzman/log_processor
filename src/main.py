import argparse
import csv
from typing import List, Union, Tuple
from statistics import mean
from tabulate import tabulate


def filter_rows(
        rows: List[List[str]],
        column_name: str,
        comparison_operator: str,
        value: Union[int, float, str]
) -> List[List[str]]:
    """Фильтрует строки таблицы по заданному критерию.

    :param rows: Список строк CSV файла.
    :param column_name: Название колонки, по которой производится фильтрация.
    :param comparison_operator: Оператор сравнения ('=', '<', '>'), определяющий правило фильтрации.
    :param value: Значение, с которым сравниваются элементы колонки.
    :return: Отфильтрованный список строк с заголовком первой строки.
    """
    header = rows.pop(0)
    index = header.index(column_name)

    def compare_text(cell_value: str, op: str, target_value: str) -> bool:
        """Сравнивает текстовые значения, применяя оператор сравнения."""
        cell_value = cell_value.lower().strip()
        target_value = target_value.lower().strip()
        if op == '=':
            return cell_value == target_value
        else:
            raise ValueError("Unsupported operator for string comparisons.")

    def compare_number(cell_value: str, op: str, target_value: Union[int, float]) -> bool:
        """Сравнивает численные значения, применяя оператор сравнения."""
        cell_value = float(cell_value)
        target_value = float(target_value)
        if op == '>':
            return cell_value > target_value
        elif op == '<':
            return cell_value < target_value
        elif op == '=':
            return cell_value == target_value
        else:
            raise ValueError("Unsupported operator for number comparisons.")

    try:
        # Попытка конвертации значения в число
        float(value)
        filtered_rows = [
            row for row in rows
            if compare_number(row[index], comparison_operator, value)
        ]
    except ValueError:
        # Если не получилось сконвертировать в число, считаем значение текстом
        filtered_rows = [
            row for row in rows
            if compare_text(row[index], comparison_operator, value)
        ]

    return [header] + filtered_rows


def aggregate_rows(
        rows: List[List[str]],
        column_name: str,
        aggregate_function: str
) -> Union[int, float]:
    """Выполняет агрегатную операцию над значениями указанной колонки.

    :param rows: Список строк CSV файла.
    :param column_name: Название колонки, по которой выполняется агрегирование.
    :param aggregate_function: Тип операции ("avg", "min", "max").
    :return: Агрегированное значение.
    """
    header = rows.pop(0)
    index = header.index(column_name)
    values = [float(row[index]) for row in rows]

    if aggregate_function == "avg":
        result = mean(values)
    elif aggregate_function == "min":
        result = min(values)
    elif aggregate_function == "max":
        result = max(values)
    else:
        raise ValueError("Unknown aggregate function.")

    return result


def find_comparison_operator(value: str) -> str:
    """Извлекает оператор сравнения из строки.

    :param value: Строка, содержащая оператор сравнения.
    :return: Извлечённый оператор сравнения.
    :raises ValueError: Если найден некорректный или отсутствующий оператор.
    """
    comparison_operator = [c for c in value if not c.isalnum()]
    if len(comparison_operator) != 1:
        raise ValueError("Invalid or missing comparison operator.")
    return comparison_operator[0]


def process_csv(
        path: str,
        where: str = None,
        aggregate: str = None
) -> None:
    """Основная функция для обработки CSV файлов.

    Производит чтение CSV файла, фильтрацию и агрегирование данных.

    :param path: Путь к файлу CSV.
    :param where: Критерий фильтрации (формат: column=condition).
    :param aggregate: Операция агрегирования (формат: column=action).
    """
    with open(path, mode='r', encoding='utf-8') as file:
        reader = csv.reader(file)
        rows = list(reader)

    # Фильтрация данных
    if where:
        comparison_operator = find_comparison_operator(where)
        parts = where.split(comparison_operator)
        column_name = parts[0].strip()
        value = parts[1].strip()
        rows = filter_rows(rows, column_name, comparison_operator, value)
        print(tabulate(rows, headers="firstrow", tablefmt="pretty"))
        return None

    # Агрегируем данные
    if aggregate:
        comparison_operator = find_comparison_operator(aggregate)
        parts = aggregate.split(comparison_operator, 1)
        column_name = parts[0].strip()
        aggregate_function = aggregate[-3:]  # Берем последние три символа для имени функции
        result = aggregate_rows(rows, column_name, aggregate_function)
        rows = [[f"{aggregate_function}({column_name})"], [result]]
        print(tabulate(rows, headers="firstrow", tablefmt="pretty"))
        return None

    # Просто выводим таблицу без изменений
    print(tabulate(rows, headers="firstrow", tablefmt="pretty"))
    return None


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Скрипт для обработки CSV файлов.")
    parser.add_argument("--path", type=str, required=True, help="Путь к входному CSV файлу.")
    parser.add_argument("--where", type=str, help="Критерии фильтрации (пример: age>=18)")
    parser.add_argument("--aggregate", type=str, help="Агрегационные действия (пример: salary=max)")
    args = parser.parse_args()

    process_csv(args.path, args.where, args.aggregate)
