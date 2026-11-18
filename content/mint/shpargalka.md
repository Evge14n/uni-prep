# Linux Mint - шпаргалка (1 сторінка)

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