# Урок 05. Налагодження 1 - traceback, print, assert, breakpoint

[← Усі уроки](#/u/mint/uroky)

**Навіщо:** програма майже ніколи не працює з першого разу. Цей урок вчить чотирьох простих способів знайти, де саме
вона помиляється: прочитати traceback, надрукувати змінні, поставити assert і зупинити програму в `breakpoint()`.
Усе в терміналі, без VS Code.

## Коротко

**Налагодження** (debugging) - пошук місця, де програма робить не те, що ти думаєш. Помилка в програмі - **баг**.

| Що бачиш | З чого почати |
|---|---|
| Програма впала, у кінці `Traceback ...` і назва помилки | прочитай traceback **знизу вгору** |
| Програма не падає, але число не те | `print(f"{x=}")` або `breakpoint()` |
| Хочеш, щоб програма сама «кричала», коли дані погані | `assert умова, "повідомлення"` |
| Програма впала, хочеш покопатись у змінних після падіння | `python3 -i файл.py` |

**Traceback** (слід виклику) - звіт Python про падіння. Читати **знизу вгору**:

```text
Traceback (most recent call last):          ← «останній виклик - внизу»
  File ".../period.py", line 16, in <module>     ← звідки все почалось (рівень файлу)
    main()
  File ".../period.py", line 13, in main         ← потім функція main, рядок 13
    print(...)
  File ".../period.py", line 7, in period        ← тут упало: функція period, рядок 7
    return 2 * math.pi * math.sqrt(length / G)
                         ^^^^^^^^^^^^^^^^^^^^^   ← ^^^ показують, ЯКА саме частина рядка впала
ValueError: math domain error                    ← 1) ЧИТАЙ ПЕРШИМ: тип помилки і пояснення
```

1. Останній рядок - **що** сталося (тип помилки + пояснення).
2. Рядок над ним - **де** (файл, номер рядка, функція) і сам рядок коду з `^^^`.
3. Вище - **як туди дійшли**: хто кого викликав. Помилка не завжди в найнижчому рядку - часто погане значення
   прийшло згори (наприклад, від'ємна довжина в списку в `main`).

Python 3.12 підказує: `Did you mean: '...'?` (може, ти мав на увазі), `Did you forget to import '...'?`
(забув імпорт), `Perhaps you forgot a comma?` (забув кому). Підказки корисні, але **не завжди правильні**
(побачиш нижче).

### Часті помилки в лабах першого курсу (справжній вивід Python 3.12.3)

| Помилка | Що означає | Приклад коду → останній рядок traceback |
|---|---|---|
| `NameError` | імені нема (одруківка, не створив змінну, забув import) | `T = 2 * math.pi` без `import math` → `NameError: name 'math' is not defined. Did you forget to import 'math'?` |
| `TypeError` | операція не підходить для цього типу | `"5" + 3` → `TypeError: can only concatenate str (not "int") to str`; `period()` → `TypeError: period() missing 1 required positional argument: 'length'` |
| `ValueError` | тип правильний, а значення ні | `float("9,81")` → `ValueError: could not convert string to float: '9,81'`; `math.sqrt(-1)` → `ValueError: math domain error` |
| `ZeroDivisionError` | ділення на нуль | `sum([]) / len([])` → `ZeroDivisionError: division by zero` |
| `IndexError` | номер за межами списку | `[0.0, 0.5, 1.0][3]` → `IndexError: list index out of range` |
| `KeyError` | ключа нема в словнику | `{"g": 9.81}["G"]` → `KeyError: 'G'` |
| `AttributeError` | у об'єкта нема такого методу | `"9.81 9.79".splitt()` → `AttributeError: 'str' object has no attribute 'splitt'. Did you mean: 'split'?` |
| `IndentationError` | відступи | тіло функції без відступу → `IndentationError: expected an indented block after function definition on line 1`; зайвий відступ → `IndentationError: unexpected indent` |
| `SyntaxError` | Python не може навіть прочитати файл | незакрита дужка `print(f"T = {T:.3f} с"` → `SyntaxError: '(' was never closed`; `if x = 5:` → `SyntaxError: invalid syntax. Maybe you meant '==' or ':=' instead of '='?`; `print("g =" g)` → `SyntaxError: invalid syntax. Perhaps you forgot a comma?` |

`SyntaxError` і `IndentationError` не мають рядка `Traceback (most recent call last)`: програма не запустилась
зовсім, жоден рядок не виконався.

### Друк для налагодження

| Запис | Що друкує |
|---|---|
| `print(f"{x=}")` | `x=` і значення (рядки - в лапках!) |
| `print(f"{x=:.3f}")` | те саме, 3 знаки після коми |
| `print(f"{a / b = :.4f}")` | можна вираз; пробіли навколо `=` зберігаються |
| `print(repr(s))` | рядок «як є»: видно пробіли, `\n`, лапки |
| `print(type(x))` | тип: `<class 'str'>`, `<class 'float'>` |
| `print(..., file=sys.stderr)` | друк у **потік помилок**, а не в звичайний вивід (потрібен `import sys`) |

### Перші команди pdb

`breakpoint()` у коді зупиняє програму і відкриває **pdb** (Python debugger, вбудований налагоджувач).
Запрошення `(Pdb)` - він чекає команду.

| Команда | Від слова | Що робить |
|---|---|---|
| `p вираз` | print | показати значення |
| `n` | next | виконати рядок і зупинитись на наступному (у функцію не заходить) |
| `s` | step | зробити крок **всередину** функції |
| `c` | continue | їхати далі до наступного `breakpoint()` або до кінця |
| `l` | list | показати код навколо; `->` - рядок, який виконається наступним |
| `q` | quit | вийти (програма обривається) |

Повний pdb - в уроці 06.

## Передбач, потім запусти

1. Що надрукує ця програма?

```python
import math

length = 1.0
T = 2 * math.pi * math.sqrt(length / 9.81)
print(f"{T=}")
print(f"{T=:.3f}")
print(f"{length / 9.81 = :.4f}")
line = "9.81\n"
word = "9.81 "
print(line, word, "|")
print(repr(line), repr(word))
```

<details markdown="1"><summary>Відповідь</summary>

```text
T=2.0060666807106475
T=2.006
length / 9.81 = 0.1019
9.81
 9.81  |
'9.81\n' '9.81 '
```

`f"{T=}"` пише ім'я, знак `=` і значення. Після двокрапки - формат, як у звичайному f-рядку. `print(line, ...)`
не показує, що в кінці `line` є `\n` (він просто переносить рядок), а в `word` - пробіл. `repr` показує все.
</details>

2. Файл `masa.py` питає дві маси. Ти вводиш `2` і `3`. Що він надрукує?

```python
mass_1 = input("Перша маса, кг: ")
mass_2 = input("Друга маса, кг: ")
total = mass_1 + mass_2
print("Разом:", total, "кг")
```

<details markdown="1"><summary>Відповідь</summary>

```text
Перша маса, кг: 2
Друга маса, кг: 3
Разом: 23 кг
```

`input()` завжди повертає **рядок**. `"2" + "3"` - це склеювання рядків, `"23"`. Помилки нема, тому traceback не
допоможе - допоможе `print(f"{mass_1=}")` (крок 5 у «Руками»).
</details>

3. У `main()` є змінні `lengths` (список) і `length` (одне число), а в коді одруківка `period(lenght)`. Python
   підкаже `Did you mean: '...'?`. Яке ім'я він запропонує?

<details markdown="1"><summary>Відповідь</summary>

`'lengths'`, а не `'length'` (справжній вивід - у кроці 1 «Руками»). Підказка рахує, яке ім'я «найближче» за
буквами, і тут вгадала неправильно. Підказка - не наказ: дивись сам, що мав на увазі.
</details>

4. У функції стоїть `assert length > 0, "..."`. Що буде, якщо запустити `python3 -O period.py` з від'ємною
   довжиною?

<details markdown="1"><summary>Відповідь</summary>

`-O` (optimize) **вимикає всі assert**. Перевірки нема, і програма падає далі, на `math.sqrt` з
`ValueError: math domain error` (крок 3 «Руками»). Тому assert - для налагодження і самоперевірки, а не для
перевірки того, що вводить користувач.
</details>

## Руками

Тека для вправ (у тебе замість `evgen` у шляхах буде твоє ім'я користувача):

```bash
mkdir -p ~/univer/praktyka/nalag1
cd ~/univer/praktyka/nalag1
nano period.py
```

### Крок 1. Прочитай traceback знизу вгору

Набери в `period.py` (період маятника `T = 2π·√(l/g)`), збережи Ctrl+O, Enter, вийди Ctrl+X:

```python
import math

G = 9.81


def period(length):
    return 2 * math.pi * math.sqrt(length / G)


def main():
    lengths = [0.5, 1.0, 1.5]
    for length in lengths:
        print(f"l = {length} м, T = {period(lenght):.3f} с")


main()
```

```bash
python3 period.py
```

```text
Traceback (most recent call last):
  File "/home/evgen/univer/praktyka/nalag1/period.py", line 16, in <module>
    main()
  File "/home/evgen/univer/praktyka/nalag1/period.py", line 13, in main
    print(f"l = {length} м, T = {period(lenght):.3f} с")
                                        ^^^^^^
NameError: name 'lenght' is not defined. Did you mean: 'lengths'?
```

Знизу вгору: `NameError` - імені `lenght` нема. Де: рядок 13, функція `main`, `^^^^^^` під `lenght`. Підказка
каже `lengths`, але ми мали на увазі `length` (одне число з циклу). Рядок 16 - лише «звідки викликали».

### Крок 2. Помилка глибше, ніж здається

Виправ `lenght` на `length`. А в списку «помились при записі даних»: заміни `1.5` на `-1.5`. Запусти знову:

```bash
python3 period.py
```

```text
l = 0.5 м, T = 1.419 с
l = 1.0 м, T = 2.006 с
Traceback (most recent call last):
  File "/home/evgen/univer/praktyka/nalag1/period.py", line 16, in <module>
    main()
  File "/home/evgen/univer/praktyka/nalag1/period.py", line 13, in main
    print(f"l = {length} м, T = {period(length):.3f} с")
                                 ^^^^^^^^^^^^^^
  File "/home/evgen/univer/praktyka/nalag1/period.py", line 7, in period
    return 2 * math.pi * math.sqrt(length / G)
                         ^^^^^^^^^^^^^^^^^^^^^
ValueError: math domain error
```

Падає в рядку 7 (`sqrt` від від'ємного), але **винен** рядок 11 зі списком. Traceback показує, де програма
впала, а не де ти помилився. Тому читаємо всі рівні, а не лише нижній.

### Крок 3. assert - програма сама каже, що не так

Додай у функцію перший рядок-перевірку (тепер функція така):

```python
def period(length):
    assert length > 0, f"довжина має бути додатна, а не {length}"
    return 2 * math.pi * math.sqrt(length / G)
```

`assert умова, повідомлення` - «я впевнений, що умова істинна; якщо ні - зупинись з цим повідомленням».

```bash
python3 period.py
```

```text
l = 0.5 м, T = 1.419 с
l = 1.0 м, T = 2.006 с
Traceback (most recent call last):
  File "/home/evgen/univer/praktyka/nalag1/period.py", line 17, in <module>
    main()
  File "/home/evgen/univer/praktyka/nalag1/period.py", line 14, in main
    print(f"l = {length} м, T = {period(length):.3f} с")
                                 ^^^^^^^^^^^^^^
  File "/home/evgen/univer/praktyka/nalag1/period.py", line 7, in period
    assert length > 0, f"довжина має бути додатна, а не {length}"
           ^^^^^^^^^^
AssertionError: довжина має бути додатна, а не -1.5
```

Тепер одразу видно причину: `-1.5`. А з `-O` перевірки зникають:

```bash
python3 -O period.py
```

```text
l = 0.5 м, T = 1.419 с
l = 1.0 м, T = 2.006 с
Traceback (most recent call last):
  File "/home/evgen/univer/praktyka/nalag1/period.py", line 17, in <module>
    main()
  File "/home/evgen/univer/praktyka/nalag1/period.py", line 14, in main
    print(f"l = {length} м, T = {period(length):.3f} с")
                                 ^^^^^^^^^^^^^^
  File "/home/evgen/univer/praktyka/nalag1/period.py", line 8, in period
    return 2 * math.pi * math.sqrt(length / G)
                         ^^^^^^^^^^^^^^^^^^^^^
ValueError: math domain error
```

### Крок 4. `python3 -i` - зазирнути всередину після падіння

`-i` (interactive) після кінця програми (і після падіння теж) відкриває Python `>>>`, де вже є все з файлу:

```bash
python3 -i period.py
```

```text
l = 0.5 м, T = 1.419 с
l = 1.0 м, T = 2.006 с
Traceback (most recent call last):
  File "/home/evgen/univer/praktyka/nalag1/period.py", line 17, in <module>
    main()
  File "/home/evgen/univer/praktyka/nalag1/period.py", line 14, in main
    print(f"l = {length} м, T = {period(length):.3f} с")
                                 ^^^^^^^^^^^^^^
  File "/home/evgen/univer/praktyka/nalag1/period.py", line 7, in period
    assert length > 0, f"довжина має бути додатна, а не {length}"
           ^^^^^^^^^^
AssertionError: довжина має бути додатна, а не -1.5
>>> G
9.81
>>> period(1.0)
2.0060666807106475
>>> period(-1.5)
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
  File "/home/evgen/univer/praktyka/nalag1/period.py", line 7, in period
    assert length > 0, f"довжина має бути додатна, а не {length}"
           ^^^^^^^^^^
AssertionError: довжина має бути додатна, а не -1.5
>>> lengths
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
NameError: name 'lengths' is not defined
>>>
```

Тут видно глобальні імена (`G`, `period`) і можна викликати функції руками. А `lengths` нема: це **локальна**
змінна `main`, вона зникла разом з функцією. Щоб побачити локальні змінні місця падіння, є `pdb.pm()` (урок 06).
Вихід з `>>>` - Ctrl+D.

### Крок 5. `breakpoint()` і перші кроки в pdb

Онови `period.py` до такого вигляду (assert лишається, у циклі додався `breakpoint()`):

```python
import math

G = 9.81


def period(length):
    assert length > 0, f"довжина має бути додатна, а не {length}"
    return 2 * math.pi * math.sqrt(length / G)


def main():
    lengths = [0.5, 1.0, -1.5]
    for length in lengths:
        breakpoint()
        print(f"l = {length} м, T = {period(length):.3f} с")


main()
```

```bash
python3 period.py
```

Нижче - справжній сеанс. Після `(Pdb)` - те, що набрано руками, далі Enter:

```text
> /home/evgen/univer/praktyka/nalag1/period.py(15)main()
-> print(f"l = {length} м, T = {period(length):.3f} с")
(Pdb) p length
0.5
(Pdb) s
--Call--
> /home/evgen/univer/praktyka/nalag1/period.py(6)period()
-> def period(length):
(Pdb) s
> /home/evgen/univer/praktyka/nalag1/period.py(7)period()
-> assert length > 0, f"довжина має бути додатна, а не {length}"
(Pdb) p length / G
0.0509683995922528
(Pdb) n
> /home/evgen/univer/praktyka/nalag1/period.py(8)period()
-> return 2 * math.pi * math.sqrt(length / G)
(Pdb) n
--Return--
> /home/evgen/univer/praktyka/nalag1/period.py(8)period()->1.4185033534428875
-> return 2 * math.pi * math.sqrt(length / G)
(Pdb) c
l = 0.5 м, T = 1.419 с
> /home/evgen/univer/praktyka/nalag1/period.py(15)main()
-> print(f"l = {length} м, T = {period(length):.3f} с")
(Pdb) l
 10
 11     def main():
 12         lengths = [0.5, 1.0, -1.5]
 13         for length in lengths:
 14             breakpoint()
 15  ->         print(f"l = {length} м, T = {period(length):.3f} с")
 16
 17
 18     main()
[EOF]
(Pdb) c
l = 1.0 м, T = 2.006 с
> /home/evgen/univer/praktyka/nalag1/period.py(15)main()
-> print(f"l = {length} м, T = {period(length):.3f} с")
(Pdb) p length
-1.5
(Pdb) q
Traceback (most recent call last):
  File "/home/evgen/univer/praktyka/nalag1/period.py", line 18, in <module>
    main()
  File "/home/evgen/univer/praktyka/nalag1/period.py", line 15, in main
    print(f"l = {length} м, T = {period(length):.3f} с")
    ^^^^^
  File "/usr/lib/python3.12/bdb.py", line 90, in trace_dispatch
    return self.dispatch_line(frame)
           ^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/lib/python3.12/bdb.py", line 115, in dispatch_line
    if self.quitting: raise BdbQuit
                      ^^^^^^^^^^^^^
bdb.BdbQuit
```

Що тут сталося:
- `> ...period.py(15)main()` - де стоїмо: файл, рядок 15, функція `main`. `->` - рядок, який **ще не виконався**.
- `s` на рядку з викликом `period(...)` зайшов усередину функції (`--Call--`), `n` ішов по рядках,
  `--Return--` і `->1.418...` - функція повертає це значення.
- `c` поїхав до наступного `breakpoint()` (наступний оберт циклу).
- `q` обриває програму, і Python 3.12 друкує traceback з `bdb.BdbQuit`. **Це не твоя помилка** - так pdb
  повідомляє «користувач вийшов». Хочеш без нього - доїдь до кінця командою `c`.

Вимкнути всі `breakpoint()` без правки файлу - змінна середовища `PYTHONBREAKPOINT=0`:

```bash
PYTHONBREAKPOINT=0 python3 period.py
```

Програма пройде без зупинок і впаде на `AssertionError` з `-1.5`, як у кроці 3.

Підказка для самоперевірки без набору: команди pdb можна подати одразу через `printf` (у виводі тоді не видно
самих команд, лише `(Pdb)` підряд):

```bash
printf 'p length\nc\np length\nc\nq\n' | python3 period.py
```

```text
> /home/evgen/univer/praktyka/nalag1/period.py(15)main()
-> print(f"l = {length} м, T = {period(length):.3f} с")
(Pdb) 0.5
(Pdb) l = 0.5 м, T = 1.419 с
> /home/evgen/univer/praktyka/nalag1/period.py(15)main()
-> print(f"l = {length} м, T = {period(length):.3f} с")
(Pdb) 1.0
(Pdb) l = 1.0 м, T = 2.006 с
> /home/evgen/univer/praktyka/nalag1/period.py(15)main()
-> print(f"l = {length} м, T = {period(length):.3f} с")
(Pdb) Traceback (most recent call last):
  File "/home/evgen/univer/praktyka/nalag1/period.py", line 18, in <module>
    main()
  File "/home/evgen/univer/praktyka/nalag1/period.py", line 15, in main
    print(f"l = {length} м, T = {period(length):.3f} с")
    ^^^^^
  File "/usr/lib/python3.12/bdb.py", line 90, in trace_dispatch
    return self.dispatch_line(frame)
           ^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/lib/python3.12/bdb.py", line 115, in dispatch_line
    if self.quitting: raise BdbQuit
                      ^^^^^^^^^^^^^
bdb.BdbQuit
```

### Крок 6. print-налагодження: `f"{x=}"`, `type`, stderr

Створи `masa.py` з «Передбач» (пункт 2) і запусти. Число `23` - підозріле. Додай друк змінних **у потік помилок**
(stderr), щоб він не змішувався зі справжнім виводом:

```python
import sys

mass_1 = input("Перша маса, кг: ")
mass_2 = input("Друга маса, кг: ")
total = mass_1 + mass_2
print(f"{mass_1=} {mass_2=} {total=}", file=sys.stderr)
print(f"{type(total)=}", file=sys.stderr)
print("Разом:", total, "кг")
```

```bash
python3 masa.py
```

```text
Перша маса, кг: 2
Друга маса, кг: 3
mass_1='2' mass_2='3' total='23'
type(total)=<class 'str'>
Разом: 23 кг
```

Лапки в `mass_1='2'` і `<class 'str'>` кажуть: це рядки, треба `float(input(...))`. На екрані stderr і звичайний
вивід видно разом, але їх можна розділити. `2>` перенаправляє лише stderr:

```bash
printf '2\n3\n' | python3 masa.py 2>/dev/null
printf '2\n3\n' | python3 masa.py 2> debug.txt
cat debug.txt
```

```text
Перша маса, кг: Друга маса, кг: Разом: 23 кг
Перша маса, кг: Друга маса, кг: Разом: 23 кг
mass_1='2' mass_2='3' total='23'
type(total)=<class 'str'>
```

(Відповіді `2` і `3` прийшли з `printf`, тому їх не видно після запрошень.) `/dev/null` - «чорна діра»,
усе, що туди пишеш, зникає. Виправ сам: `float(input(...))`, і прибери налагоджувальні `print`.

## Типові помилки

- **Забутий налагоджувальний `print` у функції ламає doctest.** doctest порівнює все, що функція надрукувала у
  звичайний вивід:

  ```text
  Failed example:
      period(1.0)
  Expected:
      'T = 2.006 с'
  Got:
      t=2.0060666807106475
      'T = 2.006 с'
  ```

  Друк з `file=sys.stderr` doctest не ловить (перевірено: той самий файл з `print(f"{length=}", file=sys.stderr)`
  показав `length=1.0` на екрані, а в `Got` його нема). Але перед здачею прибери обидва.
- **Забутий `breakpoint()`.** Програма «зависає» на `(Pdb)`. А `perevir` (урок 03) замість цього пише
  `doctest: файл питає input() при запуску. Дай відповіді після назви: perevir lab_bp.py 5`, бо pdb теж читає з
  клавіатури. Нема `input()`, а таке повідомлення є - шукай `breakpoint()`: `grep -n breakpoint *.py`.
- **`q` у pdb дає traceback з `bdb.BdbQuit`.** Це нормально, див. крок 5.
- **assert з дужками завжди «проходить».** `assert (length > 0, "текст")` - це перевірка кортежу, а непорожній
  кортеж завжди істина. Python 3.12 попереджає:
  `SyntaxWarning: assertion is always true, perhaps remove parentheses?` і програма йде далі. Пиши без дужок:
  `assert length > 0, "текст"`.
- **assert для перевірки вводу користувача.** З `python3 -O` він зникає. Для вводу - звичайна умова й
  повідомлення (або виняток `ValueError`), assert - для «цього не може бути».
- **Читати лише перший рядок traceback.** Головне - **останній** рядок і найнижчий рядок **твого** файлу.
  Рядки з `/usr/lib/python3.12/...` - це бібліотеки Python, їх зазвичай пропускаєш.
- **`SyntaxError` показує не той рядок.** Для незакритої дужки Python 3.12 показує рядок, де дужку **відкрито**
  (`'(' was never closed`). Якщо повідомлення дивне - подивись і на рядок **вище**.

## Як роблять профі

- Python з кожною версією пояснює помилки краще: `^^^` під точним місцем з'явились у 3.11 (PEP 657), підказки
  `Did you forget to import` - у 3.12. Тому перше правило налагодження - **уважно прочитати повідомлення**.
- `print(f"{x=}")` - нормальний інструмент і в 2026, але для програм довших за одну лабу професіонали переходять на
  `logging` (рівні DEBUG/INFO/WARNING, можна вимкнути одним рядком) - урок 06.
- `breakpoint()` (PEP 553, Python 3.7+) замість старого `import pdb; pdb.set_trace()`: коротше і вимикається
  через `PYTHONBREAKPOINT=0`, а через `PYTHONBREAKPOINT=ipdb.set_trace` вмикає інший налагоджувач (урок 06).
  У Python 3.12 (Mint 22) pdb зупиняється на рядку **після** `breakpoint()` (у кроці 5 - рядок 15); з Python 3.13
  - одразу на рядку з `breakpoint()`. Також з 3.13 traceback кольоровий, а 3.14 вміє підключити pdb до вже
  запущеної програми: `python -m pdb -p PID`.
- Лінтер ловить забуте: `ruff` (є у venv з уроку 03) має правила `T100` (забутий `breakpoint()`) і `T201`
  (забутий `print`): `ruff check --select T100,T201 period.py` (не в лабах - там `print` бувають потрібні).
- У VS Code ті самі речі робить графічний налагоджувач (debugpy) - це урок 27, пізніше. pdb працює скрізь, де є
  термінал: на сервері, по ssh, на комп'ютері в аудиторії.

## Самоперевірка

1. Traceback має 3 рівні: `<module>` → `main` → `period`, останній рядок `ValueError: math domain error`. У якому
   рядку і якій функції програма впала? Чи обов'язково там помилка?
2. Чим `print(f"{x=}")` кращий за `print(x)`, коли `x = "2"`?
3. Що зробить `python3 -O файл.py` з рядком `assert g > 0, "g має бути додатне"`?
4. Ти в `(Pdb)` на рядку `y = f(x)`. Чим відрізняються `n` і `s`? Що зробить `c`?
5. Що надрукує `python3 -i файл.py` після падіння і чому там не видно локальних змінних функції?

<details markdown="1"><summary>Відповіді</summary>

1. У функції `period` (найнижчий рівень, рядок з `^^^`). Не обов'язково: там програма **впала**, а погане
   значення могло прийти згори, з `main` (як `-1.5` у кроці 2).
2. `f"{x=}"` друкує ім'я і `repr` значення: `x='2'`. Лапки показують, що це рядок, а `print(x)` надрукує просто `2`.
3. Нічого: `-O` вимикає всі `assert`, рядок не виконається.
4. `n` виконає рядок повністю (разом з викликом `f`) і зупиниться на наступному; `s` зайде всередину `f`
   (`--Call--`). `c` поїде далі до наступного `breakpoint()` або до кінця програми.
5. Traceback, а потім запрошення `>>>`, де доступні глобальні імена файлу (функції, константи). Локальні змінні
   функції живуть лише поки функція працює; після падіння їх уже нема. Їх показує `import pdb; pdb.pm()` (урок 06).
</details>

## Джерела

- Python 3.12, `pdb` - https://docs.python.org/3.12/library/pdb.html (відкрито 18.11.2026)
- `breakpoint()` і `PYTHONBREAKPOINT` - https://docs.python.org/3.12/library/functions.html#breakpoint ,
  PEP 553 https://peps.python.org/pep-0553/ (відкрито 18.11.2026)
- Інструкція `assert` і `-O` - https://docs.python.org/3.12/reference/simple_stmts.html#the-assert-statement ,
  https://docs.python.org/3.12/using/cmdline.html#cmdoption-O (відкрито 18.11.2026)
- Покращені повідомлення про помилки в 3.12 - https://docs.python.org/3.12/whatsnew/3.12.html#improved-error-messages
  (відкрито 18.11.2026)
- Що нового в 3.13 (кольоровий traceback, `breakpoint()` зупиняється одразу) -
  https://docs.python.org/3/whatsnew/3.13.html ; у 3.14 (`pdb -p PID`, PEP 768) -
  https://docs.python.org/3/whatsnew/3.14.html (відкрито 18.11.2026)
- Точні місця помилок `^^^` - PEP 657 https://peps.python.org/pep-0657/ (відкрито 18.11.2026)
- f-рядки з `=` - https://docs.python.org/3.12/reference/lexical_analysis.html#f-strings (відкрито 18.11.2026)
- Правила ruff T100/T201 - https://docs.astral.sh/ruff/rules/debugger/ , https://docs.astral.sh/ruff/rules/print/
  (відкрито 18.11.2026)
- Увесь вивід у цьому уроці - справжній, з тестової Linux Mint 22.3, Python 3.12.3 (18.11.2026).
