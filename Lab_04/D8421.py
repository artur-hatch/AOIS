from prettytable import PrettyTable
from minim import *

VARIABLES4 = "abcd"

TOTAL_BITS = 4

def unmarked_code(number):
    number = abs(number)
    binary_code = ''
    while number > 0:
        binary_code += str(number % 2)
        number //= 2
    binary_code += '0' * (TOTAL_BITS - len(binary_code))
    binary_code = binary_code[::-1]
    return binary_code[-8:]

def sum() -> None:
    for element in combinations_znaczenii:
        result_values_1 = summa_extra_code(element)
        perem = convert_from_2_to_10(result_values_1)
        perem = perem % 10
        result_values_1 = unmarked_code(perem)

        result_values_s.append(result_values_1[0])
        result_values_p.append(result_values_1[1])
        result_values_f.append(result_values_1[2])
        result_values_g.append(result_values_1[3])
        result_value.append(result_values_1)

    all_values['S'] = result_values_s
    all_values['P'] = result_values_p
    all_values['F'] = result_values_f
    all_values['G'] = result_values_g

def truth_table() -> None:
    table = PrettyTable()
    table.field_names = list(all_values.keys())
    for i in range(10):
        row = [all_values[col][i] for col in table.field_names]
        table.add_row(row)
    print(table)

def cdnf(key: str) -> str:
    line = ''
    result_value = all_values[key]
    for i in range(10):
        if result_value[i] == '1':
            counter = 0
            line += '('
            for element in VARIABLES4:
                if all_values[element][i] == '1':
                    line += element
                else:
                    line += ('!' + element)
                if len(VARIABLES4) - 1 > counter:
                    line += '&'
                    counter += 1
            line += ')|'
    return line[:-1]

def summa_extra_code(binary_code_1: str, binary_code_2: str = '0101') -> str:
    digit = '0'
    sum_binary_code = ''
    max_len = max(len(binary_code_1), len(binary_code_2))
    binary_code_1 = binary_code_1.zfill(max_len)[::-1]
    binary_code_2 = binary_code_2.zfill(max_len)[::-1]
    for i in range(max_len):
        if ((binary_code_1[i] == '1' and binary_code_2[i] == '0') or (binary_code_1[i] == '0' and binary_code_2[i] == '1')) and digit == '0':
            sum_binary_code += '1'
        elif ((binary_code_1[i] == '1' and binary_code_2[i] == '0') or (binary_code_1[i] == '0' and binary_code_2[i] == '1')) and digit == '1':
            sum_binary_code += '0'
        elif (binary_code_1[i] == '0' and  binary_code_2[i] == '0') and digit == '1':
            digit = '0'
            sum_binary_code += '1'
        elif (binary_code_1[i] == '0' and  binary_code_2[i] == '0') and digit == '0':
            sum_binary_code += '0'
        elif (binary_code_1[i] == '1' and  binary_code_2[i] == '1') and digit == '0':
            digit = '1'
            sum_binary_code += '0'
        elif (binary_code_1[i] == '1' and  binary_code_2[i] == '1') and digit == '1':
            sum_binary_code += '1'
    sum_binary_code = sum_binary_code[::-1]
    return sum_binary_code

# 2 код -> 10 код
def convert_from_2_to_10(binary_code: str) -> int:
    result = 0
    for bit in range(len(binary_code)):
        result += int(binary_code[bit]) * (2 ** (len(binary_code) - 1 - bit))
    return result


combinations_znaczenii = list()
all_values = {}
for i in range(10):
    peremen = unmarked_code(i)
    combinations_znaczenii.append(peremen)
for i in range(len(VARIABLES4)):
    values = list()
    for element in combinations_znaczenii:
        values.append(element[i])
    all_values[VARIABLES4[i]] = values
result_values_s = []
result_values_p = []
result_values_f = []
result_values_g = []
result_value = []


sum()
truth_table()

x1 = cdnf('S')
x2 = cdnf('P')
x3 = cdnf('F')
x4 = cdnf('G')



print('Результат:')
print("Минимизированная СДНФ S:")
minimization_cdnf(x1)
print("\nМинимизированная СДНФ P:")
minimization_cdnf(x2)
print("\nМинимизированная СДНФ F:")
minimization_cdnf(x3)
print("\nМинимизированная СДНФ G:")
minimization_cdnf(x4)
