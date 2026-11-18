# Урок 21. Мережа і ssh

[← Усі уроки](#/u/mint/uroky)

**Навіщо:** коли «інтернет не працює», за дві хвилини зрозуміти, що саме зламалось: Wi-Fi, роутер, DNS чи сайт.
І зробити ssh-ключ - він знадобиться для GitHub (урок 24) і для входу на інший компʼютер.

## Коротко

Шлях від ноутбука до сайту:

```text
ноутбук ──Wi-Fi──► роутер (шлюз) ──► провайдер ──► інтернет ──► сайт
   │
   └── «яка адреса в linuxmint.com?» ──► DNS-сервер ──► «192.124.249.53»
```

- **IP-адреса** - номер компʼютера в мережі (напр. `192.168.0.105`).
- **Шлюз** (gateway) - куди йдуть усі пакети «назовні», зазвичай це роутер.
- **DNS** - «телефонна книга»: перетворює імʼя `linuxmint.com` на IP-адресу.
- **Порт** - номер «дверей» програми на компʼютері: 22 - ssh, 443 - https.

У Mint мережею керує служба **NetworkManager** (є на ISO 22.3, версія 1.46). Мишкою - **аплет мережі** на панелі
біля годинника: список Wi-Fi, вимкнути/увімкнути, «Мережні зʼєднання» (програма `nm-connection-editor`).
У терміналі той самий NetworkManager - це команда `nmcli`.

| Команда | Що показує |
|---|---|
| `nmcli device status` | пристрої (Wi-Fi, кабель) і чи підключені (`connected`) |
| `nmcli dev wifi list` | які Wi-Fi мережі видно, сигнал, захист |
| `ip -br a` (або `ip a`) | мої IP-адреси (`-br` - коротко) |
| `ip r` | маршрути; рядок `default via ...` - це шлюз |
| `ping -c 3 1.1.1.1` | чи доходять пакети до інтернету (3 спроби) |
| `resolvectl status` | які DNS-сервери використовує система |
| `curl -I https://сайт` | чи відповідає сайт (лише заголовки, `200` = добре) |
| `sudo ss -tulpn` | які програми слухають порти (чекають підключень) |

**Сходинки діагностики** - йди зверху вниз, перша сходинка, що не працює, і є поломка:

```text
1. nmcli device status        Wi-Fi "connected"?           ні → Wi-Fi (крок 3)
2. ip -br a                   є адреса (напр. 192.168.x.x)? ні → роутер не дав адресу
3. ip r                       є "default via ..."?         ні → нема шлюзу
4. ping -c 3 1.1.1.1          пакети доходять?             ні → роутер або провайдер
5. ping -c 3 linuxmint.com    імʼя знаходиться?            ні → DNS
6. curl -I https://linuxmint.com   відповідь 200?          ні → сам сайт
```

**ssh** (Secure Shell) - зашифрований вхід у термінал іншого компʼютера: `ssh користувач@адреса`. Замість пароля
краще **ключ** - пара файлів:

| Файл | Що це | Кому |
|---|---|---|
| `~/.ssh/id_ed25519` | приватний ключ | **нікому**, ніколи. Права `600` |
| `~/.ssh/id_ed25519.pub` | публічний ключ | можна давати: GitHub, сервер |
| `~/.ssh/known_hosts` | «відбитки» серверів, де ти вже був | ssh веде сам |
| `~/.ssh/config` | короткі імена для серверів | ти пишеш сам. Права `600` |

Сама тека `~/.ssh` - права `700` (лише ти). Що означають цифри - урок 15.

| Команда | Що робить |
|---|---|
| `ssh-keygen -t ed25519 -C "підпис"` | зробити пару ключів (ed25519 - сучасний тип) |
| `ssh-copy-id користувач@сервер` | дописати твій `.pub` на сервер (раз, з паролем) |
| `ssh користувач@сервер` | увійти |
| `scp файл користувач@сервер:тека/` | скопіювати файл туди (або назад) |
| `rsync -av тека/ куди/` | скопіювати теку, наступного разу - лише зміни |

**ssh-сервера на Mint нема** (пакета `openssh-server` нема на ISO 22.3), тобто ніхто не може зайти на твій
ноутбук по ssh. Клієнт `ssh` є. Сервер не став, поки не треба. Якщо колись знадобиться (зайти на ноутбук з іншого
компʼютера): `sudo apt install openssh-server`, потім `sudo ufw allow ssh` (урок 25), а коли вхід по ключу
запрацює - вимкнути вхід паролем (`PasswordAuthentication no` у файлі в `/etc/ssh/sshd_config.d/`).

**VPN коротко.** На ISO 22.3 є додатки NetworkManager для OpenVPN і PPTP. Якщо університет чи робота дасть файл
`.ovpn`: аплет мережі → «Мережні зʼєднання» → `+` → імпорт збереженої конфігурації VPN (назви пунктів - не
перевірено в Cinnamon GUI). Далі VPN вмикається в тому ж аплеті. Роби саме за інструкцією того, хто дав VPN.

## Передбач, потім запусти

1. Інтернет є (`ping -c 3 1.1.1.1` працює). Що скаже ping для імені, якого не існує?

```bash
ping -c 1 nema.invalid
echo $?
```

> **Нове тут:**
>
> - `ping` - перевіряє, чи доходять пакети до адреси. Назва: назва від звуку сонара «пінг»: послав сигнал - чекаєш луну. `-c` - скільки пакетів послати і зупинитись (c - count, «кількість»); без -c ping іде вічно; `nema.invalid` - домен .invalid спеціально ніколи не існує - для перевірки відповіді «такого імені нема».
> - `echo` - друкує текст і значення змінних. Назва: echo - «луна»: повторює те, що йому дали.
>
> Усе про кожну команду - у довіднику «05_Програмування/КОМАНДИ - довідник.md» (на сайті - вкладка «Команди»).

<details markdown="1"><summary>Відповідь</summary>

```text
ping: nema.invalid: Name or service not known
2
```

DNS **працює** і чесно відповів: такого імені нема (домен `.invalid` спеціально ніколи не існує). Пакети навіть
не пішли. А от якщо DNS-сервер недосяжний, відповідь інша - `Temporary failure in name resolution`; коли так
відповідає **кожне** імʼя, а `ping 1.1.1.1` працює - зламався DNS, а не інтернет (див. «Типові помилки»).
Українською: `Невідома назва чи сервіс` і `Тимчасова помилка розв'язання назв`.

</details>

2. У теці `lr1` два файли. Куди потраплять файли в кожному випадку?

```bash
rsync -av lr1/ backup-lr1/
rsync -av lr1 backup2/
```

> **Нове тут:**
>
> - `rsync` - копіює теки, а повторно - лише змінене. Назва: remote sync - «віддалена синхронізація»: копіює і між компʼютерами. `-a` - архівний режим: усе з підтеками, права і час зміни (archive); `-v` - писати, що копіюється (verbose).

<details markdown="1"><summary>Відповідь</summary>

```text
sending incremental file list
created directory backup-lr1
./
lr1_1.py
lr1_2.py

sent 205 bytes  received 90 bytes  590.00 bytes/sec
total size is 18  speedup is 0.06
sending incremental file list
created directory backup2
lr1/
lr1/lr1_1.py
lr1/lr1_2.py

sent 218 bytes  received 88 bytes  612.00 bytes/sec
total size is 18  speedup is 0.06
```

`lr1/` (зі скісною рискою) = «вміст теки» → файли лежать прямо в `backup-lr1/`. `lr1` без риски = «сама тека» →
вийде `backup2/lr1/lr1_1.py`. Це найчастіша плутанина з rsync. Швидкість (`bytes/sec`) і число після `sent` у тебе будуть інші (воно
змінюється на кілька байтів навіть від запуску до запуску).

</details>

3. Приватному ключу випадково дали права `644` (читати можуть усі). Що зробить ssh?

<details markdown="1"><summary>Відповідь</summary>

Відмовиться його використовувати (справжній вивід у тестовій Mint 22.3, ключ лежав в іншій теці):

```text
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
@         WARNING: UNPROTECTED PRIVATE KEY FILE!          @
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
Permissions 0644 for '/home/evgen/.ssh/id_ed25519' are too open.
It is required that your private key files are NOT accessible by others.
This private key will be ignored.
Load key "/home/evgen/.ssh/id_ed25519": bad permissions
evgen@localhost: Permission denied (publickey).
```

Лікується `chmod 600 ~/.ssh/id_ed25519`.

</details>

4. Ти вперше підключаєшся до сервера (тут - GitHub). Що спитає ssh і що з цим робити?

```bash
ssh -T git@github.com
```

> **Нове тут:**
>
> - `ssh` - заходить у термінал іншого компʼютера по зашифрованому каналу. Назва: Secure Shell - «захищена оболонка»: зашифрований термінал на іншому компʼютері. `-T` - прапорець: не відкривати термінал на тому боці, лише перевірити вхід (ssh -T git@github.com). GitHub не дає командного рядка, тому для нього завжди -T; якщо вхід вдався, GitHub вітає на імʼя і закриває зʼєднання з кодом 1 - це нормально (Git урок 03); `git@github.com` - користувач git на сервері github.com - так GitHub приймає всіх, а тебе впізнає за ключем.

<details markdown="1"><summary>Відповідь</summary>

```text
The authenticity of host 'github.com (140.82.121.4)' can't be established.
ED25519 key fingerprint is SHA256:+DiY3wvvV6TuJJhbpZisF/zLDA0zPMSvHdkr4UvCOqU.
This key is not known by any other names.
Are you sure you want to continue connecting (yes/no/[fingerprint])? yes
Warning: Permanently added 'github.com' (ED25519) to the list of known hosts.
git@github.com: Permission denied (publickey).
```

ssh ще не знає цей сервер і показує його «відбиток». Звір його з офіційним списком GitHub (там саме
`SHA256:+DiY3wvvV6TuJJhbpZisF/zLDA0zPMSvHdkr4UvCOqU`) і лише тоді пиши `yes`. Відбиток запишеться в
`~/.ssh/known_hosts`. `Permission denied (publickey)` - нормально: свій ключ на GitHub ти додаси в уроці 24.
IP-адреса в дужках у тебе може бути інша.

</details>

## Руками

**Крок 1. Де я в мережі.**

```bash
ip -br a
ip r
resolvectl status
```

> **Нове тут:**
>
> - `ip a` - показує мережеві пристрої і їхні IP-адреси. Назва: ip - Internet Protocol, «інтернет-протокол»; a - address, «адреса».
> - `ip r` - показує маршрути; default via - це шлюз (роутер). Назва: ip - Internet Protocol; r - route, «маршрут».
> - `resolvectl status` - показує, які DNS-сервери використовує система. Назва: resolve control - «керування розвʼязуванням імен» (імʼя сайту → IP-адреса).

Справжній вивід з **тестової** Mint 22.3 - це віртуальна машина, тому там один «кабель» `eth0`, а не Wi-Fi:

```text
lo               UNKNOWN        127.0.0.1/8 ::1/128
eth0             UP             172.29.180.211/20 fe80::215:5dff:fed7:9f51/64
default via 172.29.176.1 dev eth0 proto kernel onlink
172.29.176.0/20 dev eth0 proto kernel scope link src 172.29.180.211
```

На ноутбуці буде інакше: Wi-Fi зветься на кшталт `wlp2s0` (`wl` = wireless), кабель - `enp3s0` або схоже, адреса
від домашнього роутера найчастіше `192.168.x.x`, а `default via 192.168.x.1` - це роутер. `lo` (127.0.0.1) - «сам
собі», є завжди. `resolvectl status` покаже DNS-сервер (`Current DNS Server:`), найчастіше той самий роутер.

**Крок 2. Сходинки 4-6: інтернет, DNS, сайт.**

```bash
ping -c 3 1.1.1.1
ping -c 3 linuxmint.com
curl -I https://linuxmint.com
```

> **Нове тут:**
>
> - `ping`: `1.1.1.1` - адреса DNS-сервера Cloudflare: зручно перевіряти інтернет без участі DNS.
> - `curl` - звертається до сайту за адресою і показує відповідь. Назва: client URL - «клієнт для URL», тобто для адрес у мережі. `-I` - лише заголовки відповіді (head - «голова»), перший рядок - код, напр. HTTP/2 200.

Добре, коли в ping `3 packets transmitted, 3 received, 0% packet loss`, а curl першим рядком пише `HTTP/2 200`.
Справжній кінець ping у тестовій Mint:

```text
--- 1.1.1.1 ping statistics ---
3 packets transmitted, 3 received, 0% packet loss, time 2004ms
rtt min/avg/max/mdev = 8.621/10.028/11.370/1.123 ms
```

`time=...ms` - скільки йде пакет туди й назад. Без `-c 3` ping іде вічно - зупини Ctrl+C.

**Крок 3. Wi-Fi на ноутбуці.**

```bash
nmcli device status
nmcli dev wifi list
nmcli radio wifi
rfkill list
```

> **Нове тут:**
>
> - `nmcli device` - показує, чи підключені Wi-Fi і кабель. Назва: device - «пристрій»: мережеві пристрої очима NetworkManager. `status` - таблиця DEVICE TYPE STATE CONNECTION: пристрій, тип, стан, до якої мережі підключений.
> - `nmcli dev` - те саме, що nmcli device (скорочено). Назва: dev - скорочення від device, «пристрій».
> - `nmcli radio` - показує чи вмикає Wi-Fi (nmcli radio wifi on). Назва: radio - «радіо»: перемикачі Wi-Fi і мобільного інтернету. `wifi` - показати стан Wi-Fi: enabled - увімкнено, disabled - вимкнено.
> - `rfkill list` - показує, чи не заблоковано Wi-Fi і Bluetooth. Назва: list - «список»: блокування кожного радіопристрою.

`nmcli device status` - таблиця `DEVICE TYPE STATE CONNECTION`. Твій Wi-Fi пристрій має бути `connected` і мати
імʼя мережі. У тестовій машині NetworkManager нема (там мережу дає сама віртуалка), тому вивід nmcli тут
не показую. Ось приклад `nmcli device wifi list` з документації NetworkManager (не з твого ноутбука):

```text
*  SSID               MODE    CHAN  RATE       SIGNAL  BARS  SECURITY
   netdatacomm_local  Infra   6     54 Mbit/s  37      ▂▄__  WEP
*  F1                 Infra   11    54 Mbit/s  98      ▂▄▆█  WPA1
   LoremCorp          Infra   1     54 Mbit/s  62      ▂▄▆_  WPA2 802.1X
```

`*` - до якої мережі ти зараз підключений, `SIGNAL` - сила сигналу (0-100).

Якщо Wi-Fi не працює - по черзі:

1. `nmcli radio wifi` пише `disabled` → `nmcli radio wifi on` (або вимкни режим польоту в аплеті).
2. `rfkill list` пише `Soft blocked: yes` → те саме; `Hard blocked: yes` → фізичний перемикач або Fn-клавіша з
   антеною на ноутбуці. (rfkill є на ISO 22.3; у тестовій машині Wi-Fi нема, тому вивід не перевірено.)
3. Мережа в списку є, але не підключається → в аплеті «Забути» мережу і підключитись знову, уважно з паролем.
4. Не допомогло → `sudo systemctl restart NetworkManager` (служби - урок 20).
5. Wi-Fi пристрою взагалі нема в `nmcli device status` → драйвер, «Керування драйверами» (урок 17).

**Крок 4. Хто слухає порти.**

```bash
sudo ss -tulpn
```

> **Нове тут:**
>
> - `sudo` - виконує одну команду від імені адміністратора (root). Назва: su do - «виконати як інший користувач», зазвичай root.
> - `ss` - показує, які програми слухають мережеві порти. Назва: socket statistics - «статистика сокетів» (сокет - «гніздо» для мережевого звʼязку). `-t` - зʼєднання TCP (ssh, https); `-u` - зʼєднання UDP (DNS, мультимедіа); `-l` - лише ті, що слухають (чекають підключень); `-p` - яка програма тримає порт; чужі програми видно лише з sudo; `-n` - номери портів цифрами (22), а не назвами (ssh).

`-t` TCP, `-u` UDP, `-l` лише ті, що слухають, `-p` яка програма (тому `sudo`), `-n` номери замість назв.
Справжній вивід у тестовій Mint (там для перевірок поставлено ssh-сервер, тому є порт 22):

```text
Netid State  Recv-Q Send-Q Local Address:Port Peer Address:PortProcess
udp   UNCONN 0      0         127.0.0.54:53        0.0.0.0:*    users:(("systemd-resolve",pid=92,fd=16))
udp   UNCONN 0      0      127.0.0.53%lo:53        0.0.0.0:*    users:(("systemd-resolve",pid=92,fd=14))
udp   UNCONN 0      0          127.0.0.1:323       0.0.0.0:*
udp   UNCONN 0      0              [::1]:323          [::]:*
tcp   LISTEN 0      4096      127.0.0.54:53        0.0.0.0:*    users:(("systemd-resolve",pid=92,fd=17))
tcp   LISTEN 0      4096         0.0.0.0:22        0.0.0.0:*    users:(("systemd",pid=1,fd=58))
tcp   LISTEN 0      4096   127.0.0.53%lo:53        0.0.0.0:*    users:(("systemd-resolve",pid=92,fd=15))
tcp   LISTEN 0      4096            [::]:22           [::]:*    users:(("systemd",pid=1,fd=59))
```

Як читати: `127.0.0.53:53` - адреса «лише для себе» (127...), ззовні недосяжна, це DNS-кеш systemd-resolved.
`0.0.0.0:22` - слухає на **всіх** адресах, тобто доступно з мережі. На твоєму ноутбуці 22 не буде (сервера нема).
Можуть бути, напр., служба друку cups (`127.0.0.1:631`) і avahi (UDP `5353`) - обидві є на ISO 22.3.

## Далі - за бажанням

Кроки 5-8 - ssh і резервна копія, другим заходом. Крок 5 (ssh-ключ) **потрібен перед уроком 24** (GitHub).

**Крок 5. ssh-ключ.** Підпис після `-C` - будь-який текст, щоб упізнати ключ (пошта не обовʼязкова).

```bash
ssh-keygen -t ed25519 -C "evgen-laptop"
```

> **Нове тут:**
>
> - `ssh-keygen` - робить пару ssh-ключів і показує їхні відбитки. Назва: ssh key generator - «генератор ssh-ключів». `-t` - тип ключа; ed25519 - сучасний і короткий, його радить GitHub; `-C` - коментар-підпис, щоб упізнати ключ (напр. "evgen-laptop"); пошта не обовʼязкова; `ed25519` - тип ключа (після -t).
> - `"..."` - текст з пробілами одним словом, $ підставляється. Назва: подвійні лапки - «усе це одне слово, але $ працює».

На перше питання - просто Enter (типове місце), далі двічі пароль ключа (passphrase). З паролем безпечніше:
якщо ноутбук вкрадуть, ключ без пароля не спрацює. Символи пароля не видно. Справжній сеанс (у тестовій Mint пароль
ключа порожній, а «малюнок» і відбиток у тебе будуть інші):

```text
Generating public/private ed25519 key pair.
Enter file in which to save the key (/home/evgen/.ssh/id_ed25519):
Enter passphrase (empty for no passphrase):
Enter same passphrase again:
Your identification has been saved in /home/evgen/.ssh/id_ed25519
Your public key has been saved in /home/evgen/.ssh/id_ed25519.pub
The key fingerprint is:
SHA256:PGmwaTOKyeoFpxMOetwQ5+c3QMZ7P3nmHIZpbcv+QR8 evgen-laptop
The key's randomart image is:
+--[ED25519 256]--+
|                 |
|     .           |
|  . . =          |
|   + o * .       |
|.o... X S     .E |
|+o== = * o = . ..|
|.+*.o . o B B . .|
| oo    . o X o . |
|o.         .*..  |
+----[SHA256]-----+
```

Якщо теки `~/.ssh` ще не було, після першого питання ssh-keygen сам її зробить і напише
`Created directory '/home/evgen/.ssh'.` Перевір права і подивись публічний ключ:

```bash
ls -la ~/.ssh
ssh-keygen -l -f ~/.ssh/id_ed25519.pub
cat ~/.ssh/id_ed25519.pub
```

```text
drwx------  2 evgen evgen 4096 Nov 18 09:58 .
-rw-------  1 evgen evgen  399 Nov 18 09:58 id_ed25519
-rw-r--r--  1 evgen evgen   94 Nov 18 09:58 id_ed25519.pub
256 SHA256:PGmwaTOKyeoFpxMOetwQ5+c3QMZ7P3nmHIZpbcv+QR8 evgen-laptop (ED25519)
```

> **Нове тут:**
>
> - `ls` - показує, що лежить у теці. Назва: list - «список» (вмісту теки). `-l` - докладний список: права, власник, розмір у байтах, дата зміни (long); `-a` - показати й приховані (назва з крапки), разом з . і .. (all); `~/.ssh` - показати вміст іншої теки, не заходячи в неї.
> - `ssh-keygen`: `-l` - показати відбиток (fingerprint) ключа - коротку «назву» ключа, що починається з SHA256; `-f` - файл: куди записати новий ключ або який ключ читати (з -l).
> - `cat` - показує вміст файлу. Назва: concatenate - «зчепити»: склеює кілька файлів в один вивід.
> - `~` - домашня тека /home/evgen. Назва: tilde («тильда») - домашня тека.

(тут лише потрібні рядки виводу). `cat` покаже один рядок `ssh-ed25519 AAAAC3...  evgen-laptop` - це і є те, що
дають GitHub чи серверу. Якщо права не такі: `chmod 700 ~/.ssh` і `chmod 600 ~/.ssh/id_ed25519`.

**Крок 6. Перше підключення до GitHub** (ключ туди ще не додано - урок 24):

```bash
ssh -T git@github.com
```

Звір відбиток з передбачення 4, напиши `yes`. Має закінчитись на `Permission denied (publickey)` - це добре: звʼязок
є, просто GitHub ще не знає твій ключ.

**Крок 7. Резервна копія лаб rsync-ом** (на флешку - заміни шлях на свою флешку з `/media/evgen/`):

```bash
mkdir -p ~/backup
rsync -av ~/univer/labs/ ~/backup/labs/
rsync -av ~/univer/labs/ ~/backup/labs/
```

> **Нове тут:**
>
> - `mkdir` - створює нову теку. Назва: make directory - «зробити теку». `-p` - створює і всі проміжні теки шляху; якщо тека вже є - мовчить, без помилки.

Вдруге rsync нічого не копіює (`sending incremental file list` і одразу підсумок) - бо нічого не змінилось. Тому
rsync і беруть для резервних копій. Автоматично щодня - урок 23 (cron).

`~/backup` на тому самому диску - **лише тренування**: помре диск чи вкрадуть ноутбук - зникнуть обидві копії.
Справжня копія - на флешці чи зовнішньому диску (`rsync -av ~/univer/labs/ /media/evgen/НАЗВА/labs/`) і в git на
GitHub (урок 24).

**Крок 8 (коли буде сервер).** Якщо тобі дадуть доступ до сервера (кафедра, хмара, другий компʼютер), шаблон:

```text
ssh-copy-id користувач@адреса            раз: попросить пароль і допише твій .pub на сервер
ssh користувач@адреса                    далі вхід по ключу
scp lr1_1.py користувач@адреса:labs/     файл туди
scp користувач@адреса:labs/out.txt .     файл звідти сюди (крапка = поточна тека)
rsync -av ~/univer/labs/ користувач@адреса:labs/
exit                                     вийти з сервера (або Ctrl+D)
```

А щоб не набирати адресу щоразу, у `~/.ssh/config` (створи в nano, права `600`):

```text
Host kafedra
    HostName адреса.сервера
    User користувач
    IdentityFile ~/.ssh/id_ed25519
```

Тепер `ssh kafedra`, `scp lr1_1.py kafedra:labs/`, `rsync -av ~/univer/labs/ kafedra:labs/`. У тестовій Mint це
перевірено на ssh-сервері самої машини (`localhost`): вхід по ключу, `scp` і `rsync` через коротке імʼя.

## Типові помилки

Тексти помилок нижче - справжні, з тестової Mint 22.3 (мережу там відрізано командою `sudo unshare -n`). Якщо Mint
українською, ping пише українською (у дужках - з файлу перекладу `libc.mo` пакета `language-pack-uk-base`), а
`curl` і `ssh` - англійською (перевірено запуском з українською мовою). Англійський текст для пошуку:
`LC_ALL=C ping ...`.

- **`ping: linuxmint.com: Temporary failure in name resolution`** (`ping: linuxmint.com: Тимчасова помилка
  розв'язання назв`) - DNS-сервер недосяжний. Якщо при цьому
  `ping 1.1.1.1` працює - проблема саме в DNS: перепідключи Wi-Fi; якщо часто - у «Мережних зʼєднаннях» задай DNS
  вручну (напр. `1.1.1.1`). `Name or service not known` (`Невідома назва чи сервіс`) - DNS працює, але такого
  імені нема (одруківка).
- **`ping: connect: Network is unreachable`** (`ping: connect: Не вдалося отримати доступ до мережі`) - нема
  маршруту назовні: Wi-Fi не підключено (сходинки 1-3).
- **`curl: (6) Could not resolve host: linuxmint.com`** - те саме, що з ping: DNS або помилка в адресі.
- **`ssh: Could not resolve hostname github.com: Temporary failure in name resolution`** - знову DNS, а не ssh.
- **`WARNING: UNPROTECTED PRIVATE KEY FILE!`** - права ключа (передбачення 3). `chmod 600 ~/.ssh/id_ed25519`.
- **`Permission denied (publickey).`** - сервер не знає твій публічний ключ (не зробив `ssh-copy-id` або не додав на
  GitHub), або ssh бере інший ключ. Подивись, що він пробує: `ssh -v ...` (рядки `Offering public key`).
- **`WARNING: REMOTE HOST IDENTIFICATION HAS CHANGED!`** - відбиток сервера не той, що в `known_hosts`. Справжній
  вивід (у тестовій Mint відбиток GitHub навмисно зіпсовано):

```text
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
@    WARNING: REMOTE HOST IDENTIFICATION HAS CHANGED!     @
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
IT IS POSSIBLE THAT SOMEONE IS DOING SOMETHING NASTY!
Someone could be eavesdropping on you right now (man-in-the-middle attack)!
It is also possible that a host key has just been changed.
The fingerprint for the ED25519 key sent by the remote host is
SHA256:+DiY3wvvV6TuJJhbpZisF/zLDA0zPMSvHdkr4UvCOqU.
Please contact your system administrator.
Add correct host key in /home/evgen/.ssh/known_hosts to get rid of this message.
Offending ED25519 key in /home/evgen/.ssh/known_hosts:1
  remove with:
  ssh-keygen -f '/home/evgen/.ssh/known_hosts' -R 'github.com'
Host key for github.com has changed and you have requested strict checking.
Host key verification failed.
```

  Буває, коли сервер перевстановили, а буває - атака. **Не видаляй рядок навмання**: спершу спитай адміністратора
  (для GitHub - звір з офіційним списком відбитків). Лише коли впевнений - `ssh-keygen -R адреса` і підключись знову.
- **`ssh: connect to host ... port 22: Connection refused`** - на тому компʼютері нема ssh-сервера або він вимкнений.
  Твій ноутбук так відповідає завжди: сервера на Mint нема.
- **`Connection timed out`** - адреса не та, або брандмауер чи мережа (напр. гостьовий Wi-Fi) блокує порт 22
  (цей текст у тестовій Mint не відтворено).

## Як роблять профі

- **Ключі ed25519 з паролем, паролі для входу вимкнені.** GitHub у документації генерує саме
  `ssh-keygen -t ed25519` і радить пароль ключа (passphrase); на серверах вхід паролем вимикають, лишають ключі.
- **`~/.ssh/config` замість довгих команд.** Короткі імена (`Host kafedra`) розуміють ssh, scp, rsync і git.
  Курс MIT «Missing Semester» вчить цього в лекції про командний рядок.
- **Діагностика сходинками, а не «перезавантаж усе».** Спершу IP і шлюз, потім ping за IP, потім за імʼям, потім
  сайт. Так роблять адміністратори, і так поломку видно за хвилину.
- **Відбиток сервера звіряють.** Для GitHub офіційні відбитки опубліковані в документації; сліпе `yes` на новому
  сервері - те саме, що не дивитись, кому віддаєш пароль.

## Самоперевірка

1. `ping -c 3 1.1.1.1` працює, а `ping -c 3 linuxmint.com` пише `Temporary failure in name resolution`. Що
   зламалось?
2. Який файл ключа можна дати іншим, а який ніколи? Які права мають бути в теки `~/.ssh` і приватного ключа?
3. Чим `rsync -av lr1/ backup/` відрізняється від `rsync -av lr1 backup/`?
4. Що означає `0.0.0.0:22` у виводі `sudo ss -tulpn` і чи має таке бути на твоєму ноутбуці?
5. ssh пише `REMOTE HOST IDENTIFICATION HAS CHANGED!`. Що робити і чого не робити?

<details markdown="1"><summary>Відповіді</summary>

1. DNS: пакети до інтернету доходять (за IP), а DNS-сервер недосяжний, і імена не перетворюються на адреси.
   (`Name or service not known` означало б інше: DNS працює, але такого імені нема - одруківка.)
2. Давати - `id_ed25519.pub` (публічний). Ніколи - `id_ed25519` (приватний). `~/.ssh` - `700`, приватний ключ - `600`.
3. `lr1/` копіює вміст теки прямо в `backup/`; `lr1` копіює саму теку, вийде `backup/lr1/...`.
4. Програма (ssh-сервер) слухає порт 22 на всіх адресах, тобто до неї можна підключитись з мережі. На твоєму
   ноутбуці такого не буде: `openssh-server` на Mint не встановлено.
5. Не писати навмання `ssh-keygen -R`. Спершу дізнатись у власника сервера (або в офіційному списку), чи змінювався
   ключ. Лише коли зміна справжня - прибрати старий рядок і підключитись знову, звіривши новий відбиток.

</details>

## Джерела

- Список пакетів ISO Mint 22.3 (`casper/filesystem.manifest`: network-manager 1.46.0, network-manager-openvpn,
  network-manager-pptp, openssh-client, rsync, cups, avahi-daemon; openssh-server нема) -
  https://mirrors.kernel.org/linuxmint/stable/22.3/ - відкрито 18.11.2026
- nmcli і приклади - https://networkmanager.dev/docs/api/latest/nmcli.html ,
  https://networkmanager.dev/docs/api/latest/nmcli-examples.html - відкрито 18.11.2026
- Імена мережевих пристроїв (`wl` - Wi-Fi, `en` - кабель) -
  https://www.freedesktop.org/software/systemd/man/latest/systemd.net-naming-scheme.html - відкрито 18.11.2026
- GitHub: створення ключа, перевірка підключення, офіційні відбитки -
  https://docs.github.com/en/authentication/connecting-to-github-with-ssh/generating-a-new-ssh-key-and-adding-it-to-the-ssh-agent ,
  https://docs.github.com/en/authentication/connecting-to-github-with-ssh/testing-your-ssh-connection ,
  https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/githubs-ssh-key-fingerprints -
  відкрито 18.11.2026
- OpenSSH (ssh, ssh_config, ssh-keygen) - https://www.openssh.com/manual.html ,
  https://man.openbsd.org/ssh_config - відкрито 18.11.2026
- MIT Missing Semester - https://missing.csail.mit.edu/ - відкрито 18.11.2026
- Усі показані виводи (крім nmcli) - запуском у тестовій Mint 22.3 (OpenSSH 9.6p1, rsync 3.2.7), 18.11.2026
