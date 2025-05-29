from typing import Any, Callable


def display_menu() -> None:
    print("\nМеню:")
    print("1. Сгенерировать новую матрицу")
    print("2. Операции чтения")
    print("3. Логические операции")
    print("4. Упорядоченная выборка (сортировка)")
    print("5. Арифметические операции")
    print("0. Выход")


def get_user_input(prompt: str, input_type: Callable, min_val: Any = None, max_val: Any = None) -> Any:
    while True:
        try:
            value = input_type(input(prompt))

            if min_val is not None and value < min_val:
                print(f"Значение должно быть не меньше {min_val}")
                continue

            if max_val is not None and value > max_val:
                print(f"Значение должно быть не больше {max_val}")
                continue

            return value
        except ValueError:
            print("Ошибка: введите корректное значение")