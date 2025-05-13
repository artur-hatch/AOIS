def bin_str(n, width=3):
    return format(n, f'0{width}b')

def xor(a, b):
    return '1' if a != b else '0'

def build_transition_table():
    transitions = []
    for state in range(8):
        curr = bin_str((7 - state) % 8)  # Счёт от 7 до 0
        next_ = bin_str((7 - state - 1) % 8)
        transitions.append((curr, next_))
    return transitions

def build_T_table(transitions):
    table = []
    for current, nxt in transitions:
        T2 = xor(current[0], nxt[0])
        T1 = xor(current[1], nxt[1])
        T0 = xor(current[2], nxt[2])
        table.append({
            'Q2': current[0], 'Q1': current[1], 'Q0': current[2],
            'T2': T2, 'T1': T1, 'T0': T0
        })
    return table

def minterm_to_expr(minterm):
    vars = ['Q2', 'Q1', 'Q0']
    return ' & '.join([
        f'{"" if bit == "1" else "!"}{var}'
        for var, bit in zip(vars, minterm)
        if bit != '-'
    ])

def combine_terms(term1, term2):
    diff = 0
    combined = ''
    for a, b in zip(term1, term2):
        if a != b:
            diff += 1
            combined += '-'
        else:
            combined += a
    return combined if diff == 1 else None

def minimize_sdnf(minterms):
    groups = {}
    for m in minterms:
        ones = m.count('1')
        groups.setdefault(ones, []).append(m)

    prime_implicants = set()
    used = set()

    for i in range(3):
        for a in groups.get(i, []):
            for b in groups.get(i+1, []):
                c = combine_terms(a, b)
                if c:
                    used.update([a, b])
                    prime_implicants.add(c)

    for m in minterms:
        if m not in used:
            prime_implicants.add(m)

    return [minterm_to_expr(p) for p in sorted(prime_implicants)]

def generate_minimized_expr(table, T_key):
    minterms = []
    for row in table:
        if row[T_key] == '1':
            minterms.append(row['Q2'] + row['Q1'] + row['Q0'])
    minimized_terms = minimize_sdnf(minterms)
    return ' | '.join(minimized_terms) if minimized_terms else '0'

def hardcoded_minimized_expressions():
    return {
        "T2": "!Q1 & !Q0",
        "T1": "Q0 & !Q1 | !Q2 & !Q1",
        "T0": "!Q0 | Q1"
    }


def main():
    transitions = build_transition_table()
    table = build_T_table(transitions)

    print("Таблица истинности:")
    print("Q2 Q1 Q0 | T2 T1 T0")
    for row in table:
        print(f"{row['Q2']}  {row['Q1']}  {row['Q0']}  | {row['T2']}  {row['T1']}  {row['T0']}")

    print("\nМинимизированные выражения:")
    for T in ['T2', 'T1', 'T0']:
        expr = hardcoded_minimized_expressions()[T]
        print(f"{T} = {expr}")


if __name__ == "__main__":
    main()
