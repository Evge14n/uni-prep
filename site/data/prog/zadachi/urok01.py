"""Урок 1. Задачі з doctest (заготовка).

Як запускати (з теки Курс):
    python3 -m doctest zadachi/urok01.py -v

Спершу всі приклади червоні: замість коду стоїть pass, і функція
повертає None. Заміни pass на свій код, щоб усі стали зелені.
Обмеження як у ЛР1: без if/elif/else, без циклів, без списків.
Розвʼязок - у _rozvyazky/urok01.py (відкривай лише після 2 спроб).
"""
import doctest

SECONDS_IN_MINUTE = 60
SECONDS_IN_HOUR = 3600


def kinetic_energy(mass: float, speed: float) -> float:
    """Повертає кінетичну енергію тіла E = m * v ** 2 / 2 (у джоулях).

    :param mass: маса тіла, кг
    :param speed: швидкість тіла, м/с (знак не важить: її підносять
        до квадрата)
    :return: енергія, Дж

    >>> kinetic_energy(2.0, 3.0)
    9.0
    >>> kinetic_energy(1500.0, 20.0)
    300000.0
    >>> kinetic_energy(0.0, 10.0)
    0.0
    >>> kinetic_energy(1.0, 0.0)
    0.0
    >>> kinetic_energy(0.5, -4.0)
    4.0
    """
    pass


def trip_seconds(hours: int, minutes: int, seconds: int) -> int:
    """Переводить тривалість поїздки «години, хвилини, секунди» в секунди.

    Використай константи SECONDS_IN_HOUR і SECONDS_IN_MINUTE,
    а не числа 3600 і 60 прямо у формулі.

    :param hours: повні години (0 або більше)
    :param minutes: хвилини (від 0 до 59)
    :param seconds: секунди (від 0 до 59)
    :return: тривалість у секундах

    >>> trip_seconds(0, 0, 0)
    0
    >>> trip_seconds(1, 0, 0)
    3600
    >>> trip_seconds(0, 1, 1)
    61
    >>> trip_seconds(0, 0, 59)
    59
    >>> trip_seconds(2, 30, 15)
    9015
    """
    pass


if __name__ == "__main__":
    doctest.testmod(verbose=True)
