def weight(v):
    return sum(v)  # число единиц (вес Хэмминга)


def hamming_dist(x, y):
    return sum((a + b) % 2 for a, b in zip(x, y))


def vec_mat_mult(m, G):
    return [sum(m[i] * G[i][j] for i in range(len(m))) % 2 for j in range(len(G[0]))]


def all_codewords(G):
    k, n = len(G), len(G[0])
    words = []
    for i in range(2**k):
        m = [(i >> j) & 1 for j in range(k)]
        c = vec_mat_mult(m, G)
        words.append(tuple(c))
    return words


def min_distance(words):
    d_min = float('inf')
    for c in words:
        if any(c):
            d_min = min(d_min, weight(c))
    return d_min


# ============== Задача 1: Расширенный код Хэмминга (8,4) ==============
print("=" * 50)
print("Задача 1: Расширенный код Хэмминга (8,4)")
print("=" * 50)

# Стандартная G для кода Хэмминга (7,4) в систематическом виде:
# Инфо на позициях 1,2,3,4; проверочные 5,6,7
G_74 = [
    [1, 0, 0, 0, 1, 1, 1],
    [0, 1, 0, 0, 1, 1, 0],
    [0, 0, 1, 0, 1, 0, 1],
    [0, 0, 0, 1, 0, 1, 1]
]

# Расширенный (8,4): добавляем 8-й столбец — проверка на чётность (сумма первых 7)
G_ext = [row[:7] + [sum(row) % 2] for row in G_74]

print("\nПорождающая матрица G (8,4):")
print(G_ext)

words = all_codewords(G_ext)
weights = [weight(c) for c in words]
print(f"\nВеса кодовых слов: {sorted(set(weights))}")
print(
    f"Распределение: {dict((w, weights.count(w)) for w in sorted(set(weights)))}")

d_min = min_distance(words)
print(f"\nМинимальное расстояние d_min = {d_min}")

# Расстояния между парами (для линейного кода = веса ненулевых слов)
dists = [hamming_dist(words[i], words[j])
         for i in range(len(words)) for j in range(i+1, len(words))]
print(
    f"Расстояния между парами: {sorted(set(dists))} (это веса ненулевых слов)")

# ============== Задача 2: Дуальный коду Хэмминга — симплекс ==============
print("\n" + "=" * 50)
print("Задача 2: Дуальный коду Хэмминга — симплекс")
print("=" * 50)

# Hamming (7,4): H 3x7. Дуальный: G_dual = H, размерность 3, длина 7
# Код (7,3) — 8 кодовых слов
G_dual = [
    [0, 0, 0, 1, 1, 1, 1],
    [0, 1, 1, 0, 0, 1, 1],
    [1, 0, 1, 0, 1, 0, 1]
]
words_dual = all_codewords(G_dual)
w_dual = [weight(c) for c in words_dual if any(c)]
print(f"Дуальный код (7,3): {len(words_dual)} слов")
print(f"Веса ненулевых слов: {w_dual}")
print(
    f"Все ненулевые имеют вес 2^(r-1) = 2^2 = 4: {all(w == 4 for w in w_dual)}")
# Расстояние между c1, c2 = weight(c1+c2), т.к. c1+c2 тоже в коде — вес 4
dists_dual = [hamming_dist(words_dual[i], words_dual[j])
              for i in range(len(words_dual)) for j in range(i+1, len(words_dual))]
print(f"Расстояния между парами: {set(dists_dual)} — все равны 4")
print("Вывод: дуальный — симплекс ✓")

# ============== Задача 3: Дуальный коду с проверкой на чётность ==============
print("\n" + "=" * 50)
print("Задача 3: Дуальный коду с проверкой на чётность")
print("=" * 50)

# Код с проверкой на чётность: (n, n-1), H = [1 1 1 ... 1]
# G = [I_{n-1} | 1] — последний столбец все единицы
# Дуальный: G_dual = H = [1 1 1 ... 1], одна строка
# (n, 1)-код: 2 слова — 00...0 и 11...1 (повторный код)
n = 8  # для примера
H_parity = [[1] * n]
words_parity_dual = all_codewords(H_parity)
print(f"Дуальный код при n={n}:")
print(f"  Параметры: n={n}, k=1 — (n,1)-код")
print(f"  Число кодовых слов: 2^k = 2")
print(f"  Слова: {[list(c) for c in words_parity_dual]}")
print(f"  d_min = {n} (расстояние между 0 и 1^n)")
t = (n - 1) // 2
print(f"  Исправляет t = floor((d_min-1)/2) = floor((n-1)/2) = {t} ошибок")
