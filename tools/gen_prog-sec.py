"""Генератор тестів розділу «Python + безпека» (prog-sec, UPROGSEC1) -> content/prog-sec/quiz.json.

  python -X utf8 -P -E tools/gen_prog-sec.py           # записати quiz.json
  python -X utf8 -P -E tools/gen_prog-sec.py --check   # перевірити, що quiz.json = цьому файлу

Питання ps-001..ps-015 - з контенту «_вхідне/uni-prep-prog-sec» (17.11), виправлені (індекс відповіді,
pip-audit з дефісом, точніші формулювання); id не змінено (бот бере картки за id).
Питання з полем run: код запускається тут так само, як у браузері (tools/check_progsec.py), і правильний
варіант МУСИТЬ дорівнювати виводу, а жоден інший - ні. Код показується в питанні полем pre.
"""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from check_progsec import norm, run_like_browser  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "content" / "prog-sec" / "quiz.json"

T1, T2, T3, T4, T5 = "Ввід користувача", "Інʼєкції (SQL, команди)", "Доступ: IDOR і fail closed", "Ліміти (DoS)", "Файли й секрети"
T6, T7, T8, T9, T10 = "Помилки", "Залежності (pip)", "Веб-запити й SSRF", "Веб: XSS, CSRF, паролі", "База даних"
T0 = "OWASP Top 10:2025"
OW = "OWASP Top 10:2025, https://top10.owasp.org/2025/"

Q = [
    # ---- 1-15: з вхідного контенту, виправлені ----
    dict(id="ps-001", topic=T1, type="single",
         q="Чому int(input()) без перевірки - погана ідея?",
         options=["Повільно працює", "На буквах чи порожньому вводі кидає ValueError, і програма падає",
                  "Займає багато памʼяті", "Не працює на Linux"], answer=1,
         explain="Будь-який ввід ззовні треба перевіряти. На не-числі int() кидає ValueError. Правильно: try/except ValueError і перевірка меж (вік 0..130 тощо).",
         src="Теорія, тема 1"),
    dict(id="ps-002", topic=T1, type="single",
         q="Чому eval(input()) - це діра?",
         options=["Повільно рахує", "Виконує як код Python будь-що, що ввів користувач", "Не рахує дроби", "Застарів у Python 3"],
         answer=1,
         explain="eval виконує рядок як код: можна прочитати змінні програми (eval(\"secret\")) або викликати будь-яку функцію. Ніколи не давай ввід у eval/exec. Для чисел - int()/float(), для списків - json.loads або ast.literal_eval.",
         src="Теорія, тема 1; CWE-95 (A05 Injection)"),
    dict(id="ps-003", topic=T2, type="single",
         q="Що таке SQL-інʼєкція простими словами?",
         options=["Помилка в базі даних", "Ввід користувача вклеюється в SQL-запит і міняє його сенс",
                  "Повільний запит", "Втрата зʼєднання з базою"], answer=1,
         explain="Якщо запит склеєно з вводом (f-рядок, +), лапка у вводі закриває рядок, і дописане (напр. ' OR '1'='1) стає частиною запиту. Рятує параметризований запит (?).",
         src="Теорія, теми 2 і 10; CWE-89 (A05 Injection)"),
    dict(id="ps-004", topic=T2, type="short",
         q="Одним словом: як правильно передавати дані в SQL-запит, щоб не було інʼєкції? (через ...)",
         answer="параметри",
         accept=["параметри", "параметр", "параметрами", "параметром", "через параметри", "параметризований запит",
                 "параметризовані запити", "параметризація", "плейсхолдери", "плейсхолдер", "плейсхолдерами",
                 "підготовлені запити", "prepared statements", "placeholder", "placeholders", "parameters", "bind"],
         explain="Дані йдуть окремо від команди: con.execute(\"... WHERE name = ?\", (name,)). База отримує їх як дані і не виконує як код.",
         src="Теорія, теми 2 і 10; документація Python sqlite3 (placeholders)"),
    dict(id="ps-005", topic=T3, type="single",
         q="Що означає принцип fail closed?",
         options=["Закрити програму при будь-якій помилці", "Якщо не впевнений у праві доступу (чи перевірка зламалась) - забороняй",
                  "Закрити файл після читання", "Ловити всі помилки і йти далі"], answer=1,
         explain="За замовчуванням - заборона. Доступ даємо, лише коли точно перевірили. Протилежне - fail open (CWE-636, A10:2025): перевірка впала, а програма пустила.",
         src="Теорія, тема 3; CWE-636 (A10)"),
    dict(id="ps-006", topic=T3, type="single",
         q="IDOR - це коли...",
         options=["База впала", "Користувач міняє номер (id) у запиті і отримує чужі дані", "Повільний запит", "Немає інтернету"],
         answer=1,
         explain="Insecure Direct Object Reference: сервер віддає обʼєкт за id, але не перевіряє, чий він. Треба перевірка власника на кожен запит.",
         src="Теорія, тема 3; CWE-639 (A01 Broken Access Control)"),
    dict(id="ps-007", topic=T4, type="single",
         q="Чому цикл по вводу користувача без обмеження розміру небезпечний?",
         options=["Некрасивий код", "Величезний ввід зʼїдає памʼять і процесор і кладе сервіс для всіх (DoS)",
                  "Не компілюється", "Повільний інтернет"], answer=1,
         explain="Без ліміту користувач надішле мільйони елементів. Перевіряй довжину і кількість ДО роботи (len(text) > MAX -> відмова).",
         src="Теорія, тема 4; CWE-400"),
    dict(id="ps-008", topic=T5, type="single",
         q="Path traversal - це коли через ../ користувач...",
         options=["Прискорює читання", "Виходить за межі дозволеної теки і читає чужі файли", "Створює теку", "Стискає файл"],
         answer=1,
         explain="open(\"files/\" + name) з name = \"../../etc/passwd\" читає системний файл. Треба (BASE / name).resolve() і перевірка is_relative_to(BASE).",
         src="Теорія, тема 5; CWE-22 (A01)"),
    dict(id="ps-009", topic=T5, type="single",
         q="Де НЕ можна тримати паролі й ключі?",
         options=["У змінних оточення", "У файлі .env, доданому в .gitignore", "Прямо в коді програми", "У менеджері секретів"],
         answer=2,
         explain="Код потрапляє в git і до всіх, хто його бачить. Тримай у змінних оточення / .env (і .env у .gitignore). Пароль у коді - CWE-798 (A07:2025).",
         src="Теорія, тема 5; CWE-798"),
    dict(id="ps-010", topic=T6, type="single",
         q="Чому не можна показувати користувачу повний стектрейс помилки?",
         options=["Некрасиво", "Він показує внутрішню кухню: шляхи, версії, шматки запитів - підказка, де шукати діру",
                  "Повільно", "Займає місце на екрані"], answer=1,
         explain="Користувачу - коротке «сталася помилка (код N)», повний traceback - лише у свій лог. CWE-209 (A10:2025).",
         src="Теорія, тема 6"),
    dict(id="ps-011", topic=T7, type="short",
         q="Як називається програма (команда) від PyPA, що перевіряє встановлені pip-пакети на відомі вразливості?",
         answer="pip-audit",
         accept=["pip-audit", "pip_audit", "python -m pip_audit", "python3 -m pip_audit", "py -m pip_audit", "pip-audit -r requirements.txt"],
         explain="pip-audit (з дефісом) - окрема програма: pip install pip-audit, далі pip-audit або pip-audit -r requirements.txt. Команди «pip audit» з пробілом у pip нема: pip 25.1.1 на ПК відповів ERROR: unknown command \"audit\" (17.11.2026).",
         src="Теорія, тема 7; https://github.com/pypa/pip-audit"),
    dict(id="ps-012", topic=T8, type="single",
         q="SSRF - це коли сервер...",
         options=["Падає від навантаження", "Іде за URL, який дав користувач, і дістає внутрішні ресурси (127.0.0.1, 169.254.169.254)",
                  "Повільно віддає сторінку", "Втрачає сесію"], answer=1,
         explain="Server-Side Request Forgery: «завантаж картинку за посиланням», а посилання веде у внутрішню мережу. Захист - список дозволених хостів. У 2025 SSRF входить в A01 (CWE-918).",
         src="Теорія, тема 8"),
    dict(id="ps-013", topic=T9, type="single",
         q="Збережений XSS трапляється, коли...",
         options=["Сервер повільний", "Текст від користувача зберігся (напр. коментар) і показується іншим без екранування, тож браузер виконує його як код",
                  "На сайті нема HTTPS", "Картинка завелика"], answer=1,
         explain="Вставив <script> у коментар, він зберігся і виконується в браузері кожного, хто відкрив сторінку. Рятує екранування виводу (html.escape, автоекранування шаблонів). CWE-79 (A05).",
         src="Теорія, тема 9"),
    dict(id="ps-014", topic=T9, type="single",
         q="Як правильно зберігати паролі користувачів у базі?",
         options=["Відкритим текстом", "Хешем повільної функції з сіллю (перший вибір OWASP - Argon2id)",
                  "Зашифрувати і тримати ключ поруч", "Хешем SHA-256 без солі"], answer=1,
         explain="Пароль не зберігають ні відкрито, ні «зашифровано». Лише повільний хеш з сіллю: Argon2id (OWASP: мінімум 19 МіБ, 2 ітерації, 1 потік), для старих систем bcrypt. При вході хешують введене і звіряють.",
         src="Теорія, тема 9; OWASP Password Storage Cheat Sheet"),
    dict(id="ps-015", topic=T1, type="short",
         q="Головне правило: усе, що прийшло ззовні (ввід, файл, URL), вважай ... - поки не перевірив. Одне слово.",
         answer="ворожим",
         accept=["ворожим", "вороже", "ворожий", "недовіреним", "небезпечним", "підозрілим", "ненадійним", "шкідливим", "зловмисним"],
         explain="Звідси майже всі дірки: ввід вклеїли в запит, не обмежили розмір, не перевірили шлях.",
         src="Теорія, вступ"),

    # ---- 16+: нові (UPROGSEC1) ----
    dict(id="ps-016", topic=T1, type="single", q="Що виведе цей код?",
         run='print(int(" 18 ") + 1)',
         options=["19", "ValueError", " 18 1", "None"],
         explain="int() прощає пробіли по краях рядка, тож \" 18 \" -> 18, плюс 1 = 19. А от int(\"1 8\") - ValueError.",
         src="Теорія, тема 1; документація Python int()"),
    dict(id="ps-017", topic=T1, type="single", q="Користувач у «калькуляторі» ввів не число, а слово. Що виведе програма?",
         run='secret = "s-777"\nuser_text = "secret"\nprint(eval(user_text))',
         options=["s-777", "secret", "NameError", "SyntaxError"],
         explain="eval виконав рядок \"secret\" як код - це імʼя змінної, і програма віддала її значення. Тому eval(ввід) - ніколи.",
         src="Теорія, тема 1"),
    dict(id="ps-018", topic=T1, type="single", q="Що виведе цей код?",
         run='import ast\ntry:\n    ast.literal_eval("__import__(\'os\')")\n    print("виконано")\nexcept ValueError:\n    print("відмова")',
         options=["відмова", "виконано", "NameError", "None"],
         explain="ast.literal_eval приймає лише літерали (числа, рядки, списки, словники, кортежі). Виклик функції він не виконує, а кидає ValueError.",
         src="Теорія, тема 1; документація Python ast.literal_eval"),
    dict(id="ps-019", topic=T2, type="single", q="Скільки рядків поверне запит?",
         run=('import sqlite3\ncon = sqlite3.connect(":memory:")\ncon.execute("CREATE TABLE users (name TEXT, secret TEXT)")\n'
              'con.executemany("INSERT INTO users VALUES (?, ?)", [("anna", "s-1"), ("bob", "s-2")])\n'
              'name = "nobody\' OR \'1\'=\'1"\n'
              'rows = con.execute(f"SELECT secret FROM users WHERE name = \'{name}\'").fetchall()\nprint(len(rows))'),
         options=["2", "0", "1", "sqlite3.OperationalError"],
         explain="Лапка у вводі закрила рядок, і OR '1'='1' (завжди правда) став частиною запиту - повернулись секрети ВСІХ (2). Це SQL-інʼєкція.",
         src="Теорія, тема 2"),
    dict(id="ps-020", topic=T2, type="single", q="Той самий ввід, але через параметр. Скільки рядків поверне запит?",
         run=('import sqlite3\ncon = sqlite3.connect(":memory:")\ncon.execute("CREATE TABLE users (name TEXT, secret TEXT)")\n'
              'con.executemany("INSERT INTO users VALUES (?, ?)", [("anna", "s-1"), ("bob", "s-2")])\n'
              'name = "nobody\' OR \'1\'=\'1"\n'
              'rows = con.execute("SELECT secret FROM users WHERE name = ?", (name,)).fetchall()\nprint(len(rows))'),
         options=["0", "2", "1", "sqlite3.OperationalError"],
         explain="З параметром увесь ввід - це просто імʼя. Користувача з таким дивним іменем нема, тому 0 рядків.",
         src="Теорія, тема 2"),
    dict(id="ps-021", topic=T2, type="single", q="Який рядок безпечно шукає користувача name у SQLite?",
         options=['con.execute(f"SELECT * FROM users WHERE name = \'{name}\'")',
                  'con.execute("SELECT * FROM users WHERE name = \'" + name + "\'")',
                  'con.execute("SELECT * FROM users WHERE name = ?", (name,))',
                  'con.execute("SELECT * FROM users WHERE name = \'%s\'" % name)'],
         answer=2,
         explain="Лише варіант з ? передає дані окремо від команди. f-рядок, + і % однаково вклеюють текст у запит.",
         src="Теорія, теми 2 і 10"),
    dict(id="ps-022", topic=T2, type="single", q="Забули кому в (name,). Що виведе код?",
         run=('import sqlite3\ncon = sqlite3.connect(":memory:")\ntry:\n    con.execute("SELECT ?", ("ab"))\n    print("ок")\n'
              'except Exception as e:\n    print(type(e).__name__)'),
         options=["ProgrammingError", "ок", "TypeError", "OperationalError"],
         explain="(\"ab\") без коми - це просто рядок, а не кортеж. sqlite3 бере його як послідовність з 2 символів, а місце під значення одне - ProgrammingError «Incorrect number of bindings». Кортеж з одного елемента - (\"ab\",).",
         src="Теорія, тема 2"),
    dict(id="ps-023", topic=T2, type="single", q="Як безпечно запустити ping для хоста host, який ввів користувач?",
         options=['subprocess.run("ping -c 1 " + host, shell=True)', 'os.system(f"ping -c 1 {host}")',
                  'subprocess.run(["ping", "-c", "1", host])', 'subprocess.run(f"ping -c 1 {host}", shell=True)'],
         answer=2,
         explain="Список аргументів без shell=True: host лишається одним аргументом, а ; чи && у ньому не стають новою командою. Але host = \"--help\" ping усе ще прочитає як опцію, тому ще й перевірити, що host схожий на імʼя хоста і не починається з дефісу. CWE-78 (A05).",
         src="Теорія, тема 2"),
    dict(id="ps-024", topic=T3, type="single", q="Що виведе цей код?",
         run=('def is_admin(user, admins):\n    try:\n        return user in admins\n    except Exception:\n        return True\n\n\n'
              'print(is_admin("anna", None))'),
         options=["True", "False", "TypeError", "None"],
         explain="\"anna\" in None кидає TypeError, а except повертає True - зламана перевірка зробила anna адміном. Це fail open. Правильно: в except повертати False.",
         src="Теорія, тема 3; CWE-636 (A10)"),
    dict(id="ps-025", topic=T3, type="single", q="Функція get_note(user, note_id) повертає нотатку за номером. Що вона МУСИТЬ перевірити, щоб не було IDOR?",
         options=["Що note_id - ціле число", "Що нотатка існує і її власник - саме user", "Що user увійшов сьогодні", "Що нотатка не порожня"],
         answer=1,
         explain="IDOR - відсутність перевірки «чий обʼєкт». Перевірка власника на кожен запит.",
         src="Теорія, тема 3"),
    dict(id="ps-026", topic=T3, type="single", q="Чому на «чужу» і на «неіснуючу» нотатку краще відповідати однаково («нема доступу»)?",
         options=["Так коротше код", "Щоб не підказувати, які номери існують", "Так вимагає Python", "Щоб швидше працювало"],
         answer=1,
         explain="Різні відповіді («нема такої» / «чужа») дають перебрати номери і дізнатись, які існують.",
         src="Теорія, тема 3"),
    dict(id="ps-027", topic=T4, type="single", q="Де в функції розбору вводу має стояти перевірка довжини?",
         options=["Першою, до split і циклів", "Після розбору, коли список уже є", "У кінці, перед return", "Ніде, Python сам обмежить"],
         answer=0,
         explain="Якщо спершу розібрати 100 МБ, памʼять і час уже витрачені. Межа - до будь-якої роботи.",
         src="Теорія, тема 4"),
    dict(id="ps-028", topic=T5, type="single", q="Що виведе код?",
         run=('from pathlib import Path\n\nBASE = Path("/srv/files").resolve()\n'
              'p = (BASE / "../secret.txt").resolve()\nprint(p.is_relative_to(BASE))'),
         options=["False", "True", "ValueError", "/srv/secret.txt"],
         explain="resolve() звів .. і шлях вийшов з теки /srv/files, тому is_relative_to(BASE) - False. Так і ловлять path traversal.",
         src="Теорія, тема 5"),
    dict(id="ps-029", topic=T5, type="single", q="Що виведе код?",
         run='from pathlib import PurePosixPath\n\nprint(PurePosixPath("/srv/files") / "/etc/passwd")',
         options=["/etc/passwd", "/srv/files/etc/passwd", "/srv/files//etc/passwd", "ValueError"],
         explain="Абсолютний шлях праворуч «перебиває» теку ліворуч. Тому шукати в імені лише .. замало - перевіряти треба готовий шлях.",
         src="Теорія, тема 5; документація pathlib"),
    dict(id="ps-030", topic=T5, type="single", q="Ключ API випадково потрапив у коміт на GitHub. Що робити ПЕРШИМ?",
         options=["Видалити файл новим комітом", "Відкликати ключ і створити новий", "Зробити репозиторій приватним", "Нічого, ніхто не помітить"],
         answer=1,
         explain="Файл лишається в історії git, а боти сканують GitHub постійно. Старий ключ треба вважати вкраденим: відкликати і замінити. Потім прибрати з коду.",
         src="Теорія, тема 5"),
    dict(id="ps-031", topic=T5, type="single", q="Чим генерувати токен для скидання пароля?",
         options=["random.randint", "secrets.token_urlsafe", "time.time()", "hash(імʼя користувача)"],
         answer=1,
         explain="random передбачуваний (для ігор і симуляцій). Для паролів і токенів - модуль secrets. Слабкий генератор - CWE-338 (A04).",
         src="Теорія, тема 5; документація Python secrets"),
    dict(id="ps-032", topic=T5, type="short",
         q="Імʼя файлу з секретами, яке дописують у .gitignore (зазвичай)?",
         answer=".env", accept=[".env", "env", "файл .env", ".env-файл", "env файл"],
         explain="У .env лежать ключі й паролі. .gitignore не дає випадково закомітити. Сам Python .env не читає: python-dotenv (load_dotenv()) переносить значення в змінні оточення, звідки їх бере os.environ.",
         src="Теорія, тема 5"),
    dict(id="ps-033", topic=T6, type="single", q="Що виведе код?",
         run=('LOG = []\n\n\ndef handle(func):\n    try:\n        return func()\n    except Exception as e:\n'
              '        LOG.append(type(e).__name__)\n        return "Сталася помилка"\n\n\nprint(handle(lambda: 1 / 0), LOG)'),
         options=["Сталася помилка ['ZeroDivisionError']", "ZeroDivisionError: division by zero", "Сталася помилка []", "None ['ZeroDivisionError']"],
         explain="Користувач бачить лише коротке повідомлення, а деталь (тип помилки) пішла в лог.",
         src="Теорія, тема 6"),
    dict(id="ps-034", topic=T6, type="single", q="Чому на сервері не можна лишати DEBUG = True (Django) чи debug=True (Flask)?",
         options=["Сайт працює повільніше", "Помилки показують відвідувачам код, налаштування і стектрейси (у Flask ще й консоль налагодження)",
                  "Не працює HTTPS", "Python 3 це заборонив"], answer=1,
         explain="Режим налагодження - для свого ПК. На сервері це витік внутрішніх деталей (A02 Security Misconfiguration).",
         src="Теорія, тема 6"),
    dict(id="ps-035", topic=T7, type="single", q="Typosquatting у pip - це...",
         options=["Опечатка в коді", "Шкідливий пакет з назвою, схожою на справжню (reqeusts замість requests)",
                  "Пакет без документації", "Стара версія пакета"], answer=1,
         explain="Підробка теж лежить на pypi.org, тому назву бери з документації чи репозиторію проєкту і звіряй на pypi.org автора, репозиторій і кількість завантажень. Пакети, які порадив ШІ, - так само. Це частина A03:2025 Software Supply Chain Failures.",
         src="Теорія, тема 7"),
    dict(id="ps-036", topic=T7, type="single", q="Навіщо фіксувати версії в requirements.txt (requests==2.32.4)?",
         options=["Так швидше ставиться", "Щоб ставилась та сама перевірена версія, а не будь-яка нова, і pip-audit перевіряв саме її",
                  "Без цього pip не працює", "Щоб пакет займав менше місця"], answer=1,
         explain="Без версії сьогодні і через місяць встановиться різне - і нове «оновлення» може бути зламаним чи шкідливим.",
         src="Теорія, тема 7"),
    dict(id="ps-037", topic=T8, type="single", q="Що виведе код?",
         run='from urllib.parse import urlparse\n\nprint(urlparse("https://example.com@evil.net/x").hostname)',
         options=["evil.net", "example.com", "example.com@evil.net", "None"],
         explain="Частина до @ - це «імʼя користувача», а хост - evil.net. Тому url.startswith(\"https://example.com\") обманюється, а hostname - ні.",
         src="Теорія, тема 8; задача 6"),
    dict(id="ps-038", topic=T8, type="single", q="Що виведе код?",
         run='import ipaddress\n\nprint(ipaddress.ip_address("169.254.169.254").is_global)',
         options=["False", "True", "ValueError", "169.254.169.254"],
         explain="169.254.x.x - локальна службова адреса (у хмарі там метадані з ключами). is_global = False, тож перевірка SSRF її відкине.",
         src="Теорія, тема 8; документація ipaddress"),
    dict(id="ps-039", topic=T9, type="single", q="Що виведе код?",
         run='import html\n\nprint(html.escape("<b>hi</b>"))',
         options=["&lt;b&gt;hi&lt;/b&gt;", "<b>hi</b>", "hi", "&lt;b&gt;hi&lt;b&gt;"],
         explain="html.escape міняє < і > на &lt; і &gt;, тому браузер показує теги як текст, а не виконує.",
         src="Теорія, тема 9"),
    dict(id="ps-040", topic=T9, type="single", q="Що захищає від CSRF?",
         options=["Довгий пароль", "CSRF-токен у формі і cookie з SameSite", "HTTPS сам по собі", "Перейти з POST на GET"],
         answer=1,
         explain="CSRF: чужий сайт змушує твій браузер надіслати запит з твоїми cookie. Токен, якого чужий сайт не знає, + SameSite=Lax. CWE-352 (A01).",
         src="Теорія, тема 9"),
    dict(id="ps-041", topic=T9, type="single", q="Чому sha256(пароль) - погане зберігання пароля?",
         options=["SHA-256 зламаний", "Він дуже швидкий: відеокарта перебирає мільярди варіантів за секунду",
                  "Він дає задовгий рядок", "Його не можна порівняти"], answer=1,
         explain="Для паролів потрібна навмисно повільна функція з памʼяттю і сіллю (Argon2id). CWE-916 (A04).",
         src="Теорія, тема 9; OWASP Password Storage Cheat Sheet"),
    dict(id="ps-042", topic=T9, type="single", q="Чому токени порівнюють hmac.compare_digest(a, b), а не a == b?",
         options=["== не працює з рядками", "== зупиняється на першій різниці, і за часом відповіді можна вгадувати символи",
                  "compare_digest швидший", "Так вимагає PEP 8"], answer=1,
         explain="compare_digest порівнює за сталий час, тож час не підказує, скільки перших символів збіглося. Рядки він бере лише ASCII, тому ввід користувача порівнюють як байти (.encode()).",
         src="Теорія, тема 9; документація hmac"),
    dict(id="ps-043", topic=T10, type="single", q="Сортування ORDER BY {колонка} від користувача. Як правильно?",
         options=["Передати колонку параметром ?", "Перевірити, що колонка з дозволеного списку, і лише тоді підставити",
                  "Прибрати з назви лапки", "Взяти колонку як є"], answer=1,
         explain="Параметром ? можна передати лише значення, не назву колонки. Тому - список дозволених назв.",
         src="Теорія, тема 10; задача 10"),
    dict(id="ps-044", topic=T10, type="single", q="Яким користувачем бази має заходити вебзастосунок?",
         options=["Адміном бази (root/postgres)", "Окремим користувачем лише з потрібними правами на свої таблиці",
                  "Будь-яким", "Без пароля"], answer=1,
         explain="Найменші права зменшують шкоду: після інʼєкції не вийде видалити чужі таблиці чи всю базу (хоча свої таблиці все одно під загрозою, тому параметри обовʼязкові).",
         src="Теорія, тема 10"),
    dict(id="ps-045", topic=T1, type="multi", q="Що з цього - дані ззовні, які треба перевіряти? (кілька)",
         options=["Текст з input()", "Cookie з браузера", "Імʼя файлу, який завантажив користувач", "Константа MAX_LEN = 200 у твоєму коді"],
         answer=[0, 1, 2],
         explain="Ззовні - усе, що може змінити інша людина: ввід, cookie, заголовки, імена файлів, URL. Константа у твоєму коді - не ззовні.",
         src="Теорія, вступ і тема 1"),
    dict(id="ps-046", topic=T0, type="single", q="У якій категорії OWASP Top 10:2025 тепер SSRF?",
         options=["A01 Broken Access Control", "A10 Server-Side Request Forgery", "A05 Injection", "A02 Security Misconfiguration"],
         answer=0,
         explain="У 2021 SSRF був окремою A10. У 2025 його внесли в A01, а A10:2025 - нова категорія Mishandling of Exceptional Conditions.",
         src=OW),
    dict(id="ps-047", topic=T0, type="single", q="A03 в OWASP Top 10:2025 - це...",
         options=["Software Supply Chain Failures (ланцюг постачання: пакети, збірка, оновлення)", "Injection",
                  "Cryptographic Failures", "Insecure Design"], answer=0,
         explain="Нова назва замість «Vulnerable and Outdated Components» (2021): не лише старі пакети, а й шкідливі пакети, зламана збірка і CI.",
         src=OW),
    dict(id="ps-048", topic=T6, type="single", q="Чому погано писати except: pass навколо збереження даних?",
         options=["Це повільно", "Помилка зникає мовчки, а дані лишаються напівзміненими, і ніхто не знає",
                  "Python це забороняє", "Так займає більше памʼяті"], answer=1,
         explain="Ловити треба конкретні помилки і щось з ними робити (відкат, лог, коротке повідомлення). A10:2025 - неправильна обробка винятків.",
         src="Теорія, тема 6"),
]


def build():
    out = []
    ids = set()
    for q in Q:
        q = dict(q)
        assert q["id"] not in ids, q["id"]
        ids.add(q["id"])
        code = q.pop("run", None)
        if code:
            got = norm(run_like_browser(code))
            assert len(got) == 1, (q["id"], got)
            res = got[0]
            hits = [i for i, o in enumerate(q["options"]) if o == res]
            assert len(hits) == 1, (q["id"], res, q["options"])
            if "answer" in q:
                assert q["answer"] == hits[0], (q["id"], "answer != вивід коду")
            q["answer"] = hits[0]
            q["pre"] = code
        if q["type"] in ("single", "multi"):
            assert len(set(q["options"])) == len(q["options"]), q["id"]
            assert 3 <= len(q["options"]) <= 5, q["id"]
        if q["type"] == "short":
            assert q["answer"] in q["accept"], q["id"]
        out.append(q)
    return {"questions": out}


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    doc = build()
    text = json.dumps(doc, ensure_ascii=False, indent=1) + "\n"
    if "--check" in sys.argv:
        cur = OUT.read_text(encoding="utf-8") if OUT.exists() else ""
        if cur != text:
            print("quiz.json НЕ збігається з генератором")
            sys.exit(1)
        print(f"quiz.json = генератор, {len(doc['questions'])} питань")
        return
    OUT.write_text(text, encoding="utf-8")
    n_run = sum(1 for q in Q if "run" in q)
    print(f"записано {len(doc['questions'])} питань, з них {n_run} «що виведе» перевірено запуском")


if __name__ == "__main__":
    main()
