import random
from typing import List


class MatrixOperations:
    MATRIX_SIZE = 16

    def create_random_matrix(self, size=16) -> List[List[int]]:
        return [[random.randint(0, 1) for _ in range(size)] for _ in range(size)]

    def display_matrix(self, matrix: List[List[int]]) -> None:
        for row in matrix:
            print(' '.join(map(str, row)))

    def get_column(self, matrix: List[List[int]], col_num: int) -> List[int]:
        """Reads a column diagonally as in the original find_column function"""
        return [matrix[(col_num + row) % self.MATRIX_SIZE][row] for row in range(self.MATRIX_SIZE)]

    def get_word(self, matrix: List[List[int]], word_num: int) -> List[int]:
        """Reads a word diagonally as in the original find_logos function"""
        return [matrix[(word_num + row) % self.MATRIX_SIZE][word_num] for row in range(self.MATRIX_SIZE)]

    def perform_addition(self, matrix: List[List[int]], key: List[int]) -> List[List[int]]:
        V, A, B, S = 3, 4, 4, 5

        # Find matching columns
        matching_cols = [
            col for col in range(self.MATRIX_SIZE)
            if all(matrix[row][col] == key[row] for row in range(len(key)))
        ]

        for col in matching_cols:
            # Get operands
            a = [matrix[row][col] for row in range(V, V + A)]
            b = [matrix[row][col] for row in range(V + A, V + A + B)]

            # Perform binary addition
            sum_result = self._binary_addition(a, b)

            # Store result
            for row in range(S):
                matrix[V + A + B + row][col] = sum_result[row]

        return matrix

    def _binary_addition(self, a: List[int], b: List[int]) -> List[int]:
        result = [0] * 5
        carry = 0

        for i in range(3, -1, -1):
            total = a[i] + b[i] + carry
            result[i + 1] = total % 2
            carry = total // 2

        result[0] = carry
        return result

    def sort_matrix(self, matrix: List[List[int]]) -> List[List[int]]:
        transposed = list(zip(*matrix))
        n = len(transposed)

        for i in range(n - 1, 0, -1):
            max_col = transposed[i]

            for j in range(i):
                if self._compare_columns(transposed[j], max_col, i):
                    transposed[i], transposed[j] = transposed[j], transposed[i]
                    max_col = transposed[j]

        return [list(col) for col in zip(*transposed)]

    def _compare_columns(self, col1, col2, index):
        word1 = self._get_rotated_word(col1, index)
        word2 = self._get_rotated_word(col2, index)

        for bit1, bit2 in zip(word1, word2):
            if bit1 > bit2:
                return True
            elif bit1 < bit2:
                return False
        return False

    def _get_rotated_word(self, column, num):
        return [column[(num + i) % self.MATRIX_SIZE] for i in range(self.MATRIX_SIZE)]