import unittest
from run import (
    decimal_to_binary, bin_to_dec, addition_bin, subtract_bin,
    binary_multiply, binary_divide, float_to_ieee, ieee_to_float, ieee_add
)

class TestBinaryMath(unittest.TestCase):

    def test_decimal_to_binary_carry_in_complement(self):
        _, _, complement = decimal_to_binary(-1, bits=4)
        self.assertEqual(complement, list("1111"))

    def test_binary_multiply_zero(self):
        bin_result, result = binary_multiply(0, 10)
        self.assertEqual(result, '0')
        self.assertIn('0', bin_result)

    def test_binary_divide_negative_result(self):
        bin_result, dec_result = binary_divide(-7, 2)
        self.assertAlmostEqual(dec_result, -3.5)
        self.assertTrue(bin_result.startswith('1'))

    def test_binary_divide_fraction(self):
        bin_result, dec_result = binary_divide(1, 3, precision=6)
        self.assertTrue('.' in bin_result)
        self.assertAlmostEqual(dec_result, 0.32812, places=4)

    def test_float_to_ieee_subnormal(self):
        result = float_to_ieee(0.00001)
        self.assertEqual(len(result), 32)  # IEEE 754 format length
        self.assertTrue(result.startswith('0') or result.startswith('1'))

    def test_ieee_to_float_negative_exponent(self):
        ieee = float_to_ieee(0.00390625)  # 1/256
        val = ieee_to_float(ieee)
        self.assertAlmostEqual(val, 0.00390625, places=5)

    def test_ieee_add_negative_numbers(self):
        result, _ = ieee_add(-1.5, -2.5)
        self.assertAlmostEqual(result, -4.0, places=5)

    def test_decimal_to_binary_positive(self):
        direct, reverse, complement = decimal_to_binary(5, bits=8)
        self.assertEqual(direct, list("00000101"))
        self.assertEqual(reverse, list("00000101"))
        self.assertEqual(complement, list("00000101"))

    def test_decimal_to_binary_negative(self):
        direct, reverse, complement = decimal_to_binary(-5, bits=8)
        self.assertEqual(direct, list("10000101"))
        self.assertEqual(reverse, list("11111010"))
        self.assertEqual(complement, list("11111011"))

    def test_bin_to_dec_positive(self):
        self.assertEqual(bin_to_dec([0, 0, 0, 0, 0, 1, 0, 1]), 5)

    def test_bin_to_dec_negative(self):
        self.assertEqual(bin_to_dec([1, 1, 1, 1, 1, 0, 1, 1]), -5)

    def test_addition_bin(self):
        result, bin_result = addition_bin(5, -3)
        self.assertEqual(result, 2)
        self.assertEqual(bin_result, list('00000010'))

    def test_subtract_bin(self):
        result, bin_result = subtract_bin(5, 3)
        self.assertEqual(result, 2)
        self.assertEqual(bin_result, list('00000010'))

    def test_binary_multiply_positive(self):
        bin_result, result = binary_multiply(3, 2)
        self.assertEqual(result, '6')
        self.assertTrue(bin_result.endswith('110'))

    def test_binary_multiply_negative(self):
        bin_result, result = binary_multiply(-3, 2)
        self.assertEqual(result, '-6')
        self.assertTrue(bin_result.startswith('1'))

    def test_binary_divide(self):
        bin_result, dec_result = binary_divide(5, 2)
        self.assertAlmostEqual(dec_result, 2.5, places=5)
        self.assertIn('010', bin_result)

    def test_binary_divide_zero_division(self):
        with self.assertRaises(ValueError):
            binary_divide(5, 0)

    def test_float_to_ieee_and_back(self):
        original = 5.75
        ieee = float_to_ieee(original)
        recovered = ieee_to_float(ieee)
        self.assertAlmostEqual(recovered, original, places=5)

    def test_ieee_add(self):
        result, ieee_result = ieee_add(1.5, 2.25)
        self.assertAlmostEqual(result, 3.75, places=5)
        self.assertEqual(float_to_ieee(result), ieee_result)

if __name__ == '__main__':
    unittest.main()
