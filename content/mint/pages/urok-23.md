# Урок 23. bash-скрипти і cron

[← Усі уроки](#/u/mint/uroky)

**Навіщо:** команди, які ти щоразу набираєш перед здачею лаби, - в один скрипт `zdaty`: він перевірить doctest і
flake8 і збере правильний zip. А cron сам щодня робитиме резервну копію `~/univer`.

## Коротко

**Скрипт** - текстовий файл з командами bash, по одній на рядок. Змінні, пайпи, grep - з уроку 22.

```text
#!/bin/bash                 перший рядок (shebang): яким інтерпретатором запускати
set -euo pipefail           -e: зупинитись на першій помилці; -u: помилка, якщо змінної нема;
                            pipefail: пайп падає, якщо впала будь-яка його частина
# коментар
```

Запуск: `bash скрипт.sh` або один раз `chmod +x скрипт.sh` (дозвіл на виконання, урок 15), а далі `./скрипт.sh`.
Поклав у `~/.local/bin` (урок 22) - запускається звідусіль просто за назвою.

| Що | Значення |
|---|---|
| `$0` | як викликали скрипт |
| `$1`, `$2` ... | перший, другий аргумент |
| `$#` | скільки аргументів |
| `"$@"` | усі аргументи, кожен окремо (завжди в лапках) |
| `$?` | код виходу останньої команди (0 - успіх) |
| `exit 1` | вийти з кодом 1 (помилка) |

**Умови** `[ ... ]` - пробіли біля дужок обовʼязкові:

| Перевірка | Істина, коли |
|---|---|
| `[ -f файл ]` / `[ -d тека ]` / `[ -x файл ]` | файл є / тека є / файл можна запускати |
| `[ -z "$x" ]` / `[ -n "$x" ]` | рядок порожній / не порожній |
| `[ "$a" = "$b" ]` / `!=` | рядки рівні / різні |
| `[ "$n" -eq 1 ]` | числа: `-eq` =, `-ne` ≠, `-lt` <, `-le` ≤, `-gt` >, `-ge` ≥ |

```text
if [ -d "$lab" ]; then          for f in "$lab"/*.py; do        while read -r ryadok; do
    echo "є"                        echo "$f"                       echo "$ryadok"
else                            done                            done < spysok.txt
    echo "нема"
fi

pryvit() {                      функція: виклик - pryvit Прізвище
    local imya="$1"             local - змінна лише всередині функції
    echo "Привіт, $imya"
    return 0                    return - код виходу функції (exit - вийти з усього скрипта)
}

read -r -p "Продовжити? (y/n) " vidp      спитати користувача, відповідь у змінній vidp
```

**shellcheck** - програма, яка читає скрипт і знаходить типові помилки (лапки, `cd` без перевірки тощо).
У Mint: `sudo apt install shellcheck`, далі `shellcheck скрипт.sh`. Тиша = зауважень нема.

**cron** - служба, яка запускає команди за розкладом (на ISO 22.3 є і працює). Кожен користувач має свою
таблицю - **crontab**. Рядок таблиці:

```text
┌───────── хвилина (0-59)
│ ┌─────── година (0-23)
│ │ ┌───── день місяця (1-31)
│ │ │ ┌─── місяць (1-12)
│ │ │ │ ┌─ день тижня (0-7, 0 і 7 - неділя)
│ │ │ │ │
m h dom mon dow   команда

0 13 * * *     щодня о 13:00
30 8 * * 1-5   о 8:30 з понеділка по пʼятницю
*/15 * * * *   кожні 15 хвилин
0 20 * * 0     щонеділі о 20:00
@reboot        один раз після кожного ввімкнення
```

| Команда | Що робить |
|---|---|
| `crontab -e` | редагувати свою таблицю (перший раз спитає редактор) |
| `crontab -l` | показати таблицю |

Три правила cron:
1. **Свій короткий PATH і `/bin/sh`.** У cron нема `~/.local/bin`, venv, аліасів і функцій з `~/.bashrc`. Пиши
   **повні шляхи**: `/home/evgen/univer/.venv/bin/python`, `/home/evgen/.local/bin/zdaty`.
2. **Вивід пропадає.** Додавай у кінець `>> /home/evgen/cron.log 2>&1` - тоді і вивід, і помилки будуть у файлі.
3. **`%` у рядку cron - особливий символ** (означає новий рядок). `date +%F` треба писати `date +\%F`.

Ще: cron не «доганяє» пропущене. Якщо о 13:00 ноутбук спав або був вимкнений - запуск просто пропущено.
Сучасна заміна, яка вміє доганяти, - **таймери systemd** (`systemctl --user`, опція `Persistent=true`), урок 20.

**at** - «виконати один раз пізніше». На ISO 22.3 його нема: `sudo apt install at`, далі
`echo "команда" | at 18:00` або `at now + 10 minutes`, список - `atq`, скасувати - `atrm номер`.

## Передбач, потім запусти

1. Скрипт `arg.sh`:

```bash
printf '#!/bin/bash\necho "Скрипт: $0"\necho "Аргументів: $#"\necho "Перший: $1"\necho "Усі: $@"\n' > ~/arg.sh
chmod +x ~/arg.sh
cd ~
./arg.sh "ЛР 1" lr2
```

<details markdown="1"><summary>Відповідь</summary>

```text
Скрипт: ./arg.sh
Аргументів: 2
Перший: ЛР 1
Усі: ЛР 1 lr2
```

`"ЛР 1"` у лапках - один аргумент, тому їх два, а не три.

</details>

2. Два скрипти відрізняються лише рядком `set -euo pipefail`. Що надрукує кожен?

```bash
printf '#!/bin/bash\ncp nema.txt kopiya.txt\necho "далі"\n' > bez_e.sh
printf '#!/bin/bash\nset -euo pipefail\ncp nema.txt kopiya.txt\necho "далі"\n' > z_e.sh
bash bez_e.sh; echo "код $?"
bash z_e.sh; echo "код $?"
```

<details markdown="1"><summary>Відповідь</summary>

```text
cp: cannot stat 'nema.txt': No such file or directory
далі
код 0
cp: cannot stat 'nema.txt': No such file or directory
код 1
```

Без `set -e` скрипт іде далі після помилки і ще й «успішно» завершується - небезпечно (уяви, що далі `rm`).
З `set -e` він зупиняється на першій помилці.

</details>

3. Порожня тека, у ній нема жодного `.py`. Що надрукує цикл?

```bash
mkdir -p ~/porozhnya && cd ~/porozhnya
for f in *.py; do echo "файл: $f"; done
```

<details markdown="1"><summary>Відповідь</summary>

```text
файл: *.py
```

Якщо шаблон нічого не знайшов, bash лишає його як є - і цикл один раз проходить з «файлом» `*.py`. Тому в
скрипті `zdaty` нижче стоїть `shopt -s nullglob`: тоді порожній шаблон дає нуль файлів.

</details>

4. Рядок у crontab: `30 8 * * 1-5 /home/evgen/.local/bin/nagad`. Коли він спрацює? А `*/15 * * * *`?

<details markdown="1"><summary>Відповідь</summary>

О 8:30 з понеділка по пʼятницю (1-5). `*/15` у полі хвилин - кожні 15 хвилин: 0, 15, 30, 45 кожної години.

</details>

## Руками

**Крок 1. Тренувальна лаба 0** (справжні лаби не чіпаємо). Два файли, у другому навмисно пробіл у кінці рядка:

```bash
mkdir -p ~/univer/labs/lr0
printf 'def kub(x: float) -> float:\n    """Куб числа.\n\n    >>> kub(2)\n    8\n    """\n    return x ** 3\n' > ~/univer/labs/lr0/kub.py
printf 'def kvadrat(x: float) -> float:\n    """Квадрат числа.\n\n    >>> kvadrat(3)\n    9\n    """\n    return x*x \n' > ~/univer/labs/lr0/kvadrat.py
```

**Крок 2. Скрипт `zdaty`.** Потрібні venv з pytest і flake8 (урок 03) і програма `zip` (є на ISO 22.3).

```bash
mkdir -p ~/.local/bin
nano ~/.local/bin/zdaty
```

Встав у nano (Ctrl+Shift+V) або набери текст нижче і зміни `PIB` на своє прізвище, імʼя і групу. Це вміст
файлу, а не команди для термінала - тому блок позначено як текст:

```text
#!/bin/bash
# zdaty - перевірити лабу і зібрати zip на здачу.
# Запуск: zdaty 1      (бере теку ~/univer/labs/lr1)
set -euo pipefail

PIB="Прізвище_Імʼя_Група"        # заміни один раз на своє, напр. Іваненко_Іван_ФзІ-11
LABS="$HOME/univer/labs"
PY="$HOME/univer/.venv/bin/python"
ZDACHA="$HOME/univer/zdacha"

pomylka() {
    echo "ПОМИЛКА: $1" >&2
    exit 1
}

perevir_odyn() {
    local f="$1" ok=0
    if "$PY" -m pytest --doctest-modules -q -p no:cacheprovider "$f" < /dev/null > /dev/null 2>&1; then
        echo "  doctest  ok"
    else
        echo "  doctest  ВПАВ (або файл питає input() - перевір руками, урок 04)"
        ok=1
    fi
    if "$PY" -m flake8 --max-line-length=78 "$f"; then
        echo "  flake8   ok"
    else
        ok=1
    fi
    return "$ok"
}

[ "$#" -eq 1 ] || pomylka "дай номер лаби, напр.: zdaty 1"
n="$1"
lab="$LABS/lr$n"
[ -d "$lab" ] || pomylka "нема теки $lab"
[ -x "$PY" ] || pomylka "нема venv $PY (урок 03)"

shopt -s nullglob
files=("$lab"/*.py)
[ "${#files[@]}" -gt 0 ] || pomylka "у $lab нема .py файлів"

bad=0
for f in "${files[@]}"; do
    echo "$(basename "$f"):"
    perevir_odyn "$f" || bad=1
done

if [ "$bad" -ne 0 ]; then
    read -r -p "Є зауваження. Все одно зібрати архів? (y/n) " vidp
    [ "$vidp" = "y" ] || pomylka "архів не зроблено"
fi

nazva="${PIB}_ЛР${n}"
tmp=$(mktemp -d)
mkdir "$tmp/$nazva"
cp "${files[@]}" "$tmp/$nazva/"
mkdir -p "$ZDACHA"
rm -f "$ZDACHA/$nazva.zip"
(cd "$tmp" && zip -qr "$ZDACHA/$nazva.zip" "$nazva")
rm -rf "$tmp"
echo "Готово: $ZDACHA/$nazva.zip"
unzip -l "$ZDACHA/$nazva.zip"
```

Що тут нового:
- `files=("$lab"/*.py)` - **масив** (список) усіх `.py`; `"${files[@]}"` - усі елементи, `${#files[@]}` - скільки.
- `перевірка || pomylka "..."` - якщо перевірка не пройшла, виклич функцію помилки.
- `>&2` - повідомлення про помилку йде в stderr, як у справжніх програм.
- **zip:** у `tmp` робимо теку з потрібною назвою, кладемо туди лише `.py` і пакуємо **з самої `tmp`** (`cd`).
  Так в архіві буде рівно `Прізвище_Імʼя_Група_ЛР0/kub.py`, без `home/evgen/...` і без сміття (див. «Типові
  помилки»).
- Doctest - через pytest, як у `perevir` з уроку 03. `zdaty` - коротка перевірка (doctest і flake8); `perevir`
  перевіряє більше: doctest (до 120 с), black, flake8, pycodestyle і ruff з рядком до 78 символів, mypy. Перед
  справжньою здачею запусти й `perevir файл.py` (файл з `input()` - `perevir файл.py 5`, відповіді після назви).
  Лаба з `input()` при запуску в `zdaty` покаже «ВПАВ» - таку перевір `perevir` з відповідями або руками з
  `printf`, як в уроці 04, і на питання скрипта відповідай `y`.
- **Кирилиця в назві архіву.** В уроці 14 радимо латиницю для файлів лаб - менше пасток. Але назву архіву часто
  задає викладач (прізвище українською), і тут `zip` у Mint не підводить: він записує назви в UTF-8 і ставить в
  архіві позначку «назви в UTF-8» (перевірено в тестовій Mint: прапорець є за будь-якої мови системи). Linux і
  Python читають такий архів правильно; Windows 10/11 теж мають (на Windows не перевірено). Не впевнений - зроби
  `PIB` латиницею, напр. `Ivanenko_Ivan_FzI-11`.

Збережи (Ctrl+S, Ctrl+X) і:

```bash
chmod +x ~/.local/bin/zdaty
bash -n ~/.local/bin/zdaty
shellcheck ~/.local/bin/zdaty
```

`bash -n` перевіряє синтаксис, нічого не запускаючи. Обидві команди мають мовчати. (Якщо `shellcheck` нема -
`sudo apt install shellcheck`.)

**Крок 3. Перший запуск - є зауваження.** Набери по черзі три команди: `zdaty`, `zdaty 7`, `zdaty 0`. Якщо
`zdaty` «не знаходиться» - урок 22, крок 3 (`source ~/.profile`).

Справжній вивід `zdaty 0` у тестовій Mint 22.3 (на питання відповів `n`; шлях у тебе `/home/evgen/...`):

```text
kub.py:
  doctest  ok
  flake8   ok
kvadrat.py:
  doctest  ok
/home/evgen/univer/labs/lr0/kvadrat.py:7:15: W291 trailing whitespace
Є зауваження. Все одно зібрати архів? (y/n) n
ПОМИЛКА: архів не зроблено
```

`zdaty` без номера скаже `ПОМИЛКА: дай номер лаби, напр.: zdaty 1`, а `zdaty 7` -
`ПОМИЛКА: нема теки /home/evgen/univer/labs/lr7`. Код виходу в усіх трьох - 1 (`echo $?`).

**Крок 4. Виправ і збери.** `nano +7 ~/univer/labs/lr0/kvadrat.py`, зроби рядок `    return x * x` без
пробілу в кінці, збережи. Потім знову `zdaty 0`:

```text
kub.py:
  doctest  ok
  flake8   ok
kvadrat.py:
  doctest  ok
  flake8   ok
Готово: /home/evgen/univer/zdacha/Прізвище_Імʼя_Група_ЛР0.zip
Archive:  /home/evgen/univer/zdacha/Прізвище_Імʼя_Група_ЛР0.zip
  Length      Date    Time    Name
---------  ---------- -----   ----
        0  2026-11-18 10:11   Прізвище_Імʼя_Група_ЛР0/
      102  2026-11-18 10:11   Прізвище_Імʼя_Група_ЛР0/kub.py
      117  2026-11-18 10:11   Прізвище_Імʼя_Група_ЛР0/kvadrat.py
---------                     -------
      219                     3 files
```

Усередині архіву - одна тека з потрібною назвою і лише `.py`. Перед справжньою здачею ще раз подивись, як
викладач просить назвати файл (у тебе в `PIB` - своє).

**Крок 5. cron: перший раз.**

```bash
crontab -l
crontab -e
```

`crontab -l` скаже `no crontab for evgen` (таблиці ще нема). `crontab -e` перший раз спитає редактор. Справжній
вивід з тестової Mint (там встановлено ще micro і vim, тому список довший; у тебе пунктів може бути менше):

```text
no crontab for evgen - using an empty one

Select an editor.  To change later, run 'select-editor'.
  1. /usr/bin/micro
  2. /bin/nano        <---- easiest
  3. /usr/bin/vim.basic
  4. /bin/ed

Choose 1-4 [2]:
```

Обери nano (номер навпроти `easiest`, або просто Enter). Відкриється файл з коментарями англійською - внизу
допиши рядок резервної копії (щодня о 13:00, без `.venv` - його завжди можна перестворити):

```text
0 13 * * * date >> /home/evgen/cron.log && rsync -a --exclude=.venv /home/evgen/univer/ /home/evgen/backup/univer/ >> /home/evgen/cron.log 2>&1
```

Ctrl+S, Ctrl+X. crontab скаже `crontab: installing new crontab`. Перевір:

```bash
crontab -l
mkdir -p ~/backup
```

Тека `~/backup` має існувати (rsync створює лише останню теку шляху). Щоб не чекати 13:00, тимчасово постав
`*/2 * * * *` (кожні 2 хвилини), подивись `tail -f ~/cron.log` (Ctrl+C - вийти) і `ls ~/backup/univer`, потім
поверни `0 13`. На флешку - заміни шлях на `/media/evgen/НАЗВА_ФЛЕШКИ/univer/`; якщо флешка не вставлена,
у лозі буде помилка, і це нормально.

`~/backup` на тому самому диску - **тренування** (перевірити, що cron працює). Від смерті диска чи крадіжки
ноутбука така копія не врятує: справжня копія - на флешці чи зовнішньому диску і в git на GitHub (урок 24).

**Крок 6 (за бажанням). at.**

```bash
sudo apt install at
echo "touch ~/at_spratsyuvav" | at now + 1 minute
atq
```

```text
warning: commands will be executed using /bin/sh
job 2 at Wed Nov 18 10:14:00 2026
2	Wed Nov 18 10:14:00 2026 a evgen
```

Через хвилину зʼявиться файл `~/at_spratsyuvav`. Скасувати завдання до запуску - `atrm 2` (номер з `atq`).

## Типові помилки

Якщо Mint українською, bash пише українською - у дужках (справжній запуск з перекладом `language-pack-uk-base`).
Англійський текст для пошуку: `LC_ALL=C bash скрипт.sh`.

- **`bash: ./zdaty.sh: Permission denied`** (`bash: ./zdaty.sh: Відмовлено у доступі`) - забув `chmod +x`. Або
  запускай `bash zdaty.sh`.
- **`cannot execute: required file not found`** (`не вдалося виконати: не знайдено потрібного файла`) при
  `./скрипт.sh` - файл збережено з кінцями рядків Windows (CRLF, напр. скопійовано з Windows-редактора): shebang
  став `#!/bin/bash\r`. Лікується `sed -i 's/\r$//' скрипт.sh`.
- **`[-f: command not found`** (`[-f: команду не знайдено`) - нема пробілів біля дужок: `if [-f "$1"]`. Треба
  `if [ -f "$1" ]`.
- **`$1: unbound variable`** (`$1: неозначена змінна`) - з `set -u` скрипт запустили без аргументу. Перевіряй `$#`
  на початку, як у `zdaty`.
- **`name = 5`** у скрипті - `name: command not found` (`name: команду не знайдено`, урок 22): без пробілів біля
  `=`.
- **zip з повним шляхом.** `zip -qr lr0.zip ~/univer/labs/lr0` кладе в архів увесь шлях і сміття. Справжній
  вміст такого архіву:

```text
        0  2026-11-18 10:11   home/evgen/univer/labs/lr0/
      102  2026-11-18 10:11   home/evgen/univer/labs/lr0/kub.py
      117  2026-11-18 10:11   home/evgen/univer/labs/lr0/kvadrat.py
        0  2026-11-18 10:11   home/evgen/univer/labs/lr0/__pycache__/
      491  2026-11-18 10:11   home/evgen/univer/labs/lr0/__pycache__/kvadrat.cpython-312-pytest-7.4.4.pyc
      476  2026-11-18 10:11   home/evgen/univer/labs/lr0/__pycache__/kub.cpython-312-pytest-7.4.4.pyc
```

  А `python3 -m zipfile -c lr0.zip ~/univer/labs/lr0`, навпаки, лишає лише **останню** теку (`lr0/...`), і назва
  «Прізвище_..._ЛР0» в архіві не зʼявиться. Тому `zdaty` робить теку з потрібною назвою і пакує з її батьківської
  теки (`cd`). Числа `102`, `117` - розміри файлів у байтах, у тебе свої.
- **cron «не працює», а руками працює** - майже завжди PATH: у cron нема `~/.local/bin` і venv. Справжній запис
  у тестовій Mint, коли в cron написали просто `univer` (аліас з уроку 03):

```text
/bin/sh: 1: univer: not found
```

  А PATH, з яким cron запускає команди (теж з тестової Mint):

```text
PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/games:/usr/local/games:/snap/bin
```

- **`date +%F` у crontab** - команда тихо не виконається (у тестовій Mint файл виводу навіть не створився).
  Треба `date +\%F`.
- **Нема `>> ~/cron.log 2>&1`** - помилки cron відправляє «поштою», якої на ноутбуці нема, і вони губляться.
- **Чужий скрипт з інтернету** - спершу `less скрипт.sh` і `shellcheck`, а не одразу `bash` (урок 25).

## Як роблять профі

- **`set -euo pipefail` + shellcheck - стандарт для bash-скриптів.** Google Shell Style Guide радить bash-скрипти
  лише для невеликих утиліт, а все, що довше за ~100 рядків, - писати іншою мовою (для нас - Python).
- **Таймери systemd замість cron** на нових системах: видно в `systemctl list-timers`, журнал - у `journalctl`,
  пропущені запуски доганяються (`Persistent=true`). Урок 20.
- **Резервні копії автоматично і не лише на тому самому диску** - правило 3-2-1 (урок 25). cron + rsync на інший
  диск або флешку - найпростіший варіант.
- **Скрипт = документація.** Те, що робиш перед кожною здачею, записане в `zdaty`, - через місяць не треба
  згадувати, як правильно пакувати.

## Самоперевірка

1. Навіщо перший рядок `#!/bin/bash` і що робить `chmod +x`?
2. Що дає `set -euo pipefail` (кожна з трьох частин)?
3. Чому в `zdaty` перед `zip` стоїть `cd "$tmp"`, і що буде без нього?
4. Запиши рядок crontab: щопʼятниці о 18:00 запускати `/home/evgen/.local/bin/zdaty 3`, вивід і помилки - у
   `/home/evgen/cron.log`.
5. Скрипт працює в терміналі, а з cron - ні. Що перевірити першим?

<details markdown="1"><summary>Відповіді</summary>

1. Shebang каже системі, що файл треба виконувати через bash, коли запускаєш `./скрипт`. `chmod +x` дає дозвіл
   на виконання.
2. `-e` - зупинитись на першій помилці; `-u` - помилка, якщо використати змінну, якої нема; `pipefail` - пайп
   вважається невдалим, якщо впала будь-яка його команда (а не лише остання).
3. zip кладе в архів шлях так, як його передали. З `cd` і короткою назвою в архіві буде лише
   `Прізвище_Імʼя_Група_ЛРn/...`; без нього - увесь шлях `home/evgen/...` (або зламана назва).
4. `0 18 * * 5 /home/evgen/.local/bin/zdaty 3 >> /home/evgen/cron.log 2>&1`. (Хоча `zdaty` може спитати y/n - у
   cron відповісти нікому, тож питання завершиться помилкою; для cron краще команди без питань.)
5. Повні шляхи (PATH у cron короткий: нема `~/.local/bin`, venv, аліасів), чи є `>> лог 2>&1`, і `%` у рядку.
   Потім читати `~/cron.log`.

</details>

## Джерела

- crontab(5) Ubuntu 24.04 (поля, `%` як новий рядок) - https://manpages.ubuntu.com/manpages/noble/en/man5/crontab.5.html -
  відкрито 18.11.2026
- Список пакетів ISO Mint 22.3 (cron, anacron, zip, unzip є; at, shellcheck нема) -
  https://mirrors.kernel.org/linuxmint/stable/22.3/ - відкрито 18.11.2026
- ShellCheck - https://www.shellcheck.net/ - відкрито 18.11.2026
- Google Shell Style Guide - https://google.github.io/styleguide/shellguide.html - відкрито 18.11.2026
- systemd.timer (`Persistent=`) - https://www.freedesktop.org/software/systemd/man/latest/systemd.timer.html -
  відкрито 18.11.2026
- Попередній курс «Linux» (тека `05_Програмування/Linux`), День 10 і «Практика», завдання 3 (zibraty.sh, пастка `python -m zipfile -c`) - повторно
  перевірено в тестовій Mint 22.3
- Усі показані виводи (zdaty, zip, crontab -e, PATH у cron, `%`, at) - запуском у тестовій Mint 22.3
  (bash 5.2.21, cron 3.0pl1, zip 3.0, shellcheck 0.9.0), 18.11.2026
