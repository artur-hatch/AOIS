from typing import List


class LogicProcessor:
    def perform_all_operations(self, word1: List[int], word2: List[int]) -> None:
        results = {
            "XOR (F6)": self._xor_operation(word1, word2),
            "XNOR (F9)": self._xnor_operation(word1, word2),
            "Implication (F4)": self._implication(word1, word2),
            "Reverse Implication (F11)": self._reverse_implication(word1, word2)
        }

        for name, result in results.items():
            print(f"{name}: {result}")

    def _xor_operation(self, a: List[int], b: List[int]) -> List[int]:
        return [x ^ y for x, y in zip(a, b)]

    def _xnor_operation(self, a: List[int], b: List[int]) -> List[int]:
        return [1 if x == y else 0 for x, y in zip(a, b)]

    def _implication(self, a: List[int], b: List[int]) -> List[int]:
        return [1 if (x == 0 and y == 1) else 0 for x, y in zip(a, b)]

    def _reverse_implication(self, a: List[int], b: List[int]) -> List[int]:
        return [0 if (x == 0 and y == 1) else 1 for x, y in zip(a, b)]