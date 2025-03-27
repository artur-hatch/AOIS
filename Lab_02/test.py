import unittest
from run import TruthTable


class TestTruthTable(unittest.TestCase):

    def test_parse_expression(self):
        self.assertEqual(TruthTable.parse_expression("a->b"), "a or not b")
        self.assertEqual(TruthTable.parse_expression("a&b"), "a and b")
        self.assertEqual(TruthTable.parse_expression("a|b"), "a or b")

    def test_generate_combinations(self):
        self.assertEqual(TruthTable.generate_combinations(2), [[0, 0], [0, 1], [1, 0], [1, 1]])

    def test_tokenize(self):
        tt = TruthTable("a & b")
        tokens = tt.tokenize("a and b")
        expected_tokens = [("VARIABLE", "a"), ("OPERATOR", "and"), ("VARIABLE", "b")]
        self.assertEqual(tokens, expected_tokens)

    def test_shunting_yard(self):
        tt = TruthTable("a & b")
        tokens = [("VARIABLE", "a"), ("OPERATOR", "and"), ("VARIABLE", "b")]
        postfix = tt.shunting_yard(tokens)
        self.assertEqual(postfix, ["a", "b", "and"])

    def test_evaluate_postfix(self):
        tt = TruthTable("a & b")
        postfix = ["a", "b", "and"]
        env = {"a": 1, "b": 0}
        self.assertEqual(tt.evaluate_postfix(postfix, env), 0)
        env = {"a": 1, "b": 1}
        self.assertEqual(tt.evaluate_postfix(postfix, env), 1)

    def test_build_truth_table(self):
        tt = TruthTable("a & b")
        truth_table = tt.build_truth_table()
        expected_table = [
            [0, 0, 0],
            [0, 1, 0],
            [1, 0, 0],
            [1, 1, 1]
        ]
        self.assertEqual(truth_table, expected_table)

    def test_get_dnf(self):
        tt = TruthTable("a & b")
        truth_table = tt.build_truth_table()
        dnf, dnf_num = tt.get_dnf(truth_table)
        self.assertEqual(dnf, "(a ∧ b)")
        self.assertEqual(dnf_num, "3")

    def test_get_cnf(self):
        tt = TruthTable("a & b")
        truth_table = tt.build_truth_table()
        cnf, cnf_num = tt.get_cnf(truth_table)
        self.assertEqual(cnf, "(a ∨ b) ∧ (a ∨ ¬b) ∧ (¬a ∨ b)")
        self.assertEqual(cnf_num, "0,1,2")

    def test_index_form(self):
        tt = TruthTable("a & b")
        truth_table = tt.build_truth_table()
        bin_str, num_form = tt.index_form(truth_table)
        self.assertEqual(bin_str, "0001")
        self.assertEqual(num_form, 1)


if __name__ == "__main__":
    unittest.main()
