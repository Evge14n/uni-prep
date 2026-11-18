# Урок 27. VS Code або VSCodium (пізніше, за бажанням)

[← Усі уроки](#/u/mint/uroky)

**Навіщо:** коли лаби в терміналі вже йдуть упевнено, зручний редактор пришвидшить роботу: підказки, підсвітка
помилок, налагоджувач мишкою. Але лаби і далі перевіряєш у терміналі, а розуміти кожен рядок мусиш сам.

## Коротко

**Спершу - чому «пізніше».** Викладач перевіряє розуміння коду, а лаби ти вчишся робити без VS Code (уроки 03-12).
Редактор - зручність, не заміна вмінню. І ще: у VS Code вбудовані ШІ-функції (чат, «inline suggestions» -
редактор сам дописує код). Під час лаб їх **вимикай** (налаштування `chat.disableAIFeatures`, крок 4): дописаний
ШІ код ти не поясниш викладачу.

**Що вибрати:**

| | VS Code | VSCodium |
|---|---|---|
| Хто робить | Microsoft | спільнота, з того самого коду |
| Телеметрія Microsoft | є (можна вимкнути) | вирізана |
| Магазин розширень | Microsoft Marketplace | Open VSX (`ms-python.python` там є) |
| Як ставити на Mint | офіційний .deb з code.visualstudio.com | apt-репозиторій VSCodium |
| Команда в терміналі | `code` | `codium` |

> **Нове тут:**
>
> - `code` - відкриває файл або теку у VS Code. Назва: code - від Visual Studio Code («код»).
>
> **Як читати:**
>
> - Слово з мінусом (як `-m` тут) - **прапорець**: уточнює, що саме зробити команді.
> - Якщо поруч у дужках стоїть довга назва з двома мінусами - це той самий прапорець, пиши будь-яку одну.
> - Символи `~` `|` `>` `&` `*` набирай в англійській розкладці (`~` - Shift і клавіша ліворуч від 1; `|` - Shift і клавіша `\`).
>
> Усе про кожну команду - у довіднику «05_Програмування/КОМАНДИ - довідник.md» (на сайті - вкладка «Команди»).

**Чому не з «Керування програмами».** VS Code там - **неофіційний** Flatpak `com.visualstudio.code` з позначкою «Not
verified», тому Mint його ховає (урок 16). Його README на Flathub сам попереджає: Flatpak працює в ізольованому
середовищі (sandbox), і вбудований термінал за замовчуванням працює всередині пісочниці - щоб дістатись до
системних програм, треба `flatpak-spawn --host` або `host-spawn`. Для лаб з venv у `~/univer/.venv` це зайвий клопіт.
Тому - .deb (VS Code) або apt-репозиторій (VSCodium): тоді оновлення приходять через «Диспетчер оновлень».

**Що налаштувати (крок 3-4):** розширення Python, інтерпретатор `~/univer/.venv/bin/python`, лінійка на 78
символів, black при збереженні, ШІ вимкнути.

## Передбач, потім запусти

*Спершу відповідай подумки, нічого не запускаючи, і лише тоді розкрий «Відповідь». Файли з цих прикладів зʼявляться в розділі «Руками» нижче - запусти й перевір себе, коли його пройдеш.*

1. Ти поставив VS Code з .deb. Звідки він оновлюватиметься?

<details markdown="1"><summary>Відповідь</summary>

З «Диспетчера оновлень», разом з усією системою. Документація VS Code: «The .deb package prompts to install the apt
repository and signing key, which enables auto-update through the system package manager» - під час установки
.deb спитає, чи додати репозиторій Microsoft; відповідай «Yes». Без репозиторію завантажений .deb сам не
оновлюється.

</details>

2. У VS Code вибрано інтерпретатор `/usr/bin/python3`, а не venv. Що буде, коли натиснеш «Run» для лаби з
   `import matplotlib`?

<details markdown="1"><summary>Відповідь</summary>

`ModuleNotFoundError: No module named 'matplotlib'` - системний Python не бачить бібліотек з venv (урок 03, той
самий випадок, що «venv вимкнено» в терміналі). Вибери інтерпретатор `~/univer/.venv/bin/python` (крок 3).

</details>

3. Ти поставив точку зупинки (червона крапка) і натиснув F5. Що це за програма зупиняє код - pdb?

<details markdown="1"><summary>Відповідь</summary>

Ні, **debugpy** - налагоджувач з розширення Python Debugger (ставиться разом з розширенням Python). Ідея та сама,
що в pdb з уроків 05-06: зупинка, змінні, крок за кроком. Але на іспиті і на парі в терміналі буде лише pdb -
тому pdb не забувай.

</details>

4. VS Code підкреслює рядок на 85 символів. Чи означає це, що flake8 у терміналі теж скаржитиметься?

<details markdown="1"><summary>Відповідь</summary>

Лише якщо VS Code налаштовано так само (78). Остаточна перевірка - завжди в терміналі: `perevir файл.py` або
`python3 -m flake8 --max-line-length=78 файл.py` (уроки 03-04). Редактор може мати інші налаштування.

> **Нове тут:**
>
> - `perevir` - перевіряє лабу всіма інструментами одразу (doctest, стиль, типи).
> - `python3` - запускає Python: твій файл `.py`, один рядок коду або вбудований інструмент. Назва: Python - на честь комедійного шоу «Monty Python», 3 - третя версія мови. `-m` - запусти модуль Python (вбудований чи поставлений через pip) як програму, напр. `python3 -m venv` (module - «модуль»).
> - `python3 -m flake8` - шукає помилки стилю і зайвий код, нічого не змінює. Назва: pyflakes + pep8: обʼєднав дві старі програми перевірки коду. `--max-line-length` - найбільша дозволена довжина рядка; викладач хоче 78 (типово 79).

</details>

## Руками

**Крок 1 (варіант А). VS Code з офіційного .deb.** Завантаж .deb (кнопка «.deb» на code.visualstudio.com) або
одразу в терміналі:

```bash
cd "$(xdg-user-dir DOWNLOAD)"
wget -O code_latest_amd64.deb "https://code.visualstudio.com/sha/download?build=stable&os=linux-deb-x64"
sudo apt install ./code_latest_amd64.deb
```

> **Нове тут:**
>
> - `cd` - переходить в іншу теку. Назва: change directory - «змінити теку».
> - `"..."` (double quotes) - усе між лапками - одне слово, навіть з пробілами.
> - `$( )` (command substitution) - підставляє вивід команди в рядок.
> - `xdg-user-dir` - друкує шлях до теки завантажень, зображень тощо. Назва: XDG user directory - «тека користувача» за правилами freedesktop.org. `DOWNLOAD` - тека завантажень (туди кладуть файли браузер і Telegram).
> - `wget` - завантажує файл з інтернету за адресою. Назва: World Wide Web + get - «дістати з вебу». `-O` (`--output-document`) - під яким імʼям зберегти файл (output document - «файл для виводу»).
> - `sudo` - виконує одну команду як адміністратор; спитає твій пароль (видно зірочки). Назва: superuser do - «зроби як суперкористувач» (адміністратор).
> - `apt install` - ставить програму з інтернету; на «Бажаєте продовжити? [Y/n]» - Enter. Назва: `apt` - Advanced Package Tool - «розширений інструмент для пакетів (програм)».

Файл близько 300 МБ. Під час установки зʼявиться питання про репозиторій Microsoft - **Yes** (автооновлення).
Подвійний клік по .deb у Nemo теж працює - відкриється Captain (урок 16).

**Крок 1 (варіант Б). VSCodium з його apt-репозиторію.** Команди - з vscodium.com, варіант «Ubuntu 24.04 or newer»
(Mint 22.3 = Ubuntu 24.04). Єдина зміна: на сайті ключ записують командою `dd`, тут - `tee`, результат той самий.

```bash
wget -qO - https://gitlab.com/paulcarroty/vscodium-deb-rpm-repo/raw/master/pub.gpg | gpg --dearmor | sudo tee /usr/share/keyrings/vscodium-archive-keyring.gpg > /dev/null
echo -e 'Types: deb\nURIs: https://download.vscodium.com/debs\nSuites: vscodium\nComponents: main\nArchitectures: amd64 arm64\nSigned-by: /usr/share/keyrings/vscodium-archive-keyring.gpg' | sudo tee /etc/apt/sources.list.d/vscodium.sources
sudo apt update && sudo apt install codium
```

> **Нове тут:**
>
> - `wget`: `-q` (`--quiet`) - нічого не писати (quiet - «тихо»).
> - `|` (pipe) - вивід лівої команди йде на вхід правої.
> - `gpg` - шифрує і підписує файли; для apt перетворює ключ у потрібний вигляд. Назва: GNU Privacy Guard - «охоронець приватності GNU». `--dearmor` - зняти «броню»: текстовий ключ (`-----BEGIN PGP ...`) перетворити на двійковий, як хоче apt.
> - `tee` - показує вивід і одночасно пише у файл. Назва: tee - трійник у трубах (літера T): потік іде у два боки.
> - `>` (redirect) - пише вивід у файл, старий вміст стирає.
> - `echo` - друкує на екран текст, який йому дали. Назва: echo - «луна»: повторює те, що йому дали. `-e` - розуміти `\n` (новий рядок) і `\t` (таб) всередині тексту (escapes - «спецсимволи»).
> - `'...'` (single quotes) - текст буквально: `$`, `*` і пробіли всередині - звичайні символи.
> - `apt update` - завантажує свіжий список програм і версій, нічого не ставить.
> - `&&` (AND) - друга команда - лише якщо перша вдалась.

Що тут відбувається: 1) завантажити ключ, яким підписано репозиторій, перетворити (`--dearmor`) і покласти в
`/usr/share/keyrings/`; 2) записати файл репозиторію `vscodium.sources`; 3) оновити список пакетів і поставити
`codium`. Перший рядок довгий - копіюй цілим. (Альтернатива - перевірений Flatpak `com.vscodium.codium`, але з тією
самою пісочницею.)

**Крок 2. Розширення Python.** Відкрий редактор (меню або `code` / `codium` у терміналі), Ctrl+Shift+X, знайди
**Python** від Microsoft (`ms-python.python`) → Install. Або в терміналі:

```text
code --install-extension ms-python.python
codium --install-extension ms-python.python
```

(перше - для VS Code, друге - для VSCodium). Разом з ним стане Python Debugger (debugpy). Для форматування
поставиться окреме розширення `ms-python.black-formatter` - його ж пошукай і встанови.

**Крок 3. Відкрити теку лаб і вибрати venv.**

```text
code ~/univer/labs          (або codium ~/univer/labs)
```

Ctrl+Shift+P → набери `Python: Select Interpreter` → вибери `~/univer/.venv/bin/python` (якщо нема в списку -
«Enter interpreter path» і впиши `/home/evgen/univer/.venv/bin/python`). Вибраний Python видно в рядку стану внизу.

**Крок 4. Налаштування.** Ctrl+Shift+P → `Preferences: Open User Settings (JSON)`. Файл лежить у
`~/.config/Code/User/settings.json` (у VSCodium - `~/.config/VSCodium/User/settings.json`). Між фігурними дужками
допиши:

```text
{
    "editor.rulers": [78],
    "[python]": {
        "editor.defaultFormatter": "ms-python.black-formatter",
        "editor.formatOnSave": true
    },
    "black-formatter.args": ["--line-length", "78"],
    "chat.disableAIFeatures": true
}
```

- `editor.rulers` - вертикальна лінія на 78-му символі (як вимагає викладач);
- `formatOnSave` + black - код форматується при кожному Ctrl+S (з тими самими 78);
- `chat.disableAIFeatures` - вимикає і ховає чат та ШІ-підказки (за документацією VS Code).

**Крок 5. Вбудований термінал - і перевірка лаби там.** View → Terminal або ``Ctrl+` `` (Ctrl і клавіша з тильдою під Esc).
Він відкривається в теці лаб. Увімкни venv і перевір, як завжди:

```bash
source ~/univer/.venv/bin/activate
cd ~/univer/labs/lr1
python3 -m pytest --doctest-modules -q lr1_1.py
python3 -m flake8 --max-line-length=78 lr1_1.py
```

> **Нове тут:**
>
> - `source` - виконує команди з файлу просто в цьому вікні термінала. Назва: source - «джерело». `~/univer/.venv/bin/activate` - увімкнути venv (окремий Python для лаб); вимкнути - deactivate.
> - `~` (tilde) - твоя домашня тека, /home/evgen.
> - `python3 -m pytest` - проганяє тести (приклади `>>>`) і чесно каже: усе пройшло чи ні. Назва: py + test - «тести для Python». `--doctest-modules` - шукати doctest (приклади `>>>`) у файлах `.py`; без нього pytest шукає лише функції `test_`; `-q` (`--quiet`) - коротко: крапка за кожен тест і рядок підсумку «1 passed in 0.01s».

(або `perevir lr1_1.py`, урок 03). Зелена галочка в редакторі - не перевірка. Перевірка - ці команди.

**Крок 6. Налагоджувач мишкою.** Відкрий будь-який файл з уроку 05 (напр. `period.py`), клацни ліворуч від номера
рядка - зʼявиться червона крапка (точка зупинки). F5 → «Python Debugger» → «Python File». Код зупиниться на
крапці; ліворуч - змінні, угорі - кнопки «крок» (F10), «у функцію» (F11), «продовжити» (F5). Порівняй з pdb:
`n` = F10, `s` = F11, `c` = F5, `p змінна` = панель змінних.

## Типові помилки

- **`ModuleNotFoundError` у VS Code, а в терміналі все працює** - вибрано не той інтерпретатор (крок 3).
- **Поставив VS Code з «Керування програмами» (Flatpak)**, і термінал у ньому «не бачить» venv чи системних програм -
  це пісочниця Flatpak. Видали Flatpak-версію і постав .deb (варіант А).
- **Два VS Code одночасно** (Flatpak і .deb) - плутанина з налаштуваннями й розширеннями. Лиши один.
- **`E: Unsupported file ./code_*.deb given on commandline`** (українською `E: У командному рядку задано
  непідтримуваний файл ./code_*.deb`; англійською - `sudo LC_ALL=C apt install ...`) - у поточній теці нема
  такого файлу (ти не в «Завантаженнях»). `cd` у теку з файлом, `ls *.deb`.
- **`E: Unable to locate package code_latest_amd64.deb`** (`E: Не можу знайти пакунок code_latest_amd64.deb`) -
  забув `./` перед іменем, і apt шукає пакет з такою назвою в репозиторії, а не файл.
- **Розширення не знаходиться у VSCodium** - там Open VSX, не Microsoft Marketplace. `ms-python.python`,
  `ms-python.debugpy` і `ms-python.black-formatter` на Open VSX є (перевірено 18.11.2026); Pylance - не перевірено.
- **ШІ дописав код у лабу** - видали і напиши сам. Перевір налаштування `chat.disableAIFeatures`.
- **black «зіпсував» doctest викладача?** Ні: у docstring black лише прибирає пробіли в кінці рядків, а приклади
  doctest не міняє. Довгі рядки doctest лишаться довгими (урок 04, п. 12) - це нормально.

  > **Нове тут:**
  >
  > - `;` (semicolon) - розділяє команди в рядку, виконує всі по черзі.
  > - `ls` - показує, що лежить у теці. Назва: list - «список» (вмісту теки).
  > - `*` (asterisk) - будь-які символи в назві; bash сам замінює `*` на список файлів.

## Як роблять профі

- **Редактор + термінал, а не редактор замість термінала.** Тести, лінтери і git запускають командами, щоб так само
  працювало в CI (GitHub Actions) і на будь-якому компʼютері.
- **Налаштування в settings.json**, а не «наклацані» мишкою - їх легко перенести і зберегти.
- **Офіційне джерело пакета.** .deb від Microsoft з його apt-репозиторієм або репозиторій VSCodium, не
  неперевірений Flatpak.
- **Курс MIT «Missing Semester» 2026** має окрему лекцію про середовище розробки (Development Environment and
  Tools) і окрему - про ШІ-агентів (Agentic Coding): інструменти міняються, а навички термінала лишаються.

## Самоперевірка

1. Чому VS Code краще ставити з .deb, а не з «Керування програмами»?
2. Що зробити, щоб VS Code запускав лаби з бібліотеками з `~/univer/.venv`?
3. Які три налаштування з кроку 4 пов'язані з вимогами викладача?
4. Чим debugpy у VS Code схожий на pdb і чому pdb все одно треба знати?
5. Як остаточно перевірити лабу перед здачею, навіть якщо в редакторі все «зелене»?

<details markdown="1"><summary>Відповіді</summary>

1. У «Керування програмами» - неофіційний Flatpak («Not verified»), з пісочницею, через яку вбудований термінал не бачить
   системних програм і venv. .deb - від Microsoft і з репозиторієм для автооновлень.
2. Ctrl+Shift+P → `Python: Select Interpreter` → `~/univer/.venv/bin/python`.
3. `editor.rulers: [78]` і black з `--line-length 78` (довжина рядка до 78) і `chat.disableAIFeatures` (свій код
   без ШІ).
4. Обидва зупиняють програму, показують змінні і ведуть крок за кроком (F10 = `n`, F11 = `s`, F5 = `c`). pdb
   працює в будь-якому терміналі, і на парі чи іспиті буде саме він.
5. У терміналі: `python3 -m pytest --doctest-modules`, `python3 -m flake8 --max-line-length=78`, mypy (або
   `perevir файл.py`), як в уроках 03-04.

</details>

## Джерела

- VS Code на Linux (.deb, репозиторій, автооновлення) - https://code.visualstudio.com/docs/setup/linux -
  відкрито 18.11.2026; посилання на завантаження .deb (стабільна 1.147.0 на 18.11.2026) -
  https://code.visualstudio.com/sha/download?build=stable&os=linux-deb-x64
- VS Code: інтерпретатор - https://code.visualstudio.com/docs/python/environments ; налагодження (debugpy) -
  https://code.visualstudio.com/docs/python/debugging ; форматування (black, formatOnSave) -
  https://code.visualstudio.com/docs/python/formatting ; шлях settings.json - https://code.visualstudio.com/docs/configure/settings ;
  термінал (``Ctrl+` ``) - https://code.visualstudio.com/docs/terminal/getting-started ; вимкнути ШІ
  (`chat.disableAIFeatures`) - https://code.visualstudio.com/docs/copilot/setup - відкрито 18.11.2026
- VSCodium, встановлення на Debian/Ubuntu - https://vscodium.com/ - відкрито 18.11.2026
- Неофіційний Flatpak VS Code, README про пісочницю - https://github.com/flathub/com.visualstudio.code -
  відкрито 18.11.2026
- Розширення Python на Open VSX - https://open-vsx.org/extension/ms-python/python - відкрито 18.11.2026
- ФАКТИ Mint 22.3: Flatpak VS Code «Not verified», Captain для .deb, VSCodium (`_джерело/ФАКТИ-MINT-22.3.md`)
- Не перевірено в тестовій Mint (нема графічного робочого столу): сам запуск VS Code / VSCodium, розширення,
  налаштування, налагоджувач. Перевірено: синтаксис команд, що команди існують, адреси відповідають, ключ VSCodium
  справжній і підписує репозиторій, JSON налаштувань коректний.
