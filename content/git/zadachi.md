# Практика і підсумковий іспит

## Чотири завдання як у справжній роботі

Чотири задачі «як у житті»: не одна команда, а ціла ситуація, яку треба довести до кінця. Кожна - 20-40 хвилин.
Роби їх після уроків 01-16 (або хоча б після уроку, який вказано біля задачі).

| № | Задача | Час | Уроки |
|---|---|---|---|
| 1 | Лаба з напарником: дві гілки, два PR, конфлікт в одному рядку | 30-40 хв | 07, 08, 09, 11 |
| 2 | Аварія перед здачею: .venv і 200 МБ у коміті, втрачений коміт, токен на GitHub | 30-40 хв | 06, 12 |
| 3 | Здача ЛР з тегом і архівом | 20-30 хв | 14, «Лаби в git» |
| 4 | Свій сайт-портфоліо на Pages за 30 хв | 30 хв | 10, 15, 16 |

**Як працювати:**
1. Прочитай умову і «Що треба отримати». Спробуй сам, з уроками під рукою.
2. Застряг на 5 хвилин - відкрий **одну** підказку. Не допомогла - наступну.
3. Розвʼязок відкривай, коли зробив сам (звірити) або коли зовсім глухо (тоді пройди його і через день зроби задачу ще раз з нуля).
4. В кінці кожної задачі - «Що перевірити в кінці». Задача зроблена, лише коли всі пункти там збігаються.

**Про вивід.** Увесь вивід нижче - справжній, з перевірки (git 2.43.0, як на Mint 22.3). У перевірці час кожного коміту
зафіксовано (тому дати на кшталт `Wed Nov 18 10:10:00 2026 +0000`), а **хеші й дати в тебе будуть інші** - дивись на будову.
Рядок пушу на GitHub - `To github.com:Evge14n/РЕПО.git`. Виняток - тренажер у задачах 2-3: там «GitHub» - справжня тека
на диску, і рядок буде `To /home/ТВІЙ-ЛОГІН/trenazher/github/univer-labs.git` (у виводі нижче - `/home/...`).

---

### Задача 1. Лаба з напарником (30-40 хв)

**Умова.** ЛР4 робите вдвох з одногрупником в одному репо. Викладач дав заготовку функції `shliakh` (шлях при
рівноприскореному русі) з двома doctest. У заготовці дві помилки: нема `/ 2` у формулі і нема округлення до 0.01.
Домовились: одногрупник виправляє формулу, ти - округлення. Кожен працює у своїй гілці і відкриває свій PR.
Одногрупник встиг першим - його PR злили. Твій PR тепер у конфлікті, бо ви обидва правили **той самий рядок** `return`.

Одногрупника грає другий клон `~/druhyi-klon` (урок 08, у ньому `user.name` = «Друг»). Спільне репо - твоя приватна
пісочниця `pisochnytsia`. Якщо `~/druhyi-klon` ще нема: `git clone git@github.com:Evge14n/pisochnytsia.git ~/druhyi-klon`,
потім у ньому `git config user.name "Друг"`.

Заготовка `para/kinematyka.py` (рівно так, 9 рядків, відступи - 4 пробіли):
```text
def shliakh(v0, a, t):
    """Шлях при рівноприскореному русі, м (до 0.01).

    >>> shliakh(0, 2, 3)
    9.0
    >>> shliakh(0.1, 0, 3)
    0.3
    """
    return v0 * t + a * t ** 2
```
Правка одногрупника (рядок 9): `    return v0 * t + a * t ** 2 / 2`.
Твоя правка (рядок 9): `    return round(v0 * t + a * t ** 2, 2)`.

**Що треба отримати (готово, коли):**
- у `main` на GitHub є обидва PR, злиті через **Merge pull request**;
- `python3 -m doctest para/kinematyka.py` у `main` нічого не друкує (усі тести пройшли) - і в `~/pisochnytsia`, і в `~/druhyi-klon`;
- у файлі нема маркерів `<<<<<<<`, `=======`, `>>>>>>>`;
- `git log --oneline --graph` показує обидві гілки і обидва злиття;
- гілки `formula` і `okruhlennia` видалено (на GitHub і в себе).

<details markdown="1"><summary>Підказка 1 - з чого почати</summary>

Спершу заготовка в `main` і push - щоб обидва клони почали з одного місця. Свою гілку `okruhlennia` створи **одразу після
push**, ще до того, як одногрупник щось зробить - так буває в житті: ви почали паралельно.
</details>

<details markdown="1"><summary>Підказка 2 - чому doctest падає в кожного</summary>

Перший тест `shliakh(0, 2, 3)` ловить формулу (без `/ 2` вийде 18), другий `shliakh(0.1, 0, 3)` ловить округлення
(без `round` вийде `0.30000000000000004`). Тож у кожного з вас падає рівно один тест - «чужа» частина. Це нормально:
готово буде лише тоді, коли обидві правки зійдуться в одному рядку.
</details>

<details markdown="1"><summary>Підказка 3 - як розвʼязати конфлікт PR</summary>

Кнопка на сайті не завжди може розвʼязати конфлікт, а в терміналі - завжди. Забери свіжий `main` з GitHub (`git fetch`)
і злий його **у свою гілку**: `git merge origin/main`. Далі - як в уроці 08: маркери, nano, doctest, `git add`, `git commit`,
`git push`. PR оновиться сам - він показує гілку, а не окремі коміти.
</details>

<details markdown="1"><summary>Підказка 4 - який рядок лишити</summary>

Ні «свій», ні «чужий»: у кожному лише одна з двох правок. Потрібен **третій** рядок, де є і `/ 2`, і `round(..., 2)`.
</details>

<details markdown="1"><summary>Повний розвʼязок</summary>

**Крок 1. Ти: заготовка в main.**
```bash
cd ~/pisochnytsia
git switch main
git pull
mkdir -p para
nano para/kinematyka.py
python3 -m doctest para/kinematyka.py | tail -n 1
git add para/kinematyka.py
git commit -m "ЛР4: заготовка викладача"
git push
git switch -c okruhlennia
```
У nano вставляєш заготовку з умови. `| tail -n 1` - показати лише останній рядок звіту doctest:
```text
***Test Failed*** 2 failures.
[main a786b16] ЛР4: заготовка викладача
 1 file changed, 9 insertions(+)
 create mode 100644 para/kinematyka.py
To github.com:Evge14n/pisochnytsia.git
   fdfc53c..a786b16  main -> main
Switched to a new branch 'okruhlennia'
```
Повний звіт (без `tail`) пояснює, що саме не так, наприклад:
```text
Failed example:
    shliakh(0, 2, 3)
Expected:
    9.0
Got:
    18
```

**Крок 2. Одногрупник: формула у гілці formula.**
```bash
cd ~/druhyi-klon
git switch main
git pull
git switch -c formula
nano para/kinematyka.py
python3 -m doctest para/kinematyka.py | tail -n 1
git commit -am "ЛР4: формула шляху з / 2"
git push -u origin formula
```
У nano рядок 9 → `    return v0 * t + a * t ** 2 / 2`.
```text
***Test Failed*** 1 failures.
[formula ad64fa8] ЛР4: формула шляху з / 2
 1 file changed, 1 insertion(+), 1 deletion(-)
To github.com:Evge14n/pisochnytsia.git
 * [new branch]      formula -> formula
branch 'formula' set up to track 'origin/formula'.
```
Один тест падає - це округлення, твоя частина. PR одногрупника: на сайті жовта плашка **Compare & pull request** →
base `main` ← compare `formula` → **Create pull request** → **Merge pull request** → **Confirm merge** → **Delete branch**.
Обидва клони - твій акаунт, тож PR одногрупника відкриваєш і зливаєш сам. Або з терміналу (з `~/druhyi-klon`):
```bash
gh pr create --base main --head formula --title "ЛР4: формула шляху" --body "Виправив формулу: a * t ** 2 / 2"
gh pr merge formula --merge
```
Після `gh pr merge` гілку `formula` на GitHub видали кнопкою **Delete branch** на сторінці PR.

**Крок 3. Ти: округлення у гілці okruhlennia.** Гілка відгалузилась від `main` ще до злиття formula - про формулу вона не знає.
```bash
cd ~/pisochnytsia
nano para/kinematyka.py
python3 -m doctest para/kinematyka.py | tail -n 1
git commit -am "ЛР4: округлення до 0.01"
git push -u origin okruhlennia
```
У nano рядок 9 → `    return round(v0 * t + a * t ** 2, 2)`.
```text
***Test Failed*** 1 failures.
[okruhlennia 91bb560] ЛР4: округлення до 0.01
 1 file changed, 1 insertion(+), 1 deletion(-)
To github.com:Evge14n/pisochnytsia.git
 * [new branch]      okruhlennia -> okruhlennia
branch 'okruhlennia' set up to track 'origin/okruhlennia'.
```
Відкриваєш PR `okruhlennia` → `main`. Тепер на сторінці PR замість зеленої кнопки злиття - попередження про конфлікт
і кнопка **Resolve conflicts** (docs, «Resolving a merge conflict on GitHub»; точний текст попередження не перевірено).

**Крок 4. Ти: розвʼязати конфлікт у своїй гілці.**
```bash
git fetch
git merge origin/main
git status --short
cat para/kinematyka.py
```
```text
Auto-merging para/kinematyka.py
CONFLICT (content): Merge conflict in para/kinematyka.py
Automatic merge failed; fix conflicts and then commit the result.
UU para/kinematyka.py
?? para/__pycache__/
def shliakh(v0, a, t):
    """Шлях при рівноприскореному русі, м (до 0.01).

    >>> shliakh(0, 2, 3)
    9.0
    >>> shliakh(0.1, 0, 3)
    0.3
    """
<<<<<<< HEAD
    return round(v0 * t + a * t ** 2, 2)
=======
    return v0 * t + a * t ** 2 / 2
>>>>>>> origin/main
```
`HEAD` - твоя гілка, `origin/main` - те, що прийшло з GitHub (формула одногрупника). `?? para/__pycache__/` - тека, яку
створив doctest; у пісочниці нема `.gitignore` з уроку 06, тому git її бачить. Не додавай її в коміт (`git add` лише файлу).

Відкрий nano і заміни **всі пʼять рядків** від `<<<<<<< HEAD` до `>>>>>>> origin/main` одним:
```text
    return round(v0 * t + a * t ** 2 / 2, 2)
```
Потім:
```bash
nano para/kinematyka.py
python3 -m doctest para/kinematyka.py
git diff --check
git add para/kinematyka.py
git commit
git push
```
doctest і `git diff --check` мовчать - тести пройшли і маркерів нема. `git commit` відкриє nano з готовим повідомленням -
просто Ctrl+X:
```text
[okruhlennia e38cd66] Merge remote-tracking branch 'origin/main' into okruhlennia
To github.com:Evge14n/pisochnytsia.git
   91bb560..e38cd66  okruhlennia -> okruhlennia
```
Онови сторінку PR - конфлікту нема, кнопка **Merge pull request** зелена. Злий і натисни **Delete branch**.

**Крок 5. Ти: забрати результат і прибрати.**
```bash
git switch main
git pull
python3 -m doctest para/kinematyka.py
git log --oneline --graph -n 8
git branch -d okruhlennia
git fetch --prune
```
```text
*   985bf3e (HEAD -> main, origin/main, origin/HEAD) Merge pull request #2 from Evge14n/okruhlennia
|\
| *   e38cd66 (origin/okruhlennia, okruhlennia) Merge remote-tracking branch 'origin/main' into okruhlennia
| |\
| |/
|/|
* |   6cdbf70 Merge pull request #1 from Evge14n/formula
|\ \
| * | ad64fa8 ЛР4: формула шляху з / 2
|/ /
| * 91bb560 ЛР4: округлення до 0.01
|/
* a786b16 ЛР4: заготовка викладача
* fdfc53c Initial commit
```
Як читати граф знизу вгору: від заготовки `a786b16` пішли дві лінії - `ad64fa8` (одногрупник) і `91bb560` (ти).
Лінія одногрупника першою зійшлась у `main` (`6cdbf70`, PR #1). Потім у твоїй гілці `e38cd66` - твоє злиття
`main` у `okruhlennia` (`|/` і `|/|` - лінія з `main` заходить у твою гілку). І зверху `985bf3e` - PR #2.
Номери PR у тебе будуть інші (у пісочниці вже були PR з уроку 11).

**Крок 6. Одногрупник: забрати результат.**
```bash
cd ~/druhyi-klon
git switch main
git pull
git branch -d formula
git log --format="%h %an: %s" -n 6
```
```text
985bf3e Evge14n: Merge pull request #2 from Evge14n/okruhlennia
e38cd66 Твоє Імʼя: Merge remote-tracking branch 'origin/main' into okruhlennia
91bb560 Твоє Імʼя: ЛР4: округлення до 0.01
6cdbf70 Evge14n: Merge pull request #1 from Evge14n/formula
ad64fa8 Друг: ЛР4: формула шляху з / 2
a786b16 Твоє Імʼя: ЛР4: заготовка викладача
```
Коміти злиття PR робить GitHub: автор - той, хто натиснув Merge (у перевірці його звуть `Evge14n`; на справжньому
GitHub - імʼя з твого профілю, не перевірено).
</details>

**Що перевірити в кінці:**
- `python3 -m doctest para/kinematyka.py` мовчить у **обох** клонах (у `main`);
- `tail -n 1 para/kinematyka.py` → `    return round(v0 * t + a * t ** 2 / 2, 2)`;
- `git log --oneline --graph -n 8` - два «Merge pull request» і твоє злиття в гілці, як у розвʼязку;
- `git branch -a` у `~/pisochnytsia` - нема ні `okruhlennia`, ні `remotes/origin/okruhlennia`;
- `git status` в обох клонах: `Your branch is up to date with 'origin/main'.`

**Типові пастки:**
- **`git pull`, стоячи на своїй гілці, не приносить `main`.** Гілка `okruhlennia` стежить за `origin/okruhlennia`, тож
  pull завантажить `main`, але зливати не буде:
  ```text
  From github.com:Evge14n/pisochnytsia
     a786b16..6cdbf70  main       -> origin/main
  Already up to date.
  ```
  «Already up to date» - про твою гілку, а не про `main`. Потрібне саме `git merge origin/main`.
- **Лишив маркери** і запустив doctest - Python не може навіть прочитати файл:
  ```text
      <<<<<<< HEAD
      ^^
  SyntaxError: invalid syntax
  ```
  `git diff --check` до `git add` ловить це (код 2):
  ```text
  para/kinematyka.py:9: leftover conflict marker
  para/kinematyka.py:11: leftover conflict marker
  para/kinematyka.py:13: leftover conflict marker
  ```
- **Лишив лише свій рядок (або лише чужий).** Git не сперечатиметься, коміт пройде, а doctest скаже
  `***Test Failed*** 1 failures.` Тому після розвʼязання конфлікту - завжди doctest, а вже потім `git add`.
- **Злив `okruhlennia` у `main` у себе і запушив `main` напряму**, без PR. Працює, але одногрупник не бачив твоїх змін
  до злиття. Домовились про PR - зливайте через PR.

---

### Задача 2. Аварія перед здачею (30-40 хв)

**Умова.** Вечір перед здачею ЛР3, ти поспішаєш і робиш три помилки поспіль:
1. `git add .` - і в коміт полетіли `.venv/`, `__pycache__/` і файл вимірювань на **200 МБ** (ще не запушено);
2. хотів скасувати незакомічену правку, а набрав `git reset --hard HEAD~1` - і зник коміт із завданням 3;
3. закомітив файл з токеном доступу до GitHub прямо в коді - і **запушив**.

Треба все виправити так, щоб у гілці `lr3` лишилось лише потрібне, а токен більше нікому не був корисний.

**Тренажер, а не справжні лаби.** Усе робимо в `~/trenazher` - копії «univer-labs» з власним «GitHub»: **голим** (bare)
репо `~/trenazher/github/univer-labs.git`. Голий репо - це репо без робочої теки, лише історія; саме так репо зберігає
GitHub. Push іде в нього, а не в інтернет, тож вигаданий токен нікуди не втече, а справжні лаби лишаться цілими.

**Сцена (набери один раз):**
```bash
mkdir -p ~/trenazher/github
git init --bare -b main ~/trenazher/github/univer-labs.git
git clone ~/trenazher/github/univer-labs.git ~/trenazher/univer-labs
cd ~/trenazher/univer-labs
printf '# Тренажер univer-labs\n' > README.md
git add README.md
git commit -m "Початок"
git push -u origin main
git switch -c lr3
mkdir lr3
printf 'def kvadrat(x):\n    """\n    >>> kvadrat(3)\n    9\n    """\n    return x * x\n' > lr3/lr3_1.py
git add lr3
git commit -m "ЛР3: завдання 1"
```
`git clone` порожнього репо попередить `warning: You appear to have cloned an empty repository.` - так і має бути.

**Аварія 1 (відтвори):** venv (тут - імітація з одного файлу), doctest (він створює `__pycache__`), великі дані
(`truncate -s 200M` миттєво робить файл на 200 МБ з нулів) і `git add .`:
```bash
mkdir -p .venv/bin
printf 'home = /usr/bin\n' > .venv/pyvenv.cfg
python3 -m doctest lr3/lr3_1.py
truncate -s 200M lr3/vymiry.bin
printf 'def kub(x):\n    """\n    >>> kub(2)\n    8\n    """\n    return x ** 3\n' > lr3/lr3_2.py
git add .
git commit -m "ЛР3: завдання 2"
```
```text
[lr3 8695fa7] ЛР3: завдання 2
 4 files changed, 7 insertions(+)
 create mode 100644 .venv/pyvenv.cfg
 create mode 100644 lr3/__pycache__/lr3_1.cpython-312.pyc
 create mode 100644 lr3/lr3_2.py
 create mode 100644 lr3/vymiry.bin
```

**Що треба отримати після аварії 1:** коміт «ЛР3: завдання 2» містить лише `lr3/lr3_2.py` і `.gitignore`; у **жодному**
коміті гілки `lr3` нема `vymiry.bin` (старий коміт з ним лишиться лише в reflog, аварія 2 це покаже); файли на диску
лишились; `git status --short` порожній.

<details markdown="1"><summary>Підказка А1</summary>

Ще не запушено - отже останній коміт можна переписати (`--amend`, урок 12). Прибрати з git, лишивши на диску, -
`git rm -r --cached` (урок 06). А щоб `git add .` більше так не робив - `.gitignore`.
</details>

<details markdown="1"><summary>Розвʼязок А1</summary>

Спершу подивись, що саме в коміті:
```bash
git show --stat --oneline HEAD
```
```text
8695fa7 (HEAD -> lr3) ЛР3: завдання 2
 .venv/pyvenv.cfg                      |   1 +
 lr3/__pycache__/lr3_1.cpython-312.pyc | Bin 0 -> 323 bytes
 lr3/lr3_2.py                          |   6 ++++++
 lr3/vymiry.bin                        | Bin 0 -> 209715200 bytes
 4 files changed, 7 insertions(+)
```
`Bin 0 -> 209715200 bytes` - двійковий файл на 200 МБ. Лікуємо:
```bash
printf '.venv/\n__pycache__/\n*.pyc\n*.bin\n' > .gitignore
git rm -r --cached .venv lr3/__pycache__ lr3/vymiry.bin
git add .gitignore
git status --short
git commit --amend --no-edit
git show --stat --oneline HEAD
```
```text
rm '.venv/pyvenv.cfg'
rm 'lr3/__pycache__/lr3_1.cpython-312.pyc'
rm 'lr3/vymiry.bin'
A  .gitignore
D  .venv/pyvenv.cfg
D  lr3/__pycache__/lr3_1.cpython-312.pyc
D  lr3/vymiry.bin
[lr3 495ec62] ЛР3: завдання 2
 Date: Wed Nov 18 10:10:00 2026 +0000
 2 files changed, 10 insertions(+)
 create mode 100644 .gitignore
 create mode 100644 lr3/lr3_2.py
495ec62 (HEAD -> lr3) ЛР3: завдання 2
 .gitignore   | 4 ++++
 lr3/lr3_2.py | 6 ++++++
 2 files changed, 10 insertions(+)
```
`D` у `git status --short` - «видалено з git» (файли на диску на місці). `--amend --no-edit` замінив коміт новим
(інший хеш `495ec62`) з тим самим повідомленням. Тепер `*.bin` ігнорується - великі дані вимірювань у git не кладуть.

**Чому `--amend`, а не новий коміт «Прибрав сміття».** Новий коміт прибрав би файл лише з **наступних** знімків, а коміт
`8695fa7` з 200 МБ лишився б в історії - і `git push` повіз би його. GitHub блокує пуш файлів понад 100 МіБ, тож пуш
відхилили б, хоч у теці файла вже «нема». `--amend` до push - коміт з 200 МБ просто не потрапляє в гілку.
</details>

**Аварія 2 (відтвори):** завдання 3, коміт, потім чернетка, яку хочеш викинути, - і помилкова команда.

> **Увага.** `git reset --hard` затирає незакомічене в робочій теці. Тут ми робимо це навмисно, у тренажері.

```bash
printf 'def korin(x):\n    """\n    >>> korin(9)\n    3.0\n    """\n    return x ** 0.5\n' > lr3/lr3_3.py
git add lr3/lr3_3.py
git commit -m "ЛР3: завдання 3"
printf '# чернетка\n' >> lr3/lr3_3.py
git reset --hard HEAD~1
```
```text
HEAD is now at 495ec62 ЛР3: завдання 2
```

**Що треба отримати після аварії 2:** коміт «ЛР3: завдання 3» знову в гілці, `lr3/lr3_3.py` на місці, doctest мовчить.

<details markdown="1"><summary>Підказка А2</summary>

Коміт не зник - на нього просто більше не показує гілка. Журнал усіх рухів HEAD - `git reflog` (урок 12).
</details>

<details markdown="1"><summary>Розвʼязок А2</summary>

```bash
git log --oneline -3
ls lr3
git reflog -5
```
```text
495ec62 (HEAD -> lr3) ЛР3: завдання 2
9e9e199 ЛР3: завдання 1
bd2ae9b (origin/main, main) Початок
lr3_1.py  lr3_2.py  __pycache__  vymiry.bin
495ec62 (HEAD -> lr3) HEAD@{0}: reset: moving to HEAD~1
8ca7b84 HEAD@{1}: commit: ЛР3: завдання 3
495ec62 (HEAD -> lr3) HEAD@{2}: commit (amend): ЛР3: завдання 2
8695fa7 HEAD@{3}: commit: ЛР3: завдання 2
9e9e199 HEAD@{4}: commit: ЛР3: завдання 1
```
(`ls` у терміналі друкує назви в рядок і сортує за правилами мови системи: так в англійській і українській; порядок
і колонки в тебе можуть трохи відрізнятись.) Зверни увагу: `lr3_3.py` зник, а `__pycache__` і `vymiry.bin` - ні. `reset --hard` не чіпає файли, яких нема в git
(ігноровані й нові). У reflog видно всю історію аварій, навіть `commit (amend)` і старий коміт `8695fa7` з 200 МБ.
Потрібний рядок - `HEAD@{1}: commit: ЛР3: завдання 3`:
```bash
git reset --hard HEAD@{1}
python3 -m doctest lr3/lr3_3.py
```
```text
HEAD is now at 8ca7b84 ЛР3: завдання 3
```
Чернетки `# чернетка` нема - її ми і хотіли викинути. **Як треба було одразу:** незакомічену правку скасовує
`git restore` (коміти не чіпає):
```bash
git restore lr3/lr3_3.py
```
</details>

**Аварія 3 (відтвори):** токен прямо в коді, коміт, push. (Токен вигаданий, і push іде в тренажер.)
```bash
printf 'TOKEN = "ghp_vyhadanyi_dlia_trenazhera"\n' > lr3/nalashtuvannia.py
git add lr3/nalashtuvannia.py
git commit -m "ЛР3: налаштування"
git push -u origin lr3
```
```text
To /home/.../trenazher/github/univer-labs.git
 * [new branch]      lr3 -> lr3
branch 'lr3' set up to track 'origin/lr3'.
```

**Що треба отримати після аварії 3:** (1) токен **відкликано** на сайті - це головне; (2) у файлах гілки токена нема,
програма бере його зі змінної середовища; (3) ти сам переконався, що в історії він лишився, і розумієш, чому це не
лікується `revert`.

<details markdown="1"><summary>Підказка А3</summary>

Що потрапило на GitHub - те вже могли скопіювати (клони, форки, кеш). Тому спершу роблять токен **марним**, а вже
потім прибирають з коду. Перевір: чи бачить `git log -S текст` коміт з токеном після `git revert`?
</details>

<details markdown="1"><summary>Розвʼязок А3</summary>

**Крок 1 - одразу, ще до git: відклич токен.** Документація GitHub: «as a first step you need to revoke and/or rotate
that secret» (docs, «Removing sensitive data from a repository»). Де це:
```text
аватарка → Settings → (ліве меню, внизу) Developer settings → Personal access tokens
  → Fine-grained tokens або Tokens (classic) → біля токена кнопка Delete
```
(docs, «Managing your personal access tokens»: «Treat your access tokens like passwords».) Потрібен новий - зроби новий
і **не пиши його в код**. Якщо в коді був пароль від пошти чи університетського акаунта - негайно зміни пароль там.

**Крок 2. Прибрати з коду (revert) і переконатись, що історія памʼятає.**
```bash
git revert --no-edit HEAD
git push
git log --oneline -S ghp_vyhadanyi_dlia_trenazhera
git show HEAD~1:lr3/nalashtuvannia.py
git -C ~/trenazher/github/univer-labs.git log --oneline -S ghp_vyhadanyi_dlia_trenazhera lr3
```
```text
[lr3 062b16b] Revert "ЛР3: налаштування"
 Date: Wed Nov 18 10:15:00 2026 +0000
 1 file changed, 1 deletion(-)
 delete mode 100644 lr3/nalashtuvannia.py
To /home/.../trenazher/github/univer-labs.git
   47f17ef..062b16b  lr3 -> lr3
062b16b (HEAD -> lr3, origin/lr3) Revert "ЛР3: налаштування"
47f17ef ЛР3: налаштування
TOKEN = "ghp_vyhadanyi_dlia_trenazhera"
062b16b (lr3) Revert "ЛР3: налаштування"
47f17ef ЛР3: налаштування
```
`git log -S текст` - коміти, де цей текст зʼявився або зник. Обидва коміти на місці, і `git show HEAD~1:файл` досі
друкує токен. `git -C тека` - виконати git так, ніби ти в тій теці: тут - у «GitHub». Там те саме. **Revert прибирає
токен з файлів, але не з історії** - будь-хто з доступом до репо знайде його за хвилину.

**Крок 3. Правильна версія: токен зі змінної середовища.**
```bash
printf 'import os\n\nTOKEN = os.environ.get("LAB_TOKEN", "")\n' > lr3/nalashtuvannia.py
printf '.env\n' >> .gitignore
git add lr3/nalashtuvannia.py .gitignore
git commit -m "ЛР3: токен лише зі змінної середовища"
git push
```
`os.environ.get("LAB_TOKEN", "")` читає змінну середовища `LAB_TOKEN` (порожньо, якщо її нема). Сам токен тримають
поза git: у змінній (`export LAB_TOKEN=...` у терміналі) або у файлі `.env`, який тепер в `.gitignore`.

**Чому не «стерти історію» і `git push --force`.** Переписати історію можна (docs радять програму `git-filter-repo`),
але docs самі перелічують, де секрет лишиться: «You cannot remove sensitive data from other users' clones of your
repository», у форках, у PR, у кешованих сторінках GitHub за хешем коміту. А `--force` у спільну гілку ще й знищить
чужі коміти (урок 12). Тому: відкликати токен - обовʼязково і першим; переписувати історію - лише у своєму репо,
лише разом з відкликанням, і це вже поза курсом.

**Якби помітив до push** - було б як в аварії 1: виправив файл, `git add`, `git commit --amend --no-edit`, і токен
ніколи не покинув би ноутбук.
</details>

**Що перевірити в кінці задачі 2:**
```bash
git status --short
git ls-files
git -C ~/trenazher/github/univer-labs.git ls-tree -r --name-only lr3
```
`git status --short` - порожньо. Обидва списки однакові (у тебе і на «GitHub»):
```text
.gitignore
README.md
lr3/lr3_1.py
lr3/lr3_2.py
lr3/lr3_3.py
lr3/nalashtuvannia.py
```
Ні `.venv`, ні `__pycache__`, ні `vymiry.bin`, а `cat .gitignore` - пʼять правил: `.venv/`, `__pycache__/`, `*.pyc`,
`*.bin`, `.env`. І токен відкликано (у тренажері - уявно, у житті - по-справжньому).

**Типові пастки:**
- **«Прибрав» 200 МБ новим комітом, а не `--amend`.** Файл лишився в старому коміті, push його повезе, GitHub відхилить
  (понад 100 МіБ). Поки не запушив - `--amend` (якщо великий файл не в останньому коміті - це вже переписування історії, тоді клич
  на допомогу когось досвідченого).
- **`git rm -r .venv` без `--cached`** - видалить venv і з диска. Venv можна відновити (`python3 -m venv`), але навіщо.
- **`git reset --hard` замість `git restore`.** `restore файл` - скасувати правку у файлі; `reset --hard HEAD~1` - викинути
  цілий коміт. Незакомічене після `--hard` не врятує навіть reflog.
- **Revert «прибрав» токен - і на цьому все.** Ні: поки токен не відкликано, він робочий, а в історії його видно.

---

### Задача 3. Здача ЛР з тегом і архівом (20-30 хв)

**Умова.** ЛР3 готова в гілці `lr3` (продовжуємо тренажер із задачі 2). Завтра здача. Вимоги викладача: zip-архів,
у ньому тека з назвою «прізвище, імʼя, група, рік» і **лише файли ЛР3**; плюс посилання на здану версію в репо
(точний формат назви уточни на парі, див. «Лаби в git», «Як показати викладачу»).

**Що треба отримати (готово, коли):**
- `lr3` злита в `main`, усе запушено;
- на «GitHub» є анотований тег `lr3-zdano` на коміті, який ти здаєш;
- `~/trenazher/zdacha/lr3.zip` - тека `Прізвище_Імʼя_Група_2026/lr3/...`, без `.venv`, `__pycache__`, `.bin` і без токена;
- архів, розпакований «як у викладача», проходить doctest;
- ти знаєш, яке посилання дати викладачу.

<details markdown="1"><summary>Підказка 1</summary>

Порядок: чиста робоча тека і doctest → злиття в `main` → тег → push тегу (звичайний push тегів не везе, урок 14) → архів
**з тегу**, а не з теки на диску.
</details>

<details markdown="1"><summary>Підказка 2</summary>

`git archive --format=zip --prefix=ТЕКА/ -o ФАЙЛ.zip ТЕГ lr3` - останнє слово обмежує архів текою `lr3`.
Переглянути архів без unzip: `python3 -m zipfile -l`, розпакувати: `python3 -m zipfile -e`.
</details>

<details markdown="1"><summary>Повний розвʼязок</summary>

**Крок 1. Перевірити, що здаєш.**
```bash
cd ~/trenazher/univer-labs
git switch lr3
git status --short
python3 -m doctest lr3/lr3_1.py lr3/lr3_2.py lr3/lr3_3.py
git push
```
`git status --short` порожній (усе закомічено), doctest трьох файлів мовчить, `git push` каже `Everything up-to-date`.
Якщо status щось показує - спершу коміт: в архів потрапить лише закомічене.

**Крок 2. Злити в main, тег, push.**
```bash
git switch main
git pull
git merge lr3
git push
git tag -a lr3-zdano -m "ЛР3 здано"
git push origin lr3-zdano
git ls-remote --tags origin
```
```text
Updating bd2ae9b..0f74542
Fast-forward
 .gitignore            | 5 +++++
 lr3/lr3_1.py          | 6 ++++++
 lr3/lr3_2.py          | 6 ++++++
 lr3/lr3_3.py          | 6 ++++++
 lr3/nalashtuvannia.py | 3 +++
 5 files changed, 26 insertions(+)
 ...
To /home/.../trenazher/github/univer-labs.git
   bd2ae9b..0f74542  main -> main
To /home/.../trenazher/github/univer-labs.git
 * [new tag]         lr3-zdano -> lr3-zdano
b4a0a7cf5c9f62057ec147c860fcf3b3ec932f2d	refs/tags/lr3-zdano
0f745421a1a3e59b1635ee449ae298b6f2d3aef8	refs/tags/lr3-zdano^{}
```
`git ls-remote --tags origin` питає сам «GitHub», які там теги. Два рядки, бо тег анотований: перший хеш - сам тег
(з автором і повідомленням), рядок з `^{}` - коміт, на який він показує. Він має збігатися з `main` (`0f74542...`).

**Крок 3. Архів з тегу і перевірка вмісту.**
```bash
mkdir -p ~/trenazher/zdacha
git archive --format=zip --prefix=Прізвище_Імʼя_Група_2026/ -o ~/trenazher/zdacha/lr3.zip lr3-zdano lr3
python3 -m zipfile -l ~/trenazher/zdacha/lr3.zip
python3 -m zipfile -l ~/trenazher/zdacha/lr3.zip | grep -c -E '\.venv|__pycache__|\.bin'
```
```text
File Name                                             Modified             Size
Прізвище_Імʼя_Група_2026/                    2026-11-18 10:16:00            0
Прізвище_Імʼя_Група_2026/lr3/                2026-11-18 10:16:00            0
Прізвище_Імʼя_Група_2026/lr3/lr3_1.py        2026-11-18 10:16:00           74
Прізвище_Імʼя_Група_2026/lr3/lr3_2.py        2026-11-18 10:16:00           67
Прізвище_Імʼя_Група_2026/lr3/lr3_3.py        2026-11-18 10:16:00           75
Прізвище_Імʼя_Група_2026/lr3/nalashtuvannia.py 2026-11-18 10:16:00           51
0
```
`grep -c` рахує рядки, що збіглися з будь-яким із трьох слів (`-E` - «або» через `|`, `\.` - справжня крапка). `0` -
сміття нема, хоч на диску `.venv/`, `lr3/__pycache__/` і `lr3/vymiry.bin` лежать. Час у колонці Modified - час коміту,
а не момент створення архіву.

**Крок 4. Розпакувати як викладач і запустити.**
```bash
python3 -m zipfile -e ~/trenazher/zdacha/lr3.zip ~/trenazher/rozpakovano
cd ~/trenazher/rozpakovano/Прізвище_Імʼя_Група_2026
python3 -m doctest lr3/lr3_1.py lr3/lr3_2.py lr3/lr3_3.py
grep -r ghp_ .
```
doctest мовчить, `grep` нічого не знаходить: в архіві лише файли зі знімка під тегом, а не вся історія, тож старого
токена там нема.

**Крок 5. Посилання для викладача.** На справжньому GitHub (у `~/univer/labs`) - тека ЛР3 саме в зданій версії:
```text
https://github.com/Evge14n/univer-labs/tree/lr3-zdano/lr3
```
`univer-labs` приватний, тож посилання відкриється лише тому, кого ти додав у Collaborators («Лаби в git»). Повідомлення
викладачу, наприклад: «ЛР3 у вкладенні (lr3.zip). Здана версія в репо: посилання вище, тег lr3-zdano.»
</details>

**Що перевірити в кінці:**
- `git tag -n` → `lr3-zdano       ЛР3 здано`;
- `git ls-remote --tags origin` показує `refs/tags/lr3-zdano` - тег на «GitHub», а не лише в тебе;
- у `python3 -m zipfile -l` усі шляхи починаються з `Прізвище_Імʼя_Група_2026/lr3/`, `grep -c` дає `0`;
- doctest у розпакованій теці мовчить.

**Типові пастки:**
- **Забув скісну риску в `--prefix`.** `--prefix=Прізвище_Імʼя_Група_2026` (без `/`) - тека зливається з назвою:
  ```text
  Прізвище_Імʼя_Група_2026lr3/                 2026-11-18 10:16:00            0
  Прізвище_Імʼя_Група_2026lr3/lr3_1.py         2026-11-18 10:16:00           74
  ```
- **Тег уже є** (поставив раніше «на пробу»):
  ```text
  fatal: tag 'lr3-zdano' already exists
  ```
  Якщо тег ще **не** пушив - `git tag -d lr3-zdano` і постав знову. Якщо вже на GitHub і викладач міг його бачити -
  не пересувай, постав новий `lr3-zdano-2` з поясненням у `-m`.
- **Помилився в назві теки в кінці команди** (`lr4` замість `lr3`): `fatal: pathspec 'lr4' did not match any files`.
- **Правка після тегу.** `git archive` бере файли з тегу, тож незакомічене і закомічене після тегу в архів не потрапить.
  Це добре (архів = здана версія), але якщо справді щось виправив до здачі - коміт, потім тег.
- **`git push` без імені тегу** тег не везе (урок 14). Перевіряй `git ls-remote --tags origin`.

---

### Задача 4. Свій сайт-портфоліо на Pages за 30 хв (30 хв)

**Умова.** На стажування просять «посилання на GitHub або сайт». Зроби просту сторінку про себе в окремому
**публічному** репо `portfolio`, увімкни Pages, заведи issue з планом сторінки і закрий його комітом.

**Що треба отримати (готово, коли):**
- `https://evge14n.github.io/portfolio/` відкривається (у терміналі `curl` дає `200`);
- на сторінці є розділи «Навчання», «Проєкти», «Контакти»;
- issue #1 «План сторінки» закрито комітом з `Closes #1`;
- `git status` чистий, усе запушено.

<details markdown="1"><summary>Підказка 1</summary>

Pages на безкоштовному плані - лише з **публічного** репо (урок 15). Тому `portfolio` - окремий публічний репо, а не
`univer-labs`. Все, що кладеш туди, бачить увесь інтернет.
</details>

<details markdown="1"><summary>Підказка 2</summary>

Pages шукає `index.html` **у корені** вибраної гілки, з маленької літери. `git ls-files` покаже, де він лежить.
Issue закривається, коли коміт з `Closes #1` потрапляє в `main` на GitHub (урок 10).
</details>

<details markdown="1"><summary>Повний розвʼязок</summary>

**Крок 1. Репо на сайті.** Справа вгорі **+** → **New repository** → Repository name: `portfolio` → **Public** →
**Add a README file** → **Create repository**. Або з терміналу, з домашньої теки (gh, урок 16):
```bash
gh repo create portfolio --public --add-readme --clone
```

**Крок 2. Перша версія сторінки.**
```bash
git clone git@github.com:Evge14n/portfolio.git ~/portfolio
cd ~/portfolio
nano index.html
xdg-open index.html
git status --short
git add index.html
git commit -m "Сторінка-портфоліо: перша версія"
git push
git ls-files
```
(Якщо репо створив через gh з `--clone`, `git clone` пропусти.) Вміст `index.html` (12 рядків):
```text
<!DOCTYPE html>
<html lang="uk">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Імʼя - портфоліо</title>
</head>
<body>
  <h1>Імʼя</h1>
  <p>Студент 1 курсу. Вчу Python, git і Linux.</p>
</body>
</html>
```
`<meta charset="utf-8">` - щоб кирилиця не стала «кракозябрами», `viewport` - щоб на телефоні не було дрібно.
`xdg-open` відкриває файл у браузері за замовчуванням - подивись, перш ніж комітити.
```text
?? index.html
[main c39c39c] Сторінка-портфоліо: перша версія
 1 file changed, 12 insertions(+)
 create mode 100644 index.html
To github.com:Evge14n/portfolio.git
   c835b89..c39c39c  main -> main
README.md
index.html
```
`index.html` без теки перед назвою - у корені, як треба.

**Крок 3. Увімкнути Pages** (урок 15):
```text
Settings → Pages (ліве меню) → Build and deployment → Source: Deploy from a branch
  → Branch: main    тека: / (root)    → Save
```
Хвилину-дві чекаєш (вкладка **Actions** → «pages build and deployment», зелена галочка), потім:
```bash
curl -s -o /dev/null -w '%{http_code}\n' https://evge14n.github.io/portfolio/
```
`404` - ще не готово або Pages не ввімкнено; `200` - сайт живий. Відкрий адресу в браузері.

**Крок 4. Issue з планом.** На сайті: вкладка **Issues** → **New issue** → Title «План сторінки», опис «Розділи:
навчання, проєкти, контакти» → **Create**. Або:
```bash
gh issue create --title "План сторінки" --body "Розділи: навчання, проєкти, контакти"
```
У новому репо це буде issue **#1**.

**Крок 5. Друга версія і закриття issue.** У nano перед рядком `</body>` додай 8 рядків:
```text
  <h2>Навчання</h2>
  <p>Фізичний факультет ЛНУ, 1 курс.</p>
  <h2>Проєкти</h2>
  <ul>
    <li><a href="https://evge14n.github.io/uni-prep/">uni-prep</a> - сайт для підготовки до сесії</li>
  </ul>
  <h2>Контакти</h2>
  <p><a href="https://github.com/Evge14n">github.com/Evge14n</a></p>
```
```bash
nano index.html
git diff --stat
git commit -am "Додай розділи Навчання, Проєкти, Контакти" -m "Closes #1"
git log -1 --format=%B
git push
git log --oneline --grep="Closes #1"
```
```text
 index.html | 8 ++++++++
 1 file changed, 8 insertions(+)
[main 3425720] Додай розділи Навчання, Проєкти, Контакти
 1 file changed, 8 insertions(+)
Додай розділи Навчання, Проєкти, Контакти

Closes #1
To github.com:Evge14n/portfolio.git
   c39c39c..3425720  main -> main
3425720 (HEAD -> main, origin/main, origin/HEAD) Додай розділи Навчання, Проєкти, Контакти
```
Друге `-m` - тіло коміту, там і стоїть `Closes #1`. Коміт пішов прямо в `main`, тож GitHub закриє issue сам.
Перевір:
```bash
gh issue view 1
gh issue list --state closed
```
За хвилину онови сторінку в браузері (Ctrl+Shift+R - без старої копії з кешу) - мають зʼявитись три розділи.
</details>

**Що перевірити в кінці:**
- `git ls-files` → `README.md` і `index.html` (у корені);
- `git log --oneline` - три коміти: `Initial commit`, перша версія, другі розділи;
- `git status` → `Your branch is up to date with 'origin/main'.` і `nothing to commit, working tree clean`;
- `curl -s -o /dev/null -w '%{http_code}\n' https://evge14n.github.io/portfolio/` → `200`;
- issue #1 на сайті позначене Closed, і в ньому є посилання на коміт.

**Типові пастки:**
- **Репо приватний** - пункту Pages нема або він просить платний план. На Free - лише публічний.
- **`Index.html` з великої або `site/index.html`.** Для Linux і для Pages `Index.html` - **інший** файл (`git status --short`
  покаже його окремо: `?? Index.html`), а `index.html` у теці Pages у корені не знайде → 404.
- **`Closes #1` у коміті в іншій гілці** - issue не закриється, доки гілку не зіллють у `main` (урок 10).
- **Посилання на приватний `univer-labs`** на публічній сторінці - для всіх, крім тебе, воно не відкриється (не перевірено
  дослівно, що саме бачать: GitHub не показує чужим приватні репо). Не став таких посилань.
- **Особисте на сторінці.** Pages бачать усі: без телефону, адреси, номера залікової. Контакт - профіль GitHub.
- **Одразу після Save - 404.** Це не помилка: перша публікація триває хвилину-дві, docs кажуть «up to 10 minutes».

---

**Що далі.** Задачі 1 і 3 - це і є твій щотижневий цикл з лабами («Лаби в git»). Задачу 2 корисно повторити через тиждень з
нуля, не підглядаючи: `rm -rf ~/trenazher` прибирає тренажер повністю (команда видаляє лише цю теку, лаби не чіпає).

### Джерела

- docs.github.com, «Removing sensitive data from a repository»:
  https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/removing-sensitive-data-from-a-repository
  (відкрито 18.11.2026)
- docs.github.com, «Managing your personal access tokens»:
  https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens
  (відкрито 18.11.2026)
- docs.github.com, «Resolving a merge conflict on GitHub»:
  https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/addressing-merge-conflicts/resolving-a-merge-conflict-on-github
  (відкрито 18.11.2026)
- git-scm.com/docs: git-archive, git-reflog, git-revert, git-rm, git-ls-remote, git-log (`-S`) - https://git-scm.com/docs
  (відкрито 18.11.2026)
- Python, модуль zipfile (командний рядок `-l`, `-e`): https://docs.python.org/3/library/zipfile.html (відкрито 18.11.2026)
- Уроки курсу: 06 (.gitignore), 08 (конфлікт), 10 (Closes #N), 11 (PR), 12 (reflog, revert), 14 (теги), 15 (Pages), 16 (gh);
  «Лаби в git - univer-labs покроково».

## Іспит-самоперевірка: 20 питань

**Навіщо:** перевірити, чи ти **розумієш** git, а не памʼятаєш команди. Рівень - як випускний іспит і як технічна
співбесіда в сильній команді: майже в кожному питанні є «пастка», яку видно лише тому, хто розуміє, що git робить усередині.

**Як складати:**
- 20 питань, час - 60-90 хв, без підглядання в уроки і без терміналу. Відповідай письмово, у зошит або в nano.
- Де питають «що виведе» - пиши вивід якомога точніше, а потім **чому** саме так. «Чому» важить стільки ж, скільки вивід.
- Потім звір з розділом «Відповіді» і порахуй бал (вкінці файлу). Мета - **90 і більше з 100**.
- Після звірки перевір себе в терміналі: майже кожну відповідь можна відтворити в пісочниці `~/git-pisochnytsia`.

Умови для всіх питань: git налаштований як в Уроці 02 (`init.defaultBranch main`, `pull.rebase false`, `core.quotepath false`),
вивід англійський. «GitHub» - твій репо на GitHub, `origin` - він же. Хеші комітів у тебе будуть інші.

Відповіді, позначені «Перевірено запуском», звірені справжнім git 2.43.0 (як на Linux Mint 22.3) у файлі
`_перевірка/ispyt.sh`: 17 з 20 відповідей.

### Питання

1. (Що виведе) Що покажуть `git show HEAD:lr1.py`, `cat lr1.py` і `git status --short` після такого сценарію? Поясни, де яка версія файлу лежить.

```text
git init -q ~/q01 && cd ~/q01
printf 'a = 1\n' > lr1.py
git add lr1.py
git commit -q -m "a = 1"
printf 'a = 2\n' > lr1.py
git add lr1.py
printf 'a = 3\n' > lr1.py
git commit -q -m "a = 2?"
```

2. (Що буде з історією) Скільки комітів покаже `git rev-list --count main` у кінці, скільки **батьків** у верхнього коміту `main` і яке в нього повідомлення? Яке з двох злиттів напише `Fast-forward`?

```text
git init -q ~/q02 && cd ~/q02
printf 'A\n' > a.txt; git add a.txt; git commit -q -m "A"
git switch -q -c lr2
printf 'B\n' > b.txt; git add b.txt; git commit -q -m "B"
git switch -q main
git merge lr2
git switch -q -c lr3
printf 'C\n' > c.txt; git add c.txt; git commit -q -m "C"
git switch -q main
printf 'D\n' > d.txt; git add d.txt; git commit -q -m "D"
git merge lr3
```

3. (Що виведе) Коміт уже на GitHub. Ти ставиш два теги і пушиш. Що напише перший `git push`? Які теги будуть на GitHub після `git push --follow-tags`?

```text
git tag lr1-chernetka
git tag -a lr1-zdano -m "ЛР1 здано"
git push
git push --follow-tags
```

4. (Що виведе) Що буде у файлі після першого `pop`, що покаже `git stash list`, і що станеться при **другому** `git stash pop` одразу після першого?

```text
printf 'v0\n' > f.txt; git add f.txt; git commit -q -m "v0"
printf 'v1\n' > f.txt
git stash
printf 'v2\n' > f.txt
git stash
git stash pop
git stash list
git stash pop
```

5. (Що буде з історією) Репо склоновано з GitHub (там один коміт `Initial commit` з README). Скасовуємо **середній** коміт. Що покаже `ls`, скільки комітів стане, і що скаже другий рядок `git status`?

```text
printf 'a\n' > a.txt; git add a.txt; git commit -q -m "a"
printf 'b\n' > b.txt; git add b.txt; git commit -q -m "b"
printf 'c\n' > c.txt; git add c.txt; git commit -q -m "c"
git push -q
git revert --no-edit HEAD~1
```

6. (Що виведе) У тебе клон `~/q06`, все синхронно. Одногрупник зі свого клону пушить у `main` новий коміт «Від одногрупника» з файлом `druh.txt`. Ти в `~/q06` пишеш `git status`, потім `git fetch`, потім знову `git status`. Що скажуть обидва `git status` (другий рядок) і чи зʼявиться `druh.txt` у твоїй теці після `fetch`?

7. (Що зробиш) У `main` три коміти: «ЛР5: завдання 1», «ЛР5: завдання 2», «ЛР5: завдання 3». Ти хотів скасувати лише незакомічену правку, а набрав `git reset --hard HEAD~2`. `git log` показує лише «ЛР5: завдання 1». Коміти ще не пушив. Як повернути все? Що побачиш у `git reflog -3`? Яке є друге, ще безпечніше рішення?

8. (Що зробиш) Твій PR `lr3 → main` на GitHub пише «This branch has conflicts that must be resolved»: поки ти робив `lr3`, одногрупник змінив у `main` той самий рядок `g = 9.8` (у тебе `g = 9.81`, у нього `g = 9.80665`). Які команди в терміналі, щоб PR став без конфлікту? Чи треба закривати PR і відкривати новий?

9. (Що зробиш) Ти запушив у **публічний** репо `config.py` з токеном, потім зробив `git rm config.py`, дописав `config.py` у `.gitignore`, закомітив і запушив. Токена в репо вже нема? Що треба зробити **першим** і чому саме це?

10. (Що зробиш) Ти закомітив `lr2.py` у свій `main`, а за цей час одногрупник запушив у `main` свій коміт. `git push` відмовив. Який буде текст у квадратних дужках `[rejected]`, які команди далі, і скільки комітів стане в `main` на GitHub (якщо спершу там були `Initial commit` і коміт одногрупника)? Чому не `git push --force`?

11. (Що зробиш) Ти зробив `git checkout lr1-zdano` (тег здачі ЛР1), виправив опечатку, `git commit -am "Правка на тезі"`, потім `git switch main`. Що це був за стан, що напише git при `switch`, і як врятувати коміт? Як треба було зробити від початку?

12. (Поясни, чому) Навіщо git **три** зони (робоча тека, індекс, репозиторій), а не дві («файли» і «коміти»)? Наведи приклад з лаб, де без індексу було б погано.

13. (Поясни, чому) Коли `git merge` робить fast-forward, а коли merge-коміт? Чому кнопка GitHub «Create a merge commit» робить merge-коміт **навіть** коли можна було перемотати, і що зробить `git merge --ff-only`, якщо гілки розійшлися?

14. (Поясни, чому) Чому після push помилку скасовують `git revert`, а не `git reset`? Ти запушив у спільний `main` поганий коміт, зробив `git reset --hard HEAD~1` і `git push`. Що напише цей push? Потім - **між** цим push і наступною командою - одногрупник запушив у `main` свій коміт, а ти пишеш `git push --force-with-lease`. Що буде? І що зміниться, якщо перед `--force-with-lease` зробити `git fetch`?

15. (Поясни, чому) Чому вхід у GitHub через SSH-ключ безпечніший, ніж через пароль? Що буде, якщо хтось побачить твій `id_ed25519.pub`, а що - якщо `id_ed25519`?

16. (GitHub) Одногрупник відкрив PR у твій `univer-labs`, ти рецензент і знайшов помилку в рядку. Яку з трьох дій рев'ю обереш і де? Він виправив і запушив у ту саму гілку: що буде з PR? І чому він сам не може натиснути Approve?

17. (GitHub) Ти хочеш опублікувати сторінку з фізики через GitHub Pages з репо `univer-labs` (приватний, план Free). Чому не вийде і що робити замість цього? Яка буде адреса сайту?

18. (GitHub) Ти робиш `git commit -m "Опиши пісочницю в README" -m "Closes #3"` у гілці `lr3` і пушиш `lr3`. Коли закриється issue #3? Що покаже `git log --oneline` для цього коміту, і як знайти його пізніше?

19. (Напиши команди) Ти на гілці `lr3`, усі завдання ЛР3 закомічені і запушені (`git push -u origin lr3` уже був). Напиши повний цикл здачі без PR: злити в `main`, відправити на GitHub, поставити тег здачі, відправити тег, прибрати гілку тут і на GitHub, зробити zip для викладача з теки `lr3` саме з тегу.

20. (Напиши команди) Почни ЛР4 правильно: свіжий `main`, нова гілка, заготовки викладача в `lr4/`, перший коміт, гілка на GitHub з відстеженням. Чим перевіриш, що гілка стежить за `origin/lr4`?

<details markdown="1"><summary>Відповіді</summary>

1. **Відповідь:** `git show HEAD:lr1.py` → `a = 2`; `cat lr1.py` → `a = 3`; `git status --short` → ` M lr1.py`.

   **Чому:** `git add` знімає копію файлу **в індекс** у момент `add`. Друга правка (`a = 3`) сталася після `add`, тож
   лишилась лише в робочій теці. `git commit` без `-a` бере саме індекс. Після коміту індекс = коміт (`git diff --staged`
   порожній), а робоча тека відрізняється (` M` - пробіл зліва: в індексі нічого, `M` справа: змінено в теці;
   `git diff` покаже `-a = 2` / `+a = 3`). Пастка: багато хто думає, що коміт бере файл «як він зараз на диску».

   **Звідки:** Урок 01 (три зони, `MM`), Урок 04. Pro Git 1.3 «What is Git?»:
   https://git-scm.com/book/en/v2/Getting-Started-What-is-Git%3F; git status (короткий формат): https://git-scm.com/docs/git-status

   **Перевірено запуском:** ispyt.sh, питання 1.

2. **Відповідь:** перше злиття (`git merge lr2`) - `Fast-forward`; друге - `Merge made by the 'ort' strategy.`
   У кінці `git rev-list --count main` = `5` (A, B, C, D і коміт злиття), у верхнього коміту **2** батьки (D і C),
   повідомлення `Merge branch 'lr3'`.

   **Чому:** коли зливали `lr2`, `main` не рухався - git просто пересунув ярлик `main` на B, нового коміту нема.
   Коли зливали `lr3`, обидві гілки пішли вперед (C у `lr3`, D у `main`), тож потрібен новий коміт з двома батьками.
   Коміт B не дублюється: гілка - лише вказівник, коміти спільні.

   **Звідки:** Урок 07 (два види злиття). Pro Git 3.2 «Basic Branching and Merging»:
   https://git-scm.com/book/en/v2/Git-Branching-Basic-Branching-and-Merging

   **Перевірено запуском:** ispyt.sh, питання 2.

3. **Відповідь:** перший `git push` пише лише

   ```text
   Everything up-to-date
   ```

   і тегів на GitHub **нема**. `git push --follow-tags` відправляє тільки `lr1-zdano`:

   ```text
    * [new tag]         lr1-zdano -> lr1-zdano
   ```

   `lr1-chernetka` лишається лише в тебе (його треба `git push origin lr1-chernetka`).

   **Чому:** звичайний `push` везе гілку, а нових комітів у ній нема. `--follow-tags` бере лише **анотовані** теги
   (обʼєкт типу `tag`: автор, дата, повідомлення), які стоять на комітах, що їдуть або вже є на GitHub. Легкий тег -
   просто назва коміту, `--follow-tags` його не бере.

   **Звідки:** Урок 14. git push (`--follow-tags`): https://git-scm.com/docs/git-push; Pro Git 2.6 «Tagging»:
   https://git-scm.com/book/en/v2/Git-Basics-Tagging

   **Перевірено запуском:** ispyt.sh, питання 3.

4. **Відповідь:** після першого `pop` у файлі `v2`. `git stash list`:

   ```text
   stash@{0}: WIP on main: ХЕШ v0
   ```

   Другий `pop` **відмовить** (код 1), у файлі лишиться `v2`, схованка з `v1` не видалиться:

   ```text
   error: Your local changes to the following files would be overwritten by merge:
   	f.txt
   Please commit your changes or stash them before you merge.
   Aborting
   ...
   The stash entry is kept in case you need it again.
   ```

   **Чому:** stash - це **стос**: остання схована (`v2`) стає `stash@{0}` і виходить першою. Після `pop` вона зникає,
   а старша (`v1`) зсувається на `stash@{0}`. Другий `pop` мав би записати `v1` поверх незакоміченого `v2` - git не
   затирає незбережене, тому зупиняється і лишає схованку. (Цікаво: git 2.43 між цими рядками ще друкує весь
   `git status`.) Вихід: закомітити або сховати `v2`, потім `pop`.

   **Звідки:** Урок 13. Pro Git 7.3 «Stashing and Cleaning»: https://git-scm.com/book/en/v2/Git-Tools-Stashing-and-Cleaning;
   git stash: https://git-scm.com/docs/git-stash

   **Перевірено запуском:** ispyt.sh, питання 4.

5. **Відповідь:** `ls` → `README.md`, `a.txt`, `c.txt` (зник лише `b.txt`). Комітів **5**, `git log --oneline`:

   ```text
   ХЕШ (HEAD -> main) Revert "b"
   ХЕШ (origin/main, origin/HEAD) c
   ХЕШ b
   ХЕШ a
   ХЕШ Initial commit
   ```

   Другий рядок `git status`: `Your branch is ahead of 'origin/main' by 1 commit.` (видно і з ярликів: `main` на
   `Revert "b"`, а `origin/main` - ще на `c`).

   **Чому:** `revert` скасовує **зміни одного коміту** (тут - «додав b.txt»), а не «все після нього», і робить для цього
   новий коміт. Коміти `b` і `c` лишаються в історії. Новий коміт ще не на GitHub, тому `ahead 1` - його треба `git push`.
   Пастка: плутати з `reset --hard HEAD~1`, який прибрав би **і** `b`, **і** `c`.

   **Звідки:** Урок 12. git revert: https://git-scm.com/docs/git-revert; Pro Git 2.4 «Undoing Things»:
   https://git-scm.com/book/en/v2/Git-Basics-Undoing-Things

   **Перевірено запуском:** ispyt.sh, питання 5.

6. **Відповідь:** перший `git status`: `Your branch is up to date with 'origin/main'.` (хоч це вже неправда).
   Після `git fetch`:

   ```text
   Your branch is behind 'origin/main' by 1 commit, and can be fast-forwarded.
     (use "git pull" to update your local branch)
   ```

   `druh.txt` у теці **не** зʼявиться (`fetch` файли не чіпає). Що нового: `git log --oneline main..origin/main` →
   `ХЕШ (origin/main, origin/HEAD) Від одногрупника`.

   **Чому:** `origin/main` - **памʼять** твого git про GitHub на момент останнього `fetch`/`pull`/`push`. `git status`
   у мережу не ходить, він порівнює з цією памʼяттю. `fetch` оновлює лише `origin/main`; у твій `main` і в теку зміни
   потрапляють тільки після `merge` (або `pull` = `fetch` + `merge`).

   **Звідки:** Урок 09. Pro Git 3.5 «Remote Branches»: https://git-scm.com/book/en/v2/Git-Branching-Remote-Branches;
   git fetch: https://git-scm.com/docs/git-fetch

   **Перевірено запуском:** ispyt.sh, питання 6.

7. **Відповідь:**

   ```text
   git reflog -3
   git reset --hard HEAD@{1}
   ```

   `git reflog -3` покаже (замість `ХЕШ` - короткі хеші, у тебе свої):

   ```text
   ХЕШ (HEAD -> main) HEAD@{0}: reset: moving to HEAD~2
   ХЕШ HEAD@{1}: commit: ЛР5: завдання 3
   ХЕШ HEAD@{2}: commit: ЛР5: завдання 2
   ```

   Перший хеш - це «ЛР5: завдання 1» (туди тебе відкинув `reset`), тому біля нього ярлик `(HEAD -> main)`. На
   «завдання 3» і «завдання 2» вже не показує жодна гілка - ярликів нема.

   Безпечніше - спершу закріпити загублений коміт гілкою, нічого не затираючи: `git branch vriatovano HEAD@{1}`
   (або хеш з reflog), подивитись `git log --oneline vriatovano`, і лише потім пересувати `main`.

   **Чому:** `reset --hard` пересунув гілку назад, але коміти не видалив - вони стали недосяжними. Reflog записує
   кожен рух HEAD, тож `HEAD@{1}` = «де я був один крок тому» = «завдання 3» (воно містить і «завдання 2»). Записи reflog
   живуть 90 днів, недосяжні коміти - 30. Чого reflog **не** рятує: незакомічених змін, які затер `--hard`.
   Увага: `HEAD@{1}` дійсне одразу після помилки; після інших команд номер зміниться - дивись reflog.

   **Звідки:** Урок 12 (Крок 7, reflog). git reflog: https://git-scm.com/docs/git-reflog; git gc (90/30 днів):
   https://git-scm.com/docs/git-gc; Pro Git 7.7 «Reset Demystified»: https://git-scm.com/book/en/v2/Git-Tools-Reset-Demystified

   **Перевірено запуском:** ispyt.sh, питання 7 (обидва способи).

8. **Відповідь:** злити свіжий `main` у свою гілку, розвʼязати конфлікт у себе і запушити **ту саму** гілку:

   ```text
   git switch main
   git pull
   git switch lr3
   git merge main              ← CONFLICT (content): Merge conflict in lr3.py
   git status --short          ← UU lr3.py
   nano lr3.py                 ← лишити правильний рядок, прибрати <<<<<<< ======= >>>>>>>
   python3 -m doctest lr3.py   ← перевірити, що код живий
   git add lr3.py
   git commit                  ← повідомлення злиття вже готове
   git push
   ```

   PR закривати **не треба**: він показує гілку `lr3`, а не знімок на момент відкриття, тож новий коміт зʼявиться в ньому
   сам, і кнопка Merge стане доступною. Для простого конфлікту можна і кнопкою «Resolve conflicts» на сторінці PR.

   **Чому:** конфлікт - коли дві гілки змінили ті самі рядки. GitHub не вибирає за тебе. Злиття `main` у `lr3` робить
   `main` частиною історії `lr3`, тож після нього злиття `lr3 → main` проходить без конфлікту. Розвʼязувати в себе
   краще, бо можна запустити doctest до push.

   **Звідки:** Уроки 08 і 11. GitHub, «Resolving a merge conflict using the command line»:
   https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/addressing-merge-conflicts/resolving-a-merge-conflict-using-the-command-line;
   «About pull requests» («The Commits tab shows how the pull request branch changed over time»):
   https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/proposing-changes-to-your-work-with-pull-requests/about-pull-requests

   **Перевірено запуском:** ispyt.sh, питання 8 (до злиття гілки на «GitHub» конфліктують, після push - ні).

9. **Відповідь:** токен **досі в репо** - в історії. Будь-хто, хто склонує, побачить його: `git show HEAD~1:config.py`
   або `git log -S taiemnyi-123` (знайде і коміт, що додав, і коміт, що прибрав). Першим ділом - **відкликати (revoke)
   або замінити (rotate) сам токен** на тому сервісі, де його видали. Потім уже: секрет у змінну середовища або файл з
   `.gitignore`, а історію за потреби чистять `git-filter-repo` з force push (у своєму репо, за інструкцією GitHub).

   **Чому:** коміт - знімок; новий коміт без файлу не змінює старих знімків. Публічний репо могли вже склонувати або
   просканувати боти за хвилини, а чистка історії не дістане чужих клонів і форків. Тому єдине, що точно робить
   витік нешкідливим, - зробити сам токен недійсним. Документація GitHub: «as a first step you need to revoke and/or
   rotate that secret».

   **Звідки:** Урок 15 (Типова 4), Урок 03 (Типова 6 - те саме з SSH-ключем). GitHub, «Removing sensitive data from a
   repository»: https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/removing-sensitive-data-from-a-repository
   (відкрито 18.11.2026); «About secret scanning»:
   https://docs.github.com/en/code-security/secret-scanning/introduction/about-secret-scanning

   **Перевірено запуском:** ispyt.sh, питання 9 (свіжий клон після видалення досі бачить токен в історії).

10. **Відповідь:** `! [rejected]        main -> main (fetch first)`. Далі:

    ```text
    git pull        ← відкриє nano з готовим повідомленням злиття
    git push
    ```

    `git pull` забирає коміт одногрупника і робить коміт злиття, тож **відкриває nano** з готовим повідомленням
    `Merge branch 'main' of github.com:Evge14n/РЕПО`. Нічого не міняй: Ctrl+O, Enter (зберегти), Ctrl+X (вийти). Після
    цього `pull` допише `Merge made by the 'ort' strategy.` (Якщо `pull` дасть конфлікт - розвʼязати, як у питанні 8.) На GitHub стане **4** коміти: `Initial commit`,
    коміт одногрупника, твій `lr2.py` і коміт злиття з двома батьками.

    **Чому:** push приймається, лише якщо твій коміт **продовжує** те, що на GitHub. Там є коміт, якого нема в тебе -
    git не дає його затерти. `pull` забирає його і зливає з твоїм, після цього твій `main` продовжує GitHub-івський і push
    проходить. `--force` зробив би GitHub «як у тебе» - коміт одногрупника зник би з `main`.

    **Звідки:** Урок 09 («rejected - fetch first»). git push: https://git-scm.com/docs/git-push; git pull:
    https://git-scm.com/docs/git-pull

    **Перевірено запуском:** ispyt.sh, питання 10 (і що `pull` відкриває редактор саме з цим повідомленням).

11. **Відповідь:** це **detached HEAD** («HEAD відчеплений»): `git status` пише `HEAD detached at lr1-zdano`, ти
    стоїш на коміті, а не на гілці. Коміт «Правка на тезі» не належить жодній гілці, тож при `git switch main` git
    попереджає:

    ```text
    Warning: you are leaving 1 commit behind, not connected to
    any of your branches:

      ХЕШ Правка на тезі
    ```

    Порятунок - дати коміту гілку: `git branch lr1-pravka HEAD@{1}` (або хеш з попередження). Тег при цьому не
    зрушив. Правильно від початку: `git switch -c lr1-pravka lr1-zdano` (або на тезі `git switch -c lr1-pravka`
    **до** коміту) - тоді коміт одразу на гілці.

    **Чому:** новий коміт пересуває вперед **поточну гілку**. Тег не їде, а гілки нема - тож нового коміту ніщо не
    тримає, крім reflog (і через 30 днів git може його прибрати).

    **Звідки:** Урок 14 (Типова 4), Урок 12 (reflog). git switch / git checkout (DETACHED HEAD):
    https://git-scm.com/docs/git-switch, https://git-scm.com/docs/git-checkout

    **Перевірено запуском:** ispyt.sh, питання 11.

12. **Відповідь:** індекс дає змогу **зібрати коміт руками** - вибрати, що саме в нього піде, з усього, що зараз змінено.
    Приклад: ти доробив завдання 2 в `lr1.py` і заодно почав чернетку в `lr2.py`. `git add lr1.py` + `git commit` -
    у коміті лише завдання 2, а `lr2.py` чекає (` M lr2.py`). Ще тонше: `git add -p` бере навіть частину змін одного
    файлу. Без індексу коміт був би «все, що зараз на диску»: чернетки, налагоджувальні `print` і зламаний код разом.

    **Чому це важливо:** один коміт = одна логічна зміна. Тоді `git revert` скасовує рівно одну річ, `git log` читається
    як план роботи, а рев'ю PR бачить зрозумілі кроки. Третя зона (репозиторій) - це вже незмінні знімки з хешами.

    **Звідки:** Уроки 01 і 04. Pro Git 1.3 (working tree, staging area, Git directory):
    https://git-scm.com/book/en/v2/Getting-Started-What-is-Git%3F; git add (`-p`): https://git-scm.com/docs/git-add

    **Перевірено запуском:** ispyt.sh, питання 12 (у коміті лише `lr1.py`).

13. **Відповідь:** **fast-forward** - коли поточна гілка не рухалась з моменту відгалуження: git просто пересуває
    вказівник, нового коміту нема, історія пряма. **Merge-коміт** - коли обидві гілки мають нові коміти: потрібен коміт
    з двома батьками. «Create a merge commit» на GitHub = `git merge --no-ff`: коміт злиття робиться **завжди**, щоб в
    історії `main` було видно «тут злито PR #N» і щоб весь PR можна було скасувати одним `git revert -m 1` цього коміту.
    `git merge --ff-only` на розбіжних гілках відмовляє і нічого не змінює (код 128):

    ```text
    fatal: Not possible to fast-forward, aborting.
    ```

    **Чому:** вибір - між прямою історією (ff, squash, rebase) і явними межами злиттів (merge-коміт). Обидва правильні,
    команда домовляється про один. `--ff-only` (і `git pull --ff-only`) - запобіжник «не зливай нічого несподівано».

    **Звідки:** Уроки 07 і 11 (три кнопки злиття), Урок 09 (`--ff-only`). git merge: https://git-scm.com/docs/git-merge;
    GitHub, «About pull request merges»:
    https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/incorporating-changes-from-a-pull-request/about-pull-request-merges

    **Перевірено запуском:** ispyt.sh, питання 13 (`--no-ff` дає 2 батьки там, де можна перемотати; `--ff-only` - код 128).

14. **Відповідь:** `revert` **додає** новий коміт, що скасовує зміни, а `reset` **переписує** історію (відкидає коміти).
    Запушені коміти вже є в інших (клони одногрупників, викладача, GitHub). Після `reset` звичайний push відмовить:

    ```text
     ! [rejected]        main -> main (non-fast-forward)
    ```

    (`non-fast-forward`, а не `fetch first`: на GitHub лише твій поганий коміт, і він у тебе є.)
    `git push --force-with-lease` після того, як одногрупник запушив, теж відмовить:

    ```text
     ! [rejected]        main -> main (stale info)
    ```

    бо твій `origin/main` застарів - git бачить, що на GitHub не те, що ти востаннє бачив. Простий `--force` затер би
    коміт одногрупника. **Пастка:** якщо перед `--force-with-lease` зробити `git fetch`, `origin/main` оновиться до коміту
    одногрупника, перевірка пройде - і `--force-with-lease` **затре** його коміт так само, як `--force`:

    ```text
     + ХЕШ...ХЕШ main -> main (forced update)
    ```

    Правильний шлях: `git pull` (поверне все), `git revert --no-edit ХЕШ`, `git push` - поганий коміт лишається в
    історії, а його дія скасована.

    **Чому:** у спільній історії не можна «вирвати сторінку», яку вже скопіювали інші: їхні клони розійдуться з
    GitHub, а сила знищить чужу роботу. `--force-with-lease` - сила з перевіркою «на GitHub досі те, що я востаннє
    бачив?». Вона захищає лише від того, чого ти ще **не** бачив: після `git fetch` git вважає, що чужий коміт ти бачив і
    затираєш свідомо. Тому lease - лише для своєї гілки, і без `fetch` перед ним.

    **Звідки:** Урок 12. git push (`--force`, `--force-with-lease`): https://git-scm.com/docs/git-push; Pro Git 2.4
    «Undoing Things»: https://git-scm.com/book/en/v2/Git-Basics-Undoing-Things

    **Перевірено запуском:** ispyt.sh, питання 14 (обидві відмови, коміт одногрупника цілий, revert пушиться; після
    `git fetch` lease проходить і коміт одногрупника зникає з `main` на «GitHub»).

15. **Відповідь:** пароль ти щоразу **передаєш** (його можна підгледіти, вкрасти фішингом, підібрати, він часто
    однаковий на кількох сайтах). При SSH приватний ключ **ніколи не покидає** ноутбук: ssh лише доводить, що ключ у тебе.
    Ключ довгий і випадковий - не підбереш. Кожен ключ окремий: загубив ноутбук - видалив на GitHub лише його ключ.
    Крім того, з 13.08.2021 GitHub узагалі не приймає пароль акаунта для git - лише SSH-ключ або токен.
    `id_ed25519.pub` (замок) можна показувати всім - він сам доступу не дає. `id_ed25519` (ключ від замка) - хто його має,
    той заходить як ти: вважай украденим, видали на GitHub (Settings → SSH and GPG keys), створи новий.

    **Чому ще:** ssh перевіряє і **сервер** - відбиток github.com (`SHA256:+DiY3wvvV6TuJJhbpZisF/zLDA0zPMSvHdkr4UvCOqU`)
    у `known_hosts`, тож підмінений сервер у чужому Wi-Fi видно. Приватний ключ має права `600`, інакше ssh його ігнорує.
    Додатково ключ можна закрити паролем-фразою (passphrase).

    **Звідки:** Урок 03. GitHub, «About SSH» («With SSH keys, you can connect to GitHub without supplying your username
    and personal access token at each visit»): https://docs.github.com/en/authentication/connecting-to-github-with-ssh/about-ssh
    (відкрито 18.11.2026); «GitHub's SSH key fingerprints»:
    https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/githubs-ssh-key-fingerprints;
    github.blog, «Token authentication requirements for Git operations» (за ФАКТИ-GIT)

    **Не запускається:** потрібен справжній GitHub.

16. **Відповідь:** вкладка **Files changed** → коментар до рядка → **Review changes** → **Request changes** («спершу
    виправ») → Submit review. Коли автор запушить виправлення в **ту саму гілку**, нові коміти зʼявляться в тому ж PR
    (новий PR не потрібен), ти перевіриш і поставиш **Approve**. Автор не може схвалити свій PR: «Pull request authors
    cannot approve their own pull requests» - сенс рев'ю в **другій парі очей**.

    **Чому:** Comment - просто думка, Approve - «можна зливати», Request changes - «зливати рано». У командах `main`
    часто захищають правилом «злиття лише з Approve», тож самосхвалення зламало б увесь захист.

    **Звідки:** Урок 11. GitHub, «Reviewing proposed changes in a pull request»:
    https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/reviewing-changes-in-pull-requests/reviewing-proposed-changes-in-a-pull-request;
    «Approving a pull request with required reviews»:
    https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/reviewing-changes-in-pull-requests/approving-a-pull-request-with-required-reviews

    **Не запускається:** це кнопки сайту. (Що push у ту саму гілку оновлює PR - див. питання 8.)

17. **Відповідь:** на GitHub Free Pages працює **лише з публічного** репо («If the account that owns the repository uses
    GitHub Free ..., the repository must be public»). Робити `univer-labs` публічним не можна - там розвʼязки лаб.
    Тому: окремий **публічний** репо, наприклад `fizyka-storinka`, у корені `index.html`, push, потім Settings → Pages →
    Source: **Deploy from a branch** → `main`, `/ (root)` → Save. Адреса: `https://evge14n.github.io/fizyka-storinka/`
    (логін малими літерами). Оновлюється після кожного push у вибрану гілку (docs: до 10 хв).

    **Чому:** це **обмеження тарифу** Free: Pages з приватного репо - платна можливість. На GitHub Pro (і вище) Pages
    можна і з приватного репо (docs, «GitHub's plans»). Чи дає Pro студентський GitHub Student Developer Pack - (не
    перевірено: на сторінках docs GitHub Education про Pro не сказано). Але навіть на Pro **сайт однаково публічний**: «GitHub Pages
    sites are publicly available on the internet, even if the repository for the site is private». Тож розвʼязки лаб
    на Pages потрапили б в інтернет за будь-якого тарифу - розділення «приватне - лаби, публічне - сайт» правильне завжди.

    **Звідки:** Урок 15. GitHub, «Creating a GitHub Pages site»:
    https://docs.github.com/en/pages/getting-started-with-github-pages/creating-a-github-pages-site; «Configuring a
    publishing source»: https://docs.github.com/en/pages/getting-started-with-github-pages/configuring-a-publishing-source-for-your-github-pages-site;
    «GitHub's plans»: https://docs.github.com/en/get-started/learning-about-github/githubs-plans (відкрито 18.11.2026)

    **Не запускається:** потрібен справжній GitHub.

18. **Відповідь:** issue #3 закриється **лише коли коміт потрапить у гілку за замовчуванням** (`main`) - тобто після
    злиття `lr3` (PR або merge + push). Push самої `lr3` його не закриє. `git log --oneline` покаже лише заголовок
    `Опиши пісочницю в README`, бо `Closes #3` - другий `-m`, тобто **тіло** коміту (`git log -1 --format=%b`).
    Знайти: `git log --oneline --grep="Closes #3"`.

    **Чому:** кожен `-m` - окремий абзац; `--oneline` показує лише перший рядок, а GitHub шукає ключове слово в усьому
    тексті. Те саме `Closes #3` можна написати в описі PR - issue закриється при злитті PR.

    **Звідки:** Уроки 10 і 11. GitHub, «Linking a pull request to an issue»:
    https://docs.github.com/en/issues/tracking-your-work-with-issues/using-issues/linking-a-pull-request-to-an-issue

    **Перевірено запуском:** ispyt.sh, питання 18 (тіло коміту і `--grep`; закриття issue - справа сайту, не запускається).

19. **Відповідь:**

    ```text
    git switch main
    git pull
    git merge lr3
    git push
    git tag -a lr3-zdano -m "ЛР3 здано"
    git push origin lr3-zdano
    git branch -d lr3
    git push origin --delete lr3
    mkdir -p ~/univer/zdacha
    git archive --format=zip --prefix=Прізвище_Імʼя_Група_2026/ -o ~/univer/zdacha/lr3.zip lr3-zdano lr3
    python3 -m zipfile -l ~/univer/zdacha/lr3.zip
    ```

    **Чому так:** `pull` перед `merge` - щоб злити в **свіжий** `main` (інакше push відмовить, питання 10). Тег
    **анотований** (`-a`) - бо здачу бачать інші: в тегу автор, дата, повідомлення. Тег ставиться **після** злиття,
    тобто на коміт у `main`, який реально лежить на GitHub. Звичайний `git push` теги не везе - тому окремо
    `git push origin lr3-zdano`. `branch -d` (мала `d`) - безпечне видалення: git не дасть, якщо гілка не злита.
    `git archive` бере файли **з тегу**, тож в архіві рівно здана версія і без `.venv`/`__pycache__`.
    Шлях через PR: `git push`, `gh pr create --fill --base main`, Merge на сайті, потім `git switch main`, `git pull`,
    і тег так само.

    **Звідки:** «Лаби в git» (рецепт і ЛР1 від гілки до архіву), Уроки 07, 09, 14. git tag:
    https://git-scm.com/docs/git-tag; git archive: https://git-scm.com/docs/git-archive

    **Перевірено запуском:** ispyt.sh, питання 19 (команди дослівно: тег типу `tag` на `origin/main`, на GitHub тег є,
    гілки `lr3` нема, архів містить `lr3/lr3_1.py`).

20. **Відповідь:**

    ```text
    cd ~/univer/labs
    git switch main
    git pull
    git switch -c lr4
    mkdir -p lr4
    (поклади заготовки викладача в lr4/)
    git add lr4
    git commit -m "ЛР4: заготовки викладача"
    git push -u origin lr4
    ```

    Перевірка: `git status -sb` перший рядок `## lr4...origin/lr4`, або `git rev-parse --abbrev-ref lr4@{upstream}` →
    `origin/lr4`. Push напише `branch 'lr4' set up to track 'origin/lr4'.`

    **Чому так:** `switch main` + `pull` - нова лаба стартує від `main` з усіма попередніми лабами (інакше гілка
    почнеться без ЛР3). Перший коміт - **чиста заготовка**, щоб `git diff` потім показував лише твої зміни (викладач
    забороняє міняти назви функцій і doctest). `-u` запамʼятовує звʼязок `lr4 ↔ origin/lr4`: далі просто `git push`
    і `git pull`, а `git status` пише ahead/behind.

    **Звідки:** «Лаби в git» (рецепт), Уроки 07 і 09. git switch: https://git-scm.com/docs/git-switch;
    git push (`-u`): https://git-scm.com/docs/git-push

    **Перевірено запуском:** ispyt.sh, питання 20 (команди дослівно; заготовка - `printf` замість копіювання).

### Таблиця «питання → урок»

| № | Тип | Тема | Урок | Перевірено запуском |
|---|---|---|---|---|
| 1 | що виведе | три зони, add і друга правка | 01, 04 | так |
| 2 | історія | fast-forward і merge-коміт | 07 | так |
| 3 | що виведе | легкі й анотовані теги, push | 14 | так |
| 4 | що виведе | stash як стос, pop не затирає | 13 | так |
| 5 | історія | revert середнього коміту | 12 | так |
| 6 | що виведе | origin/main - памʼять, fetch | 09 | так |
| 7 | ситуація | загублені коміти, reflog | 12 | так |
| 8 | ситуація | конфлікт у PR | 08, 11 | так |
| 9 | ситуація | запушений секрет | 15, 03 | так |
| 10 | ситуація | відстав від main, fetch first | 09 | так |
| 11 | ситуація | detached HEAD на тезі | 14, 12 | так |
| 12 | поясни | навіщо індекс | 01, 04 | так |
| 13 | поясни | ff, --no-ff, --ff-only | 07, 09, 11 | так |
| 14 | поясни | revert, а не reset; force-with-lease | 12 | так |
| 15 | поясни | SSH-ключ проти пароля | 03 | ні (справжній GitHub) |
| 16 | GitHub | рев'ю PR | 11 | ні (сайт) |
| 17 | GitHub | Pages на Free | 15 | ні (сайт) |
| 18 | GitHub | Closes #N | 10, 11 | так (частково) |
| 19 | команди | цикл здачі ЛР з тегом | Лаби в git, 07, 09, 14 | так |
| 20 | команди | почати лабу з гілки | Лаби в git, 07, 09 | так |

Слабке питання = перечитай урок з таблиці і зроби його «Руками» ще раз.

### Як рахувати бал

Кожне питання - **5 балів**, усього **100**.

| Бали | Коли |
|---|---|
| 5 | відповідь правильна **і** «чому» пояснено своїми словами (для «що виведе» - ключові рядки виводу) |
| 3 | відповідь правильна, але «чому» немає або хибне; або в командах пропущено один крок (`git pull` перед злиттям, push тегу) |
| 1 | правильний напрям, але результат хибний (наприклад, «reflog», але без команди повернення) |
| 0 | хибно, порожньо, або порада, що шкодить (`git push --force` у `main`, `git reset` після push, «просто видали файл з секретом») |

- **90-100** - мета: git для лаб і командної роботи ти розумієш.
- **75-89** - основу знаєш; переглянь уроки з таблиці для питань, де менше 5.
- **нижче 75** - пройди ще раз уроки 07, 09, 12, 14 і «Лаби в git», через тиждень склади іспит знову (питання ті самі -
  тож вдруге пояснюй «чому» ще детальніше, а виводи перевір у пісочниці).

Чесне правило: 5 балів лише якщо ти **написав** відповідь до того, як глянув у розділ «Відповіді».

### Як перевірено сам іспит (UGIT1, 18.11.2026)

- 17 з 20 відповідей підтверджено запуском справжнього git 2.43.0 (`_перевірка/ispyt.sh`, 95+ перевірок, усі ok); 15-17 (SSH, рев'ю PR, Pages) - за docs.github.com.
- Незалежний рецензент склав іспит наосліп: **20/20**, хибних еталонів 0; 4 неточності (п. 7, 10, 14, 17) виправлено того ж дня.
- Твій результат запиши сюди з датою, через тиждень - удруге:

| Дата | Бали | Що повторити |
|---|---|---|
|  |  |  |


</details>
