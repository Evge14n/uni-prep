#!/bin/bash
# Налаштування Linux Mint 22.x для лаб з програмування (ULINUX2, 18.11.2026).
# Запуск у терміналі Mint:   bash ustanovka-mint.sh
# Можна запускати скільки завгодно разів - нічого не видаляє і не зламає.
# Систему НЕ оновлює (це робить Менеджер оновлень, урок 02) - лише доставляє потрібне для лаб.

set -e

if ! grep -qi "mint\|ubuntu" /etc/os-release; then
    echo "Схоже, це не Linux Mint / Ubuntu - скрипт розрахований на Mint 22.x. Зупиняюсь."
    exit 1
fi
. /etc/os-release
echo "Система: $PRETTY_NAME (база Ubuntu ${UBUNTU_CODENAME:-?})"

if [ -z "$NO_APT" ]; then
    echo
    echo "== 1/4 Пакети для лаб: venv, pip, tkinter (turtle), git, htop, tree"
    echo "   Попросить пароль (замість символів - зірочки, це нормально)."
    sudo apt-get update
    sudo DEBIAN_FRONTEND=noninteractive apt-get -y install \
        python3-venv python3-pip python3-tk python3-doc git htop tree
fi

echo
echo "== 2/4 Тека ~/univer і віртуальне середовище ~/univer/.venv"
mkdir -p ~/univer/labs ~/univer/praktyka
if [ ! -x ~/univer/.venv/bin/python ]; then
    python3 -m venv ~/univer/.venv
fi
~/univer/.venv/bin/python -m pip install --quiet --upgrade pip
~/univer/.venv/bin/python -m pip install --quiet \
    pytest flake8 black pycodestyle ruff mypy matplotlib numpy

echo
echo "== 3/4 Команди univer і perevir у ~/.bashrc"
# старий блок (якщо був) прибираємо і пишемо свіжий
sed -i '/# >>> univer >>>/,/# <<< univer <<</d' ~/.bashrc
cat >> ~/.bashrc <<'BASHRC'
# >>> univer >>>
# univer  - перейти в ~/univer і увімкнути venv
alias univer='cd ~/univer && source ~/univer/.venv/bin/activate'
# perevir файл.py [ввід ...] - doctest + black + flake8 + pycodestyle + ruff + mypy, як вимагає викладач
#   perevir lr1_1.py 127   - якщо файл питає input(), відповіді пиши після назви (кожна - окремий рядок вводу)
# doctest - через pytest: він не плутається з doctest.testmod() у самому файлі
perevir() {
    if [ -z "$1" ]; then echo "Напиши: perevir файл.py [відповіді на input() через пробіл]"; return 1; fi
    local f="$1"; shift
    local py=~/univer/.venv/bin/python out rc
    out=$(mktemp)
    echo "--- doctest (через pytest; зупиню, якщо довше 120 с)"
    if [ $# -gt 0 ]; then
        printf '%s\n' "$@" | timeout 120 "$py" -m pytest --doctest-modules -q -s -p no:cacheprovider "$f" > "$out" 2>&1
    else
        timeout 120 "$py" -m pytest --doctest-modules -q -p no:cacheprovider "$f" < /dev/null > "$out" 2>&1
    fi
    rc=$?
    if [ $rc = 0 ]; then
        echo "doctest: усе пройшло ($(tail -n 1 "$out"))"
    elif [ $rc = 5 ]; then
        echo "doctest: у файлі нема жодного doctest (прикладів >>>)"
    elif [ $rc = 124 ]; then
        echo "doctest: довше 120 с - зупинив. Якийсь приклад рахує дуже довго - перевір функції по одній у python3 -i $f"
    elif grep -q "reading from stdin\|EOFError" "$out"; then
        echo "doctest: файл питає input() при запуску. Дай відповіді після назви: perevir $f 5"
    else
        cat "$out"
        echo "doctest: Є ПОМИЛКИ (дивись Expected / Got вище)"
    fi
    rm -f "$out"
    echo "--- black (лише перевірка, файл не змінює; виправити: black -l 78 $f)"
    if "$py" -m black --check -q -l 78 "$f"; then echo "black: оформлення ок"
    else echo "black: ТРЕБА ПЕРЕФОРМАТУВАТИ - виконай: python3 -m black -l 78 $f"; fi
    echo "--- flake8 і pycodestyle (рядок до 78 символів, як каже викладач)"
    "$py" -m flake8 --max-line-length=78 "$f" && echo "flake8: зауважень нема"
    "$py" -m pycodestyle --max-line-length=78 "$f" && echo "pycodestyle: зауважень нема"
    echo "--- ruff"
    "$py" -m ruff check -q --line-length 78 "$f" && echo "ruff: зауважень нема"
    echo "--- mypy"
    "$py" -m mypy --ignore-missing-imports "$f"
}
# <<< univer <<<
BASHRC

echo
echo "== 4/4 git"
git config --global core.quotepath false
git config --global init.defaultBranch main
if [ -z "$(git config --global user.name)" ]; then
    echo "Git ще не знає, хто ти. Один раз виконай (своє ім'я і пошту):"
    echo '   git config --global user.name "Твоє Імʼя Прізвище"'
    echo '   git config --global user.email "твоя@пошта"'
fi

echo
echo "Готово. Відкрий нове вікно термінала (або: source ~/.bashrc). Перевірка:"
~/univer/.venv/bin/python --version
git --version
~/univer/.venv/bin/python -m pytest --version
~/univer/.venv/bin/python -m flake8 --version | head -1
~/univer/.venv/bin/python -c "import tkinter; print('tkinter (turtle) є, Tk', tkinter.TkVersion)"
