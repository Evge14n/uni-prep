"""Генератор розділу «linux» (навичка: Linux/WSL для лаб з Python), ULINUX1 17.11.2026.

Джерело тексту - курс «Linux за 10 днів» у D:\\Універ\\05_Програмування\\Linux\\ (його пише ULINUX1).
Скрипт збирає з нього content/linux/teoriya.md, zadachi.md, shpargalka.md, пише quiz.json з даних нижче
і кладе site/files/ustanovka.sh (скрипт налаштування Ubuntu, його качають на ноутбук через wget).

Запуск:
    python -P -E tools/gen_linux.py                 - записати файли розділу
    python -P -E tools/gen_linux.py --check [файл]  - звірити quiz.json (або копію) з даними тут
    python -P -E tools/gen_linux.py --wsl           - прогнати в Ubuntu (WSL) команди питань з полем sh
                                                      і звірити вивід з правильною відповіддю
"""
import json
import re
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "content" / "linux"
COURSE = Path(r"D:\Універ\05_Програмування\Linux")
SHPARG = Path(r"D:\Універ\_У_ЗОШИТ\Linux - шпаргалка.md")

# на публічний сайт не йдуть ПІБ і група
# (шаблонами, щоб самих імен не було і в коді публічного репо)
SANITIZE = [
    (r"\b[^\W\d_]+_[^\W\d_]+_[^\W\d_]+-\d+_20\d\d\b", "Прізвище_Імʼя_Група_2026"),
    (r'(git config --global user\.name )"[^"]*"', r'\1"Твоє Імʼя Прізвище"'),
]

DAYS = [
    ("День 01 - термінал і файли.md", "Термінал і де які файли"),
    ("День 02 - mkdir cp mv rm безпечно.md", "Створити, скопіювати, видалити безпечно"),
    ("День 03 - nano і VS Code.md", "Переглянути і редагувати: nano і VS Code"),
    ("День 04 - права і sudo.md", "Права і sudo"),
    ("День 05 - пакети apt.md", "Пакети: apt"),
    ("День 06 - процеси.md", "Процеси"),
    ("День 07 - пайпи і grep.md", "Пайпи, перенаправлення, grep"),
    ("День 08 - python у venv і ЛР.md", "Python у venv і запуск ЛР"),
    ("День 09 - git.md", "git"),
    ("День 10 - bash-скрипт.md", "Свій bash-скрипт"),
]

T0 = "0. Встановлення і WSL"
TOP = {n: f"{n}. {t}" for n, (_, t) in enumerate(DAYS, 1)}


def S(id_, topic, q, options, answer, explain, src, sh=None):
    """single; sh = (команда bash, очікуваний вивід) - перевірка в WSL (--wsl)."""
    d = {"id": id_, "topic": topic, "type": "single", "q": q, "options": options, "answer": answer,
         "explain": explain, "src": src}
    if sh:
        d["_sh"] = sh
    return d


def T(id_, topic, q, answer, accept, explain, src, sh=None):
    """short: відповідь словом/командою; sh - як у S."""
    d = {"id": id_, "topic": topic, "type": "short", "q": q, "answer": answer, "accept": accept,
         "explain": explain, "src": src}
    if sh:
        d["_sh"] = sh
    return d


D = "Курс Linux, день "
Q = [
    # 0. Встановлення
    S("w-01", T0, "Яка команда в PowerShell (від адміністратора) встановлює WSL з Ubuntu?",
      ["wsl --install", "apt install ubuntu", "winget install linux", "sudo wsl"], 0,
      "wsl --install ставить WSL і Ubuntu (Ubuntu - за замовчуванням), потім перезавантаження. apt і sudo - це вже команди всередині Linux.",
      "Почни тут, крок 2; Microsoft «Install WSL»"),
    S("w-02", T0, "З якої збірки Windows 10 вікна з Linux (turtle) відкриваються у WSL?",
      ["19044", "19041", "22000", "з будь-якої"], 0,
      "Microsoft: «Windows 10 Build 19044+ or Windows 11». 19041 - мінімум для самого WSL, але без вікон. 22000 - це вже Windows 11. Збірку видно в winver.",
      "Почни тут, крок 1; Microsoft «Run Linux GUI apps»"),
    S("w-03", T0, "Де тримати файли лаб, щоб усе працювало найшвидше?",
      ["у ~/univer/labs (файлова система Linux)", "у /mnt/c/Users/...", "у /tmp", "у /root"], 0,
      "Microsoft радить тримати файли проєкту у файловій системі WSL. /mnt/c - доступ до диска Windows через міст, повільніше. /tmp чиститься, /root - не твоя тека.",
      "Почни тут, крок 6; Microsoft «Working across file systems»"),
    S("w-04", T0, "Яка команда відкриває поточну теку Linux у Провіднику Windows?",
      ["explorer.exe .", "explorer.exe", "open .", "cd explorer"], 0,
      "Крапка в кінці - «ця тека». Без крапки Провідник відкриється на «Документах», а не тут. Адреса буде \\\\wsl.localhost\\Ubuntu\\home\\...",
      "Почни тут, крок 6"),
    S("w-05", T0, "Як з PowerShell повністю перезапустити Ubuntu, якщо все зависло?",
      ["wsl --shutdown", "exit", "sudo reboot", "Ctrl+C"], 0,
      "wsl --shutdown зупиняє всі дистрибутиви WSL; потім просто знову відкрий Ubuntu.", D + "6"),
    S("w-06", T0, "Ти закрив вікно Ubuntu посеред sudo apt upgrade. Наступного разу «dpkg was interrupted». Що робити?",
      ["sudo dpkg --configure -a, потім повторити команду", "перевстановити Ubuntu", "видалити файли lock у /var/lib/dpkg",
       "нічого, усе доставиться саме"], 0,
      "dpkg --configure -a доналаштовує обірвані пакети. Ubuntu у WSL гасне за кілька секунд після закриття всіх вікон - тому довгі команди не можна кидати.",
      D + "5"),
    # 1
    T("t1-01", TOP[1], "Яка команда показує, в якій теці ти зараз?", "pwd", ["pwd"],
      "pwd = print working directory.", D + "1", sh=("cd ~ && pwd | sed 's|.*/||'", "evgen")),
    S("t1-02", TOP[1], "Ти в /home/evgen/univer/labs. Де будеш після cd ../.. ?",
      ["/home/evgen", "/home", "/home/evgen/univer", "/"], 0,
      "Кожне .. - на одну теку вище: labs → univer → evgen.", D + "1",
      sh=("mkdir -p home/evgen/univer/labs && cd home/evgen/univer/labs && cd ../.. && basename \"$(pwd)\"", "evgen")),
    S("t1-03", TOP[1], "Як у WSL називається диск D: Windows?", ["/mnt/d", "D:/", "/d", "/dev/d"], 0,
      "Диски Windows примонтовані в /mnt: C: → /mnt/c, D: → /mnt/d.", D + "1", sh=("[ -d /mnt/c ] && echo /mnt/c", "/mnt/c")),
    S("t1-04", TOP[1], "Що показує ls -a, чого не показує ls?",
      ["приховані файли (імена з крапкою)", "розміри файлів", "лише теки", "файли в підтеках"], 0,
      "Файли, чиє імʼя починається з крапки (.bashrc, .venv), приховані. -a = all. Розміри - це -l.", D + "1",
      sh=("touch .h x && ls | wc -l && ls -A | wc -l", "1\n2")),
    S("t1-05", TOP[1], "Що робить клавіша Tab у терміналі?",
      ["дописує назву файлу, теки чи команди", "вставляє табуляцію", "перемикає вікно", "скасовує команду"], 0,
      "Tab дописує, два Tab - показують варіанти. Рятує з кириличними назвами.", D + "1"),
    S("t1-06", TOP[1], "cd Univer пише «No such file or directory», хоча тека univer є. Чому?",
      ["Linux розрізняє великі й малі літери", "треба sudo", "тека лежить на диску D:", "треба писати cd /Univer"], 0,
      "Univer і univer - різні імена. Тисни Tab замість вгадувати.", D + "1"),
    # 2
    S("t2-01", TOP[2], "Що станеться після mkdir ЛР 4 ?",
      ["створяться дві теки: ЛР і 4", "одна тека «ЛР 4»", "помилка", "тека ЛР4"], 0,
      "Пробіл розділяє аргументи. Одна тека з пробілом: mkdir \"ЛР 4\".", D + "2",
      sh=("mkdir ЛР 4 && ls | sort | tr '\\n' ' '", "4 ЛР ")),
    T("t2-02", TOP[2], "Як перейменувати lab.py на lab4.py? (одна команда)", "mv lab.py lab4.py", ["mv lab.py lab4.py"],
      "mv і переміщує, і перейменовує.", D + "2", sh=("touch lab.py && mv lab.py lab4.py && ls", "lab4.py")),
    S("t2-03", TOP[2], "Чим rmdir безпечніший за rm -r?",
      ["видаляє лише порожню теку", "кладе в кошик", "питає пароль", "нічим"], 0,
      "rmdir відмовить, якщо в теці є файли. rm -r видалить усе всередині. Кошика в Linux нема.", D + "2",
      sh=("mkdir a && touch a/f && (rmdir a 2>/dev/null || echo ні) && ls a", "ні\nf")),
    S("t2-04", TOP[2], "cp new.py old.py, а old.py уже існує. Що буде?",
      ["old.py мовчки перезапишеться", "cp спитає дозволу", "помилка", "створиться old(1).py"], 0,
      "cp і mv перезаписують без питань. З -i (cp -i) спитають.", D + "2",
      sh=("echo нове > new.py && echo старе > old.py && cp new.py old.py && cat old.py", "нове")),
    S("t2-05", TOP[2], "(Не вводь це.) Що зробила б команда rm з шаблоном * .py - з пробілом між * і .py?",
      ["видалила б усі файли в теці", "видалила б лише .py", "нічого", "спитала б підтвердження"], 0,
      "Аргументів два: * (усі файли теки) і .py. Перевірити без ризику - echo перед командою: echo rm * .py надрукує, що зачепило б.",
      D + "2", sh=("touch a b c.py && echo rm * .py", "rm a b c.py .py")),
    S("t2-06", TOP[2], "Що зробити ПЕРЕД rm *.png?",
      ["ls *.png - подивитись, що саме видалиться", "sudo", "chmod 777", "нічого, є кошик"], 0,
      "rm стирає назавжди. ls з тим самим шаблоном показує, що піде під видалення.", D + "2"),
    S("t2-07", TOP[2], "cp ЛР3 ЛР3-копія пише «-r not specified; omitting directory». Що додати?",
      ["-r", "-f", "-i", "sudo"], 0, "-r = рекурсивно, тобто теку з усім вмістом.", D + "2",
      sh=("mkdir ЛР3 && (cp ЛР3 К 2>&1 | grep -c 'not specified')", "1")),
    # 3
    S("t3-01", TOP[3], "Як зберегти файл і вийти з nano?",
      ["Ctrl+O, Enter, потім Ctrl+X", "Esc, потім :wq", "Ctrl+S, потім Ctrl+Q", "Alt+F4"], 0,
      "^O = Write Out (зберегти), ^X = Exit. :wq - це vim.", D + "3"),
    T("t3-02", TOP[3], "Команда: показати останні 5 рядків файлу log.txt.", "tail -n 5 log.txt",
      ["tail -n 5 log.txt", "tail -5 log.txt", "tail -n5 log.txt", "tail --lines=5 log.txt", "tail --lines 5 log.txt"],
      "tail - кінець файлу, head - початок. -n - скільки рядків.", D + "3",
      sh=("seq 1 10 > log.txt && tail -n 5 log.txt | tr '\\n' ' '", "6 7 8 9 10 ")),
    S("t3-03", TOP[3], "Скрипт падає з bash: $'\\r': command not found. Що це?",
      ["файл має кінці рядків Windows (CRLF)", "у файла нема права x", "bash не встановлено", "помилка в Python"], 0,
      "Windows закінчує рядок \\r\\n, bash бачить зайвий \\r. VS Code: CRLF → LF, або sed -i 's/\\r$//' файл.", D + "3",
      sh=("printf '#!/bin/bash\\r\\n\\r\\necho hi\\r\\n' > c.sh && bash c.sh 2>&1 | grep -c 'command not found'", "1")),
    S("t3-04", TOP[3], "Як відкрити поточну теку у VS Code з терміналу Ubuntu?",
      ["code .", "vscode", "open code", "start code"], 0,
      "code . - крапка означає поточну теку. VS Code має бути встановлений у Windows з галочкою «Add to PATH».", D + "3"),
    S("t3-05", TOP[3], "Як у nano скасувати останню зміну?",
      ["Alt+U", "Ctrl+Z", "Ctrl+U", "Esc"], 0,
      "Alt+U = Undo. Ctrl+Z у nano 7 лише пише «To suspend, type ^T^Z», а Ctrl+U - це «вставити» вирізаний рядок.", D + "3"),
    S("t3-06", TOP[3], "Чим less кращий за cat для довгого файлу?",
      ["гортає по екрану, можна назад і пошук /слово", "less змінює файл", "cat не читає довгі файли", "нічим"], 0,
      "cat вивалює все одразу. less: пробіл, стрілки, /слово, q - вийти.", D + "3"),
    # 4
    S("t4-01", TOP[4], "Що означають права -rw-r--r--?",
      ["власник читає і пише, група й інші лише читають", "усі можуть усе", "лише власник читає", "файл можна запускати"], 0,
      "Перший символ - тип (- файл), далі трійки: власник rw-, група r--, інші r--. x ніде нема.", D + "4"),
    T("t4-02", TOP[4], "Яким числом записати права rwxr-xr-x?", "755", ["755", "0755"],
      "r=4, w=2, x=1: rwx = 7, r-x = 5, r-x = 5.", D + "4", sh=("touch f && chmod u=rwx,go=rx f && stat -c %a f", "755")),
    T("t4-03", TOP[4], "Яким числом записати права rw------- ?", "600", ["600", "0600"],
      "rw- = 4+2 = 6, далі нулі: ніхто інший нічого.", D + "4", sh=("touch f && chmod u=rw,go= f && stat -c %a f", "600")),
    S("t4-04", TOP[4], "Чому ./run.sh пише Permission denied, а bash run.sh працює?",
      ["у файлу нема права x, а bash просто читає файл", "треба sudo", "файл пошкоджений", "bash має права root"], 0,
      "./run.sh запускає файл як програму - потрібне x (chmod +x). bash run.sh запускає bash, якому досить права r.", D + "4",
      sh=("echo 'echo ok' > run.sh && (./run.sh 2>&1 | grep -c denied) && bash run.sh", "1\nok")),
    S("t4-05", TOP[4], "Чий пароль питає sudo в Ubuntu у WSL?",
      ["пароль користувача Ubuntu, заданий при встановленні", "пароль Windows", "пароль облікового запису Microsoft", "ніякий"], 0,
      "Це твій пароль Linux. Символи при вводі не видно - це нормально.", D + "4"),
    T("t4-06", TOP[4], "Команда, яка дозволяє запускати run.sh як ./run.sh", "chmod +x run.sh",
      ["chmod +x run.sh", "chmod u+x run.sh", "chmod 755 run.sh", "chmod a+x run.sh"],
      "+x додає право запуску. 755 теж дає x.", D + "4",
      sh=("echo 'echo ok' > run.sh && chmod +x run.sh && ./run.sh", "ok")),
    S("t4-07", TOP[4], "Забув пароль Ubuntu. Як задати новий?",
      ["у PowerShell Windows: wsl -u root passwd evgen", "перевстановити Windows", "sudo passwd без пароля",
       "видалити /etc/passwd"], 0,
      "wsl -u root відкриває Ubuntu від root без пароля, passwd evgen задає новий пароль користувачу evgen.", D + "4"),
    # 5
    S("t5-01", TOP[5], "Чим sudo apt update відрізняється від sudo apt upgrade?",
      ["update оновлює список пакетів, upgrade ставить новіші версії", "це одне й те саме",
       "update оновлює Windows", "upgrade лише показує список"], 0,
      "Порядок: спершу update, потім upgrade або install.", D + "5"),
    S("t5-02", TOP[5], "Що буде, якщо в Ubuntu 24.04 поза venv виконати pip install numpy?",
      ["помилка externally-managed-environment", "numpy нормально встановиться", "numpy встановиться у venv",
       "видалиться системний Python"], 0,
      "Ubuntu захищає системний Python (правило PEP 668). Бібліотеки - у venv: спершу univer або source .venv/bin/activate.",
      D + "5"),
    S("t5-03", TOP[5], "Що робить && у команді a && b?",
      ["b виконується лише якщо a завершилась успішно", "b виконується завжди", "b запускається у фоні",
       "a і b виконуються одночасно"], 0,
      "Успіх = код 0. false && echo x нічого не виведе.", D + "5", sh=("false && echo x; true && echo y", "y")),
    S("t5-04", TOP[5], "sudo apt install htop пише «Unable to locate package». Що спершу?",
      ["sudo apt update", "видалити lock-файли", "pip install htop", "перезапустити ПК"], 0,
      "Список пакетів застарів або порожній - update його оновить.", D + "5"),
    S("t5-05", TOP[5], "Що ставити через apt, а що через pip?",
      ["apt - система (python3, git, python3-tk), pip - бібліотеки Python у venv", "усе через pip",
       "усе через apt", "pip - для системи, apt - для venv"], 0,
      "turtle потребує python3-tk з apt; matplotlib, numpy, pytest - pip у venv.", D + "5"),
    S("t5-06", TOP[5], "apt пише «Could not get lock /var/lib/dpkg/lock-frontend». Що робити?",
      ["інший apt уже працює (часто автооновлення) - зачекати кілька хвилин", "видалити lock-файл",
       "перевстановити apt", "вимкнути інтернет"], 0,
      "Lock-файли не видаляють - можна зламати базу пакетів. Зачекай і повтори.", D + "5"),
    # 6
    S("t6-01", TOP[6], "Чим Ctrl+C відрізняється від Ctrl+Z?",
      ["Ctrl+C зупиняє програму, Ctrl+Z лише призупиняє", "це одне й те саме", "Ctrl+C копіює текст",
       "Ctrl+Z зупиняє, Ctrl+C призупиняє"], 0,
      "Після Ctrl+Z програма жива: jobs покаже Stopped, fg поверне.", D + "6",
      sh=("timeout -s INT 2 python3 -c 'import time; time.sleep(9)' 2>&1 | grep -c KeyboardInterrupt", "1")),
    S("t6-02", TOP[6], "Як знайти PID усіх запущених python?",
      ["pgrep -af python", "ls /python", "pwd python", "which python"], 0,
      "pgrep -af: PID і повна команда. По-старому ps aux | grep python (PID - друга колонка, останній рядок - сам grep). which показує лише шлях до програми.",
      D + "6", sh=("sleep 30 & pgrep -af 'sleep 30' | grep -cE '^[0-9]+ sleep 30$'; kill %1", "1")),
    S("t6-03", TOP[6], "Що робить & у кінці команди?",
      ["запускає її у фоні, термінал одразу вільний", "запускає від root", "повторює команду", "зберігає вивід у файл"], 0,
      "jobs покаже фонові задачі, kill %1 зупинить першу.", D + "6"),
    S("t6-04", TOP[6], "Працював python3 forever.py, ти натиснув Ctrl+Z, і програма «зникла». Як побачити, що вона ще жива?",
      ["jobs", "ls", "pwd", "history"], 0, "jobs - задачі цього терміналу (Stopped / Running).", D + "6"),
    T("t6-05", TOP[6], "Команда: вбити процес з PID 1234 без питань (якщо звичайний kill не допоміг).", "kill -9 1234",
      ["kill -9 1234", "kill -KILL 1234", "kill -SIGKILL 1234", "kill -s KILL 1234", "kill -s 9 1234"],
      "Спершу звичайний kill 1234 (програма встигне закрити файли), -9 - крайній випадок.", D + "6"),
    S("t6-06", TOP[6], "Програма стоїть, курсор блимає на порожньому рядку. Найімовірніше:",
      ["вона чекає input() - введи значення", "зависла, треба kill -9", "Ubuntu вимкнулась", "нема інтернету"], 0,
      "Порожній рядок з курсором - очікування вводу. Ctrl+D - кінець вводу.", D + "6"),
    # 7
    S("t7-01", TOP[7], "Чим > відрізняється від >> ?",
      ["> перезаписує файл, >> дописує в кінець", "це одне й те саме", ">> перезаписує, > дописує",
       "> для помилок, >> для виводу"], 0, "Два запуски з >> дадуть два рядки, з > - один.", D + "7",
      sh=("echo a > f; echo b > f; echo c >> f; wc -l < f", "2")),
    T("t7-02", TOP[7], "Що виведе printf 'a\\nb\\nc\\n' | wc -l ?", "3", ["3"],
      "Три рядки (три \\n) - wc -l рахує рядки.", D + "7", sh=("printf 'a\\nb\\nc\\n' | wc -l", "3")),
    S("t7-03", TOP[7], "Що виведе grep -c \"def \" lab.py ?",
      ["скільки рядків містять «def »", "номери рядків з def", "самі рядки з def", "назву файлу"], 0,
      "-c = count. Номери рядків - це -n.", D + "7",
      sh=("printf 'def a():\\n    pass\\n\\n\\ndef b():\\n    pass\\n' > lab.py && grep -c 'def ' lab.py", "2")),
    S("t7-04", TOP[7], "Лаба питає одне число через input(). Як подати їй 10 без клавіатури?",
      ["printf \"10\\n\" | python lab.py", "python lab.py 10", "python lab.py > 10", "python lab.py & 10"], 0,
      "Пайп передає текст на ввід програми. python lab.py 10 - це аргумент (sys.argv), input() його не бачить.", D + "7",
      sh=("printf 'x = int(input())\\nprint(x * 2)\\n' > lab.py && printf '10\\n' | python3 lab.py", "20")),
    S("t7-05", TOP[7], "Чому python3 lab.py > lab.py - погана ідея?",
      ["> спершу очищає lab.py, і код зникає", "Python не вміє писати у файли", "буде Permission denied", "нічого поганого"], 0,
      "Перенаправлення відкриває файл на запис (обнуляє) ДО запуску програми. Вивід - в інший файл.", D + "7",
      sh=("echo 'print(1)' > lab.py && python3 lab.py > lab.py; wc -c < lab.py", "0")),
    S("t7-06", TOP[7], "Що робить 2> err.txt ?",
      ["записує помилки (stderr) у файл", "запускає команду двічі", "записує другий рядок", "дописує в кінець"], 0,
      "1 - звичайний вивід, 2 - помилки. 2>&1 - помилки туди ж, куди вивід.", D + "7",
      sh=("python3 nema.py 2> err.txt; grep -c 'No such file' err.txt", "1")),
    T("t7-07", TOP[7], "Що виведе printf '3\\n1\\n2\\n' | sort | head -n 1 ?", "1", ["1"],
      "sort впорядковує (1, 2, 3), head -n 1 бере перший рядок.", D + "7", sh=("printf '3\\n1\\n2\\n' | sort | head -n 1", "1")),
    # 8
    S("t8-01", TOP[8], "Як зрозуміти, що venv увімкнено?",
      ["рядок починається з (.venv)", "термінал стає зеленим", "python3 --version показує venv", "ніяк не видно"], 0,
      "Ще перевірка: which python показує шлях з .venv.", D + "8"),
    S("t8-02", TOP[8], "У кінці lab.py стоїть doctest.testmod(). python lab.py нічого не вивів про doctest. Що це означає?",
      ["усі doctest пройшли", "doctest не запускались", "сталася помилка", "файл порожній"], 0,
      "testmod() мовчить, коли все добре. Подробиці - python lab.py -v, внизу «Test passed.».", D + "8",
      sh=("printf 'import doctest\\n\\n\\ndef f():\\n    \"\"\"\\n    >>> f()\\n    1\\n    \"\"\"\\n    return 1\\n\\n\\ndoctest.testmod()\\n' > lab.py && python3 lab.py | wc -c && python3 lab.py -v | tail -n 1", "0\nTest passed.")),
    T("t8-03", TOP[8], "У кінці lab.py стоїть doctest.testmod(). Який ключ дописати до python lab.py, щоб побачити подробиці кожного прикладу?", "-v",
      ["-v", "--verbose", "python lab.py -v", "python3 lab.py -v"],
      "-v = verbose: testmod() сам бачить його в аргументах. Унизу буде «Test passed.» або «***Test Failed***».", D + "8"),
    S("t8-04", TOP[8], "Як перевірити, що всі рядки лаби не довші за 78 символів?",
      ["flake8 --max-line-length=78 lab.py", "python lab.py 78", "mypy --lines 78 lab.py", "wc -l lab.py"], 0,
      "flake8 перевіряє PEP 8; E501 = задовгий рядок. Наша команда perevir робить це разом з doctest і mypy.", D + "8"),
    S("t8-05", TOP[8], "Чому теку .venv не копіюють на інший компʼютер?",
      ["venv привʼязаний до шляхів і Python того компʼютера - на новому його створюють заново",
       "вона завелика для флешки", "копіювати заборонено ліцензією", "можна, це нормальна практика"], 0,
      "Скрипти у .venv/bin мають абсолютні шляхи. На новому ПК - python3 -m venv і pip install (або ustanovka.sh).", D + "8"),
    S("t8-06", TOP[8], "python -m doctest lab.py показує «1 of 21 in __main__.DebugRunner ***Test Failed***», хоча твої doctest правильні. Чому?",
      ["у файлі doctest.testmod() на верхньому рівні, а -m doctest робить головним модулем сам doctest - і testmod() перевіряє його",
       "у твоїх doctest помилка в 21-му прикладі", "не увімкнено venv", "Python 3.12 не підтримує doctest"], 0,
      "Для файлів з testmod() у кінці: python lab.py (або -v) чи python -m pytest --doctest-modules lab.py. Помилка не твоя.",
      D + "8", sh=("printf 'import doctest\\n\\n\\ndef f():\\n    \"\"\"\\n    >>> f()\\n    1\\n    \"\"\"\\n    return 1\\n\\n\\ndoctest.testmod()\\n' > lab.py && python3 -m doctest lab.py | grep -q 'of  21 in __main__.DebugRunner' && echo чужа", "чужа")),
    S("t8-08", TOP[8], "Яка перевірка doctest дає надійний код помилки (для скрипта перевірки всіх лаб)?",
      ["python -m pytest --doctest-modules -q lab.py", "python lab.py", "python -m doctest lab.py", "cat lab.py"], 0,
      "python lab.py завершується з кодом 0 навіть при Test Failed, а -m doctest плутається з testmod() у файлі. pytest: 1 passed або FAILED і код 1.",
      D + "8, 10", sh=("printf 'import doctest\\n\\n\\ndef f():\\n    \"\"\"\\n    >>> f()\\n    2\\n    \"\"\"\\n    return 1\\n\\n\\ndoctest.testmod()\\n' > lab.py && (python3 lab.py > /dev/null; echo $?) && (~/univer/.venv/bin/python -m pytest --doctest-modules -q -p no:cacheprovider lab.py > /dev/null; echo $?)", "0\n1")),
    S("t8-07", TOP[8], "Вікно turtle зʼявляється і одразу закривається. Чого бракує в кінці програми?",
      ["turtle.done()", "turtle.start()", "sudo", "import tkinter"], 0,
      "turtle.done() тримає вікно, поки його не закриєш (так і в методичці ЛР4). Малювання і done() - під if __name__ == \"__main__\":, щоб перевірка doctest не відкривала вікно.", D + "8"),
    # 9
    S("t9-01", TOP[9], "Яка послідовність зберігає зміни в git?",
      ["git add файл, потім git commit -m \"опис\"", "git commit, потім git add", "git save", "git push"], 0,
      "add вибирає, що піде в коміт, commit робить знімок. push - вивантаження на GitHub, не збереження.", D + "9"),
    T("t9-02", TOP[9], "Команда: показати, що змінилось у файлах з останнього коміту.", "git diff", ["git diff"],
      "git status - які файли змінені, git diff - що саме в них. Вийти з перегляду - q.", D + "9"),
    T("t9-03", TOP[9], "Ти зіпсував lab.py і ще не комітив. Команда, щоб повернути його як в останньому коміті:",
      "git restore lab.py", ["git restore lab.py", "git checkout -- lab.py", "git checkout lab.py"],
      "Незакомічені зміни зникнуть назавжди - перед цим глянь git diff.", D + "9",
      sh=("git init -q && echo 1 > lab.py && git add lab.py && git -c user.name=T -c user.email=t@t commit -qm a && echo 2 > lab.py && git restore lab.py && cat lab.py", "1")),
    S("t9-04", TOP[9], "Що писати в .gitignore для Python-лаби?",
      [".venv/ і __pycache__/", "*.py", "усі файли", "нічого, він не потрібен"], 0,
      "venv - тисячі файлів і привʼязаний до компʼютера, __pycache__ - кеш Python. Код (*.py) якраз треба зберігати.", D + "9",
      sh=("git init -q && printf '.venv/\\n' > .gitignore && mkdir .venv && touch .venv/x && git status --porcelain | grep -c venv", "0")),
    S("t9-05", TOP[9], "git commit пише «Author identity unknown». Що зробити?",
      ["git config --global user.name і user.email", "git init ще раз", "sudo git commit", "видалити .git"], 0,
      "Один раз на компʼютер: git config --global user.name \"Імʼя\" і user.email \"пошта\".", D + "9"),
    S("t9-06", TOP[9], "git commit без -m відкрив vim. Як вийти без збереження?",
      ["Esc, потім :q! і Enter", "Ctrl+C", "Ctrl+X", "закрити вікно"], 0,
      "Наступного разу пиши git commit -m \"опис\" - редактор не відкриється.", D + "9"),
    # 10
    S("t10-01", TOP[10], "Що не так у рядку bash-скрипта count = 5 ?",
      ["пробіли навколо =", "треба лапки навколо 5", "треба $count = 5", "усе правильно"], 0,
      "З пробілами bash шукає команду count. Правильно: count=5.", D + "10",
      sh=("bash -c 'count = 5' 2>&1 | grep -c 'command not found'", "1")),
    S("t10-02", TOP[10], "Навіщо перший рядок #!/bin/bash ?",
      ["каже, яким інтерпретатором виконувати файл при ./скрипт.sh", "це коментар без змісту", "вмикає sudo",
       "робить файл виконуваним"], 0,
      "Shebang. Право запуску окремо дає chmod +x.", D + "10"),
    S("t10-03", TOP[10], "Чому пишуть \"$1\" у лапках?",
      ["щоб шлях з пробілом лишився одним аргументом", "так швидше", "без лапок $1 не працює", "щоб вивести знак долара"], 0,
      "Без лапок «Лаба 4» розпадеться на два аргументи.", D + "10",
      sh=("f() { echo $#; }; x='Лаба 4'; f $x; f \"$x\"", "2\n1")),
    T("t10-04", TOP[10], "Що виведе: x=3; if [ $x -gt 2 ]; then echo так; else echo ні; fi", "так", ["так"],
      "-gt = greater than, 3 > 2.", D + "10", sh=("x=3; if [ $x -gt 2 ]; then echo так; else echo ні; fi", "так")),
    T("t10-05", TOP[10], "Що виведе: false; echo $?", "1", ["1"],
      "$? - код завершення останньої команди: 0 успіх, не 0 помилка. false завжди повертає 1.", D + "10",
      sh=("false; echo $?", "1")),
    T("t10-06", TOP[10], "Що виведе: for w in a b c; do echo -n $w; done", "abc", ["abc"],
      "-n - без переходу на новий рядок, тому все в один рядок.", D + "10",
      sh=("for w in a b c; do echo -n $w; done", "abc")),
    S("t10-07", TOP[10], "if [-f \"$1\"]; then ... дає помилку. Чому?",
      ["нема пробілів всередині [ ]", "треба подвійні дужки", "-f не існує", "треба лапки навколо if"], 0,
      "[ - це команда, їй потрібні пробіли: if [ -f \"$1\" ]; then.", D + "10",
      sh=("bash -c 'if [-f x]; then :; fi' 2>&1 | grep -c 'command not found'", "1")),
]


def clean(s: str) -> str:
    for a, b in SANITIZE:
        s = re.sub(a, b, s)
    s = s.replace("<details><summary>", '<details markdown="1"><summary>')
    return s


def body(md: str) -> str:
    """Без заголовка # і з заголовками на рівень нижче (## → ###)."""
    lines = md.splitlines()
    if lines and lines[0].startswith("# "):
        lines = lines[1:]
    out = []
    fence = False
    for ln in lines:
        if ln.startswith("```"):
            fence = not fence
        if not fence and re.match(r"#{2,5} ", ln):
            ln = "#" + ln
        out.append(ln)
    return "\n".join(out).strip() + "\n"


def build_pages() -> dict:
    start = (COURSE / "00 - Почни тут (встановлення на ноутбуці).md").read_text(encoding="utf-8")
    start = start[start.index("## Крок 0"):]
    teor = ["# Linux за 10 днів по 15 хв",
            "",
            "Щоб писати і запускати лаби з Python в Ubuntu (WSL) на ноутбуці. День = одна тема: 5 хв прочитати,",
            "10 хв зробити руками в терміналі, 5 питань самоперевірки. Усі вправи «Руками» прогнано скриптом",
            "у справжній Ubuntu 24.04 (87 перевірок, 17.11.2026).",
            "",
            "## Тема 0. Встановлення: Ubuntu, VS Code, усе для лаб",
            "",
            body("# x\n" + start)]
    for n, (fn, title) in enumerate(DAYS, 1):
        md = (COURSE / fn).read_text(encoding="utf-8")
        teor += [f"## Тема {n}. День {n}: {title}", "", body(md)]
    prak = (COURSE / "Практика - 3 завдання.md").read_text(encoding="utf-8")
    exam = (COURSE / "ІСПИТ-САМОПЕРЕВІРКА.md").read_text(encoding="utf-8")
    qpart, apart = exam.split("## Відповіді", 1)
    zad = ["# Практика і підсумковий іспит", "",
           "## Три завдання як у справжній роботі", "", body(prak),
           "## Іспит-самоперевірка: 20 питань", "", body(qpart),
           '<details markdown="1"><summary>Відповіді</summary>', "", apart.strip(), "", "</details>", ""]
    sh = SHPARG.read_text(encoding="utf-8")
    sh = "\n".join(ln for ln in sh.splitlines() if not ln.startswith("→"))
    return {"teoriya.md": clean("\n".join(teor)), "zadachi.md": clean("\n".join(zad)), "shpargalka.md": clean(sh)}


META = {
    "id": "linux",
    "title": "Навичка - Linux для лаб (WSL Ubuntu)",
    "kind": "skill",
    "subject": "Linux (термінал, WSL) для лаб з Python",
    "date": "без дати - вчи по 15 хв на день у своєму темпі",
    "points": "Балів не дає. Потрібно, щоб зручно писати і перевіряти лаби",
    "format": "10 днів по 15 хв: тема, вправи руками в Ubuntu на ноутбуці, 5 питань самоперевірки. Як встановити - Тема 0 у Теорії.",
    "include": [],
    "test": {"timer": 15, "count": 15, "note": "самоперевірка за 10 днями курсу; деякі відповіді перевірено запуском команд в Ubuntu"},
}


def quiz() -> list:
    return [{k: v for k, v in q.items() if not k.startswith("_")} for q in Q]


def check(path: Path) -> list:
    errs = []
    data = json.loads(path.read_text(encoding="utf-8"))["questions"]
    want = {q["id"]: q for q in quiz()}
    got = {q["id"]: q for q in data}
    if set(want) != set(got):
        errs.append(f"різні id: {sorted(set(want) ^ set(got))}")
    for i, q in want.items():
        g = got.get(i)
        if g and json.dumps(g, sort_keys=True, ensure_ascii=False) != json.dumps(q, sort_keys=True, ensure_ascii=False):
            errs.append(f"{i}: quiz.json не збігається з даними генератора")
    ids = [q["id"] for q in Q]
    if len(ids) != len(set(ids)):
        errs.append("повтор id")
    for q in Q:
        if q["type"] == "single":
            if not (0 <= q["answer"] < len(q["options"])) or len(set(q["options"])) != len(q["options"]):
                errs.append(f"{q['id']}: answer поза варіантами або повтор варіанта")
        else:
            if q["answer"] not in q["accept"]:
                errs.append(f"{q['id']}: answer нема в accept")
    return errs


def wsl_check() -> list:
    """Кожну команду sh запускає в окремій порожній теці Ubuntu і порівнює вивід з очікуваним."""
    items = [q for q in Q if "_sh" in q]
    lines = ["#!/bin/bash", "B=$(mktemp -d -p ~/.cache glinux.XXXX)"]
    for q in items:
        cmd, _ = q["_sh"]
        lines += [f"mkdir \"$B/{q['id']}\" && cd \"$B/{q['id']}\"",
                  f"echo '@@{q['id']}'", f"( {cmd} ) 2>/dev/null"]
    lines += ["cd ~ && rm -rf \"$B\""]
    with tempfile.NamedTemporaryFile("w", suffix=".sh", delete=False, encoding="utf-8", newline="\n") as f:
        f.write("\n".join(lines) + "\n")
        p = f.name
    wp = subprocess.run(["wsl.exe", "-d", "Ubuntu", "--", "wslpath", "-u", p.replace("\\", "/")],
                        capture_output=True, text=True).stdout.strip()
    r = subprocess.run(["wsl.exe", "-d", "Ubuntu", "--cd", "~", "--", "bash", wp], capture_output=True, timeout=300)
    out = r.stdout.decode("utf-8", "replace")
    got = {}
    for chunk in out.split("@@")[1:]:
        qid, _, rest = chunk.partition("\n")
        got[qid.strip()] = rest.rstrip("\n")
    errs = []
    for q in items:
        exp = q["_sh"][1]
        if got.get(q["id"]) != exp:
            errs.append(f"{q['id']}: чекав {exp!r}, Ubuntu дала {got.get(q['id'])!r}")
    print(f"WSL: {len(items) - len(errs)} з {len(items)} команд дали очікуване")
    return errs


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    if "--check" in sys.argv:
        i = sys.argv.index("--check")
        path = Path(sys.argv[i + 1]) if len(sys.argv) > i + 1 else OUT / "quiz.json"
        errs = check(path)
        print("\n".join(errs) if errs else f"OK: {len(Q)} питань збігаються з даними")
        sys.exit(1 if errs else 0)
    if "--wsl" in sys.argv:
        errs = wsl_check()
        print("\n".join(errs))
        sys.exit(1 if errs else 0)
    OUT.mkdir(parents=True, exist_ok=True)
    for name, text in build_pages().items():
        (OUT / name).write_text(text, encoding="utf-8", newline="\n")
    (OUT / "meta.json").write_text(json.dumps(META, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (OUT / "quiz.json").write_text(json.dumps({"questions": quiz()}, ensure_ascii=False, indent=1) + "\n",
                                   encoding="utf-8")
    files = ROOT / "site" / "files"
    files.mkdir(parents=True, exist_ok=True)
    (files / "ustanovka.sh").write_bytes((COURSE / "ustanovka.sh").read_bytes().replace(b"\r\n", b"\n"))
    errs = check(OUT / "quiz.json")
    print(f"linux: {len(Q)} питань, з них {sum(1 for q in Q if '_sh' in q)} з перевіркою в Ubuntu; "
          + ("OK" if not errs else "; ".join(errs)))


if __name__ == "__main__":
    main()
