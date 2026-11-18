# Урок 06. Налагодження 2 - pdb повністю, post-mortem, logging

[← Усі уроки](#/u/mint/uroky)

**Навіщо:** в уроці 05 був `breakpoint()` і п'ять команд pdb. Тут - усі налагоджувачі, які є в терміналі: pdb
повністю, налагодження **після** падіння (post-mortem), як налагоджувати doctest (ним викладач перевіряє лаби),
`logging` замість `print`, корисні прапорці `python3 -X ...` і два сторонні налагоджувачі (ipdb, pudb).
Наприкінці - 7 зламаних програм для тренування.

**Як ділити.** Захід 1: «Коротко», кроки 1-4. Захід 2: кроки 5-8 (post-mortem і doctest - найважливіше для лаб) і
тренування (крок 9). Кроки 10-12 (logging, прапорці `-X`, faulthandler, trace, importtime, cProfile, ipdb, pudb)
винесено в розділ «Далі - за бажанням» - для ЛР1-ЛР3 вони не потрібні, повернешся, коли захочеш.

## Коротко

### Чотири способи запустити pdb

| Як | Коли |
|---|---|
| `python3 -m pdb файл.py` | з першого рядка, коли не знаєш, де шукати |
| `breakpoint()` у коді | знаєш місце - зупинка саме там (урок 05) |
| `python3 -m pdb -c continue файл.py` | працює повним ходом, а при падінні зупиняється **в місці падіння** |
| `python3 -i файл.py`, далі `import pdb; pdb.pm()` | програма вже впала - зайти в місце падіння |

**Post-mortem** («після смерті») - налагодження вже впалої програми: змінні в момент падіння ще живі, їх можна
дивитись, але йти далі вже нікуди.

### Усі команди pdb, які знадобляться

| Група | Команда | Що робить |
|---|---|---|
| Рух | `n` (next) | наступний рядок, у функції не заходить |
| | `s` (step) | крок усередину функції |
| | `c` (continue) | до наступної точки зупинки |
| | `r` (return) | до кінця поточної функції (`--Return--`) |
| | `unt` / `until` | до рядка з **більшим** номером (вийти з циклу); `until 16` - до рядка 16 |
| | `j 13` (jump) | **перестрибнути** на рядок 13 без виконання того, що між ними (лише в поточній функції) |
| | Enter (порожній рядок) | повторити попередню команду |
| Де я | `l` / `ll` | код навколо / уся поточна функція |
| | `w` (where) | стек: хто кого викликав (як traceback) |
| | `u` / `d` (up / down) | піднятись до функції, що викликала, і назад |
| | `a` (args) | аргументи поточної функції |
| Дивитись | `p вираз` / `pp вираз` | показати / показати гарно (довгі списки, словники) |
| | `display вираз` | показувати щоразу при зупинці, якщо змінилось; `undisplay` - прибрати |
| | `retval` | що функція щойно повернула (після `--Return--`) |
| | `whatis вираз` | тип |
| Точки зупинки | `b 14` / `b kydok.py:14` / `b height` | на рядку / рядку в файлі / на початку функції |
| | `b 14, k == 3` | з умовою: зупинитись, лише коли умова істинна |
| | `b` | список усіх точок |
| | `tbreak 22` | тимчасова: спрацює один раз і зникне |
| | `cl 1` / `cl` | прибрати точку 1 / всі (питає `Clear all breaks?`) |
| | `disable 1` / `enable 1` | вимкнути / ввімкнути, не прибираючи |
| | `condition 1 k > 2` | змінити умову; `condition 1` без умови - прибрати умову |
| | `ignore 1 2` | пропустити наступні 2 проходи через точку 1 |
| | `commands 1` | команди, які виконаються самі на точці 1 (до `end` або до `c`) |
| Змінити | `!вираз` | виконати рядок Python (`!h = 0`); для глобальної: `!global G; G = 1.62` |
| | `interact` | повний Python `>>>` з усіма змінними; назад у pdb - Ctrl+D |
| Інше | `restart` / `run` | запустити програму заново (точки зупинки лишаються) |
| | `h` / `h команда` | список команд / довідка про команду |
| | `q` | вийти |

### doctest, logging, прапорці, сторонні налагоджувачі

| Задача | Інструмент |
|---|---|
| Побачити кожен приклад doctest | лаба викладача: `python3 лаба.py -v` або `perevir лаба.py ...` (урок 03) |
| Зупинитись на першій помилці doctest | `doctest.testmod(optionflags=doctest.FAIL_FAST)` у своєму файлі |
| Подивитись змінні всередині функції під час doctest | `breakpoint()` у функції + `python3 лаба.py` (ввід - руками) |
| doctest впав з винятком (Traceback) | `python3 -m pytest --doctest-modules --pdb лаба.py` |
| Програма зависла | Ctrl+C (traceback показує рядок) |
| *За бажанням (кроки 10-12):* слідкувати за довгою програмою | `logging` (рівні DEBUG, INFO, WARNING, ERROR) |
| *За бажанням:* знайти приховані проблеми | `python3 -X dev`, `python3 -W error` |
| *За бажанням:* зависла, а Ctrl+C не допомагає | `faulthandler.dump_traceback_later` |
| *За бажанням:* «впала» без traceback (Segmentation fault) | `python3 -X faulthandler` |
| *За бажанням:* що повільне | `python3 -m cProfile -s cumtime`, `python3 -m timeit`, `python3 -X importtime` |
| *За бажанням:* кожен виконаний рядок | `python3 -m trace --trace` |
| *За бажанням:* зручніший pdb | `ipdb` (кольори, Tab), `pudb` (на весь екран) - ставляться у venv |

`python3 -m doctest -v файл.py` і `python3 -m doctest -o FAIL_FAST файл.py` - **лише для файлів, де `testmod()`
стоїть під `if __name__ == "__main__":`** (або його нема зовсім), як у прикладах цього уроку. На лабах викладача,
де `doctest.testmod()` просто внизу файлу і є `input()`, ця команда дає чужий провал `DebugRunner` і питає ввід
(урок 04, «Типові помилки» п. 10) - там `python3 лаба.py -v` або `perevir`.

## Передбач, потім запусти

Відповіді - справжній вивід з кроків «Руками» нижче (номер кроку в дужках).

1. У функції є змінна `h` (висота). Ти зупинився в pdb і набрав просто `h`, Enter. Що покаже pdb?

<details markdown="1"><summary>Відповідь</summary>

**Довідку**, а не висоту: `h` - це команда help (крок 6). Змінну з іменем команди треба писати через `p h`, а
змінювати через `!h = 0`. Те саме з `c`, `n`, `s`, `l`, `a`, `b`, `j`, `r`, `w`, `u`, `d`, `q`. Ще одна причина
давати змінним довгі імена, як вимагає викладач (`height_m`, а не `h`).
</details>

2. Програма зупинена в `table()`. Набираєш `!G = 1.62` (як на Місяці), потім `p G`. Далі `u` (вгору, у `main`) і
   знову `p G`. Що буде?

<details markdown="1"><summary>Відповідь</summary>

У `table()` - `1.62`, у `main` - `9.81` (крок 5). `!G = 1.62` створив **нову локальну** змінну `G` всередині
`table`, а глобальна `G`, якою користується `height()`, не змінилась. Щоб змінити глобальну:
`!global G; G = 1.62`.
</details>

3. `python3 -m pdb -c continue vymiry.py`, програма падає, ти дивишся змінні і набираєш `q`. Ти вийшов з pdb?

<details markdown="1"><summary>Відповідь</summary>

Ні. pdb пише `Post mortem debugger finished. ... will be restarted` і запускає програму **знову** з першого рядка
(крок 7). Треба ще раз `q`.
</details>

4. У `logging.basicConfig` рівень `DEBUG` змінили на `WARNING`. Які рядки логу лишаться?

<details markdown="1"><summary>Відповідь</summary>

Лише `WARNING` і серйозніші (`ERROR`, `CRITICAL`). Рядки `DEBUG` і `INFO` зникнуть, а сам код міняти не треба
(крок 10, за бажанням).
</details>

## Руками

### Крок 1. `python3 -m pdb` з першого рядка

```bash
mkdir -p ~/univer/praktyka/nalag2
cd ~/univer/praktyka/nalag2
nano kydok.py
```

> **Нове тут:**
>
> - `mkdir` - створює нову теку. Назва: make directory - «зробити теку». `-p` - створює і всі проміжні теки шляху; якщо тека вже є - мовчить, без помилки.
> - `cd` - переходить в іншу теку. Назва: change directory - «змінити теку».
> - `nano` - простий редактор файлів у терміналі. Назва: nano - жарт з одиницями: наступник редактора pico (піко < нано).
> - `~` - домашня тека /home/evgen. Назва: tilde («тильда») - домашня тека.
>
> Усе про кожну команду - у довіднику «05_Програмування/КОМАНДИ - довідник.md» (на сайті - вкладка «Команди»).

Тіло кинули вгору зі швидкістю 10 м/с, рахуємо висоту `h = v0·t - g·t²/2` кожні 0.5 с. Набери (номери рядків
важливі для точок зупинки, тому порожні рядки теж):

```python
"""Тіло кинули вертикально вгору: таблиця висот."""
G = 9.81


def height(v0, t):
    h = v0 * t - G * t ** 2 / 2
    return round(h, 3)


def table(v0, dt, steps):
    rows = []
    for k in range(steps):
        t = k * dt
        h = height(v0, t)
        rows.append((t, h))
    return rows


def main():
    rows = table(10, 0.5, 5)
    for t, h in rows:
        print(f"t = {t:.1f} с   h = {h:6.3f} м")
    print("готово")


main()
```

(Короткі імена `v0`, `t`, `h` тут як у формулі; у лабі викладач хоче довші.) Спершу просто запусти:

```bash
python3 kydok.py
```

```text
t = 0.0 с   h =  0.000 м
t = 0.5 с   h =  3.774 м
t = 1.0 с   h =  5.095 м
t = 1.5 с   h =  3.964 м
t = 2.0 с   h =  0.380 м
готово
```

> **Нове тут:**
>
> - `python3` - запускає Python: файл, рядок коду або модуль. Назва: Python - на честь комедійного шоу «Monty Python», 3 - третя версія мови.

Тепер під pdb:

```bash
python3 -m pdb kydok.py
```

```text
> /home/evgen/univer/praktyka/nalag2/kydok.py(1)<module>()
-> """Тіло кинули вертикально вгору: таблиця висот."""
(Pdb) l
  1  -> """Тіло кинули вертикально вгору: таблиця висот."""
  2     G = 9.81
  3
  4
  5     def height(v0, t):
  6         h = v0 * t - G * t ** 2 / 2
  7         return round(h, 3)
  8
  9
 10     def table(v0, dt, steps):
 11         rows = []
(Pdb) b 14
Breakpoint 1 at /home/evgen/univer/praktyka/nalag2/kydok.py:14
(Pdb) c
> /home/evgen/univer/praktyka/nalag2/kydok.py(14)table()
-> h = height(v0, t)
(Pdb) p k, t
(0, 0.0)
(Pdb) s
--Call--
> /home/evgen/univer/praktyka/nalag2/kydok.py(5)height()
-> def height(v0, t):
(Pdb) a
v0 = 10
t = 0.0
(Pdb) w
  /usr/lib/python3.12/bdb.py(600)run()
-> exec(cmd, globals, locals)
  <string>(1)<module>()
  /home/evgen/univer/praktyka/nalag2/kydok.py(26)<module>()
-> main()
  /home/evgen/univer/praktyka/nalag2/kydok.py(20)main()
-> rows = table(10, 0.5, 5)
  /home/evgen/univer/praktyka/nalag2/kydok.py(14)table()
-> h = height(v0, t)
> /home/evgen/univer/praktyka/nalag2/kydok.py(5)height()
-> def height(v0, t):
(Pdb) u
> /home/evgen/univer/praktyka/nalag2/kydok.py(14)table()
-> h = height(v0, t)
(Pdb) p k, rows
(0, [])
(Pdb) d
> /home/evgen/univer/praktyka/nalag2/kydok.py(5)height()
-> def height(v0, t):
(Pdb) r
--Return--
> /home/evgen/univer/praktyka/nalag2/kydok.py(7)height()->0.0
-> return round(h, 3)
(Pdb) n
> /home/evgen/univer/praktyka/nalag2/kydok.py(15)table()
-> rows.append((t, h))
(Pdb) c
> /home/evgen/univer/praktyka/nalag2/kydok.py(14)table()
-> h = height(v0, t)
(Pdb) p k
1
(Pdb) ll
 10     def table(v0, dt, steps):
 11         rows = []
 12         for k in range(steps):
 13             t = k * dt
 14 B->         h = height(v0, t)
 15             rows.append((t, h))
 16         return rows
(Pdb) cl
Clear all breaks? y
Deleted breakpoint 1 at /home/evgen/univer/praktyka/nalag2/kydok.py:14
(Pdb) c
t = 0.0 с   h =  0.000 м
t = 0.5 с   h =  3.774 м
t = 1.0 с   h =  5.095 м
t = 1.5 с   h =  3.964 м
t = 2.0 с   h =  0.380 м
готово
The program finished and will be restarted
> /home/evgen/univer/praktyka/nalag2/kydok.py(1)<module>()
-> """Тіло кинули вертикально вгору: таблиця висот."""
(Pdb) q
```

> **Нове тут:**
>
> - `python3`: `-m` - запусти модуль як програму: python3 -m pytest, python3 -m venv, python3 -m pdb.
> - `python3 -m pdb` - запускає програму покроково в налагоджувачі pdb. Назва: Python debugger - «налагоджувач Python» (debug - «виловити жуків», помилки).

Розбір:
- `w` показує стек знизу вгору як traceback, тільки «живий»: `>` - де ми зараз. Два верхні рядки (`bdb.py`,
  `<string>`) - це сам pdb, їх пропускай.
- `u` піднявся в `table()`: там видно `k` і `rows`, яких нема в `height()`. `d` повернув назад.
- `r` доїхав до кінця `height()`: `->0.0` - що вона повертає.
- У `ll` буква `B` - точка зупинки, `->` - поточний рядок.
- Коли програма закінчилась, pdb пише `The program finished and will be restarted` і починає знову.
  Вийти - `q`.

Порожній рядок (просто Enter) повторює попередню команду, зручно для багатьох `n` підряд:

```bash
python3 -m pdb kydok.py
```

```text
> /home/evgen/univer/praktyka/nalag2/kydok.py(1)<module>()
-> """Тіло кинули вертикально вгору: таблиця висот."""
(Pdb) b 13
Breakpoint 1 at /home/evgen/univer/praktyka/nalag2/kydok.py:13
(Pdb) c
> /home/evgen/univer/praktyka/nalag2/kydok.py(13)table()
-> t = k * dt
(Pdb) n
> /home/evgen/univer/praktyka/nalag2/kydok.py(14)table()
-> h = height(v0, t)
(Pdb)
> /home/evgen/univer/praktyka/nalag2/kydok.py(15)table()
-> rows.append((t, h))
(Pdb) p t
0.0
(Pdb) q
```

### Крок 2. Точки зупинки: на функції, з умовою, тимчасові

```bash
python3 -m pdb kydok.py
```

```text
> /home/evgen/univer/praktyka/nalag2/kydok.py(1)<module>()
-> """Тіло кинули вертикально вгору: таблиця висот."""
(Pdb) b height
Breakpoint 1 at /home/evgen/univer/praktyka/nalag2/kydok.py:5
(Pdb) b 14, k == 3
Breakpoint 2 at /home/evgen/univer/praktyka/nalag2/kydok.py:14
(Pdb) tbreak 22
Breakpoint 3 at /home/evgen/univer/praktyka/nalag2/kydok.py:22
(Pdb) b
Num Type         Disp Enb   Where
1   breakpoint   keep yes   at /home/evgen/univer/praktyka/nalag2/kydok.py:5
2   breakpoint   keep yes   at /home/evgen/univer/praktyka/nalag2/kydok.py:14
        stop only if k == 3
3   breakpoint   del  yes   at /home/evgen/univer/praktyka/nalag2/kydok.py:22
(Pdb) disable 1
Disabled breakpoint 1 at /home/evgen/univer/praktyka/nalag2/kydok.py:5
(Pdb) c
> /home/evgen/univer/praktyka/nalag2/kydok.py(14)table()
-> h = height(v0, t)
(Pdb) p k, t
(3, 1.5)
(Pdb) enable 1
Enabled breakpoint 1 at /home/evgen/univer/praktyka/nalag2/kydok.py:5
(Pdb) c
> /home/evgen/univer/praktyka/nalag2/kydok.py(6)height()
-> h = v0 * t - G * t ** 2 / 2
(Pdb) a
v0 = 10
t = 1.5
(Pdb) cl 1
Deleted breakpoint 1 at /home/evgen/univer/praktyka/nalag2/kydok.py:5
(Pdb) c
Deleted breakpoint 3 at /home/evgen/univer/praktyka/nalag2/kydok.py:22
> /home/evgen/univer/praktyka/nalag2/kydok.py(22)main()
-> print(f"t = {t:.1f} с   h = {h:6.3f} м")
(Pdb) p t, h
(0.0, 0.0)
(Pdb) c
t = 0.0 с   h =  0.000 м
t = 0.5 с   h =  3.774 м
t = 1.0 с   h =  5.095 м
t = 1.5 с   h =  3.964 м
t = 2.0 с   h =  0.380 м
готово
The program finished and will be restarted
> /home/evgen/univer/praktyka/nalag2/kydok.py(1)<module>()
-> """Тіло кинули вертикально вгору: таблиця висот."""
(Pdb) q
```

- `b 14, k == 3` пропустила `k = 0, 1, 2` і зупинилась одразу на `k = 3`. Це головний інструмент для циклів:
  не тиснути `c` 100 разів, а одразу зупинитись на потрібному оберті.
- У списку `b`: `Disp del` - тимчасова (зникне), `Enb yes` - увімкнена.
- `cl 1` (з номером) прибирає без питань, `cl` (усі) питає `Clear all breaks?`.
- `tbreak 22` спрацювала один раз: `Deleted breakpoint 3` - і зникла.

Умову можна поміняти потім, а `whatis` каже тип:

```text
> /home/evgen/univer/praktyka/nalag2/kydok.py(1)<module>()
-> """Тіло кинули вертикально вгору: таблиця висот."""
(Pdb) b kydok.py:14
Breakpoint 1 at /home/evgen/univer/praktyka/nalag2/kydok.py:14
(Pdb) condition 1 k > 2
New condition set for breakpoint 1.
(Pdb) c
> /home/evgen/univer/praktyka/nalag2/kydok.py(14)table()
-> h = height(v0, t)
(Pdb) p k
3
(Pdb) condition 1
Breakpoint 1 is now unconditional.
(Pdb) c
> /home/evgen/univer/praktyka/nalag2/kydok.py(14)table()
-> h = height(v0, t)
(Pdb) p k
4
(Pdb) whatis k
<class 'int'>
(Pdb) h until
      Usage: unt(il) [lineno]

      Without argument, continue execution until the line with a
      number greater than the current one is reached.  With a line
      number, continue execution until a line with a number greater
      or equal to that is reached.  In both cases, also stop when
      the current frame returns.
(Pdb) q
```

### Крок 3. `commands` - точка зупинки, яка сама друкує і їде далі

```text
> /home/evgen/univer/praktyka/nalag2/kydok.py(1)<module>()
-> """Тіло кинули вертикально вгору: таблиця висот."""
(Pdb) b 15
Breakpoint 1 at /home/evgen/univer/praktyka/nalag2/kydok.py:15
(Pdb) commands 1
(com) silent
(com) p k, t, h
(com) c
(Pdb) c
(0, 0.0, 0.0)
(1, 0.5, 3.774)
(2, 1.0, 5.095)
(3, 1.5, 3.964)
(4, 2.0, 0.38)
t = 0.0 с   h =  0.000 м
t = 0.5 с   h =  3.774 м
t = 1.0 с   h =  5.095 м
t = 1.5 с   h =  3.964 м
t = 2.0 с   h =  0.380 м
готово
The program finished and will be restarted
> /home/evgen/univer/praktyka/nalag2/kydok.py(1)<module>()
-> """Тіло кинули вертикально вгору: таблиця висот."""
(Pdb) q
```

Це «print без правки файлу». `silent` - не друкувати рядок `> ...kydok.py(15)` при кожній зупинці. Запрошення
`(com)` - ти вводиш список команд. **`c` у списку одразу закінчує список** (pdb 3.12 так і робить, у
документації: будь-яка команда, що продовжує виконання, завершує список). Якщо після `c` набрати ще й `end`,
отримаєш `*** NameError: name 'end' is not defined`. Список без `c` закінчуй словом `end`.

### Крок 4. `ignore`, `display`, `until`, `retval`

```text
> /home/evgen/univer/praktyka/nalag2/kydok.py(1)<module>()
-> """Тіло кинули вертикально вгору: таблиця висот."""
(Pdb) b 14
Breakpoint 1 at /home/evgen/univer/praktyka/nalag2/kydok.py:14
(Pdb) ignore 1 2
Will ignore next 2 crossings of breakpoint 1.
(Pdb) c
> /home/evgen/univer/praktyka/nalag2/kydok.py(14)table()
-> h = height(v0, t)
(Pdb) p k
2
(Pdb) display t
display t: 1.0
(Pdb) display h
display h: 3.774
(Pdb) n
> /home/evgen/univer/praktyka/nalag2/kydok.py(15)table()
-> rows.append((t, h))
display h: 5.095  [old: 3.774]
(Pdb) cl 1
Deleted breakpoint 1 at /home/evgen/univer/praktyka/nalag2/kydok.py:14
(Pdb) until
> /home/evgen/univer/praktyka/nalag2/kydok.py(16)table()
-> return rows
display t: 2.0  [old: 1.0]
display h: 0.38  [old: 5.095]
(Pdb) undisplay
(Pdb) n
--Return--
> /home/evgen/univer/praktyka/nalag2/kydok.py(16)table()->[(0.0, 0.0), (0.5, 3.774), (1.0, 5.095), (1.5, 3.964), (2.0, 0.38)]
-> return rows
(Pdb) retval
[(0.0, 0.0), (0.5, 3.774), (1.0, 5.095), (1.5, 3.964), (2.0, 0.38)]
(Pdb) n
> /home/evgen/univer/praktyka/nalag2/kydok.py(21)main()
-> for t, h in rows:
(Pdb) q
```

- `ignore 1 2` - перші два проходи пропущено, зупинка при `k = 2`.
- `display` друкує вираз лише тоді, коли він **змінився**, і показує старе значення `[old: ...]`. Значення `h`
  тут - з попереднього оберту, бо рядок 14 ще не виконався.
- `until` на останньому рядку циклу (15) прокрутив **увесь цикл** і зупинився на рядку 16. Важливо: спершу прибрали
  точку на рядку 14 (`cl 1`), інакше `until` зупинився б на ній на наступному оберті.
- `retval` - значення, яке функція повертає (тут уся таблиця).

### Крок 5. Змінити значення і перестрибнути: `!`, `global`, `j`, `pp`

Спершу пастка з «Передбач» 2:

```text
> /home/evgen/univer/praktyka/nalag2/kydok.py(1)<module>()
-> """Тіло кинули вертикально вгору: таблиця висот."""
(Pdb) b 15, k == 2
Breakpoint 1 at /home/evgen/univer/praktyka/nalag2/kydok.py:15
(Pdb) c
> /home/evgen/univer/praktyka/nalag2/kydok.py(15)table()
-> rows.append((t, h))
(Pdb) !G = 1.62
(Pdb) p G
1.62
(Pdb) u
> /home/evgen/univer/praktyka/nalag2/kydok.py(20)main()
-> rows = table(10, 0.5, 5)
(Pdb) p G
9.81
(Pdb) q
```

Правильно - з `global`, а потім `j 14` (стрибок назад на рядок 14), щоб перерахувати висоту вже «на Місяці»:

```text
> /home/evgen/univer/praktyka/nalag2/kydok.py(1)<module>()
-> """Тіло кинули вертикально вгору: таблиця висот."""
(Pdb) b 15, k == 2
Breakpoint 1 at /home/evgen/univer/praktyka/nalag2/kydok.py:15
(Pdb) c
> /home/evgen/univer/praktyka/nalag2/kydok.py(15)table()
-> rows.append((t, h))
(Pdb) pp rows
[(0.0, 0.0), (0.5, 3.774)]
(Pdb) p t, h
(1.0, 5.095)
(Pdb) !global G; G = 1.62
(Pdb) j 14
> /home/evgen/univer/praktyka/nalag2/kydok.py(14)table()
-> h = height(v0, t)
(Pdb) n
> /home/evgen/univer/praktyka/nalag2/kydok.py(15)table()
-> rows.append((t, h))
(Pdb) p h
9.19
(Pdb) cl 1
Deleted breakpoint 1 at /home/evgen/univer/praktyka/nalag2/kydok.py:15
(Pdb) b 23
Breakpoint 2 at /home/evgen/univer/praktyka/nalag2/kydok.py:23
(Pdb) c
t = 0.0 с   h =  0.000 м
t = 0.5 с   h =  3.774 м
t = 1.0 с   h =  9.190 м
t = 1.5 с   h = 13.178 м
t = 2.0 с   h = 16.760 м
> /home/evgen/univer/praktyka/nalag2/kydok.py(23)main()
-> print("готово")
(Pdb) j 22
*** Jump failed: can't jump into the body of a for loop
(Pdb) q
```

Перевір числа: `10·1 - 1.62·1²/2 = 9.19`. З `t = 1.0 с` усі висоти пораховано вже з `G = 1.62`. Це спосіб
перевірити гіпотезу «а що, якби тут було інше значення» без правки файлу. `j` не вміє стрибати всередину циклу
`for` - pdb пише `Jump failed`.

### Крок 6. `h`-пастка, `interact`, `restart`

```text
> /home/evgen/univer/praktyka/nalag2/kydok.py(1)<module>()
-> """Тіло кинули вертикально вгору: таблиця висот."""
(Pdb) b 15
Breakpoint 1 at /home/evgen/univer/praktyka/nalag2/kydok.py:15
(Pdb) c
> /home/evgen/univer/praktyka/nalag2/kydok.py(15)table()
-> rows.append((t, h))
(Pdb) h

Documented commands (type help <topic>):
========================================
EOF    c          d        h         list      q        rv       undisplay
a      cl         debug    help      ll        quit     s        unt
alias  clear      disable  ignore    longlist  r        source   until
args   commands   display  interact  n         restart  step     up
b      condition  down     j         next      return   tbreak   w
break  cont       enable   jump      p         retval   u        whatis
bt     continue   exit     l         pp        run      unalias  where

Miscellaneous help topics:
==========================
exec  pdb

(Pdb) p h
0.0
(Pdb) !h = 0
(Pdb) n
> /home/evgen/univer/praktyka/nalag2/kydok.py(12)table()
-> for k in range(steps):
(Pdb) p rows
[(0.0, 0)]
(Pdb) interact
*interactive*
>>> len(rows)
1
>>> rows[-1]
(0.0, 0)
>>>
now exiting InteractiveConsole...
(Pdb) restart
Restarting /home/evgen/univer/praktyka/nalag2/kydok.py with arguments:

> /home/evgen/univer/praktyka/nalag2/kydok.py(1)<module>()
-> """Тіло кинули вертикально вгору: таблиця висот."""
(Pdb) q
```

- `h` показав довідку, а не змінну. `p h` - значення, `!h = 0` - змінити (в `rows` потрапило ціле `0`).
- `interact` відкрив `>>>`, де можна писати багаторядковий код. Порожній `>>>` у виводі - це натиснуто Ctrl+D,
  повернення в `(Pdb)`.
- `restart` запустив програму заново з першого рядка (`run` - те саме).

### Крок 7. Post-mortem: три способи

Файл `vymiry.py` - середні значення серій вимірювань, одна серія порожня:

```python
def mean(values):
    return sum(values) / len(values)


def analyze(series):
    result = {}
    for name, values in series.items():
        result[name] = mean(values)
    return result


data = {"t1": [2.01, 1.99, 2.02], "t2": [1.42, 1.40], "t3": []}
print(analyze(data))
```

**Спосіб 1:** `-c continue` - pdb не зупиняється на початку, а лише в місці падіння:

```bash
python3 -m pdb -c continue vymiry.py
```

```text
Traceback (most recent call last):
  File "/usr/lib/python3.12/pdb.py", line 1944, in main
    pdb._run(target)
  File "/usr/lib/python3.12/pdb.py", line 1738, in _run
    self.run(target.code)
  File "/usr/lib/python3.12/bdb.py", line 600, in run
    exec(cmd, globals, locals)
  File "<string>", line 1, in <module>
  File "/home/evgen/univer/praktyka/nalag2/vymiry.py", line 13, in <module>
    print(analyze(data))
          ^^^^^^^^^^^^^
  File "/home/evgen/univer/praktyka/nalag2/vymiry.py", line 8, in analyze
    result[name] = mean(values)
                   ^^^^^^^^^^^^
  File "/home/evgen/univer/praktyka/nalag2/vymiry.py", line 2, in mean
    return sum(values) / len(values)
           ~~~~~~~~~~~~^~~~~~~~~~~~~
ZeroDivisionError: division by zero
Uncaught exception. Entering post mortem debugging
Running 'cont' or 'step' will restart the program
> /home/evgen/univer/praktyka/nalag2/vymiry.py(2)mean()
-> return sum(values) / len(values)
(Pdb) p values
[]
(Pdb) u
> /home/evgen/univer/praktyka/nalag2/vymiry.py(8)analyze()
-> result[name] = mean(values)
(Pdb) p name, result
('t3', {'t1': 2.0066666666666664, 't2': 1.41})
(Pdb) q
Post mortem debugger finished. The /home/evgen/univer/praktyka/nalag2/vymiry.py will be restarted
> /home/evgen/univer/praktyka/nalag2/vymiry.py(1)<module>()
-> def mean(values):
(Pdb) q
```

> **Нове тут:**
>
> - `python3 -m pdb`: `-c` - виконати команду pdb одразу після старту; -c continue - їхати до падіння і зупинитись там.

`values` порожній, `u` показав, яка серія винна: `'t3'`. Зверху в traceback - рядки самого pdb (`pdb.py`,
`bdb.py`), пропускай їх. Після першого `q` програма **перезапускається**, тому `q` двічі.

**Спосіб 2:** програма вже впала в `python3 -i` - `pdb.pm()` (post mortem):

```bash
python3 -i vymiry.py
```

```text
Traceback (most recent call last):
  File "/home/evgen/univer/praktyka/nalag2/vymiry.py", line 13, in <module>
    print(analyze(data))
          ^^^^^^^^^^^^^
  File "/home/evgen/univer/praktyka/nalag2/vymiry.py", line 8, in analyze
    result[name] = mean(values)
                   ^^^^^^^^^^^^
  File "/home/evgen/univer/praktyka/nalag2/vymiry.py", line 2, in mean
    return sum(values) / len(values)
           ~~~~~~~~~~~~^~~~~~~~~~~~~
ZeroDivisionError: division by zero
>>> import pdb; pdb.pm()
> /home/evgen/univer/praktyka/nalag2/vymiry.py(2)mean()
-> return sum(values) / len(values)
(Pdb) p values
[]
(Pdb) u
> /home/evgen/univer/praktyka/nalag2/vymiry.py(8)analyze()
-> result[name] = mean(values)
(Pdb) p name
't3'
(Pdb) q
>>>
```

> **Нове тут:**
>
> - `python3`: `-i` - спершу виконати файл, а потім лишитись у Python з >>> і всіма його функціями.

Тут `q` повертає в `>>>` (останній порожній `>>>` - вихід Ctrl+D).

**Спосіб 3:** `pdb.post_mortem()` у самому коді - коли падіння ловить `try/except`. Заміни останній рядок
`vymiry.py` на:

```python
try:
    print(analyze(data))
except ZeroDivisionError:
    import pdb

    pdb.post_mortem()
```

Збережи як `vymiry_pm.py` (у nano: Ctrl+O, нове ім'я, Enter, на питання про інше ім'я - Y):

```bash
python3 vymiry_pm.py
```

```text
> /home/evgen/univer/praktyka/nalag2/vymiry_pm.py(2)mean()
-> return sum(values) / len(values)
(Pdb) p values
[]
(Pdb) w
  /home/evgen/univer/praktyka/nalag2/vymiry_pm.py(14)<module>()
-> print(analyze(data))
  /home/evgen/univer/praktyka/nalag2/vymiry_pm.py(8)analyze()
-> result[name] = mean(values)
> /home/evgen/univer/praktyka/nalag2/vymiry_pm.py(2)mean()
-> return sum(values) / len(values)
(Pdb) q
```

### Крок 8. Налагодження doctest

Викладач перевіряє лаби doctest-ами, і **їх не можна міняти**. Налагоджуємо функцію, а не тест. Приклад - не лаба,
схожа задача (`lab_demo.py`):

```python
"""Приклад для налагодження doctest (це не лаба)."""
import math


def period(length: float) -> str:
    """Період математичного маятника.

    >>> period(1.0)
    'T = 2.006 с'
    >>> period(0.25)
    'T = 1.003 с'
    """
    g = 9.81
    t = 2 * math.pi * math.sqrt(length / g)
    return f"T = {t:.2f} с"


if __name__ == "__main__":
    import doctest

    doctest.testmod()
```

```bash
python3 lab_demo.py
```

```text
**********************************************************************
File "/home/evgen/univer/praktyka/nalag2/lab_demo.py", line 8, in __main__.period
Failed example:
    period(1.0)
Expected:
    'T = 2.006 с'
Got:
    'T = 2.01 с'
**********************************************************************
File "/home/evgen/univer/praktyka/nalag2/lab_demo.py", line 10, in __main__.period
Failed example:
    period(0.25)
Expected:
    'T = 1.003 с'
Got:
    'T = 1.00 с'
**********************************************************************
1 items had failures:
   2 of   2 in __main__.period
***Test Failed*** 2 failures.
```

`Expected` - що чекав тест, `Got` - що повернула функція. Порівнюй посимвольно: тут різниця в кількості знаків
після коми. Якщо все пройшло, `python3 lab_demo.py` **нічого не друкує**. Щоб бачити кожен приклад - `-v`
(`testmod()` сам бачить `-v` у команді):

```bash
python3 lab_demo.py -v
```

```text
Trying:
    period(1.0)
Expecting:
    'T = 2.006 с'
**********************************************************************
File "/home/evgen/univer/praktyka/nalag2/lab_demo.py", line 8, in __main__.period
Failed example:
    period(1.0)
Expected:
    'T = 2.006 с'
Got:
    'T = 2.01 с'
Trying:
    period(0.25)
Expecting:
    'T = 1.003 с'
**********************************************************************
File "/home/evgen/univer/praktyka/nalag2/lab_demo.py", line 10, in __main__.period
Failed example:
    period(0.25)
Expected:
    'T = 1.003 с'
Got:
    'T = 1.00 с'
1 items had no tests:
    __main__
**********************************************************************
1 items had failures:
   2 of   2 in __main__.period
2 tests in 2 items.
0 passed and 2 failed.
***Test Failed*** 2 failures.
```

Багато прикладів падають - почни з першого: прапорець `FAIL_FAST` (зупинитись на першій помилці). Через
`python3 -m doctest` (тоді рядок `doctest.testmod()` у файлі не потрібен). Тут так можна, бо в `lab_demo.py`
`testmod()` стоїть під `if __name__ == "__main__":`; на лабі викладача з `testmod()` унизу і `input()` - ні
(див. «Коротко»):

```bash
python3 -m doctest -o FAIL_FAST lab_demo.py
```

```text
**********************************************************************
File "/home/evgen/univer/praktyka/nalag2/lab_demo.py", line 8, in lab_demo.period
Failed example:
    period(1.0)
Expected:
    'T = 2.006 с'
Got:
    'T = 2.01 с'
**********************************************************************
1 items had failures:
   1 of   1 in lab_demo.period
***Test Failed*** 1 failures.
```

> **Нове тут:**
>
> - `python3 -m doctest` - перевіряє приклади >>> з опису функцій. Назва: doc test - «тест у документації»: приклади >>> в описі функції. `-o` - увімкнути опцію doctest, напр. -o FAIL_FAST - зупинитись на першому провалі.

У коді це `doctest.testmod(optionflags=doctest.FAIL_FAST)`. Інші прапорці: `doctest.ELLIPSIS` (`...` в очікуваному
означає «будь-що»), `doctest.NORMALIZE_WHITESPACE` (не зважати на кількість пробілів). Прапорці - лише для **свого**
налагодження: doctest викладача не змінюй.

**Подивитись змінні всередині функції під час doctest:** додай `breakpoint()` перед `return` (збережи як
`lab_bp.py`). doctest уміє працювати з pdb:

```bash
python3 lab_bp.py
```

```text
> /home/evgen/univer/praktyka/nalag2/lab_bp.py(16)period()
-> return f"T = {t:.2f} с"
(Pdb) p t
2.0060666807106475
(Pdb) c
**********************************************************************
File "/home/evgen/univer/praktyka/nalag2/lab_bp.py", line 8, in __main__.period
Failed example:
    period(1.0)
Expected:
    'T = 2.006 с'
Got:
    'T = 2.01 с'
> /home/evgen/univer/praktyka/nalag2/lab_bp.py(16)period()
-> return f"T = {t:.2f} с"
(Pdb) p t
1.0030333403553238
(Pdb) c
**********************************************************************
File "/home/evgen/univer/praktyka/nalag2/lab_bp.py", line 10, in __main__.period
Failed example:
    period(0.25)
Expected:
    'T = 1.003 с'
Got:
    'T = 1.00 с'
**********************************************************************
1 items had failures:
   2 of   2 in __main__.period
***Test Failed*** 2 failures.
```

`t = 2.0060666...` - число правильне, неправильний лише формат `:.2f` (треба `:.3f`). Під `pytest` (і в
`perevir`) `breakpoint()` у doctest не працює без ключа `-s`, pytest пише:

```text
OSError: pytest: reading from stdin while output is captured!  Consider using `-s`.
```

**`doctest.debug`** - пройти приклади з docstring кроками pdb. Він перетворює приклади на маленький скрипт
(`<string>`), тому перші кроки - всередині цього скрипту:

```bash
python3 -c 'import doctest, lab_demo; doctest.debug(lab_demo, "lab_demo.period")'
```

```text
> <string>(1)<module>()
(Pdb) s
--Call--
> <string>(0)<module>()
(Pdb) s
> <string>(3)<module>()
(Pdb) s
--Call--
> /home/evgen/univer/praktyka/nalag2/lab_demo.py(5)period()
-> def period(length: float) -> str:
(Pdb) s
> /home/evgen/univer/praktyka/nalag2/lab_demo.py(13)period()
-> g = 9.81
(Pdb) s
> /home/evgen/univer/praktyka/nalag2/lab_demo.py(14)period()
-> t = 2 * math.pi * math.sqrt(length / g)
(Pdb) l
  9         'T = 2.006 с'
 10         >>> period(0.25)
 11         'T = 1.003 с'
 12         """
 13         g = 9.81
 14  ->     t = 2 * math.pi * math.sqrt(length / g)
 15         return f"T = {t:.2f} с"
 16
 17
 18     if __name__ == "__main__":
 19         import doctest
(Pdb) q
```

> **Нове тут:**
>
> - `python3`: `-c` - виконати рядок коду з командного рядка, без файлу: python3 -c 'print(2 ** 10)'.
> - `"..."` - текст з пробілами одним словом, $ підставляється. Назва: подвійні лапки - «усе це одне слово, але $ працює».
> - `'...'` - текст буквально, нічого не підставляється. Назва: одинарні лапки - «буквально, як написано».

**pytest з `--pdb`** зупиняється в місці падіння, але корисний, лише коли doctest впав з **винятком** (Traceback).
Зроби копію `lab_exc.py`, де формат уже `:.3f`, а в другому прикладі навмисно рядок: `>>> period("0.25")`.
pytest стоїть у venv (урок 03), тож спершу `source ~/univer/.venv/bin/activate`:

```bash
python3 -m pytest --doctest-modules --pdb -q lab_exc.py
```

```text
F
>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> traceback >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
006 Період математичного маятника.
007
008     >>> period(1.0)
009     'T = 2.006 с'
010     >>> period("0.25")
UNEXPECTED EXCEPTION: TypeError("unsupported operand type(s) for /: 'str' and 'float'")
Traceback (most recent call last):
  File "/usr/lib/python3.12/doctest.py", line 1361, in __run
    exec(compile(example.source, filename, "single",
  File "<doctest lab_exc.period[1]>", line 1, in <module>
  File "/home/evgen/univer/praktyka/nalag2/lab_exc.py", line 14, in period
    t = 2 * math.pi * math.sqrt(length / g)
                                ~~~~~~~^~~
TypeError: unsupported operand type(s) for /: 'str' and 'float'
/home/evgen/univer/praktyka/nalag2/lab_exc.py:10: UnexpectedException
>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> entering PDB >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

>>>>>>>>>>>>>>>>>>>>>>>>>>>> PDB post_mortem (IO-capturing turned off) >>>>>>>>>>>>>>>>>>>>>>>>>>>>>
> /home/evgen/univer/praktyka/nalag2/lab_exc.py(14)period()
-> t = 2 * math.pi * math.sqrt(length / g)
(Pdb) p length
'0.25'
(Pdb) w
  /usr/lib/python3.12/doctest.py(1361)__run()
-> exec(compile(example.source, filename, "single",
  <doctest lab_exc.period[1]>(1)<module>()
> /home/evgen/univer/praktyka/nalag2/lab_exc.py(14)period()
-> t = 2 * math.pi * math.sqrt(length / g)
(Pdb) q

===================================== short test summary info ======================================
FAILED lab_exc.py::lab_exc.period
!!!!!!!!!!!!!!!!!!!!!!!!!!!!! _pytest.outcomes.Exit: Quitting debugger !!!!!!!!!!!!!!!!!!!!!!!!!!!!!
1 failed in 1.38s
```

> **Нове тут:**
>
> - `python3 -m pytest` - проганяє doctest і дає чесний код виходу 0/1. Назва: py + test - «тести для Python». `--doctest-modules` - шукати doctest (приклади >>>) у файлах .py; без нього pytest шукає лише функції test_; `--pdb` - при провалі або винятку одразу відкрити pdb у місці падіння; `-q` - коротко: крапка за кожен тест і рядок підсумку «1 passed in 0.01s».

А коли doctest просто дав інше число (`Expected`/`Got`), `--pdb` зупиняється всередині коду самого pytest
(`_pytest/doctest.py ... raise failure`), де твоїх змінних нема: `p t` дає `*** NameError: name 't' is not defined`.
`--trace` (зупинка на початку кожного тесту) на doctest у pytest 9.2 не діє - тест просто проходить до кінця:

```bash
python3 -m pytest --doctest-modules --trace -q lab_demo.py
```

```text
F                                                                                            [100%]
============================================= FAILURES =============================================
____________________________________ [doctest] lab_demo.period _____________________________________
006 Період математичного маятника.
007
008     >>> period(1.0)
Expected:
    'T = 2.006 с'
Got:
    'T = 2.01 с'

/home/evgen/univer/praktyka/nalag2/lab_demo.py:8: DocTestFailure
===================================== short test summary info ======================================
FAILED lab_demo.py::lab_demo.period
1 failed in 0.01s
```

> **Нове тут:**
>
> - `python3 -m pytest`: `--trace` - зупинитись у pdb на початку кожного тесту.

Підсумок для лаб: інше число → `python3 лаба.py -v` і `breakpoint()` у функції; виняток → `--pdb` або `-c continue`.

**З `breakpoint()` ввід набирай руками**, не через `printf ... |`. pdb читає команди з того самого входу, що й
`input()`: після `printf` там уже кінець вводу, pdb отримує його замість команди і зупиняє програму - в кінці
traceback буде `bdb.BdbQuit`. Тому `python3 лаба.py -v`, на `input()` набери число, а на `(Pdb)` - команди.

### Крок 9. Тренування

Тека **«Налагодження - зламані програми»** поруч з уроками курсу: `bug_1.py` ... `bug_7.py` і `ЗАВДАННЯ.md`. Тека
курсу лежить на ПК; на ноутбук її переносиш флешкою, через GitHub або пересилаєш собі в Telegram архівом (zip;
розпакувати в Nemo - подвійний клік). Коли тека на ноутбуці (наприклад, у `~/Завантаження`), скопіюй її в робоче
місце (лапки - бо в назві пробіли):

```bash
mkdir -p ~/univer/praktyka
cp -r ~/Завантаження/"Налагодження - зламані програми" ~/univer/praktyka/zlamani
ls ~/univer/praktyka/zlamani
```

> **Нове тут:**
>
> - `cp` - копіює файл або теку. Назва: copy - «копіювати». `-r` - копіювати теку разом з усім, що всередині (recursive); те саме -R.
> - `ls` - показує, що лежить у теці. Назва: list - «список» (вмісту теки).

Не знаходиш теку - `find ~ -name "bug_1.py"`. Далі по черзі: прочитай симптом, вибери метод, знайди баг сам, і
лише потім відкривай підказки. Методи з logging і faulthandler там - лише другий варіант (є і print).

## Далі - за бажанням (для ЛР1-ЛР3 не потрібно)

Кроки 10-12 - інструменти, які знадобляться пізніше, на довгих програмах. Можна пропустити й повернутись згодом.

### Крок 10. logging замість print

**logging** (журналювання) - друк налагоджувальних повідомлень з **рівнем** важливості. Рівні від найменшого:
`DEBUG` (подробиці), `INFO` (що відбувається), `WARNING` (щось підозріле), `ERROR`, `CRITICAL`. `kydok_log.py`:

```python
"""Тіло кинули вертикально вгору: таблиця висот (з logging)."""
import logging

logging.basicConfig(
    level=logging.DEBUG,
    format="%(levelname)s %(funcName)s:%(lineno)d %(message)s",
)
G = 9.81


def height(v0, t):
    h = v0 * t - G * t ** 2 / 2
    logging.debug(f"{t=} {h=:.3f}")
    if h < 0:
        logging.warning(f"тіло вже впало, {h=:.3f}")
    return round(h, 3)


def table(v0, dt, steps):
    logging.info(f"рахую {steps} рядків, крок {dt} с")
    rows = []
    for k in range(steps):
        t = k * dt
        rows.append((t, height(v0, t)))
    return rows


def main():
    for t, h in table(10, 0.5, 6):
        print(f"t = {t:.1f} с   h = {h:6.3f} м")


main()
```

```bash
python3 kydok_log.py
```

```text
INFO table:20 рахую 6 рядків, крок 0.5 с
DEBUG height:13 t=0.0 h=0.000
DEBUG height:13 t=0.5 h=3.774
DEBUG height:13 t=1.0 h=5.095
DEBUG height:13 t=1.5 h=3.964
DEBUG height:13 t=2.0 h=0.380
DEBUG height:13 t=2.5 h=-5.656
WARNING height:15 тіло вже впало, h=-5.656
t = 0.0 с   h =  0.000 м
t = 0.5 с   h =  3.774 м
t = 1.0 с   h =  5.095 м
t = 1.5 с   h =  3.964 м
t = 2.0 с   h =  0.380 м
t = 2.5 с   h = -5.656 м
```

`format` додав рівень, функцію і номер рядка - видно, звідки кожне повідомлення. logging пише в stderr, тому лог
не змішується з результатом у файлі (`2>`). Тепер заміни `level=logging.DEBUG` на `level=logging.WARNING`:

```text
WARNING height:15 тіло вже впало, h=-5.656
t = 0.0 с   h =  0.000 м
t = 0.5 с   h =  3.774 м
t = 1.0 с   h =  5.095 м
t = 1.5 с   h =  3.964 м
t = 2.0 с   h =  0.380 м
t = 2.5 с   h = -5.656 м
```

Лог у файл: у `basicConfig` напиши `level=logging.DEBUG, filename="kydok.log", filemode="w",` (`"w"` - щоразу
новий файл, без нього дописує в кінець):

```bash
python3 kydok_log.py
cat kydok.log
```

```text
t = 0.0 с   h =  0.000 м
t = 0.5 с   h =  3.774 м
t = 1.0 с   h =  5.095 м
t = 1.5 с   h =  3.964 м
t = 2.0 с   h =  0.380 м
t = 2.5 с   h = -5.656 м
INFO table:20 рахую 6 рядків, крок 0.5 с
DEBUG height:13 t=0.0 h=0.000
DEBUG height:13 t=0.5 h=3.774
DEBUG height:13 t=1.0 h=5.095
DEBUG height:13 t=1.5 h=3.964
DEBUG height:13 t=2.0 h=0.380
DEBUG height:13 t=2.5 h=-5.656
WARNING height:15 тіло вже впало, h=-5.656
```

> **Нове тут:**
>
> - `cat` - показує вміст файлу. Назва: concatenate - «зчепити»: склеює кілька файлів в один вивід.

Чим краще за `print`: рядки налагодження не треба видаляти (лише змінити рівень), видно функцію й рядок, можна
писати у файл і читати потім. Для лаби з doctest - теж зручно: logging іде в stderr і doctest його не бачить.

### Крок 11. Прапорці Python для пошуку прихованих проблем

**`-X dev`** - режим розробника: показує попередження, які зазвичай мовчать. `dani.py` відкриває файл і не
закриває:

```python
values = [float(line) for line in open("dani.txt")]
print(f"середнє: {sum(values) / len(values):.3f}")
```

```bash
printf '2.01\n1.99\n2.02\n' > dani.txt
python3 -X dev dani.py
```

```text
/home/evgen/univer/praktyka/nalag2/dani.py:1: ResourceWarning: unclosed file <_io.TextIOWrapper name='dani.txt' mode='r' encoding='UTF-8'>
  values = [float(line) for line in open("dani.txt")]
ResourceWarning: Enable tracemalloc to get the object allocation traceback
середнє: 2.007
```

> **Нове тут:**
>
> - `printf` - друкує текст за шаблоном; \n - Enter. Назва: print formatted - «надрукувати за шаблоном».
> - `python3`: `-X` - особливі режими: -X dev (усі попередження), -X faulthandler (аварії), -X importtime (час імпорту).
> - `>` - пише вивід у файл, старий вміст стирає. Назва: redirect - «перенаправлення» виводу у файл.

Без `-X dev` - лише `середнє: 2.007`. Правильно: `with open("dani.txt") as file:`.

**`-W error`** - кожне попередження (warning) стає помилкою. `chysla.py` шукає числа в рядку:

```python
import re

text = "t=0.5 h=3.774"
numbers = re.findall("\d+\.\d+", text)
print(numbers)
```

```bash
python3 chysla.py
python3 -W error chysla.py
```

```text
/home/evgen/univer/praktyka/nalag2/chysla.py:4: SyntaxWarning: invalid escape sequence '\d'
  numbers = re.findall("\d+\.\d+", text)
['0.5', '3.774']
  File "/home/evgen/univer/praktyka/nalag2/chysla.py", line 4
    numbers = re.findall("\d+\.\d+", text)
                         ^^^^^^^^^^
SyntaxError: invalid escape sequence '\d'
```

> **Нове тут:**
>
> - `python3`: `-W` - що робити з попередженнями (warnings): -W error робить кожне попередження помилкою.

Попередження легко не помітити, а з `-W error` програма не запуститься, поки не виправиш. Виправлення:
`r"\d+\.\d+"` (буква `r` - «сирий» рядок, `\` у ньому - просто символ).

**Програма зависла.** `zavis.py` гальмує швидкість по 0.4, поки вона не стане рівно 0 (а через похибку float вона
ніколи не буде рівно 0):

```python
speed = 10.0
while speed != 0:
    speed -= 0.4
print("зупинилось")
```

```bash
python3 zavis.py
```

Через кілька секунд натисни Ctrl+C. Traceback покаже, **де** програма крутилась:

```text
^CTraceback (most recent call last):
  File "/home/evgen/univer/praktyka/nalag2/zavis.py", line 2, in <module>
    while speed != 0:
          ^^^^^^^^^^
KeyboardInterrupt
```

Якщо програма висить у місці, де Ctrl+C не допомагає, або хочеш автоматично, - `faulthandler`
(обробник аварій). Додай на початок `zavis.py`:

```python
import faulthandler

faulthandler.dump_traceback_later(3, exit=True)
speed = 10.0
while speed != 0:
    speed -= 0.4
print("зупинилось")
```

```text
Timeout (0:00:03)!
Thread 0x000075e683cf2080 (most recent call first):
  File "/home/evgen/univer/praktyka/nalag2/zavis.py", line 6 in <module>
```

Через 3 с він сам надрукував, у якому рядку програма, і завершив її (`exit=True`). Число `0x...` у тебе буде інше,
а рядок може бути 5 або 6 (з чотирьох запусків тричі був 6): програма крутиться в обох рядках циклу, і `faulthandler`
показує той, де вона була в момент знімка.

**`-X faulthandler`** - для справжніх аварій інтерпретатора (Segmentation fault), коли Python не встигає надрукувати
traceback. Буває з бібліотеками на C (numpy, tkinter/turtle). Штучна аварія для прикладу:

```bash
python3 -X faulthandler -c "import ctypes; ctypes.string_at(0)"
```

```text
Fatal Python error: Segmentation fault

Current thread 0x0000781de291d080 (most recent call first):
  File "/usr/lib/python3.12/ctypes/__init__.py", line 525 in string_at
  File "<string>", line 1 in <module>
```

Без `-X faulthandler` bash напише лише `Segmentation fault (core dumped)` - без жодного рядка коду (так англійською;
у системі українською текст може бути перекладений, не перевірено).

**Коротко про швидкість і трасування:**

```bash
python3 -X importtime -c "import fractions" |& tail -3
python3 -m trace --trace kydok.py | head -12
python3 -m timeit "sum(range(1000))"
python3 -m cProfile -s cumtime kydok.py | head -14
```

```text
import time:       130 |        130 |     copyreg
import time:       444 |       2641 |   re
import time:      1604 |       7823 | fractions
 --- modulename: kydok, funcname: <module>
kydok.py(1): """Тіло кинули вертикально вгору: таблиця висот."""
kydok.py(2): G = 9.81
kydok.py(5): def height(v0, t):
kydok.py(10): def table(v0, dt, steps):
kydok.py(19): def main():
kydok.py(26): main()
 --- modulename: kydok, funcname: main
kydok.py(20):     rows = table(10, 0.5, 5)
 --- modulename: kydok, funcname: table
kydok.py(11):     rows = []
kydok.py(12):     for k in range(steps):
20000 loops, best of 5: 9.99 usec per loop
t = 0.0 с   h =  0.000 м
t = 0.5 с   h =  3.774 м
t = 1.0 с   h =  5.095 м
t = 1.5 с   h =  3.964 м
t = 2.0 с   h =  0.380 м
готово
         26 function calls in 0.000 seconds

   Ordered by: cumulative time

   ncalls  tottime  percall  cumtime  percall filename:lineno(function)
        1    0.000    0.000    0.000    0.000 {built-in method builtins.exec}
        1    0.000    0.000    0.000    0.000 kydok.py:1(<module>)
        1    0.000    0.000    0.000    0.000 kydok.py:19(main)
```

> **Нове тут:**
>
> - `python3 -m trace` - друкує кожен виконаний рядок програми. Назва: trace - «слід», «простежити»: показує шлях програми по рядках. `--trace` - друкувати кожен рядок перед виконанням (видно шлях програми без print).
> - `head` - показує перші рядки файлу. Назва: head - «голова»: початок файлу.
> - `python3 -m timeit` - міряє, скільки триває маленький шматок коду. Назва: time it - «засічи час цього».
> - `python3 -m cProfile` - показує, які функції скільки разів викликались і скільки часу. Назва: C profile - «профіль» програми; модуль написаний мовою C, тому швидкий. `-s` - як сортувати таблицю: cumtime (загальний час), ncalls (кількість викликів), tottime.
> - `|` - передає вивід однієї команди на ввід іншій. Назва: pipe - «труба» (пайп), вертикальна риска.

- `-X importtime` - скільки мікросекунд імпортується кожен модуль (числа в тебе будуть інші). Він пише в stderr,
  тому `|&` замість `|`: так у `tail` іде і звичайний вивід, і stderr.
- `trace --trace` друкує **кожен** виконаний рядок - видно шлях програми без жодного `print`.
- `timeit` міряє дрібний вираз багато разів; `cProfile` - скільки разів викликана кожна функція і скільки часу
  забрала (`ncalls`, `cumtime`). Для лаб рідко треба, але коли програма «думає» хвилину - саме те.

### Крок 12. ipdb і pudb - сторонні налагоджувачі (у venv)

Ставимо **у venv**, не в систему (PEP 668, урок 03):

```bash
~/univer/.venv/bin/pip install ipdb pudb
source ~/univer/.venv/bin/activate
```

> **Нове тут:**
>
> - `./скрипт` - запускає свій файл-скрипт з поточної теки. Назва: ./ - «звідси»: крапка = поточна тека, / відділяє теку від файлу.
> - `source` - виконує файл у поточному bash (venv, ~/.bashrc). Назва: source - «джерело»: виконати команди з файлу-джерела. `~/univer/.venv/bin/activate` - увімкнути venv для лаб; вимкнути - deactivate.

**ipdb** - той самий pdb, але в стилі IPython: кольори, Tab доповнює імена, код навколо видно одразу. Вмикається
без правки файлу - через `PYTHONBREAKPOINT` (тоді кожен `breakpoint()` відкриває ipdb). На `period.py` з уроку 05:

```bash
cd ~/univer/praktyka/nalag1
PYTHONBREAKPOINT=ipdb.set_trace python3 period.py
```

Справжній екран (ipdb 0.13.13, IPython 9.18):

```text
> /home/evgen/univer/praktyka/nalag1/period.py(15)main()
     14         breakpoint()
---> 15         print(f"l = {length} м, T = {period(length):.3f} с")
     16

ipdb> p length
0.5
ipdb> c
l = 0.5 м, T = 1.419 с
> /home/evgen/univer/praktyka/nalag1/period.py(15)main()
     14         breakpoint()
---> 15         print(f"l = {length} м, T = {period(length):.3f} с")
     16

ipdb> q
Error in sys.excepthook:
Traceback (most recent call last):
  File "/home/evgen/univer/.venv/lib/python3.12/site-packages/IPython/core/debugger.py", line 183, i
n BdbQuit_excepthook
    raise ValueError(
ValueError: `BdbQuit_excepthook` is deprecated since version 5.1. It is still around only because it
 is still imported by ipdb.

Original exception was:
Traceback (most recent call last):
  File "/home/evgen/univer/praktyka/nalag1/period.py", line 18, in <module>
    main()
  File "/home/evgen/univer/praktyka/nalag1/period.py", line 15, in main
    print(f"l = {length} м, T = {period(length):.3f} с")
    ^^^^^
  File "/usr/lib/python3.12/bdb.py", line 90, in trace_dispatch
    return self.dispatch_line(frame)
           ^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/lib/python3.12/bdb.py", line 115, in dispatch_line
    if self.quitting: raise BdbQuit
                      ^^^^^^^^^^^^^
bdb.BdbQuit
```

Команди ті самі, що в pdb. Неприємність ipdb 0.13.13 з новим IPython 9: після виходу (і після будь-якого
необробленого винятку) зверху друкується `Error in sys.excepthook ... deprecated`. Справжня помилка - нижче, після
`Original exception was:`. Запуск з першого рядка: `python3 -m ipdb kydok.py`.

**pudb** - налагоджувач **на весь екран** термінала, схожий на графічний: код, змінні, стек і точки зупинки видно
одночасно:

```bash
cd ~/univer/praktyka/nalag2
python3 -m pudb kydok.py
```

> **Нове тут:**
>
> - `python3 -m pudb` - налагоджувач на весь екран, як графічний (ставиться у venv). Назва: назва не розшифровується; db - від debugger, «налагоджувач».

Перший запуск показує вікно «Welcome to PudB 2026.1!», потім «Edit Preferences» (налаштування; закрий кнопкою
`< OK >`). Екран після кількох `n` і `s` (справжній, термінал 100×30):

```text
PuDB 2026.1 - ?:help  n:next  s:step into  b:breakpoint  !:python command line
                                                                   Variables:
                                                                   dt: 0.5
  def height(v0, t):                                               h: 0.0
      h = v0 * t - G * t ** 2 / 2                                  k: 0
      return round(h, 3)                                           rows: list (0)
                                                                   steps: 5
                                                                   t: 0.0
  def table(v0, dt, steps):                                        v0: 10
      rows = []
      for k in range(steps):
          t = k * dt                                               Stack:
          h = height(v0, t)                                        >> table kydok.py:15
>         rows.append((t, h))                                         main kydok.py:20
      return rows                                                     <module> kydok.py:26


  def main():
      rows = table(10, 0.5, 5)
      for t, h in rows:
          print(f"t = {t:.1f} с   h = {h:6.3f} м")
      print("готово")                                              Breakpoints:


  main()
Command line: [ctrl x]



>>>                                                     < Clear  >
```

Клавіші pudb (одна літера, без Enter): `n`, `s`, `c`, `b` (точка на рядку під курсором), `!` (Python), `?` (довідка),
`q` (вийти: з'явиться вікно Finished з `< Restart >` / `< Quit >`, там ще раз `q`).

## Типові помилки

- **Змінна з іменем команди** (`h`, `c`, `n`, `s`, `l`, `a`, `b`...): pdb виконує команду. Пиши `p h`, `!h = 0`.
- **`!G = 1.62` не змінює глобальну `G`** - створює локальну. Треба `!global G; G = 1.62`.
- **`commands` з `c` і потім `end`** → `*** NameError: name 'end' is not defined`: `c` уже закінчив список.
- **`until` «не вийшов» з циклу** - на шляху стоїть точка зупинки. Прибери її (`cl номер`).
- **`j` у цикл** → `*** Jump failed: can't jump into the body of a for loop`. Стрибати можна лише в межах поточної
  функції і не всередину циклу.
- **post-mortem `q` → програма знову з першого рядка.** Так задумано (`will be restarted`), `q` ще раз.
- **`p змінна` → `NameError` у post-mortem** - ти не в тій функції. `w` покаже стек, `u`/`d` - перейти.
- **`breakpoint()` у функції + pytest** → `OSError: pytest: reading from stdin while output is captured!`, а
  `perevir` (урок 03) у цьому випадку пише «файл питає input()». Налагоджуй через `python3 лаба.py`, а перед
  здачею прибери `breakpoint()`.
- **Номери рядків з'їхали** - ти змінив файл, а pdb показує старі номери. Після правки - `restart` або вийти і
  запустити знову.
- **`logging.basicConfig` нічого не змінює** - його треба викликати **до** першого `logging.warning(...)` /
  `logging.debug(...)`. Перший такий виклик сам налаштовує logging (рівень WARNING), і пізніший
  `basicConfig(level=logging.DEBUG)` уже ігнорується: `logging.debug("друге")` після нього не друкується.

## Як роблять профі

- У 2025-2026 у великих проєктах налагоджують у редакторі (VS Code / PyCharm: точки зупинки мишкою, debugpy) -
  це урок 27, пізніше. Але pdb знає кожен, бо він є всюди: на сервері по ssh, у Docker, на чужому комп'ютері.
- Python 3.14 додав `python -m pdb -p PID` - підключитись до програми, **що вже працює** (PEP 768), і підсвітку
  коду в pdb. У Mint 22 стоїть 3.12, там цього нема.
- `logging` у бібліотеках пишуть «ліниво»: `logging.debug("h=%s", h)` замість f-рядка - рядок не збирається,
  коли рівень DEBUG вимкнено. Для лаб f-рядок теж нормально.
- Профілювання: cProfile для початку, для довгих програм - `py-spy` (стороння програма, не перевірено в Mint 22).
- `pytest --pdb` у великих проєктах - звичайний спосіб: тест упав → одразу в pdb у місці падіння.

## Самоперевірка

1. Як зупинитись у циклі `for k in range(1000)` лише на `k == 500`, не натискаючи `c` 500 разів?
2. Програма впала з `ZeroDivisionError` у функції `mean`. Опиши два способи подивитись значення змінних у момент
   падіння, не додаючи нічого в код.
3. У функції є змінна `c`. Що станеться, якщо в pdb набрати `c`? Як подивитись значення змінної?
4. У лабі два doctest впали по-різному: один - `Expected: 'T = 2.006 с'`, `Got: 'T = 2.01 с'`, другий -
   `UNEXPECTED EXCEPTION: TypeError(...)`. Яким інструментом дивитись змінні в кожному випадку і чому не одним?
5. Навіщо `logging` замість `print`, якщо обидва просто друкують текст? Назви дві переваги.

<details markdown="1"><summary>Відповіді</summary>

1. Точка зупинки з умовою: `b номер_рядка, k == 500` (або `condition 1 k == 500` для вже поставленої точки).
   Ще варіант - `ignore 1 500`.
2. `python3 -m pdb -c continue файл.py` - pdb сам зупиниться в місці падіння; або `python3 -i файл.py`, а після
   падіння `import pdb; pdb.pm()`. Далі `p змінна`, `u`, `w`.
3. pdb виконає команду continue (поїде далі). Значення - `p c`, змінити - `!c = ...`.
4. Інше число (`Expected`/`Got`): `breakpoint()` перед `return` + `python3 файл.py -v`, на `(Pdb)` - `p t`
   (ввід для `input()` - руками). Виняток: `python3 -m pytest --doctest-modules --pdb файл.py` - зупиниться в
   місці падіння, там `p length`. `--pdb` при простому `Expected`/`Got` зупиняється всередині pytest, де твоїх
   змінних нема (крок 8).
5. Можна вимкнути/увімкнути всі повідомлення одним рівнем (`DEBUG` → `WARNING`) без видалення рядків; у кожному
   рядку видно рівень, функцію і номер рядка; легко писати у файл; іде в stderr і не ламає doctest.
</details>

## Джерела

- `pdb` (усі команди, `commands`, `!` з `global`, post-mortem і перезапуск) - https://docs.python.org/3.12/library/pdb.html
  (відкрито 18.11.2026)
- `doctest` (`-v`, `optionflags`, `FAIL_FAST`, `debug`) - https://docs.python.org/3.12/library/doctest.html
  (відкрито 18.11.2026)
- `logging` HOWTO і `basicConfig` - https://docs.python.org/3.12/howto/logging.html ,
  https://docs.python.org/3.12/library/logging.html#logging.basicConfig (відкрито 18.11.2026)
- Прапорці `-X dev`, `-X faulthandler`, `-X importtime`, `-W` - https://docs.python.org/3.12/using/cmdline.html ,
  `faulthandler` - https://docs.python.org/3.12/library/faulthandler.html (відкрито 18.11.2026)
- `trace`, `timeit`, `cProfile` - https://docs.python.org/3.12/library/trace.html ,
  https://docs.python.org/3.12/library/timeit.html , https://docs.python.org/3.12/library/profile.html
  (відкрито 18.11.2026)
- pytest: `--pdb`, `--trace`, doctest - https://docs.pytest.org/en/stable/how-to/failures.html ,
  https://docs.pytest.org/en/stable/how-to/doctest.html (відкрито 18.11.2026)
- ipdb - https://pypi.org/project/ipdb/ ; pudb - https://documen.tician.de/pudb/ (відкрито 18.11.2026)
- Python 3.14: `pdb -p PID`, PEP 768 - https://docs.python.org/3/whatsnew/3.14.html (відкрито 18.11.2026)
- Увесь вивід у цьому уроці - справжній, з тестової Linux Mint 22.3, Python 3.12.3, pytest 9.2.0, ipdb 0.13.13,
  pudb 2026.1 (18.11.2026). Екрани ipdb і pudb зняті емулятором термінала 100×30.
