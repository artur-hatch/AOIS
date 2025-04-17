def decimal_to_binary(num, bits=8):
    if num >= 0:
        binary = bin(num)[2:].zfill(bits)  # Прямой код для положительного числа
        direct_code = binary
        reverse_code = binary
        complement_code = binary
    else:
        binary = bin(abs(num))[2:].zfill(bits)
        direct_code = '1' + binary[1:]
        reverse_code = ''.join('1' if i == '0' else '0' for i in binary)
        bit = '0' * (bits - 1) + '1'
        max_len = max(len(reverse_code), len(bit))
        rev_code = reverse_code.zfill(max_len)
        bit = bit.zfill(max_len)
        result = ''
        carry = 0
        for i in range(max_len - 1, -1, -1):
            r = carry
            r += 1 if rev_code[i] == '1' else 0
            r += 1 if bit[i] == '1' else 0
            result = ('1' if r % 2 == 1 else '0') + result
            carry = 1 if r >= 2 else 0
        if carry != 0:
            result = '1' + result
        complement_code = result[-max_len:]
    return list(direct_code), list(reverse_code), list(complement_code)

def bin_to_dec(bin_num):
    if bin_num[0] == 0:
        return int(''.join(map(str, bin_num[1:])), 2)
    rev = [1] + bin_num[1:]
    for i in range(len(rev)-1, 0, -1):
        if rev[i] == 1:
            rev[i] = 0
            break
        rev[i] = 1
    rev = [1] + [1 - a for a in rev[1:]]
    return -int(''.join(map(str, rev[1:])), 2)

def addition_bin(first_num: int, sec_num: int):
    sec_num = [int(item) for item in decimal_to_binary(sec_num)[2]]
    first_num = [int(item) for item in decimal_to_binary(first_num)[2]]
    res = [0]*len(first_num)
    carry = 0
    for i in range(len(first_num) - 1, -1, -1):
        total = first_num[i] + sec_num[i] + carry
        res[i] = total % 2
        carry = total // 2

    res = bin_to_dec(res)
    res_bin = decimal_to_binary(res)[2]
    return res, res_bin

def subtract_bin(first_num: int, sec_num: int):
    sec_num = -sec_num
    res, res_bin = addition_bin(first_num, sec_num)
    return res, res_bin

def binary_multiply(first_num, sec_num, bits=8):
    sign_a = 0 if first_num >= 0 else 1
    sign_b = 0 if sec_num >= 0 else 1
    sign_res = sign_a ^ sign_b
    a_abs = abs(first_num)
    b_abs = abs(sec_num)

    result = 0
    for i in range(bits):
        if (b_abs >> i) & 1:
            result += a_abs << i

    bin_res =''.join(decimal_to_binary(result)[0])
    binary_number = bin_res.lstrip('0') or '0'
    res_bin = str(sign_res)+ ' ' + binary_number
    result = "-" + str(result) if sign_res == 1 else str(result)
    return res_bin, result

def binary_divide(first_num, sec_num, precision=5):
    if sec_num == 0:
        raise ValueError("Ошибка: Деление на ноль")

    sign = 0 if (first_num >= 0 and sec_num > 0) or (first_num < 0 and sec_num < 0) else 1
    a_abs = abs(first_num)
    b_abs = abs(sec_num)
    int_part = a_abs // b_abs
    remainder = a_abs % b_abs

    frac_binary = ""
    frac_decimal = 0
    for i in range(1, precision + 1):
        remainder *= 2
        bit = remainder // b_abs
        frac_binary += str(bit)
        frac_decimal += bit * (1 / (2 ** i))
        remainder %= b_abs

    int_bin = ''.join(decimal_to_binary(int_part)[0])
    int_bin = int_bin.rjust(precision, '0')
    full_binary = f"{sign} {int_bin}.{frac_binary}"

    result_decimal = int_part + frac_decimal
    if sign == 1:
        result_decimal *= -1
    result_decimal = round(result_decimal, 5)

    return full_binary, result_decimal

def float_to_ieee(num):
    sign = 0 if num >= 0 else 1
    num = abs(num)
    int_part = int(num)
    frac_part = num - int_part

    int_bin = ""
    while int_part > 0:
        int_bin = str(int_part % 2) + int_bin
        int_part //= 2
    int_bin = int_bin or "0"

    frac_bin = ""
    frac = frac_part
    while len(frac_bin) < 30:
        frac *= 2
        bit = int(frac)
        frac_bin += str(bit)
        frac -= bit

    if int_bin != "0":
        exponent = len(int_bin) - 1
        mantissa = int_bin[1:] + frac_bin
    else:
        first_one = frac_bin.find('1')
        exponent = - (first_one + 1)
        mantissa = frac_bin[first_one + 1:]

    exponent_bits = bin(exponent + 127)[2:].rjust(8, '0')
    mantissa_bits = (mantissa + "0"*23)[:23]

    ieee_bin = f"{sign}{exponent_bits}{mantissa_bits}"
    return ieee_bin

def ieee_to_float(binary):
    sign = int(binary[0])
    exponent = int(binary[1:9], 2) - 127
    mantissa = binary[9:]

    full = "1" + mantissa
    if exponent >= 0:
        int_part = full[:exponent + 1]
        frac_part = full[exponent + 1:]
    else:
        int_part = "0"
        frac_part = "0" * (-exponent - 1) + full

    int_val = int(int_part, 2) if int_part else 0
    frac_val = sum([int(a) * (2 ** -(i + 1)) for i, a in enumerate(frac_part)])

    result = int_val + frac_val
    return -result if sign else result


def ieee_add(a_float, b_float):
    a_bin = float_to_ieee(a_float)
    b_bin = float_to_ieee(b_float)

    a_val = ieee_to_float(a_bin)
    b_val = ieee_to_float(b_bin)

    result = a_val + b_val
    result_bin = float_to_ieee(result)

    return result, result_bin

# Пример использования
def main():
    while True:
        a = input("Введите первое число: ")
        b = input("Введите второе число: ")
        try:
            a = int(a)
            b = int(b)
            break
        except ValueError:
            print("\nОшибка: это не число. Попробуйте снова.")

    print(
        f"\nПервое число:\nПрямой код: {decimal_to_binary(a)[0]}\nОбратный код: {decimal_to_binary(a)[1]}\nДополнительный код: {decimal_to_binary(a)[2]}")
    print(
        f"\nВторое число:\nПрямой код: {decimal_to_binary(b)[0]}\nОбратный код: {decimal_to_binary(b)[1]}\nДополнительный код: {decimal_to_binary(b)[2]}")

    addition, add_bin = addition_bin(a, b)
    print(f"\nРезультат сложения:\nДоп. код: {add_bin}\nДесятичный результат: {addition}")

    subtract, sub_bin = subtract_bin(a, b)
    print(f"\nРезультат вычитания:\nДоп. код: {sub_bin}\nДесятичный результат: {subtract}")
    umn_bin, umn = binary_multiply(a, b)
    print(f"\nРезультат умножения:\nПрямой код: {umn_bin}\nДесятичный результат: {umn}")
    sign_del, c = binary_divide(a, b)
    print(f"\nРезультат деления:\nПрямой код: {sign_del}\nДесятичный результат: {c}")

    while True:
        a = input("\nВведите число с плавающей точкой: ")
        b = input("Введите число с плавающей точкой: ")
        try:
            a = float(a)
            b = float(b)
            break
        except ValueError:
            print("\nОшибка: это не число с плавающей точкой. Попробуйте снова.")
    fl_add, fl_add_bin = ieee_add(a, b)
    print(
        f"\nРезультат суммы с плавающей точкой:\nЧисло в десятичном виде: {fl_add}\nЧисло в формате IEEE-754-2008: {fl_add_bin}")

if __name__ == "__main__":
    main()