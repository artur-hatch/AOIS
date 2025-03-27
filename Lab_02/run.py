import re
import operator

class TruthTable:
    def __init__(self, expr):
        self.expression = expr.replace('∨', '|').replace('∧', '&').replace(' ', '')
        self.used_vars = sorted(set(re.findall(r'[a-zA-Z_]\w*', expr)))
        self.operators = {
            'and': operator.and_,
            'or': operator.or_,
            'not': operator.not_,
        }

    # Функция для преобразования строки в логическое выражение
    @staticmethod
    def parse_expression(expr):
        expr = re.sub(r'\s*->\s*', ' or not ', expr)
        expr = expr.replace('~', 'not ')
        expr = expr.replace('&', ' and ')
        expr = expr.replace('|', ' or ')
        expr = expr.replace('!', 'not ')
        return expr.strip()

    # Функция для генерации всех возможных комбинаций значений переменных
    @staticmethod
    def generate_combinations(num_vars):
        combinations = []
        for i in range(2 ** num_vars):
            binary = bin(i)[2:].zfill(num_vars)
            combinations.append([int(bit) for bit in binary])
        return combinations

    # Алгоритм сортировочной станции для преобразования в постфиксную запись
    def shunting_yard(self, tokens):
        precedence = {'not': 3, 'and': 2, 'or': 1}
        output = []
        operators = []
        for token_type, token_value in tokens:
            if token_type == 'NUMBER':
                output.append(token_value)
            elif token_type == 'VARIABLE':
                output.append(token_value)
            elif token_type == 'OPERATOR':
                if token_value == '(':
                    operators.append(token_value)
                elif token_value == ')':
                    while operators and operators[-1] != '(':
                        output.append(operators.pop())
                    operators.pop()
                else:
                    while (operators and operators[-1] != '(' and
                           precedence[operators[-1]] >= precedence[token_value]):
                        output.append(operators.pop())
                    operators.append(token_value)
        while operators:
            output.append(operators.pop())
        return output

    # Функция для токенизации
    def tokenize(self, expr):
        token_pattern = re.compile(r'\s*(=>|or|and|not|\(|\)|\w+|\d+)\s*')
        tokens = []
        for match in token_pattern.finditer(expr):
            token = match.group(1)
            if token.isdigit():
                tokens.append(('NUMBER', int(token)))
            elif token in self.operators or token in ('(', ')'):
                tokens.append(('OPERATOR', token))
            else:
                tokens.append(('VARIABLE', token))
        return tokens

    # Вычисление постфиксного выражения
    def evaluate_postfix(self, postfix, env):
        stack = []
        for token in postfix:
            if isinstance(token, int):
                stack.append(token)
            elif token in self.used_vars:
                stack.append(env[token])
            elif token in self.operators:
                if token == 'not':
                    operand = stack.pop()
                    stack.append(self.operators[token](operand))
                else:
                    right = stack.pop()
                    left = stack.pop()
                    stack.append(self.operators[token](left, right))
        return int(stack.pop())

    # Функция для вычисления логического выражения
    def eval_expr(self, expr, env):
        tokens = self.tokenize(expr)
        postfix = self.shunting_yard(tokens)
        return self.evaluate_postfix(postfix, env)

    # Функция для создания таблицы истинности
    def build_truth_table(self):
        parsed_expr = self.parse_expression(self.expression)
        num_vars = len(self.used_vars)
        truth_table_list = []
        combinations = self.generate_combinations(num_vars)
        for values in combinations:
            substitution = {}
            for var, val in zip(self.used_vars, values):
                substitution[var] = bool(val)
            result = self.eval_expr(parsed_expr, substitution)
            truth_table_list.append(values + [result])
        return truth_table_list

    # Функция для печати таблицы истинности
    def print_truth_table(self, truth_table_list):
        header = self.used_vars + ['result']
        print(' | '.join(header))
        print('-' * (len(header) * 3 - 1))
        for row in truth_table_list:
            print(' | '.join(map(str, row)))

    # Функция для получения СДНФ
    def get_dnf(self, truth_table_list):
        dnf_terms = []
        for row in truth_table_list:
            values = row[:-1]
            result = row[-1]
            term_dnf = []
            for i, var in enumerate(self.used_vars):
                if values[i] == 1:
                    term_dnf.append(var)
                else:
                    term_dnf.append(f"¬{var}")
            if result == 1:
                dnf_terms.append("(" + " ∧ ".join(term_dnf) + ")")

        dnf = " ∨ ".join(dnf_terms)
        dnf_num_list = [i for i, row in enumerate(truth_table_list) if row[-1] == 1]
        dnf_num = ",".join(map(str, dnf_num_list))
        return dnf, dnf_num

    # Функция для получения СКНФ
    def get_cnf(self, truth_table_list):
        cnf_terms = []
        for row in truth_table_list:
            values = row[:-1]
            result = row[-1]
            term_cnf = []
            for i, var in enumerate(self.used_vars):
                if values[i] == 1:
                    term_cnf.append(f"¬{var}")
                else:
                    term_cnf.append(var)
            if result == 0:
                cnf_terms.append("(" + " ∨ ".join(term_cnf) + ")")

        cnf = " ∧ ".join(cnf_terms)
        cnf_num_list = [i for i, row in enumerate(truth_table_list) if row[-1] == 0]
        cnf_num =",".join(map(str, cnf_num_list))
        return cnf, cnf_num

    # Функция для получения индексной формы
    def index_form(self, table):
        bin_form = [i[-1] for i in table]
        bin_str = ''.join(map(str, bin_form))
        num_form = int(bin_str, 2)
        return bin_str, num_form

if __name__ == "__main__":
    expression = 'a & b'
    tt = TruthTable(expression)
    # Создание и печать таблицы истинности
    print(tt.parse_expression(expression))
    tt_list = tt.build_truth_table()
    print('\nТаблица истинности:')
    tt.print_truth_table(tt_list)
    # СДНФ и СКНФ в символьной и числовой форме
    print(f'\nСовершенная дизъюнктивная нормальная форма (СДНФ): {tt.get_dnf(tt_list)[0]} '
          f'\nСовершенная конъюнктивная нормальная форма (СKНФ): {tt.get_cnf(tt_list)[0]}')
    print(f'\nЧисловые формы: \n({tt.get_dnf(tt_list)[1]}) v '
          f'\n({tt.get_cnf(tt_list)[1]}) ∧')
    # Индексная форма
    print(f'\nИндексная форма: {tt.index_form(tt_list)[1]} - {tt.index_form(tt_list)[0]}\n')