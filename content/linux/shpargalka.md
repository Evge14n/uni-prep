# Linux - шпаргалка (1 сторінка)


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