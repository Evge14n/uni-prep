# Задачі: напиши безпечну функцію

10 задач, по одній на тему. У кожній - заготовка з doctest: функція поки що `pass`, тому перевірка червона.
Допиши функцію так, щоб усі приклади пройшли. Кнопка «doctest -v» під кодом перевіряє прямо тут,
на ПК - `python3 файл.py` (у кінці файлу вже стоїть запуск doctest).

<div class="pybox" id="pybox"></div>

Як працювати: 1) прочитай умову і приклади (приклади - це і є вимоги); 2) натисни «Змінити», напиши код;
3) «doctest -v»; 4) розвʼязок відкривай лише після двох своїх спроб.

## Задача 1. Безпечне читання числа (тема 1)

Функція `read_int(text, low, high)` повертає ціле число з рядка, якщо воно в межах `low..high` (межі включно).
Якщо рядок не число або число поза межами - `None`. Функція ніколи не падає. `eval` не можна.

```python
"""Задача 1. Безпечне читання числа."""
import doctest


def read_int(text, low, high):
    """Ціле з рядка в межах low..high або None.

    >>> read_int("42", 0, 100)
    42
    >>> read_int(" 7 ", 0, 10)
    7
    >>> read_int("100", 0, 100)
    100
    >>> read_int("101", 0, 100) is None
    True
    >>> read_int("abc", 0, 100) is None
    True
    >>> read_int("", 0, 100) is None
    True
    >>> read_int("2+2", 0, 100) is None
    True
    """
    pass


if __name__ == "__main__":
    doctest.testmod(verbose=True)
```

<details markdown="1"><summary>Розвʼязок (відкривай лише після 2 своїх спроб)</summary>

```python
"""Задача 1. Безпечне читання числа. Розвʼязок."""
import doctest


def read_int(text, low, high):
    """Ціле з рядка в межах low..high або None.

    >>> read_int("42", 0, 100)
    42
    >>> read_int(" 7 ", 0, 10)
    7
    >>> read_int("100", 0, 100)
    100
    >>> read_int("101", 0, 100) is None
    True
    >>> read_int("abc", 0, 100) is None
    True
    >>> read_int("", 0, 100) is None
    True
    >>> read_int("2+2", 0, 100) is None
    True
    """
    try:
        value = int(text)
    except ValueError:
        return None
    if low <= value <= high:
        return value
    return None


if __name__ == "__main__":
    doctest.testmod(verbose=True)
```

Чому так: `int("2+2")` кидає `ValueError` - рядок не рахується як вираз (на відміну від `eval`). Межі перевіряємо
після перетворення, бо до нього це ще рядок.

</details>

## Задача 2. Пошук без SQL-інʼєкції (тема 2)

Функція `find_secret(con, name)` повертає секрет користувача з таблиці `users` або `None`, якщо такого нема.
Запит - лише з параметром `?`. Базу для прикладів робить готова функція `make_db()`.

```python
"""Задача 2. Пошук без SQL-інʼєкції."""
import doctest
import sqlite3


def make_db():
    con = sqlite3.connect(":memory:")
    con.execute("CREATE TABLE users (name TEXT, secret TEXT)")
    con.executemany("INSERT INTO users VALUES (?, ?)",
                    [("anna", "s-111"), ("bob", "s-222")])
    return con


def find_secret(con, name):
    """Секрет користувача name або None.

    >>> con = make_db()
    >>> find_secret(con, "anna")
    's-111'
    >>> find_secret(con, "bob")
    's-222'
    >>> find_secret(con, "ira") is None
    True
    >>> find_secret(con, "nobody' OR '1'='1") is None
    True
    """
    pass


if __name__ == "__main__":
    doctest.testmod(verbose=True)
```

<details markdown="1"><summary>Розвʼязок (відкривай лише після 2 своїх спроб)</summary>

```python
"""Задача 2. Пошук без SQL-інʼєкції. Розвʼязок."""
import doctest
import sqlite3


def make_db():
    con = sqlite3.connect(":memory:")
    con.execute("CREATE TABLE users (name TEXT, secret TEXT)")
    con.executemany("INSERT INTO users VALUES (?, ?)",
                    [("anna", "s-111"), ("bob", "s-222")])
    return con


def find_secret(con, name):
    """Секрет користувача name або None.

    >>> con = make_db()
    >>> find_secret(con, "anna")
    's-111'
    >>> find_secret(con, "bob")
    's-222'
    >>> find_secret(con, "ira") is None
    True
    >>> find_secret(con, "nobody' OR '1'='1") is None
    True
    """
    row = con.execute("SELECT secret FROM users WHERE name = ?",
                      (name,)).fetchone()
    if row is None:
        return None
    return row[0]


if __name__ == "__main__":
    doctest.testmod(verbose=True)
```

Чому так: `fetchone()` дає один рядок-кортеж `('s-111',)` або `None`. Останній приклад - перевірка, що
інʼєкція не спрацювала: з f-рядком там повернувся б секрет `anna`.

</details>

## Задача 3. Файл лише зі своєї теки (тема 5)

Функція `safe_join(base, name)` повертає повний шлях (`Path`) до файлу `name` усередині теки `base`.
Якщо після зведення шлях виходить за `base` - `ValueError("вихід за межі теки")`.

```python
"""Задача 3. Файл лише зі своєї теки."""
import doctest
from pathlib import Path


def safe_join(base, name):
    """Шлях до name всередині base, або ValueError.

    >>> safe_join("/srv/files", "a/b.txt").name
    'b.txt'
    >>> safe_join("/srv/files", "x/../c.txt").name
    'c.txt'
    >>> safe_join("/srv/files", "../secret.txt")
    Traceback (most recent call last):
        ...
    ValueError: вихід за межі теки
    >>> safe_join("/srv/files", "/etc/passwd")
    Traceback (most recent call last):
        ...
    ValueError: вихід за межі теки
    """
    pass


if __name__ == "__main__":
    doctest.testmod(verbose=True)
```

<details markdown="1"><summary>Розвʼязок (відкривай лише після 2 своїх спроб)</summary>

```python
"""Задача 3. Файл лише зі своєї теки. Розвʼязок."""
import doctest
from pathlib import Path


def safe_join(base, name):
    """Шлях до name всередині base, або ValueError.

    >>> safe_join("/srv/files", "a/b.txt").name
    'b.txt'
    >>> safe_join("/srv/files", "x/../c.txt").name
    'c.txt'
    >>> safe_join("/srv/files", "../secret.txt")
    Traceback (most recent call last):
        ...
    ValueError: вихід за межі теки
    >>> safe_join("/srv/files", "/etc/passwd")
    Traceback (most recent call last):
        ...
    ValueError: вихід за межі теки
    """
    root = Path(base).resolve()
    path = (root / name).resolve()
    if not path.is_relative_to(root):
        raise ValueError("вихід за межі теки")
    return path


if __name__ == "__main__":
    doctest.testmod(verbose=True)
```

Чому так: `resolve()` прибирає `..` і робить шлях повним, а `is_relative_to` перевіряє, що він починається з теки.
Перевірка «чи є в рядку `..`» не ловить `/etc/passwd`.

</details>

## Задача 4. Лише свої нотатки (тема 3)

`get_note(notes, user, note_id)` повертає текст нотатки, якщо вона існує і її власник - `user`.
Інакше - `PermissionError("нема доступу")` (однаково і для чужої, і для неіснуючої).

```python
"""Задача 4. Лише свої нотатки."""
import doctest

NOTES = {
    1: {"owner": "anna", "text": "покупки"},
    2: {"owner": "bob", "text": "пароль від Wi-Fi"},
}


def get_note(notes, user, note_id):
    """Текст своєї нотатки або PermissionError.

    >>> get_note(NOTES, "anna", 1)
    'покупки'
    >>> get_note(NOTES, "bob", 2)
    'пароль від Wi-Fi'
    >>> get_note(NOTES, "anna", 2)
    Traceback (most recent call last):
        ...
    PermissionError: нема доступу
    >>> get_note(NOTES, "anna", 99)
    Traceback (most recent call last):
        ...
    PermissionError: нема доступу
    """
    pass


if __name__ == "__main__":
    doctest.testmod(verbose=True)
```

<details markdown="1"><summary>Розвʼязок (відкривай лише після 2 своїх спроб)</summary>

```python
"""Задача 4. Лише свої нотатки. Розвʼязок."""
import doctest

NOTES = {
    1: {"owner": "anna", "text": "покупки"},
    2: {"owner": "bob", "text": "пароль від Wi-Fi"},
}


def get_note(notes, user, note_id):
    """Текст своєї нотатки або PermissionError.

    >>> get_note(NOTES, "anna", 1)
    'покупки'
    >>> get_note(NOTES, "bob", 2)
    'пароль від Wi-Fi'
    >>> get_note(NOTES, "anna", 2)
    Traceback (most recent call last):
        ...
    PermissionError: нема доступу
    >>> get_note(NOTES, "anna", 99)
    Traceback (most recent call last):
        ...
    PermissionError: нема доступу
    """
    note = notes.get(note_id)
    if note is None or note["owner"] != user:
        raise PermissionError("нема доступу")
    return note["text"]


if __name__ == "__main__":
    doctest.testmod(verbose=True)
```

Чому так: `notes.get(...)` не падає на неіснуючому номері. Одна й та сама відповідь для «чужої» і «нема» не
підказує, які номери існують.

</details>

## Задача 5. Оцінки з ліміту (тема 4)

`parse_scores(text)` розбирає рядок оцінок через кому: `"90,75,82"` → `[90, 75, 82]`. Правила:
довше 200 символів - `ValueError("задовгий ввід")`; більше 20 чисел - `ValueError("забагато оцінок")`;
кожна оцінка 0..100, інакше `ValueError("погана оцінка")`. Довжину перевір ДО `split`.

```python
"""Задача 5. Оцінки з ліміту."""
import doctest

MAX_LEN = 200
MAX_ITEMS = 20


def parse_scores(text):
    """Список оцінок з рядка через кому, з лімітами.

    >>> parse_scores("90,75,82")
    [90, 75, 82]
    >>> parse_scores("100")
    [100]
    >>> parse_scores("9" * 300)
    Traceback (most recent call last):
        ...
    ValueError: задовгий ввід
    >>> parse_scores(",".join(["5"] * 21))
    Traceback (most recent call last):
        ...
    ValueError: забагато оцінок
    >>> parse_scores("90,abc")
    Traceback (most recent call last):
        ...
    ValueError: погана оцінка
    >>> parse_scores("90,101")
    Traceback (most recent call last):
        ...
    ValueError: погана оцінка
    """
    pass


if __name__ == "__main__":
    doctest.testmod(verbose=True)
```

<details markdown="1"><summary>Розвʼязок (відкривай лише після 2 своїх спроб)</summary>

```python
"""Задача 5. Оцінки з ліміту. Розвʼязок."""
import doctest

MAX_LEN = 200
MAX_ITEMS = 20


def parse_scores(text):
    """Список оцінок з рядка через кому, з лімітами.

    >>> parse_scores("90,75,82")
    [90, 75, 82]
    >>> parse_scores("100")
    [100]
    >>> parse_scores("9" * 300)
    Traceback (most recent call last):
        ...
    ValueError: задовгий ввід
    >>> parse_scores(",".join(["5"] * 21))
    Traceback (most recent call last):
        ...
    ValueError: забагато оцінок
    >>> parse_scores("90,abc")
    Traceback (most recent call last):
        ...
    ValueError: погана оцінка
    >>> parse_scores("90,101")
    Traceback (most recent call last):
        ...
    ValueError: погана оцінка
    """
    if len(text) > MAX_LEN:
        raise ValueError("задовгий ввід")
    parts = text.split(",")
    if len(parts) > MAX_ITEMS:
        raise ValueError("забагато оцінок")
    scores = []
    for part in parts:
        try:
            score = int(part)
        except ValueError:
            raise ValueError("погана оцінка") from None
        if not 0 <= score <= 100:
            raise ValueError("погана оцінка")
        scores.append(score)
    return scores


if __name__ == "__main__":
    doctest.testmod(verbose=True)
```

Чому так: `int("abc")` сам кидає `ValueError`, але з іншим текстом - ловимо і кидаємо свій, зрозумілий.
`from None` ховає першу помилку з виводу.

</details>

## Задача 6. Завантаження лише з дозволених сайтів (тема 8)

`is_allowed_url(url, allowed)` - `True`, лише якщо схема `https` і хост рівно один з множини `allowed`.
Розбирати адресу через `urlparse`, а не `startswith` чи `in` (дивись приклади з `@` і `.evil.net`).
Функція ніколи не падає.

```python
"""Задача 6. Завантаження лише з дозволених сайтів."""
import doctest
from urllib.parse import urlparse

ALLOWED = {"example.com", "img.example.com"}


def is_allowed_url(url, allowed):
    """True лише для https і хоста зі списку allowed.

    >>> is_allowed_url("https://example.com/cat.png", ALLOWED)
    True
    >>> is_allowed_url("https://img.example.com/a.jpg", ALLOWED)
    True
    >>> is_allowed_url("http://example.com/cat.png", ALLOWED)
    False
    >>> is_allowed_url("https://example.com.evil.net/x", ALLOWED)
    False
    >>> is_allowed_url("https://example.com@evil.net/x", ALLOWED)
    False
    >>> is_allowed_url("https://127.0.0.1/admin", ALLOWED)
    False
    >>> is_allowed_url("not a url", ALLOWED)
    False
    >>> is_allowed_url("https://[abc/x", ALLOWED)
    False
    """
    pass


if __name__ == "__main__":
    doctest.testmod(verbose=True)
```

<details markdown="1"><summary>Розвʼязок (відкривай лише після 2 своїх спроб)</summary>

```python
"""Задача 6. Завантаження лише з дозволених сайтів. Розвʼязок."""
import doctest
from urllib.parse import urlparse

ALLOWED = {"example.com", "img.example.com"}


def is_allowed_url(url, allowed):
    """True лише для https і хоста зі списку allowed.

    >>> is_allowed_url("https://example.com/cat.png", ALLOWED)
    True
    >>> is_allowed_url("https://img.example.com/a.jpg", ALLOWED)
    True
    >>> is_allowed_url("http://example.com/cat.png", ALLOWED)
    False
    >>> is_allowed_url("https://example.com.evil.net/x", ALLOWED)
    False
    >>> is_allowed_url("https://example.com@evil.net/x", ALLOWED)
    False
    >>> is_allowed_url("https://127.0.0.1/admin", ALLOWED)
    False
    >>> is_allowed_url("not a url", ALLOWED)
    False
    >>> is_allowed_url("https://[abc/x", ALLOWED)
    False
    """
    try:
        parts = urlparse(url)
    except ValueError:
        return False
    return parts.scheme == "https" and parts.hostname in allowed


if __name__ == "__main__":
    doctest.testmod(verbose=True)
```

Чому так: у `https://example.com@evil.net/x` частина до `@` - це «імʼя користувача», а справжній хост - `evil.net`.
`url.startswith("https://example.com")` тут сказав би «так». `urlparse(...).hostname` бере саме хост.
А на зламаній адресі (`https://[abc/x`) `urlparse` сам кидає `ValueError` - ловимо і відмовляємо (fail closed).

</details>

## Задача 7. Коментар без XSS (тема 9)

`render_comment(author, text)` повертає HTML `<p><b>автор</b>: текст</p>`, де і автор, і текст екрановані
`html.escape`.

```python
"""Задача 7. Коментар без XSS."""
import doctest
import html


def render_comment(author, text):
    """HTML коментаря з екрануванням.

    >>> render_comment("anna", "привіт")
    '<p><b>anna</b>: привіт</p>'
    >>> render_comment("<i>bob</i>", "<script>alert(1)</script>")
    '<p><b>&lt;i&gt;bob&lt;/i&gt;</b>: &lt;script&gt;alert(1)&lt;/script&gt;</p>'
    >>> render_comment("ira", 'a "b" & c')
    '<p><b>ira</b>: a &quot;b&quot; &amp; c</p>'
    """
    pass


if __name__ == "__main__":
    doctest.testmod(verbose=True)
```

<details markdown="1"><summary>Розвʼязок (відкривай лише після 2 своїх спроб)</summary>

```python
"""Задача 7. Коментар без XSS. Розвʼязок."""
import doctest
import html


def render_comment(author, text):
    """HTML коментаря з екрануванням.

    >>> render_comment("anna", "привіт")
    '<p><b>anna</b>: привіт</p>'
    >>> render_comment("<i>bob</i>", "<script>alert(1)</script>")
    '<p><b>&lt;i&gt;bob&lt;/i&gt;</b>: &lt;script&gt;alert(1)&lt;/script&gt;</p>'
    >>> render_comment("ira", 'a "b" & c')
    '<p><b>ira</b>: a &quot;b&quot; &amp; c</p>'
    """
    return f"<p><b>{html.escape(author)}</b>: {html.escape(text)}</p>"


if __name__ == "__main__":
    doctest.testmod(verbose=True)
```

Чому так: екранувати треба ВСЕ, що прийшло від користувача, і імʼя теж. `html.escape` міняє `<` `>` `&` `"` `'`.

</details>

## Задача 8. Одноразовий код (теми 5 і 9)

`new_code()` повертає 6-значний код з цифр (може починатися з 0) через `secrets`, не `random`.
`check_code(given, expected)` порівнює через `hmac.compare_digest` і не падає на будь-якому вводі (навіть кирилиці).

```python
"""Задача 8. Одноразовий код."""
import doctest
import hmac
import secrets


def new_code():
    """6 випадкових цифр рядком.

    >>> c = new_code()
    >>> len(c), c.isdigit()
    (6, True)
    >>> len({new_code() for _ in range(50)}) > 40
    True
    """
    pass


def check_code(given, expected):
    """Чи збігається код, порівняння за сталий час.

    >>> check_code("012345", "012345")
    True
    >>> check_code("012346", "012345")
    False
    >>> check_code("", "012345")
    False
    >>> check_code("абвгде", "012345")
    False
    """
    pass


if __name__ == "__main__":
    doctest.testmod(verbose=True)
```

<details markdown="1"><summary>Розвʼязок (відкривай лише після 2 своїх спроб)</summary>

```python
"""Задача 8. Одноразовий код. Розвʼязок."""
import doctest
import hmac
import secrets


def new_code():
    """6 випадкових цифр рядком.

    >>> c = new_code()
    >>> len(c), c.isdigit()
    (6, True)
    >>> len({new_code() for _ in range(50)}) > 40
    True
    """
    return f"{secrets.randbelow(10**6):06d}"


def check_code(given, expected):
    """Чи збігається код, порівняння за сталий час.

    >>> check_code("012345", "012345")
    True
    >>> check_code("012346", "012345")
    False
    >>> check_code("", "012345")
    False
    >>> check_code("абвгде", "012345")
    False
    """
    return hmac.compare_digest(given.encode(), expected.encode())


if __name__ == "__main__":
    doctest.testmod(verbose=True)
```

Чому так: `secrets.randbelow(10**6)` дає 0..999999, а `:06d` доповнює нулями зліва (`42` → `000042`).
Другий приклад `new_code` - що коди справді різні: 50 кодів з мільйона майже ніколи не повторюються
(ймовірність хоча б одного збігу ≈ 0,1 %, а щоб різних було лише 40, треба 10 збігів - практично неможливо).
`.encode()` - бо рядки з кирилицею `compare_digest` не бере (кидає `TypeError`), а байти - будь-які.
І головне про такі коди: варіантів лише мільйон, тому справжній захист - ліміт спроб (тема 4), строк дії
(кілька хвилин) і «використав - код згорів».

</details>

## Задача 9. Помилка без витоку (тема 6)

`safe_call(func, log)` викликає `func()`. Якщо все добре - повертає `("ok", результат)`.
Якщо виняток - дописує в список `log` назву типу помилки і повертає `("error", "Сталася помилка")`.
Деталей помилки користувач не бачить.

```python
"""Задача 9. Помилка без витоку."""
import doctest


def safe_call(func, log):
    """Виклик func з короткою відповіддю на помилку.

    >>> log = []
    >>> safe_call(lambda: 2 + 2, log)
    ('ok', 4)
    >>> safe_call(lambda: 1 / 0, log)
    ('error', 'Сталася помилка')
    >>> safe_call(lambda: int("x"), log)
    ('error', 'Сталася помилка')
    >>> log
    ['ZeroDivisionError', 'ValueError']
    """
    pass


if __name__ == "__main__":
    doctest.testmod(verbose=True)
```

<details markdown="1"><summary>Розвʼязок (відкривай лише після 2 своїх спроб)</summary>

```python
"""Задача 9. Помилка без витоку. Розвʼязок."""
import doctest


def safe_call(func, log):
    """Виклик func з короткою відповіддю на помилку.

    >>> log = []
    >>> safe_call(lambda: 2 + 2, log)
    ('ok', 4)
    >>> safe_call(lambda: 1 / 0, log)
    ('error', 'Сталася помилка')
    >>> safe_call(lambda: int("x"), log)
    ('error', 'Сталася помилка')
    >>> log
    ['ZeroDivisionError', 'ValueError']
    """
    try:
        return ("ok", func())
    except Exception as e:
        log.append(type(e).__name__)
        return ("error", "Сталася помилка")


if __name__ == "__main__":
    doctest.testmod(verbose=True)
```

Чому так: `except Exception` ловить звичайні помилки, але не `KeyboardInterrupt` (Ctrl+C) - так і треба.
У справжній програмі в лог іде весь `traceback.format_exc()`, тут лише назва, щоб приклад був коротким.

</details>

## Задача 10. Сортування зі списку дозволених (тема 10)

`top_names(con, column)` повертає імена з таблиці `marks`, відсортовані за колонкою `column` за спаданням.
Назву колонки параметром `?` не передаси, тому - лише `"name"` або `"mark"`, інакше `ValueError("не можна")`.

```python
"""Задача 10. Сортування зі списку дозволених."""
import doctest
import sqlite3

ALLOWED = {"name", "mark"}


def make_db():
    con = sqlite3.connect(":memory:")
    con.execute("CREATE TABLE marks (name TEXT, mark INTEGER)")
    con.executemany("INSERT INTO marks VALUES (?, ?)",
                    [("anna", 90), ("bob", 75), ("ira", 82)])
    return con


def top_names(con, column):
    """Імена за спаданням column; column лише зі списку ALLOWED.

    >>> con = make_db()
    >>> top_names(con, "mark")
    ['anna', 'ira', 'bob']
    >>> top_names(con, "name")
    ['ira', 'bob', 'anna']
    >>> top_names(con, "mark; DROP TABLE marks")
    Traceback (most recent call last):
        ...
    ValueError: не можна
    >>> top_names(con, "mark")
    ['anna', 'ira', 'bob']
    """
    pass


if __name__ == "__main__":
    doctest.testmod(verbose=True)
```

<details markdown="1"><summary>Розвʼязок (відкривай лише після 2 своїх спроб)</summary>

```python
"""Задача 10. Сортування зі списку дозволених. Розвʼязок."""
import doctest
import sqlite3

ALLOWED = {"name", "mark"}


def make_db():
    con = sqlite3.connect(":memory:")
    con.execute("CREATE TABLE marks (name TEXT, mark INTEGER)")
    con.executemany("INSERT INTO marks VALUES (?, ?)",
                    [("anna", 90), ("bob", 75), ("ira", 82)])
    return con


def top_names(con, column):
    """Імена за спаданням column; column лише зі списку ALLOWED.

    >>> con = make_db()
    >>> top_names(con, "mark")
    ['anna', 'ira', 'bob']
    >>> top_names(con, "name")
    ['ira', 'bob', 'anna']
    >>> top_names(con, "mark; DROP TABLE marks")
    Traceback (most recent call last):
        ...
    ValueError: не можна
    >>> top_names(con, "mark")
    ['anna', 'ira', 'bob']
    """
    if column not in ALLOWED:
        raise ValueError("не можна")
    rows = con.execute(f"SELECT name FROM marks ORDER BY {column} DESC")
    return [row[0] for row in rows]


if __name__ == "__main__":
    doctest.testmod(verbose=True)
```

Чому так: f-рядок тут безпечний лише тому, що `column` уже перевірено - це точно `"name"` або `"mark"`.
Останній приклад показує, що таблиця після спроби на місці. (SQLite і так не виконав би два запити через `;`,
але в `ORDER BY` можна вставити підзапит - тому перевірка списком обовʼязкова.)

</details>
