"""Урок 4. Задачі з doctest (заготовка).

Як запускати (з теки Курс):
    python3 -m doctest zadachi/urok04.py -v

Спершу всі приклади червоні: замість коду стоїть pass, і функція
повертає None. Заміни pass на свій код, щоб усі стали зелені.
Тут уже можна цикли for і while, if, break, continue (Лекція 4).
Розвʼязок - у _rozvyazky/urok04.py (відкривай лише після 2 спроб).
"""
import doctest


def alternating_sum(count: int) -> int:
    """Повертає знакозмінну суму 1 - 2 + 3 - 4 + ... ± count.

    Знак чергується: непарні числа додаються, парні віднімаються.
    Обмеження: без ** і без if (знак тримай в окремій змінній).

    :param count: останнє число суми (0 або більше)
    :return: значення суми; для count = 0 сума порожня, тобто 0

    >>> alternating_sum(1)
    1
    >>> alternating_sum(2)
    -1
    >>> alternating_sum(5)
    3
    >>> alternating_sum(10)
    -5
    >>> alternating_sum(0)
    0
    """
    pass


def collatz_steps(number: int) -> int:
    """Повертає кількість кроків гри «3n + 1», щоб дійти до 1.

    Крок: парне число ділимо навпіл, непарне множимо на 3 і додаємо 1.
    Для 6: 6 -> 3 -> 10 -> 5 -> 16 -> 8 -> 4 -> 2 -> 1, тобто 8 кроків.

    :param number: натуральне число (1 або більше)
    :return: кількість кроків до 1; для number = 1 це 0

    >>> collatz_steps(1)
    0
    >>> collatz_steps(2)
    1
    >>> collatz_steps(6)
    8
    >>> collatz_steps(7)
    16
    >>> collatz_steps(27)
    111
    """
    pass


if __name__ == "__main__":
    doctest.testmod(verbose=True)
