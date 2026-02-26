import math
from itertools import combinations


def xor_add(a, b):
    """Поразрядное сложение по mod 2 (XOR)."""
    return tuple((x + y) % 2 for x, y in zip(a, b))


def dot(u, v):
    """Скалярное произведение по GF(2)."""
    return sum((a * b) % 2 for a, b in zip(u, v)) % 2


def hamming_weight(x):
    """Вес Хэмминга — число единиц."""
    return sum(x)


def hamming_distance(x, y):
    """Расстояние Хэмминга."""
    return hamming_weight(xor_add(x, y))


def matmul_mod2(A, B):
    """Умножение матриц по mod 2. A (m×n), B (n×p) -> (m×p)"""
    m, n, p = len(A), len(A[0]), len(B[0])
    result = [[0] * p for _ in range(m)]
    for i in range(m):
        for j in range(p):
            result[i][j] = sum(A[i][k] * B[k][j] for k in range(n)) % 2
    return result


def transpose(M):
    return list(zip(*M))


# ============== Задача 1: (5,2)-код ==============
print("=" * 50)
print("Задача 1: (5,2)-код")
print("=" * 50)

p = 1e-3
n = 5
# P_ошибка = sum C(5,k) p^k (1-p)^(5-k) for k=2..5
P_err = sum(
    math.comb(n, k) * (p ** k) * ((1 - p) ** (n - k))
    for k in range(2, n + 1)
)
print(f"Вероятность ошибки при p={p}: {P_err:.2e}")

# Кодовые слова
# ИС: 00, 01, 10, 11 -> КС (порядок: первый бит ИС = m1, второй = m2)
codewords_52 = {
    (0, 0): (0, 0, 0, 0, 0),
    (0, 1): (1, 0, 1, 1, 0),
    (1, 0): (0, 1, 0, 1, 1),
    (1, 1): (1, 1, 1, 0, 1),
}

# Строки G: для (1,0) -> 01011, для (0,1) -> 10110
G1 = [
    [0, 1, 0, 1, 1],  # m=(1,0)
    [1, 0, 1, 1, 0],  # m=(0,1)
]

print("\nПорождающая матрица G:")
for row in G1:
    print(" ", row)

# Проверка: m*G даёт кодовые слова
for m, c_expected in codewords_52.items():
    c = tuple(dot(m, col) for col in transpose(G1))
    assert c == c_expected, f"Не совпало для {m}: {c} != {c_expected}"
print("✓ G корректна (все кодовые слова восстанавливаются)")

# Проверочная матрица H: G*H^T = 0
# Приведём G к систематическому виду [I_2|P] и возьмём H = [P^T|I_3]
# G = [[0,1,0,1,1],[1,0,1,1,0]]. Поменяем строки: [[1,0,1,1,0],[0,1,0,1,1]] -> [I_2|P], P=[[1,1,0],[0,1,1]]
# H = [P^T|I_3]
H1 = [
    [1, 0, 1, 0, 0],
    [1, 1, 0, 1, 0],
    [0, 1, 0, 0, 1],
]

print("\nПроверочная матрица H:")
for row in H1:
    print(" ", row)

GHt = matmul_mod2(G1, transpose(H1))
print("Проверка G*H^T = 0:", GHt)
assert all(x == 0 for row in GHt for x in row), "G*H^T ≠ 0"
print("✓ H корректна")

# d_min кода
weights = [hamming_weight(c)
           for c in codewords_52.values() if hamming_weight(c) > 0]
d_min_52 = min(weights)
print(f"\nd_min = {d_min_52} (код исправляет 1 ошибку)")


# ============== Задача 2: Метрика Хэмминга ==============
print("\n" + "=" * 50)
print("Задача 2: Проверка аксиом метрики для d(x,y)")
print("=" * 50)

x, y, z = (1, 0, 1, 1, 0), (0, 1, 1, 0, 1), (1, 1, 0, 1, 1)
# 1. Неотрицательность
assert hamming_distance(x, y) >= 0 and (
    hamming_distance(x, y) == 0) == (x == y)
# 2. Симметричность
assert hamming_distance(x, y) == hamming_distance(y, x)
# 3. Неравенство треугольника
assert hamming_distance(x, z) <= hamming_distance(
    x, y) + hamming_distance(y, z)
print("✓ Аксиомы метрики выполняются (проверка на примерах)")


# ============== Задача 4: (6,3)-код ==============
print("\n" + "=" * 50)
print("Задача 4: (6,3)-код — матрицы G и H")
print("=" * 50)

codewords_63 = {
    (0, 0, 0): (0, 0, 0, 0, 0, 0),
    (1, 0, 0): (1, 1, 0, 1, 0, 0),
    (0, 1, 0): (0, 1, 1, 0, 1, 0),
    (1, 1, 0): (1, 0, 1, 1, 1, 0),
    (0, 0, 1): (1, 0, 1, 0, 0, 1),
    (1, 0, 1): (0, 1, 1, 1, 0, 1),
    (0, 1, 1): (1, 1, 0, 0, 1, 1),
    (1, 1, 1): (0, 0, 0, 1, 1, 1),
}

# Базис: кодовые слова для 100, 010, 001
G4 = [
    [1, 1, 0, 1, 0, 0],
    [0, 1, 1, 0, 1, 0],
    [1, 0, 1, 0, 0, 1],
]

print("Порождающая матрица G:")
for row in G4:
    print(" ", row)

for m, c_expected in codewords_63.items():
    c = tuple(dot(m, col) for col in transpose(G4))
    assert c == c_expected, f"Не совпало для {m}: {c} != {c_expected}"
print("✓ G корректна")

# H из условия G*H^T = 0. Система g·h=0: h1+h2+h4=0, h2+h3+h5=0, h1+h3+h6=0
# Базис решений (ортогональных всем строкам G):
H4 = [
    [1, 1, 1, 0, 0, 0],
    [1, 0, 0, 1, 0, 1],
    [1, 1, 0, 0, 1, 1],
]

print("\nПроверочная матрица H:")
for row in H4:
    print(" ", row)

GHt4 = matmul_mod2(G4, transpose(H4))
print("Проверка G*H^T = 0:", GHt4)
assert all(x == 0 for row in GHt4 for x in row), "G*H^T ≠ 0"
print("✓ H корректна")

# d_min
weights_63 = [hamming_weight(c)
              for c in codewords_63.values() if hamming_weight(c) > 0]
d_min_63 = min(weights_63)
print(f"\nd_min = {d_min_63}")
t_max = (d_min_63 - 1) // 2
print(f"Код исправляет до {t_max} ошибок")

print("\n" + "=" * 50)
print("Все проверки пройдены успешно.")
print("=" * 50)
