# Шпаргалки

Усе на одній сторінці. Розгорни потрібну.

<details markdown="1" open><summary>Python</summary>


```
7/2=3.5  7//2=3  -7//2=-4  7%2=1  -7%2=1
n%10 остання цифра   n//10%10 передостання
input() -> str!  "2"+"3"="23"  int(input())
True=1 False=0   "так"*(x>0)
a if умова else b   (вираз, не оператор)
not > and > or      0 < x < 10
range(1,10,2): 1 3 5 7 9  (stop не входить)
while: змінна з умови міняється всередині
break - вихід; for...else - якщо без break
НСД: while b: a, b = b, a % b
НСК = a*b // НСД;  дільники до d*d <= n
Фібоначчі: p, c = c, p + c  (одночасно!)
ряд eˣ: a = a * x / n;  S = S + a
ε: while abs(cur - prev) >= eps
бісекція: f(a)*f(c) < 0 -> b = c
  кроків ≈ log₂((b - a) / ε)
Горнер: v = v * x + coef
lst[-1] останній  lst[1:3]  lst[::-1]
append -> None!   b = a НЕ копія: a.copy()
[[0]*m for _ in range(n)]  не [[0]*m]*n
(5,) кортеж   (5) число
sorted(.., key=lambda r: (-r[1], r[0]))
sum(1 for x in lst if x % 2 == 0)
f"{x:.2f}" f"{s:<10}" f"{n:>5}" f"{x:.3g}"
print(a, b, sep=", ", end="")
```

**Функція:** без `return` повертає `None`. Один `return`, частини через `\n`. Назву і doctest
із заготовки не міняти.

**doctest:** порівнює вивід **як текст**: рядок у лапках, зайвий пробіл - падіння.
`python -m doctest -v file.py`.

**PEP 8:** 4 пробіли; рядок до 79; 2 порожні рядки між функціями; пробіли навколо `=` і після
коми; `snake_case`, `UPPER_CASE` для констант; не `list`, `sum`, `str`, `id` як імена;
назви змістовні (`last_digit`, а не `a`).

**Лінтери:** pycodestyle (PEP 8), flake8 (+ невикористане), ruff (швидше), mypy (типи),
black (переформатовує).

**Помилки:** `TypeError` "2"+3; `ValueError` int("abc"); `ZeroDivisionError`;
`IndexError` lst[10]; `KeyError` d["нема"]; `NameError` нема змінної.

**Залік:** формат і бали невідомі - спитати викладача.

</details>

<details markdown="1"><summary>Linux Mint</summary>


Курс: `05_Програмування\Linux-Mint\`. Термінал Ctrl+Alt+T; копіювати/вставити - Ctrl+Shift+C / V.
Помилка українською, а шукати треба англійською: `LC_ALL=C команда` (урок 00).

**Перед зміною системи - знімок:** `sudo timeshift --create --comments "перед ..."`
```text
sudo apt update      apt list --upgradable      sudo apt upgrade (прочитай список, без -y)
flatpak update       fwupdmgr get-updates (прошивки)      sudo timeshift --list
```
**Python** - системний python3 (3.12) не чіпати і не видаляти; бібліотеки - лише у venv:
```text
sudo apt install python3-venv python3-pip python3-tk git
python3 -m venv ~/univer/.venv    source ~/univer/.venv/bin/activate    (deactivate - вимкнути)
pip install pytest flake8 black mypy ruff     pip list --outdated     pip install -U пакет
```
`externally-managed-environment` = ти поза venv. Не `sudo pip`, не `--break-system-packages`.

**Лаба** (`univer` = cd + venv; `univer`, `perevir` і htop ставить `ustanovka-mint.sh`):
```text
mkdir -p ~/univer/labs/lr1 && cd ~/univer/labs/lr1    nano lr1_1.py (Ctrl+S, Ctrl+X)
python3 lr1_1.py -v                              doctest з подробицями
python3 -m pytest --doctest-modules -q lr1_1.py  doctest з чесним кодом виходу
printf "127\n" | python3 -m pytest --doctest-modules -q -s lr1_1.py   якщо є input()
perevir lr1_1.py [відповіді на input()]   doctest, black, flake8, pycodestyle, ruff (78), mypy
```
`python3 -m doctest файл.py` на файлі з `doctest.testmod()` у кінці тестує ще й сам doctest і пише
чужий провал `... in __main__.DebugRunner` - твій код ні до чого. Бери `-v`, pytest або `perevir`.

**Налагодження:**
```text
print(f"{x=}")    breakpoint()    python3 -i lab.py (змінні після падіння)
python3 -m pdb lab.py: n s c l ll p pp w u d  b 12  b 12, x > 5  tbreak  cl 1  r  until  j  q
python3 -m pdb -c continue lab.py (post-mortem)   python3 -X dev lab.py   python3 -W error lab.py
```
**Файли, пошук, місце:**
```text
pwd  ls -la  cd ~  cd ..  cd -    Tab - дописати    Ctrl+R - пошук в історії    man команда (q)
cp -i a b   mv -i a b   rm -i файл   gio trash файл (у смітник)   mkdir -p a/b   ln -s ціль імʼя
grep -rn "print(" ~/univer/labs    find ~/univer -name "*.py" -mtime -1
df -h /    du -h --max-depth=1 | sort -h    lsblk -o NAME,SIZE,MODEL,MOUNTPOINT
```
**Права, програми, процеси, журнали:**
```text
chmod +x run.sh   ls -l   id   groups   sudo -k      sudo apt install ./файл.deb (з ./)
apt search назва   sudo apt install назва   sudo apt remove назва   sudo apt autoremove
htop (F9 вбити, F10 вийти)   pgrep -af назва   kill PID   Ctrl+C   flatpak list
systemctl status NetworkManager    systemctl --failed    sudo journalctl -b -p err
```
**Мережа, git, безпека:**
```text
ip -br a   ping -c 3 1.1.1.1   ping -c 3 linuxmint.com   nmcli device status   sudo ss -tulpn
ssh-keygen -t ed25519   ssh -T git@github.com   sudo ufw enable   sudo ufw status verbose
git status   git add .   git commit -m "ЛР1 завд. 1"   git log --oneline   git push
```
**Cinnamon:** Super - меню, Ctrl+Alt+L - заблокувати (Super+L - НЕ блокування), Super+D - стіл,
Super+E - домашня тека, Super+стрілки - половина екрана, Ctrl+Alt+←/→ - робочий простір,
Ctrl+Alt+Esc - перезапустити Cinnamon, Print - знімок екрана.
**Не завантажується:** Shift/Esc при старті → GRUB → Advanced options → старе ядро. Чорний екран →
Ctrl+Alt+F2 (TTY), назад Ctrl+Alt+F7. Зовсім погано → live USB → Timeshift → відновити.

</details>

<details markdown="1"><summary>Git і GitHub</summary>



## Один раз на ноутбуці (уроки 02-03)
```
sudo apt install git
git config --global user.name "Твоє Імʼя"
git config --global user.email "128326252+Evge14n@users.noreply.github.com"
git config --global init.defaultBranch main
git config --global core.editor nano
git config --global pull.rebase false
git config --global core.quotepath false
ssh-keygen -t ed25519 -C "128326252+Evge14n@users.noreply.github.com"
ssh -T git@github.com            (відповідь: Hi Evge14n! You've successfully authenticated...)
gh auth login -p ssh -w
```

## Три зони
```
робоча тека  --git add-->  індекс (staging)  --git commit-->  репозиторій  --git push-->  GitHub
             <-git restore-                   <-restore --staged-                  <-git pull--
```

## Щодня (уроки 04-06)
| Команда | Що робить |
|---|---|
| `git status` | що змінено і що піде в коміт |
| `git add файл` / `git add .` | вибрати в коміт |
| `git commit -m "Завд. 2: перевірка вводу"` | знімок; перший рядок ≤ 50 знаків, що змінено |
| `git log --oneline --graph --all` | історія з гілками |
| `git diff` / `git diff --staged` | що змінено / що вже в індексі |
| `git show HEAD` | останній коміт повністю |
| `.gitignore` | `.venv/` `__pycache__/` `*.pyc` `.pytest_cache/` |
| `git rm --cached -r .venv` | прибрати з git, лишити на диску |

## Гілки і конфлікт (уроки 07-08)
| Команда | Що робить |
|---|---|
| `git switch -c lr3` | нова гілка і перейти |
| `git switch main` | назад на main |
| `git merge lr3` | злити lr3 у поточну |
| `git branch -d lr3` | видалити злиту гілку |
| `git merge --abort` | скасувати злиття з конфліктом |
```
<<<<<<< HEAD          ← твоя версія
=======
>>>>>>> lr3           ← версія з гілки
```
- Конфлікт: відкрив у nano, лишив правильне, прибрав маркери, `git add файл`, `git commit`.

## GitHub (уроки 09-11, 16)
| Команда | Що робить |
|---|---|
| `git clone git@github.com:Evge14n/univer-labs.git` | скачати репо |
| `git push -u origin lr3` | перший пуш гілки |
| `git push` / `git pull` | відправити / забрати і злити |
| `git fetch` | лише забрати, не зливати |
| `gh pr create --fill` | Pull Request з гілки |
| `gh pr merge --squash --delete-branch` | злити PR |
- «rejected (fetch first)» = на GitHub є нове: `git pull`, потім `git push`.
- «Closes #3» у коміті закриває issue 3, коли коміт потрапить у main.

## Скасувати (уроки 12-13)
| Сталося | Лікування |
|---|---|
| зіпсував файл, не комітив | `git restore файл` |
| додав у індекс зайве | `git restore --staged файл` |
| помилка в останньому коміті, ще не push | `git commit --amend` або `git reset --soft HEAD~1` |
| поганий коміт уже на GitHub | `git revert хеш` (новий коміт) |
| «загубив» коміт після reset --hard | `git reflog`, потім `git reset --hard HEAD@{1}` |
| треба терміново на іншу гілку | `git stash`, потім повернувся - `git stash pop` |
- `git push --force` у спільну гілку - НІКОЛИ. Якщо дуже треба у своїй: `--force-with-lease`.

## Здача ЛР (урок 14, «Лаби в git»)
```
git switch -c lr3            (на початку лаби)
git status                   (подивись, що змінено)
git add lr3 && git commit -m "Завд. 1: ..."   (після кожного завдання з зеленим doctest)
git switch main && git merge lr3
git tag -a lr3-zdano -m "ЛР3 здано"
git push origin main lr3-zdano
```
- `--follow-tags` везе лише анотовані теги (`-a`). GitHub Pages на безкоштовному плані - лише з публічного репо.

</details>

<details markdown="1"><summary>Безпечний код</summary>


```
ПРАВИЛО 0: усе ззовні - вороже,
поки не перевірив (ввід, файл, URL,
cookie, JSON, назва файлу)

ВВІД      int() у try/except + межі
          ніколи eval(ввід), exec(ввід)
          текст -> дані: json.loads,
          ast.literal_eval
ІНʼЄКЦІЇ  SQL: "... WHERE name = ?",
          (name,)
          НЕ f-рядок, НЕ +
          shell: subprocess.run([...]),
          без shell=True
ДОСТУП    перевірка на початку функції
          чий обʼєкт? (IDOR)
          fail closed: помилка = відмова
ЛІМІТИ    len(ввід) ДО роботи
          розмір файлу, к-сть спроб
ФАЙЛИ     p = (BASE / name).resolve()
          p.is_relative_to(BASE)
СЕКРЕТИ   не в коді: os.environ, .env
          .env у .gitignore,
          читати: python-dotenv
          витік у git -> замінити ключ
          токени: secrets, НЕ random
ПОМИЛКИ   користувачу коротко + код
          traceback - лише в лог
          DEBUG = False на сервері
PIP       venv + requirements.txt
          pip-audit (з дефісом!)
          назву - з сайту проєкту,
          на pypi.org звір автора
URL       лише https, timeout
          SSRF: список дозволених хостів
          хост: urlparse(url).hostname
XSS       html.escape(все від людей)
          посилання - лише https
ПАРОЛІ    Argon2id (argon2-cffi)
          НЕ sha256, НЕ відкрито
ТОКЕНИ    порівнювати лише так:
          hmac.compare_digest(
            a.encode(), b.encode())
БАЗА      параметри; колонка - зі списку
          права БД - мінімальні
```

OWASP Top 10:2025: A01 доступ (IDOR, path traversal, SSRF, CSRF) · A02 налаштування · A03 ланцюг постачання (pip) ·
A04 криптографія · A05 інʼєкції (SQL, команди, XSS, eval) · A06 небезпечний дизайн · A07 автентифікація ·
A08 цілісність · A09 логи й тривоги · A10 обробка помилок (fail open, витік у помилці).

</details>

<details markdown="1"><summary>Linux у WSL</summary>



**Де я і що тут**
```
pwd                 де я
ls -la              що тут (детально, з прихованими)
cd тека             зайти;  cd ..  вище;  cd ~  додому
/mnt/c, /mnt/d      диски Windows
explorer.exe .      відкрити теку в Провіднику
```
Tab - дописати назву. ↑ - попередня команда. Ctrl+R - пошук в історії.

**Файли і теки**
```
mkdir -p a/b        створити теку
touch f.py          порожній файл
cp f.py g.py        копія (cp -r тека нова - теку)
mv f.py g.py        перейменувати / перемістити
rm f.py             видалити НАЗАВЖДИ (кошика нема)
rmdir тека          видалити порожню теку
```
Перед `rm *.щось` - спершу `ls *.щось`. Назви з пробілом - у лапки.

**Подивитись і редагувати**
```
cat f               весь файл
less f              гортати, q - вийти
tail -n 20 f        кінець (head - початок)
nano f.py           Ctrl+O Enter - зберегти, Ctrl+X - вийти
code .              VS Code у цій теці
```

**Права і sudo**
```
ls -l               -rwxr-xr-x : власник / група / інші
chmod +x s.sh       дозволити запуск, потім ./s.sh
chmod 755 s.sh      r=4 w=2 x=1
sudo команда        від root (пароль Ubuntu)
```
Свої файли - без sudo.

**Пакети**
```
sudo apt update
sudo apt upgrade
sudo apt install назва
```
Python-бібліотеки - лише у venv (pip).

**Процеси**
```
Ctrl+C              зупинити;  Ctrl+Z - призупинити, fg - назад
pgrep -af python    PID усіх python
kill PID            зупинити (kill -9 PID - силою)
top                 хто їсть процесор, q - вийти
wsl --shutdown      (у PowerShell) перезапустити Ubuntu
```

**Пайпи і пошук**
```
к > f    перезаписати    к >> f   дописати    к 2> f   помилки
к1 | к2  вивід к1 → вхід к2
grep -n "def " f.py      grep -rn "текст" тека
printf "5\n" | python lab.py      ввід без клавіатури
```

**Python і лаби**
```
univer              ~/univer + venv увімкнено, видно (.venv)
python lab.py       doctest (testmod у файлі) + програма
python lab.py -v    doctest з подробицями
perevir lab.py      doctest (pytest) + flake8 78 + mypy
deactivate
```
Не `python -m doctest`, якщо в файлі є `doctest.testmod()` - чужий «DebugRunner Failed».

**git**
```
git init
git status
git add .
git commit -m "що зробив"
git log --oneline
git diff
git restore f.py
```

**bash-скрипт**
```
#!/bin/bash
x=5                 без пробілів біля =
echo "$1"           аргумент, у лапках
if [ -f "$1" ]; then ... fi
for f in *.py; do ... done
```

**Помилки**: `Permission denied` → chmod +x або чужий файл; `command not found` → нема програми або забув `./`;
`$'\r'` → CRLF, VS Code → LF; `externally-managed-environment` → увімкни venv; `dpkg was interrupted` →
`sudo dpkg --configure -a`.

</details>

