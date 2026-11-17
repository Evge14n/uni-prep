# Програмування (Python) - задачі з розвʼязанням

> Задачі - з файлу підготовки UNI2 (теми 1-10) і нові на ті самі прийоми. Код кожної
> задачі разом з doctest перевіряє генератор сайту `tools/gen_prog.py`: він виконує кожен
> блок коду з цієї сторінки і проганяє всі doctest. Останній запуск - 0 падінь.
>
> Як розвʼязувати, щоб зарахували: назву функції і doctest не міняти, результат
> **повертати** (`return`), назви змінних англійські і змістовні, PEP 8, кожен рядок уміти
> пояснити. Спершу прочитай doctest - це і є умова.

## Тема 1. Арифметика без циклів

### Задача 1. Секунди в години, хвилини, секунди

Функція отримує кількість секунд і повертає рядок `'1 год 2 хв 5 с'`.

<details markdown="1"><summary>Розвʼязання</summary>

**Крок 1.** У годині 3600 с. Цілі години - `total_seconds // 3600`.

**Крок 2.** Те, що лишилось після годин, - `total_seconds % 3600`. З цього цілі хвилини - `// 60`.

**Крок 3.** Секунди - остача від ділення на 60.

```python
def split_seconds(total_seconds: int) -> str:
    """Переводить секунди в години, хвилини і секунди.

    >>> split_seconds(3725)
    '1 год 2 хв 5 с'
    >>> split_seconds(59)
    '0 год 0 хв 59 с'
    >>> split_seconds(86400)
    '24 год 0 хв 0 с'
    """
    hours = total_seconds // 3600
    minutes = total_seconds % 3600 // 60
    seconds = total_seconds % 60
    return f"{hours} год {minutes} хв {seconds} с"
```

Перевірка вручну: 3725 = 3600 + 120 + 5, тобто 1 год, 2 хв, 5 с.

</details>

### Задача 2. Сума цифр тризначного числа без циклу

<details markdown="1"><summary>Розвʼязання</summary>

**Крок 1.** Число може бути відʼємним, тому спершу `abs`.

**Крок 2.** Перша цифра - `// 100`, друга - `// 10 % 10`, остання - `% 10`.

```python
def three_digit_sum(number: int) -> int:
    """Сума цифр тризначного числа без циклу.

    >>> three_digit_sum(472)
    13
    >>> three_digit_sum(-905)
    14
    """
    number = abs(number)
    first_digit = number // 100
    second_digit = number // 10 % 10
    last_digit = number % 10
    return first_digit + second_digit + last_digit
```

Без `abs`: -905 // 100 = -10 (округлення вниз), і сума вийде неправильна.

</details>

### Задача 3. Парне чи непарне без `if`

<details markdown="1"><summary>Розвʼязання</summary>

`True` = 1, `False` = 0. Рядок, помножений на `True`, лишається, на `False` - стає порожнім.
Рівно одна з двох умов істинна, тому сума дає одне слово.

```python
def parity_text(number: int) -> str:
    """Парне чи непарне - множенням рядка на умову.

    >>> parity_text(10)
    'парне'
    >>> parity_text(7)
    'непарне'
    >>> parity_text(-3)
    'непарне'
    """
    return "парне" * (number % 2 == 0) + "непарне" * (number % 2 == 1)
```

Для -3: `-3 % 2` дорівнює 1 (знак як у дільника), тому працює і для відʼємних.

</details>

### Задача 4. Розміняти суму монетами 5, 2 і 1 без циклів і списків

Найменша кількість монет. Повернути рядок `'5 грн: 3, 2 грн: 1, 1 грн: 1'` для 18.

<details markdown="1"><summary>Розвʼязання</summary>

**Крок 1.** Спершу беремо скільки влізе найбільших: `amount // 5`.

**Крок 2.** Залишок `amount % 5` розмінюємо двійками, те, що лишилось, - одиницями.

```python
def coins_change(amount: int) -> str:
    """Розмін суми монетами 5, 2 і 1 грн.

    >>> coins_change(18)
    '5 грн: 3, 2 грн: 1, 1 грн: 1'
    >>> coins_change(4)
    '5 грн: 0, 2 грн: 2, 1 грн: 0'
    """
    used_5 = amount // 5
    rest = amount % 5
    used_2 = rest // 2
    used_1 = rest % 2
    return f"5 грн: {used_5}, 2 грн: {used_2}, 1 грн: {used_1}"
```

Перевірка: 18 = 3·5 + 1·2 + 1·1.

</details>

## Тема 2. Функції, return, f-рядки

### Задача 5. Один return з кількома рядками

Повернути радіус, довжину кола і площу круга, кожне з 3 знаками після коми, в окремому рядку.

<details markdown="1"><summary>Розвʼязання</summary>

Вимога викладача: один `return`, один рядок, частини склеєні через `\n`. Довгий вираз
беремо в дужки, щоб перенести на кілька рядків (PEP 8, до 79 символів).

```python
import math


def circle_info(radius: float) -> str:
    """Один return, частини склеєні через переведення рядка.

    >>> print(circle_info(2))
    Радіус: 2.000
    Довжина кола: 12.566
    Площа круга: 12.566
    """
    length = 2 * math.pi * radius
    area = math.pi * radius ** 2
    return (f"Радіус: {radius:.3f}\n"
            f"Довжина кола: {length:.3f}\n"
            f"Площа круга: {area:.3f}")
```

У doctest тут `print(...)`, бо інакше doctest показав би рядок з `\n` у лапках.

</details>

### Задача 6. Чому doctest падає, якщо функція друкує

<details markdown="1"><summary>Розвʼязання</summary>

`print` лише показує число на екрані, а функція повертає `None`. Doctest чекає значення,
яке функція **повернула**.

```python
def bad_square(number: int) -> None:
    """Типова помилка: print замість return.

    >>> result = bad_square(3)
    9
    >>> print(result)
    None
    """
    print(number ** 2)


def good_square(number: int) -> int:
    """Правильно: функція повертає значення.

    >>> good_square(3)
    9
    >>> good_square(3) + 1
    10
    """
    return number ** 2
```

`bad_square(3) + 1` дав би `TypeError`: не можна додати `None` і число.

</details>

### Задача 7. Таблиця з шириною колонок

<details markdown="1"><summary>Розвʼязання</summary>

`:<10` - ширина 10, вирівнювання вліво; `:>3` - ширина 3 вправо; `:.2f` - 2 знаки.

```python
def price_line(product_name: str, price: float, count: int) -> str:
    """Рядок таблиці: назва, кількість, сума.

    >>> price_line("зошит", 12.5, 4)
    'зошит     |   4 шт | 50.00 грн'
    """
    total = price * count
    return f"{product_name:<10}| {count:>3} шт | {total:.2f} грн"
```

</details>

## Тема 3. Розгалуження

### Задача 8. Координатна чверть

<details markdown="1"><summary>Розвʼязання</summary>

Спершу особливий випадок (точка на осі), потім чверті. `x < 0 < y` - ланцюжок порівнянь.

```python
def quadrant(x: float, y: float) -> int:
    """Номер координатної чверті, 0 - якщо точка на осі.

    >>> quadrant(1, 2), quadrant(-1, 2), quadrant(-1, -2), quadrant(1, -2)
    (1, 2, 3, 4)
    >>> quadrant(0, 5)
    0
    """
    if x == 0 or y == 0:
        return 0
    elif x > 0 and y > 0:
        return 1
    elif x < 0 < y:
        return 2
    elif x < 0 and y < 0:
        return 3
    else:
        return 4
```

</details>

### Задача 9. Вид трикутника

<details markdown="1"><summary>Розвʼязання</summary>

**Крок 1.** Трикутник існує, якщо найбільша сторона менша за суму двох інших. Сума двох
інших = периметр мінус найбільша.

**Крок 2.** Рівносторонній перевіряємо раніше за рівнобедрений, бо рівносторонній - теж
«дві сторони рівні».

```python
def triangle_type(side_a: float, side_b: float, side_c: float) -> str:
    """Вид трикутника за сторонами.

    >>> triangle_type(3, 4, 5)
    'різносторонній'
    >>> triangle_type(2, 2, 3)
    'рівнобедрений'
    >>> triangle_type(1, 1, 1)
    'рівносторонній'
    >>> triangle_type(1, 2, 3)
    'не існує'
    """
    longest = max(side_a, side_b, side_c)
    if longest >= side_a + side_b + side_c - longest:
        return "не існує"
    if side_a == side_b == side_c:
        return "рівносторонній"
    if side_a == side_b or side_b == side_c or side_a == side_c:
        return "рівнобедрений"
    return "різносторонній"
```

</details>

### Задача 10. Високосний рік одним виразом

<details markdown="1"><summary>Розвʼязання</summary>

Високосний: ділиться на 4, але не на 100, **або** ділиться на 400. `and` сильніший за `or`,
тому дужки не потрібні.

```python
def is_leap(year: int) -> bool:
    """Високосний рік без if.

    >>> is_leap(2024), is_leap(1900), is_leap(2000), is_leap(2026)
    (True, False, True, False)
    """
    return year % 4 == 0 and year % 100 != 0 or year % 400 == 0
```

</details>

### Задача 11. Найбільше з трьох тернарним виразом

<details markdown="1"><summary>Розвʼязання</summary>

Тернарний вираз `a if умова else b` - це вираз, тож його можна вкласти. Без `max` і без
оператора `if`.

```python
def max_of_three(first: int, second: int, third: int) -> int:
    """Найбільше з трьох чисел тернарним виразом.

    >>> max_of_three(3, 9, 4), max_of_three(7, 2, 7), max_of_three(-1, -5, -3)
    (9, 7, -1)
    """
    larger = first if first > second else second
    return larger if larger > third else third
```

</details>

## Тема 4. Цикли

### Задача 12. Кількість цифр числа

<details markdown="1"><summary>Розвʼязання</summary>

Ділимо на 10, поки число не стане однозначним. Починаємо з 1, тому 0 має одну цифру.

```python
def count_digits(number: int) -> int:
    """Кількість цифр числа (while).

    >>> count_digits(12345)
    5
    >>> count_digits(0)
    1
    >>> count_digits(-70)
    2
    """
    number = abs(number)
    digits_count = 1
    while number >= 10:
        number //= 10
        digits_count += 1
    return digits_count
```

</details>

### Задача 13. Сума квадратів непарних до limit

<details markdown="1"><summary>Розвʼязання</summary>

`range(1, limit + 1, 2)` дає 1, 3, 5, ... Плюс один - бо stop не входить.

```python
def sum_odd_squares(limit: int) -> int:
    """Сума квадратів непарних від 1 до limit.

    >>> sum_odd_squares(5)
    35
    >>> sum_odd_squares(0)
    0
    """
    total = 0
    for odd_number in range(1, limit + 1, 2):
        total += odd_number ** 2
    return total
```

Перевірка: 1 + 9 + 25 = 35.

</details>

### Задача 14. Перший степінь трійки, не менший за число (лекція 7)

<details markdown="1"><summary>Розвʼязання</summary>

Наперед не знаємо, скільки кроків, тому `while`. Множимо на 3, поки менше за межу.

```python
def first_power_of_three(limit: int) -> int:
    """Найменше 3 ** k, яке >= limit.

    >>> first_power_of_three(10)
    27
    >>> first_power_of_three(81)
    81
    >>> first_power_of_three(1)
    1
    """
    power = 1
    while power < limit:
        power *= 3
    return power
```

</details>

## Тема 5. Цілочисельні алгоритми

### Задача 15. НСД і НСК

<details markdown="1"><summary>Розвʼязання</summary>

Евклід: пара (a, b) замінюється на (b, a % b), поки b не стане 0. Тоді a - НСД.
48, 18 → 18, 12 → 12, 6 → 6, 0. НСК = добуток / НСД.

```python
def gcd_euclid(first: int, second: int) -> int:
    """НСД за алгоритмом Евкліда.

    >>> gcd_euclid(48, 18)
    6
    >>> gcd_euclid(17, 5)
    1
    """
    while second != 0:
        first, second = second, first % second
    return first


def lcm_numbers(first: int, second: int) -> int:
    """НСК через НСД.

    >>> lcm_numbers(10, 15)
    30
    >>> lcm_numbers(4, 6)
    12
    """
    return first * second // gcd_euclid(first, second)
```

</details>

### Задача 16. Кількість дільників, перебір до √n

<details markdown="1"><summary>Розвʼязання</summary>

Кожен дільник d ≤ √n має пару n // d. Якщо d == n // d (повний квадрат), рахуємо один раз.
Для 36: пари (1, 36), (2, 18), (3, 12), (4, 9), (6, 6) - разом 9.

```python
def divisor_count(number: int) -> int:
    """Кількість дільників, перебір лише до кореня.

    >>> divisor_count(36)
    9
    >>> divisor_count(13)
    2
    >>> divisor_count(1)
    1
    """
    divisors_found = 0
    divisor = 1
    while divisor * divisor <= number:
        if number % divisor == 0:
            divisors_found += 1
            if divisor != number // divisor:
                divisors_found += 1
        divisor += 1
    return divisors_found
```

</details>

### Задача 17. Чи просте число

<details markdown="1"><summary>Розвʼязання</summary>

Числа менші за 2 - не прості. Далі шукаємо дільник від 2 до √n; знайшли - одразу `False`.

```python
def is_prime(number: int) -> bool:
    """Чи просте число.

    >>> [n for n in range(1, 20) if is_prime(n)]
    [2, 3, 5, 7, 11, 13, 17, 19]
    """
    if number < 2:
        return False
    divisor = 2
    while divisor * divisor <= number:
        if number % divisor == 0:
            return False
        divisor += 1
    return True
```

</details>

### Задача 18. Число задом наперед і паліндром без рядків

<details markdown="1"><summary>Розвʼязання</summary>

Беремо останню цифру `% 10` і дописуємо її в кінець результату: `result * 10 + digit`.

```python
def reversed_number(number: int) -> int:
    """Число задом наперед без рядків.

    >>> reversed_number(1203)
    3021
    >>> reversed_number(500)
    5
    """
    result = 0
    while number > 0:
        result = result * 10 + number % 10
        number //= 10
    return result


def is_palindrome(number: int) -> bool:
    """Чи читається число однаково з обох боків.

    >>> is_palindrome(12321), is_palindrome(1230)
    (True, False)
    """
    return reversed_number(number) == number
```

</details>

## Тема 6. Рекурентні співвідношення

### Задача 19. Фібоначчі двома змінними

<details markdown="1"><summary>Розвʼязання</summary>

F(0) = 0, F(1) = 1, F(n) = F(n-1) + F(n-2). Тримаємо лише дві останні величини і оновлюємо
їх **одночасно**.

```python
def fibonacci(index: int) -> int:
    """Число Фібоначчі без списку.

    >>> [fibonacci(n) for n in range(10)]
    [0, 1, 1, 2, 3, 5, 8, 13, 21, 34]
    """
    previous, current = 0, 1
    for _ in range(index):
        previous, current = current, previous + current
    return previous
```

Якщо написати `previous = current` і потім `current = previous + current`, друга дія візьме
вже нове `previous`, і вийде 1, 2, 4, 8... - степені двійки.

</details>

### Задача 20. Часткова сума ряду для eˣ

<details markdown="1"><summary>Розвʼязання</summary>

S(n) = 1 + x + x²/2! + ... + xⁿ/n!. Член a(n) = a(n-1) · x / n - рахуємо з попереднього,
без факторіала.

```python
def exp_partial_sum(x: float, last_index: int) -> float:
    """Часткова сума ряду для e ** x.

    >>> round(exp_partial_sum(1, 10), 6)
    2.718282
    >>> exp_partial_sum(2, 0)
    1.0
    """
    term = 1.0
    partial_sum = 1.0
    for index in range(1, last_index + 1):
        term = term * x / index
        partial_sum += term
    return partial_sum
```

</details>

## Тема 7. Точність ε, бісекція, Горнер

### Задача 21. Корінь за Героном з точністю ε

<details markdown="1"><summary>Розвʼязання</summary>

x(n) = (x(n-1) + number / x(n-1)) / 2. Рахуємо, поки два сусідні наближення відрізняються
на ε або більше.

```python
def sqrt_heron(number: float, eps: float) -> float:
    """Корінь квадратний за Героном.

    >>> round(sqrt_heron(2, 1e-12), 10)
    1.4142135624
    >>> sqrt_heron(9, 1e-12)
    3.0
    """
    previous = number
    current = (previous + number / previous) / 2
    while abs(current - previous) >= eps:
        previous = current
        current = (previous + number / previous) / 2
    return current
```

</details>

### Задача 22. Бісекція з лічильником кроків

Повернути кортеж: корінь і кількість поділів навпіл.

<details markdown="1"><summary>Розвʼязання</summary>

**Крок 1.** Середина `middle`. Якщо знаки f(left) і f(middle) різні - корінь зліва.

**Крок 2.** Кожен крок ділить довжину навпіл. Для [0, 2] і ε = 10⁻⁶: 2 / 2ᵏ < 10⁻⁶, тобто
2ᵏ > 2·10⁶. 2²⁰ = 1048576 замало, 2²¹ = 2097152 досить - 21 крок.

```python
def bisection_steps(function, left: float, right: float,
                    eps: float) -> tuple[float, int]:
    """Бісекція: корінь і кількість кроків.

    >>> root, steps = bisection_steps(lambda x: x * x - 2, 0, 2, 1e-6)
    >>> round(root, 5), steps
    (1.41421, 21)
    """
    steps = 0
    while right - left >= eps:
        middle = (left + right) / 2
        if function(left) * function(middle) < 0:
            right = middle
        else:
            left = middle
        steps += 1
    return (left + right) / 2, steps
```

</details>

### Задача 23. Значення многочлена схемою Горнера (ЛР6)

<details markdown="1"><summary>Розвʼязання</summary>

Коефіцієнти від старшого: [1, 0, -2, -5] означає x³ - 2x - 5. `value = value * x + coefficient`.
Для x = 2: 1 → 1·2 + 0 = 2 → 2·2 - 2 = 2 → 2·2 - 5 = -1.

```python
def horner(coefficients: list[float], x: float) -> float:
    """Значення многочлена схемою Горнера.

    >>> horner([1, 0, -2, -5], 2)
    -1
    >>> horner([1, 0, -2, -5], 3)
    16
    """
    value = coefficients[0]
    for coefficient in coefficients[1:]:
        value = value * x + coefficient
    return value
```

</details>

## Тема 8. Списки

### Задача 24. Рядок чисел у список

<details markdown="1"><summary>Розвʼязання</summary>

`split()` без аргументу ділить за будь-якими пробілами (і подвійними теж).

```python
def read_numbers(text: str) -> list[float]:
    """Рядок «1 2.5 3» у список дійсних чисел.

    >>> read_numbers("1 2.5  3")
    [1.0, 2.5, 3.0]
    >>> read_numbers("")
    []
    """
    return [float(item) for item in text.split()]
```

</details>

### Задача 25. Найбільший елемент і його індекс без `max`

<details markdown="1"><summary>Розвʼязання</summary>

`enumerate` дає пари (індекс, значення). Строго `>`, тому при рівних лишається перший.

```python
def max_with_index(values: list[float]) -> tuple[float, int]:
    """Найбільший елемент і його індекс.

    >>> max_with_index([3, 9, 2, 9])
    (9, 1)
    """
    best_value = values[0]
    best_index = 0
    for index, value in enumerate(values):
        if value > best_value:
            best_value = value
            best_index = index
    return best_value, best_index
```

</details>

### Задача 26. Транспонування матриці

<details markdown="1"><summary>Розвʼязання</summary>

Рядок нової матриці номер `column` - це стовпчик `column` старої.

```python
def transpose(matrix: list[list[int]]) -> list[list[int]]:
    """Транспонування матриці.

    >>> transpose([[1, 2, 3], [4, 5, 6]])
    [[1, 4], [2, 5], [3, 6]]
    """
    rows_count = len(matrix)
    columns_count = len(matrix[0])
    return [[matrix[row][column] for row in range(rows_count)]
            for column in range(columns_count)]
```

</details>

### Задача 27. Пастки: псевдонім і матриця через множення

<details markdown="1"><summary>Розвʼязання</summary>

`alias = original` - те саме імʼя для того самого списку. `[[0] * 2] * 2` - два посилання на
**один** рядок.

```python
def list_traps() -> tuple[list[int], list[int], list[list[int]]]:
    """Що змінюється, коли список не скопійовано.

    >>> list_traps()
    ([1, 2, 99], [1, 2], [[7, 0], [7, 0]])
    """
    original = [1, 2]
    alias = original
    real_copy = original.copy()
    alias.append(99)
    bad_matrix = [[0] * 2] * 2
    bad_matrix[0][0] = 7
    return original, real_copy, bad_matrix
```

Правильно матрицю: `[[0] * 2 for _ in range(2)]`.

</details>

## Тема 9. Кортежі, генератор-вирази, сортування

### Задача 28. Кілька результатів одним return

<details markdown="1"><summary>Розвʼязання</summary>

`return a, b, c` повертає кортеж, а при виклику його розпаковують у три змінні.

```python
def min_max_mean(values: list[float]) -> tuple[float, float, float]:
    """Найменше, найбільше, середнє.

    >>> smallest, largest, mean = min_max_mean([4, 1, 7])
    >>> smallest, largest, mean
    (1, 7, 4.0)
    """
    return min(values), max(values), sum(values) / len(values)
```

</details>

### Задача 29. Підрахунок генератор-виразом і сортування за двома ключами

<details markdown="1"><summary>Розвʼязання</summary>

`sum(1 for ...)` додає одиничку за кожен підхожий елемент. У `sorted` ключ `(-бал, імʼя)`:
мінус робить спадання за балом, при рівних бал іде імʼя за алфавітом.

```python
def count_even(values: list[int]) -> int:
    """Скільки парних.

    >>> count_even([12, 0, 7, 15, 21, 8, 13, 0, 2])
    5
    """
    return sum(1 for value in values if value % 2 == 0)


def rank_students(records: list[tuple[str, int]]) -> list[tuple[str, int]]:
    """Бал за спаданням, при рівних - за імʼям.

    >>> rank_students([("Олег", 80), ("Анна", 95), ("Борис", 80)])
    [('Анна', 95), ('Борис', 80), ('Олег', 80)]
    """
    return sorted(records, key=lambda record: (-record[1], record[0]))
```

</details>

## Тема 11. Словники і винятки [нема конспекту - звір з лекцією]

### Задача 30. Скільки разів трапляється кожне слово

<details markdown="1"><summary>Розвʼязання</summary>

`counts.get(word, 0)` дає 0 для нового слова, тому не буде `KeyError`.

```python
def word_counts(text: str) -> dict[str, int]:
    """Частота слів у рядку.

    >>> word_counts("так ні так так")
    {'так': 3, 'ні': 1}
    """
    counts: dict[str, int] = {}
    for word in text.split():
        counts[word] = counts.get(word, 0) + 1
    return counts
```

</details>

### Задача 31. Безпечне ділення через try / except

<details markdown="1"><summary>Розвʼязання</summary>

Ділення на нуль кидає `ZeroDivisionError`. Перехоплюємо лише його, а не всі помилки.

```python
def safe_divide(dividend: float, divisor: float) -> str:
    """Частка або повідомлення про ділення на нуль.

    >>> safe_divide(7, 2)
    '3.5'
    >>> safe_divide(1, 0)
    'ділення на нуль'
    """
    try:
        return str(dividend / divisor)
    except ZeroDivisionError:
        return "ділення на нуль"
```

</details>
