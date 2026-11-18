# Задачі, практика й іспит

## Тренування: 7 зламаних програм

Збережи кожну програму у файл з такою ж назвою (наприклад `nano bug_1.py`, встав, Ctrl+O, Enter, Ctrl+X) і шукай
помилку способом, який підказує завдання (уроки 05-06).

<details markdown="1"><summary>bug_1.py</summary>

```python
"""Середнє прискорення вільного падіння з 5 вимірювань."""
measurements = [9.79, 9.83, 9.81, 9.78, 9.84]


def mean(values):
    total = 0
    for k in range(1, len(values)):
        total += values[k]
    return total / len(values)


g_mean = mean(measurements)
print(f"g = {g_mean:.3f} м/с²")
```

</details>

<details markdown="1"><summary>bug_2.py</summary>

```python
"""Переведення швидкості з км/год у м/с."""


def kmh_to_ms(speed_kmh: float) -> float:
    """Швидкість у м/с, округлена до 3 знаків після коми.

    >>> kmh_to_ms(36)
    10.0
    >>> kmh_to_ms(90)
    25.0
    >>> kmh_to_ms(100)
    27.778
    """
    return round(speed_kmh * 1000 // 3600, 3)


if __name__ == "__main__":
    import doctest

    doctest.testmod()
```

</details>

<details markdown="1"><summary>bug_3.py</summary>

```python
"""Корені квадратного рівняння a·x² + b·x + c = 0 (дискримінант > 0)."""
import math


def roots(coef_a, coef_b, coef_c):
    disc = coef_b ** 2 - 4 * coef_a * coef_c
    root_1 = (-coef_b + math.sqrt(disc)) / 2 * coef_a
    root_2 = (-coef_b - math.sqrt(disc)) / 2 * coef_a
    return root_1, root_2


equations = [(1, -3, 2), (2, -6, 4), (1, -5, 6)]
for coef_a, coef_b, coef_c in equations:
    root_1, root_2 = roots(coef_a, coef_b, coef_c)
    residual = coef_a * root_1 ** 2 + coef_b * root_1 + coef_c
    assert abs(residual) < 1e-9, f"x1 = {root_1} не корінь"
    print(f"{coef_a, coef_b, coef_c}: x1 = {root_1}, x2 = {root_2}")
```

</details>

<details markdown="1"><summary>bug_4.py</summary>

```python
"""Рахуємо кроки часу по 0.1 с, поки не дійдемо до 1 с."""
time_s = 0.0
steps = 0
while time_s != 1.0:
    time_s += 0.1
    steps += 1
print(f"кроків: {steps}")
```

</details>

<details markdown="1"><summary>bug_5.py</summary>

```python
"""Кінетична енергія тіла: E = m·v²/2."""


def kinetic_energy(mass: float, speed: float) -> str:
    """Рядок з енергією в джоулях.

    >>> kinetic_energy(2, 3)
    'E = 9.0 Дж'
    >>> kinetic_energy(3, 0.7)
    'E = 0.735 Дж'
    """
    energy = mass * speed ** 2 / 2
    print(f"E = {energy} Дж")


if __name__ == "__main__":
    import doctest

    doctest.testmod()
```

</details>

<details markdown="1"><summary>bug_6.py</summary>

```python
"""Дві окремі серії вимірювань періоду маятника."""


def add_measurement(value, series=[]):
    series.append(value)
    return series


series_1 = add_measurement(2.01)
series_1 = add_measurement(1.99, series_1)
series_2 = add_measurement(1.42)
print("серія 1:", series_1)
print("серія 2:", series_2)
```

</details>

<details markdown="1"><summary>bug_7.py</summary>

```python
"""Швидкість на кожній ділянці і середня швидкість на всьому шляху."""
distances = [120.0, 80.0, 100.0]  # м
times = [12.0, 10.0, 8.0]  # с

for k in range(len(distances)):
    speed = distances[k] / times[k]
    print(f"ділянка {k + 1}: {speed:.2f} м/с")

sum = 0
for distance in distances:
    sum += distance
total_time = sum(times)
print(f"середня швидкість: {sum / total_time:.2f} м/с")
```

</details>

Сім маленьких програм, у кожній **один** баг (у `bug_5.py` - два, один за одним). Кожна справді поводиться так, як
написано в «Симптомі» (перевірено в Linux Mint 22.3, Python 3.12.3). Порядок роботи:

1. Скопіюй теку в `~/univer/praktyka/zlamani` (як перенести її з ПК і яка команда `cp` - урок 06, крок 9) і перейди
   туди: `cd ~/univer/praktyka/zlamani`.
2. Запусти програму, порівняй з симптомом.
3. Знайди баг **методом, який указано** (саме ним - це тренування методу, а не вгадування).
4. Лише якщо застряг - відкривай «Підказки». «Виправлення» - коли вже виправив сам, для перевірки.

Шляхи у виводі нижче - з `/home/evgen/...`; у тебе буде твоє ім'я користувача.

| Файл | Що рахує | Метод |
|---|---|---|
| `bug_1.py` | середнє g з 5 вимірювань | print `f"{x=}"` або `logging.debug` |
| `bug_2.py` | км/год → м/с, doctest | `python3 bug_2.py -v`, `Expected` / `Got` |
| `bug_3.py` | корені квадратного рівняння | `assert` уже є + точка зупинки pdb з умовою |
| `bug_4.py` | кроки часу по 0.1 с | Ctrl+C (traceback) + print / `faulthandler` |
| `bug_5.py` | кінетична енергія, doctest | `python3 bug_5.py -v`, двічі |
| `bug_6.py` | дві серії вимірювань | pdb: `b`, `p id(...)` при кожному виклику |
| `bug_7.py` | середня швидкість | traceback + post-mortem `-c continue`, `p type(...)` |

---

### bug_1.py - середнє g

**Симптом.** П'ять вимірювань близько 9.8, а середнє чомусь менше за кожне з них:

```bash
python3 bug_1.py
```

```text
g = 7.852 м/с²
```

> **Нове тут:**
>
> - `python3` - запускає Python: файл, рядок коду або модуль. Назва: Python - на честь комедійного шоу «Monty Python», 3 - третя версія мови.
>
> Усе про кожну команду - у довіднику «05_Програмування/КОМАНДИ - довідник.md» (на сайті - вкладка «Команди»).

**Метод:** print-налагодження `f"{x=}"` (урок 05) або `logging.debug` (урок 06, крок 10): надрукуй, **які** значення
потрапляють у суму.

<details markdown="1"><summary>Підказки</summary>

- Середнє менше за найменше вимірювання - значить, у суму потрапило не все. Додай у цикл
  `print(f"{k=} {values[k]=}")` і порахуй рядки: їх має бути 5.
- Або з logging: на початку `import logging` і `logging.basicConfig(level=logging.DEBUG)`, у циклі
  `logging.debug(f"{k=} {total=}")`.
- Або pdb: `python3 -m pdb bug_1.py`, `b 8`, `c`, `p k, values[k]` - з якого `k` починається?
</details>

<details markdown="1"><summary>Виправлення</summary>

`range(1, len(values))` починається з 1, тому `values[0] = 9.79` не потрапляє в суму (а ділимо все одно на 5).
Типова помилка «на одиницю» (off-by-one). Правильно `range(len(values))`:

```text
    for k in range(len(values)):
```

Після виправлення:

```text
g = 9.810 м/с²
```

Ще простіше без циклу: `sum(values) / len(values)`.
</details>

---

### bug_2.py - переведення км/год у м/с

**Симптом.** Усі три doctest-и падають:

```bash
python3 bug_2.py
```

```text
**********************************************************************
File "/home/evgen/univer/praktyka/zlamani/bug_2.py", line 7, in __main__.kmh_to_ms
Failed example:
    kmh_to_ms(36)
Expected:
    10.0
Got:
    10
**********************************************************************
File "/home/evgen/univer/praktyka/zlamani/bug_2.py", line 9, in __main__.kmh_to_ms
Failed example:
    kmh_to_ms(90)
Expected:
    25.0
Got:
    25
**********************************************************************
File "/home/evgen/univer/praktyka/zlamani/bug_2.py", line 11, in __main__.kmh_to_ms
Failed example:
    kmh_to_ms(100)
Expected:
    27.778
Got:
    27
**********************************************************************
1 items had failures:
   3 of   3 in __main__.kmh_to_ms
***Test Failed*** 3 failures.
```

**Метод:** doctest `-v` (урок 06, крок 8): уважно порівняй `Expected` і `Got`. doctest не міняй - він правильний.

<details markdown="1"><summary>Підказки</summary>

- `python3 bug_2.py -v` покаже кожен приклад окремо.
- `10` замість `10.0` - це вже підказка про **тип**: ціле число, а не дробове. Перевір у `python3`:
  `type(36 * 1000 // 3600)` і `type(36 * 1000 / 3600)`.
- Який оператор ділення дає ціле і відкидає дробову частину?
</details>

<details markdown="1"><summary>Виправлення</summary>

`//` - ділення націло (з відкиданням дробової частини): `100000 // 3600 = 27`. Потрібне звичайне ділення `/`:

```text
    return round(speed_kmh * 1000 / 3600, 3)
```

Після виправлення `python3 bug_2.py` нічого не друкує (усі doctest пройшли), а `python3 bug_2.py -v` закінчується
рядком `Test passed.`
</details>

---

### bug_3.py - корені квадратного рівняння

**Симптом.** Перше рівняння пораховано, на другому спрацьовує `assert` (перевірка, що `x1` справді корінь):

```bash
python3 bug_3.py
```

```text
(1, -3, 2): x1 = 2.0, x2 = 1.0
Traceback (most recent call last):
  File "/home/evgen/univer/praktyka/zlamani/bug_3.py", line 16, in <module>
    assert abs(residual) < 1e-9, f"x1 = {root_1} не корінь"
           ^^^^^^^^^^^^^^^^^^^^
AssertionError: x1 = 8.0 не корінь
```

**Метод:** `assert` уже знайшов, **що** не так (`x1 = 8.0` для `2x² - 6x + 4 = 0`, а корені 2 і 1). Знайти, **де** -
точка зупинки pdb з умовою всередині `roots`.

<details markdown="1"><summary>Підказки</summary>

- Post-mortem (`python3 -m pdb -c continue bug_3.py`) тут зупиниться на рівні модуля, рядок 16: змінної `disc` там
  нема (`*** NameError: name 'disc' is not defined`), вона жила лише всередині `roots`.
- Тому так: `python3 -m pdb bug_3.py`, далі `b 9, coef_a == 2` (рядок `return` у `roots`, лише для другого
  рівняння), `c`, `p disc, root_1`.
- Порахуй руками: `x = (6 + √4) / (2·2)`. Тепер у pdb: `p (-coef_b + math.sqrt(disc)) / 2 * coef_a` і
  `p (-coef_b + math.sqrt(disc)) / (2 * coef_a)`. Яке дає 2.0?
- Чому перше рівняння проходило? Подивись, чому дорівнює `coef_a` там.
</details>

<details markdown="1"><summary>Виправлення</summary>

`/ 2 * coef_a` означає `(... / 2) * coef_a`: ділення і множення виконуються зліва направо, тому `coef_a`
**множить**, а не ділить. Для `coef_a = 1` різниці нема, тому перше рівняння проходило. Потрібні дужки:

```text
    root_1 = (-coef_b + math.sqrt(disc)) / (2 * coef_a)
    root_2 = (-coef_b - math.sqrt(disc)) / (2 * coef_a)
```

Після виправлення:

```text
(1, -3, 2): x1 = 2.0, x2 = 1.0
(2, -6, 4): x1 = 2.0, x2 = 1.0
(1, -5, 6): x1 = 3.0, x2 = 2.0
```
</details>

---

### bug_4.py - кроки часу по 0.1 с

**Симптом.** Програма має надрукувати `кроків: 10`, а вона нічого не друкує і не закінчується. Зупини Ctrl+C:

```bash
python3 bug_4.py
```

```text
^CTraceback (most recent call last):
  File "/home/evgen/univer/praktyka/zlamani/bug_4.py", line 4, in <module>
    while time_s != 1.0:
          ^^^^^^^^^^^^^
KeyboardInterrupt
```

**Метод:** Ctrl+C показує, **де** програма крутиться (рядок 4, умова циклу). Далі - подивитись, які значення
набуває `time_s`: print або `faulthandler` (урок 06, крок 11 - за бажанням).

<details markdown="1"><summary>Підказки</summary>

- Додай у цикл `print(f"{steps=} {time_s=}")` і **запобіжник**, щоб не друкувати вічно: другим рядком у циклі
  `assert steps < 20, "забагато кроків"`. Подивись на значення біля 10-го кроку.
- Перевір у `python3`: `0.1 + 0.1 + 0.1` і `0.1 + 0.1 + 0.1 == 0.3`.
- Інший спосіб знайти місце зависання: на початку файлу `import faulthandler` і
  `faulthandler.dump_traceback_later(3, exit=True)`.
</details>

<details markdown="1"><summary>Виправлення</summary>

0.1 у двійковому вигляді не записується точно, тому після 10 додавань `time_s = 0.9999999999999999`, а після 11 -
`1.0999999999999999`. Рівно `1.0` не буває ніколи, умова `!=` завжди істинна. **Дробові числа не порівнюють на
рівність.** Порівнювати з запасом:

```text
while time_s < 1.0 - 1e-9:
```

Після виправлення:

```text
кроків: 10
```

Увага: просто `while time_s < 1.0:` дасть `кроків: 11` (бо `0.9999999999999999 < 1.0`). Найнадійніше -
рахувати цілими кроками: `for steps in range(1, 11):` і `time_s = steps * 0.1`.
</details>

---

### bug_5.py - кінетична енергія

**Симптом.** Обидва doctest-и падають, хоча числа «майже ті»:

```bash
python3 bug_5.py
```

```text
**********************************************************************
File "/home/evgen/univer/praktyka/zlamani/bug_5.py", line 7, in __main__.kinetic_energy
Failed example:
    kinetic_energy(2, 3)
Expected:
    'E = 9.0 Дж'
Got:
    E = 9.0 Дж
**********************************************************************
File "/home/evgen/univer/praktyka/zlamani/bug_5.py", line 9, in __main__.kinetic_energy
Failed example:
    kinetic_energy(3, 0.7)
Expected:
    'E = 0.735 Дж'
Got:
    E = 0.7349999999999999 Дж
**********************************************************************
1 items had failures:
   2 of   2 in __main__.kinetic_energy
***Test Failed*** 2 failures.
```

**Метод:** doctest `-v` і посимвольне порівняння `Expected` / `Got`. Тут два баги - виправляй по одному і запускай
знову.

<details markdown="1"><summary>Підказки</summary>

- Порівняй перший приклад: чим `'E = 9.0 Дж'` відрізняється від `E = 9.0 Дж`? Лапки показують `repr` **рядка**,
  який функція **повернула**. Без лапок - текст, який вона **надрукувала**. Що функція повертає, якщо в ній нема
  `return`?
- Після першого виправлення другий приклад покаже `Got: 'E = 0.7349999999999999 Дж'`. Це похибка float
  (`3 * 0.7 ** 2 / 2`). Як округлити до 3 знаків?
</details>

<details markdown="1"><summary>Виправлення</summary>

1. Функція друкує (`print`), а не повертає: повертає `None`, а doctest бачить лише надрукований текст без лапок.
   Заміни `print(...)` на `return ...`. Після цього лишається одна помилка:

```text
**********************************************************************
File "/home/evgen/univer/praktyka/zlamani/bug_5.py", line 9, in __main__.kinetic_energy
Failed example:
    kinetic_energy(3, 0.7)
Expected:
    'E = 0.735 Дж'
Got:
    'E = 0.7349999999999999 Дж'
**********************************************************************
1 items had failures:
   1 of   2 in __main__.kinetic_energy
***Test Failed*** 1 failures.
```

2. Округлити: `round(energy, 3)` дає `0.735`, а `9.0` лишається `9.0` (формат `:.3f` дав би `9.000` і зламав
   перший приклад):

```text
    return f"E = {round(energy, 3)} Дж"
```

Після виправлення `python3 bug_5.py` нічого не друкує - усі doctest пройшли.
</details>

---

### bug_6.py - дві серії вимірювань

**Симптом.** Друга серія мала б бути `[1.42]`, а в ній значення першої:

```bash
python3 bug_6.py
```

```text
серія 1: [2.01, 1.99, 1.42]
серія 2: [2.01, 1.99, 1.42]
```

**Метод:** pdb з точкою зупинки у функції; при кожній зупинці дивись **сам список** і його `id` (номер об'єкта в
пам'яті - однаковий `id` означає «той самий список»).

<details markdown="1"><summary>Підказки</summary>

- `python3 -m pdb bug_6.py`, `b 5`, `c`, `p series, id(series)`, знову `c` і `p series, id(series)` - тричі.
- На третьому виклику (`add_measurement(1.42)`, без другого аргументу) `series` має бути **новим порожнім**
  списком. Чи він порожній? Чи `id` новий?
- `p add_measurement.__defaults__` - де Python зберігає значення за замовчуванням.
</details>

<details markdown="1"><summary>Виправлення</summary>

Значення за замовчуванням `series=[]` створюється **один раз**, коли Python читає `def`, і потім той самий список
використовується в кожному виклику без другого аргументу. Тому `series_1` і `series_2` - один і той самий список.
Правильний прийом - `None` і новий список усередині:

```text
def add_measurement(value, series=None):
    if series is None:
        series = []
```

Після виправлення:

```text
серія 1: [2.01, 1.99]
серія 2: [1.42]
```
</details>

---

### bug_7.py - середня швидкість

**Симптом.** Швидкості на ділянках правильні, а на середній - падіння:

```bash
python3 bug_7.py
```

```text
ділянка 1: 10.00 м/с
ділянка 2: 8.00 м/с
ділянка 3: 12.50 м/с
Traceback (most recent call last):
  File "/home/evgen/univer/praktyka/zlamani/bug_7.py", line 12, in <module>
    total_time = sum(times)
                 ^^^^^^^^^^
TypeError: 'float' object is not callable
```

**Метод:** прочитати traceback (урок 05), потім post-mortem: `python3 -m pdb -c continue bug_7.py` і подивитись,
**що** таке `sum` у момент падіння.

<details markdown="1"><summary>Підказки</summary>

- `'float' object is not callable` - «дробове число не можна викликати як функцію». Хто в рядку 12 викликається
  дужками?
- У post-mortem: `p type(sum)` і `p sum`. Потім `q` двічі (урок 06, крок 7).
- Знайди в файлі, де `sum` отримує значення: `grep -n "sum" bug_7.py`.
</details>

<details markdown="1"><summary>Виправлення</summary>

Рядок `sum = 0` **затінив** вбудовану функцію `sum` (shadowing): після нього ім'я `sum` означає число `300.0`, і
`sum(times)` пробує викликати число. Змінна має мати власне ім'я:

```text
total_distance = 0
for distance in distances:
    total_distance += distance
```

і в останньому рядку `total_distance / total_time`. Після виправлення:

```text
ділянка 1: 10.00 м/с
ділянка 2: 8.00 м/с
ділянка 3: 12.50 м/с
середня швидкість: 10.00 м/с
```

Імена, які не можна брати для змінних, бо вони вже зайняті: `sum`, `max`, `min`, `list`, `input`, `len`, `round`,
`type`, `id`. Лінтер `ruff check --select A bug_7.py` (у venv) таке ловить.
</details>

## Практика: 4 завдання як у справжній роботі

Чотири реальні задачі, які збирають разом кілька уроків. Це **не лаби викладача**, тому повні розвʼязки тут є.

Як працювати: прочитай умову, зроби сам (20-40 хвилин на завдання), і лише тоді відкривай «Розвʼязок» і порівнюй.
Застряг надовго - відкрий розвʼязок до першого кроку, якого не знаєш, і далі знову сам.

Файли до завдань 2 і 3 лежать поруч у теці `Практика - файли` (`lab_zlamana.py`, `zibraty.sh`), а ще вони повністю
надруковані нижче - можна набрати або вставити в nano. Увесь вивід у розвʼязках - справжній, з тестової Linux Mint
22.3 (перевіряє `_перевірка/u_ispyt.sh`); шлях `/home/evgen/...` у тебе буде зі своїм логіном.

---

### Завдання 1. Робоче місце з нуля на свіжій Mint

**Умова.** Свіжовстановлена Mint 22.3, нічого не налаштовано. Треба отримати:

1. знімок системи «як після встановлення»;
2. оновлену систему;
3. пакети для лаб (git, venv, pip, tkinter);
4. venv `~/univer/.venv` з pytest, flake8, black, mypy, ruff;
5. git з твоїм імʼям і гілкою `main` за замовчуванням;
6. команду `perevir`, яка на тестовому `hello.py` не має жодного зауваження.

Склади чекліст **у правильному порядку** з командами і поясни, чому порядок саме такий. Наприкінці - таблиця
«як перевірити, що кожен пункт готовий».

<details markdown="1"><summary>Розвʼязок</summary>

**Чому такий порядок.** Знімок - першим: ним відкочуєш, якщо щось далі зламається (і він найменший, поки система
чиста). Оновлення - до пакетів: `apt install` ставить найновіші версії зі свіжого списку. venv - лише після пакета
`python3-venv`, інакше `ensurepip is not available`. git і `perevir` - наприкінці, бо їм потрібні venv і пакети.

**Крок 1. Знімок (урок 01).** Спершу один раз мишкою: Меню → Адміністрування → Timeshift → RSYNC → диск → розклад
Daily і Boot по 2-3 знімки → Finish. Домашню теку **не** вмикай. Потім:

```bash
sudo timeshift --create --comments "свіжа система"
sudo timeshift --list
```

> **Нове тут:**
>
> - `sudo` - виконує одну команду від імені адміністратора (root). Назва: su do - «виконати як інший користувач», зазвичай root.
> - `timeshift` - робить і відновлює знімки системи. Назва: time shift - «зсув у часі»: повернути систему в минуле. `--create` - зробити знімок зараз; `--comments` - підпис до знімка, напр. --comments "перед драйвером" (видно в стовпці Description); `--list` - список знімків: Num, Name (дата і час), Tags, Description.
> - `"..."` - текст з пробілами одним словом, $ підставляється. Назва: подвійні лапки - «усе це одне слово, але $ працює».
>
> Усе про кожну команду - у довіднику «05_Програмування/КОМАНДИ - довідник.md» (на сайті - вкладка «Команди»).

**Крок 2. Оновлення (урок 02).** Мишкою - Диспетчер оновлень, або в терміналі (список перед `Y` - читати):

```bash
sudo apt update
sudo apt upgrade
flatpak update
```

> **Нове тут:**
>
> - `apt update` - оновлює список пакетів, нічого не ставить. Назва: update - «оновити» (тут оновлюється лише список пакетів).
> - `apt upgrade` - ставить оновлення всіх пакетів. Назва: upgrade - «перейти на новішу версію».
> - `flatpak update` - оновлює всі Flatpak-програми. Назва: update - «оновити».

Значок у треї попросить перезавантаження (якщо було нове ядро) - перезавантаж зараз, до лаб.

**Крок 3. Пакети для лаб.** На свіжій Mint 22.3 їх нема (git, python3-venv, python3-pip, python3-tk):

```bash
sudo apt install git python3-venv python3-pip python3-tk
```

> **Нове тут:**
>
> - `apt install` - ставить програму (пакет) зі сховища. Назва: install - «встановити».

**Крок 4. Тека і venv (урок 03).**

```bash
mkdir -p ~/univer/labs/lr1 ~/univer/praktyka
python3 -m venv ~/univer/.venv
source ~/univer/.venv/bin/activate
python -m pip install --upgrade pip
python -m pip install pytest flake8 black mypy ruff
```

> **Нове тут:**
>
> - `mkdir` - створює нову теку. Назва: make directory - «зробити теку». `-p` - створює і всі проміжні теки шляху; якщо тека вже є - мовчить, без помилки.
> - `python3` - запускає Python: файл, рядок коду або модуль. Назва: Python - на честь комедійного шоу «Monty Python», 3 - третя версія мови. `-m` - запусти модуль як програму: python3 -m pytest, python3 -m venv, python3 -m pdb.
> - `python3 -m venv` - створює окреме середовище Python (venv) для бібліотек лаб. Назва: virtual environment - «віртуальне середовище». `~/univer/.venv` - наш venv на всі лаби; крапка на початку - тека прихована (ls -a її покаже).
> - `source` - виконує файл у поточному bash (venv, ~/.bashrc). Назва: source - «джерело»: виконати команди з файлу-джерела. `~/univer/.venv/bin/activate` - увімкнути venv для лаб; вимкнути - deactivate.
> - `python3 -m pip install` - ставить бібліотеки Python (лише у venv!). Назва: pip installs packages - «pip ставить пакети»; install - «встановити». `--upgrade` - оновити пакет до найновішої версії, якщо він уже є.
> - `~` - домашня тека /home/evgen. Назва: tilde («тильда») - домашня тека.

`python` (без 3) працює саме тому, що ввімкнено venv - у системі є лише `python3`.

**Крок 5. git (урок 24).** Імʼя і пошту - свої:

```bash
git config --global user.name "Твоє Імʼя Прізвище"
git config --global user.email "tvoya.poshta@example.com"
git config --global init.defaultBranch main
git config --global core.quotepath false
```

> **Нове тут:**
>
> - `git config` - читає і змінює налаштування git (імʼя, пошта, редактор). Назва: config - від configuration, «налаштування». `--global` - для тебе на цьому ноутбуці: пише у файл ~/.gitconfig, діє в усіх репо.

`core.quotepath false` - щоб git показував кириличні назви файлів як є, а не `\320\233...`.

**Крок 6. perevir.** Найпростіше - скрипт курсу `ustanovka-mint.sh` (він робить кроки 3-6 сам і додає в `~/.bashrc`
команди `univer` і `perevir`), див. «00 - Почни тут». Після нього - нове вікно термінала. Тестовий файл
`~/univer/praktyka/hello.py`:

```python
def pryvit(imya: str) -> str:
    """Привітання.

    >>> pryvit("Прізвище")
    'Привіт, Прізвище!'
    """
    return f"Привіт, {imya}!"
```

```bash
cd ~/univer/praktyka
perevir hello.py
```

```text
--- doctest (через pytest; зупиню, якщо довше 120 с)
doctest: усе пройшло (1 passed in 0.01s)
--- black (лише перевірка, файл не змінює; виправити: black -l 78 hello.py)
black: оформлення ок
--- flake8 і pycodestyle (рядок до 78 символів, як каже викладач)
flake8: зауважень нема
pycodestyle: зауважень нема
--- ruff
ruff: зауважень нема
--- mypy
Success: no issues found in 1 source file
```

> **Нове тут:**
>
> - `cd` - переходить в іншу теку. Назва: change directory - «змінити теку».
> - `perevir` - перевіряє лабу всіма інструментами одразу (doctest, стиль, типи). Назва: наша назва: «перевір» - перевірка лаби перед здачею.

(Час `0.01s` у тебе інший.)

**Таблиця готовності:**

| Пункт | Перевірка | Має бути |
|---|---|---|
| знімок | `sudo timeshift --list` | рядок з коментарем «свіжа система» |
| оновлення | `apt list --upgradable` | `Listing...` і жодного пакета під ним |
| версія | `cat /etc/os-release` | `PRETTY_NAME="Linux Mint 22.3"` |
| tkinter | `python3 -c "import tkinter; print(tkinter.TkVersion)"` | `8.6` |
| venv | `source ~/univer/.venv/bin/activate`, потім `which python` | `/home/evgen/univer/.venv/bin/python` |
| бібліотеки | `python -m pytest --version` | `pytest` і номер версії |
| git | `git config --global init.defaultBranch` | `main` |
| perevir | `perevir hello.py` | кожен інструмент без зауважень, як вище |

**Типові пастки цього завдання:** venv створено до `python3-venv` → видалити недороблену `~/univer/.venv` і створити
знову; `pip install` поза venv → `externally-managed-environment` (увімкни venv, не `sudo pip`); домашня тека в
знімках Timeshift → диск забивається за тиждень.

Джерела: уроки 01, 02, 03, 24; `00 - Почни тут.md` (швидке налаштування).

</details>

---

### Завдання 2. «Лабу зламано»

**Умова.** Файл `lab_zlamana.py` рахує середню швидкість на ділянках шляху. Doctest-и в ньому **правильні** (це
умова задачі, їх не міняють), а код має кілька помилок - і логічних, і стилю. Треба:

1. знайти всі логічні помилки, користуючись **лише** `python3 -m doctest -v`, повним звітом doctest і pdb
   post-mortem (`python3 -m pdb -c continue`) - не вгадуючи;
2. виправити код, не чіпаючи doctest;
3. довести до чистоти: doctest `0 failed`, black не має що міняти, flake8 мовчить, mypy - `Success`.

Підготовка (venv увімкнено):

```bash
mkdir -p ~/univer/praktyka/p2
cd ~/univer/praktyka/p2
nano lab_zlamana.py
```

> **Нове тут:**
>
> - `nano` - простий редактор файлів у терміналі. Назва: nano - жарт з одиницями: наступник редактора pico (піко < нано).

Встав код (Ctrl+Shift+V) або скопіюй файл з теки `Практика - файли`:

```python
"""Практика 2: середня швидкість на ділянках (навмисно зламано)."""
import math


def to_ms(speed_kmh: float) -> float:
    """Перевести км/год у м/с, округлити до 2 знаків.

    >>> to_ms(36)
    10.0
    >>> to_ms(90)
    25.0
    """
    return round(speed_kmh * 3.6, 2)


def mean_speed(distances: list[float], times: list[float]) -> float:
    """Середня швидкість на всьому шляху, м/с: увесь шлях / увесь час.

    Порожній список ділянок - швидкість 0.0.

    >>> mean_speed([100, 200], [10, 30])
    7.5
    >>> mean_speed([], [])
    0.0
    """
    total=0
    for k in range(len(distances)):
        total += distances[k] / times[k]
    return total / len(distances)


if __name__ == "__main__":
    dani = {
        "ділянка A": ([100.0, 200.0], [10.0, 30.0]),
        "ділянка B": ([], []),
    }
    for nazva, (d, t) in dani.items():
        print(nazva, mean_speed(d, t), "м/с")
```

<details markdown="1"><summary>Розвʼязок</summary>

**Крок 1. Скільки всього впало.**

```bash
python3 -m doctest -v lab_zlamana.py | tail -n 3
```

```text
4 tests in 3 items.
0 passed and 4 failed.
***Test Failed*** 4 failures.
```

> **Нове тут:**
>
> - `python3 -m doctest` - перевіряє приклади >>> з опису функцій. Назва: doc test - «тест у документації»: приклади >>> в описі функції. `-v` - докладно: кожен приклад (Trying, Expecting, ok) і підсумок «N passed and M failed».
> - `tail` - показує останні рядки; -f стежить наживо. Назва: tail - «хвіст»: кінець файлу. `-n` - скільки останніх рядків показати: -n 3 (lines).
> - `|` - передає вивід однієї команди на ввід іншій. Назва: pipe - «труба» (пайп), вертикальна риска.

Упали всі чотири приклади. `-m doctest` тут безпечний: `if __name__ == "__main__":` захищає від чужого провалу.

**Крок 2. Повний звіт - читаємо Expected / Got.**

```bash
python3 -m doctest lab_zlamana.py
```

```text
**********************************************************************
File "/home/evgen/univer/praktyka/p2/lab_zlamana.py", line 21, in lab_zlamana.mean_speed
Failed example:
    mean_speed([100, 200], [10, 30])
Expected:
    7.5
Got:
    8.333333333333334
**********************************************************************
File "/home/evgen/univer/praktyka/p2/lab_zlamana.py", line 23, in lab_zlamana.mean_speed
Failed example:
    mean_speed([], [])
Exception raised:
    Traceback (most recent call last):
      File "/usr/lib/python3.12/doctest.py", line 1361, in __run
        exec(compile(example.source, filename, "single",
      File "<doctest lab_zlamana.mean_speed[1]>", line 1, in <module>
        mean_speed([], [])
      File "/home/evgen/univer/praktyka/p2/lab_zlamana.py", line 29, in mean_speed
        return total / len(distances)
               ~~~~~~^~~~~~~~~~~~~~~~
    ZeroDivisionError: division by zero
**********************************************************************
File "/home/evgen/univer/praktyka/p2/lab_zlamana.py", line 8, in lab_zlamana.to_ms
Failed example:
    to_ms(36)
Expected:
    10.0
Got:
    129.6
**********************************************************************
File "/home/evgen/univer/praktyka/p2/lab_zlamana.py", line 10, in lab_zlamana.to_ms
Failed example:
    to_ms(90)
Expected:
    25.0
Got:
    324.0
**********************************************************************
2 items had failures:
   2 of   2 in lab_zlamana.mean_speed
   2 of   2 in lab_zlamana.to_ms
***Test Failed*** 4 failures.
```

Читаємо як фізики:

- **Баг 1, `to_ms`.** `Got 129.6` = 36 × 3,6. Множимо замість ділити: 1 м/с = 3,6 км/год, тож 36 км/год = 10 м/с.
- **Баг 2, `mean_speed`.** `Got 8.333...` = (100/10 + 200/30) / 2 - це **середнє швидкостей**. А середня швидкість
  = **увесь шлях / увесь час** = 300 / 40 = 7,5 (так і в doctest). Класична помилка з фізики, а не з Python.
- **Баг 3, `mean_speed([], [])`.** Ділення на `len([])` = 0. Doctest каже: має бути `0.0`.

**Крок 3. Post-mortem: на яких даних падає справжня програма.**

```bash
python3 -m pdb -c continue lab_zlamana.py
```

> **Нове тут:**
>
> - `python3 -m pdb` - запускає програму покроково в налагоджувачі pdb. Назва: Python debugger - «налагоджувач Python» (debug - «виловити жуків», помилки). `-c` - виконати команду pdb одразу після старту; -c continue - їхати до падіння і зупинитись там.

Кінець виводу (вище - traceback з рядками самого pdb, їх пропускай) і сеанс:

```text
ZeroDivisionError: division by zero
Uncaught exception. Entering post mortem debugging
Running 'cont' or 'step' will restart the program
> /home/evgen/univer/praktyka/p2/lab_zlamana.py(29)mean_speed()
-> return total / len(distances)
(Pdb) p distances, times
([], [])
(Pdb) u
> /home/evgen/univer/praktyka/p2/lab_zlamana.py(38)<module>()
-> print(nazva, mean_speed(d, t), "м/с")
(Pdb) p nazva, d, t
('ділянка B', [], [])
(Pdb) q
Post mortem debugger finished. The /home/evgen/univer/praktyka/p2/lab_zlamana.py will be restarted
> /home/evgen/univer/praktyka/p2/lab_zlamana.py(1)<module>()
-> """Практика 2: середня швидкість на ділянках (навмисно зламано)."""
(Pdb) q
```

`p distances, times` - у момент падіння обидва списки порожні; `u` - на рівень вище, у головну частину; `p nazva`
каже, яка ділянка винна. Після першого `q` програма перезапускається - тому `q` двічі.

**Крок 4. Що кажуть інструменти стилю і типів.**

```bash
python3 -m flake8 --max-line-length=78 lab_zlamana.py
python3 -m mypy lab_zlamana.py
```

```text
lab_zlamana.py:2:1: F401 'math' imported but unused
lab_zlamana.py:26:10: E225 missing whitespace around operator
lab_zlamana.py:28: error: Incompatible types in assignment (expression has type "float", variable has type "int")  [assignment]
Found 1 error in 1 file (checked 1 source file)
```

> **Нове тут:**
>
> - `python3 -m flake8` - шукає помилки стилю і зайвий код, нічого не змінює. Назва: pyflakes + pep8: обʼєднав дві старі програми перевірки коду. `--max-line-length` - найбільша дозволена довжина рядка; викладач хоче 78 (типово 79).
> - `python3 -m mypy` - перевіряє типи (int, str ...) без запуску програми. Назва: назва не розшифровується (py - від Python).

- `F401` - зайвий `import math` (**помилка стилю 1**), `E225` - `total=0` без пробілів (**помилка стилю 2**).
- mypy підказує ще й про логіку: `total = 0` - ціле, а додаємо дроби. У виправленому коді `total` взагалі не
  потрібен.

Що вміє black, а що ні - перевір на копії:

```bash
cp lab_zlamana.py kopiya.py
python3 -m black -l 78 kopiya.py
python3 -m flake8 --max-line-length=78 kopiya.py
```

```text
reformatted kopiya.py

All done! ✨ 🍰 ✨
1 file reformatted.
kopiya.py:3:1: F401 'math' imported but unused
```

> **Нове тут:**
>
> - `cp` - копіює файл або теку. Назва: copy - «копіювати».
> - `python3 -m black` - сам гарно оформлює код Python (пробіли, переноси). Назва: black - «чорний»: як у Форда, «будь-який колір, якщо він чорний». `-l` - найбільша довжина рядка; викладач хоче 78 (black сам ставить 88).

black виправив пробіли (`total = 0`) і додав порожній рядок після docstring (тому `math` тепер у рядку 3), а зайвий
імпорт лишився: black - форматер, він не прибирає код. Такі речі - руками (або `ruff check --fix`).

**Крок 5. Виправлений файл** (doctest не змінено ні на символ):

```python
"""Практика 2: середня швидкість на ділянках (виправлено)."""


def to_ms(speed_kmh: float) -> float:
    """Перевести км/год у м/с, округлити до 2 знаків.

    >>> to_ms(36)
    10.0
    >>> to_ms(90)
    25.0
    """
    return round(speed_kmh / 3.6, 2)


def mean_speed(distances: list[float], times: list[float]) -> float:
    """Середня швидкість на всьому шляху, м/с: увесь шлях / увесь час.

    Порожній список ділянок - швидкість 0.0.

    >>> mean_speed([100, 200], [10, 30])
    7.5
    >>> mean_speed([], [])
    0.0
    """
    if not times:
        return 0.0
    return sum(distances) / sum(times)


if __name__ == "__main__":
    dani = {
        "ділянка A": ([100.0, 200.0], [10.0, 30.0]),
        "ділянка B": ([], []),
    }
    for nazva, (d, t) in dani.items():
        print(nazva, mean_speed(d, t), "м/с")
```

**Крок 6. Фінальна перевірка.**

```bash
python3 -m doctest -v lab_zlamana.py | tail -n 3
python3 lab_zlamana.py
python3 -m black -l 78 --check lab_zlamana.py
python3 -m flake8 --max-line-length=78 lab_zlamana.py
python3 -m mypy lab_zlamana.py
```

```text
4 tests in 3 items.
4 passed and 0 failed.
Test passed.
ділянка A 7.5 м/с
ділянка B 0.0 м/с
All done! ✨ 🍰 ✨
1 file would be left unchanged.
Success: no issues found in 1 source file
```

> **Нове тут:**
>
> - `python3 -m black`: `--check` - лише перевірити: файл не змінюється, код виходу 1, якщо треба переформатувати.

flake8 мовчить - зауважень нема. Підсумок: **3 логічні помилки** (множення замість ділення, середнє швидкостей
замість шлях/час, ділення на нуль для порожніх даних) і **2 стилю** (зайвий імпорт, пробіли).

Чесне питання на співбесіді: а якщо `times = [0.0]`? Тоді `sum(times)` = 0 і знову `ZeroDivisionError`. Doctest про
це не питає - але варто сказати викладачу про такий граничний випадок (як у ЛР7: граничні випадки - теж тести).

Джерела: урок 04 (Expected / Got, print і return); урок 05 (traceback знизу вгору); урок 06, кроки 7-8
(post-mortem, налагодження doctest); урок 12 (граничні випадки в тестах).

</details>

---

### Завдання 3. Скрипт `zibraty.sh` і щоденна копія

**Умова.**

1. Напиши скрипт `~/univer/zibraty.sh`, який перевіряє **всі** лаби в `~/univer/labs/lr*/`: для кожного `.py` -
   doctest через pytest і flake8 до 78 символів, і друкує одну таблицю «лаба | файл | doctest | flake8». Код
   виходу: 0 - усе чисто, 1 - є провали чи зауваження, 2 - помилка запуску (нема venv чи теки). З номером лаби
   (`bash zibraty.sh 1`) він ще й збирає `~/univer/zdacha/Прізвище_Імʼя_Група_ЛР1.zip`, у якому рівно одна тека
   `Прізвище_Імʼя_Група_ЛР1/` і лише `.py`.
2. Налаштуй щоденну копію `~/univer` в іншу теку через rsync (без `.venv` і `__pycache__`): варіант cron і варіант
   таймера systemd. Поясни, що вибрав би на ноутбуці.

Пастки, які скрипт мусить обійти: `python3 файл.py` дає код 0 навіть при проваленому doctest; файл з `input()` при
імпорті «вішає» pytest; файл без жодного doctest pytest вважає «нема тестів» (код 5); `zip -r` з повним шляхом
кладе в архів увесь `home/evgen/...`; `python3 -m zipfile -c` лишає лише останню теку.

<details markdown="1"><summary>Розвʼязок</summary>

**Скрипт** (файл `zibraty.sh` є і в теці `Практика - файли`):

```bash
#!/bin/bash
# zibraty.sh - перевірити всі лаби в ~/univer/labs і (за бажанням) зібрати zip однієї.
#   bash zibraty.sh      - лише таблиця перевірок
#   bash zibraty.sh 2    - таблиця + архів лаби ~/univer/labs/lr2
#   LABS=~/proba/labs bash zibraty.sh   - інша тека з лабами (для тренування)
# Код виходу: 0 - усе чисто, 1 - є провали чи зауваження, 2 - помилка запуску.
set -uo pipefail

PIB="Прізвище_Імʼя_Група"        # заміни на своє, як у zdaty (урок 23)
LABS="${LABS:-$HOME/univer/labs}"
PY="$HOME/univer/.venv/bin/python"
ZDACHA="$HOME/univer/zdacha"

pomylka() {
    echo "ПОМИЛКА: $1" >&2
    exit 2
}

[ -x "$PY" ] || pomylka "нема venv $PY (урок 03)"
[ -d "$LABS" ] || pomylka "нема теки $LABS"
shopt -s nullglob

rezultat=0
ryadky=()
for lab in "$LABS"/lr*/; do
    for f in "$lab"*.py; do
        "$PY" -m pytest --doctest-modules -q -p no:cacheprovider "$f" < /dev/null > /dev/null 2>&1
        kod=$?
        if [ "$kod" -eq 0 ]; then
            d="ok"
        elif [ "$kod" -eq 5 ]; then
            d="нема тестів"
        else
            d="ВПАВ"
            rezultat=1
        fi
        n=$("$PY" -m flake8 --max-line-length=78 "$f" | wc -l)
        if [ "$n" -eq 0 ]; then
            s="ok"
        else
            s="$n зауваж."
            rezultat=1
        fi
        ryadky+=("$(basename "$lab")|$(basename "$f")|$d|$s")
    done
done
printf '%s\n' "лаба|файл|doctest|flake8" "${ryadky[@]}" | column -t -s '|'

[ "$#" -eq 0 ] && exit "$rezultat"

n="$1"
lab="$LABS/lr$n"
[ -d "$lab" ] || pomylka "нема теки $lab"
files=("$lab"/*.py)
[ "${#files[@]}" -gt 0 ] || pomylka "у $lab нема .py файлів"
nazva="${PIB}_ЛР${n}"
tmp=$(mktemp -d)
mkdir "$tmp/$nazva"
cp "${files[@]}" "$tmp/$nazva/"
mkdir -p "$ZDACHA"
rm -f "$ZDACHA/$nazva.zip"
(cd "$tmp" && zip -qr "$ZDACHA/$nazva.zip" "$nazva")
rm -r "$tmp"
echo
echo "Архів: $ZDACHA/$nazva.zip"
unzip -Z1 "$ZDACHA/$nazva.zip"
exit "$rezultat"
```

> **Нове тут:**
>
> - `set` - вмикає суворий режим bash у скриптах. Назва: set - «встановити» (налаштування самого bash). `-u` - помилка, якщо скрипт бере змінну, якої нема (а не тиха порожнеча); nounset; `-o` - увімкнути налаштування за назвою: -o pipefail; `pipefail` - з -o: труба вважається невдалою, якщо впала будь-яка її частина, а не лише остання.
> - `echo` - друкує текст і значення змінних. Назва: echo - «луна»: повторює те, що йому дали.
> - `exit` - виходить зі скрипта або термінала з кодом. Назва: exit - «вихід». `2` - у zibraty.sh - помилка запуску (нема venv чи теки).
> - `[` - перевіряє умову: код 0 - так, 1 - ні. Назва: [ - друга назва команди test («перевірити»); ] лише закриває умову. `-x` - правда, якщо файл можна запускати (є дозвіл x); `]` - закриває умову, обовʼязково останнім словом і через пробіл; `-d` - правда, якщо є така тека (directory); `-e` - правда, якщо є файл або тека з такою назвою (exists - «існує»); `$#` - кількість аргументів скрипта: [ "$#" -eq 0 ] - скрипт запустили без аргументів.
> - `pomylka` - друкує ПОМИЛКА: ... і зупиняє скрипт. Назва: наша назва: «помилка» латиницею (функція в скриптах zibraty.sh і zdaty).
> - `shopt` - вмикає або вимикає налаштування bash. Назва: shell options - «налаштування оболонки» bash. `-s` - увімкнути (set) налаштування; `nullglob` - шаблон без збігів (*.py у порожній теці) зникає, а не лишається текстом «*.py».
> - `wc` - рахує рядки, слова, символи. Назва: word count - «підрахунок слів»; рахує ще рядки й байти. `-l` - лише кількість рядків (lines).
> - `basename` - дає назву файлу без шляху. Назва: base name - «основна назва»: остання частина шляху.
> - `printf` - друкує текст за шаблоном; \n - Enter. Назва: print formatted - «надрукувати за шаблоном».
> - `column` - вирівнює текст у таблицю. Назва: column - «стовпець»: вирівняти текст у стовпці. `-t` - зробити таблицю: поля кожного рядка - у свої стовпці; `-s` - з -t: який символ ділить поля (типово пробіли): -s '|'.
> - `mktemp` - створює тимчасовий файл чи теку і друкує шлях. Назва: make temporary - «зробити тимчасовий» файл чи теку. `-d` - створити теку, а не файл.
> - `rm` - видаляє файли назавжди, без кошика. Назва: remove - «прибрати, видалити». `-f` - не питати і не лаятись, якщо файлу нема (force - «силоміць»); `-r` - видаляти теки разом з усім, що всередині (recursive).
> - `zip` - пакує файли й теки в .zip. Назва: zip - «мчати, свистіти»: формат ZIP (1989), натяк на швидкість. `-q` - тихо: без рядків adding; `-r` - брати теки з усім, що в них (без -r - лише порожня тека).
> - `unzip` - розпаковує .zip або показує його вміст. Назва: un + zip - «розстібнути»: розпакувати .zip. `-Z` - режим zipinfo; -Z1 - лише назви файлів, по одній у рядку.
> - `$ЗМІННА` - підставляє значення змінної. Назва: dollar («долар») - «значення змінної».
> - `;` - розділяє команди в рядку, виконує всі по черзі. Назва: крапка з комою - роздільник команд.
> - `*` - шаблон: будь-які символи в назві файлу. Назва: asterisk («зірочка») - шаблон «будь-які символи».
> - `2>&1` - помилки йдуть разом зі звичайним виводом. Назва: «потік 2 туди ж, куди потік 1»: помилки разом зі звичайним виводом.
> - `>` - пише вивід у файл, старий вміст стирає. Назва: redirect - «перенаправлення» виводу у файл.
> - `<` - подає файл програмі замість клавіатури. Назва: input redirect - «ввід з файлу».
> - `$( )` - підставляє вивід команди в рядок. Назва: command substitution - «підстановка команди».
> - `'...'` - текст буквально, нічого не підставляється. Назва: одинарні лапки - «буквально, як написано».
> - `#` - коментар: далі до кінця рядка bash не читає. Назва: hash («решітка») - коментар.

**Чому саме так:**

- **pytest, а не `python3 файл.py`** - лише pytest дає чесний код виходу (іспит, питання А4). Код 5 = «тестів
  нема» - окремий стан, не провал.
- **`< /dev/null`** - файл з `input()` на імпорті одразу отримує «кінець вводу» і падає, а не чекає вічно.
  Такий файл у таблиці буде `ВПАВ` - перевір його руками з `printf`, як в уроці 04.
- **`set -uo pipefail` без `-e`.** `-e` зупинив би скрипт на першому ж проваленому pytest, а нам треба перевірити
  всі файли і зібрати таблицю. Помилки запуску ловимо явно (`pomylka`, код 2).
- **`shopt -s nullglob`** - тека без `.py` дає нуль ітерацій, а не «файл» `*.py` (урок 23, «Передбач» 3).
- **`column -t -s '|'`** - вирівнює стовпці навіть з кириличними назвами.
- **Коди 0 / 1 / 2** - скрипт можна ставити в cron чи в `&&`: «лаби брудні» і «скрипт не зміг запуститись» -
  різні речі.
- **zip:** тимчасова тека з **потрібною** назвою, туди лише `.py`, і `zip` **з неї** (`cd "$tmp"`). Без `cd` в архів
  потрапив би повний шлях `home/evgen/univer/labs/lr1/...` і `__pycache__`; `python3 -m zipfile -c` дав би
  `lr1/...` без потрібної назви (іспит, В16).

Збережи скрипт як `~/univer/zibraty.sh` (nano, Ctrl+Shift+V, Ctrl+S, Ctrl+X).

**Перевірка на двох тренувальних лабах.** Справжні лаби не чіпаємо: тренувальні лежать у `~/proba/labs`, а скрипт
бере їх, бо перед ним стоїть `LABS=~/proba/labs` (змінна лише для цієї однієї команди, урок 22).

```bash
mkdir -p ~/proba/labs/lr1 ~/proba/labs/lr2
printf 'def kub(x: float) -> float:\n    """Куб числа.\n\n    >>> kub(2)\n    8\n    """\n    return x ** 3\n' > ~/proba/labs/lr1/kub.py
printf 'def kvadrat(x: float) -> float:\n    """Квадрат числа.\n\n    >>> kvadrat(3)\n    9\n    """\n    return x * 2 \n' > ~/proba/labs/lr2/kvadrat.py
printf 'print("Привіт")\n' > ~/proba/labs/lr2/pryklad.py
cd ~/univer
LABS=~/proba/labs bash zibraty.sh; echo "код $?"
```

```text
лаба  файл        doctest      flake8
lr1   kub.py      ok           ok
lr2   kvadrat.py  ВПАВ         1 зауваж.
lr2   pryklad.py  нема тестів  ok
код 1
```

> **Нове тут:**
>
> - `bash` - оболонка, що виконує команди; bash файл.sh запускає скрипт. Назва: Bourne-Again SHell - «знову оболонка Борна» (гра слів: born again - «народжений знову»). `zibraty.sh` - назва скрипта; bash виконає його рядки по черзі.

У `kvadrat.py` два дефекти: `x * 2` замість `x ** 2` (doctest) і пробіл у кінці рядка (`W291`, flake8).
`pryklad.py` без doctest - не провал. Тепер архів ЛР1:

```bash
LABS=~/proba/labs bash zibraty.sh 1; echo "код $?"
```

```text
лаба  файл        doctest      flake8
lr1   kub.py      ok           ok
lr2   kvadrat.py  ВПАВ         1 зауваж.
lr2   pryklad.py  нема тестів  ok

Архів: /home/evgen/univer/zdacha/Прізвище_Імʼя_Група_ЛР1.zip
Прізвище_Імʼя_Група_ЛР1/
Прізвище_Імʼя_Група_ЛР1/kub.py
код 1
```

Код 1 - бо ЛР2 ще брудна (таблиця завжди про всі лаби). Неіснуюча лаба:

```bash
LABS=~/proba/labs bash zibraty.sh 7 > /dev/null; echo "код $?"
```

```text
ПОМИЛКА: нема теки /home/evgen/proba/labs/lr7
код 2
```

(Повідомлення йде в stderr, тому `> /dev/null` його не сховав.) І перевірка самого скрипта:

```bash
bash -n zibraty.sh
shellcheck zibraty.sh
```

> **Нове тут:**
>
> - `bash`: `-n` - лише перевірити скрипт на синтаксичні помилки, нічого не виконуючи (no execute).
> - `shellcheck` - шукає типові помилки в bash-скриптах. Назва: shell check - «перевірка (скрипта) оболонки».

Обидві команди мовчать - зауважень нема.

**Щоденна копія. Варіант 1: cron** (урок 23). `crontab -e` і рядок (щодня о 21:30):

```text
30 21 * * * mkdir -p /home/evgen/backup && /usr/bin/rsync -a --exclude=.venv --exclude=__pycache__ /home/evgen/univer/ /home/evgen/backup/univer/ >> /home/evgen/backup.log 2>&1
```

Повні шляхи, `>> лог 2>&1`, без `%` у рядку. `--exclude=.venv` без риски в кінці: venv завжди можна перестворити.

**Варіант 2: таймер systemd** (урок 20, крок 7). Два файли в `~/.config/systemd/user/`.
`kopiya-univer.service`:

```text
[Unit]
Description=Копія ~/univer у ~/backup (rsync)

[Service]
Type=oneshot
ExecStartPre=/usr/bin/mkdir -p %h/backup
ExecStart=/usr/bin/rsync -a --exclude=.venv --exclude=__pycache__ %h/univer/ %h/backup/univer/
```

`kopiya-univer.timer`:

```text
[Unit]
Description=Щодня копіювати ~/univer

[Timer]
OnCalendar=daily
Persistent=true

[Install]
WantedBy=timers.target
```

```bash
mkdir -p ~/.config/systemd/user
nano ~/.config/systemd/user/kopiya-univer.service
nano ~/.config/systemd/user/kopiya-univer.timer
systemctl --user daemon-reload
systemctl --user enable --now kopiya-univer.timer
systemctl --user start kopiya-univer.service
ls ~/backup/univer
systemctl --user list-timers
journalctl --user -u kopiya-univer.service -n 5
```

> **Нове тут:**
>
> - `systemctl daemon-reload` - systemd перечитує файли служб після правки. Назва: daemon reload - «перечитати демона»: systemd заново читає файли юнітів. `--user` - перечитати твої власні юніти з ~/.config/systemd/user (без sudo).
> - `systemctl enable` - вмикає автозапуск служби чи таймера. Назва: enable - «увімкнути» автозапуск. `--user` - твій власний юніт (з ~/.config/systemd/user), без sudo; `--now` - ще й запустити зараз, а не лише при наступному старті.
> - `systemctl start` - запускає службу зараз. Назва: start - «запустити». `--user` - твій власний юніт (zapys.service з уроку 20), без sudo.
> - `ls` - показує, що лежить у теці. Назва: list - «список» (вмісту теки).
> - `systemctl list-timers` - показує таймери і коли вони спрацюють. Назва: list timers - «список таймерів». `--user` - твої власні таймери (як zapys.timer з уроку 20).
> - `journalctl` - показує журнал системи і служб. Назва: journal control - «керування журналом» systemd. `--user` - журнал твоїх власних служб (systemctl --user), sudo не треба; `-u` - лише одна служба (u - unit, «одиниця»), напр. -u cron; `-n` - лише останні N рядків, напр. -n 5.

`OnCalendar=daily` = щодня о 00:00 (`systemd-analyze calendar daily` покаже `Normalized form: *-*-* 00:00:00`).
`start` служби - щоб не чекати півночі й одразу побачити копію.

**Що вибрати на ноутбуці - таймер**: о 00:00 чи 21:30 ноутбук часто закритий, а `Persistent=true` виконає пропущену
копію при наступній нагоді; cron пропущене не доганяє. Плюс журнал (`journalctl --user -u ...`) замість ручного
лог-файлу.

**Чесно про межі такої копії:** вона на **тому самому диску** - від «сам стер лабу» рятує, від смерті SSD - ні.
Правило 3-2-1: ще флешка (`rsync -rtv --modify-window=1 --exclude=.venv --exclude=__pycache__ ~/univer/ /media/evgen/НАЗВА/univer/` -
на FAT/exFAT `-a` не працює, урок 01) і приватний GitHub. І це **дзеркало**,
а не історія: зіпсований файл завтра перезапише хорошу копію - історію версій дає git (урок 24).

Джерела: урок 23 (скрипти, `zdaty`, cron, zip); урок 22 (лапки, `"$@"`, коди виходу); урок 20 (таймери, журнал);
урок 01 і 25 (3-2-1).

</details>

---

### Завдання 4. Ноутбук не стартує після оновлення ядра

**Умова.** Учора Диспетчер оновлень поставив нове ядро. Сьогодні після логотипа Mint - чорний екран, нічого не
відбувається. На ноутбуці лише Mint. Склади покроковий план діагностики і відновлення: що робиш, як зрозумієш,
що крок спрацював, і що робиш, якщо ні. Окремо: як написати на форум питання, на яке захочуть відповісти.

<details markdown="1"><summary>Розвʼязок</summary>

**Крок 0. Не панікувати і не перевстановлювати.** Сфотографуй екран телефоном. Згадай, що стоїть з «особливого»:
драйвер NVIDIA (DKMS), PPA, `.deb` з сайтів. Чи є знімок Timeshift і live USB.

**Крок 1. Чи живе система «під» чорним екраном?** Ctrl+Alt+F2.
- Є `login:` → ядро стартувало, зламалась графіка. Увійди, `df -h /` (диск не повний?),
  `sudo journalctl -b -p err` (що впало), `dkms status` (чи зібрано модуль NVIDIA під **нове** ядро - DKMS збирає
  модуль під кожне ядро окремо). Далі - відновлення знімка з TTY: `sudo timeshift --list`,
  `sudo timeshift --restore`.
- Нема реакції → крок 2.

**Крок 2. Старе ядро через GRUB.** Перезавантаж (довге натискання кнопки - лише якщо нічого іншого не реагує). При
старті тримай Esc (UEFI) або Shift (старий BIOS) → «Advanced options for Linux Mint» → рядок з **попереднім**
ядром (без `(recovery mode)`).
- Стартувало → винне нове ядро (або модуль під нього). Крок 3.
- Не стартує й старе → крок 4.

**Крок 3. Робоча система на старому ядрі - діагностика і прибирання.**

```bash
uname -r
sudo journalctl --list-boots
sudo journalctl -b -1 -p err
sudo journalctl -b -1 -e
```

> **Нове тут:**
>
> - `uname` - показує назву і версію ядра Linux. Назва: Unix name - «імʼя Unix-системи». `-r` - версія ядра, яке працює зараз.
> - `journalctl`: `--list-boots` - список завантажень: 0 - поточне, -1 - попереднє; `-b` - лише поточне завантаження (b - boot); -b -1 - попереднє; `-p` - лише ця важливість і гірше: -p err - помилки, -p warning - ще й попередження; `-1` - після -b: попереднє завантаження (-2 - ще раніше); `err` - після -p: рівень «помилка» і все гірше; `-e` - одразу в кінець журналу - найсвіжіші рядки.

`uname -r` - переконатись, що працює **старе** ядро. `-b -1` - попереднє (невдале) завантаження: помилки і останні
рядки перед зависанням. (Якщо зависло раніше, ніж система встигла записати журнал на диск, такого завантаження в
списку не буде - тоді лишається фото екрана; на ноутбуці не перевірено.)

Потім Диспетчер оновлень → Вигляд → Ядра Linux → вибрати **нове** ядро → Видалити (поточне видалити не можна - і
добре). Щоб наступного разу меню GRUB було видно без ловлі клавіші: «Керування системою» → «Меню завантаження» →
«Показати меню», затримка 3 с.

**Крок 4. Не стартує жодне ядро.** Чорний екран саме після логотипа на будь-якому ядрі - схоже на відео: на рядку
Mint у GRUB `e` → `quiet splash` замінити на `nomodeset` → F10 (діє лише на один запуск), увійти, «Керування
драйверами», перезавантаження без `nomodeset`. Ще варіант - GRUB → `(recovery mode)` → пункт `dpkg` («Полагодити
пошкоджені пакунки»), якщо оновлення обірвалось на півдорозі.

**Крок 5. Останній рубіж - live USB.** Завантажся з флешки Mint → Timeshift (є на образі) → вибрати диск і знімок
→ Restore. Нема знімка - скопіюй `~/univer` з внутрішнього диска на іншу флешку через Nemo і лише тоді
перевстановлюй.

**Профілактика:** знімок перед кожним оновленням, live USB поруч (урок 26, крок 3), видиме меню GRUB, лаби в git.

**Питання на форум** (forums.linuxmint.com або r/linuxmint, англійською). Спершу зібрати дані зі старого ядра:

```bash
inxi -c0 -Fxxxz > ~/inxi.txt
sudo journalctl -b -1 -p err > ~/pomylky-b1.txt
uname -r
```

> **Нове тут:**
>
> - `inxi` - показує, що за залізо і які драйвери. Назва: назва не розшифровується (так назвав автор програми). `-c` - кольори; -c0 - без кольорів (для файлу чи форуму); `-F` - повний звіт: усі основні розділи (System, CPU, Graphics, Network...); `-x` - більше подробиць; -xx і -xxx - ще більше; `-z` - ховає MAC-адреси, серійні номери, IP - для форуму.

`-Fxxxz`: усе (F), максимум деталей (xxx), без MAC-адрес і серійних номерів (z). `-c0` - без кодів кольору: у
тестовій Mint без нього у файл потрапляли службові символи кольору (`^C12System:`), а з ним файл чистий і його
зручно вставити на форум. Шаблон допису:

```text
Тема: Mint 22.3 Cinnamon: чорний екран після оновлення ядра 6.14.0-37 → 6.14.0-NN, старе ядро працює

Що сталось: учора Update Manager поставив ядро 6.14.0-NN. Після перезавантаження - чорний екран
після логотипа, Ctrl+Alt+F2 не реагує.
Що вже пробував:
1. Advanced options → 6.14.0-37 - стартує нормально (зараз пишу з нього).
2. nomodeset на новому ядрі - те саме, чорний екран.
Що є з «нестандартного»: драйвер nvidia-driver-580-open з Driver Manager, Secure Boot увімкнено.
Вивід inxi -Fxxxz: (вставити вміст ~/inxi.txt у блок коду)
Помилки попереднього завантаження: (вставити ~/pomylky-b1.txt)
Фото екрана: (посилання)
```

Добре питання = що робив, точний текст і фото, що вже пробував і з яким результатом, `inxi`. Погане - «нічого не
працює, допоможіть». І не виконуй порад, яких не розумієш (explainshell.com), особливо з `rm`, `dd` чи `sudo` перед
скриптом з інтернету.

Джерела: урок 26 (драбина, сценарії Б, В, Г, Є, «Як просити допомоги», крок 4); урок 20 (`journalctl -b -1`);
урок 17 (DKMS, NVIDIA); урок 02 (Ядра Linux у Диспетчері оновлень); урок 01 (Timeshift з live USB).

</details>

## Іспит-самоперевірка: 60 питань

Три блоки по 20 питань - рівень випускного іспиту або співбесіди на сильного джуна. Половина питань не «згадай
команду», а «поясни, чому» і «що зробиш по черзі»: так перевіряють, чи ти розумієш систему, а не памʼятаєш рядки.

**Як складати:**

1. Один блок за раз, 60-90 хвилин, без уроків і без пошуку.
2. Відповідай на папері або вголос, **потім** відкривай «Відповідь». Питання «що виведе» - спершу передбач, потім
   запусти і порівняй.
3. Рахуй бали: 1 - відповідь повна, 0,5 - суть правильна, але бракує важливого, 0 - ні.
4. Кожна відповідь має «Джерело» - урок і розділ, де про це написано. Помилився - читай саме там.

**Код у питаннях справжній.** Вивід у відповідях скопійовано з тестової Linux Mint 22.3 (Python 3.12.3), його
перевіряє скрипт `_перевірка/u_ispyt.sh`. Шлях у виводі - `/home/evgen/...`, у тебе буде твій логін. Для
питань з кодом спершу зроби теку:

```bash
mkdir -p ~/ispyt
cd ~/ispyt
```

Коли в питанні є блок Python і написано «файл `~/ispyt/назва.py`» - відкрий `nano ~/ispyt/назва.py`, встав код
(Ctrl+Shift+V), збережи (Ctrl+S, Ctrl+X) і тоді виконуй команди. Після іспиту теку можна прибрати в смітник:
`gio trash ~/ispyt`.

---

### Блок А. Лаби, оновлення, налагодження (уроки 01-12)

#### А1. Timeshift відновив систему. А лаба?

Учора ввечері ти змінив `~/univer/labs/lr3/lr3_1.py`, а вночі поставив оновлення, після якого система поводиться
дивно. Вранці відновлюєш знімок Timeshift, зроблений позавчора (налаштування типові).

а) Що станеться з учорашніми змінами в `lr3_1.py`?
б) Через місяць SSD ноутбука помер. Що з твоїх даних урятує Timeshift?
в) Чому Timeshift - не резервна копія, і що тоді нею є?

<details markdown="1"><summary>Відповідь</summary>

а) Нічого: домашня тека типово **не входить** у знімок, і відновлення її не чіпає. Офіційний посібник Mint:
знімки «не включають і не змінюють твої особисті дані». Учорашня версія `lr3_1.py` лишиться.

б) Нічого. Знімки лежать у теці `timeshift/snapshots` на диску, і в них нема домашньої теки. Помер диск - пропали і
система, і знімки на ньому, і лаби.

в) Timeshift - «збереження гри» для **системи**: відкотити невдале оновлення чи драйвер. Резервна копія - це копії
**твоїх файлів** на інших носіях за правилом 3-2-1: 3 копії, на 2 різних носіях, 1 - поза домом. Для лаб: git +
приватний GitHub, `rsync` на флешку (можна за розкладом через cron), хмара. І навпаки: якби ти ввімкнув домашню теку
в знімках, відкат знімка відкотив би і лаби до позавчорашніх.

Джерело: урок 01, розділи «Коротко» і «Типові помилки»; урок 25, «Решта звичок» (3-2-1).

</details>

#### А2. Що виведе? (rsync і риска в кінці)

```bash
mkdir -p ~/ispyt/a2/univer/labs && touch ~/ispyt/a2/univer/labs/lab.py
cd ~/ispyt/a2
rsync -a univer backup1/
rsync -a univer/ backup2/
find backup1 backup2 -name lab.py | sort
```

<details markdown="1"><summary>Відповідь</summary>

```text
backup1/univer/labs/lab.py
backup2/labs/lab.py
```

Без риски (`univer`) rsync копіює **саму теку**, з рискою (`univer/`) - лише її **вміст**. Типова помилка: двічі
скопіював без риски в теку, що вже зветься `univer`, - вийшло `univer/univer/...`. Для копії лаб на флешку пиши
`rsync -rtv --modify-window=1 ~/univer/ /media/evgen/НАЗВА/univer/` - риска в джерелі, тоді структура однакова
(на флешці FAT/exFAT `-a` дає `failed to set permissions`, тому `-rt` і `--modify-window=1`, урок 01).

Джерело: урок 01, «Коротко» (правило 3-2-1, rsync) і «Типові помилки»; урок 21, «Самоперевірка» 3.

</details>

#### А3. Що виведе pip поза venv? І чому так задумано

Новий термінал, venv **не** ввімкнено, пакет `python3-pip` уже стоїть (урок 03 або `ustanovka-mint.sh`):

```bash
cd ~
python3 -m pip install requests > pip.txt 2>&1; echo "код $?"
head -n 1 pip.txt
```

Поясни, чому Mint так робить і чому правильна відповідь - venv, а не `sudo pip` чи `--break-system-packages`.

<details markdown="1"><summary>Відповідь</summary>

```text
код 1
error: externally-managed-environment
```

Це PEP 668: у Mint 22 (база Ubuntu 24.04) лежить файл `/usr/lib/python3.12/EXTERNALLY-MANAGED`, і pip відмовляється
ставити пакети в **системний** Python. Причина: на `/usr/bin/python3` працюють програми самої Mint (Диспетчер
оновлень, Джерела програм та інші). Симуляція видалення `python3` тягне за собою понад сотню пакетів, серед них
mintupdate. Пакет з pip, що підмінив бібліотеку apt, може зламати їх тихо, через тижні.

- `sudo pip` - пише в системні теки від root, саме те, від чого захищає PEP 668.
- `--break-system-packages` - ти сам вимикаєш захист.
- venv (`~/univer/.venv`) - окрема тека зі своїм Python і своїми бібліотеками: ламай скільки хочеш, видалив теку -
  створив знову. Для програм-утиліт (uv, ruff як команда) - `pipx`.

Джерело: урок 02, «Типові помилки» і «Самоперевірка» 2; урок 03, «Коротко» (venv); урок 25, «Що НЕ запускати з
sudo».

</details>

#### А4. Код виходу 0 - отже, все добре?

Файл `~/ispyt/kv.py`:

```python
def kvadrat(x):
    """
    >>> kvadrat(3)
    9
    """
    return x * 2


if __name__ == "__main__":
    import doctest

    doctest.testmod()
```

```bash
cd ~/ispyt
source ~/univer/.venv/bin/activate
python3 kv.py > /dev/null; echo "код $?"
python3 -m pytest --doctest-modules -q -p no:cacheprovider kv.py > /dev/null; echo "код $?"
```

Що виведуть дві останні команди? Чому це важливо для скриптів на кшталт `zdaty` і для cron?

<details markdown="1"><summary>Відповідь</summary>

```text
код 0
код 1
```

doctest справді впав (`kvadrat(3)` дає 6), але `doctest.testmod()` лише **друкує** звіт, а код виходу програми
лишається 0. pytest повертає 1, коли є провали. Тому:

- `python3 kv.py && echo готово` надрукує «готово» навіть зі зламаним кодом;
- скрипт перевірки (урок 23, `zdaty`) чи завдання cron, які дивляться на код виходу, мають запускати doctest через
  pytest, а не через `python3 файл.py`;
- людині для читання зручніший `python3 kv.py -v` (видно кожен приклад), а **машині** - pytest.

Джерело: урок 03, «Типові помилки» (останній пункт); урок 04, «Типові помилки» п. 11 і «Самоперевірка» 1; урок 22,
«Код виходу»; урок 23, крок 2 (`perevir_odyn`).

</details>

#### А5. Чужий провал: що виведе і чому

Файл `~/ispyt/lab5.py` (так виглядають заготовки ЛР5: `testmod()` просто внизу файлу):

```python
import doctest


def dvichi(x):
    """
    >>> dvichi(2)
    4
    """
    return x * 2


doctest.testmod()
```

```bash
cd ~/ispyt
python3 -m doctest lab5.py | tail -n 3
python3 -m doctest lab5.py > /dev/null; echo "код $?"
```

<details markdown="1"><summary>Відповідь</summary>

```text
1 items had failures:
   1 of  21 in __main__.DebugRunner
***Test Failed*** 1 failures.
код 0
```

Код правильний (`dvichi(2)` = 4), а провал - **чужий**. При `python3 -m doctest` головним модулем (`__main__`) стає
сам doctest. Він імпортує `lab5.py`, на імпорті виконується рядок `doctest.testmod()`, а `testmod()` без аргументів
тестує модуль `__main__` - тобто власні приклади doctest, один з яких у клас `DebugRunner` падає. Навіть код виходу
0: звіт надрукувала твоя ж `testmod()` під час імпорту, а сам `-m doctest` твій файл перевірив успішно.

Ліки: обгорнути виклик у `if __name__ == "__main__":` або перевіряти `python3 lab5.py -v` чи pytest.

Джерело: урок 04, «Типові помилки» п. 10 і «Самоперевірка» 3; урок 10, «Коротко», «Типові помилки» і
«Самоперевірка» 1.

</details>

#### А6. venv увімкнено, а pip знову «externally-managed»

Ти поставив Python 3.13 через uv і зробив:

```text
~/.local/bin/uv venv --python 3.13 .venv313
source .venv313/bin/activate
pip install numpy
error: externally-managed-environment
```

Venv же ввімкнено (`(.venv313)` на початку рядка). Чому так, як це перевірити однією командою і як виправити
(два способи)?

<details markdown="1"><summary>Відповідь</summary>

`uv venv` без `--seed` робить venv **без pip**. Набираєш `pip` - bash шукає його по теках PATH зліва направо:
`.venv313/bin` стоїть першою, але pip там нема, тож знаходиться наступний - системний `/usr/bin/pip`, а він ставить
у системний Python і впирається в PEP 668.

Перевірка: `which pip` (або `type pip`) покаже `/usr/bin/pip` замість `.../.venv313/bin/pip`.

Виправлення: `uv venv --seed --python 3.13 .venv313` (pip покладеться у venv) або ставити через
`~/.local/bin/uv pip install numpy` (uv сам знає, що venv активний).

Загальний урок: «команда не та» - майже завжди PATH. `type` / `which` перед тим, як щось лагодити.

Джерело: урок 02, «Типові помилки» (venv від uv) і «Самоперевірка» 4; урок 22, «PATH» і «Де команда?».

</details>

#### А7. Що виведе? (`f"{x=}"` і типи)

Файл `~/ispyt/typy.py`, запуск `python3 typy.py`:

```python
x = "2"
y = 2
print(x * 3, y * 3)
print(f"{x=} {y=}")
print(type(x), type(y))
```

<details markdown="1"><summary>Відповідь</summary>

```text
222 6
x='2' y=2
<class 'str'> <class 'int'>
```

`print(x)` надрукував би просто `2` - і рядок, і число виглядають однаково. `f"{x=}"` друкує `repr`: лапки одразу
кажуть «це рядок». Так ловиться найчастіший баг першого курсу - забутий `int(...)` навколо `input()`: ввів 5, а
програма видала `55` замість `10`, і жодного traceback.

Джерело: урок 05, «Друк для налагодження» і «Самоперевірка» 2; урок 04, «Типові помилки» п. 4.

</details>

#### А8. Знайди помилку (assert)

Файл `~/ispyt/a8.py`, запуск `python3 a8.py`:

```python
# БАГ: знайди помилку
g = -9.81
assert (g > 0, "g має бути додатне")
print("далі")
```

Що надрукує програма? Де помилка, як правильно, і чи годиться `assert` для перевірки числа, яке ввів користувач?

<details markdown="1"><summary>Відповідь</summary>

```text
/home/evgen/ispyt/a8.py:3: SyntaxWarning: assertion is always true, perhaps remove parentheses?
  assert (g > 0, "g має бути додатне")
далі
```

Дужки зробили з умови і тексту **кортеж** з двох елементів, а непорожній кортеж завжди істинний. Python 3.12
попереджає, але програма йде далі з `g = -9.81`. Правильно без дужок: `assert g > 0, "g має бути додатне"`.

Для вводу користувача assert не годиться: `python3 -O` вимикає всі assert. Там - звичайна умова і повідомлення
(або `raise ValueError(...)`). assert - для «цього не може бути, якщо мій код правильний».

Джерело: урок 05, «Типові помилки» (assert з дужками, assert для вводу) і «Самоперевірка» 3.

</details>

#### А9. post-mortem чи `breakpoint()`?

Програма за 10 хвилин обробляє 1000 файлів вимірювань і десь посередині падає з `ZeroDivisionError` у функції
`mean`. Одногрупник радить: «Постав `breakpoint()` у `mean` і дивись». Чому це погана порада тут? Що зробиш ти,
нічого не змінюючи в коді, і які команди pdb набереш першими? Коли `breakpoint()` усе ж правильний вибір?

<details markdown="1"><summary>Відповідь</summary>

`breakpoint()` у `mean` зупинить програму на **кожному** виклику - до падіння доведеться 500 разів тиснути `c`.
І забутий `breakpoint()` потім «вішає» pytest (`reading from stdin while output is captured`) і `perevir`.

Краще **post-mortem** - налагодження вже впалої програми, змінні в момент падіння ще живі:

- `python3 -m pdb -c continue vymiry.py` - працює повним ходом і зупиняється рівно в місці падіння;
- або, якщо вже впало в `python3 -i vymiry.py`, - `import pdb; pdb.pm()`.

Далі: `p values` (що прийшло в `mean`), `u` (на рівень вище, у функцію, що викликала) і `p name` (яка серія
винна), `w` (увесь стек). Після `q` у варіанті `-c continue` програма перезапускається - `q` двічі. Сам
`python3 -i` без `pdb.pm()` показує лише глобальні імена: локальних змінних функції після падіння вже нема.

`breakpoint()` (або `b рядок, умова` у pdb) - коли програма **не падає**, а дає не те число, і ти знаєш, де
дивитись; для циклу - точка з умовою `b 14, k == 500`, а не 500 разів `c`.

Джерело: урок 05, «Типові помилки» (забутий `breakpoint()`) і «Самоперевірка» 5; урок 06, «Чотири способи
запустити pdb», «Крок 7. Post-mortem», «Типові помилки», «Самоперевірка» 1-2.

</details>

#### А10. Знайди помилку в сеансі pdb

У функції є змінна `c = 3e8` (швидкість світла). Ти зупинився в pdb і набрав `c`, щоб побачити її значення, а
програма поїхала до кінця. Потім в іншому запуску хочеш перевірити, що буде на Місяці, набираєш `!G = 1.62`, але
функція далі рахує з `G = 9.81`. Що пішло не так у кожному випадку і як правильно?

<details markdown="1"><summary>Відповідь</summary>

1. `c` - це команда pdb continue, вона сильніша за імʼя змінної. Подивитись змінну: `p c`; змінити: `!c = ...`.
   Те саме з `n`, `s`, `l`, `a`, `b`, `h`.
2. `!G = 1.62` усередині функції створює **локальну** змінну `G`, глобальна лишається 9.81. Треба
   `!global G; G = 1.62`.

Джерело: урок 06, «Усі команди pdb» (група «Змінити»), «Типові помилки» і «Самоперевірка» 3.

</details>

#### А11. Що виведе? (logging)

Файл `~/ispyt/log.py`, запуск `python3 log.py`:

```python
import logging

logging.warning("перше")
logging.basicConfig(level=logging.DEBUG)
logging.debug("друге")
logging.warning("третє")
```

<details markdown="1"><summary>Відповідь</summary>

```text
WARNING:root:перше
WARNING:root:третє
```

Перший виклик `logging.warning(...)` сам налаштовує logging з рівнем WARNING. Пізніший `basicConfig(level=DEBUG)`
уже нічого не змінює, тому `debug("друге")` не друкується. `basicConfig` - найпершим рядком програми.

Бонус-питання «навіщо logging, якщо є print»: рівнем (DEBUG → WARNING) вимикаєш усі налагоджувальні рядки, не
видаляючи їх; logging пише в stderr і тому не ламає doctest, а забутий `print` у функції - ламає (`Got` з зайвим
рядком).

Джерело: урок 06, «Типові помилки» (останній пункт) і «Самоперевірка» 5; урок 05, «Типові помилки» (забутий
print).

</details>

#### А12. Що виведе? (float)

Файл `~/ispyt/fl.py`, запуск `python3 fl.py`:

```python
import math

s = 0.1 + 0.2
print(s == 0.3, math.isclose(s, 0.3))
print(s, f"{s:.3f}", round(s, 3))
```

Як це повʼязано з doctest, де очікують `'v = 0.3 м/с'`, а отримують `'v = 0.30000000000000004 м/с'`?

<details markdown="1"><summary>Відповідь</summary>

```text
False True
0.30000000000000004 0.300 0.3
```

0,1 і 0,2 не записуються у двійковому вигляді точно, сума має крихітну похибку. Порівнювати float через `==` -
помилка; для «чи рівні» - `math.isclose` (для чисел біля нуля - з `abs_tol`). Для **виводу** - формат `:.3f` або
`round`: саме так лікується doctest з `0.30000000000000004` (яке саме - залежить від умови: `:.3f` дає рядок рівно з
трьома знаками). У ЛР7 з тієї ж причини прямий кут при дробових координатах не перевіряють через `== 0`.

Джерело: урок 12, «Типові помилки» (рядок `0.1 + 0.2 == 0.3`) і «Самоперевірка» 4.

</details>

#### А13. Що виведе? (відʼємне число в printf)

Набери в терміналі по черзі:

```bash
printf "-5\n" | python3 -c "print(int(input()) * 2)"
printf -- "-5\n" | python3 -c "print(int(input()) * 2)"
printf '%s\n' -5 | python3 -c "print(int(input()) * 2)"
```

<details markdown="1"><summary>Відповідь</summary>

```text
bash: printf: -5: invalid option
printf: usage: printf [-v var] format [arguments]
Traceback (most recent call last):
  File "<string>", line 1, in <module>
EOFError: EOF when reading a line
-10
-10
```

У першому рядку bash вважає `-5` опціями самого `printf`, нічого не друкує, і Python отримує порожній ввід -
`EOFError`. Дві риски `--` кажуть «опції скінчились»; `'%s\n'` робить `-5` аргументом, а не форматом. Обидва
способи - для перевірки лаб з відʼємними числами (ЛР2).

Джерело: урок 04, «Типові помилки» п. 7-8; урок 07, «Типові помилки» п. 1 і «Самоперевірка» 2.

</details>

#### А14. Що виведе і що виправити? (print чи return)

Файл `~/ispyt/pr.py`:

```python
def speed_text(v_kmh: float) -> str:
    """
    >>> speed_text(36)
    '10.0 м/с'
    """
    print(f"{v_kmh / 3.6:.1f} м/с")


def age_chat(age: int) -> None:
    """
    >>> age_chat(18)
    Тобі 18 років
    """
    return f"Тобі {age} років"
```

```bash
cd ~/ispyt
python3 -m doctest pr.py
```

<details markdown="1"><summary>Відповідь</summary>

```text
**********************************************************************
File "/home/evgen/ispyt/pr.py", line 11, in pr.age_chat
Failed example:
    age_chat(18)
Expected:
    Тобі 18 років
Got:
    'Тобі 18 років'
**********************************************************************
File "/home/evgen/ispyt/pr.py", line 3, in pr.speed_text
Failed example:
    speed_text(36)
Expected:
    '10.0 м/с'
Got:
    10.0 м/с
**********************************************************************
2 items had failures:
   1 of   1 in pr.age_chat
   1 of   1 in pr.speed_text
***Test Failed*** 2 failures.
```

Читай лапки: `Expected` **у лапках** = функція має **повернути** рядок (`speed_text`: замінити `print(...)` на
`return ...`). `Expected` **без лапок** = функція має **надрукувати** (`age_chat`: `print(...)` замість `return`, як
`age_chat` у ЛР2). Анотації (`-> str`, `-> None`) кажуть те саме, і mypy це спіймав би до запуску.

Джерело: урок 04, «Типові помилки» п. 5 і «Самоперевірка» 2; урок 07, «Типові помилки» п. 3 і «Самоперевірка» 3.

</details>

#### А15. Чому лаба «зависає» і як перевіряти без вікон

Поясни для ЛР3 (графіки matplotlib) і ЛР4 (turtle): чому після запуску термінал «завис», як перевірити doctest, не
відкриваючи вікон, і що зробити, щоб `python3 -m doctest lab4.py` не відкривав вікно черепашки. Що буде, якщо
запустити малюнок через ssh?

<details markdown="1"><summary>Відповідь</summary>

- ЛР3: `plt.show()` чекає, доки закриєш вікно графіка, і лише тоді йде `doctest.testmod()`. Без вікон:
  `MPLBACKEND=Agg` перед командою (`printf "12\n" | MPLBACKEND=Agg python3 lr3_1.py`); попередження
  `FigureCanvasAgg is non-interactive` тоді нормальне.
- ЛР4: `turtle.done()` тримає вікно і програма на ньому чекає; закрий вікно або Ctrl+C. Математику (кути, позиції)
  перевіряють doctest-ом з `turtle.TNavigator()` - він рахує позицію без вікна.
- Щоб `python3 -m doctest` не малював: код малювання - під `if __name__ == "__main__":`, бо doctest імпортує файл,
  а все, що на верхньому рівні, на імпорті виконується.
- Через ssh чи в TTY нема екрана: `_tkinter.TclError: no display name and no $DISPLAY environment variable`.

Джерело: урок 08, «Коротко», «Типові помилки» п. 5 і 8, «Самоперевірка» 2; урок 09, «Коротко» і «Типові помилки».

</details>

#### А16. Що виведе? (файл з назвою модуля)

```bash
mkdir -p ~/ispyt/a16 && cd ~/ispyt/a16
printf 'import turtle\n\nturtle.forward(100)\nturtle.done()\n' > turtle.py
python3 turtle.py 2>&1 | tail -n 1
```

<details markdown="1"><summary>Відповідь</summary>

```text
AttributeError: partially initialized module 'turtle' has no attribute 'forward' (most likely due to a circular import)
```

`import turtle` спершу шукає модуль у теці скрипта, знаходить **твій** `turtle.py` і імпортує його замість
справжнього. Вікно навіть не відкривається. Не називай файли як модулі (`turtle.py`, `math.py`, `random.py`) -
перейменуй, наприклад, `lr4_1.py`.

Джерело: урок 09, «Типові помилки» і «Самоперевірка» 3.

</details>

#### А17. Що виведе? (timeout)

```bash
timeout 1 python3 -c "while True: pass"; echo "код $?"
```

Навіщо це в ЛР5 і чим відрізняється від Ctrl+C?

<details markdown="1"><summary>Відповідь</summary>

```text
код 124
```

`timeout 1` зупиняє команду через 1 секунду, а код **124** каже «зупинено за часом» - не плутаєш з помилкою програми
(1). У ЛР5 деякі doctest (`pi_gregory(10)`) рахують хвилинами - `timeout 60 python3 ...` не дасть терміналу
«зависнути» навічно, а малі n краще перевірити окремим викликом. Ctrl+C - те саме вручну: Python покаже
`KeyboardInterrupt` і рядок, де крутився цикл.

Джерело: урок 10, «Коротко», «Типові помилки» і «Самоперевірка» 5; урок 08, «Типові помилки» п. 2.

</details>

#### А18. Що виведе? (зріз і `del`)

Файл `~/ispyt/zriz.py`, запуск `python3 zriz.py`:

```python
lst = [10, 11, 12, 13, 14, 15, 16, 17, 18, 19]
del lst[2::3]
print(lst)
```

<details markdown="1"><summary>Відповідь</summary>

```text
[10, 11, 13, 14, 16, 17, 19]
```

`[2::3]` - **позиції** 2, 5, 8 (з нуля), тобто значення 12, 15, 18. Зрізи працюють за позиціями, а не за значеннями
- пастка решета в ЛР7, де значення і позиції легко сплутати.

Джерело: урок 12, «Типові помилки» (IndexError у решеті) і «Самоперевірка» 2.

</details>

#### А19. «Мовчить - значить, пройшло»?

Студент запускає `python3 lr6_1.py` (файл ЛР6 від викладача) - порожньо. Каже: «Тести пройшли». Чи правий він?
Чому для ЛР6 `python3 -m doctest lr6_1.py` безпечний, а для ЛР5 той самий запуск показує чужий провал? Яка одна
команда дає чесну відповідь для будь-якої лаби?

<details markdown="1"><summary>Відповідь</summary>

Не правий. У файлі ЛР6 **нема** `doctest.testmod()`, тож `python3 lr6_1.py` лише визначає функції - тести ніхто
не запускав. Тиша нічого не означає.

`python3 -m doctest lr6_1.py` для ЛР6 правильний: він сам запускає приклади і друкує лише провали (тиша тут = усе
пройшло, а `-v | tail -n 3` дає підсумок). У ЛР5 той самий запуск дає чужий провал, бо у файлі ЛР5 `testmod()`
стоїть на верхньому рівні (питання А5).

Чесно для будь-якої лаби: `python3 -m pytest --doctest-modules -q файл.py` - пише `N passed` / `failed` і дає код
виходу 0 або 1 (для файлів з `input()` - ще `-s` і `printf`).

Джерело: урок 11, «Коротко» і «Самоперевірка» 2; урок 10, «Коротко»; урок 04, «Перевір перед здачею».

</details>

#### А20. Сценарій: завтра дедлайн, а Диспетчер оновлень пропонує 40 оновлень, серед них нове ядро

Що робиш і в якому порядку? Поясни, чому порядок саме такий.

<details markdown="1"><summary>Відповідь</summary>

1. **Спершу лаби в безпеку**, незалежно від системи: `git add`, `git commit`, `git push` у приватний репозиторій
   (або `rsync` на флешку). Timeshift лаби не зберігає.
2. **Знімок системи:** `sudo timeshift --create --comments "перед оновленням"`.
3. **Оновлення** через Диспетчер оновлень (або `sudo apt update`, `sudo apt upgrade`), **читаючи список**, без
   `-y` наосліп. Якщо `Could not get lock` - зачекай, lock-файли не видаляй.
4. Перезавантаження, коли просить значок у треї (нове ядро вмикається лише після нього).
5. Перевірка: `uname -r`, `source ~/univer/.venv/bin/activate`, `perevir` на поточній лабі. Venv переживе
   оновлення, бо системний Python 3.12 лишається тим самим.
6. Якщо нове ядро не стартує - GRUB → Advanced options → попереднє ядро; не допомогло - відновити знімок.

Чесний варіант для дедлайну: відкласти **оновлення ядра** на день після здачі (Mint 22.x підтримується до 2029, день
нічого не змінить), але безпекові оновлення програм поставити.

Джерело: урок 01, «Коротко»; урок 02, «Коротко» і «Типові помилки»; урок 24, «Коротко»; урок 26, «Сценарії
порятунку» (Б).

</details>

---

### Блок Б. Mint як система (уроки 13-18, 25, 26)

#### Б1. Чотири комбінації клавіш

а) Як заблокувати екран, коли відходиш від ноутбука? б) Що насправді робить Super+L? в) Чим небезпечна
Ctrl+Alt+Backspace і чим вона відрізняється від Ctrl+Alt+Delete? г) Що робить Ctrl+Alt+Esc?

<details markdown="1"><summary>Відповідь</summary>

а) Ctrl+Alt+L. б) Відкриває «Збільшувальне скло» (Looking Glass) - налагоджувач Cinnamon, екран лишається
**незаблокованим**. в) Миттєво вбиває весь графічний сеанс без питань (у Mint увімкнено навмисно), незбережене
пропадає; Ctrl+Alt+Delete - вихід із сеансу, спершу питає. г) Перезапускає Cinnamon (панель, робочий стіл), вікна і
програми лишаються.

Джерело: урок 13, «Коротко» (гарячі клавіші), «Типові помилки» і «Самоперевірка» 1, 3; урок 25, «Решта звичок».

</details>

#### Б2. Сценарій: панель і меню застигли, мишка рухається

Твої кроки по черзі, від найлагіднішого. Що робити, якщо застигло все і навіть Ctrl+Alt+Esc не допоміг? А якщо
проблема почалась після того, як ти поставив новий аплет?

<details markdown="1"><summary>Відповідь</summary>

1. Ctrl+Alt+Esc - перезапуск Cinnamon, вікна і програми лишаються.
2. Не допомогло - Ctrl+Alt+F2, текстовий вхід (TTY): логін і пароль. Там `top` (або `pgrep -af назва`) - знайти, що
   «їсть» процесор чи памʼять, `kill PID` (спершу без `-9`). Назад до графіки - Ctrl+Alt+F7. Крайній випадок -
   `sudo reboot` з TTY, а не кнопка живлення.
3. Почалось після аплету - «Аплети» → «Налаштування» → вибрати його → «-». Якщо через нього не стартує панель -
   права кнопка на панелі → «Вирішення проблем» → «Повернути типові значення налаштувань» (скине налаштування панелі).

Джерело: урок 13, «Типові помилки» і «Самоперевірка» 3; урок 19, «Коротко»; урок 26, «Драбина порятунку» і
«Руками», крок 1.

</details>

#### Б3. Що виведе? (посилання і `rm -r`)

```bash
mkdir -p ~/ispyt/b3/lr1 && touch ~/ispyt/b3/lr1/lab.py
cd ~/ispyt/b3 && ln -s lr1 posylannya
rm -r posylannya/
ls -A lr1; echo "--"; ls -l posylannya | cut -c1
```

<details markdown="1"><summary>Відповідь</summary>

```text
rm: cannot remove 'posylannya/': Not a directory
--
l
```

Риска в кінці «проводить» шлях крізь посилання в справжню теку: `rm -r` стирає **вміст** `lr1` (там тепер
порожньо), а саме посилання лишається (`l` - тип «посилання»), і `rm` ще й пише помилку - легко подумати, що нічого
не сталось. Посилання видаляють без `-r` і без риски: `rm posylannya`. А свої файли безпечніше класти в смітник:
`gio trash`.

Джерело: урок 14, «Типові помилки» (перший пункт) і «Коротко» (кошик і термінал).

</details>

#### Б4. Сценарій: посеред оновлення зникло світло

Після старту `sudo apt upgrade` пише `E: dpkg was interrupted, you must manually run 'sudo dpkg --configure -a' to
correct the problem.`, а в іншому вікні відкритий Диспетчер оновлень. Що робиш по черзі і чого **не** робиш? Що,
якщо система після обриву навіть не завантажує робочий стіл?

<details markdown="1"><summary>Відповідь</summary>

1. Закрити Диспетчер оновлень (і Менеджер програм) - інакше `Could not get lock /var/lib/dpkg/lock-frontend`.
2. `sudo dpkg --configure -a` - доналаштувати перервані пакети.
3. `sudo apt-get install -f` - докачати залежності, яких бракує.
4. `sudo apt update`, потім `sudo apt upgrade` - доробити оновлення.

Не робити: не видаляти lock-файли (dpkg прямо пише, що це завжди неправильно), не вбивати процес посеред
встановлення.

Графіка не стартує - Ctrl+Alt+F2 і ті самі команди з TTY, або GRUB → recovery mode → пункт `dpkg` («Полагодити
пошкоджені пакунки»).

Джерело: урок 16, «Типові помилки»; урок 26, «Передбач» 2, «Сценарії порятунку» (Д), «Самоперевірка» 4.

</details>

#### Б5. Що виведе? (umask і chmod)

```bash
mkdir -p ~/ispyt/b5 && cd ~/ispyt/b5
umask 0002
touch nove.txt && mkdir -p nova
stat -c '%A %a %n' nove.txt nova
chmod 640 nove.txt && stat -c '%A %a' nove.txt
chmod g-r,o+r nove.txt && stat -c '%A %a' nove.txt
```

<details markdown="1"><summary>Відповідь</summary>

```text
-rw-rw-r-- 664 nove.txt
drwxrwxr-x 775 nova
-rw-r----- 640
-rw----r-- 604
```

umask 0002 (так у Mint після входу) «забирає» право w в інших: файл 666 → 664, тека 777 → 775. 640 = rw- (6) r-- (4)
--- (0). Останній рядок дивний, але законний: група не читає, а «інші» - читають. Таке поєднання майже завжди -
помилка; звичайні права для файлу - 644 або 600.

Джерело: урок 15, «Коротко» (числа, `chmod o-r`, umask у Mint) і «Самоперевірка» 1.

</details>

#### Б6. Знайди помилку (групи)

Для плати Arduino треба група `dialout`. Ти виконав `sudo usermod -G dialout evgen`, перезайшов - і тепер будь-яка
команда з `sudo` пише `evgen is not in the sudoers file.` Що сталось, як треба було, і як тепер повернути права?

<details markdown="1"><summary>Відповідь</summary>

Без `-a` (append) `usermod -G` **замінює** всі додаткові групи однією `dialout` - ти випав з групи `sudo`.
Правильно: `sudo usermod -aG dialout "$USER"`, вийти з сеансу і зайти, перевірити `groups`.

Повернути: sudo вже не працює, тож потрібен root іншим шляхом - GRUB → Advanced options → `(recovery mode)` →
`root` → `mount -o remount,rw /` → `usermod -aG sudo evgen` → `reboot`. (Або інший адміністратор ноутбука:
«Користувачі та групи» → «Тип обліківки» → «Адміністратор».)

Джерело: урок 15, «Коротко» (групи), «Типові помилки» і «Самоперевірка» 5; урок 26, «Сценарії порятунку» (Г).

</details>

#### Б7. Чому «Permission denied» на власному файлі?

Ти створив новий файл лаби `sudo nano ~/univer/labs/lr1/lab2.py`, а ще раніше запускав `sudo xed`. Тепер без sudo
файл не зберігається, а xed поводиться дивно. Поясни механізм, як це діагностувати однією командою, як виправити і як
правильно редагувати **системні** файли.

<details markdown="1"><summary>Відповідь</summary>

Новий файл, створений від root, стає власністю root - тобі вже не можна в нього писати (наявний файл `sudo nano`
зберігає зі старим власником). Віконна програма з sudo так само лишає у твоїй домашній теці свої налаштування вже
від root.

Діагностика: `stat -c '%U' ~/univer/labs/lr1/lab2.py` → `root`.

Виправлення: `sudo chown "$USER:$USER" ~/univer/labs/lr1/lab2.py` (теку - з `-R`; після віконних програм практики
радять `sudo chown -R "$USER:$USER" "$HOME"`).

Системні файли - `sudoedit /etc/файл` (= `sudo -e`): відкриває твій звичайний редактор, а зберігає від root. Свої
файли - ніколи через sudo.

Джерело: урок 15, «Типові помилки» і «Самоперевірка» 4; урок 25, «Що НЕ запускати з sudo».

</details>

#### Б8. Що виведе? (apt у Mint)

```bash
type apt
type apt-get
apt-get install ncdu
```

Чому `apt install ncdu` без sudo питає пароль, а `apt-get` - ні?

<details markdown="1"><summary>Відповідь</summary>

```text
apt is /usr/local/bin/apt
apt-get is /usr/bin/apt-get
E: Could not open lock file /var/lib/dpkg/lock-frontend - open (13: Permission denied)
E: Unable to acquire the dpkg frontend lock (/var/lib/dpkg/lock-frontend), are you root?
```

`apt` у Mint - не справжній apt, а обгортка Mint `/usr/local/bin/apt`: вона стоїть у PATH раніше за `/usr/bin` і
сама додає `sudo` до install, remove, update, upgrade. `apt-get` - справжня програма без обгортки, без `sudo` вона не
може взяти lock бази пакетів. Що насправді виконає обгортка - `apt help install`.

Джерело: урок 16, «Коротко» (apt у Mint - обгортка), «Типові помилки» і «Самоперевірка» 1; урок 22, «PATH».

</details>

#### Б9. Знайди помилку: три спроби поставити `.deb`

Файл `prog.deb` лежить у «Завантаженнях». Ти в домашній теці.

```text
1) sudo apt install prog.deb      → E: Unable to locate package prog.deb
2) sudo apt install ./prog.deb    → E: Unsupported file ./prog.deb given on commandline
3) apt deb ~/Завантаження/prog.deb  → поставилось, але програма не запускається: бракує бібліотек
```

Що не так у кожній і як правильно? Чи оновлюватиметься така програма сама?

<details markdown="1"><summary>Відповідь</summary>

1. Без `./` apt шукає **пакет** з такою назвою в сховищах, а не файл.
2. `./prog.deb` - файл у **поточній** теці, а ти не в «Завантаженнях».
3. `apt deb` = `sudo dpkg -i`: ставить сам файл, але **не докачує залежності**. Лікування: `sudo apt-get install -f`.

Правильно: перейти в теку з файлом (`cd ~/Завантаження`, `ls *.deb`) і `sudo apt install ./prog.deb` - apt сам
докачає залежності. Оновлюватиметься лише тоді, коли пакет додав своє сховище (так роблять VS Code, Chrome); інакше
нова версія - знову вручну з сайту.

Джерело: урок 16, «Коротко» (.deb з сайту), «Типові помилки» і «Самоперевірка» 3; урок 27, «Типові помилки».

</details>

#### Б10. Сценарій: «для Python 3.13 додай PPA»

Порада з форуму: додати PPA і поставити `python3.13` через apt. Чому це погана ідея саме на Mint і саме перед
наступною великою версією Mint? Як отримати Python 3.13 правильно? Якщо PPA уже додано - як прибрати його чисто?

<details markdown="1"><summary>Відповідь</summary>

- `sudo apt install python3.13` → `E: Unable to locate package python3.13`: у сховищах Ubuntu 24.04 його нема,
  тому і радять PPA - **стороннє** сховище однієї людини чи команди.
- Документація Ubuntu: сторонні сховища - найчастіша причина зламаного оновлення версії системи. Ключ PPA доводить
  лише «звідки пакет», а не «що він безпечний». Наступна Mint (на базі Ubuntu 26.04) ще попереду - зайвий PPA може
  зламати саме цей перехід.
- Правильно: Python 3.13 **поруч** із системним, без apt: `pipx install uv`, `~/.local/bin/uv python install 3.13`.
  Системний `python3` (3.12) не чіпати ніколи.
- Прибрати PPA: `sudo add-apt-repository --remove ppa:власник/назва`, а пакети з нього повернути до офіційних -
  `ppa-purge`. Мишкою: «Джерела програмного забезпечення» → «Пакунки PPA».

Джерело: урок 02, «Коротко», «Типові помилки» і «Самоперевірка» 3; урок 16, «Коротко» (PPA) і «Типові помилки».

</details>

#### Б11. apt, Flatpak чи «Керування програмами»?

Програма є і в apt, і на Flathub. Що вибереш і чому? Чому VS Code у «Керуванні програмами» схований, і чим погана
Flatpak-версія VS Code саме для лаб у `~/univer/.venv`?

<details markdown="1"><summary>Відповідь</summary>

Правило практиків: «Deb if available, flatpak if not» - системний пакет, якщо є (менше місця, оновлюється разом із
системою), Flatpak - коли в apt нема або версія дуже стара.

VS Code там - **неперевірений** Flatpak (`com.visualstudio.code`, «Not verified»: виклав не Microsoft), а Mint ховає
неперевірені, бо це ризик безпеки. До того ж Flatpak працює в пісочниці: вбудований термінал не бачить системних
програм і venv без `flatpak-spawn --host`. Для лаб - .deb з code.visualstudio.com (додає своє сховище, оновлення
через Диспетчер оновлень) або VSCodium з його apt-сховища.

Джерело: урок 16, «Коротко» (таблиця шляхів, «Керування програмами», Flatpak); урок 27, «Коротко» (чому не з
Менеджера програм) і «Самоперевірка» 1.

</details>

#### Б12. Сценарій: NVIDIA і синій екран

Ти поставив рекомендований драйвер NVIDIA в «Керуванні драйверами», перезавантажився, побачив синій екран з
англійським меню і, не читаючи, вибрав продовжити завантаження. Тепер низька роздільність або чорний екран. Secure
Boot увімкнено. Що сталось і що робиш? Чого не робиш?

<details markdown="1"><summary>Відповідь</summary>

Синій екран - MOK Manager: треба було вибрати «Enroll MOK» і ввести пароль, придуманий під час встановлення
драйвера. З Secure Boot ядро вантажить лише підписані модулі, а модуль NVIDIA, зібраний DKMS, підписаний твоїм
ключем MOK, якого UEFI ще не знає. Без нього драйвер не завантажився.

Що робити: Ctrl+Alt+F2 (TTY) → `mokutil --sb-state` (переконатись, що Secure Boot увімкнено) →
`sudo update-secureboot-policy --enroll-key` → `sudo reboot` → на синьому екрані «Enroll MOK», підтвердити, той
самий пароль. Перевірка: `nvidia-smi` показує `Driver Version`, `inxi -G` - `driver: nvidia`, `dkms status`.

Не робити: не вимикати Secure Boot «щоб не морочитись» (з BitLocker Windows почне питати ключ відновлення); не
ставити `.run` з nvidia.com (ламається з кожним ядром).

Джерело: урок 17, «Коротко» (Secure Boot, MOK), «Типові помилки» і «Самоперевірка» 3-4; урок 26, «Подвійне
завантаження».

</details>

#### Б13. Сценарій: після встановлення Mint не видно Wi-Fi

Опиши діагностику по сходинках: які команди, що в їхньому виводі шукаєш і що робиш на кожен результат. Інтернету
немає зовсім (кабелю теж).

<details markdown="1"><summary>Відповідь</summary>

1. `rfkill list` - `Soft blocked: yes` → вимкнено програмно (режим «у літаку»): `rfkill unblock wifi` або аплет.
   `Hard blocked: yes` → фізична кнопка чи Fn-клавіша з антеною.
2. `nmcli device status` - чи є пристрій `wifi` взагалі. Нема - драйвера нема.
3. `lspci -k` (або `lsusb` для USB-адаптера) - знайти мережевий контролер і рядок `Kernel driver in use`. Нема
   рядка - модуль не завантажився.
4. Intel / AMD - драйвер уже в ядрі, прошивка в `linux-firmware`; найчастіше винен rfkill. Broadcom - «Керування
   драйверами»: без інтернету воно попросить live USB → «Змонтувати інсталяційний носій» (флешка стане джерелом
   пакетів).
5. Не вийшло - на форум з виводом `inxi -Fxz` (`z` ховає MAC-адреси).

Джерело: урок 17, «Коротко» (таблиця команд, Broadcom, без інтернету) і «Самоперевірка» 5; урок 21, «Коротко»
(сходинки діагностики).

</details>

#### Б14. Що виведе? (`sort -n` чи `sort -h`)

```bash
mkdir -p ~/ispyt/b14/foto ~/ispyt/b14/kurs ~/ispyt/b14/labs && cd ~/ispyt/b14
head -c 900K /dev/zero > foto/a.bin; head -c 5M /dev/zero > kurs/b.bin; head -c 40K /dev/zero > labs/c.py
du -sh */ | sort -n
echo "-"
du -sh */ | sort -h
```

<details markdown="1"><summary>Відповідь</summary>

```text
5.1M	kurs/
44K	labs/
904K	foto/
-
44K	labs/
904K	foto/
5.1M	kurs/
```

`sort -n` дивиться лише на число (5.1 < 44 < 904) і не знає, що M більше за K, - найбільша тека опинилась
**першою**. `sort -h` розуміє K, M, G. Звідси правило: `du -h ... | sort -h`, найбільше - внизу. Розміри трохи
більші за файли (904K, 5.1M), бо `du` рахує зайняті блоки диска разом із самою текою.

Джерело: урок 18, «Коротко» (`du -h --max-depth=1 | sort -h`) і «Самоперевірка» 2; урок 22, «Фільтри» (`sort -n`).

</details>

#### Б15. Сценарій: диск заповнено на 100 %. Хто зʼїв місце?

Графіка ще працює. Опиши, як **знайти**, що саме заповнило диск, і в якому порядку безпечно звільняти місце. Які
«підозрювані» перевіриш першими і чому? Чого не робиш?

<details markdown="1"><summary>Відповідь</summary>

Знайти:

1. `df -h /` - скільки вільно (стовпець `Avail`).
2. `sudo du -xh --max-depth=1 / 2>/dev/null | sort -h | tail` - найбільші теки системного розділу; `-x` - не
   заходити на флешки й інші диски, `2>/dev/null` - сховати `Permission denied`. Далі спускатись у найбільшу
   (або `sudo ncdu -x /` і стрілками).
3. Типові підозрювані:
   - журнали: `sudo journalctl --disk-usage` (бували випадки на сотні ГБ);
   - знімки Timeshift (тека `timeshift` у корені диска), особливо якщо в них потрапили `/home` чи `/var/lib/flatpak`;
   - `/var/lib/flatpak` - старі бібліотеки, `/var/cache/apt/archives` - кеш .deb, старі ядра;
   - `~/.cache` і смітник (`~/.local/share/Trash`).

Звільняти від найбезпечнішого: `gio trash --empty`, `sudo apt clean`, `sudo apt autoremove --purge`,
`sudo journalctl --vacuum-time=2weeks`, `flatpak uninstall --unused`, старі ядра в Диспетчері оновлень, зайві знімки
в Timeshift.

Не робити: «чистильники» на кшталт BleachBit, видалення програм Mint «для місця», ручне видалення з `/var` чи
`/usr`. Якщо графіка вже не пускає - те саме з TTY (Ctrl+Alt+F2).

Джерело: урок 18, «Коротко» (безпечне прибирання), «Типові помилки» і «Самоперевірка» 3, 5; урок 01, «Типові
помилки»; урок 20, «Коротко» (`journalctl --disk-usage`).

</details>

#### Б16. Знайди помилку (fstab)

У `/etc/fstab` ти додав зовнішній диск для копій:

```text
UUID=3f6c2a1e-8b1d-4c55-9a0e-2f7d4b6c9e10  /media/evgen/arhiv  ext4  defaults  0  2
```

Тиждень усе добре, потім диск лишився вдома, а ноутбук у гуртожитку стартує з `You are in emergency mode`. Чому, як
виправити рядок і як дістатись до файлу з цього режиму?

<details markdown="1"><summary>Відповідь</summary>

Без `nofail` диск із fstab вважається обовʼязковим: нема диска - систему не довантажено. Рядок має бути з
`defaults,nofail` (тоді без диска старт іде далі).

З аварійного режиму: Enter (або пароль) → `journalctl -xb` - знайти червоний рядок про `mount` → `nano /etc/fstab`
- дописати `nofail` або закоментувати рядок `#` → `findmnt --verify` → `systemctl reboot`.

Джерело: урок 18, «Типові помилки» і «Самоперевірка» 4; урок 26, «Сценарії порятунку» (Ґ).

</details>

#### Б17. Сценарій: ноутбук після оновлення показує чорний екран. Твої 3 кроки по порядку

Що робиш спершу, що потім, і як зрозуміти, яка з причин (ядро, відеодрайвер, щось інше)? Що робити, якщо жоден
крок не допоміг?

<details markdown="1"><summary>Відповідь</summary>

**Крок 1. Чи живе система під графікою?** Ctrl+Alt+F2. Є `login:` - ядро працює, зламалась графіка або місце: увійти,
`df -h /` (диск 100 %?), `sudo journalctl -b -p err` (що впало). Щойно ставив драйвер чи оновлення - відкотити:
`sudo timeshift --list`, `sudo timeshift --restore`.

**Крок 2. TTY нема, зависає одразу після логотипа - GRUB.** Перезавантаження, меню GRUB (Esc на UEFI, Shift на
BIOS) → «Advanced options for Linux Mint» → **попереднє** ядро (не recovery).
- Стартувало - винне нове ядро: `uname -r` (старе), Диспетчер оновлень → Вигляд → Ядра Linux → видалити нове.
  Помилки невдалого старту - `sudo journalctl -b -1 -p err`.
- І старе не стартує, чорний екран після логотипа - відео: на рядку Mint `e`, `quiet splash` → `nomodeset`, F10;
  потім «Керування драйверами» і перезавантаження без `nomodeset` (діє лише на один запуск).

**Крок 3. Нічого не допомогло** - live USB → Timeshift (є на образі) → вибрати диск і знімок → Restore. Або
скопіювати `~/univer` на іншу флешку через Nemo і перевстановити - лаби вціліють.

Чого не робити: перевстановлювати Mint при першій проблемі.

Джерело: урок 26, «Драбина порятунку», «Сценарії порятунку» (А, Б, В, Є), «Передбач» 3, «Типові помилки»; урок 02,
«Типові помилки» (останній пункт); урок 20, «Коротко» (`journalctl -b -1`).

</details>

#### Б18. Поясни: як скинути забутий пароль і що це каже про безпеку

Перелічи кроки. Чому recovery mode пускає без пароля? Від чого захищає шифрування диска і коли його вмикають? Що
означає `passwd: Authentication token manipulation error` у цьому режимі?

<details markdown="1"><summary>Відповідь</summary>

GRUB → «Advanced options» → `(recovery mode)` → `root` → Enter → `mount -o remount,rw /` → `passwd evgen` →
`reboot`.

Пароль root у Mint заблоковано, і `sulogin` у такому разі пускає по Enter: хто фізично має ноутбук, той може стати
root. Від цього захищає лише шифрування диска (LUKS): без пароля диска recovery mode нічого не прочитає. Вмикають
його **тільки під час встановлення** Mint; потім - лише перевстановленням.

`Authentication token manipulation error` - забув `mount -o remount,rw /`, диск ще лише для читання.

Джерело: урок 26, «Сценарії порятунку» (Г) і «Типові помилки»; урок 25, «Решта звичок» (шифрування диска).

</details>

#### Б19. Поясни: «брандмауер працює, дивись - active»

Одногрупник показує `systemctl status ufw` → `Active: active (exited)` і каже: «брандмауер увімкнено». Чи правий він?
Що реально змінює `sudo ufw enable` для тебе і для інших компʼютерів у мережі гуртожитку? Як перевірити, чи
взагалі щось на ноутбуці чекає вхідних підключень?

<details markdown="1"><summary>Відповідь</summary>

Не обовʼязково. `active (exited)` - служба при старті один раз виконала свою дію і успішно завершилась; стан самого
брандмауера показує лише `sudo ufw status` (на свіжій Mint - `Status: inactive`).

Після `sudo ufw enable`: вхідні підключення заборонені, вихідні дозволені. Ти нічого не помітиш (інтернет,
оновлення, GitHub працюють), а інші компʼютери більше не зможуть підключитись до ноутбука, поки ти явно щось не
дозволиш (`sudo ufw allow ...`).

Хто слухає порти: `sudo ss -tulpn`. Рядок `0.0.0.0:22` означав би ssh-сервер для всієї мережі - на Mint його нема,
`openssh-server` не встановлено.

Джерело: урок 25, «Коротко» (брандмауер) і «Самоперевірка» 1; урок 20, «Коротко» (стани) і «Самоперевірка» 2;
урок 21, «Коротко» і «Самоперевірка» 4.

</details>

#### Б20. Знайди помилку: «порада» з чату

У чаті групи скинули «рецепт, щоб усе запрацювало», три рядки. Перший завантажує скрипт з невідомого сайту
curl-ом і одразу передає його в `sudo bash`. Другий - `sudo pip install numpy` з ключем `--break-system-packages`.
Третій рекурсивно ставить права 777 на `~/univer`. Що не так з кожним, і що робиш замість цього?

<details markdown="1"><summary>Відповідь</summary>

1. Скрипт у `sudo bash` наосліп: ти навіть не бачиш, що виконується, а виконується від root - що завгодно. Замість:
   завантажити у файл, прочитати (`less`), перевірити `shellcheck`, розібрати незнайомі команди на explainshell.com,
   і лише тоді вирішувати.
2. `sudo pip` + `--break-system-packages` - ламає системний Python, на якому працює сама Mint. Замість: venv
   (`~/univer/.venv`), для програм - pipx.
3. 777 - будь-хто і будь-яка програма може змінити файл. Скрипту досить `chmod +x`, файлу - 644, теці - 755.

Головне правило: пароль sudo - це твоя згода на все, що написано далі. Нічого не вставляєш, поки не розумієш кожне
слово.

Джерело: урок 25, «Коротко» (що не запускати з sudo), «Типові помилки» і «Самоперевірка» 2, 5; урок 15, «Типові
помилки» (777); урок 23, «Типові помилки» (чужий скрипт).

</details>

---

### Блок В. Термінал і адміністрування (уроки 19-24, 27)

#### В1. Що виведе? (код виходу після сигналу)

```bash
cd ~/ispyt
printf 'sleep 30 &\nkill $!\nwait $!; echo "код $?"\nsleep 30 &\nkill -9 $!\nwait $!; echo "код $?"\n' > kody.sh
bash kody.sh 2> /dev/null
```

<details markdown="1"><summary>Відповідь</summary>

```text
код 143
код 137
```

Процес, убитий сигналом, має код 128 + номер сигналу: SIGTERM (15, звичайний `kill`) → 143, SIGKILL (9, `kill -9`)
→ 137, Ctrl+C (SIGINT, 2) → 130. `$!` - PID останньої фонової команди. (Якщо набирати ці рядки в терміналі, bash
ще повідомить про задачу, наприклад `[1]+  Terminated  sleep 30`.) За кодом у журналі чи в cron видно, «сам упав»
чи «його вбили».

Джерело: урок 19, «Коротко» (сигнали, код 128 + номер) і «Самоперевірка» 3.

</details>

#### В2. Поясни: Ctrl+Z і `killall python3`

Лаба з нескінченним циклом. Ти натиснув Ctrl+Z, запрошення повернулось. Що з програмою зараз? Як її правильно
завершити? Одногрупник радить «просто `killall python3`» - чим це небезпечно в Mint і як вбивати точково?

<details markdown="1"><summary>Відповідь</summary>

Ctrl+Z лише **призупиняє** (SIGTSTP): програма жива, `jobs` покаже `Stopped`. Завершити: `fg` і Ctrl+C, або
`kill %1`.

`killall python3` (чи `pkill -f python`) вбиває **всі** Python-процеси, разом із програмами Mint на Python
(Диспетчер оновлень теж на Python). Точково: `pgrep -af python` (PID і повна команда) → `kill PID` (SIGTERM, дає
програмі закрити файли) → лише якщо за кілька секунд не завершилась - `kill -9 PID`.

Джерело: урок 19, «Коротко», «Типові помилки» і «Самоперевірка» 1-2; урок 02, «Самоперевірка» 2 (Mint на системному
Python).

</details>

#### В3. Поясни: одна команда, три результати

`zdaty 3` у терміналі працює. `sudo zdaty 3` каже, що такої команди нема. Той самий рядок у crontab пише в лог
`/bin/sh: 1: zdaty: not found`. Поясни всі три випадки і як зробити правильно.

<details markdown="1"><summary>Відповідь</summary>

Усе - PATH, список тек, де шукаються команди:

- у твоєму терміналі в PATH є `~/.local/bin` (її додає `~/.profile` при вході, якщо тека тоді вже була) - `zdaty`
  знаходиться;
- `sudo` використовує свій короткий безпечний PATH без твоїх тек і аліасів. Та й запускати свої скрипти від root не
  треба;
- cron запускає `/bin/sh` з коротким PATH
  (`/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:...`), без `~/.local/bin`, venv, аліасів і функцій
  з `~/.bashrc`.

Правильно в cron - повні шляхи: `/home/evgen/.local/bin/zdaty`, `/home/evgen/univer/.venv/bin/python`. Перевірити,
що саме знаходить твій bash: `type zdaty`.

Джерело: урок 22, «PATH» і «Типові помилки» (останні два пункти); урок 23, «Три правила cron» і «Типові помилки».

</details>

#### В4. Поясни: cron чи таймер systemd для щоденної копії на ноутбуці?

Копія `~/univer` має робитися раз на день. Ноутбук часто закритий о тій годині, коли стоїть завдання. Що вибереш і
чому? Що спільного в пастках обох способів?

<details markdown="1"><summary>Відповідь</summary>

**Таймер systemd** (`systemctl --user`) з `Persistent=true`: якщо час пропущено (ноутбук спав чи був вимкнений),
запуск відбудеться при наступній нагоді. cron пропущене **не доганяє**: о 13:00 ноутбук закритий - копії сьогодні
не буде. Ще плюс таймера: вивід іде в журнал (`journalctl --user -u назва`), а статус видно в
`systemctl --user list-timers`.

Спільні пастки: команда запускається не з твого термінала - нема твого PATH, venv, аліасів; потрібні **повні
шляхи** (`ExecStart=/usr/bin/rsync ...`, у cron - `/usr/bin/...` чи `/home/evgen/...`). У cron ще `%` треба писати
`\%` і самому дописувати `>> лог 2>&1`; у systemd - після правки файлу `systemctl --user daemon-reload`.

Джерело: урок 23, «Коротко» (три правила cron, пропущений запуск); урок 20, «Коротко», «Руками» крок 7, «Типові
помилки».

</details>

#### В5. Сценарій: ноутбук уночі сам перезавантажився

Вранці ти бачиш, що ноутбук перезавантажувався. Якими командами дізнаєшся, коли це було і які помилки були перед
цим? Які рівні важливості покаже `-p err`?

<details markdown="1"><summary>Відповідь</summary>

- `last reboot | head -3` або `uptime -s` - коли вмикався;
- `sudo journalctl --list-boots` - список завантажень (`0` - поточне, `-1` - попереднє);
- `sudo journalctl -b -1 -p err` - лише помилки попереднього завантаження;
- `sudo journalctl -b -1 -e` - одразу кінець попереднього завантаження: що було останнім перед падінням;
- ядро окремо: `sudo journalctl -k -b -1` (і `sudo dmesg` для поточного - без sudo ядро Mint свій журнал не
  показує).

`-p err` = рівні 0-3: `emerg`, `alert`, `crit`, `err`.

Джерело: урок 20, «Коротко» (журнал, рівні), «Руками» кроки 5-6, «Самоперевірка» 3.

</details>

#### В6. Знайди помилки (служба systemd)

Ти зробив `~/.config/systemd/user/kopiya.service` і запустив `systemctl --user start kopiya.service`:

```text
[Unit]
Description=Копія лаб

[Service]
Type=oneshot
ExecStart=/usr/bin/pyton3 %h/univer/kopiya.py
```

```text
Job for kopiya.service failed because the control process exited with error code.
```

`systemctl --user status kopiya.service` показує `status=203/EXEC`. Ти виправив файл і знову `start` - а status пише
`... changed on disk. Run 'systemctl --user daemon-reload' to reload units.` Що не так і в якому порядку
лагодити?

<details markdown="1"><summary>Відповідь</summary>

1. `203/EXEC` - systemd не зміг запустити програму: одруківка `pyton3`. Шлях - повний і справжній:
   `/usr/bin/python3` (перевір `which python3`). `%h` - правильно, systemd сам підставить домашню теку.
2. Після правки файлу systemd досі працює зі старою версією - спершу `systemctl --user daemon-reload`, потім
   `systemctl --user start kopiya.service`, `systemctl --user status kopiya.service`.

Загальний порядок діагностики: `status` (код), `journalctl --user -xeu kopiya.service` (подробиці).

Джерело: урок 20, «Типові помилки» (daemon-reload, `ExecStart`) і «Самоперевірка» 5.

</details>

#### В7. Сценарій: Wi-Fi підключено, а сайти не відкриваються

```text
$ ping -c 3 1.1.1.1
3 packets transmitted, 3 received, 0% packet loss
$ ping -c 3 linuxmint.com
ping: linuxmint.com: Temporary failure in name resolution
```

Що зламалось, що робиш? Чим відрізняються `Name or service not known` і `Network is unreachable`?

<details markdown="1"><summary>Відповідь</summary>

Пакети в інтернет ходять (за IP), а імена не перетворюються на адреси - **DNS**. `resolvectl status` - які
DNS-сервери; перепідключити Wi-Fi; якщо повторюється - у «Мережних зʼєднаннях» задати DNS вручну (напр.
`1.1.1.1`).

- `Name or service not known` - DNS працює, але такого імені нема (одруківка в адресі).
- `Network is unreachable` - нема маршруту назовні: Wi-Fi не підключено (сходинки `nmcli device status`, `ip -br a`,
  `ip r`).

Джерело: урок 21, «Коротко» (сходинки діагностики), «Типові помилки» і «Самоперевірка» 1.

</details>

#### В8. Що виведе? (права ключа ssh)

```bash
mkdir -p ~/ispyt/v8 && cd ~/ispyt/v8
ssh-keygen -q -t ed25519 -N "" -C "proba" -f kluch
stat -c '%a %n' kluch kluch.pub
```

Який з файлів можна дати GitHub, а який нікому? Що скаже ssh, якщо в приватного ключа права 644?

<details markdown="1"><summary>Відповідь</summary>

```text
600 kluch
644 kluch.pub
```

`kluch` (у житті `~/.ssh/id_ed25519`) - **приватний**, лише ти, права 600; `kluch.pub` - публічний, його дають
GitHub і серверам. Тека `~/.ssh` - 700. З правами 644 на приватному ключі ssh відмовиться його брати:
`WARNING: UNPROTECTED PRIVATE KEY FILE!` - лікується `chmod 600`. (`-N ""` тут - ключ без пароля лише для вправи.)

Джерело: урок 21, «Коротко» (файли ключа), «Типові помилки» і «Самоперевірка» 2; урок 15, «Коротко» (600, 700).

</details>

#### В9. Що виведе? (лапки)

```bash
name="ЛР 1"
echo "$name" '$name'
printf '[%s]\n' $name
printf '[%s]\n' "$name"
```

<details markdown="1"><summary>Відповідь</summary>

```text
ЛР 1 $name
[ЛР]
[1]
[ЛР 1]
```

У подвійних лапках змінна підставляється, в одинарних - друкується буквально. Без лапок значення з пробілом
розпадається на **два** аргументи - звідси правило «змінну завжди в `"$x"`» (інакше `cp $f ...` з назвою
«Лаба 1» шукатиме два файли).

Джерело: урок 22, «Коротко» (змінні) і «Самоперевірка» 1.

</details>

#### В10. Що виведе? (stdout, stderr)

```bash
mkdir -p ~/ispyt/v10 && cd ~/ispyt/v10
printf 'print("ok")\nprint(1 / 0)\n' > p.py
python3 p.py > out.txt 2> /dev/null
cat out.txt
python3 p.py > all.txt 2>&1
tail -n 1 all.txt
```

А що зробить `python3 p.py > p.py`?

<details markdown="1"><summary>Відповідь</summary>

```text
ok
ZeroDivisionError: division by zero
```

`>` перенаправляє лише stdout (1), traceback іде в stderr (2) - його в `out.txt` нема. `> all.txt 2>&1` - обидва
потоки в один файл (коротко `&> all.txt`).

`python3 p.py > p.py` **стирає код**: bash спершу обнуляє файл для `>`, а вже потім запускає Python - той бачить
порожній файл. Вивід - завжди в інший файл.

Джерело: урок 22, «Потоки і перенаправлення», «Типові помилки» і «Самоперевірка» 5.

</details>

#### В11. Що виведе? (`uniq` без `sort`)

```bash
printf 'b\na\nb\nb\na\n' | uniq -c
printf 'b\na\nb\nb\na\n' | sort | uniq -c | sort -rn
```

<details markdown="1"><summary>Відповідь</summary>

```text
      1 b
      1 a
      2 b
      1 a
      3 b
      2 a
```

`uniq -c` склеює лише **сусідні** однакові рядки - без `sort` числа «дивні». `sort | uniq -c | sort -rn` - класичний
«частотний словник»: найчастіше - згори (наприклад, які помилки найчастіше в журналі чи які коди flake8 у лабі).

Джерело: урок 22, «Фільтри» і «Типові помилки».

</details>

#### В12. Що виведе? (`find` без лапок)

```bash
mkdir -p ~/ispyt/v12/sub && cd ~/ispyt/v12 && touch a.py b.py sub/c.py
find . -name *.py; echo "код $?"
find . -name "*.py" | sort
```

<details markdown="1"><summary>Відповідь</summary>

```text
find: paths must precede expression: `b.py'
find: possible unquoted pattern after predicate `-name'?
код 1
./a.py
./b.py
./sub/c.py
```

Без лапок bash **сам** розгортає `*.py` у назви файлів поточної теки: find отримує `-name a.py b.py` і не розуміє
зайвого `b.py`. А якби в теці був лише один `.py` - find мовчки шукав би тільки його (ще гірше: помилки нема, а
результат неповний). Шаблон - завжди в лапках.

Джерело: урок 22, «Фільтри» (`find`) і «Типові помилки».

</details>

#### В13. Знайди помилки (рядок crontab)

```text
0 18 * * 5 zdaty 3 > ~/zvit-$(date +%F).txt
```

Мета: щопʼятниці о 18:00 зібрати ЛР3 і зберегти звіт. Знайди всі проблеми і запиши правильний рядок.

<details markdown="1"><summary>Відповідь</summary>

1. `zdaty` у cron не знайдеться: PATH короткий, без `~/.local/bin` (буде `/bin/sh: 1: zdaty: not found`).
2. `%` у рядку cron означає новий рядок - `date +%F` ламає команду, вона тихо не виконується. Треба `\%`.
3. Нема `2>&1` - помилки підуть «поштою», якої на ноутбуці нема, і загубляться.
4. `zdaty` при зауваженнях питає `(y/n)` - у cron відповісти нікому, питання закінчиться помилкою. Для cron -
   команди без питань.

Виправлено:

```text
0 18 * * 5 /home/evgen/.local/bin/zdaty 3 >> /home/evgen/cron.log 2>&1
```

(Якщо потрібна дата в назві - `$(date +\%F)`.)

Джерело: урок 23, «Три правила cron», «Типові помилки» і «Самоперевірка» 4-5.

</details>

#### В14. Що виведе? (`set -e` і пайпи)

```bash
bash -c 'set -e; false | true; echo "далі 1"'; echo "код $?"
bash -c 'set -eo pipefail; false | true; echo "далі 2"'; echo "код $?"
```

<details markdown="1"><summary>Відповідь</summary>

```text
далі 1
код 0
код 1
```

Код пайпу - це код **останньої** команди (`true` → 0), тож `set -e` не помічає, що `false` упав. З `pipefail` пайп
вважається невдалим, якщо впала будь-яка його частина, і `set -e` зупиняє скрипт. Тому в скриптах -
`set -euo pipefail`: інакше, наприклад, `python3 -m pytest ... | tail -n 1` «успішний» навіть при провалених тестах.

Джерело: урок 23, «Коротко» (`set -euo pipefail`) і «Самоперевірка» 2; урок 22, «Код виходу».

</details>

#### В15. Що виведе? (`"$@"` і `$@`)

```bash
cd ~/ispyt
printf '#!/bin/bash\nfor a in "$@"; do echo "[$a]"; done\nfor a in $@; do echo "<$a>"; done\n' > args.sh
bash args.sh "ЛР 1" lr2
```

<details markdown="1"><summary>Відповідь</summary>

```text
[ЛР 1]
[lr2]
<ЛР>
<1>
<lr2>
```

`"$@"` у лапках - кожен аргумент окремо, як його передали (2 аргументи). `$@` без лапок - знову розбиття за
пробілами (3 «аргументи»). У скрипті, що приймає назви файлів чи тек, - тільки `"$@"`.

Джерело: урок 23, «Коротко» (таблиця `$0`, `$#`, `"$@"`) і «Передбач» 1; урок 22, «Коротко» (лапки).

</details>

#### В16. Що виведе? (що потрапляє в zip)

```bash
mkdir -p ~/ispyt/v16/labs/lr1 && cd ~/ispyt/v16 && printf 'x = 1\n' > labs/lr1/a.py
zip -qr z1.zip ~/ispyt/v16/labs/lr1
python3 -m zipfile -c z2.zip ~/ispyt/v16/labs/lr1
unzip -Z1 z1.zip; echo "-"; unzip -Z1 z2.zip
```

Як отримати архів, усередині якого рівно `Прізвище_Імʼя_Група_ЛР1/a.py`?

<details markdown="1"><summary>Відповідь</summary>

```text
home/evgen/ispyt/v16/labs/lr1/
home/evgen/ispyt/v16/labs/lr1/a.py
-
lr1/
lr1/a.py
```

`zip -r` кладе шлях так, як його передали (увесь `home/evgen/...`, разом із `__pycache__`, якщо є), а
`python3 -m zipfile -c` лишає лише **останню** теку (`lr1/`), і потрібної назви в архіві нема. Правильно, як у
`zdaty`: зробити тимчасову теку з потрібною назвою, скопіювати туди лише `.py` і пакувати **з батьківської** теки:
`(cd "$tmp" && zip -qr "$ZDACHA/$nazva.zip" "$nazva")`.

Джерело: урок 23, «Руками» крок 2, «Типові помилки» (zip з повним шляхом) і «Самоперевірка» 3; урок 14, «Коротко»
(архіви).

</details>

#### В17. Поясни: `git restore` і пароль у коміті

а) Ти набрав `git restore lab3.py` і втратив дві години незакоміченої роботи. Чому git не питав і чому нема «назад»?
Що робити наступного разу? б) Ти закомітив і запушив файл з токеном, потім зробив `git rm --cached token.txt` і
новий коміт. Проблему розвʼязано?

<details markdown="1"><summary>Відповідь</summary>

а) `git restore файл` викидає **незакомічені** зміни: їх ніде не було збережено (ні в коміті, ні в staging), тому
повертати нема звідки, і git не питає. Наступного разу: спершу `git diff` (що саме зникне) або коміт; часті малі
коміти - це і є «збереження гри» для коду.

б) Ні. `git rm --cached` прибирає файл лише з **наступних** комітів, у старих (і на GitHub) він лишається. Токен
вважати витеклим: **відкликати / змінити**. Надалі - секрети поза репозиторієм, їхні файли в `.gitignore`.

Джерело: урок 24, «Коротко» (`git restore`), «Типові помилки» і «Самоперевірка» 2.

</details>

#### В18. Що виведе? (`.gitignore`)

```bash
mkdir -p ~/ispyt/v18 && cd ~/ispyt/v18 && git init -q -b main
printf '.venv/\n__pycache__/\n' > .gitignore
mkdir -p .venv __pycache__ && touch .venv/x a.py __pycache__/a.pyc
git status --short
```

<details markdown="1"><summary>Відповідь</summary>

```text
?? .gitignore
?? a.py
```

`??` - файл ще не відстежується. `.venv/` і `__pycache__/` git не бачить зовсім - їх можна перестворити, а у
репозиторії вони були б тисячами зайвих файлів. Сам `.gitignore` комітять. Якщо `.venv` уже закомічено -
`git rm -r --cached .venv` і коміт.

Джерело: урок 24, «Коротко» (`.gitignore`), «Типові помилки» і «Самоперевірка» 3.

</details>

#### В19. Сценарій: `git push` не проходить

Три різні повідомлення в різні дні. Що означає кожне і що робиш?

```text
1) git@github.com: Permission denied (publickey).
2) ! [rejected]        main -> main (fetch first)
3) remote: Support for password authentication was removed
```

<details markdown="1"><summary>Відповідь</summary>

1. GitHub не знає твій ключ або ssh бере інший. По черзі: `ls -l ~/.ssh` (ключ є, права 600), `ssh -T git@github.com`
   (має привітати), `.pub` доданий на GitHub (Settings → SSH and GPG keys), `ssh -v git@github.com` (рядки
   `Offering public key`).
2. На GitHub є коміти, яких нема в тебе (пушив з іншого компʼютера): `git pull`, потім `git push`.
3. Адреса `origin` - `https://...`, а пароль GitHub не приймає: `git remote -v`, потім
   `git remote set-url origin git@github.com:Evge14n/labs.git`.

Джерело: урок 24, «Коротко», «Типові помилки» і «Самоперевірка» 4; урок 21, «Типові помилки»
(`Permission denied (publickey)`).

</details>

#### В20. Поясни: «у VS Code усе зелене»

Ти поставив VS Code, і редактор не підсвічує помилок. Чому перед здачею все одно треба перевірити лабу в терміналі
(якими командами)? Навіщо знати pdb, якщо у VS Code є налагоджувач debugpy? Яке налаштування VS Code обовʼязково
вимкнути для лаб і чому?

<details markdown="1"><summary>Відповідь</summary>

- «Зелене» в редакторі - це підсвітка, не doctest. Викладач перевіряє doctest, flake8 до 78, mypy - саме ними:
  `python3 -m pytest --doctest-modules`, `python3 -m flake8 --max-line-length=78`, mypy (або `perevir файл.py`), з
  venv `~/univer/.venv`. До того ж VS Code міг узяти **не той** інтерпретатор (`ModuleNotFoundError` у ньому, а в
  терміналі працює).
- debugpy - той самий принцип, що pdb (F10 = `n`, F11 = `s`, F5 = `c`), але pdb працює в будь-якому терміналі: по
  ssh, у TTY, на парі чи іспиті без VS Code.
- ШІ-функції (`chat.disableAIFeatures`): код, який дописав ШІ, ти не поясниш викладачу, а пояснення кожного рядка -
  частина здачі.

Джерело: урок 27, «Коротко», «Типові помилки» і «Самоперевірка» 2-5; урок 04, «Перевір перед здачею»; урок 06,
«Коротко».

</details>

---

### Як оцінити себе

| Бали в блоці | Що робити |
|---|---|
| **≥ 18 з 20** | блок зараховано - далі |
| менше 18 | перечитай уроки з тих питань, де помилився (рядок «Джерело»), і **перескладай блок через 2 дні** |

Перескладай без підглядання в цей файл: за 2 дні памʼять «відпускає» дослівні відповіді, і лишається те, що ти
справді зрозумів. Питання «що виведе» запускай знову: якщо вивід у тебе інший - це теж знахідка (інша версія Mint
чи Python), запиши її.

### Підсумок перевірки курсу (18.11.2026, ULINUX2)

Незалежний агент-«екзаменований» склав усі 60 питань, читаючи лише уроки (відповіді в цьому файлі він не бачив; скрипт
вирізав блоки «Відповідь»), і запускав кожне «що виведе» в тестовій Linux Mint 22.3.

| Блок | Результат | Примітка |
|---|---|---|
| А. Лаби, оновлення, налагодження | 20 / 20 | А20 - відповідь зібрана з уроків 01, 02, 25, 26 (окремого сценарію нема) |
| Б. Mint як система | 20 / 20 | Б6 - шлях через recovery mode взято з уроку 26 |
| В. Термінал і адміністрування | 20 / 20 | В17 - про git stash уроки не кажуть (і не треба) |

Разом 60 / 60 = 100 %, мета стандарту (не менше 90 %) виконана. Це перевірка **курсу** (чи вистачає уроків для
відповіді), а не твоя: твій результат рахуй за таблицею вище.
