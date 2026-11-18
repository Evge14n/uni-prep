# Урок 26. Коли щось зламалось - GRUB, старе ядро, TTY, live USB

[← Усі уроки](#/u/mint/uroky)

**Навіщо:** рано чи пізно ноутбук не завантажиться: після оновлення ядра, драйвера, правки `/etc/fstab` чи
переповненого диска. Майже завжди систему можна врятувати без перевстановлення і без втрати лаб - якщо знаєш драбину
порятунку і **заздалегідь** зробив знімок (урок 01) і live USB. Цей урок - та драбина, від простого до складного.

## Коротко

Нові слова:
- **GRUB** - завантажувач: перша програма з диска, показує меню (Mint, старіше ядро, Windows) і запускає ядро.
- **Ядро** (kernel) - серце Linux. Mint тримає кілька версій; якщо нове не стартує, можна вибрати попереднє.
- **TTY** - текстовий вхід без графіки (Ctrl+Alt+F2). Працює, навіть коли робочий стіл зламався.
- **Recovery mode** - режим відновлення: меню з готовими діями і командний рядок root.
- **Live USB** - флешка з Mint, з якої ставив систему. З неї можна запустити Mint, не чіпаючи диск.

**Драбина порятунку:**

| Що сталось | Перший крок | Урок |
|---|---|---|
| Після оновлення чи драйвера все дивно, але система вантажиться | Timeshift → відновити знімок | 01 |
| Завис робочий стіл, мишка рухається | Ctrl+Alt+Esc (перезапуск Cinnamon) | 19 |
| Чорний екран або завис робочий стіл | Ctrl+Alt+F2 → TTY → лагодити або відновити знімок | тут |
| Нове ядро не стартує | GRUB → Advanced options → попереднє ядро | тут |
| Чорний екран одразу після логотипа | GRUB → `e` → `nomodeset` | тут, 17 |
| Диск 100 % | TTY → звільнити місце | 18 |
| Забув пароль | recovery mode → root → `passwd evgen` | тут |
| «emergency mode» після від'єднання диска | fstab + `nofail` | 18, тут |
| Зламався apt («dpkg was interrupted») | `sudo dpkg --configure -a`, `sudo apt-get install -f` | тут |
| Нема меню GRUB, `grub rescue>` | live USB → Boot Repair | тут |
| Нічого не допомагає | live USB → Timeshift або скопіювати файли | тут, 01 |

## Передбач, потім запусти

1. У тебе ще й Windows, і після кожного запуску Windows годинник у Mint (або навпаки) неправильний на 2-3 години.
Подивись налаштування часу:

```bash
timedatectl
```

Який рядок про це?

<details markdown="1"><summary>Відповідь</summary>

Справжній вивід з тестової системи (у тебе буде `Europe/Kyiv` і свій час):

```text
               Local time: Wed 2026-11-18 09:57:10 UTC
           Universal time: Wed 2026-11-18 09:57:10 UTC
                 RTC time: Wed 2026-11-18 09:57:10
                Time zone: Etc/UTC (UTC, +0000)
System clock synchronized: yes
              NTP service: inactive
          RTC in local TZ: no
```

`RTC` - годинник у самому ноутбуці (на материнській платі). `RTC in local TZ: no` - Linux вважає, що там час UTC
(за Гринвічем). Windows за замовчуванням пише туди **місцевий** час - звідси різниця на 2-3 години (Київ = UTC+2,
влітку +3). Рішення - нижче, «Подвійне завантаження».

Ще два рядки - про **NTP** (Network Time Protocol - звірка годинника з серверами точного часу в інтернеті).
`System clock synchronized: yes` - час уже звірено. `NTP service: active` - служба звірки (`systemd-timesyncd`,
є на ISO 22.3) працює і стежить за годинником сама. У тестовій системі там `inactive`, бо служба там не стартує
(у `systemctl status systemd-timesyncd` видно `ConditionVirtualization=!container was not met`), а на ноутбуці має
бути `active` (не перевірено). Якщо `inactive` на ноутбуці - `sudo timedatectl set-ntp true` або «Системні
налаштування» → «Дата та час» → «Мережевий час».

</details>

2. Відкрито Диспетчер оновлень, а ти в терміналі ставиш пакет. Що скажуть `apt` і `apt-get`?

<details markdown="1"><summary>Відповідь</summary>

Справжній вивід з тестової системи, коли базу пакетів тримав інший процес (з PID 1430):

```text
Waiting for cache lock: Could not get lock /var/lib/dpkg/lock-frontend. It is held by process 1430 (python3)...
```

`apt` чекає, поки інший менеджер пакетів закінчить. У дужках - назва програми, що тримає базу (у тесті lock тримав
Python-скрипт, тому `python3`; на ноутбуці буде назва того, що відкрите). `apt-get` не чекає і одразу падає:

```text
E: Could not get lock /var/lib/dpkg/lock-frontend. It is held by process 1430 (python3)
E: Unable to acquire the dpkg frontend lock (/var/lib/dpkg/lock-frontend), is another process using it?
```

Що робити: дочекатись або закрити іншу програму (Диспетчер оновлень, «Керування програмами»). **Не видаляй** lock-файли і не
вбивай процес посеред встановлення - так і ламають базу пакетів.

</details>

3. Ти в меню GRUB натиснув `e`, замінив `quiet splash` на `nomodeset` і завантажився. Чи буде `nomodeset` і при
наступному старті?

<details markdown="1"><summary>Відповідь</summary>

Ні. Правка через `e` діє лише на один запуск. Це і добре: `nomodeset` - тимчасова «милиця» (вимикає нормальні
відеодрайвери, картинка буде повільна і в низькій роздільності). Завантажився - став правильний драйвер (урок 17),
перезавантажся без `nomodeset`. Постійно параметр додають у «Керування системою» → «Меню завантаження» →
«Параметри завантаження» (нижче), але для `nomodeset` так роблять лише як крайній захід.

</details>

## Руками

Тут вправи, які безпечно зробити **зараз**, поки все працює: потренуватись і підготуватись. Самі рятувальні кроки -
у «Сценаріях» нижче.

**Крок 1. Потренуйся в TTY.**
1. Ctrl+Alt+F2 - чорний екран з `login:`. Введи свій логін (`evgen`) і пароль (символи не видно - це нормально).
2. Тут працюють усі команди з курсу:

```bash
uname -r
df -h /
systemctl --failed
```

3. Вийти: `exit`. Назад до графіки - **Ctrl+Alt+F7** (так пишуть на r/linuxmint, 24.12.2025; якщо F7 не
   повернув - спробуй Ctrl+Alt+F1, на твоєму ноутбуці не перевірено).

**Крок 2. Зроби меню GRUB видимим.** Якщо на ноутбуці лише Mint, меню при старті сховане і проскакує. Щоб не
ловити момент клавішею (Shift на старих BIOS, Esc на UEFI), у Mint 22.3 є програма **«Керування системою»**
(System Administration, `mintsysadm`):

```text
Меню → «Керування системою» (попросить пароль) → «Меню завантаження»
  [x] Показати меню
  Затримка перед завантаженням усталеного вибору (секунд): 3
  [ ] Запам'ятовувати останній вибір як усталений
  Параметри завантаження: (тут можна додати параметр ядра)
  [Зберегти] → «Оновлення меню завантаження» → «Успіх»
```

Програма записує файл `/etc/default/grub.d/98_mintsysadm.cfg` і сама запускає `update-grub` (з коду mintsysadm 1.0.4).
Для показаного вище вибору файл буде такий:

```text
# Do not edit this file. It is generated by mintsysadm.
GRUB_TIMEOUT_STYLE=menu
GRUB_TIMEOUT=3
GRUB_CMDLINE_LINUX_DEFAULT="$GRUB_CMDLINE_LINUX_DEFAULT "
```

Перевір: `cat /etc/default/grub.d/98_mintsysadm.cfg`. Меню на кожному старті з таймаутом 1-3 с - нормально, а
«Grub Customizer» ставити не треба (r/linuxmint, 15.10.2026, 64 бали). Перезавантажся і просто **подивись** на
меню: перший рядок - Linux Mint, далі «Advanced options for Linux Mint ...». Нічого не вибирай.

**Крок 3. Зроби live USB заздалегідь.** Образ Mint 22.3 Cinnamon важить 3,1 ГБ (3 091 660 800 байт на
дзеркалі mirrors.kernel.org), тож флешка потрібна 4 ГБ або більше. **Усе на ній зітреться.**
1. Завантаж ISO Mint 22.3 Cinnamon і файл `sha256sum.txt` з linuxmint.com (сторінка Download) у теку «Завантаження».
2. Перевір, що образ не пошкоджений:

```bash
cd "$(xdg-user-dir DOWNLOAD)"
sha256sum -c sha256sum.txt --ignore-missing
```

   `xdg-user-dir DOWNLOAD` друкує шлях до теки завантажень (назва залежить від мови). Має бути рядок
   `linuxmint-22.3-cinnamon-64bit.iso: OK` (з образом не перевірено; ключ `--ignore-missing` - не сваритись на інші
   образи зі списку).
3. Встав флешку, `lsblk -o NAME,SIZE,MODEL,MOUNTPOINT` - запам'ятай її розмір і модель (урок 18).
4. Меню → «Запис образу на USB-нагромаджувач» → вибери ISO → вибери флешку (**звір розмір і модель!**) →
   «Записати» → дочекайся «Образ було успішно записано».
5. Підпиши флешку і поклади поруч з ноутбуком.

Завантажитись з неї: увімкнути ноутбук і натиснути клавішу меню завантаження - у різних виробників різна (часто F12,
F11, F10 або Esc; для твого ноутбука не перевірено - глянь на сайті виробника).

**Крок 4. Збери «паспорт» системи для форуму** (поки все працює - щоб було з чим порівняти):

```bash
inxi -Fxxxz > ~/inxi.txt
sudo journalctl -b -p err > ~/pomylky.txt
head -4 ~/inxi.txt
```

`-Fxxxz` - усе (F), максимум деталей (xxx), без MAC і серійних номерів (z). Файл складається з розділів
`System:`, `Machine:`, `CPU:`, `Graphics:`, `Audio:`, `Network:`, `Drives:`, `Partition:`, `Swap:`, `Sensors:`,
`Info:` (так у тестовій системі). У рядку `System:` є `Distro: Linux Mint 22.3 Zena base: Ubuntu 24.04 LTS Noble`;
на ноутбуці там ще буде `Desktop: Cinnamon` і ядро на кшталт `6.14.0-37-generic` (тестова система віртуальна, у неї
ядро своє і `Desktop: N/A`, тому її вивід тут не показую).

**Крок 5. Перевір, що apt здоровий.**

```bash
dpkg --audit
sudo dpkg --configure -a
sudo apt-get install -f
```

Коли все гаразд, `dpkg --audit` і `dpkg --configure -a` нічого не друкують, а `apt-get install -f` закінчується
рядком `0 upgraded, 0 newly installed, 0 to remove and ... not upgraded.`

## Сценарії порятунку

**А. Чорний екран, завис робочий стіл, диск 100 %.** Ctrl+Alt+F2 → вхід. Далі за ситуацією:
- щойно ставив драйвер чи оновлення - `sudo timeshift --list`, потім `sudo timeshift --restore` (урок 01);
- диск повний - урок 18 (`df -h /`, `sudo journalctl --vacuum-time=2d`, `sudo apt autoremove --purge`);
- зависла програма - `top`, `kill PID` (урок 19);
- потім `sudo reboot`.

Свіжий приклад (05.11.2026, 255 балів): пакет `linux-firmware-amd-graphics` зламав екран входу на AMD RX 9060/9070,
лагодили з TTY: `sudo apt update`, `sudo apt install linux-firmware-amd-graphics`, `sudo update-initramfs -u -k all`,
`sudo reboot`.

**Б. Нове ядро не стартує** (r/linuxmint, 28.07.2026, 126 балів: оновлення до ядра 7.0).
1. При старті меню GRUB (крок 2, або Esc/Shift) → «Advanced options for Linux Mint ...» → вибери рядок з
   **попереднім** ядром (без `(recovery mode)`).
2. Завантажився - `uname -r` покаже старе ядро.
3. Диспетчер оновлень → Вигляд → Ядра Linux → вибери погане (нове) ядро → Видалити. Поточне видалити не можна, і це
   правильно.

**В. Чорний екран одразу після логотипа (відео).** За посібником Mint: у меню GRUB виділи рядок Linux Mint,
натисни `e`, заміни `quiet splash` на `nomodeset`, натисни F10 - завантажиться з простим відеорежимом. Потім
«Керування драйверами» (урок 17) і перезавантаження без `nomodeset` (передбач 3).

**Г. Забув пароль.** GRUB → «Advanced options» → рядок з `(recovery mode)`. З'явиться «Меню Відновлення» (Recovery
Menu, українською або англійською - залежить від мови системи):

```text
Меню Відновлення (стан файлової системи: лише читання)
   resume   Повторити звичайне завантаження
   clean    Спробувати звільнити більше місця
   dpkg     Полагодити пошкоджені пакунки
   fsck     Перевірити всі файлові системи
   grub     Оновити початковий завантажувач grub
   network  Увімкнути мережеве з'єднання
   root     Перейти до командного рядку root
   system-summary  Інформація про систему
```

(Пункти, порядок і переклад - з пакета `friendly-recovery` 0.2.42, він є на ISO 22.3; вигляд вікна приблизний.
Пункти `failsafeX` і `apt-snapshots` з'являються, лише якщо стоять пакети `xdiagnose` і `apt-btrfs-snapshot`, а
на ISO 22.3 їх нема.) Вибери `root`. Буде:

```text
Press Enter for maintenance
(or press Control-D to continue):
```

Enter - і ти root без пароля (перевірено в тестовій Mint 22.3: `sulogin`, коли пароль root заблокований, як у Mint
за замовчуванням, пускає по Enter). Диск змонтований **лише для читання**, тому:

```text
mount -o remount,rw /
passwd evgen
reboot
```

Перший рядок дозволяє запис, другий питає новий пароль двічі (символи не видно), третій перезавантажує. Тут нема
`sudo` - ти вже root. (Цей сценарій з GRUB на ноутбуці не перевірено, лише його частини: меню і `sulogin`.)
Те саме вміють пункти `dpkg` (полагодити пакети) і `clean` (звільнити місце) - без ручних команд.

Висновок про безпеку: хто має фізичний доступ до ноутбука, той може так само стати root. Від цього захищає
шифрування диска (його вмикають під час встановлення Mint).

**Ґ. «You are in emergency mode».** Так виглядає екран (текст зібрано з програм systemd 255 і sulogin у тестовій
Mint 22.3; сам аварійний режим на ноутбуці не перевірено):

```text
You are in emergency mode. After logging in, type "journalctl -xb" to view
system logs, "systemctl reboot" to reboot, or "exit"
to continue bootup.
Press Enter for maintenance
(or press Control-D to continue):
```

Найчастіше - у `/etc/fstab` диск, якого нема (від'єднали зовнішній, r/linuxmint, 04.10.2026). Що робити: Enter
(у Mint пароля root нема, тому одразу відкриється консоль root), `journalctl -xb` - знайти червоний рядок про
`mount` або `.mount`; `nano /etc/fstab` - дописати `nofail` або закоментувати рядок `#`; `findmnt --verify`;
`systemctl reboot` (урок 18). Якщо nano при збереженні пише `Error writing /etc/fstab: Read-only file system`
(українською `Помилка під час спроби записати /etc/fstab: Файлова система тільки для зчитування`) - диск ще лише
для читання: вийди з nano (Ctrl+X, `N`), спершу `mount -o remount,rw /`, потім знову `nano /etc/fstab`.

**Д. Зламався apt.** Після обриву світла чи закритого посеред оновлення вікна `apt` (і `sudo apt-get`) пише
(справжній текст apt 2.8 з тестової системи, де перерване встановлення змодельовано на копії бази пакетів):

```text
E: dpkg was interrupted, you must manually run 'sudo dpkg --configure -a' to correct the problem.
```

По черзі: `sudo dpkg --configure -a` (доробити перервану установку), `sudo apt-get install -f` (довставити
залежності), `sudo apt update`, `sudo apt upgrade`. Якщо винна стороння програма (PPA, `.deb` з сайту) - прибери її
(урок 16). Те саме вміє пункт `dpkg` у recovery mode.

**Е. Нема меню GRUB, чорний екран з `grub rescue>`** (часто після видалення розділу чи Windows-оновлення,
r/linuxmint, 12.05.2026). Завантажся з live USB. **Boot Repair** у live-сесії Mint 22.3 уже стоїть (пакет
`boot-repair` є в списку пакетів ISO і видаляється лише після встановлення), тому PPA, про який пишуть старі статті,
не треба. Запусти `boot-repair` з меню (пошук «Boot Repair») і вибери «Recommended repair». Програма покаже
посилання на звіт - його і дають на форумі. (Сам ремонт на ноутбуці не перевірено.)

**Є. Нічого не допомагає.** Live USB → Timeshift (є на образі) → вибери свій диск і знімок → Restore (урок 01).
Або просто скопіюй `~/univer` з внутрішнього диска на іншу флешку через Nemo і перевстанови Mint - лаби вціліють.

**Подвійне завантаження з Windows.**
- **Годинник** (r/linuxmint, 02.10.2026): спершу часовий пояс `sudo timedatectl set-timezone Europe/Kyiv`. Різницю в
  2-3 години радять лікувати в Windows параметром `RealTimeIsUniversal=1` (точна команда - ArchWiki «System time»,
  розділ про Windows; не перевірено). Варіант з боку Linux - `timedatectl set-local-rtc 1`, але тоді `timedatectl`
  попереджає: «The system is configured to read the RTC time in the local time zone» - systemd цей режим не радить.
- **BitLocker** (r/linuxmint, 22.02.2026 і 01.06.2026): **до** встановлення Mint чи зміни налаштувань BIOS збережи
  ключ відновлення BitLocker (у Windows або в акаунті Microsoft). Secure Boot не вимикай: після змін завантаження і
  вимірювань TPM Windows може попросити ключ відновлення (стаття Microsoft «BitLocker recovery overview»; на
  ноутбуці не перевірено).
- **Secure Boot** лиши ввімкненим; драйвери - через MOK (урок 17).

## Як просити допомоги

- Форум **forums.linuxmint.com** (англійською), r/linuxmint. Напиши: що робив перед поломкою, що бачиш (точний текст
  помилки, фото екрана телефоном, якщо в TTY), вивід `inxi -Fxxxz` (крок 4) і, якщо система вантажиться,
  `sudo journalctl -b -p err`.
- **Не вставляй команди, яких не розумієш** - з YouTube, форумів чи від ШІ (r/linux4noobs: пост 18.08.2026,
  283 бали - «поради» з YouTube на кшталт `chmod 777` і все від root; пост 29.06.2026 - людина виконала пораду ШІ з
  `apt purge` і стерла сервер). Розбери команду на explainshell.com - він пояснює кожне
  слово. Особливо небезпечні: `rm -rf` з `/` або `*`, `dd`, `mkfs`, `chmod -R 777`, `sudo` перед тим, що з інтернету
  «треба просто вставити».

## Типові помилки

- **Перевстановлювати Mint при першій проблемі.** Спершу драбина: TTY → знімок → старе ядро → recovery → live USB.
- **Нема ні знімка, ні live USB, коли вже зламалось.** Обидва роблять заздалегідь (урок 01, крок 3 тут).
Якщо Mint українською - у дужках текст з файлів перекладу `language-pack-uk-base` (у recovery mode мова може бути
й англійська). Англійський текст для пошуку: `LC_ALL=C команда`.

- **`Could not get lock /var/lib/dpkg/lock-frontend`** (`Не вдалося заблокувати /var/lib/dpkg/lock-frontend`) -
  відкритий інший менеджер пакетів. Чекай, не видаляй lock.
- **`passwd: Authentication token manipulation error`** (`passwd: Помилка маніпуляції лексемою розпізнавання`) у
  recovery mode - забув `mount -o remount,rw /`, диск ще лише для читання (текст помилки з досвіду користувачів, не
  перевірено).
- **Залишив `nomodeset` назавжди** - відео повільне, яскравість і зовнішній монітор не працюють. Прибери після
  встановлення драйвера.
- **Вимкнув Secure Boot на ноутбуці з BitLocker** - Windows може попросити ключ відновлення (48 цифр; він у
  Windows або в акаунті Microsoft). Введи його і увімкни Secure Boot назад у BIOS.

## Як роблять профі

- **Готуються, поки все працює:** знімки за розкладом, live USB у шухляді, лаби в GitHub (урок 24) - тоді будь-яка
  поломка - це 10-20 хвилин.
- **Не ламають наосліп:** перед драйвером чи PPA - знімок (урок 01); після поломки спершу читають журнал
  (`journalctl -xb`, урок 20), а не вставляють першу пораду з пошуку.
- **Старе ядро як страховка:** не видаляють попереднє ядро, поки нове не відпрацювало кілька днів (r/linuxmint,
  28.07.2026).
- **Питають з `inxi -Fxxxz` і точним текстом помилки** - так відповідь приходить за години, а не за дні.

## Самоперевірка

1. Після оновлення ядра Mint не стартує. Як завантажитись і як прибрати погане ядро?
2. Як перейти в текстовий вхід і як повернутись до графіки?
3. Забув пароль. Перелічи кроки.
4. Що робити з повідомленням `E: dpkg was interrupted ...`?
5. Годинник у Windows і Mint розходиться на 2 години. Чому і як виправити?

<details markdown="1"><summary>Відповіді</summary>

1. У меню GRUB → «Advanced options for Linux Mint» → рядок з попереднім ядром. Потім Диспетчер оновлень → Вигляд →
   Ядра Linux → видалити нове.
2. Ctrl+Alt+F2 - TTY; назад Ctrl+Alt+F7.
3. GRUB → Advanced options → `(recovery mode)` → `root` → Enter → `mount -o remount,rw /` → `passwd evgen` → `reboot`.
4. `sudo dpkg --configure -a`, потім `sudo apt-get install -f`, потім `sudo apt update` і `sudo apt upgrade`.
5. Linux вважає, що годинник ноутбука в UTC (`RTC in local TZ: no`), а Windows пише туди місцевий час. Краще
   ввімкнути в Windows `RealTimeIsUniversal=1`; перевір також `sudo timedatectl set-timezone Europe/Kyiv`.

</details>

## Джерела

- Посібник установки Mint, «Boot options» (nomodeset, `e`, F10) - https://linuxmint-installation-guide.readthedocs.io/en/latest/boot_options.html -
  відкрито 18.11.2026
- Посібник установки Mint, «Verify your ISO image» і «Create the bootable media» -
  https://linuxmint-installation-guide.readthedocs.io/en/latest/verify.html ,
  https://linuxmint-installation-guide.readthedocs.io/en/latest/burn.html - відкрито 18.11.2026
- Код mintsysadm 1.0.4 (меню завантаження, `98_mintsysadm.cfg`) і переклад - пакет `mintsysadm` з репозиторію Mint,
  прочитано 18.11.2026
- friendly-recovery 0.2.42 (меню відновлення і переклад) - пакет з репозиторію Ubuntu 24.04, прочитано 18.11.2026
- util-linux, sulogin - https://github.com/util-linux/util-linux/blob/v2.39.3/login-utils/sulogin.c - відкрито
  18.11.2026; поведінка перевірена запуском у тестовій Mint 22.3
- Boot Repair - https://launchpad.net/boot-repair - відкрито 18.11.2026; пакет `boot-repair` 4ppa2075 є в репозиторії
  Mint (zena/import) і в списку пакетів ISO 22.3
- ArchWiki, «System time» (Windows і UTC) - https://wiki.archlinux.org/title/System_time - відкрито 18.11.2026
- explainshell - https://explainshell.com/ - відкрито 18.11.2026
- r/linuxmint: старе ядро https://www.reddit.com/r/linuxmint/comments/1v8vj62/ ; прошивка AMD і TTY
  https://www.reddit.com/r/linuxmint/comments/1xo6jg2/ ; диск 100 % і Ctrl+Alt+F7 https://www.reddit.com/r/linuxmint/comments/1pu9p8v/ ;
  emergency mode і nofail https://www.reddit.com/r/linuxmint/comments/1wx45gx/ ; grub rescue і boot-repair
  https://www.reddit.com/r/linuxmint/comments/1taqd1h/ ; меню GRUB і таймаут https://www.reddit.com/r/linuxmint/comments/1x6ncxf/ ;
  годинник https://www.reddit.com/r/linuxmint/comments/1wvv81b/ ; BitLocker https://www.reddit.com/r/linuxmint/comments/1rbtttr/ ,
  https://www.reddit.com/r/linuxmint/comments/1tu696g/ - відкрито 18.11.2026
- r/linux4noobs, не вставляти незрозумілі команди - https://www.reddit.com/r/linux4noobs/comments/1vrmeqc/ ,
  порада ШІ з `apt purge` - https://www.reddit.com/r/linux4noobs/comments/1uitco4/ - відкрито 18.11.2026
- `timedatectl`, `apt`/`apt-get` при зайнятому lock, `dpkg --audit`, `sulogin`, `inxi -Fxxxz`, тексти apt і systemd -
  перевірено запуском у тестовій Mint 22.3, 18.11.2026
