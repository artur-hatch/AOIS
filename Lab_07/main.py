from matrix_operations import MatrixOperations
from logic_processor import LogicProcessor
from utils import display_menu, get_user_input


class MatrixApp:
    def __init__(self):
        self.matrix_ops = MatrixOperations()
        self.logic_processor = LogicProcessor()
        self.matrix = self.matrix_ops.create_random_matrix()

    def run(self):
        while True:
            display_menu()
            choice = get_user_input("Выберите действие (0-5): ", int, 0, 5)

            if choice == 0:
                print("Выход из программы.")
                break
            elif choice == 1:
                self.matrix = self.matrix_ops.create_random_matrix()
                self.matrix_ops.display_matrix(self.matrix)
            elif choice == 2:
                self.read_operation()
            elif choice == 3:
                self.logic_operation()
            elif choice == 4:
                self.matrix = self.matrix_ops.sort_matrix(self.matrix)
            elif choice == 5:
                self.arithmetic_operation()

    def read_operation(self):
        sub_choice = get_user_input(
            "1 - Чтение столбца\n2 - Чтение слова\nВыберите (1-2): ",
            int, 1, 2
        )
        num = get_user_input("Введите номер (0-15): ", int, 0, 15)

        if sub_choice == 1:
            result = self.matrix_ops.get_column(self.matrix, num)
            print(f"Столбец {num}: {result}")
        else:
            result = self.matrix_ops.get_word(self.matrix, num)
            print(f"Слово {num}: {result}")

    def logic_operation(self):
        num1 = get_user_input("Введите номер первого слова (0-15): ", int, 0, 15)
        num2 = get_user_input("Введите номер второго слова (0-15): ", int, 0, 15)

        word1 = self.matrix_ops.get_word(self.matrix, num1)
        word2 = self.matrix_ops.get_word(self.matrix, num2)

        print(f"Слово 1 ({num1}): {word1}")
        print(f"Слово 2 ({num2}): {word2}")

        self.logic_processor.perform_all_operations(word1, word2)

    def arithmetic_operation(self):
        print("Введите ключ из 3 битов (0 или 1):")
        key = [
            get_user_input("Бит 1: ", int, 0, 1),
            get_user_input("Бит 2: ", int, 0, 1),
            get_user_input("Бит 3: ", int, 0, 1)
        ]

        self.matrix = self.matrix_ops.perform_addition(self.matrix, key)
        print("Матрица после арифметической операции:")
        self.matrix_ops.display_matrix(self.matrix)


if __name__ == "__main__":
    app = MatrixApp()
    app.run()