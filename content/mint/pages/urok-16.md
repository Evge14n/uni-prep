# Урок 16. Програми - apt, «Керування програмами», Flatpak, deb, PPA

[← Усі уроки](#/u/mint/uroky)

**Навіщо:** ставити і прибирати програми так, щоб вони оновлювались самі і не ламали систему. У Mint є чотири шляхи
(apt, Flatpak, .deb з сайту, PPA) - тут, який брати першим і чого боятись.

## Коротко

**Пакет** - архів з програмою і списком того, що їй потрібно (залежності). **Сховище** (репозиторій) - сервер з
тисячами перевірених пакетів, звідки система бере і програми, і їх оновлення.

| Шлях | Звідки | Хто оновлює | Коли брати |
|---|---|---|---|
| **apt** (системний пакет) | сховища Ubuntu 24.04 і Mint | Диспетчер оновлень | **першим**: python3-..., git, gnuplot, ncdu |
| **Flatpak** | Flathub | Диспетчер оновлень (у тому ж списку) | коли в apt нема або версія дуже стара (Telegram, Zoom, OBS) |
| **.deb з сайту** | сайт розробника | лише якщо пакет додав своє сховище | коли нема ні в apt, ні у Flatpak |
| **PPA** | особисте сховище на Launchpad | Диспетчер оновлень | рідко і обережно |

Практики r/linuxmint (16.01.2026, 42 бали) кажуть коротко: **«Deb if available, flatpak if not»** - системний пакет,
якщо є, інакше Flatpak.

**apt у Mint - обгортка.** Команда `apt` у Mint - це не справжній apt, а скрипт Mint `/usr/local/bin/apt`. Він сам
додає `sudo` (тому `apt install` питає пароль і без `sudo`) і вміє більше. Справжній - `/usr/bin/apt`.

> **Нове тут:**
>
> - `apt install` - ставить програму з інтернету; на «Бажаєте продовжити? [Y/n]» - Enter. Назва: `apt` - Advanced Package Tool - «розширений інструмент для пакетів (програм)».
>
> **Як читати:**
>
> - Слово з мінусом (як `-S` тут) - **прапорець**: уточнює, що саме зробити команді.
> - Якщо поруч у дужках стоїть довга назва з двома мінусами - це той самий прапорець, пиши будь-яку одну.
> - Символи `|` `>` набирай в англійській розкладці (`|` - Shift і клавіша `\`).
>
> Усе про кожну команду - у довіднику «05_Програмування/КОМАНДИ - довідник.md» (на сайті - вкладка «Команди»).

| Команда | Що робить (за обгорткою стоїть) |
|---|---|
| `apt update` | оновити **список** пакетів (`sudo /usr/bin/apt update`) |
| `apt search слово` | пошук (`aptitude search`): `i` - встановлено, `p` - ні |
| `apt show пакет` | опис, розмір, залежності |
| `apt install пакет` | встановити (`sudo /usr/bin/apt install`) |
| `apt remove пакет` | видалити програму, налаштування в `/etc` лишаються |
| `apt purge пакет` | видалити разом із системними налаштуваннями |
| `apt autoremove` | прибрати залежності, що вже нікому не потрібні |
| `apt policy пакет` | яка версія стоїть, яка доступна і **звідки** (`apt-cache policy`) |
| `apt version пакет` | лише встановлена версія |
| `apt held` | пакети, «заморожені» від оновлень |
| `apt contains /шлях/файл` | з якого пакета файл (`dpkg -S`) |
| `apt content пакет` | які файли поставив пакет (`dpkg -L`) |
| `apt deb файл.deb` | поставити .deb (`sudo dpkg -i` - **без** докачування залежностей, див. нижче) |
| `apt help команда` | показати, що насправді виконається |

> **Нове тут:**
>
> - `apt update` - завантажує свіжий список програм і версій, нічого не ставить.
> - `apt search` - шукає програми за словом у назві: `i` - стоїть, `p` - ні.
> - `apt show` - показує опис програми (пакета): версію, розмір, від чого залежить.
> - `apt remove` - видаляє програму, налаштування в /etc лишаються.
> - `apt purge` - видаляє програму разом з її налаштуваннями в `/etc`.
> - `apt autoremove` - прибирає програми, що ставились «за компанію» і вже не потрібні. Назва: auto remove - «автоматично прибрати».
> - `apt policy` - показує версії програми і з якого сховища (сервера) вона береться. Назва: policy - «політика» (яку версію і звідки бере apt).
> - `apt version` - друкує версію встановленої програми (пакета).
> - `apt held` - показує програми (пакети), заморожені від оновлень. Назва: held - «утримані» (заморожені від оновлень).
> - `apt contains` - каже, з якого пакета (програми з набором файлів) прийшов файл. Назва: contains - «містить» (який пакет містить файл).
> - `apt content` - показує, які файли поставила програма (пакет). Назва: content - «вміст» (що всередині пакета).
> - `apt deb` - ставить файл .deb, але без залежностей. Назва: deb - від Debian: так звуться файли пакетів .deb.
> - `apt help` - показує, яку справжню команду запустить `apt` у Mint (з `sudo` чи без).
> - `sudo` - виконує одну команду як адміністратор; спитає твій пароль (видно зірочки). Назва: superuser do - «зроби як суперкористувач» (адміністратор).
> - `apt-cache policy` - показує версії програми (пакета) і звідки вона береться. Назва: apt-cache - «кеш apt» (збережений список пакетів); policy - «політика».
> - `dpkg` - ставить один файл `.deb` і веде список встановлених програм. Назва: Debian package - «пакет Debian». `-S` (`--search`) - з якого пакета файл, те саме, що `apt contains` (search - «шукати»); `-L` (`--listfiles`) - усі файли, які поставив пакет, те саме, що `apt content` (list files - «список файлів»); `-i` (`--install`) - ставить файл `.deb`; залежностей сам не докачує (install - «встановити»).
> - `./скрипт` - запускає програму за шляхом до її файлу, напр. `./файл.sh`. Назва: ./ - «звідси».

Порядок завжди: `apt update`, потім `apt install`. Про оновлення всієї системи - урок 02.

**dpkg** - нижчий рівень: ставить один .deb і веде список встановленого. `dpkg -l пакет` (стан: `ii` = встановлено),
`dpkg -L пакет` (файли), `dpkg -S файл` (чий файл).

> **Нове тут:**
>
> - `dpkg`: `-l` (`--list`) - рядок стану пакета: `ii` - встановлено, `rc` - видалено, лишились налаштування (list - «список»).

**«Керування програмами»** (Software Manager, у меню так і зветься) - «магазин» Mint. Шукає одночасно в apt і на
Flathub. Біля програми видно формат: «Системний пакунок» або Flatpak. Кнопки «Встановити», «Вилучити», «Запуск».
Меню (☰) → «Налаштування»:
- «Коли програма є в різних форматах:» - типово «Показувати всі типи»; можна «Показувати тільки системні пакунки».
- «Показувати неперевірені пакунки Flatpak (не рекомендовано)» - **вимкнено** і так і лишай. Неперевірений
  («Неперевірений Flatpak») - його виклав на Flathub не автор програми, а хтось інший. Mint пише:
  «Не перевірені пакунки Flatpak становлять великий ризик для безпеки». Так, наприклад, захований неофіційний
  Flatpak VS Code.

**Flatpak** - програма разом з усіма бібліотеками в «пісочниці» (окремо від системи). Займає більше місця, зате не
залежить від версії Mint. Flathub у Mint увімкнено одразу для всієї системи; програми лежать у `/var/lib/flatpak`.

| Команда | Що робить |
|---|---|
| `flatpak search назва` | пошук на Flathub |
| `flatpak install flathub ID` | встановити (ID - як `com.github.tchx84.Flatseal`) |
| `flatpak run ID` | запустити з терміналу |
| `flatpak list --app` | встановлені програми |
| `flatpak info ID` | версія, розмір, звідки |
| `flatpak uninstall ID` | видалити |
| `flatpak uninstall --unused` | прибрати бібліотеки (runtimes), які вже нікому не треба |
| `flatpak update` | оновити все (урок 02) |

> **Нове тут:**
>
> - `flatpak search` - шукає програми на Flathub. Назва: `flatpak` - flat pack - «пласка упаковка», як меблі в коробці, які збираєш сам.
> - `flatpak install` - ставить програму з Flathub. `flathub` - назва сховища (remote), звідки брати; у Mint flathub підключено одразу.
> - `flatpak run` - запускає Flatpak-програму за її ID.
> - `flatpak list` - показує встановлені Flatpak-програми. `--app` - лише програми, без спільних бібліотек (runtimes).
> - `flatpak info` - показує версію, розмір і джерело встановленої Flatpak-програми.
> - `flatpak uninstall` - видаляє Flatpak-програму або непотрібні бібліотеки. `--unused` - прибрати спільні бібліотеки (runtimes), які вже не потрібні жодній програмі (unused - «невикористані»).
> - `flatpak update` - оновлює всі Flatpak-програми.

**Flatseal** (`com.github.tchx84.Flatseal`, перевірений на Flathub) - вікно, де видно і можна обмежити, що дозволено
кожному Flatpak: доступ до домашньої теки, мережі, камери.

**.deb з сайту.** Подвійний клік відкриває **«Установник пакунків»** (Captain). У терміналі - `sudo apt install ./файл.deb`
(з `./`!): apt сам докачає залежності. Оновлюватись такий пакет буде **лише якщо додав своє сховище** (так роблять
VS Code, Google Chrome). Інакше - нова версія лише вручну з сайту.

**PPA** (Personal Package Archive) - сховище однієї людини чи команди на Launchpad. Ключ PPA доводить лише «звідки
пакет», а не «що він безпечний». Документація Ubuntu: сторонні сховища - найчастіша причина зламаного оновлення
системи. Додати: `sudo add-apt-repository ppa:власник/назва`, прибрати: `--remove`, відкотити його пакети до
офіційних - `ppa-purge`. Мишкою: меню → «Джерела програмного забезпечення» → «Пакунки PPA».

> **Нове тут:**
>
> - `add-apt-repository` - додає чуже сховище програм (напр. PPA), з `-r` прибирає. Назва: add apt repository - «додати сховище для apt».

**Snap** у Mint вимкнено (Mint блокує `snapd`). Не вмикай його навмисно - для того самого є Flatpak.

**AppImage** - один файл-програма: `chmod +x програма.AppImage`, `./програма.AppImage`. Сам не оновлюється, у меню не
зʼявляється. Багатьом старим AppImage потрібна бібліотека FUSE 2: на базі Ubuntu 24.04 пакет зветься `libfuse2t64`.

> **Нове тут:**
>
> - `chmod` - змінює права файлу: хто може читати, змінювати, запускати. Назва: change mode - «змінити режим», тобто права доступу файлу. `+x` - `+` - додати право, `x` (execute - «виконувати») - запускати файл як програму; без u/g/o - власнику, групі й іншим.

**Python-програми** (не бібліотеки для лаб!), як `uv` чи `ruff`, ставлять через `pipx` - урок 02. Не `sudo pip`.

> **Нове тут:**
>
> - `pip` - ставить, оновлює і видаляє бібліотеки Python (у venv). Назва: pip installs packages - «pip ставить пакети» (назва, що посилається сама на себе).

**Вільні програми (FOSS) і ліцензії.** Майже все в Mint - вільне і відкрите програмне забезпечення (FOSS - Free and
Open Source Software): код відкритий, його можна читати, змінювати і поширювати. Умови пише **ліцензія**: GPL
(bash, coreutils, nano, git, ядро Linux) дозволяє все це, але змінену версію, яку поширюєш, теж треба давати з кодом;
MIT, BSD, Apache - дозволяють майже все, аби лишили імʼя автора. Ліцензія кожного пакета лежить у
`/usr/share/doc/ПАКЕТ/copyright`, повні тексти - у `/usr/share/common-licenses/`:

```bash
grep -m1 "^License:" /usr/share/doc/bash/copyright /usr/share/doc/git/copyright
ls /usr/share/common-licenses/ | head -5
```

```text
/usr/share/doc/bash/copyright:License: GPL-3+
/usr/share/doc/git/copyright:License: GPL-2
Apache-2.0
Artistic
BSD
CC0-1.0
GFDL
```

> **Нове тут:**
>
> - `grep` - шукає рядки з текстом (у файлах або те, що прийшло через `|`). Назва: g/re/p з редактора ed: global regular expression print - «скрізь знайти шаблон, надрукувати». `-m` (`--max-count`) - зупинитись після стількох збігів: -m1 - лише перший (max count - «найбільше»); `^` на початку шаблону - «рядок починається з цього тексту».
> - `"..."` (double quotes) - усе між лапками - одне слово, навіть з пробілами.
> - `ls` - показує, що лежить у теці. Назва: list - «список» (вмісту теки).
> - `|` (pipe) - вивід лівої команди йде на вхід правої.
> - `head` - показує перші рядки файлу (або того, що прийшло через `|`). Назва: head - «голова». `-5` - лише 5 перші рядки (те саме, що `-n 5`).

Невільне (закрите) теж буває: драйвер NVIDIA (урок 17), частина прошивок і кодеків. Mint ставить його окремо і
питає. Сховища Ubuntu поділені на частини `main restricted universe multiverse` (усі чотири ввімкнені у файлі
`/etc/apt/sources.list.d/official-package-repositories.list`); у `restricted` і `multiverse` - те, що має обмеження
ліцензії (поділ за ліцензіями - зі слів документації Ubuntu, тут не перевірено).

## Передбач, потім запусти

*Спершу відповідай подумки, нічого не запускаючи, і лише тоді розкрий «Відповідь». Файли з цих прикладів зʼявляться в розділі «Руками» нижче - запусти й перевір себе, коли його пройдеш.*

1. Що насправді зробить `apt install` у Mint?

```bash
apt help install
```

> **Нове тут:**
>
> - `apt help`: `install` - `apt help install` покаже, що install іде через `sudo /usr/bin/apt install`.

<details markdown="1"><summary>Відповідь</summary>

```text
"apt install " is equivalent to "sudo /usr/bin/apt install"
```

Обгортка Mint сама додала `sudo`. Тому `apt install` питає пароль, навіть якщо ти не писав `sudo`.

</details>

2. Скільки програм на імʼя `apt` знайде bash?

```bash
type -a apt
```

> **Нове тут:**
>
> - `type` - каже, що це за команда і де вона. Назва: type - «тип». `-a` - показати всі варіанти з цією назвою, а не лише той, що запуститься (all - «усі»).

<details markdown="1"><summary>Відповідь</summary>

```text
apt is /usr/local/bin/apt
apt is /usr/bin/apt
apt is /bin/apt
```

Першою в PATH стоїть `/usr/local/bin`, тому запускається обгортка Mint. `/bin/apt` - той самий файл, що
`/usr/bin/apt` (у Mint `/bin` - посилання на `/usr/bin`).

</details>

3. А `apt deb` - те саме, що `sudo apt install ./файл.deb`?

```bash
apt help deb
```

> **Нове тут:**
>
> - `apt help`: `deb` - `apt help deb` покаже, що deb = `sudo dpkg -i` (без докачування залежностей).

<details markdown="1"><summary>Відповідь</summary>

```text
"apt deb " is equivalent to "sudo dpkg -i"
```

Ні. `dpkg -i` ставить лише сам файл і **не докачує залежності**. Якщо їх бракує, пакет лишиться недоналаштованим, і
доведеться `sudo apt-get install -f`. Тому краще `sudo apt install ./файл.deb`.

> **Нове тут:**
>
> - `apt-get install` - ставить програму (пакет); з `-f` лагодить зламані залежності. Назва: `apt-get` - apt (Advanced Package Tool) + get - «дістати»; apt-get - «apt, дістань»; install - «встановити». `-f` (`--fix-broken`) - докачує залежності, яких бракує, і доналаштовує пакети (fix broken - «полагодити зламане»).

</details>

4. Ти поставив програму, а `apt install` у сусідньому вікні ще працює (або Диспетчер оновлень ставить оновлення).
   Що скаже друга команда?

<details markdown="1"><summary>Відповідь</summary>

`apt` (у тому числі обгортка Mint) чекає і пише щокілька секунд:

```text
Waiting for cache lock: Could not get lock /var/lib/dpkg/lock-frontend. It is held by process 2915 (python3)...
```

а `apt-get` одразу здається:

```text
E: Could not get lock /var/lib/dpkg/lock-frontend. It is held by process 2957 (python3)
E: Unable to acquire the dpkg frontend lock (/var/lib/dpkg/lock-frontend), is another process using it?
```

Номер і назва процесу в дужках у тебе будуть свої (наприклад, Диспетчер оновлень). Пакети одночасно ставить лише
одна програма. Зачекай, поки та закінчить.

</details>

## Руками

**Крок 1. Подивись, що в тебе стоїть і звідки.**

```bash
apt version python3
dpkg -S /usr/bin/python3
apt contains /usr/bin/nano
dpkg -L nano | grep bin
apt list --installed | wc -l
```

```text
3.12.3-0ubuntu2.1
python3-minimal: /usr/bin/python3
nano: /usr/bin/nano
/usr/bin
/usr/bin/nano
/usr/bin/rnano
```

> **Нове тут:**
>
> - `apt version`: `python3` - версія системного Python (3.12.3...) - той, що не можна видаляти.
> - `apt list` - показує список програм (пакетів): встановлених або з оновленнями. `--installed` - лише пакети, що вже стоять у системі (installed - «встановлені»).
> - `dpkg`: `/usr/bin/python3` - `dpkg -S /usr/bin/python3` - з якої програми (пакета) прийшов системний Python.
> - `wc` - рахує рядки, слова, символи. Назва: word count - «підрахунок слів»; рахує ще рядки й байти. `-l` (`--lines`) - лише кількість рядків (lines - «рядки»).

Версія у тебе може бути новішою. Остання команда покаже число пакетів (на свіжій Mint 22.3 близько двох тисяч:
в образі 2005) і ще попередження `WARNING: apt does not have a stable CLI interface. Use with caution in scripts.` -
це apt нагадує, що його вивід не для скриптів; на число воно не впливає.

**Крок 2. Звідки пакет.**

```bash
apt policy nano
```

```text
nano:
  Installed: 7.2-2ubuntu0.2
  Candidate: 7.2-2ubuntu0.2
  Version table:
 *** 7.2-2ubuntu0.2 500
        500 http://archive.ubuntu.com/ubuntu noble-updates/main amd64 Packages
        500 http://security.ubuntu.com/ubuntu noble-security/main amd64 Packages
        100 /var/lib/dpkg/status
     7.2-2build1 500
        500 http://archive.ubuntu.com/ubuntu noble/main amd64 Packages
```

`Installed` - що стоїть, `Candidate` - що поставиться при оновленні, `***` - поточна. Рядки з адресами - звідки
пакет (тут сховище Ubuntu, у тебе адреса може бути дзеркалом, наприклад українським). Якщо під версією лише
`100 /var/lib/dpkg/status` - пакет **нізвідки** («сторонній»): його поставили з .deb, і оновлень він не отримає.
Список усіх таких:

```bash
apt list --installed 2>/dev/null | grep ",local]"
```

> **Нове тут:**
>
> - `2>` (redirect stderr) - пише лише помилки у файл.

На свіжій системі - порожньо.

**Крок 3. Поставити і прибрати програму.**

```bash
apt update
apt search cowsay
apt show cowsay
apt install cowsay
cowsay "Привіт, Mint"
apt remove cowsay
apt autoremove
```

> **Нове тут:**
>
> - `apt remove`: `cowsay` - пакет-іграшка (корова в терміналі): на ньому зручно вчитись ставити і прибирати програми.
> - `cowsay` - корова в терміналі каже твій текст (іграшка для вправ). Назва: cow say - «корова каже».

`apt install` покаже, що поставить і скільки місця займе, і спитає `Do you want to continue? [Y/n]` (українською
`Бажаєте продовжити?`) - прочитай і натисни Enter. `cowsay` намалює корову з твоїм текстом. Після `remove` команда `cowsay` зникне.

Те саме мишкою: меню → «Керування програмами» → пошук `cowsay` → «Встановити» → «Вилучити».

**Крок 4. Flatpak: Flatseal.**

```bash
flatpak --installations
flatpak install flathub com.github.tchx84.Flatseal
flatpak list --app
flatpak run com.github.tchx84.Flatseal
```

> **Нове тут:**
>
> - `flatpak`: `--installations` - друкує, куди ставляться Flatpak-програми для всієї системи.
> - `flatpak install`: `com.github.tchx84.Flatseal` - ID програми: перевернута адреса автора + назва, з точними великими літерами.
> - `flatpak run`: `com.github.tchx84.Flatseal` - ID Flatseal - програми, де видно дозволи кожного Flatpak.

Перша команда покаже `/var/lib/flatpak` - туди Mint ставить Flatpak для всієї системи. `install` спитає підтвердження
і, можливо, докачає runtime (спільні бібліотеки). У Flatseal зліва список Flatpak-програм, справа - їхні дозволи.
Видалити:

```bash
flatpak uninstall com.github.tchx84.Flatseal
flatpak uninstall --unused
```

У «Керування програмами» той самий Flatseal позначено як Flatpak, а для програм, що є в обох форматах, видно обидва
варіанти.

**Крок 5. .deb з сайту** (коли справді треба). Спершу перевір, чи нема програми в «Керування програмами». Нема -
завантаж `.deb` з **офіційного** сайту і:

```text
sudo apt install ./назва_файлу.deb
```

Потім подивись, чи пакет додав своє сховище (тоді він оновлюватиметься):

```bash
ls /etc/apt/sources.list.d/
```

Файли `official-...` - офіційні сховища Mint. Зʼявився новий файл з назвою програми чи фірми - пакет
оновлюватиметься разом із системою.

**Крок 6. PPA - лише подивитись.**

```bash
add-apt-repository --help | grep remove
```

```text
  -r, --remove  Remove the specified repository
```

> **Нове тут:**
>
> - `add-apt-repository`: `--help` - коротка довідка: які є параметри.

Відкрий меню → «Джерела програмного забезпечення» (спитає пароль). Вкладки: «Офіційні репозиторії», «Пакунки PPA»,
«Додаткові сховища», «Ключі автентифікації», «Обслуговування». На останній - «Вилучити сторонні пакунки» і
«Понизити сторонні пакунки»: так після проблемного PPA повертають усе до офіційних версій. Нічого не міняй, просто закрий.

## Типові помилки

Якщо Mint українською, apt і dpkg пишуть українською - варіант у дужках (перші два - справжній запуск у тестовій Mint
з перекладом `language-pack-uk-base`, решта - з того самого файлу перекладу). Англійський текст для пошуку:
`LC_ALL=C команда`.

- **`E: Unable to acquire the dpkg frontend lock (/var/lib/dpkg/lock-frontend), are you root?`**
  (`E: Неможливо здобути блокування клієнтської частини (/var/lib/dpkg/lock-frontend), ви маєте root-права?`) -
  запустив `apt-get install` (або справжній `/usr/bin/apt`) без `sudo`. Обгортка `apt` у Mint додає `sudo` сама,
  `apt-get` - ні.
- **`E: Unable to locate package nema-takoho`** (`E: Не можу знайти пакунок nema-takoho`) - нема такого пакета або
  давно не було `apt update`. Перевір назву (`apt search`), зроби `apt update`.
- **`Could not get lock /var/lib/dpkg/lock-frontend`** (`Не вдалося заблокувати /var/lib/dpkg/lock-frontend.
  Утримується процесом ...`, передбач 4) - інша програма вже ставить пакети. Зачекай. `dpkg` у такому разі прямо
  пише: `Note: removing the lock file is always wrong, can damage the locked area` (`Примітка: видаляти файл
  блокування завжди неправильно, це може пошкодити заблоковану область`) - lock-файли **не видаляють**.
- **`E: dpkg was interrupted, you must manually run 'sudo dpkg --configure -a' to correct the problem.`**
  (`E: dpkg було перервано, ви повинні вручну запустити 'sudo dpkg --configure -a' аби виправити проблему.`) -
  установку перервали (закрили вікно, вимкнулось світло). Лікування:

```bash
sudo dpkg --configure -a
sudo apt-get install -f
```

> **Нове тут:**
>
> - `dpkg`: `--configure` - доналаштовує розпаковані пакети; з `-a` - усі, які перервались (configure - «налаштувати»); `-a` (`--pending`) - з `--configure`: усі пакети, що чекають налаштування (pending - «ті, що чекають»).

  Перше доналаштовує обірвані пакети, друге (`-f` = fix) докачує залежності, яких бракує. Те саме після
  `apt deb файл.deb` (`dpkg -i`), коли бракує залежностей.
- **`error: externally-managed-environment` від `pip install`** - не обходь, а став бібліотеки у venv, а програми -
  через pipx (урок 02).
- **Порада з інтернету «додай PPA» для того, що є в apt чи на Flathub** - не треба. Кожен PPA - ризик зламати
  наступне велике оновлення Mint. Додав - запиши собі який, щоб потім прибрати.
- **«Немає програми в "Керуванні програмами"»** - може, вона є лише як неперевірений Flatpak (схований). Пошукай на flathub.org,
  хто його виклав; якщо не автор - краще .deb з офіційного сайту.
- **Видаляти програми, що прийшли з Mint** (наприклад, «щоб звільнити місце») - так ламають систему: `apt remove`
  може потягти за собою пів робочого столу. **Читай список** «The following packages will be REMOVED» («Такі
  пакунки будуть ВИЛУЧЕНІ:») перед тим, як погодитись.
- **Snap «не встановлюється»** - так задумано в Mint; бери Flatpak.

  > **Нове тут:**
  >
  > - `pip install` - ставить бібліотеку Python (лише у venv). Назва: pip installs packages - «pip ставить пакети»; install - «встановити».

## Як роблять профі

- **Одна програма - один формат.** Не ставлять ту саму програму і з apt, і з Flatpak (і тим паче Snap): дві копії,
  плутанина з налаштуваннями, а Snap поруч з .deb на r/linuxmint (18.10.2026) зламав apt.
- **Офіційні джерела першими:** apt → перевірений Flatpak → .deb з офіційного сайту → PPA. Чим нижче, тим більше
  перевіряють, хто автор.
- **Перед PPA або чужим .deb - знімок Timeshift** (урок 01).
- **Дозволи Flatpak переглядають у Flatseal**, особливо доступ до всієї домашньої теки.
- **`apt help команда`** - щоб бачити, що насправді виконає обгортка, перш ніж давати їй `sudo`.
- **Бібліотеки для лаб - у venv, утиліти на Python - у pipx**, системні пакети `python3-...` - лише через apt (урок 02).

## Самоперевірка

1. Чому `apt install ncdu` у Mint питає пароль, хоча ти не писав `sudo`?
2. Як дізнатись, з якого пакета файл `/usr/bin/nano` і звідки (з якого сховища) цей пакет?
3. Чим `sudo apt install ./prog.deb` краще за `apt deb prog.deb`?
4. Програма є і в apt, і на Flathub. Що вибрати і чому?
5. `apt install` пише `Could not get lock /var/lib/dpkg/lock-frontend`. Що робити і чого не робити?

<details markdown="1"><summary>Відповіді</summary>

1. `apt` у Mint - обгортка `/usr/local/bin/apt`, вона сама додає `sudo` до install, remove, update тощо
   (`apt help install` це показує).
2. `apt contains /usr/bin/nano` (або `dpkg -S /usr/bin/nano`) → пакет `nano`; потім `apt policy nano` - адреси
   сховищ під версією.
3. `apt install ./...` докачає залежності; `apt deb` = `sudo dpkg -i`, який їх не ставить (тоді треба
   `sudo apt-get install -f`).
4. Системний пакет (apt): менше місця, оновлюється разом із системою. Flatpak - якщо в apt нема або версія дуже
   стара («Deb if available, flatpak if not»).
5. Зачекати, поки інша програма (Диспетчер оновлень, інше вікно з apt) закінчить. Lock-файли не видаляти.

</details>

## Джерела

- Обгортка `/usr/local/bin/apt` (пакет mintsystem): `apt help ...`, `type -a apt`, `apt version`, `apt contains`,
  повідомлення про lock - перевірено запуском у тестовій Mint 22.3, 18.11.2026
- `_джерело/ФАКТИ-MINT-22.3.md` (Flathub, неперевірені Flatpak, Captain, mintsources, PPA, Snap) - 18.11.2026
- Українські назви - `mintinstall.mo`, `mintsources.mo`, `captain.mo` з mint-translations 2026.01.08 і captain 1.1.2;
  налаштування «Керування програмами» - `prefs.py` і схема `com.linuxmint.install` з mintinstall 8.4.0, перевірено 18.11.2026
- Що нового в Mint 22 (неперевірені Flatpak сховані) - https://www.linuxmint.com/rel_wilma_whatsnew.php - відкрито 18.11.2026
- Сторонні сховища (Ubuntu) - https://documentation.ubuntu.com/server/explanation/software/third-party-repository-usage/ -
  відкрито 18.11.2026
- Snap у Mint, файл `nosnap.pref` - https://linuxmint-user-guide.readthedocs.io/en/latest/snap.html - відкрито 18.11.2026
- Flatseal на Flathub (перевірений: API verification `"verified":true`) - https://flathub.org/apps/com.github.tchx84.Flatseal -
  відкрито 18.11.2026
- AppImage і FUSE 2 (`libfuse2t64` в Ubuntu 24.04) - https://docs.appimage.org/user-guide/troubleshooting/fuse.html -
  відкрито 18.11.2026
- dpkg lock FAQ - https://wiki.debian.org/Teams/Dpkg/FAQ#db-lock - відкрито 18.11.2026
- Українські повідомлення apt/dpkg - `apt.mo`, `libapt-pkg6.0.mo`, `dpkg.mo` з language-pack-uk-base 24.04+20260905,
  перевірено запуском у тестовій Mint 22.3, 18.11.2026; ліцензії - `/usr/share/doc/*/copyright`, `/usr/share/common-licenses`
  у тестовій Mint 22.3, 18.11.2026
- Практики: «Deb if available, flatpak if not» https://www.reddit.com/r/linuxmint/comments/1qeu0rr/ ; .deb без
  сховища сам не оновлюється, Flatseal https://www.reddit.com/r/linuxmint/comments/1xdyslz/ ; Snap і .deb зламали apt
  https://www.reddit.com/r/linuxmint/comments/1x982xk/ ; ключ PPA доводить лише «звідки»
  https://www.reddit.com/r/linuxmint/comments/1sehxf0/ - відкрито 18.11.2026
