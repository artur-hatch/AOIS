from tabulate import tabulate
import itertools
import math

VARIABLES = ['X1', 'X2', 'X3']
TRUTH_TABLE = [
    (0, 0, 0, 0, 0),
    (0, 0, 1, 0, 1),
    (0, 1, 0, 0, 1),
    (0, 1, 1, 1, 0),
    (1, 0, 0, 0, 1),
    (1, 0, 1, 1, 0),
    (1, 1, 0, 1, 0),
    (1, 1, 1, 1, 1),
]

def binary(n, width):
    return bin(n)[2:].zfill(width)

def bit_count(string, symbol):
    return string.count(symbol)

def merge_terms(term1, term2):
    mismatch = 0
    result = []
    for a, b in zip(term1, term2):
        if a == b:
            result.append(a)
        else:
            mismatch += 1
            result.append('-')
            if mismatch > 1:
                return None
    return ''.join(result)

def extract_primes(mint_list, count):
    grouped = {}
    for m in mint_list:
        b = binary(m, count)
        ones = bit_count(b, '1')
        grouped.setdefault(ones, set()).add(b)

    prime_set = set()
    while grouped:
        temp = {}
        visited = set()
        for i in sorted(grouped):
            next_group = grouped.get(i + 1)
            if not next_group:
                continue
            for a, b in itertools.product(grouped[i], next_group):
                merged = merge_terms(a, b)
                if merged:
                    visited.update([a, b])
                    ones = bit_count(merged, '1')
                    temp.setdefault(ones, set()).add(merged)
        for group in grouped.values():
            for term in group:
                if term not in visited:
                    prime_set.add(term)
        grouped = temp
    return prime_set

def matches(impl, term, count):
    bits = binary(term, count)
    return all(ic == '-' or ic == bc for ic, bc in zip(impl, bits))

def find_essential(primes, term, count):
    table = {imp: {m for m in term if matches(imp, m, count)} for imp in primes}
    term_map = {}
    for imp, covers in table.items():
        for m in covers:
            term_map.setdefault(m, []).append(imp)

    essentials = set()
    covered = set()
    for m, imps in term_map.items():
        if len(imps) == 1:
            essentials.add(imps[0])
            covered.update(table[imps[0]])

    uncovered = set(term) - covered
    while uncovered:
        best_impl = max(table, key=lambda x: len(table[x] & uncovered))
        essentials.add(best_impl)
        covered.update(table[best_impl])
        uncovered = set(term) - covered
    return essentials

def format_impl(imp):
    literals = []
    for b, var in zip(imp, VARIABLES):
        if b == '1':
            literals.append(var)
        elif b == '0':
            literals.append(f'¬{var}')
    return f"({' ∨ '.join(literals)})"

def minimize(term, count):
    if not term:
        return '0'
    primes = extract_primes(term, count)
    essentials = find_essential(primes, term, count)
    return ' ∧ '.join(format_impl(imp) for imp in sorted(essentials))

var_count = int(math.log2(len(TRUTH_TABLE)))

P_terms = []
D_terms = []
for x1, x2, x3, p_out, d_out in TRUTH_TABLE:
    index = (x1 << 2) | (x2 << 1) | x3
    if p_out:
        P_terms.append(index)
    if d_out:
        D_terms.append(index)

table_headers = ["X1", "X2", "X3", "P", "D"]
table_data = [[x1, x2, x3, p, d] for x1, x2, x3, p, d in TRUTH_TABLE]
print(tabulate(table_data, headers=table_headers, tablefmt="grid"))

result_P = minimize(P_terms, var_count)
result_D = minimize(D_terms, var_count)

print("\nМинимизированная СКНФ:")
print("P  =", result_P)
print("D  =", result_D)