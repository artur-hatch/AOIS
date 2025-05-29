import unittest
from unittest.mock import patch
from matrix_operations import MatrixOperations
from logic_processor import LogicProcessor
from utils import display_menu, get_user_input
import sys
from io import StringIO

class TestMatrixApp(unittest.TestCase):
    def setUp(self):
        self.matrix_ops = MatrixOperations()
        self.logic_processor = LogicProcessor()
        self.matrix_size = self.matrix_ops.MATRIX_SIZE

    # Tests for MatrixOperations
    def test_create_random_matrix(self):
        matrix = self.matrix_ops.create_random_matrix()
        self.assertEqual(len(matrix), self.matrix_size)
        self.assertEqual(len(matrix[0]), self.matrix_size)
        for row in matrix:
            for bit in row:
                self.assertIn(bit, [0, 1])

    def test_create_random_matrix_custom_size(self):
        size = 4
        matrix = self.matrix_ops.create_random_matrix(size)
        self.assertEqual(len(matrix), size)
        self.assertEqual(len(matrix[0]), size)
        for row in matrix:
            for bit in row:
                self.assertIn(bit, [0, 1])

    def test_display_matrix(self):
        matrix = [[0, 1], [1, 0]]
        captured_output = StringIO()
        sys.stdout = captured_output
        self.matrix_ops.display_matrix(matrix)
        sys.stdout = sys.__stdout__
        self.assertEqual(captured_output.getvalue().strip(), "0 1\n1 0")

    def test_get_column(self):
        matrix = [[0] * 16 for _ in range(16)]  # 16x16 matrix
        matrix[0][0] = 1
        matrix[1][1] = 1
        column = self.matrix_ops.get_column(matrix, 0)
        expected = [1, 1] + [0] * 14  # Diagonal starting at (0,0)
        self.assertEqual(column, expected)

    def test_get_word(self):
        matrix = [[0] * 16 for _ in range(16)]  # 16x16 matrix
        matrix[0][0] = 1
        matrix[1][1] = 1
        word = self.matrix_ops.get_word(matrix, 0)
        expected = [1] + [0] * 15  # Diagonal starting at (0,0)
        self.assertEqual(word, expected)

    def test_perform_addition(self):
        matrix = [[0] * 16 for _ in range(16)]  # 16x16 matrix
        matrix[0][0] = 0; matrix[1][0] = 0; matrix[2][0] = 0  # Key match
        matrix[3][0] = 1; matrix[4][0] = 0; matrix[5][0] = 1; matrix[6][0] = 0  # a = [1,0,1,0]
        matrix[7][0] = 1; matrix[8][0] = 0; matrix[9][0] = 1; matrix[10][0] = 0  # b = [1,0,1,0]
        key = [0, 0, 0]
        result_matrix = self.matrix_ops.perform_addition(matrix, key)
        expected_sum = [1, 0, 1, 0, 0]  # 1010 + 1010 = 10100
        for i, bit in enumerate(expected_sum):
            self.assertEqual(result_matrix[11 + i][0], bit)

    def test_binary_addition(self):
        a = [1, 0, 1, 0]
        b = [1, 0, 1, 0]
        result = self.matrix_ops._binary_addition(a, b)
        expected = [1, 0, 1, 0, 0]  # 1010 + 1010 = 10100 (5 bits)
        self.assertEqual(result, expected)

        a = [1, 1, 1, 1]
        b = [1, 1, 1, 1]
        result = self.matrix_ops._binary_addition(a, b)
        expected = [1, 1, 1, 1, 0]  # 1111 + 1111 = 11110
        self.assertEqual(result, expected)

    def test_sort_matrix(self):
        matrix = [[0] * 16 for _ in range(16)]  # 16x16 matrix
        matrix[0][0] = 1; matrix[0][1] = 0; matrix[0][2] = 0
        matrix[1][0] = 0; matrix[1][1] = 1; matrix[1][2] = 0
        sorted_matrix = self.matrix_ops.sort_matrix(matrix)
        word0 = self.matrix_ops._get_rotated_word([sorted_matrix[r][0] for r in range(16)], 0)
        word1 = self.matrix_ops._get_rotated_word([sorted_matrix[r][1] for r in range(16)], 0)
        word2 = self.matrix_ops._get_rotated_word([sorted_matrix[r][2] for r in range(16)], 0)
        self.assertTrue(all(a <= b for a, b in zip(word0, word1)))
        self.assertTrue(all(a <= b for a, b in zip(word1, word2)))

    def test_compare_columns(self):
        col1 = [1] + [0] * 15
        col2 = [0] * 16
        result = self.matrix_ops._compare_columns(col1, col2, 0)
        self.assertTrue(result)

    def test_get_rotated_word(self):
        column = [1] + [0] * 15
        word = self.matrix_ops._get_rotated_word(column, 1)
        expected = [0] * 15 + [1]  # Rotated by 1
        self.assertEqual(word, expected)

    # Tests for LogicProcessor
    def test_xor_operation(self):
        word1 = [1, 0, 1, 0]
        word2 = [0, 1, 1, 0]
        result = self.logic_processor._xor_operation(word1, word2)
        expected = [1, 1, 0, 0]
        self.assertEqual(result, expected)

    def test_xnor_operation(self):
        word1 = [1, 0, 1, 0]
        word2 = [0, 1, 1, 0]
        result = self.logic_processor._xnor_operation(word1, word2)
        expected = [0, 0, 1, 1]
        self.assertEqual(result, expected)

    def test_implication(self):
        word1 = [1, 0, 1, 0]
        word2 = [0, 1, 1, 0]
        result = self.logic_processor._implication(word1, word2)
        expected = [0, 1, 0, 0]
        self.assertEqual(result, expected)

    def test_reverse_implication(self):
        word1 = [1, 0, 1, 0]
        word2 = [0, 1, 1, 0]
        result = self.logic_processor._reverse_implication(word1, word2)
        expected = [1, 0, 1, 1]
        self.assertEqual(result, expected)

    def test_perform_all_operations(self):
        word1 = [1, 0]
        word2 = [0, 1]
        captured_output = StringIO()
        sys.stdout = captured_output
        self.logic_processor.perform_all_operations(word1, word2)
        sys.stdout = sys.__stdout__
        output = captured_output.getvalue()
        self.assertIn("XOR (F6): [1, 1]", output)
        self.assertIn("XNOR (F9): [0, 0]", output)
        self.assertIn("Implication (F4): [0, 1]", output)
        self.assertIn("Reverse Implication (F11): [1, 0]", output)

    # Tests for utils
    def test_display_menu(self):
        captured_output = StringIO()
        sys.stdout = captured_output
        display_menu()
        sys.stdout = sys.__stdout__
        output = captured_output.getvalue()
        self.assertIn("Меню:", output)
        self.assertIn("1. Сгенерировать новую матрицу", output)
        self.assertIn("0. Выход", output)

    @patch('builtins.input')
    def test_get_user_input_valid(self, mock_input):
        mock_input.side_effect = ['5']
        result = get_user_input("Enter: ", int, 0, 10)
        self.assertEqual(result, 5)

    @patch('builtins.input')
    def test_get_user_input_out_of_range(self, mock_input):
        mock_input.side_effect = ['11', '5']
        captured_output = StringIO()
        sys.stdout = captured_output
        result = get_user_input("Enter: ", int, 0, 10)
        sys.stdout = sys.__stdout__
        self.assertEqual(result, 5)
        self.assertIn("Значение должно быть не больше 10", captured_output.getvalue())

    @patch('builtins.input')
    def test_get_user_input_invalid_type(self, mock_input):
        mock_input.side_effect = ['abc', '5']
        captured_output = StringIO()
        sys.stdout = captured_output
        result = get_user_input("Enter: ", int, 0, 10)
        sys.stdout = sys.__stdout__
        self.assertEqual(result, 5)
        self.assertIn("Ошибка: введите корректное значение", captured_output.getvalue())

if __name__ == '__main__':
    unittest.main()