#!/bin/bash
# Налаштування Ubuntu (WSL) для лаб з програмування.
# Запуск:  bash ustanovka.sh
#   або:   bash ustanovka.sh "C:\Users\Євген\Documents\Програмування"
#          (шлях до теки з лабами на Windows - тоді в ~/univer буде посилання на неї)
# Скрипт можна запускати скільки завгодно разів - нічого не зламає і нічого не видаляє.

set -e

if [ -z "$NO_APT" ]; then
echo "== 1/5 Оновлення Ubuntu (попросить пароль від Ubuntu, символи не видно - це нормально)"
echo "   Перший раз це 5-20 хвилин. Не закривай вікно, поки не з'явиться «Готово»."
sudo apt-get update
sudo DEBIAN_FRONTEND=noninteractive apt-get -y upgrade

echo "== 2/5 Python, venv, pip, git, pytest, flake8, turtle (python3-tk), nano, tree"
sudo DEBIAN_FRONTEND=noninteractive apt-get -y install \
    python3 python3-venv python3-pip python3-tk python3-pytest flake8 \
    git nano tree
fi

echo "== 3/5 Тека ~/univer і віртуальне середовище ~/univer/.venv"
mkdir -p ~/univer
if [ ! -x ~/univer/.venv/bin/python ]; then
    python3 -m venv ~/univer/.venv
fi
~/univer/.venv/bin/python -m pip install --quiet --upgrade pip
~/univer/.venv/bin/python -m pip install --quiet \
    pytest flake8 black pycodestyle ruff mypy matplotlib numpy

echo "== 4/5 Посилання на теку з лабами"
if [ -n "$1" ]; then
    target=$(wslpath -u "$1")
elif [ -d "/mnt/d/Універ/05_Програмування" ]; then
    target="/mnt/d/Універ/05_Програмування"
else
    target=""
fi
if [ -n "$target" ] && [ -d "$target" ]; then
    if [ -e ~/univer/prog ] && [ ! -L ~/univer/prog ]; then
        echo "   ~/univer/prog уже є і це не посилання - не чіпаю"
    else
        ln -sfn "$target" ~/univer/prog
        echo "   ~/univer/prog -> $target"
    fi
else
    echo "   Теку з Windows не задано - лаби клади в ~/univer/labs (так найшвидше)"
    echo "   (або запусти ще раз: bash ustanovka.sh \"C:\\шлях\\до\\лаб\")"
fi
mkdir -p ~/univer/labs ~/univer/praktyka

echo "== 5/5 Команди univer і perevir у ~/.bashrc"
if ! grep -q "# >>> univer >>>" ~/.bashrc; then
    cat >> ~/.bashrc <<'BASHRC'
# >>> univer >>>
# univer  - перейти в ~/univer і увімкнути venv
alias univer='cd ~/univer && source ~/univer/.venv/bin/activate'
# perevir файл.py - doctest + flake8 + mypy, як вимагає викладач
perevir() {
    if [ -z "$1" ]; then echo "Напиши: perevir назва_файлу.py"; return 1; fi
    local py=~/univer/.venv/bin/python
    echo "--- doctest"
    "$py" -m doctest "$1" && echo "doctest: усе пройшло"
    echo "--- flake8 (рядок до 78 символів)"
    "$py" -m flake8 --max-line-length=78 "$1" && echo "flake8: зауважень нема"
    echo "--- mypy"
    "$py" -m mypy --ignore-missing-imports "$1"
}
# <<< univer <<<
BASHRC
    echo "   додано (відкрий нове вікно Ubuntu або виконай: source ~/.bashrc)"
else
    echo "   уже було"
fi

if [ -z "$(git config --global user.name)" ]; then
    echo
    echo "Git ще не знає, хто ти. Один раз виконай (своє ім'я і пошту):"
    echo '   git config --global user.name "Твоє Імʼя Прізвище"'
    echo '   git config --global user.email "твоя@пошта"'
fi

echo
echo "Готово. Перевірка:"
~/univer/.venv/bin/python --version
git --version
~/univer/.venv/bin/python -m pytest --version
~/univer/.venv/bin/python -m flake8 --version | head -1
~/univer/.venv/bin/python -c "import tkinter; print('tkinter (turtle) є, Tk', tkinter.TkVersion)"
