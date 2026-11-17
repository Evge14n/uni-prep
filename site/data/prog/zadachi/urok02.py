"""Урок 2. Задачі з doctest (заготовка).

Як запускати (з теки Курс):
    python3 -m doctest zadachi/urok02.py -v

Спершу всі приклади червоні: замість коду стоїть pass, і функція
повертає None. Заміни pass на свій код, щоб усі стали зелені.
Обмеження як у ЛР1: без if/elif/else, без циклів, без списків.
Функція ПОВЕРТАЄ рядок через return, а не друкує його.
Розвʼязок - у _rozvyazky/urok02.py (відкривай лише після 2 спроб).
"""
import doctest


def temperature_report(celsius: float) -> str:
    """Повертає рядок «C °C = F °F», а для морозу дописує « (мороз)».

    Формула: F = C * 9 / 5 + 32. Обидва числа - з одним знаком
    після коми. Мороз - коли температура нижче нуля (0.0 - ще ні).
    Без if: використай прийом «рядок * умова».

    :param celsius: температура в градусах Цельсія
    :return: рядок-звіт

    >>> temperature_report(0.0)
    '0.0 °C = 32.0 °F'
    >>> temperature_report(36.6)
    '36.6 °C = 97.9 °F'
    >>> temperature_report(100.0)
    '100.0 °C = 212.0 °F'
    >>> temperature_report(-40.0)
    '-40.0 °C = -40.0 °F (мороз)'
    >>> temperature_report(-0.5)
    '-0.5 °C = 31.1 °F (мороз)'
    """
    pass


def receipt(item: str, price: float, quantity: int) -> str:
    """Повертає чек з двох рядків, склеєних через символ нового рядка.

    Перший рядок: назва товару (займає щонайменше 8 знаків,
    вирівняна вліво), риска, кількість і ціна за штуку.
    Другий рядок: загальна сума. Ціни - з двома знаками після коми.
    Один return з одним f-рядком.

    :param item: назва товару
    :param price: ціна за штуку, грн
    :param quantity: кількість штук (0 або більше)
    :return: текст чека

    >>> receipt("Milk", 28.5, 2)
    'Milk    | 2 x 28.50\\nTotal: 57.00 UAH'
    >>> receipt("Tea", 45.0, 0)
    'Tea     | 0 x 45.00\\nTotal: 0.00 UAH'
    >>> receipt("Chocolate", 52.25, 3)
    'Chocolate| 3 x 52.25\\nTotal: 156.75 UAH'
    >>> print(receipt("Bread", 19.9, 1))
    Bread   | 1 x 19.90
    Total: 19.90 UAH
    """
    pass


if __name__ == "__main__":
    doctest.testmod(verbose=True)
