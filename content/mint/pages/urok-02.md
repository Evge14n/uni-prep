# Урок 02. Оновлення - система, Flatpak, прошивки, Python

[← Усі уроки](#/u/mint/uroky)

**Навіщо:** оновлення закривають дірки в безпеці і виправляють помилки. Але одне оновлюють регулярно, а одне не чіпають
ніколи: системний Python 3.12 потрібен самій Mint. Тут - що, чим і як часто, і як поставити новіший Python поруч, не зламавши систему.

**Що робити сьогодні, а що пізніше.** Сьогодні (до ЛР1): кроки 1, 2, 3 і 5 - оновити систему і Flatpak, подивитись,
який Python. Крок 4 (прошивки) і крок 6 (новий Python через uv, pyenv) - **пізніше, для ЛР1 не потрібно**.
Кроки 7-8 працюють з venv лаб `~/univer/.venv`, якого ще нема, - роби їх **після уроку 03**.

## Коротко

| Що оновлюємо | Чим | Як часто |
|---|---|---|
| Пакети системи (ядро, програми з apt) | «Диспетчер оновлень» або `sudo apt update` + `sudo apt upgrade` | раз на кілька днів |
| Flatpak-програми | той самий Диспетчер оновлень або `flatpak update` | разом з системою |
| Прошивки (BIOS, тачпад, SSD) | `fwupdmgr` | раз на місяць-два |
| Бібліотеки для лаб (pytest, numpy...) | `pip` **у venv** | коли треба |
| Новіший Python (3.13) | `uv python install 3.13` - **поруч** із системним | лише якщо треба для курсу |

**Перед великим оновленням - знімок Timeshift** (урок 01): `sudo timeshift --create --comments "перед оновленням"`.

**Диспетчер оновлень** (Update Manager, у меню українською «Диспетчер оновлень», mintupdate 7.1.4):
- Рівнів оновлень (1-5), про які пишуть старі статті, **більше нема**. Показує все, ти вибираєш галочками.
- Flatpak-оновлення показуються в тому ж списку.
- Ядра: Вигляд → Ядра Linux (View → Linux Kernels). Яке ядро працює зараз - `uname -r`. Поточне видалити не можна.
- Параметри → Автоматизація: автоматично ставити оновлення, видаляти застарілі ядра, оновлювати Flatpak при вході.
  Mint попереджає: спершу налаштуй знімки.
- У 22.3 значок у треї сам каже, коли треба перезавантажитись.
- **Точкове оновлення** 22, 22.1 або 22.2 → 22.3: знімок, «Оновити», потім Правка → «Upgrade to Linux Mint 22.3 Zena».
  Якщо в меню Правка такого пункту нема - у тебе вже 22.3 (перевір: `cat /etc/os-release`).
- **Наступна версія Mint** (база Ubuntu 26.04) запланована на Різдво 2026 і ще не вийшла. Велике оновлення між
  базами (як 21.3 → 22) робили окремою програмою `mintupgrade` за інструкцією в блозі Mint. Як саме буде цього
  разу - ще не оголошено (не перевірено). 22.3 підтримується до квітня 2029, тож поспішати не треба.

**Те саме в терміналі:**

| Команда | Що робить |
|---|---|
| `sudo apt update` | оновити **список** пакетів (нічого не ставить) |
| `apt list --upgradable` | що можна оновити |
| `sudo apt upgrade` | поставити оновлення - **прочитай список**, потім Y |
| `mintupdate-cli list` | список, як у Диспетчері (з позначкою security) |
| `sudo mintupdate-cli upgrade -r` | оновити, як Диспетчер (`-r` - спершу оновити кеш) |
| `flatpak update` | оновити Flatpak-програми |
| `flatpak uninstall --unused` | прибрати непотрібні Flatpak-бібліотеки (runtimes) |

У Mint `apt` - обгортка (`/usr/local/bin/apt`), вона сама додає `sudo` до install, update, upgrade.

## Передбач, потім запусти

1. Ти поза venv і пробуєш поставити бібліотеку в системний Python:

```bash
pip install requests
```

Що буде?

<details markdown="1"><summary>Відповідь</summary>

Помилка (справжній вивід з Mint 22.3, перші рядки):

```text
error: externally-managed-environment

× This environment is externally managed
╰─> To install Python packages system-wide, try apt install
    python3-xyz, where xyz is the package you are trying to
    install.
```

і внизу `hint: See PEP 668 for the detailed specification.` Це захист (правило PEP 668): системний Python належить
Mint, бібліотеки став у venv. На свіжій Mint, де ще нема пакета `python3-pip`, буде просто `pip: command not found`
(на українській Mint `pip: команду не знайдено`; повідомлення самого pip - англійською завжди).

</details>

2. Перший рядок програми «Диспетчер оновлень»:

```bash
head -1 /usr/bin/mintupdate
```

Що там і що це означає для тебе?

<details markdown="1"><summary>Відповідь</summary>

```text
#!/usr/bin/python3
```

Диспетчер оновлень написаний на Python і запускається системним `/usr/bin/python3`. Так само `mintsources`,
`mintupdate-automation` і десятки інших програм Mint (`mintupdate-cli` - маленька bash-обгортка над
`/usr/lib/linuxmint/mintUpdate/mintupdate-cli.py`, у якого той самий перший рядок). Зламаєш системний Python - зламаєш
інструменти, якими лагодять систему.

</details>

3. Скільки пакетів apt прибрав би разом з `python3`? Ключ `-s` - лише симуляція, нічого не видаляє, sudo не треба:

```bash
apt-get -s remove python3 | grep -c '^Remv'
```

<details markdown="1"><summary>Відповідь</summary>

У тестовій Mint 22.3 (без робочого столу) - `124`. Серед них `mintupdate`, `mintsources`, `mintsystem`, `timeshift`,
`xed`. На ноутбуці з Cinnamon число буде інше, але теж велике. Тому `python3` не видаляють і не підміняють.

</details>

4. (Це питання - на потім, до кроку 6.) Ти поставив Python 3.13 через uv. Що тепер покаже системна команда?

```bash
python3 --version
```

<details markdown="1"><summary>Відповідь</summary>

```text
Python 3.12.3
```

uv кладе свій Python у `~/.local/share/uv/python/` і посилання `python3.13` у `~/.local/bin/`. Системний `python3`
лишається 3.12.3 - так і треба. Python 3.13 вмикається лише там, де ти сам попросив: `python3.13` або venv на 3.13.

</details>

## Руками

**Крок 1. Яка система, яке ядро.**

```bash
cat /etc/os-release
uname -r
```

**Крок 2. Оновлення в терміналі, уважно.**

```bash
sudo apt update
apt list --upgradable
```

Вивід `apt list --upgradable` (початок; у тебе пакети будуть свої):

```text
Listing...
alsa-ucm-conf/noble-updates 1.2.10-1ubuntu5.16 all [upgradable from: 1.2.10-1ubuntu5.14]
apt/noble-updates,noble-security 2.8.4ubuntu0.1 amd64 [upgradable from: 2.8.3]
```

`noble-security` - оновлення безпеки. Якщо передати вивід далі через `|` (наприклад, `apt list --upgradable | less`),
apt ще допише першим рядком `WARNING: apt does not have a stable CLI interface. Use with caution in scripts.` -
це попередження для тих, хто пише скрипти, тобі можна не зважати (у звичайному терміналі його нема).

```bash
sudo apt upgrade
```

apt покаже список і спитає. Справжній вивід (скорочено, у середині ще 70 імен пакетів):

```text
The following upgrades have been deferred due to phasing:
  alsa-ucm-conf distro-info libdistro-info-perl libegl-mesa0 libegl1-mesa-dev
The following packages will be upgraded:
  apt bubblewrap distro-info-data dmidecode gir1.2-xapp-1.0 gstreamer1.0-gl
80 upgraded, 6 newly installed, 0 to remove and 12 not upgraded.
Need to get 75.7 MB of archives.
After this operation, 9466 kB of additional disk space will be used.
Do you want to continue? [Y/n]
```

Дивись на рядок `... to remove`. Якщо там не 0 і серед видалених щось важливе (`cinnamon`, `mint...`, `python3`) -
натисни `n` і з'ясуй причину. «Deferred due to phasing» - Ubuntu видає це оновлення поступово, частині людей пізніше.
Це нормально, нічого робити не треба.

Те саме через інструмент Mint:

```bash
mintupdate-cli list
sudo mintupdate-cli upgrade -r
```

`mintupdate-cli list` (початок справжнього виводу):

```text
security        aom                                           3.8.2-2ubuntu0.2
package         apparmor                                      4.0.1really4.0.1-0ubuntu0.24.04.9
security        apt                                           2.8.4ubuntu0.1
```

**Крок 3. Flatpak.**

```bash
flatpak update
flatpak uninstall --unused
```

Коли все свіже, буде `Nothing to do.` і `Nothing unused to uninstall`.

**Крок 4. Прошивки (пізніше, для ЛР1 не потрібно)** (fwupd - служба, що бере прошивки з сайту LVFS від
виробників). Ноутбук - на зарядці.

```bash
fwupdmgr get-devices
fwupdmgr refresh
fwupdmgr get-updates
fwupdmgr update
```

`get-devices` - які пристрої вміють оновлюватись, `refresh` - свіжий список прошивок, `get-updates` - що є нового,
`update` - поставити (може попросити перезавантаження). Назви команд перевірено з `fwupdmgr --help` у Mint 22.3,
а сам прохід на залізі - **не перевірено** (у тестовій системі нема справжніх пристроїв і служба fwupd не стартує).
Якщо ноутбука нема в списку - для нього прошивки йдуть лише через сайт виробника, це нормально.

**Крок 5. Який Python у тебе працює.**

```bash
which python3
python3 --version
type -a python3
```

Справжній вивід:

```text
/usr/bin/python3
Python 3.12.3
python3 is /usr/bin/python3
python3 is /bin/python3
```

Два рядки в `type -a` - не два Python, а один файл, видний двома шляхами (`/bin` у Mint - посилання на `/usr/bin`).

**Крок 6. Новіший Python поруч - через uv (пізніше, для ЛР1 не потрібно: лаби йдуть на системному 3.12).**
uv - швидкий менеджер Python і пакетів (від Astral). pipx ставить
програми на Python в окремий venv, щоб не чіпати систему. На свіжій Mint pipx нема, тому спершу його:

```bash
sudo apt install pipx
pipx install uv
pipx ensurepath
```

Справжній вивід `pipx install uv` (версія у тебе може бути новіша):

```text
installing uv...
⚠️  Note: '/home/evgen/.local/bin' is not on your PATH environment variable.
    These apps will not be globally accessible until your PATH is updated. Run
    `pipx ensurepath` to automatically add it, or manually modify your PATH in
    your shell's config file (i.e. ~/.bashrc).
done! ✨ 🌟 ✨
  installed package uv 0.13.9, installed using Python 3.12.3
```

`pipx ensurepath` додає `~/.local/bin` у PATH (список тек, де шукаються команди, урок 22). Після нього **закрий і
відкрий термінал** - тоді можна писати просто `uv`. Нижче повний шлях `~/.local/bin/uv`, він працює завжди.

```bash
~/.local/bin/uv python install 3.13
~/.local/bin/uv python list --only-installed
```

```text
Downloading cpython-3.13.18-linux-x86_64-gnu (download) (33.9MiB)
 Downloaded cpython-3.13.18-linux-x86_64-gnu (download)
Installed Python 3.13.18 in 1.24s
 + cpython-3.13.18-linux-x86_64-gnu (python3.13)
```

Venv на 3.13 для пробної теки. **`--seed` обовʼязково** - без нього у venv не буде pip:

```bash
mkdir -p ~/proba313
cd ~/proba313
~/.local/bin/uv venv --python 3.13 --seed
source .venv/bin/activate
which python
python --version
```

```text
/home/evgen/proba313/.venv/bin/python
Python 3.13.18
```

Вимкнути venv - `deactivate`. Прибрати пробу: `cd ~` і `rm -r ~/proba313`. Для лаб поки лишайся на системному 3.12 у `~/univer/.venv` (урок 03), якщо викладач
не просить іншу версію.

**Альтернатива - pyenv** (теж пізніше і лише за потреби; не перевірено в Mint 22.3: pyenv збирає Python з вихідного коду, для цього треба
поставити пакети для збірки за списком з вікі pyenv). Кроки за офіційним README, лише для ознайомлення:

```text
1. curl -fsSL https://pyenv.run | bash          (автоматичний встановлювач)
2. дописати 3 рядки в ~/.bashrc                  (README, розділ «Set up your shell environment for Pyenv»)
3. поставити пакети для збірки                   (вікі pyenv, розділ «Suggested build environment»)
4. pyenv install 3.13
```

uv простіший: нічого не збирає, ставить готовий Python за секунди.

**Крок 7. Оновити бібліотеки у venv лаб (після уроку 03 - там venv `~/univer/.venv` створюється).** Якщо venv ще
нема, `source` нижче напише `bash: /home/evgen/univer/.venv/bin/activate: No such file or directory`
(укр. `... Немає такого файла або каталогу`) - спершу урок 03.

```bash
source ~/univer/.venv/bin/activate
pip list --outdated
```

Справжній вивід у venv, де застаріли pip і six:

```text
Package Version Latest Type
------- ------- ------ -----
pip     24.0    26.3   wheel
six     1.16.0  1.17.0 wheel
```

Оновити одну: `pip install -U six` (`-U` = upgrade). Записати, що стоїть, у файл:

```bash
python3 -m pip freeze > ~/univer/requirements.txt
cat ~/univer/requirements.txt
```

**Крок 8. Перестворити venv (після уроку 03; потрібно після нової версії Python або якщо venv зламався).**
Venv не оновлюють - його створюють заново зі списку:

```bash
~/univer/.venv/bin/python -m pip freeze > ~/univer/requirements.txt
cat ~/univer/.venv/pyvenv.cfg
rm -r ~/univer/.venv
python3 -m venv ~/univer/.venv
~/univer/.venv/bin/python -m pip install -r ~/univer/requirements.txt
```

`pyvenv.cfg` показує, з якого Python зроблено venv (рядок `version = 3.12.3`). Файли лаб у `~/univer/labs`
при цьому не чіпаються - видаляється лише тека `.venv`.

## Типові помилки

- **`error: externally-managed-environment`** - ти поза venv. Увімкни venv (`source ~/univer/.venv/bin/activate`,
  на початку рядка має бути `(.venv)`). Не `sudo pip` і не `--break-system-packages`: так ламають пакети Mint.
- **У venv від uv той самий `externally-managed-environment`.** Venv створено без `--seed`, pip у ньому нема,
  і команда `pip` знайшла системний `/usr/bin/pip`. Перевір: `which pip`. Виправлення: `uv venv --seed` або
  ставити через `uv pip install пакет`.
- **`uv: command not found`** (укр. `uv: команду не знайдено`) після `pipx install uv` - `~/.local/bin` ще не в
  PATH. `pipx ensurepath` і новий термінал (або пиши `~/.local/bin/uv`).
- **`sudo apt install python3.13`** → `E: Unable to locate package python3.13`
  (укр. `E: Неможливо знайти пакунок python3.13`). У репозиторії Ubuntu 24.04 його нема.
  Порада «додай PPA deadsnakes» - сторонній репозиторій, а сторонні репозиторії - найчастіша причина зламаного
  оновлення версії (урок 16). Бери uv.
- **Venv зламався після зміни Python:** `.venv/bin/python: No such file or directory` або
  `pip: cannot execute: required file not found` (справжні повідомлення, коли Python, з якого зроблено venv, видалили;
  укр. `.venv/bin/python: Немає такого файла або каталогу` і `pip: не вдалося виконати: не знайдено потрібного
  файла`). Перестворити venv (крок 8).
- **`Could not get lock /var/lib/dpkg/lock-frontend. It is held by process ...`** - відкрито інший менеджер пакетів
  (Диспетчер оновлень, Менеджер програм). На українській Mint:
  `E: Не вдалося заблокувати /var/lib/dpkg/lock-frontend. Утримується процесом ...` і далі
  `E: Неможливо здобути блокування клієнтської частини (/var/lib/dpkg/lock-frontend), її використовує інший процес?`.
  Закрий інший менеджер і зачекай. Lock-файли не видаляй.
- **`apt upgrade -y` наосліп.** `-y` відповідає «так» на все, навіть на видалення пакетів. Читай список.
- **Після оновлення ядра система не стартує** - у меню GRUB вибери Advanced options → попереднє ядро, потім
  Диспетчер оновлень → Вигляд → Ядра Linux → видалити погане (урок 26).

## Як роблять профі

- **Знімок → оновлення → перезавантаження.** Перед точковим оновленням до 22.3 радили Timeshift
  (r/linuxmint, 11.01.2026, 108 балів).
- **Не `apt upgrade -y` наосліп**, краще Диспетчер оновлень, де видно, що ставиш (r/linuxmint, 28.05.2026).
- **Свіжий приклад, навіщо знімок і TTY:** 05.11.2026 пакет прошивки `linux-firmware-amd-graphics` зламав екран входу
  на відеокартах AMD RX 9060/9070 (255 балів, 355 коментарів). Лагодили з текстового входу (Ctrl+Alt+F2):
  `sudo apt update`, `sudo apt install linux-firmware-amd-graphics`, `sudo update-initramfs -u -k all`, `sudo reboot`.
- **Python:** системний не чіпають; бібліотеки - у venv; програми-утиліти - через pipx; потрібна інша версія Python -
  uv або pyenv. Так радять і на r/linux4noobs (20.08.2026) у відповідь на `externally-managed-environment`.

## Самоперевірка

1. Чим `sudo apt update` відрізняється від `sudo apt upgrade`?
2. Чому не можна видалити або підмінити системний `python3` у Mint?
3. Як поставити Python 3.13, не чіпаючи системний 3.12?
4. Що не так з командою `uv venv --python 3.13` без `--seed`, якщо потім пишеш `pip install`?
5. Як подивитись, які бібліотеки у venv застаріли, і як оновити одну?

<details markdown="1"><summary>Відповіді</summary>

1. `update` лише оновлює список доступних версій. `upgrade` реально ставить новіші версії (і показує список перед цим).
2. Програми Mint (Диспетчер оновлень, Джерела програм, Timeshift через залежності) працюють на `/usr/bin/python3`.
   Симуляція `apt-get -s remove python3` показує, що разом з ним пішли б понад сотню пакетів, серед них mintupdate.
3. `sudo apt install pipx`, `pipx install uv`, потім `~/.local/bin/uv python install 3.13`. Новий Python - у
   `~/.local/share/uv/python/`, системний лишається 3.12.3.
4. У такому venv нема pip, тож `pip` знаходить системний `/usr/bin/pip` і дає `externally-managed-environment`.
   Треба `--seed` або `uv pip install`.
5. У venv: `pip list --outdated`, потім `pip install -U назва`.

</details>

## Джерела

- Посібник користувача Mint, Update Manager - https://linuxmint-user-guide.readthedocs.io/en/latest/mintupdate.html -
  відкрито 18.11.2026
- Оновлення до Mint 22 (mintupgrade) - https://linuxmint-user-guide.readthedocs.io/en/latest/upgrade-to-mint-22.html -
  відкрито 18.11.2026
- Блог Mint про наступну версію (Різдво 2026) - https://blog.linuxmint.com/?p=5019 - відкрито 18.11.2026
- Mint 22.3 і термін підтримки - https://linuxmint.com/download_all.php - відкрито 18.11.2026
- uv, встановлення Python - https://docs.astral.sh/uv/guides/install-python/ - відкрито 18.11.2026
- pyenv - https://github.com/pyenv/pyenv - відкрито 18.11.2026 (кроки встановлення не перевірено)
- PEP 668 - https://peps.python.org/pep-0668/ - відкрито 18.11.2026
- fwupd - https://fwupd.org/ - відкрито 18.11.2026
- Ubuntu про сторонні репозиторії - https://documentation.ubuntu.com/server/explanation/software/third-party-repository-usage/ -
  відкрито 18.11.2026
- r/linuxmint: знімок перед 22.3 https://www.reddit.com/r/linuxmint/comments/1qa50ii/ ; не `apt upgrade -y`
  https://www.reddit.com/r/linuxmint/comments/1tpxaio/ ; прошивка AMD і TTY https://www.reddit.com/r/linuxmint/comments/1xo6jg2/ ;
  нове ядро не стартує https://www.reddit.com/r/linuxmint/comments/1v8vj62/ - відкрито 18.11.2026
- r/linux4noobs, externally-managed-environment - https://www.reddit.com/r/linux4noobs/comments/1vtewxq/ - відкрито 18.11.2026
- `fwupdmgr --help`, `mintupdate-cli --help`, `uv --help`, `timeshift --help` - перевірено запуском у Mint 22.3, 18.11.2026
