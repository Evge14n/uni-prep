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

## Передбач, потім запусти

1. Що скажуть ці команди для служби, якої в системі взагалі нема?

```bash
systemctl is-active nemaservisu
systemctl is-enabled nemaservisu
```

> **Нове тут:**
>
> - `systemctl is-active` - одним словом: чи працює служба зараз. Назва: is active? - «чи працює?».
> - `systemctl is-enabled` - одним словом: чи вмикається служба при старті. Назва: is enabled? - «чи ввімкнений автозапуск?».
>
> Усе про кожну команду - у довіднику «05_Програмування/КОМАНДИ - довідник.md» (на сайті - вкладка «Команди»).

<details markdown="1"><summary>Відповідь</summary>

```text
inactive
not-found
```

`is-active` каже лише «не працює» - йому однаково, є така служба чи ні. А `is-enabled` чесно пише `not-found`.
Тому коли «служба не стартує», спершу перевір назву: `systemctl list-unit-files | grep назва`.

</details>

2. Ти забув `sudo`:

```bash
systemctl stop cron
```

> **Нове тут:**
>
> - `systemctl stop` - зупиняє службу зараз. Назва: stop - «зупинити».

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

> **Нове тут:**
>
> - `systemctl status` - показує стан служби і останні рядки її журналу. Назва: status - «стан».

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
> - `systemctl` - керує службами systemd: стан, запуск, зупинка, автозапуск. Назва: system control - «керування системою» (systemd). `--failed` - лише юніти, що впали з помилкою.
> - `systemctl is-system-running` - одним словом: чи все гаразд з системою. Назва: is system running? - «чи система працює нормально?».
> - `systemctl list-units` - показує завантажені служби і чи вони працюють. Назва: list units - «список юнітів» (одиниць systemd). `--type` - лише такого типу: --type=service - служби, --type=timer - таймери.

На здоровому ноутбуці `systemctl --failed` пише `0 loaded units listed.`, а `is-system-running` - `running`.
Якщо `degraded` - щось упало, дивись `--failed` і журнал тієї служби (крок 4). У тестовій віртуальній системі
справжній вивід - `degraded` і кілька впалих юнітів, серед них `tpm-udev` (там нема чіпа TPM, це нормально для
неї).

**Крок 3. Таймери - що Mint робить за розкладом.**

```bash
systemctl list-timers
```

> **Нове тут:**
>
> - `systemctl list-timers` - показує таймери і коли вони спрацюють. Назва: list timers - «список таймерів».

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

**Крок 4. Журнал: помилки, одна служба, наживо.**

```bash
sudo journalctl -p err -b
sudo journalctl -u cron -b
sudo journalctl --since "1 hour ago"
sudo journalctl -f
```

> **Нове тут:**
>
> - `sudo` - виконує одну команду від імені адміністратора (root). Назва: su do - «виконати як інший користувач», зазвичай root.
> - `journalctl` - показує журнал системи і служб. Назва: journal control - «керування журналом» systemd. `-p` - лише ця важливість і гірше: -p err - помилки, -p warning - ще й попередження; `-b` - лише поточне завантаження (b - boot); -b -1 - попереднє; `err` - після -p: рівень «помилка» і все гірше; `-u` - лише одна служба (u - unit, «одиниця»), напр. -u cron; `--since` - з якого часу, напр. --since "1 hour ago" - за останню годину; `-f` - показувати нові рядки наживо; не закінчується сам, вийти Ctrl+C.
> - `"..."` - текст з пробілами одним словом, $ підставляється. Назва: подвійні лапки - «усе це одне слово, але $ працює».

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
> - `journalctl`: `--list-boots` - список завантажень: 0 - поточне, -1 - попереднє; `-1` - після -b: попереднє завантаження (-2 - ще раніше); `-e` - одразу в кінець журналу - найсвіжіші рядки.

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
> - `dmesg` - показує повідомлення ядра: пристрої, драйвери, помилки. Назва: display message - «показати повідомлення» (ядра); офіційної розшифровки нема.
> - `tail` - показує останні рядки; -f стежить наживо. Назва: tail - «хвіст»: кінець файлу.
> - `journalctl`: `-k` - лише повідомлення ядра (k - kernel): диски, USB, драйвери.
> - `systemd-analyze` - показує, скільки тривав запуск системи. Назва: systemd analyze - «аналіз systemd»: розбір запуску системи. `blame` - «звинуватити»: служби за часом запуску, найдовші вгорі (дивись з | head).
> - `head` - показує перші рядки файлу. Назва: head - «голова»: початок файлу.
> - `uptime` - показує, скільки працює система, і навантаження. Назва: up time - «час роботи» з увімкнення. `-s` - лише дата і час увімкнення: 2026-11-18 09:38:55.
> - `last` - показує останні входи і перезавантаження. Назва: last - «останні»: останні входи в систему і перезавантаження. `reboot` - лише перезавантаження (увімкнення) компʼютера.
> - `|` - передає вивід однієї команди на ввід іншій. Назва: pipe - «труба» (пайп), вертикальна риска.

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
> - `mkdir` - створює нову теку. Назва: make directory - «зробити теку». `-p` - створює і всі проміжні теки шляху; якщо тека вже є - мовчить, без помилки.
> - `printf` - друкує текст за шаблоном; \n - Enter. Назва: print formatted - «надрукувати за шаблоном».
> - `~` - домашня тека /home/evgen. Назва: tilde («тильда») - домашня тека.
> - `'...'` - текст буквально, нічого не підставляється. Назва: одинарні лапки - «буквально, як написано».
> - `>` - пише вивід у файл, старий вміст стирає. Назва: redirect - «перенаправлення» виводу у файл.

Тепер служба і таймер. `cat > файл <<'EOF'` записує в файл усе до рядка `EOF` (можна і через `nano`). `%h` -
systemd сам підставить домашню теку:

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

> **Нове тут:**
>
> - `cat` - показує вміст файлу. Назва: concatenate - «зчепити»: склеює кілька файлів в один вивід.

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
> - `systemctl daemon-reload` - systemd перечитує файли служб після правки. Назва: daemon reload - «перечитати демона»: systemd заново читає файли юнітів. `--user` - перечитати твої власні юніти з ~/.config/systemd/user (без sudo).
> - `systemctl start` - запускає службу зараз. Назва: start - «запустити». `--user` - твій власний юніт (zapys.service з уроку 20), без sudo.
> - `systemctl enable` - вмикає автозапуск служби чи таймера. Назва: enable - «увімкнути» автозапуск. `--user` - твій власний юніт (з ~/.config/systemd/user), без sudo; `--now` - ще й запустити зараз, а не лише при наступному старті.
> - `systemctl list-timers`: `--user` - твої власні таймери (як zapys.timer з уроку 20).

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
> - `journalctl`: `--user` - журнал твоїх власних служб (systemctl --user), sudo не треба; `--no-hostname` - не друкувати імʼя компʼютера в кожному рядку; `-n` - лише останні N рядків, напр. -n 5.

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
> - `systemctl disable` - прибирає службу чи таймер з автозапуску. Назва: disable - «вимкнути» автозапуск. `--user` - твій власний юніт (з ~/.config/systemd/user), без sudo; `--now` - ще й зупинити зараз, а не лише після перезавантаження.
> - `rm` - видаляє файли назавжди, без кошика. Назва: remove - «прибрати, видалити». `-r` - видаляти теки разом з усім, що всередині (recursive).

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
