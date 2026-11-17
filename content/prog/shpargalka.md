# Програмування - шпаргалка

```
7/2=3.5  7//2=3  -7//2=-4  7%2=1  -7%2=1
n%10 остання цифра   n//10%10 передостання
input() -> str!  "2"+"3"="23"  int(input())
True=1 False=0   "так"*(x>0)
a if умова else b   (вираз, не оператор)
not > and > or      0 < x < 10
range(1,10,2): 1 3 5 7 9  (stop не входить)
while: змінна з умови міняється всередині
break - вихід; for...else - якщо без break
НСД: while b: a, b = b, a % b
НСК = a*b // НСД;  дільники до d*d <= n
Фібоначчі: p, c = c, p + c  (одночасно!)
ряд eˣ: a = a * x / n;  S = S + a
ε: while abs(cur - prev) >= eps
бісекція: f(a)*f(c) < 0 -> b = c
  кроків ≈ log₂((b - a) / ε)
Горнер: v = v * x + coef
lst[-1] останній  lst[1:3]  lst[::-1]
append -> None!   b = a НЕ копія: a.copy()
[[0]*m for _ in range(n)]  не [[0]*m]*n
(5,) кортеж   (5) число
sorted(.., key=lambda r: (-r[1], r[0]))
sum(1 for x in lst if x % 2 == 0)
f"{x:.2f}" f"{s:<10}" f"{n:>5}" f"{x:.3g}"
print(a, b, sep=", ", end="")
```

**Функція:** без `return` повертає `None`. Один `return`, частини через `\n`. Назву і doctest
із заготовки не міняти.

**doctest:** порівнює вивід **як текст**: рядок у лапках, зайвий пробіл - падіння.
`python -m doctest -v file.py`.

**PEP 8:** 4 пробіли; рядок до 79; 2 порожні рядки між функціями; пробіли навколо `=` і після
коми; `snake_case`, `UPPER_CASE` для констант; не `list`, `sum`, `str`, `id` як імена;
назви змістовні (`last_digit`, а не `a`).

**Лінтери:** pycodestyle (PEP 8), flake8 (+ невикористане), ruff (швидше), mypy (типи),
black (переформатовує).

**Помилки:** `TypeError` "2"+3; `ValueError` int("abc"); `ZeroDivisionError`;
`IndexError` lst[10]; `KeyError` d["нема"]; `NameError` нема змінної.

**Залік:** формат і бали невідомі - спитати викладача.
