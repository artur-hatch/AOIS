import itertools
import re

allowed_var = {'a', 'b', 'c', 'd', 'e'}
allowed_sym = {'&', '|', '!', '->', '~', '(', ')'}

def is_valid_expression(expr):
    expr = expr.replace('->', 'IMPL').replace('~', 'EQV')  # временная замена
    tokens = re.findall(r'[a-e]|IMPL|EQV|[&|!() ]', expr)
    for token in tokens:
        if token not in allowed_var and token not in allowed_sym and token not in {'IMPL', 'EQV'}:
            return False
    return True

def parse_expression(expr):
    expr = re.sub(r'([a-e)!]+)\s*->\s*([a-e(!]+)', r'(not (\1) or (\2))', expr)
    expr = re.sub(r'([a-e)!]+)\s*~\s*([a-e(!]+)', r'((\1) == (\2))', expr)
    expr = expr.replace('!', 'not ')
    expr = expr.replace('&', ' and ')
    expr = expr.replace('|', ' or ')
    return expr

def build_truth_table(variables, expr):
    truth_table = []
    dnf = []
    cnf = []
    for values in itertools.product([0, 1], repeat=len(variables)):
        context = dict(zip(variables, values))
        try:
            result = eval(parse_expression(expr), {}, context)
        except Exception as e:
            raise ValueError(f"Ошибка в выражении: {e}")
        truth_table.append((values, result))
        if result:
            dnf.append(values)
        else:
            cnf.append(values)
    return truth_table, dnf, cnf

def glue_impl(impl):
    def can_glue(a, b):
        diff = 0
        pos = -1
        for i in range(len(a)):
            if a[i] != b[i]:
                diff += 1
                pos = i
        return diff == 1, pos

    new_impl = set()
    used = set()
    for i in range(len(impl)):
        for j in range(i + 1, len(impl)):
            can, pos = can_glue(impl[i], impl[j])
            if can:
                glued = list(impl[i])
                glued[pos] = 'X'
                new_impl.add(tuple(glued))
                used.add(i)
                used.add(j)
    for i, imp in enumerate(impl):
        if i not in used:
            new_impl.add(tuple(imp))
    return list(new_impl)

def impl_to_str(imp, variables, mode='dnf'):
    terms = []
    for i, val in enumerate(imp):
        if val == 'X':
            continue
        if mode == 'dnf':
            terms.append(f'¬{variables[i]}' if val == 0 else variables[i])
        else:
            terms.append(variables[i] if val == 0 else f'¬{variables[i]}')
    connector = ' & ' if mode == 'dnf' else ' ∨ '

    return connector.join(terms)

def minimize_dnf(expr, variables):
    _, dnf, _ = build_truth_table(variables, expr)
    impl = [tuple(val) for val in dnf]
    print("Начальные импликанты СДНФ:")
    for i, imp in enumerate(impl):
        print(f"{i+1}: {imp}")
    stage = 1
    while True:
        new_impl = glue_impl(impl)
        if new_impl == impl:
            break
        print(f"\nСтадия склеивания {stage} (СДНФ):")
        for i, imp in enumerate(new_impl):
            print(f"{impl_to_str(imp, variables, mode='dnf')}")
        impl = new_impl
        stage += 1
    return impl

def minimize_cnf(expr, variables):
    _, _, cnf = build_truth_table(variables, expr)
    impl = [tuple(val) for val in cnf]
    print("Начальные импликанты СКНФ:")
    for i, imp in enumerate(impl):
        print(f"{i+1}: {imp}")
    stage = 1
    while True:
        new_impl = glue_impl(impl)
        if new_impl == impl:
            break
        print(f"\nСтадия склеивания {stage} (СКНФ):")
        for i, imp in enumerate(new_impl):
            print(f"{impl_to_str(imp, variables, mode='cnf')}")
        impl = new_impl
        stage += 1
    return impl

def generate_karnaugh_map(truth_table, variables):
    n = len(variables)
    if n < 2 or n > 4:
        raise ValueError("Метод Карно поддерживает 2–4 переменные.")
        return []

    if n == 2:
        row_vars = [variables[0]]
        col_vars = [variables[1]]
    elif n == 3:
        row_vars = [variables[0]]
        col_vars = [variables[1], variables[2]]
    elif n == 4:
        row_vars = [variables[0], variables[1]]
        col_vars = [variables[2], variables[3]]

    row_labels = [format(i ^ (i >> 1), f'0{len(row_vars)}b') for i in range(2 ** len(row_vars))]
    col_labels = [format(i ^ (i >> 1), f'0{len(col_vars)}b') for i in range(2 ** len(col_vars))]
    value_map = {}
    for values, result in truth_table:
        var_dict = dict(zip(variables, values))
        row_key = ''.join(str(var_dict[v]) for v in row_vars)
        col_key = ''.join(str(var_dict[v]) for v in col_vars)
        value_map[(row_key, col_key)] = result

    print("\nКарта Карно:")
    header = "   " + "  ".join(col_labels)
    print(header)
    for r in row_labels:
        row = f"{r} |"
        for c in col_labels:
            val = value_map.get((r, c), ' ')
            row += f" {int(val)} " if isinstance(val, int) else "   "
        print(row)
    selected = []

    return selected

if __name__ == "__main__":
    while True:
        user_input = input("Введите логическое выражение (используйте &, |, !, ->, ~): ").strip()
        if not is_valid_expression(user_input):
            print("Ошибка: выражение содержит недопустимые символы.")
        else:
            used_vars = sorted(set(re.findall(r'[a-e]', user_input)))
            if len(used_vars) > 5:
                print("Ошибка: допустимо не более 5 переменных.")
            else:
                print("\n=== Минимизация СДНФ ===")
                minimized_dnf = minimize_dnf(user_input, used_vars)
                print("\nМинимизированная СДНФ:")
                res_dnf = []
                for imp in minimized_dnf:
                    res_dnf.append(impl_to_str(imp, used_vars, mode='dnf'))
                print(' '.join(res_dnf))

                print("\n=== Минимизация СКНФ ===")
                minimized_cnf = minimize_cnf(user_input, used_vars)
                print("\nМинимизированная СКНФ:")
                res_cnf=[]
                for imp in minimized_cnf:
                    res_cnf.append(impl_to_str(imp, used_vars, mode='cnf'))
                print(' ∧ '.join(res_cnf))

                print("\n=== Метод Карно ===")
                truth_table, _, _ = build_truth_table(used_vars, user_input)
                karnaugh_imp_dnf = generate_karnaugh_map(truth_table, used_vars)
                break
                #a->b
                #(!a&!b&c)
                #!(!a->!b)&c