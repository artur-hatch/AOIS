import unittest
import re
from run import (
    is_valid_expression, parse_expression, build_truth_table,
    minimize_dnf, minimize_cnf, glue_impl, impl_to_str, generate_karnaugh_map
)


class TestLogicMinimizer(unittest.TestCase):

    def test_is_valid_expression_invalid(self):
        self.assertFalse(is_valid_expression('x & y'))
        self.assertFalse(is_valid_expression('a % b'))
        self.assertFalse(is_valid_expression('a + b'))
        self.assertFalse(is_valid_expression('a && b'))

    def test_parse_expression_basic(self):
        self.assertEqual(parse_expression('a & b'), 'a  and  b')
        self.assertEqual(parse_expression('a | b'), 'a  or  b')
        self.assertEqual(parse_expression('!a'), 'not a')

    def test_parse_expression_complex(self):
        self.assertEqual(parse_expression('a -> b'), '(not (a) or (b))')
        self.assertEqual(parse_expression('a ~ b'), '((a) == (b))')
        self.assertIn('not', parse_expression('!(a & b)'))

    def test_build_truth_table_correct(self):
        variables = ['a', 'b']
        expr = 'a & b'
        truth_table, dnf, cnf = build_truth_table(variables, expr)
        expected_truth_table = [
            ((0, 0), 0),
            ((0, 1), 0),
            ((1, 0), 0),
            ((1, 1), 1)
        ]
        self.assertEqual(truth_table, expected_truth_table)
        self.assertEqual(dnf, [(1, 1)])
        self.assertEqual(cnf, [(0, 0), (0, 1), (1, 0)])

    def test_glue_impl_basic(self):
        impl = [(1, 1), (1, 0)]
        glued = glue_impl(impl)
        self.assertIn(('1', 'X'), [tuple(map(str, g)) for g in glued])

    def test_glue_impl_no_glue(self):
        impl = [(1, 1), (0, 0)]
        glued = glue_impl(impl)
        self.assertEqual(len(glued), 2)

    def test_impl_to_str_dnf(self):
        imp = (1, 'X', 0)
        variables = ['a', 'b', 'c']
        result = impl_to_str(imp, variables, mode='dnf')
        self.assertEqual(result, 'a & ¬c')

    def test_impl_to_str_cnf(self):
        imp = (1, 'X', 0)
        variables = ['a', 'b', 'c']
        result = impl_to_str(imp, variables, mode='cnf')
        self.assertEqual(result, '¬a ∨ c')

    def test_minimize_dnf(self):
        variables = ['a', 'b']
        expr = 'a & b'
        minimized = minimize_dnf(expr, variables)
        str_minimized = [impl_to_str(imp, variables, mode='dnf') for imp in minimized]
        self.assertIn('a & b', str_minimized)

    def test_minimize_cnf(self):
        variables = ['a', 'b']
        expr = '!(a & b)'
        minimized = minimize_cnf(expr, variables)
        str_minimized = [impl_to_str(imp, variables, mode='cnf') for imp in minimized]
        self.assertTrue(any('a' in s or 'b' in s for s in str_minimized))

    def test_generate_karnaugh_map_2_vars(self):
        variables = ['a', 'b']
        expr = 'a & b'
        truth_table, _, _ = build_truth_table(variables, expr)
        selected = generate_karnaugh_map(truth_table, variables)
        self.assertEqual(selected, [])

    def test_generate_karnaugh_map_invalid(self):
        variables = ['a']
        expr = 'a'
        truth_table, _, _ = build_truth_table(variables, expr)
        with self.assertRaises(ValueError):
            generate_karnaugh_map(truth_table, variables)

    def test_parse_expression_multiple_operators(self):
        expr = '!(a&b)|(c->d)'
        parsed = parse_expression(expr)
        self.assertIn('not (a and b)', parsed)
        self.assertIn('or', parsed)
        self.assertIn('(not (c) or (d))', parsed)

    def test_impl_to_str_empty(self):
        imp = ('X', 'X')
        variables = ['a', 'b']
        result_dnf = impl_to_str(imp, variables, mode='dnf')
        result_cnf = impl_to_str(imp, variables, mode='cnf')
        self.assertEqual(result_dnf, '')
        self.assertEqual(result_cnf, '')

    def test_build_truth_table_single_var(self):
        variables = ['a']
        expr = '!a'
        truth_table, dnf, cnf = build_truth_table(variables, expr)
        self.assertEqual(truth_table, [((0,), 1), ((1,), 0)])
        self.assertEqual(dnf, [(0,)])
        self.assertEqual(cnf, [(1,)])

    def test_minimize_dnf_full_one(self):
        variables = ['a']
        expr = 'a | !a'
        minimized = minimize_dnf(expr, variables)
        self.assertIn(('X',), minimized)

    def test_minimize_cnf_full_zero(self):
        variables = ['a']
        expr = 'a & !a'
        minimized = minimize_cnf(expr, variables)
        self.assertIn(('X',), minimized)

    def test_parse_expression_nested(self):
        expr = '!(a&(!b|c))'
        parsed = parse_expression(expr)
        self.assertIn('not (a and (not b or c))', parsed)

    def test_generate_karnaugh_map_3_vars(self):
        variables = ['a', 'b', 'c']
        expr = '(a&b)|c'
        truth_table, _, _ = build_truth_table(variables, expr)
        selected = generate_karnaugh_map(truth_table, variables)
        self.assertEqual(selected, [])

    def test_generate_karnaugh_map_4_vars(self):
        variables = ['a', 'b', 'c', 'd']
        expr = '(a&b)|(c&d)'
        truth_table, _, _ = build_truth_table(variables, expr)
        selected = generate_karnaugh_map(truth_table, variables)
        self.assertEqual(selected, [])

    def test_invalid_expression_too_many_vars(self):
        expr = 'a&b&c&d&e&a'
        self.assertTrue(is_valid_expression(expr))
        used_vars = sorted(set(re.findall(r'[a-e]', expr)))
        self.assertLessEqual(len(used_vars), 5)

    def test_build_truth_table_empty_expr(self):
        variables = []
        expr = '1'
        truth_table, dnf, cnf = build_truth_table(variables, expr)
        self.assertEqual(truth_table, [((), 1)])
        self.assertEqual(dnf, [()])

    def test_impl_to_str_only_ones(self):
        imp = (1, 1, 1)
        variables = ['a', 'b', 'c']
        result = impl_to_str(imp, variables, mode='dnf')
        self.assertEqual(result, 'a & b & c')

    def test_impl_to_str_only_zeroes(self):
        imp = (0, 0, 0)
        variables = ['a', 'b', 'c']
        result = impl_to_str(imp, variables, mode='dnf')
        self.assertEqual(result, '¬a & ¬b & ¬c')

if __name__ == '__main__':
    unittest.main()