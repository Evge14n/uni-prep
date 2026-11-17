"""Урок 7. Задачі з doctest (заготовка).

Як запускати (з теки Курс):
    python3 -m doctest zadachi/urok07.py -v

Спершу всі приклади червоні: замість коду стоїть pass, і функція
повертає None. Заміни pass на свій код, щоб усі стали зелені.
Можна: цикли for і while, if, змінні (усе це є в лекціях 4-7).
Списки ще не потрібні - вистачить кількох змінних.
Розвʼязок - у _rozvyazky/urok07.py (відкривай лише після 2 спроб).
"""
import doctest


def sqrt2_fraction(steps: int) -> str:
    """Наближення кореня з 2 дробом p/q за системою рекурентних.

    Система (перехресна - нове p і нове q рахуються зі старих):
        p₀ = 1, q₀ = 1,
        pₖ = pₖ₋₁ + 2 * qₖ₋₁,
        qₖ = pₖ₋₁ + qₖ₋₁,   k >= 1.
    Дріб p/q з кожним кроком ближчий до √2 = 1.41421...

    :param steps: скільки кроків зробити (steps >= 0)
    :return: рядок 'p/q' після steps кроків

    >>> sqrt2_fraction(0)
    '1/1'
    >>> sqrt2_fraction(1)
    '3/2'
    >>> sqrt2_fraction(2)
    '7/5'
    >>> sqrt2_fraction(4)
    '41/29'
    >>> sqrt2_fraction(6)
    '239/169'
    """
    pass


def heron_sqrt(number: float, eps: float) -> str:
    """Корінь з number методом Герона з точністю eps.

    Послідовність: x₀ = number, xₙ = (xₙ₋₁ + number / xₙ₋₁) / 2.
    Рахуємо, поки |xₙ - xₙ₋₁| >= eps. steps - скільки разів
    порахували нове xₙ. Значення - з 6 знаками після коми.

    :param number: додатне число, з якого беремо корінь
    :param eps: точність (eps > 0)
    :return: рядок 'sqrt(number) = значення, steps = кроки'

    >>> heron_sqrt(2, 1e-6)
    'sqrt(2) = 1.414214, steps = 5'
    >>> heron_sqrt(9, 1e-6)
    'sqrt(9) = 3.000000, steps = 6'
    >>> heron_sqrt(1, 1e-6)
    'sqrt(1) = 1.000000, steps = 1'
    >>> heron_sqrt(0.25, 1e-6)
    'sqrt(0.25) = 0.500000, steps = 5'
    >>> heron_sqrt(10000, 1e-6)
    'sqrt(10000) = 100.000000, steps = 11'
    """
    pass


if __name__ == "__main__":
    doctest.testmod(verbose=True)
