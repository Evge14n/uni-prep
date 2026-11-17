# Програмування + безпека: теорія

Принцип: кожну тему Python вчу одразу з її стороною безпеки. Більшість дірок береться не з «хакерства»,
а з того, як написаний звичайний код: склеїв рядок, не перевірив ввід, показав помилку.

<div class="pybox" id="pybox"></div>

Як читати кожну тему: **що треба з Python** → **де діра** (код «погано», його можна запустити) →
**як правильно** (код «добре») → **типова помилка** → де це в списку OWASP Top 10:2025 (головний список
ризиків вебзастосунків, https://top10.owasp.org/2025/).

> Усі приклади - на своїх іграшкових даних у браузері. «Перевіряти» чужі сайти чи сервери без письмового
> дозволу власника не можна: це може бути злочином (зокрема ст. 361 Кримінального кодексу України -
> несанкціоноване втручання в роботу інформаційних систем). Учимось писати код, який не ламається.

Код під кожним прикладом можна запустити кнопкою «Запустити» і змінити кнопкою «Змінити». Вивід під кодом
перевірено запуском (Python 3.13 на ПК і Python 3.13 у браузері; приклад з argon2 - лише на ПК).

## Тема 1. Ввід користувача

**Що треба з Python:** `input()` завжди повертає рядок. `int("17")` дає 17, а `int("abc")` кидає `ValueError`.
`try/except` ловить помилку. `eval(рядок)` виконує рядок як код Python.

**Де діра 1: програма падає на будь-якому «неправильному» вводі.** Для сервера це означає, що один
запит зупиняє обробку.

```python
text = "abc"          # уяви, що це прийшло з input()
age = int(text)
print("Через рік тобі", age + 1)
```

```text
Traceback (most recent call last):
  File "<код>", line 2
    age = int(text)
ValueError: invalid literal for int() with base 10: 'abc'
```

**Як правильно:** перевірити і тип, і межі. Не впевнений - повертаєш «нема значення», а не падаєш.

```python
def read_age(text):
    try:
        age = int(text)
    except ValueError:
        return None          # не число
    if not 0 <= age <= 130:
        return None          # число, але неможливе
    return age


for t in ["17", "abc", "", "-5", "999", " 18 "]:
    print(repr(t), "->", read_age(t))
```

```text
'17' -> 17
'abc' -> None
'' -> None
'-5' -> None
'999' -> None
' 18 ' -> 18
```

Зверни увагу: `int(" 18 ")` пробіли по краях прощає, а от `int("1 8")` - ні. Ще `int()` приймає
`"+18"` і `"1_8"` (це 18) - тому межі після перетворення перевіряти обовʼязково.

**Де діра 2: `eval` виконує ввід як код.** Хотів калькулятор, а користувач ввів не число, а імʼя змінної:

```python
secret = "пароль-123"
user_text = "secret"     # користувач ввів не число
print(eval(user_text))
```

```text
пароль-123
```

Програма віддала те, що мала тримати в собі. Так само через `eval` можна викликати будь-яку функцію,
навіть видалення файлів. **Правило: ніколи `eval(ввід)` і `exec(ввід)`.**

**Як правильно:** якщо треба число - `int()` / `float()`. Якщо треба список чи словник з тексту -
спершу `json.loads`. Якщо саме синтаксис Python - `ast.literal_eval` (приймає лише літерали: числа, рядки,
списки, словники), але з лімітом довжини і ловити кілька помилок: на `"1+"` він кидає `SyntaxError`, а не
`ValueError`, а на дуже глибоких дужках може закінчитись памʼять.

```python
import ast

print(ast.literal_eval("[1, 2, 3]"))
try:
    ast.literal_eval("secret")
except (ValueError, SyntaxError) as e:
    print("відмова:", type(e).__name__)
```

```text
[1, 2, 3]
відмова: ValueError
```

**Типова помилка:** перевіряти ввід лише в браузері (JavaScript-форма). Запит можна надіслати й без форми,
тому перевірка завжди на сервері, у Python.

OWASP: A05 Injection (eval - це інʼєкція коду, CWE-95).

## Тема 2. Рядки й інʼєкції

**Що треба з Python:** f-рядок `f"... {x} ..."` просто вставляє текст. Python не знає, що цей рядок потім
стане командою для бази даних чи терміналу.

**Де діра:** ввід ліпиться в команду, і користувач міняє сенс команди. Приклад - SQL-запит до бази
(SQLite є в Python, `import sqlite3`). Створюємо свою іграшкову базу в памʼяті:

```python
import sqlite3

con = sqlite3.connect(":memory:")
con.execute("CREATE TABLE users (name TEXT, secret TEXT)")
con.executemany("INSERT INTO users VALUES (?, ?)",
                [("anna", "s-111"), ("bob", "s-222")])

name = "nobody' OR '1'='1"      # ввід користувача
sql = f"SELECT name, secret FROM users WHERE name = '{name}'"
print(sql)
print(con.execute(sql).fetchall())
```

```text
SELECT name, secret FROM users WHERE name = 'nobody' OR '1'='1'
[('anna', 's-111'), ('bob', 's-222')]
```

Лапка у вводі закрила рядок, і `OR '1'='1'` (завжди правда) стало частиною запиту. Запит віддав
секрети всіх. Це **SQL-інʼєкція**.

**Як правильно: дані окремо від команди.** У запиті ставиш `?`, а значення передаєш другим аргументом.
База отримує їх як дані і ніколи не виконує як код.

```python
import sqlite3

con = sqlite3.connect(":memory:")
con.execute("CREATE TABLE users (name TEXT, secret TEXT)")
con.executemany("INSERT INTO users VALUES (?, ?)",
                [("anna", "s-111"), ("bob", "s-222")])

name = "nobody' OR '1'='1"
rows = con.execute("SELECT name, secret FROM users WHERE name = ?",
                   (name,)).fetchall()
print(rows)
print(con.execute("SELECT secret FROM users WHERE name = ?",
                  ("anna",)).fetchall())
```

```text
[]
[('s-111',)]
```

Користувача з іменем `nobody' OR '1'='1` нема - і запит чесно повертає порожній список.
Зверни увагу на кому в `(name,)`: це кортеж з одного елемента.

**Command-інʼєкція - те саме з командою терміналу.** Склеїв команду рядком і віддав у shell:

```python
host = "example.com; echo ЗЛАМАНО"     # ввід користувача
cmd = "ping -c 1 " + host
print(cmd)
```

```text
ping -c 1 example.com; echo ЗЛАМАНО
```

Shell бачить `;` і виконує ДВІ команди. Правильно: `subprocess.run(["ping", "-c", "1", host])` - список
аргументів без `shell=True`, тоді `host` лишається одним аргументом, а не командою. Але аргумент усе ще
може бути опцією: `host = "--help"` ping прочитає як ключ (це argument injection). Тому ще й перевірити,
що `host` схожий на імʼя хоста: лише літери, цифри, крапки, дефіс, і НЕ починається з дефісу.

**Типова помилка:** «екранувати лапки самому» (`name.replace("'", "")`). Завжди знайдеться обхід;
параметри (`?`) - єдиний надійний спосіб.

OWASP: A05 Injection (SQL - CWE-89, команди ОС - CWE-78).

## Тема 3. Функції й доступ

**Що треба з Python:** функція отримує аргументи і може кинути виняток `raise PermissionError(...)`.
Перевірки - на самому початку функції.

**Три правила:**
1. **Перевіряй вхід на початку функції** (тип, межі, хто питає).
2. **Fail closed:** не впевнений - забороняй. Помилка під час перевірки = відмова, не дозвіл.
3. **Найменші права:** функція робить лише своє (функція «показати нотатку» не вміє видаляти).

**Де діра: IDOR** (Insecure Direct Object Reference). Нотатки лежать за номером, і функція віддає будь-яку
нотатку за номером, не дивлячись, чия вона:

```python
notes = {
    1: {"owner": "anna", "text": "мій список покупок"},
    2: {"owner": "bob", "text": "пароль від Wi-Fi"},
}


def get_note_bad(user, note_id):
    return notes[note_id]["text"]


print(get_note_bad("anna", 1))
print(get_note_bad("anna", 2))     # anna поміняла номер у запиті
```

```text
мій список покупок
пароль від Wi-Fi
```

**Як правильно:** перевірити власника. Якщо нотатки нема або вона чужа - однакова відмова
(щоб не підказувати, які номери існують).

```python
notes = {
    1: {"owner": "anna", "text": "мій список покупок"},
    2: {"owner": "bob", "text": "пароль від Wi-Fi"},
}


def get_note(user, note_id):
    note = notes.get(note_id)
    if note is None or note["owner"] != user:
        raise PermissionError("нема доступу")
    return note["text"]


print(get_note("anna", 1))
for nid in (2, 99):
    try:
        get_note("anna", nid)
    except PermissionError as e:
        print(nid, "->", e)
```

```text
мій список покупок
2 -> нема доступу
99 -> нема доступу
```

**Fail open - як НЕ треба:**

```python
def is_admin_bad(user, admins):
    try:
        return user in admins
    except Exception:
        return True          # перевірка зламалась - пускаємо (погано!)


def is_admin(user, admins):
    try:
        return user in admins
    except Exception:
        return False         # зламалась - не пускаємо


print(is_admin_bad("anna", None), is_admin("anna", None))
```

```text
True False
```

`"anna" in None` кидає `TypeError`. Погана функція з цього зробила «так, адмін».

Дрібниця на потім: `PermissionError` - це різновид `OSError` (помилок файлів), тож `except OSError` поруч його
проковтне. У великій програмі для відмови в доступі роблять свій клас: `class AccessDenied(Exception): ...`.

OWASP: A01 Broken Access Control (IDOR - CWE-639), A10 Mishandling of Exceptional Conditions (fail open - CWE-636).

## Тема 4. Списки, цикли, ліміти

**Що треба з Python:** `len()`, `split()`, цикл `for`. Памʼять і час компʼютера скінченні.

**Де діра:** цикл чи список по вводу без обмеження. Хтось надішле рядок на 100 МБ або мільйон чисел -
програма зʼїсть памʼять і процесор, і сервіс перестане відповідати всім. Це відмова в обслуговуванні (DoS).

**Як правильно:** межа на вході, ДО будь-якої роботи.

```python
MAX_TEXT = 1000
MAX_ITEMS = 100


def parse_numbers(text):
    if len(text) > MAX_TEXT:
        raise ValueError("задовгий ввід")
    parts = text.split(",")
    if len(parts) > MAX_ITEMS:
        raise ValueError("забагато чисел")
    return [int(p) for p in parts]


print(parse_numbers("1,2,3"))
for t in ["1," * 199 + "1", "9" * 5000]:
    try:
        parse_numbers(t)
    except ValueError as e:
        print(len(t), "символів ->", e)
```

```text
[1, 2, 3]
399 символів -> забагато чисел
5000 символів -> задовгий ввід
```

Інші місця, де потрібна межа: розмір файлу, який завантажують; кількість спроб входу (інакше перебір
паролів); глибина рекурсії; регулярні вирази з вкладеними `(a+)+` на довгому вводі (можуть працювати
дуже довго, це називають ReDoS).

**Типова помилка:** перевірити довжину ПІСЛЯ того, як усе вже прочитав і розібрав. Межа має стояти
до роботи.

OWASP: окремої категорії в Top 10:2025 для цього нема (CWE-400 «неконтрольоване споживання ресурсів» і CWE-770
«ресурси без ліміту» не значаться в жодній з 10). Але це класична відмова в обслуговуванні - ліміт ставлять завжди.

## Тема 5. Файли й секрети

**Що треба з Python:** `open(шлях)`, модуль `pathlib`: `Path("a") / "b"`, `.resolve()` (зводить `..` і
дає повний шлях), `.is_relative_to(тека)` (Python 3.9+).

**Де діра: path traversal.** Сайт віддає файли з теки за іменем від користувача: `open("files/" + name)`.
Користувач передає `../` і виходить з теки, наприклад `../../etc/passwd` на Linux.

**Як правильно:** звести шлях і перевірити, що він досі всередині дозволеної теки.

```python
from pathlib import Path

BASE = Path("/srv/files").resolve()


def is_safe(name):
    p = (BASE / name).resolve()
    return p.is_relative_to(BASE)


for name in ["notes.txt", "sub/../notes.txt", "../secret.txt",
             "../../etc/passwd", "/etc/passwd"]:
    print(name, "->", is_safe(name))
```

```text
notes.txt -> True
sub/../notes.txt -> True
../secret.txt -> False
../../etc/passwd -> False
/etc/passwd -> False
```

Зверни увагу на останній: `Path("/srv/files") / "/etc/passwd"` дає просто `/etc/passwd` - абсолютний
шлях «перебиває» теку. Тому перевіряти треба результат, а не шукати `..` у рядку.
Ще надійніше - не брати імʼя файлу від користувача взагалі, а зберігати файли під своїми номерами.

**Секрети (паролі, ключі API, токени):**
- ніколи не писати в код: код потрапляє в git, на GitHub, до всіх, хто його бачить;
- тримати в змінних оточення або у файлі `.env`, а `.env` дописати в `.gitignore`;
- `.env` Python сам НЕ читає: потрібен пакет `python-dotenv` (`from dotenv import load_dotenv`, потім
  `load_dotenv()`), тоді значення зʼявляться в `os.environ`;
- читати так:

```python
import os

key = os.environ.get("UNIPREP_DEMO_KEY")
if key is None:
    print("ключ не задано - працюю без нього")
```

```text
ключ не задано - працюю без нього
```

- випадкові паролі й токени - лише модуль `secrets`, не `random` (`random` передбачуваний, він для ігор і симуляцій):

```python
import secrets

token = secrets.token_urlsafe(32)    # 32 випадкові байти
print(len(token))
```

```text
43
```

Якщо секрет уже потрапив у git - видалити файл замало (він лишається в історії). Ключ треба
**замінити на новий** (відкликати старий).

OWASP: A01 Broken Access Control (path traversal - CWE-22), A07 Authentication Failures (пароль у коді - CWE-798),
A04 Cryptographic Failures (слабкий випадковий генератор - CWE-338).

## Тема 6. Помилки

**Що треба з Python:** `try/except`, модуль `traceback`, `logging`.

**Де діра:** показати користувачу весь стектрейс. Там шляхи до файлів, версії бібліотек, шматки SQL -
готова карта для того, хто шукає діру.

**Як правильно:** користувачу - коротко і з номером, повний текст - у свій журнал (лог).

```python
import traceback

LOG = []                       # журнал; у справжній програмі - logging у файл


def handle(request_id, func):
    try:
        return func()
    except Exception:
        LOG.append(traceback.format_exc())
        return f"Сталася помилка (код {request_id}). Спробуй пізніше."


print(handle(7, lambda: 1 / 0))
print(len(LOG), "запис у журналі, останній рядок:",
      LOG[0].strip().splitlines()[-1])
```

```text
Сталася помилка (код 7). Спробуй пізніше.
1 запис у журналі, останній рядок: ZeroDivisionError: division by zero
```

Інші правила:
- не ловити все підряд `except:` і мовчки йти далі - помилка зникає, а дані лишаються напівзмінені;
- у вебі вимкнути режим налагодження на сервері (`DEBUG = False` у Django, `debug=False` у Flask);
- у журнал не писати паролі й токени.

OWASP: A10 Mishandling of Exceptional Conditions (CWE-209 - витік деталей у помилці), A02 Security Misconfiguration (debug на сервері).

## Тема 7. Залежності (pip)

**Що треба з Python:** `pip install пакет`, віртуальне оточення `python3 -m venv .venv`, файл `requirements.txt`.

**Де діра:**
- у старій версії бібліотеки є відома діра - вразливість з номером CVE, а ти її не оновив;
- підробка: пакет з назвою, схожою на справжню (`reqeusts` замість `requests`) - це називають typosquatting;
- атака на ланцюг постачання: зламали самого автора пакета, і шкідлива версія приходить «оновленням».

**Як правильно:**
- ставити лише потрібне; назву брати з документації чи репозиторію проєкту, а на pypi.org звірити автора,
  посилання на репозиторій, дату і кількість завантажень (підробка теж лежить на pypi.org);
- пакет, який порадив ШІ, перевірити так само: ШІ іноді вигадує назви, а зловмисники реєструють
  пакети з такими вигаданими назвами;
- фіксувати версії в `requirements.txt` (`requests==2.32.4`), кожен проєкт - у своєму venv;
- перевіряти на відомі дірки програмою **pip-audit** (від PyPA, тих, хто робить pip):

```bash
pip install pip-audit
pip-audit                      # перевірити те, що встановлено у venv
pip-audit -r requirements.txt  # перевірити файл залежностей
```

Перевірено 17.11.2026 (pip-audit 2.10.0): для `requests==2.19.0` він видав PYSEC-2018-28 (виправлено в 2.20.0),
PYSEC-2023-74 (виправлено в 2.31.0) і ще кілька. Пастка: команди `pip audit` (з пробілом) у pip нема - pip 25.1.1
на ПК відповів `ERROR: unknown command "audit"`. Правильно - з дефісом, окрема програма.

OWASP: A03 Software Supply Chain Failures (нова назва в 2025, раніше «вразливі й застарілі компоненти»).

## Тема 8. Веб-запити й SSRF

**Що треба з Python:** `urllib.parse.urlparse(url)` розбирає адресу на схему, хост, порт; модуль `ipaddress`
каже, чи адреса приватна.

**Правила для запитів:**
- лише `https://` (TLS шифрує і перевіряє, що сервер справжній); не вимикати перевірку сертифіката
  (`verify=False` у бібліотеці requests);
- секрети не в URL (URL пишеться в логи і історію браузера) - у заголовку;
- завжди ставити `timeout` (інакше один повільний сервер підвішує твою програму).

**Де діра: SSRF** (Server-Side Request Forgery). Сервер вміє «завантажити картинку за посиланням». Користувач
дає не картинку, а внутрішню адресу: `http://127.0.0.1:...` (сам сервер), `http://169.254.169.254/` (службові
дані хмари, там бувають ключі доступу), `http://192.168.0.1/` (роутер у мережі).

**Як правильно:** дозволяти лише потрібне (краще список дозволених доменів); не ходити на приватні адреси.

```python
import ipaddress
from urllib.parse import urlparse


def is_safe_url(url):
    try:
        u = urlparse(url)
    except ValueError:
        return False             # urlparse теж падає на смітті
    if u.scheme != "https" or not u.hostname:
        return False
    try:
        ip = ipaddress.ip_address(u.hostname)
    except ValueError:
        return True              # не IP у звичайному записі - текстом не перевірити
    return ip.is_global


for url in ["https://example.com/cat.png", "http://example.com/",
            "https://127.0.0.1/admin", "https://169.254.169.254/",
            "https://192.168.0.1/", "file:///etc/passwd"]:
    print(url, "->", is_safe_url(url))
```

```text
https://example.com/cat.png -> True
http://example.com/ -> False
https://127.0.0.1/admin -> False
https://169.254.169.254/ -> False
https://192.168.0.1/ -> False
file:///etc/passwd -> False
```

**Пастка:** ця перевірка дивиться лише на текст адреси. Вона пропустить `https://localhost/`, `https://127.1/`
і `https://2130706433/` - а система все одно перетворить їх на `127.0.0.1`. Імʼя домену теж може вести на
`127.0.0.1`, а сервер може відповісти перенаправленням на внутрішню адресу. Тому в справжньому сервісі перевіряють IP **після** того,
як імʼя перетворили на адресу, вимикають автоматичні перенаправлення або пускають такі запити через
окремий проксі. Найнадійніше - список дозволених доменів.

OWASP: A01 Broken Access Control (у 2025 SSRF входить сюди, CWE-918), A04 Cryptographic Failures (без TLS).

## Тема 9. Веб-застосунок (OWASP)

**Автентифікація** - хто ти (логін). **Авторизація** - що тобі можна (див. тему 3, IDOR).

**XSS** (cross-site scripting): ввід користувача потрапляє на сторінку як HTML і виконується як JavaScript
у браузері ІНШИХ людей. Збережений XSS - коли текст зберігся (коментар) і показується всім.

```python
import html

comment = "<script>alert(1)</script>"     # «коментар» користувача
print("<p>" + comment + "</p>")             # погано
print("<p>" + html.escape(comment) + "</p>")  # добре
```

```text
<p><script>alert(1)</script></p>
<p>&lt;script&gt;alert(1)&lt;/script&gt;</p>
```

Після `html.escape` браузер показує текст як текст. Це працює для тексту в HTML і для атрибута в лапках,
але не для посилань: `href="javascript:..."` екранування не рятує - у посиланнях від користувача пускай лише
схему `https`. Шаблонізатори (Jinja2 у Flask, шаблони Django) екранують
самі - не вимикай це (`|safe`, `Markup`) для вводу користувача.

**CSRF:** чужий сайт змушує твій браузер надіслати запит на сайт, де ти залогінений (браузер сам додає твої
cookie). Захист: CSRF-токен у формах (у Django і Flask-WTF є готовий), cookie з `SameSite=Lax`, зміни лише через POST.

**Паролі:** ніколи не зберігати відкрито і не «шифрувати». Зберігати **хеш повільною функцією з сіллю**.
OWASP Password Storage Cheat Sheet: перший вибір Argon2id (мінімум 19 МіБ памʼяті, 2 ітерації, 1 потік),
якщо його нема - scrypt, bcrypt - лише для старих систем (і він бере лише перші 72 байти пароля). Звичайний SHA-256 для паролів -
**ні**: він швидкий, відеокарта перебирає мільярди за секунду.

```python
# не запускати: у браузері нема argon2-cffi - запускай у терміналі на ПК
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError

ph = PasswordHasher()   # типово 64 МіБ, 3 ітерації, 4 потоки - вище за мінімум OWASP
stored = ph.hash("мій-пароль")      # це й зберігаємо в базі
print(stored[:9])                   # $argon2id
print(ph.verify(stored, "мій-пароль"))
try:
    ph.verify(stored, "не-той")
except VerifyMismatchError:
    print("неправильний пароль")
```

```text
$argon2id
True
неправильний пароль
```

**Порівняння секретів** (токен, код з листа) - `hmac.compare_digest(a, b)`, а не `a == b`: звичайне `==` зупиняється
на першій різниці, і за часом відповіді можна вгадувати символи по одному. Рядки `compare_digest` бере лише
латинські (ASCII): на `"абв"` він кидає `TypeError`, тому для вводу користувача порівнюй байти - `.encode()`.

```python
import hmac

print(hmac.compare_digest(b"abc123", b"abc123"), hmac.compare_digest("абв".encode(), b"abc123"))
```

```text
True False
```

OWASP: A05 Injection (XSS - CWE-79), A01 (CSRF - CWE-352), A07 Authentication Failures, A04 Cryptographic Failures (слабкий хеш пароля - CWE-916).

## Тема 10. База даних

**Головне:** лише параметризовані запити (`?` у SQLite, `%s` у psycopg для PostgreSQL), ніколи f-рядок чи `+`.
Увага: `%s` у psycopg - це мітка, значення йде ДРУГИМ аргументом `execute(sql, (name,))`. А оператор Python
`"... %s" % name` - це знову склеювання рядка, тобто діра.

**Пастка: параметром можна передати лише ЗНАЧЕННЯ.** Назву колонки чи таблиці (`ORDER BY колонка`) параметром не
передаси. Тоді - лише вибір зі списку дозволених:

```python
import sqlite3

con = sqlite3.connect(":memory:")
con.execute("CREATE TABLE marks (name TEXT, mark INTEGER)")
con.executemany("INSERT INTO marks VALUES (?, ?)",
                [("anna", 90), ("bob", 75), ("ira", 82)])

ALLOWED = {"name", "mark"}


def top(order_by):
    if order_by not in ALLOWED:
        raise ValueError("так сортувати не можна")
    return con.execute(f"SELECT name FROM marks ORDER BY {order_by}").fetchall()


print(top("mark"))
try:
    top("mark; DROP TABLE marks")
except ValueError as e:
    print(e)
```

```text
[('bob',), ('ira',), ('anna',)]
так сортувати не можна
```

Тут f-рядок безпечний лише тому, що `order_by` - точно одне зі слів списку. (SQLite і так не виконає два
запити через `;`, але в `ORDER BY` можна вставити підзапит, тому перевірка списком - обовʼязкова.)

**Найменші права:** програма заходить у базу користувачем, який може лише те, що їй треба (читати і писати
свої таблиці), а не адміном бази. Тоді інʼєкція не зможе видалити таблиці чи дістатись до інших баз - хоча
дані своїх таблиць усе одно під загрозою. Права зменшують шкоду, а не замінюють параметри.

**Ще:** резервні копії бази (і перевірка, що з них можна відновитись), паролі - хешем (тема 9),
особисті дані - лише ті, що справді потрібні.

OWASP: A05 Injection (CWE-89), A02 Security Misconfiguration (зайві права).

## Тренажер (на ПК)

Є окремий тренажер з локальною моделлю на ПК (дає задачу з вимогою безпеки і перевіряє рішення, працює
без інтернету). На сайті його нема - він живе лише на компʼютері.

## Джерела

- OWASP Top 10:2025 - https://top10.owasp.org/2025/ (категорії A01-A10; номери CWE звірено зі списками «Mapped CWEs» сторінок категорій 17.11.2026).
- OWASP Password Storage Cheat Sheet - https://cheatsheetseries.owasp.org/cheatsheets/Password_Storage_Cheat_Sheet.html (Argon2id 19 МіБ / 2 / 1).
- Документація Python: `sqlite3` (розділ про placeholders - «How to use placeholders to bind values in SQL queries»),
  `secrets`, `hmac.compare_digest`, `html.escape`, `ast.literal_eval`, `pathlib.PurePath.is_relative_to`.
- pip-audit (PyPA) - https://github.com/pypa/pip-audit (запуск 17.11.2026, версія 2.10.0).
- CWE (каталог типів дірок) - https://cwe.mitre.org/ (номери біля кожної теми).
- Кримінальний кодекс України, ст. 361 «Несанкціоноване втручання в роботу інформаційних (автоматизованих), електронних
  комунікаційних, інформаційно-комунікаційних систем, електронних комунікаційних мереж» - https://zakon.rada.gov.ua/laws/show/2341-14
