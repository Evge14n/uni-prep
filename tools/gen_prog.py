"""Генератор тестів розділу prog (залік з програмування) -> content/prog/quiz.json.

Запуск: python -P -E tools/gen_prog.py

Що перевіряє, перш ніж записати quiz.json:
1. Кожне питання «що виведе код» - виконує код через exec в ізольованому namespace,
   ловить stdout і порівнює з правильним варіантом; жоден неправильний варіант не може
   збігатися з виводом.
2. Питання «яка помилка» - виконує код і порівнює назву винятку з правильним варіантом.
3. Питання про doctest - проганяє doctest із коду справжнім doctest.DocTestRunner.
4. Питання з verify (calc) - рахує verify через sympy (як tools/verify_quizzes.py) і
   порівнює з виводом exec: це два незалежні шляхи (Python-код і математична формула).
5. content/prog/zadachi.md - виконує кожен блок ```python і проганяє всі doctest у ньому.
6. Нема LaTeX і довгих тире.

Джерела: лекції 1, 2, 7-9, вимоги викладача, файл UNI2 (теми 1-10).
"""
import builtins
import contextlib
import doctest
import io
import json
import re
import sys
import textwrap
import types
from pathlib import Path

import sympy as sp

ROOT = Path(__file__).resolve().parent.parent
UNIT = ROOT / "content" / "prog"

NS = {name: getattr(sp, name) for name in dir(sp) if not name.startswith("_")}
NS.update({"e": sp.E, "E": sp.E, "pi": sp.pi, "oo": sp.oo, "ln": sp.log})
for _s in "x y z t u v w a b c n k m h r s".split():
    NS[_s] = sp.Symbol(_s, real=True)

NUM = re.compile(r"-?\d+(\.\d+)?")
QS = []
ERRORS = []

S_L2 = "Лекція 2 (конспект)"
S_REQ = "Вимоги викладача"
S_U = "UNI2 тема "
S_NO = "[нема конспекту - звір з лекцією] стандартний Python"


def ev(expr):
    return sp.sympify(eval(expr, {"__builtins__": {}}, NS))  # noqa: S307 - лише наші рядки


def run(code):
    """Виконує код в ізольованому namespace. Повертає (вивід, назва винятку або None)."""
    code = textwrap.dedent(code).strip("\n")
    buf = io.StringIO()
    ns = {"__builtins__": builtins, "__name__": "__quiz__"}
    exc = None
    with contextlib.redirect_stdout(buf):
        try:
            exec(compile(code, "<quiz>", "exec"), ns)  # noqa: S102 - наш код
        except BaseException as e:  # noqa: BLE001
            exc = type(e).__name__
    return buf.getvalue().rstrip("\n").replace("\n", " / "), exc


def add(q):
    q["id"] = f"p-{len(QS) + 1:03d}"
    QS.append(q)


def out(topic, code, options, answer, explain, src, verify=None, q=None):
    """«Що виведе код?» з exec-перевіркою."""
    code = textwrap.dedent(code).strip("\n")
    got, exc = run(code)
    where = f"{topic}: {code.splitlines()[0]}"
    if exc:
        ERRORS.append(f"{where}: код упав з {exc}")
    if got != options[answer]:
        ERRORS.append(f"{where}: exec дав «{got}», а правильний варіант «{options[answer]}»")
    for i, o in enumerate(options):
        if i != answer and o == got:
            ERRORS.append(f"{where}: неправильний варіант {i} теж дорівнює виводу")
    text = q or "Що виведе код?"
    if " / " in got:
        text += " (рядки виводу розділено « / »)"
    item = {"topic": topic, "type": "single", "q": text, "pre": code,
            "options": options, "answer": answer, "explain": explain, "src": src}
    if verify:
        if not NUM.fullmatch(got):
            ERRORS.append(f"{where}: verify для нечислового виводу «{got}»")
        else:
            val = sp.sympify(got)
            if abs(float(sp.N(ev(verify))) - float(val)) > 1e-9 * max(1.0, abs(float(val))):
                ERRORS.append(f"{where}: verify={ev(verify)} ≠ exec={got}")
            ov = []
            for i, o in enumerate(options):
                if NUM.fullmatch(o):
                    if i != answer and abs(float(o) - float(val)) < 1e-12:
                        ERRORS.append(f"{where}: варіант {i} числом дорівнює відповіді")
                    ov.append(o)
                else:
                    ov.append(None)
            item.update({"calc": True, "verify": verify, "value": got, "optionValues": ov})
    add(item)


def err(topic, code, options, answer, explain, src, q="Що станеться при запуску коду?"):
    """«Яка помилка?» - перевіряє назву винятку."""
    code = textwrap.dedent(code).strip("\n")
    _, exc = run(code)
    want = options[answer].split()[0]
    if exc != want:
        ERRORS.append(f"{topic}: {code.splitlines()[0]}: виняток {exc}, а у відповіді {want}")
    add({"topic": topic, "type": "single", "q": q, "pre": code, "options": options,
         "answer": answer, "explain": explain, "src": src})


def doctest_result(code):
    """Проганяє всі doctest з коду. Повертає (спроб, падінь)."""
    code = textwrap.dedent(code).strip("\n")
    ns = {"__builtins__": builtins, "__name__": "__doctest__"}
    with contextlib.redirect_stdout(io.StringIO()):
        exec(compile(code, "<doctest>", "exec"), ns)  # noqa: S102
    parser = doctest.DocTestParser()
    runner = doctest.DocTestRunner(verbose=False, optionflags=0)
    for name, obj in list(ns.items()):
        if isinstance(obj, types.FunctionType) and obj.__doc__:
            test = parser.get_doctest(obj.__doc__, dict(ns), name, "<doctest>", 0)
            runner.run(test, out=lambda _s: None)
    return runner.tries, runner.failures


def dt(topic, code, options, answer, explain, src, fails, q):
    """Питання про doctest: кількість падінь перевіряє справжній doctest."""
    code = textwrap.dedent(code).strip("\n")
    tries, failed = doctest_result(code)
    if failed != fails:
        ERRORS.append(f"{topic}: {q[:40]}: doctest упав {failed} з {tries}, очікував {fails}")
    add({"topic": topic, "type": "single", "q": q, "pre": code, "options": options,
         "answer": answer, "explain": explain, "src": src})


def th(topic, q, options, answer, explain, src, kind="single", keep=False):
    item = {"topic": topic, "type": kind, "q": q, "options": options, "answer": answer,
            "explain": explain, "src": src}
    if keep:
        item["keepOrder"] = True
    add(item)


# ======================================================== 1. Арифметика і типи
T = "Арифметика і типи"
out(T, "print(-7 // 2)", ["-4", "-3", "-3.5", "4"], 0,
    "// округлює ВНИЗ (до меншого числа), а не до нуля: -3,5 → -4. Типова помилка - -3, "
    "ніби ціла частина просто відкидає дробову.",
    S_U + "1", verify="floor(Rational(-7, 2))")
out(T, "print(-7 % 3)", ["2", "-1", "1", "-2"], 0,
    "Остача має знак дільника: -7 = 3·(-3) + 2. Перевірка: (-7 // 3)·3 + (-7 % 3) = -9 + 2 = -7.",
    S_U + "1", verify="Mod(-7, 3)")
out(T, "print(2 ** 3 ** 2)", ["512", "64", "36", "18"], 0,
    "Степінь рахується справа наліво: 3 ** 2 = 9, потім 2 ** 9 = 512. 64 вийшло б з (2 ** 3) ** 2.",
    S_U + "1", verify="Pow(2, 9)")
out(T, """
    number = 472
    print(number // 10 % 10)
    """, ["7", "2", "4", "47"], 0,
    "472 // 10 = 47, потім 47 % 10 = 7 - передостання цифра. 47 - це лише перший крок.",
    S_U + "1", verify="Mod(floor(Rational(472, 10)), 10)")
out(T, """
    number1 = "12"
    number2 = "18"
    print(number1 + number2)
    """, ["1218", "30", "12 18", "TypeError"], 0,
    "Обидва значення - рядки (так їх повертає input()), а для рядків + склеює. Щоб отримати 30, "
    "треба int(input()).", S_L2)
out(T, "print(type(8 / 4))", ["<class 'float'>", "<class 'int'>", "2", "<class 'str'>"], 0,
    "Звичайне ділення / завжди дає float, навіть якщо ділиться націло: 8 / 4 = 2.0.",
    S_U + "1")
out(T, "print(10 / 4)", ["2.5", "2", "3", "0.4"], 0,
    "/ - звичайне ділення: 2.5. 2 дало б 10 // 4.", S_U + "1", verify="Rational(10, 4)")
out(T, """
    count = 5
    count += 3
    count *= 2
    print(count)
    """, ["16", "11", "13", "10"], 0,
    "count += 3 - це count = count + 3 = 8; count *= 2 - це 8·2 = 16.",
    S_L2, verify="(5 + 3)*2")
out(T, "print(True + True + False)", ["2", "TrueTrue", "True", "TypeError"], 0,
    "True поводиться як 1, False як 0: 1 + 1 + 0 = 2. На цьому тримається прийом «рядок * умова».",
    S_U + "1", verify="1 + 1 + 0")
out(T, 'print("ha" * 3)', ["hahaha", "ha3", "ha ha ha", "TypeError"], 0,
    "Рядок, помножений на ціле, повторюється стільки разів.", S_U + "1")
out(T, """
    x = 2
    y = (x ** 3
         + x ** 2)
    print(y)
    """, ["12", "8", "4", "SyntaxError"], 0,
    "Дужки кажуть Python, що вираз триває на наступному рядку: 8 + 4 = 12. Без дужок другий рядок "
    "став би окремою командою і y = 8 (пастка з лекції 2).", S_L2, verify="2**3 + 2**2")

# ======================================================== 2. Функції і return
T = "Функції і return"
out(T, """
    def add(first, second):
        result = first + second

    print(add(3, 5))
    """, ["None", "8", "35", "нічого не виведе"], 0,
    "Функція порахувала, але нічого не повернула, а без return функція повертає None. "
    "Найчастіша помилка в ЛР1.", S_L2)
out(T, """
    def square(number):
        print(number * number)

    result = square(4)
    print(result)
    """, ["16 / None", "16 / 16", "None", "16"], 0,
    "Перший print - усередині функції (16). Але функція повертає None, тому другий print дає None.",
    S_U + "2")
out(T, """
    def double(value):
        value = value * 2
        return value

    number = 3
    double(number)
    print(number)
    """, ["3", "6", "None", "NameError"], 0,
    "Усередині функції value - локальна змінна. Результат double(number) нікуди не присвоїли, "
    "а number лишилось 3.", S_L2)
out(T, """
    def sign_word(number):
        if number > 0:
            return "plus"

    print(sign_word(-1))
    """, ["None", "plus", "minus", "порожній рядок"], 0,
    "Для -1 умова хибна, до return справа не доходить - функція повертає None.", S_U + "2")
out(T, """
    def add_item(items):
        items.append(1)

    data = []
    add_item(data)
    add_item(data)
    print(data)
    """, ["[1, 1]", "[]", "[1]", "None"], 0,
    "Список передається як посилання на той самий обʼєкт, тому append змінює data. Двічі - [1, 1].",
    S_U + "8")

# ======================================================== 3. print і f-рядки
T = "print і f-рядки"
out(T, 'print(1, 2, 3, sep="-")', ["1-2-3", "1 2 3", "-1-2-3-", "123"], 0,
    "sep ставиться МІЖ значеннями, а не на краях.", S_L2)
out(T, """
    print("a", end="")
    print("b")
    """, ["ab", "a / b", "a b", "b"], 0,
    "end=\"\" замінює перехід на новий рядок порожнім рядком, тому b друкується одразу після a.",
    S_L2)
out(T, 'print(f"{3.14159:.2f}")', ["3.14", "3.1", "3.14159", "3.15"], 0,
    ".2f - два знаки після коми з округленням: 3.14159 → 3.14.", S_L2)
out(T, """print(f"[{'ab':>4}]")""", ["[  ab]", "[ab  ]", "[ab]", "[ ab ]"], 0,
    ">4 - ширина 4, вирівнювання вправо, зайві місця - пробіли зліва.", S_U + "2")
out(T, 'print(f"{1234567:,}")', ["1,234,567", "1234567", "1 234 567", "1.234.567"], 0,
    "Кома у форматі розділяє тисячі комою.", S_L2)
out(T, 'print(f"{2 / 3:.3g}")', ["0.667", "0.666", "0.6667", "0.67"], 0,
    ".3g - три ЗНАЧУЩІ цифри (нулі на початку не рахуються) з округленням: 0.6666... → 0.667.",
    S_L2)

# ======================================================== 4. Розгалуження
T = "Розгалуження і логіка"
out(T, """
    x = 5
    print(0 < x < 10 and x % 2 == 0)
    """, ["False", "True", "5", "SyntaxError"], 0,
    "0 < x < 10 - True, але x % 2 == 0 - False (5 непарне). True and False = False.", S_U + "3")
out(T, "print(True or False and False)", ["True", "False", "None", "SyntaxError"], 0,
    "and сильніший за or: спершу False and False = False, потім True or False = True. "
    "Якби рахувати зліва направо, вийшло б False.", S_U + "3")
out(T, """
    year = 1900
    print(year % 4 == 0 and year % 100 != 0 or year % 400 == 0)
    """, ["False", "True", "1900", "None"], 0,
    "1900 ділиться на 4, але й на 100, і не ділиться на 400 - не високосний.", S_U + "3")
out(T, """
    x = -3
    print("pos" if x > 0 else "neg" if x < 0 else "zero")
    """, ["neg", "pos", "zero", "SyntaxError"], 0,
    "Тернарні вирази можна вкладати: x > 0 хибне, далі x < 0 істинне - neg.", S_U + "3")
out(T, "print(0.1 + 0.2 == 0.3)", ["False", "True", "0.3", "None"], 0,
    "0.1 і 0.2 у двійковому записі неточні, сума 0.30000000000000004. Дійсні числа через == "
    "не порівнюють, а дивляться abs(a - b) < ε.", S_U + "3")
out(T, 'print("парне" * (7 % 2 == 0) + "!")', ["!", "парне!", "непарне!", "TypeError"], 0,
    "7 % 2 == 0 - False = 0, рядок * 0 = порожній рядок, лишається \"!\".", S_REQ)

# ======================================================== 5. Цикли
T = "Цикли"
out(T, """
    total = 0
    for i in range(1, 10, 3):
        total += i
    print(total)
    """, ["12", "22", "15", "45"], 0,
    "range(1, 10, 3) дає 1, 4, 7 (10 не входить). 1 + 4 + 7 = 12.",
    S_U + "4", verify="summation(3*k + 1, (k, 0, 2))")
out(T, "print(list(range(5, 0, -2)))", ["[5, 3, 1]", "[5, 3, 1, 0]", "[5, 3]", "[]"], 0,
    "Крок -2, стоп 0 не входить: 5, 3, 1.", S_U + "4")
out(T, """
    count = 0
    number = 100
    while number > 1:
        number //= 2
        count += 1
    print(count)
    """, ["6", "7", "50", "5"], 0,
    "100 → 50 → 25 → 12 → 6 → 3 → 1: шість ділень. Це цілий log₂ 100.",
    S_U + "4", verify="floor(log(100, 2))")
out(T, """
    for i in range(3):
        i = 10
    print(i)
    """, ["10", "2", "3", "0"], 0,
    "Присвоєння i = 10 не впливає на range: на кожному кроці i бере нове значення з range, а потім "
    "стає 10. Після останнього кроку i = 10.", S_U + "4")
out(T, """
    for divisor in range(2, 7):
        if 7 % divisor == 0:
            break
    else:
        print("просте")
    """, ["просте", "нічого не виведе", "SyntaxError", "просте / просте"], 0,
    "7 не ділиться на 2..6, break не спрацював, тому виконується else після циклу.", S_U + "4")
out(T, """
    total = 0
    for i in range(1, 6):
        total += i * i
    print(total)
    """, ["55", "30", "25", "91"], 0,
    "1 + 4 + 9 + 16 + 25 = 55. 30 - якби range(1, 5).",
    S_U + "4", verify="summation(k**2, (k, 1, 5))")
out(T, """
    count = 0
    for i in range(4):
        for j in range(i):
            count += 1
    print(count)
    """, ["6", "16", "10", "4"], 0,
    "Внутрішній цикл робить 0, 1, 2, 3 кроки: разом 6. Це кількість пар j < i з чисел 0..3.",
    S_U + "4", verify="binomial(4, 2)")

# ======================================================== 6. Цілочисельні алгоритми
T = "Цілочисельні алгоритми"
out(T, """
    first, second = 84, 36
    while second != 0:
        first, second = second, first % second
    print(first)
    """, ["12", "6", "4", "252"], 0,
    "Евклід: (84, 36) → (36, 12) → (12, 0). НСД = 12. 252 - це НСК.",
    S_U + "5", verify="gcd(84, 36)")
out(T, """
    number = 2026
    digit_sum = 0
    while number > 0:
        digit_sum += number % 10
        number //= 10
    print(digit_sum)
    """, ["10", "2026", "4", "8"], 0,
    "Беремо останню цифру і відкидаємо її: 6 + 2 + 0 + 2 = 10.", S_U + "5", verify="2 + 0 + 2 + 6")
out(T, """
    number = 28
    found = 0
    divisor = 1
    while divisor * divisor <= number:
        if number % divisor == 0:
            found += 1
            if divisor != number // divisor:
                found += 1
        divisor += 1
    print(found)
    """, ["6", "3", "5", "28"], 0,
    "Пари (1, 28), (2, 14), (4, 7) - 6 дільників. 3 - якби забути другий з пари.",
    S_U + "5", verify="divisor_count(28)")
out(T, """
    first, second = 4, 6
    a, b = first, second
    while b != 0:
        a, b = b, a % b
    print(first * second // a)
    """, ["12", "24", "2", "6"], 0,
    "НСД(4, 6) = 2, НСК = 4·6 // 2 = 12. 24 - забули поділити на НСД.",
    S_U + "5", verify="lcm(4, 6)")
out(T, """
    def is_prime(number):
        if number < 2:
            return False
        divisor = 2
        while divisor * divisor <= number:
            if number % divisor == 0:
                return False
            divisor += 1
        return True

    print(sum(1 for n in range(30) if is_prime(n)))
    """, ["10", "11", "9", "15"], 0,
    "Прості до 30: 2, 3, 5, 7, 11, 13, 17, 19, 23, 29 - десять. 1 не просте.",
    S_U + "5", verify="primepi(29)")
out(T, """
    number = 1230
    result = 0
    while number > 0:
        result = result * 10 + number % 10
        number //= 10
    print(result)
    """, ["321", "0321", "1230", "3210"], 0,
    "Нуль у кінці стає нулем на початку, а число не пишеться з нуля спереду: 321.", S_U + "5")

# ======================================================== 7. Рекурентні
T = "Рекурентні співвідношення"
out(T, """
    previous, current = 0, 1
    for _ in range(10):
        previous, current = current, previous + current
    print(previous)
    """, ["55", "89", "34", "10"], 0,
    "Після n кроків previous = F(n). F(10) = 55. 89 - це current, тобто F(11).",
    S_U + "6", verify="fibonacci(10)")
out(T, """
    previous, current = 0, 1
    for _ in range(5):
        previous = current
        current = previous + current
    print(current)
    """, ["32", "8", "13", "5"], 0,
    "Помилка послідовного присвоєння: current = previous + current бере вже НОВИЙ previous, "
    "тобто current подвоюється: 2, 4, 8, 16, 32. З одночасним присвоєнням було б 8.",
    "Лекція 7", verify="2**5")
out(T, """
    x3, x2, x1 = 1, 0, 1
    for _ in range(3, 9):
        x3, x2, x1 = x2, x1, x1 + 2 * x2 + x3
    print(x1)
    """, ["88", "41", "19", "9"], 0,
    "Послідовність з лекції 7: 1, 0, 1, 2, 4, 9, 19, 41, 88. Після кроків n = 3..8 x1 = x(8) = 88.",
    "Лекція 7")
out(T, """
    term = 1
    for n in range(1, 5):
        term = term * 2 / n
    print(term)
    """, ["0.6666666666666666", "16", "1.3333333333333333", "0.5"], 0,
    "Член ряду eˣ при x = 2: a(4) = 2⁴ / 4! = 16 / 24 = 2/3. Рахуємо з попереднього, без факторіала.",
    "Лекція 7", verify="Rational(2**4, factorial(4))")
out(T, """
    a_value, b_value = 1, 1
    for _ in range(3):
        a_value, b_value = a_value * b_value, a_value + b_value
    print(a_value, b_value)
    """, ["6 5", "8 12", "6 6", "2 3"], 0,
    "Кроки: (1, 2), (2, 3), (6, 5). Якщо рахувати b вже з нового a (без одночасного присвоєння), "
    "вийде (1, 2), (2, 4), (8, 12) - це помилка з лекції 7.", "Лекція 7")

# ======================================================== 8. Точність і корені
T = "Точність ε і корені"
out(T, """
    left, right = 0.0, 1.0
    steps = 0
    while right - left >= 0.001:
        middle = (left + right) / 2
        if middle * middle - 0.5 < 0:
            left = middle
        else:
            right = middle
        steps += 1
    print(steps)
    """, ["10", "9", "1000", "11"], 0,
    "Кожен крок ділить довжину навпіл: 1/2ᵏ < 0,001 вперше при k = 10 (1/1024). Кількість кроків "
    "бісекції ≈ log₂((b - a)/ε).", "Лекція 7", verify="ceiling(log(1000, 2))")
out(T, """
    coefficients = [2, -3, 0, 1]
    x = 2
    value = coefficients[0]
    for coefficient in coefficients[1:]:
        value = value * x + coefficient
    print(value)
    """, ["5", "1", "13", "-3"], 0,
    "Горнер для 2x³ - 3x² + 1 при x = 2: 2 → 2·2 - 3 = 1 → 1·2 + 0 = 2 → 2·2 + 1 = 5.",
    "ЛР6 (схема Горнера)", verify="2*2**3 - 3*2**2 + 1")
th(T, "Яка умова while правильна для «рахувати, поки не досягнуто точності eps»?",
   ["while abs(current - previous) >= eps:", "while abs(current - previous) < eps:",
    "while current - previous >= eps:", "while current == previous:"], 0,
   "Умова while - заперечення умови зупинки. Зупиняємось, коли різниця < eps, отже продовжуємо, "
   "поки >= eps. Без abs цикл зупиниться, якщо наближення спадають (різниця відʼємна).",
   "Лекція 7; UNI2 тема 7")
th(T, "Бісекція на [a, b]: c = (a + b) / 2 і f(a)·f(c) < 0. Що далі?",
   ["корінь на [a, c], тому b = c", "корінь на [c, b], тому a = c", "c - точний корінь",
    "треба змінити ε"], 0,
   "Різні знаки на кінцях [a, c] означають, що f перетинає нуль між a і c. Тому правий кінець "
   "переносимо в c.", "Лекція 7")
th(T, "У методі хорд один кінець відрізка нерухомий. Який?",
   ["той, де знак f збігається зі знаком f''", "завжди лівий a", "той, де |f| більше",
    "середина відрізка"], 0,
   "Так написано в ЛР6 і лекції 7: нерухомий кінець - де f і f'' одного знака.",
   "ЛР6; UNI2 тема 7")

# ======================================================== 9. Списки
T = "Списки"
out(T, """
    first = [1, 2]
    second = first
    second.append(3)
    print(first)
    """, ["[1, 2, 3]", "[1, 2]", "[3]", "None"], 0,
    "second = first - не копія, а друге імʼя того самого списку. Копія - first.copy() або first[:].",
    "Лекція 8")
out(T, """
    matrix = [[0] * 2] * 2
    matrix[0][0] = 5
    print(matrix)
    """, ["[[5, 0], [5, 0]]", "[[5, 0], [0, 0]]", "[[5, 5], [0, 0]]", "[[5, 5], [5, 5]]"], 0,
    "[[0] * 2] * 2 - два посилання на ОДИН рядок. Правильно: [[0] * 2 for _ in range(2)].",
    "Лекція 8")
out(T, """
    values = [10, 20, 30, 40, 50]
    print(values[1:4])
    """, ["[20, 30, 40]", "[10, 20, 30, 40]", "[20, 30, 40, 50]", "[20, 30]"], 0,
    "Індекси 1, 2, 3; кінець зрізу (4) не входить.", "Лекція 8")
out(T, """
    values = [10, 20, 30, 40, 50]
    print(values[::-2])
    """, ["[50, 30, 10]", "[10, 30, 50]", "[50, 40]", "[40, 20]"], 0,
    "Крок -2 з кінця: 50, 30, 10.", "Лекція 8")
out(T, """
    result = [3, 1, 2].append(4)
    print(result)
    """, ["None", "[3, 1, 2, 4]", "4", "[4]"], 0,
    "append змінює список і повертає None. Тому result = список.append(...) - типова помилка.",
    "Лекція 8")
out(T, "print([x * x for x in range(6) if x % 2])", ["[1, 9, 25]", "[0, 4, 16]",
                                                     "[1, 4, 9, 16, 25]", "[0, 1, 4, 9, 16, 25]"], 0,
    "x % 2 дає 1 (True) для непарних: 1, 3, 5 → квадрати 1, 9, 25.", "Лекція 8")
out(T, """
    values = [5, 3, 8]
    values.sort()
    print(values[-1] - values[0])
    """, ["5", "3", "-5", "0"], 0,
    "Після sort: [3, 5, 8]. Останній мінус перший = 8 - 3 = 5.",
    "Лекція 8", verify="Max(5, 3, 8) - Min(5, 3, 8)")
out(T, """
    values = [3, 1, 2]
    sorted(values)
    print(values)
    """, ["[3, 1, 2]", "[1, 2, 3]", "None", "[2, 1, 3]"], 0,
    "sorted повертає НОВИЙ список і не міняє values. Результат тут нікуди не присвоєно.",
    "Лекція 9")

# ======================================================== 10. Кортежі
T = "Кортежі і сортування"
out(T, "print(type((5)), type((5,)))", ["<class 'int'> <class 'tuple'>",
                                        "<class 'tuple'> <class 'tuple'>",
                                        "<class 'int'> <class 'int'>",
                                        "<class 'tuple'> <class 'int'>"], 0,
    "(5) - просто 5 у дужках. Кортеж з одного елемента робить кома: (5,).", "Лекція 2; лекція 9")
out(T, """
    first, second = 1, 2
    first, second = second, first + second
    print(first, second)
    """, ["2 3", "2 4", "1 3", "2 2"], 0,
    "Спершу рахується вся права частина (2, 1 + 2), потім присвоєння: 2 3.", "Лекція 9")
out(T, 'print(sorted(["bb", "a", "ccc"], key=len))', ["['a', 'bb', 'ccc']",
                                                      "['ccc', 'bb', 'a']",
                                                      "['a', 'ccc', 'bb']", "[1, 2, 3]"], 0,
    "key=len - сортує за довжиною, а виводить самі рядки.", "Лекція 9")
out(T, 'print(sorted([("Олег", 80), ("Анна", 95), ("Борис", 80)], key=lambda r: (-r[1], r[0])))',
    ["[('Анна', 95), ('Борис', 80), ('Олег', 80)]",
     "[('Анна', 95), ('Олег', 80), ('Борис', 80)]",
     "[('Борис', 80), ('Олег', 80), ('Анна', 95)]",
     "[('Олег', 80), ('Борис', 80), ('Анна', 95)]"], 0,
    "-r[1] - бал за спаданням; при рівних балах r[0] - імʼя за алфавітом: Борис раніше за Олега.",
    S_U + "9")
out(T, "print(sum(1 for x in [12, 0, 7, 15, 21] if x % 3 == 0))", ["4", "48", "3", "5"], 0,
    "Генератор-вираз дає 1 за кожне кратне 3: 12, 0, 15, 21 - чотири (0 теж ділиться на 3). "
    "48 - це сума самих чисел.", S_U + "9")

# ======================================================== 11. Помилки в коді
T = "Помилки в коді"
EXC = ["TypeError", "ValueError", "IndexError", "KeyError", "NameError", "ZeroDivisionError",
       "SyntaxError", "IndentationError"]


def exc_opts(right, wrong):
    return [right] + wrong


err(T, 'age = 18\nprint("Вік: " + age)', exc_opts("TypeError", ["ValueError", "NameError",
                                                                "нічого, виведе Вік: 18"]), 0,
    "Рядок + число не означено. Треба f\"Вік: {age}\" або str(age).", S_L2)
err(T, 'number = int("12.5")', exc_opts("ValueError", ["TypeError", "нічого, number = 12",
                                                       "SyntaxError"]), 0,
    "int() з рядка вміє лише цілі. Для \"12.5\" спершу float(), потім int().", S_NO)
err(T, "values = [1, 2, 3]\nprint(values[3])", exc_opts("IndexError", ["KeyError",
                                                                       "нічого, виведе 3",
                                                                       "TypeError"]), 0,
    "Індекси 0, 1, 2. Останній - values[2] або values[-1].", "Лекція 8")
err(T, 'ages = {"Ann": 18}\nprint(ages["Bob"])', exc_opts("KeyError", ["IndexError", "нічого, виведе None",
                                                                      "NameError"]), 0,
    "Ключа нема. Без помилки - ages.get(\"Bob\") (дасть None) або ages.get(\"Bob\", 0).", S_NO)
err(T, "total = 5\nprint(totl)", exc_opts("NameError", ["SyntaxError", "нічого, виведе 5",
                                                       "TypeError"]), 0,
    "Змінної totl не існує - опечатка. Синтаксично рядок правильний, помилка виникає під час виконання.",
    S_NO)
err(T, "point = (1, 2)\npoint[0] = 5", exc_opts("TypeError", ["IndexError", "нічого, point = (5, 2)",
                                                             "ValueError"]), 0,
    "Кортеж незмінний. Треба створити новий: point = (5, point[1]).", "Лекція 9")
err(T, "x = 3\nif x > 0 print(x)", exc_opts("SyntaxError", ["IndentationError", "нічого, виведе 3",
                                                          "NameError"]), 0,
    "Після умови if потрібна двокрапка, а тіло - з нового рядка з відступом.", S_U + "3")
err(T, "def get_one():\nreturn 1", exc_opts("IndentationError", ["SyntaxError (бракує дужок)",
                                                                 "нічого", "NameError"]), 0,
    "Тіло функції мусить мати відступ 4 пробіли. IndentationError - окремий вид SyntaxError.",
    S_L2)
err(T, "count = 0\nprint(10 / count)", exc_opts("ZeroDivisionError", ["ValueError", "нічого, виведе 0",
                                                                     "нічого, виведе inf"]), 0,
    "Ділення на нуль. Перевіряють заздалегідь або ловлять try / except ZeroDivisionError.", S_NO)

# ======================================================== 12. PEP 8 і лінтери
T = "PEP 8 і лінтери"
th(T, "Яка назва змінної відповідає PEP 8 і вимогам викладача?",
   ["last_digit", "lastDigit", "d", "LastDigit"], 0,
   "PEP 8: snake_case для змінних. Викладач окремо забороняв однолітерні a, b, d. camelCase - "
   "стиль Java, не Python.", S_REQ)
th(T, "Яка рекомендована PEP 8 найбільша довжина рядка коду?",
   ["79 символів", "120 символів", "60 символів", "без обмеження"], 0,
   "79 символів (docstring 72). Викладач казав: 88-100 ще приймуть, понад 100 - ні.", S_L2)
th(T, "Скільки порожніх рядків PEP 8 вимагає між функціями верхнього рівня?",
   ["2", "1", "0", "3"], 0, "Два порожні рядки між функціями і класами, один - між методами в класі.",
   S_L2, keep=True)
th(T, "Який інструмент перевіряє, чи код дотримується своїх анотацій типів?",
   ["mypy", "black", "pycodestyle", "doctest"], 0,
   "mypy знаходить, наприклад, порівняння str з int (забули int(input())). black лише форматує, "
   "pycodestyle - стиль.", S_L2)
th(T, "Який інструмент сам переформатовує файл під стандарт?",
   ["black", "flake8", "mypy", "pycodestyle"], 0,
   "black переписує файл. flake8, pycodestyle і mypy лише повідомляють про проблеми.", S_L2)
th(T, "Що з цього порушує PEP 8? (кілька відповідей)",
   ["result=a+b", "list = [1, 2, 3]", "def CalcSum(values):", "MAX_SIZE = 100"], [0, 1, 2],
   "result=a+b - нема пробілів навколо операторів; list - вбудоване імʼя; CalcSum - не snake_case. "
   "MAX_SIZE - правильний запис константи.", S_L2, kind="multi")
th(T, "Скільки пробілів - один рівень відступу за PEP 8?",
   ["4", "2", "1 табуляція", "8"], 0, "4 пробіли. Табуляцію з пробілами не змішувати.", S_L2)
th(T, "Що з цього викладач вимагає в кожній лабі? (кілька відповідей)",
   ["функція повертає результат через return", "назва і doctest із заготовки не змінені",
    "проходять усі doctest", "кожна функція друкує результат через print"], [0, 1, 2],
   "Повертати, а не друкувати; заготовку не міняти; лаба зарахована, коли пройшли всі doctest.",
   S_REQ, kind="multi")
th(T, "Що таке DRY?",
   ["не повторювати той самий код, а винести його у функцію", "писати коментар до кожного рядка",
    "уникати циклів", "спершу тести, потім код"], 0,
   "Don't Repeat Yourself. «Спершу тести» - це Test Driven Development.", S_L2)

# ======================================================== 13. doctest
T = "doctest"
dt(T, '''
    def greet():
        """
        >>> greet()
        Hello
        """
        return "Hello"
    ''', ["ні: функція повертає рядок, і doctest чекає 'Hello' у лапках", "так",
          "ні: у doctest не можна викликати функцію без аргументів", "так, якщо додати print"], 0,
   "Doctest порівнює так, як показав би інтерпретатор: рядок - у лапках, 'Hello'.", S_L2, 1,
   "Чи пройде цей doctest?")
dt(T, '''
    def square(number):
        """
        >>> square(3)
        9
        """
        print(number * number)
    ''', ["так, бо doctest порівнює те, що зʼявилось на екрані, - але викладач не прийме: треба return",
          "ні, бо функція повертає None", "ні, бо print заборонений у функціях",
          "так, і це правильний розвʼязок"], 0,
   "Doctest бачить вивід 9 і тест проходить. Але функція повертає None, і square(3) + 1 впаде. "
   "Вимога викладача - return.", S_REQ, 0, "Чи пройде цей doctest?")
dt(T, '''
    def add_tenths():
        """
        >>> add_tenths()
        0.3
        """
        return 0.1 + 0.2
    ''', ["ні: насправді 0.30000000000000004", "так", "ні: SyntaxError", "так, бо 0.1 + 0.2 = 0.3"], 0,
   "Дійсні числа в двійковому записі неточні. У doctest пишуть round(..., 6) або порівнюють з допуском.",
   S_U + "3", 1, "Чи пройде цей doctest?")
dt(T, '''
    def count_digits(number):
        """
        >>> count_digits(123)
        3
        >>> count_digits(7)
        1
        >>> count_digits(0)
        1
        """
        digits_count = 0
        while number > 0:
            number //= 10
            digits_count += 1
        return digits_count
    ''', ["1", "0", "2", "3"], 0,
   "Для 0 цикл не виконується жодного разу і повертається 0, а тест чекає 1. Граничний випадок "
   "(edge case) - саме те, що ловлять doctest. Правильно - починати з 1 і ділити, поки >= 10.",
   S_U + "4", 1, "Скільки з трьох doctest НЕ пройдуть?")
th(T, "Як doctest вирішує, що тест пройдено?",
   ["виконує рядок після >>> і порівнює вивід з наступним рядком як ТЕКСТ",
    "перевіряє лише, що функція не впала", "порівнює числа з допуском 1 %",
    "перевіряє анотації типів"], 0,
   "Порівняння текстове: зайвий пробіл або лапки - і тест не пройдено.", S_L2)
th(T, "Знайшов помилку в doctest викладача (тест чекає неправильне число). Що робити?",
   ["порахувати вручну і показати викладачу, код не підганяти", "змінити doctest під свій код",
    "підігнати код, щоб видавав очікуване", "видалити цей тест"], 0,
   "Викладачі самі просили надсилати знайдені помилки в doctest. Doctest без дозволу не міняти.",
   S_REQ)
th(T, "Що таке Test Driven Development?",
   ["спершу пишуть тести, потім код, який їх проходить", "код пишуть без тестів",
    "тести пише інша людина після здачі", "тестують лише вручну"], 0,
   "У лабах doctest уже написані до коду - це і є TDD. Читай doctest першими.", S_L2)

# ======================================================== 14. Складність
T = "Складність і кількість кроків"
out(T, """
    number = 10 ** 6
    steps = 0
    divisor = 1
    while divisor * divisor <= number:
        steps += 1
        divisor += 1
    print(steps)
    """, ["1000", "1000000", "500000", "999"], 0,
    "Перебір до √n: √10⁶ = 1000 кроків замість мільйона.",
    S_U + "5", verify="floor(sqrt(10**6))")
out(T, """
    number = 97
    steps = 0
    divisor = 2
    while divisor * divisor <= number:
        steps += 1
        divisor += 1
    print(steps)
    """, ["8", "9", "95", "48"], 0,
    "divisor = 2..9 (9·9 = 81 ≤ 97, 10·10 = 100 > 97) - 8 кроків. Простим 97 оголосять після них.",
    S_U + "5", verify="floor(sqrt(97)) - 1")
out(T, """
    size = 10
    operations = 0
    for row in range(size):
        for column in range(size):
            operations += 1
    print(operations)
    """, ["100", "20", "10", "55"], 0,
    "Два вкладені цикли по n дають n² кроків. Для матриці n×n це нормально, для пошуку - повільно.",
    "Лекція 8", verify="10**2")
out(T, """
    number = 1024
    steps = 0
    while number > 1:
        number //= 2
        steps += 1
    print(steps)
    """, ["10", "512", "11", "1024"], 0,
    "Ділення навпіл: 2¹⁰ = 1024, тобто 10 кроків. Так само швидкі бісекція і двійковий пошук.",
    "Лекція 9", verify="log(1024, 2)")
out(T, """
    first, second = 21, 13
    steps = 0
    while second != 0:
        first, second = second, first % second
        steps += 1
    print(steps)
    """, ["6", "13", "21", "2"], 0,
    "(21, 13) → (13, 8) → (8, 5) → (5, 3) → (3, 2) → (2, 1) → (1, 0): 6 кроків. Сусідні числа "
    "Фібоначчі - найгірший випадок для Евкліда, але навіть так кроків мало.", S_U + "5")
th(T, "Зондування кроком eps = 10⁻⁶ на [2, 3] і бісекція з тим самим eps. Що швидше?",
   ["бісекція: близько 20 кроків проти близько 10⁵ - 10⁶ кроків зондування",
    "зондування, бо воно простіше", "однаково", "бісекція повільніша, бо рахує середину"], 0,
   "Бісекція ділить відрізок навпіл: log₂(1/10⁻⁶) ≈ 20. Зондування йде кроком eps до кореня - "
   "у прикладі ЛР6 це 94551 крок.", "ЛР6; UNI2 тема 7")

# ======================================================== 15. Matplotlib
T = "Matplotlib"
th(T, "Що означає plt.subplot(3, 1, 2)?",
   ["сітка 3 рядки на 1 стовпчик, малюємо в 2-й графік", "3 графіки по 1 точці, крок 2",
    "графік розміром 3 на 1 дюйм, номер 2", "2 рядки, 1 стовпчик, 3-й графік"], 0,
   "subplot(рядки, стовпчики, номер). Так у ЛР3 три графіки один під одним.", "ЛР3 (умова)")
th(T, "Яку функцію взяти для графіка збіжності, де похибка спадає в мільйони разів?",
   ["plt.semilogy", "plt.bar", "plt.scatter", "plt.axhline"], 0,
   "semilogy - логарифмічна вісь y: на звичайній осі видно лише перші кроки.", "ЛР6 (умова)")

# ======================================================== 16. Рядки, словники, винятки
T = "Рядки, словники, винятки"
out(T, """
    counts = {"a": 1}
    counts["a"] += 1
    counts["b"] = 5
    print(len(counts), counts["a"])
    """, ["2 2", "3 2", "2 1", "KeyError"], 0,
    "Ключ \"a\" вже був - змінили значення на 2; \"b\" - новий ключ. Ключів 2.", S_NO)
out(T, 'print({"x": 1}.get("y", 0))', ["0", "None", "KeyError", "1"], 0,
    "get повертає друге значення, якщо ключа нема, і не кидає KeyError.", S_NO)
out(T, "print(len({1, 2, 2, 3}))", ["3", "4", "2", "TypeError"], 0,
    "Множина зберігає кожне значення один раз: {1, 2, 3}.", S_NO)
out(T, """
    try:
        number = int("abc")
    except ValueError:
        print("помилка")
    else:
        print("ок")
    """, ["помилка", "ок", "помилка / ок", "ValueError"], 0,
    "int(\"abc\") кидає ValueError, його перехоплює except. else виконується лише без помилки.", S_NO)
out(T, 'print("Python"[1:4])', ["yth", "Pyt", "ytho", "ython"], 0,
    "Зрізи рядків - як у списків: індекси 1, 2, 3.", S_NO)
out(T, 'print("-".join(["1", "2", "3"]))', ["1-2-3", "-1-2-3-", "['1', '2', '3']", "123"], 0,
    "Рядок перед .join ставиться МІЖ елементами.", S_NO)


# ======================================================== перевірка zadachi.md
def check_zadachi():
    text = (UNIT / "zadachi.md").read_text(encoding="utf-8")
    n_tasks = len(re.findall(r"^### Задача \d+", text, flags=re.M))
    blocks = re.findall(r"```python\n(.*?)```", text, flags=re.S)
    tries_all = fails_all = 0
    bad = []
    for i, block in enumerate(blocks, 1):
        try:
            tries, failed = doctest_result(block)
        except Exception as e:  # noqa: BLE001
            bad.append(f"блок {i}: не виконується: {type(e).__name__}: {e}")
            continue
        if tries == 0:
            bad.append(f"блок {i}: нема жодного doctest")
        if failed:
            bad.append(f"блок {i}: впало {failed} з {tries} doctest")
        tries_all += tries
        fails_all += failed
    return n_tasks, len(blocks), tries_all, fails_all, bad


def main():
    n_tasks, n_blocks, tries, fails, bad = check_zadachi()
    if n_tasks < 20:
        bad.append(f"задач лише {n_tasks}, треба 20+")
    if ERRORS or bad:
        print("ПОМИЛКИ:")
        for e in ERRORS + bad:
            print("  ", e)
        return 1
    raw = json.dumps({"questions": QS}, ensure_ascii=False, indent=1)
    for pat in ["$$", "\\frac", "\\sqrt", "begin{", "\\(", "\\[", chr(0x2014), chr(0x2013)]:
        assert pat not in raw, pat
    for f in UNIT.glob("*.md"):
        t = f.read_text(encoding="utf-8")
        for pat in ["$$", "\\frac", "\\sqrt", "begin{", "\\(", "\\[", chr(0x2014), chr(0x2013)]:
            assert pat not in t, (f.name, pat)
    (UNIT / "quiz.json").write_text(raw + "\n", encoding="utf-8")
    ncalc = sum(1 for q in QS if q.get("calc"))
    nexec = sum(1 for q in QS if "pre" in q)
    topics = []
    for q in QS:
        if q["topic"] not in topics:
            topics.append(q["topic"])
    print(f"prog: питань {len(QS)}, з них з кодом (exec/doctest-перевірка) {nexec}, calc з verify {ncalc}")
    print(f"prog: тем {len(topics)}: {', '.join(topics)}")
    print(f"prog: zadachi.md - {n_tasks} задач, {n_blocks} блоків коду, {tries} doctest, падінь {fails}")
    return 0


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    sys.exit(main())
