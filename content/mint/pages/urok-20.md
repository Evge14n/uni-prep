# Урок 20. systemd і журнали

[← Усі уроки](#/u/mint/uroky)

**Навіщо:** коли щось «саме не працює» (Wi-Fi не підключається, звук зник, система довго стартує), відповідь майже
завжди лежить у журналі. А служби (мережа, брандмауер, оновлення за розкладом) вмикає і вимикає systemd. Тут - як
подивитись стан служби, як читати журнал і як зробити свій таймер, що сам запускає Python-скрипт.

## Коротко

**systemd** - перша програма, яку запускає ядро (PID 1). Вона запускає все інше і стежить, щоб воно працювало.
Одиниця керування - **unit** (юніт):
- `.service` - **служба** (демон): програма, що працює у фоні (`NetworkManager.service` - мережа, `cron.service` -
  розклад, `ufw.service` - брандмауер).
- `.timer` - **таймер**: «будильник», що запускає службу за розкладом (як cron, урок 23).
- `.target` - група юнітів (наприклад, `graphical.target` - «система з графікою готова»).

| Команда | Що робить |
|---|---|
| `systemctl status cron` | стан служби + останні рядки її журналу |
| `sudo systemctl start / stop / restart cron` | запустити / зупинити / перезапустити зараз |
| `sudo systemctl enable / disable cron` | вмикати / не вмикати при старті системи (`--now` - ще й зараз) |
| `systemctl is-active cron`, `systemctl is-enabled cron` | коротка відповідь одним словом |
| `systemctl --failed` | що впало |
| `systemctl list-units --type=service` | які служби завантажені |
| `systemctl list-timers` | таймери: коли наступний запуск |
| `systemctl --user ...` | те саме для **твоїх** служб (без sudo) |

> **Нове тут:**
>
> - `systemctl status` - показує стан служби (фонової програми) і останні рядки її журналу.
> - `systemctl start` - запускає службу (фонову програму) зараз.
> - `systemctl enable` - вмикає автозапуск служби (фонової програми) чи таймера.
> - `systemctl is-active` - одним словом: чи працює служба (фонова програма) зараз. Назва: is active? - «чи працює?».
> - `systemctl is-enabled` - одним словом: чи вмикається служба сама при старті. Назва: is enabled? - «чи ввімкнений автозапуск?».
> - `systemctl` - керує службами (фоновими програмами): показує, запускає, зупиняє, вмикає автозапуск. Назва: system control - «керування системою» (через systemd - програму, що запускає служби). `--failed` - лише служби й таймери (юніти), що впали з помилкою (failed - «зазнали невдачі»); `--user` - твої власні служби і таймери (з `~/.config/systemd/user`), без sudo.
> - `systemctl list-units` - показує завантажені служби і чи вони працюють. Назва: list units - «список юнітів» (служб, таймерів - того, чим керує systemd). `--type` - лише такого типу: `--type=service` - служби, `--type=timer` - таймери.
> - `systemctl list-timers` - показує таймери (запуски за розкладом) і коли вони спрацюють. Назва: list timers - «список таймерів».
> - `sudo` - виконує одну команду як адміністратор; спитає твій пароль (видно зірочки). Назва: superuser do - «зроби як суперкористувач» (адміністратор).
>
> **Як читати:**
>
> - Слово з мінусом (як `-b` тут) - **прапорець**: уточнює, що саме зробити команді.
> - Якщо поруч у дужках стоїть довга назва з двома мінусами - це той самий прапорець, пиши будь-яку одну.
> - Короткі можна склеювати: `-xb` = `-x` і `-b`.
> - Символи `~` `|` `>` `*` набирай в англійській розкладці (`~` - Shift і клавіша ліворуч від 1; `|` - Shift і клавіша `\`).
>
> Усе про кожну команду - у довіднику «05_Програмування/КОМАНДИ - довідник.md» (на сайті - вкладка «Команди»).

**Стани:** `active (running)` - працює; `active (exited)` - одноразова дія виконалась успішно (так буває в `ufw`);
`inactive (dead)` - не працює; `failed` - упала з помилкою. При старті: `enabled` - вмикається сама, `disabled` - ні,
`static` - сама не вмикається, її запускає інший юніт (наприклад, таймер).

**Журнал** (journal) - куди systemd складає повідомлення ядра і всіх служб. Читають його `journalctl`:

| Команда | Що показує |
|---|---|
| `journalctl -b` | усе з поточного завантаження (b = boot) |
| `journalctl -b -1` | з попереднього завантаження (коли система впала і ти перезавантажився) |
| `journalctl --list-boots` | список завантажень |
| `journalctl -p err -b` | лише помилки (err і гірше) цього завантаження |
| `journalctl -u NetworkManager` | лише одна служба (u = unit) |
| `journalctl -f` | дивитись наживо, нові рядки з'являються самі (вийти Ctrl+C) |
| `journalctl -xb` | поточне завантаження з поясненнями (x) - так просять на форумах |
| `journalctl --since "1 hour ago"` | за останню годину |
| `journalctl --disk-usage` | скільки місця займає (урок 18) |

> **Нове тут:**
>
> - `journalctl` - показує журнал системи: повідомлення програм і служб (фонових програм). Назва: journal control - «керування журналом» (systemd - програма, що запускає служби). `-b` (`--boot`) - лише з останнього ввімкнення компʼютера; `-b -1` - попереднє (boot - «завантаження»); `-1` - після `-b`: попереднє завантаження (`-2` - ще раніше); `--list-boots` - список завантажень: 0 - поточне, -1 - попереднє; `-p` (`--priority`) - лише ця важливість і гірше: `-p err` - помилки, `-p warning` - ще й попередження (priority); `err` - після `-p`: рівень «помилка» і все гірше; `-u` (`--unit`) - лише записи однієї служби, напр. `-u cron` (unit - «одиниця» systemd); `-f` (`--follow`) - показувати нові рядки наживо; не закінчується сам, вийти Ctrl+C (follow - «стежити»); `-x` (`--catalog`) - додати пояснення до відомих повідомлень; `-xb` так просять на форумах (catalog - «довідник»); `--since` - з якого часу, напр. `--since "1 hour ago"` - за останню годину (since - «відколи»); `--disk-usage` - скільки місця на диску займає журнал.
> - `"..."` (double quotes) - усе між лапками - одне слово, навіть з пробілами.

Рівні важливості (`-p`): `emerg` 0, `alert` 1, `crit` 2, `err` 3, `warning` 4, `notice` 5, `info` 6, `debug` 7.
`-p err` = 0-3.

Журнал довгий, тому він відкривається в «пейджері» `less`: стрілки/PgDn - гортати, `/слово` - шукати, `q` - вийти.
Журнал інших користувачів і системи бачать root і групи `adm`, `systemd-journal`. Першого користувача ноутбука
інсталятор Mint додає в `adm` (урок 15, крок 1), тож у тебе `journalctl` найпевніше покаже все і без sudo (на
ноутбуці не перевірено - глянь `groups`). У тестовій системі курсу користувач не в `adm`, тому нижче команди з `sudo`:
так спрацює в будь-якому разі.

**Ядро окремо - `dmesg`** - повідомлення ядра (диски, USB, драйвери, прошивки). На ноутбуці потрібен `sudo dmesg`:
ядро Mint (з ISO 22.3) зібране з `CONFIG_SECURITY_DMESG_RESTRICT=y`, тобто без root ядро свій журнал не показує.
Те саме без sudo-проблем: `sudo journalctl -k -b` (`-k` - лише ядро).

> **Нове тут:**
>
> - `dmesg` - показує повідомлення ядра (серця Linux): пристрої, драйвери, помилки. Назва: display message - «показати повідомлення» (ядра); офіційної розшифровки нема.
> - `journalctl`: `-k` (`--dmesg`) - лише повідомлення ядра (серця Linux): диски, USB, драйвери (kernel - «ядро»).

## Передбач, потім запусти

*Спершу відповідай подумки, нічого не запускаючи, і лише тоді розкрий «Відповідь». Файли з цих прикладів зʼявляться в розділі «Руками» нижче - запусти й перевір себе, коли його пройдеш.*

1. Що скажуть ці команди для служби, якої в системі взагалі нема?

```bash
systemctl is-active nemaservisu
systemctl is-enabled nemaservisu
```

<details markdown="1"><summary>Відповідь</summary>

```text
inactive
not-found
```

`is-active` каже лише «не працює» - йому однаково, є така служба чи ні. А `is-enabled` чесно пише `not-found`.
Тому коли «служба не стартує», спершу перевір назву: `systemctl list-unit-files | grep назва`.

> **Нове тут:**
>
> - `systemctl list-unit-files` - показує всі встановлені служби і чи ввімкнений їхній автозапуск. Назва: list unit files - «список файлів юнітів».
> - `|` (pipe) - вивід лівої команди йде на вхід правої.
> - `grep` - шукає рядки з текстом (у файлах або те, що прийшло через `|`). Назва: g/re/p з редактора ed: global regular expression print - «скрізь знайти шаблон, надрукувати».

</details>

2. Ти забув `sudo`:

```bash
systemctl stop cron
```

> **Нове тут:**
>
> - `systemctl stop` - зупиняє службу (фонову програму) зараз.

<details markdown="1"><summary>Відповідь</summary>

Справжній вивід з тестової системи:

```text
Failed to stop cron.service: Interactive authentication required.
See system logs and 'systemctl status cron.service' for details.
```

Зупиняти системні служби може лише root. На ноутбуці з робочим столом замість цієї помилки може вискочити вікно з
паролем (не перевірено). Правильно: `sudo systemctl stop cron`. Дивитись стан (`status`, `is-active`) можна без sudo.

</details>

3. Брандмауер `ufw` у Mint вимкнений (урок 25). Що покаже його служба?

```bash
systemctl status ufw
```

<details markdown="1"><summary>Відповідь</summary>

Справжній вивід (час і PID у тебе інші):

```text
● ufw.service - Uncomplicated firewall
     Loaded: loaded (/usr/lib/systemd/system/ufw.service; enabled; preset: enabled)
     Active: active (exited) since Wed 2026-11-18 10:26:24 UTC; 31s ago
       Docs: man:ufw(8)
    Process: 78 ExecStart=/usr/lib/ufw/ufw-init start quiet (code=exited, status=0/SUCCESS)
   Main PID: 78 (code=exited, status=0/SUCCESS)
        CPU: 7ms
```

Служба `active (exited)`: при старті вона один раз запустила `ufw-init` і завершилась успішно (`status=0/SUCCESS`).
Чи брандмауер **увімкнений**, служба не каже - це видно лише з `sudo ufw status` (`Status: inactive`). Не плутай
стан служби зі станом самої програми.

> **Нове тут:**
>
> - `ufw status` - показує, чи увімкнений брандмауер (захист) і які правила. Назва: `ufw` - Uncomplicated Firewall - «нескладний брандмауер».

</details>

## Руками

**Крок 1. Стан однієї служби.**

```bash
systemctl status cron
```

Справжній вивід з тестової системи (час, PID і пам'ять у тебе інші):

```text
● cron.service - Regular background program processing daemon
     Loaded: loaded (/usr/lib/systemd/system/cron.service; enabled; preset: enabled)
     Active: active (running) since Wed 2026-11-18 09:43:44 UTC; 11min ago
       Docs: man:cron(8)
   Main PID: 123 (cron)
      Tasks: 1 (limit: 57708)
     Memory: 400.0K (peak: 18.8M)
        CPU: 262ms
     CGroup: /system.slice/cron.service
             └─123 /usr/sbin/cron -f -P
```

- `●` зелена - працює, `○` - не працює, `×` червоний - впала.
- `Loaded: ... enabled` - вмикається при старті. `Active: active (running) since ...` - працює з такого часу.
- З `sudo systemctl status cron` унизу будуть ще останні рядки журналу цієї служби.
- Довгий вивід відкривається в `less` - вийти `q`.

На ноутбуці подивись так само `systemctl status NetworkManager` (мережа) - у тестовій системі цієї служби нема.

**Крок 2. Що впало і що є.**

```bash
systemctl --failed
systemctl is-system-running
systemctl list-units --type=service
```

> **Нове тут:**
>
> - `systemctl is-system-running` - одним словом: чи все гаразд з системою. Назва: is system running? - «чи система працює нормально?».

На здоровому ноутбуці `systemctl --failed` пише `0 loaded units listed.`, а `is-system-running` - `running`.
Якщо `degraded` - щось упало, дивись `--failed` і журнал тієї служби (крок 4). У тестовій віртуальній системі
справжній вивід - `degraded` і кілька впалих юнітів, серед них `tpm-udev` (там нема чіпа TPM, це нормально для
неї).

**Крок 3. Таймери - що Mint робить за розкладом.**

```bash
systemctl list-timers
```

Справжній вивід з тестової системи (дати у тебе інші):

```text
NEXT                            LEFT LAST                        PASSED UNIT                         ACTIVATES
Wed 2026-11-18 09:58:43 UTC 3min 10s -                                - systemd-tmpfiles-clean.timer systemd-tmpfiles-clean.service
Wed 2026-11-18 16:19:57 UTC       6h Wed 2026-11-18 08:35:42 UTC      - motd-news.timer              motd-news.service
Thu 2026-11-19 00:00:00 UTC      14h Wed 2026-11-18 08:35:42 UTC      - dpkg-db-backup.timer         dpkg-db-backup.service
Thu 2026-11-19 02:23:02 UTC      16h Wed 2026-11-18 08:35:42 UTC      - apt-daily.timer              apt-daily.service
Thu 2026-11-19 04:34:25 UTC      18h Wed 2026-11-18 08:35:42 UTC      - man-db.timer                 man-db.service
Thu 2026-11-19 06:57:25 UTC      21h Wed 2026-11-18 08:35:42 UTC      - apt-daily-upgrade.timer      apt-daily-upgrade.service
Sun 2026-11-22 03:10:24 UTC   3 days Wed 2026-11-18 08:35:42 UTC      - e2scrub_all.timer            e2scrub_all.service

7 timers listed.
Pass --all to see loaded but inactive timers, too.
```

- `apt-daily.timer` - фонове оновлення **списку** пакетів (розклад `OnCalendar=*-*-* 6,18:00`, з
  `systemctl cat apt-daily.timer`), `dpkg-db-backup` - копія бази пакетів, `man-db` - індекс довідки.
- На ноутбуці будуть ще `fstrim.timer` (TRIM для SSD, урок 18) і `fwupd-refresh.timer` (список прошивок).
- **Диспетчер оновлень → Параметри → Автоматизація**: галочки вмикають таймери `mintupdate-automation-upgrade.timer`
  (`OnCalendar=daily`) і `mintupdate-automation-autoremove.timer` (з коду `mintupdate-automation`). Без галочок вони
  `disabled` - перевір: `systemctl list-unit-files "mint*"`.

  > **Нове тут:**
  >
  > - `systemctl cat` - показує файл налаштувань служби (фонової програми) чи таймера. Назва: cat - як однойменна команда `cat`: надрукувати файл.

**Крок 4. Журнал: помилки, одна служба, наживо.**

```bash
sudo journalctl -p err -b
sudo journalctl -u cron -b
sudo journalctl --since "1 hour ago"
sudo journalctl -f
```

Останню зупини Ctrl+C. Кожен рядок журналу: дата і час, ім'я комп'ютера, хто пише (служба[PID]), повідомлення.
На ноутбуці корисні: `-u NetworkManager` (Wi-Fi), `-u bluetooth`, `-u lightdm` (екран входу).

**Крок 5. Коли система впала або перезавантажилась сама.**

```bash
sudo journalctl --list-boots
sudo journalctl -b -1 -p err
sudo journalctl -b -1 -e
```

> **Нове тут:**
>
> - `journalctl`: `-e` (`--pager-end`) - одразу в кінець журналу - найсвіжіші рядки (end - «кінець»).

`--list-boots` - номери завантажень: `0` - поточне, `-1` - попереднє. `-e` - одразу в кінець: останні рядки перед
падінням. Щоб попередні завантаження зберігались, журнал має бути на диску (`/var/log/journal`) - у Mint так і є
(у тестовій системі `--list-boots` показує кілька завантажень).

**Крок 6. Ядро, час старту, коли вмикався.**

```bash
sudo dmesg | tail -20
sudo journalctl -k -b -p warning
systemd-analyze
systemd-analyze blame | head
uptime -s
last reboot | head -3
```

> **Нове тут:**
>
> - `tail` - показує останні рядки (файлу чи того, що прийшло через `|`). Назва: tail - «хвіст». `-20` - лише 20 останні рядки (те саме, що `-n 20`).
> - `systemd-analyze` - показує, скільки тривав запуск системи і які служби найдовші. Назва: systemd analyze - «аналіз systemd». `blame` - «звинуватити»: служби за часом запуску, найдовші вгорі (дивись з `| head`).
> - `head` - показує перші рядки файлу (або того, що прийшло через `|`). Назва: head - «голова». `-3` - лише 3 перші рядки (те саме, що `-n 3`).
> - `uptime` - показує, скільки працює компʼютер, і навантаження процесора. Назва: up time - «час роботи» з увімкнення. `-s` (`--since`) - лише дата і час увімкнення: 2026-11-18 09:38:55.
> - `last` - показує останні входи і перезавантаження. Назва: last - «останні». `reboot` - лише перезавантаження (увімкнення) компʼютера.

- `dmesg` - флешку встромив, а вона не з'явилась? `sudo dmesg | tail -20` одразу після цього покаже, що побачило ядро.
- `systemd-analyze` - скільки тривав старт; `blame` - хто з служб довше за всіх стартував. Справжній вивід з тестової
  системи - `Startup finished in 689ms (userspace)`; на ноутбуці буде довше і з розбивкою `firmware + loader +
  kernel + userspace`, бо там справжнє залізо (не перевірено).
- `uptime -s` - коли увімкнули (дата і час, наприклад `2026-11-18 09:38:55`), `last reboot` - історія
  перезавантажень.

**Крок 7. Свій таймер: Python-скрипт щохвилини.** Користувацькі юніти лежать у `~/.config/systemd/user/`, sudo не
треба. Спершу скрипт, що дописує поточний час у файл:

```bash
mkdir -p ~/proba/timer ~/.config/systemd/user
printf 'import datetime\nfrom pathlib import Path\n\nfail = Path.home() / "proba" / "timer" / "chas.txt"\nwith open(fail, "a") as f:\n    print(datetime.datetime.now().isoformat(timespec="seconds"), file=f)\n' > ~/proba/timer/zapys.py
```

> **Нове тут:**
>
> - `mkdir` - створює нову теку. Назва: make directory - «зробити теку». `-p` (`--parents`) - створює й усі проміжні теки шляху; тека вже є - без помилки (parents - «батьківські»).
> - `~` (tilde) - твоя домашня тека, /home/evgen.
> - `printf` - друкує текст; `\n` у ньому - Enter (новий рядок). Назва: print formatted - «надрукувати за шаблоном».
> - `'...'` (single quotes) - текст буквально: `$`, `*` і пробіли всередині - звичайні символи.
> - `>` (redirect) - пише вивід у файл, старий вміст стирає.

Тепер служба і таймер. `cat > файл <<'EOF'` записує в файл усе до рядка `EOF` (можна і через `nano`). `%h` -
systemd сам підставить домашню теку:

> **Нове тут:**
>
> - `cat` - показує вміст файлу. Назва: concatenate - «зчепити» (уміє склеїти кілька файлів в один вивід).

```bash
cat > ~/.config/systemd/user/zapys.service <<'EOF'
[Unit]
Description=Запис часу у файл (проба)

[Service]
Type=oneshot
ExecStart=/usr/bin/python3 %h/proba/timer/zapys.py
EOF
cat > ~/.config/systemd/user/zapys.timer <<'EOF'
[Unit]
Description=Щохвилини запускати zapys.service

[Timer]
OnCalendar=*:*:00

[Install]
WantedBy=timers.target
EOF
```

`Type=oneshot` - програма відпрацювала і завершилась (не висить постійно). `OnCalendar=*:*:00` - кожну хвилину на
нульовій секунді. `WantedBy=timers.target` - куди «вчепити» таймер при `enable`. Запускаємо:

```bash
systemctl --user daemon-reload
systemctl --user start zapys.service
cat ~/proba/timer/chas.txt
systemctl --user enable --now zapys.timer
systemctl --user list-timers
```

> **Нове тут:**
>
> - `systemctl daemon-reload` - каже systemd (головній програмі служб) перечитати їхні файли після правки. Назва: daemon reload - «перезавантажити демона» (демон - фонова програма, тут systemd). `--user` - перечитати твої власні служби й таймери з `~/.config/systemd/user` (без sudo).
> - `systemctl start`: `--user` - твоя власна служба чи таймер, без sudo.
> - `systemctl enable`: `--user` - твоя власна служба чи таймер (з `~/.config/systemd/user`), без sudo; `--now` - ще й запустити зараз, а не лише при наступному старті (now - «зараз»).
> - `systemctl list-timers`: `--user` - лише твої власні таймери, без sudo.

`daemon-reload` - systemd перечитує файли юнітів (після кожної правки). `start` один раз запускає службу - у файлі
з'явиться час, наприклад `2026-11-18T10:26:55`. `enable --now` - справжній вивід:

```text
Created symlink /home/evgen/.config/systemd/user/timers.target.wants/zapys.timer → /home/evgen/.config/systemd/user/zapys.timer.
```

У `list-timers` таймер буде з `NEXT` - найближча нульова секунда. Через пару хвилин у `chas.txt` додадуться рядки.
Журнал служби (`--no-hostname` - без імені комп'ютера):

```bash
journalctl --user -u zapys.service --no-hostname -n 5
```

```text
Nov 18 10:26:55 systemd[204]: Starting zapys.service - Запис часу у файл (проба)...
Nov 18 10:26:55 systemd[204]: Finished zapys.service - Запис часу у файл (проба).
```

> **Нове тут:**
>
> - `journalctl`: `--user` - журнал твоїх власних служб (фонових програм), sudo не треба; `--no-hostname` - не друкувати імʼя компʼютера в кожному рядку; `-n` (`--lines`) - лише останні N рядків, напр. `-n 5` (number - «кількість»).

Користувацькі таймери працюють, поки ти увійшов у систему (без входу - лише після `loginctl enable-linger`).
Прибери за собою:

```bash
systemctl --user disable --now zapys.timer
rm ~/.config/systemd/user/zapys.service ~/.config/systemd/user/zapys.timer
systemctl --user daemon-reload
rm -r ~/proba
```

> **Нове тут:**
>
> - `systemctl disable` - прибирає службу (фонову програму) чи таймер з автозапуску. `--user` - твоя власна служба чи таймер (з `~/.config/systemd/user`), без sudo; `--now` - ще й зупинити зараз, а не лише після перезавантаження.
> - `rm` - видаляє файли назавжди, без кошика. Назва: remove - «прибрати, видалити». `-r` (`--recursive`) - видаляти теки разом з усім, що всередині (recursive - «рекурсивно», углиб).

## Типові помилки

- **Забув `daemon-reload` після правки юніта** - systemd працює зі старою версією, а `status` пише попередження
  `... changed on disk. Run 'systemctl --user daemon-reload' to reload units.` Виконай
  `systemctl --user daemon-reload` (для системних юнітів - `sudo systemctl daemon-reload`).
- **Помилка в шляху `ExecStart`** (наприклад, `/usr/bin/pyton3`). Справжній вивід:

```text
Job for zapysbad.service failed because the control process exited with error code.
See "systemctl --user status zapysbad.service" and "journalctl --user -xeu zapysbad.service" for details.
```

  а в `status` - `status=203/EXEC`: «не вдалося запустити програму». Шлях у `ExecStart` має бути **повним**
  (`/usr/bin/python3`, не `python3`), перевір `which python3`.
- **`Failed to stop cron.service: Interactive authentication required.`** - забув `sudo` для системної служби.
- **`enable` без `--now`** - служба ввімкнеться лише після перезавантаження. `--now` = ще й запустити зараз.
- **`journalctl` показує мало і пише `Hint: You are currently not seeing messages from other users and the system.`** -
  ти не в групі `adm` (так буває з другим користувачем, якого створили пізніше; першого інсталятор додає в `adm`).
  Пиши `sudo journalctl ...`. Повідомлення systemd (`journalctl`, `systemctl`) англійською навіть в українській Mint:
  перекладу для них у `language-pack-uk-base` нема (перевірено запуском).
- **Вимкнув «непотрібну» службу за порадою з інтернету** - і зникла мережа чи звук. Повернути:
  `sudo systemctl enable --now назва`. Не вимикай службу, поки не знаєш, що вона робить.

  > **Нове тут:**
  >
  > - `which` - показує, який саме файл запуститься. Назва: which - «котрий».

## Як роблять профі

- **Діагностика за 3 команди:** `systemctl --failed` → `systemctl status назва` → `sudo journalctl -u назва -b`.
  На форумі просять саме вивід `journalctl -xb` або `journalctl -b -p err`, а не «у мене не працює».
- **Після збою при старті** (аварійний режим, від'єднаний диск) - `journalctl -xb` (r/linuxmint, 04.10.2026, урок 26).
- **Журнал великий - шукай причину**: якась служба пише помилку щосекунди (r/linuxmint, 24.12.2025: журнали до
  900 ГБ). `sudo journalctl -p err -b | tail` покаже, хто.
- **Свої регулярні задачі** роблять або через cron (урок 23), або user-таймером systemd, як у кроці 7: у таймера є
  журнал, `Persistent=true` (запустить пропущене, якщо ноутбук був вимкнений) і `systemctl --user list-timers`.

## Самоперевірка

1. Чим `systemctl start` відрізняється від `systemctl enable`?
2. Що означає `active (exited)` у службі `ufw`?
3. Як подивитись лише помилки з попереднього завантаження?
4. Як дивитись журнал однієї служби наживо?
5. Ти змінив файл `~/.config/systemd/user/zapys.timer`. Що треба виконати, щоб systemd побачив зміни?

<details markdown="1"><summary>Відповіді</summary>

1. `start` запускає службу зараз (до перезавантаження). `enable` - щоб вона вмикалась при кожному старті системи.
   `enable --now` - і те, і те.
2. Служба один раз виконала свою дію при старті і успішно завершилась. Це не означає, що брандмауер увімкнений -
   його стан показує `sudo ufw status`.
3. `sudo journalctl -b -1 -p err`.
4. `sudo journalctl -u назва -f` (вийти Ctrl+C).
5. `systemctl --user daemon-reload`, а якщо таймер уже працював - ще `systemctl --user restart zapys.timer`.

   > **Нове тут:**
   >
   > - `systemctl restart` - перезапускає службу (фонову програму): зупинити і запустити. `--user` - твоя власна служба чи таймер, без sudo.

</details>

## Джерела

- systemd: systemctl, journalctl, systemd.timer, systemd.unit (`%h`, `OnCalendar`) -
  https://www.freedesktop.org/software/systemd/man/latest/systemctl.html ,
  https://www.freedesktop.org/software/systemd/man/latest/journalctl.html ,
  https://www.freedesktop.org/software/systemd/man/latest/systemd.timer.html ,
  https://www.freedesktop.org/software/systemd/man/latest/systemd.unit.html - відкрито 18.11.2026
- Код `mintupdate-automation` і `/usr/share/linuxmint/mintupdate/automation/index.json` (mintupdate 7.1.4) -
  прочитано в тестовій Mint 22.3, 18.11.2026
- Конфіг ядра `linux-modules-6.14.0-37-generic` (`CONFIG_SECURITY_DMESG_RESTRICT=y`) - прочитано з пакета,
  18.11.2026
- r/linuxmint: nofail і journalctl -xb https://www.reddit.com/r/linuxmint/comments/1wx45gx/ ; журнали 900 ГБ
  https://www.reddit.com/r/linuxmint/comments/1pu9p8v/ - відкрито 18.11.2026
- `systemctl`, `journalctl`, `systemd-analyze`, user-служба і таймер - перевірено запуском у тестовій Mint 22.3
  (systemd 255), 18.11.2026
