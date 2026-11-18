# Git і GitHub з нуля - у терміналі Linux Mint

17 уроків по 15-20 хв: 5 хв прочитати, 10 хв зробити руками в терміналі, 5 питань самоперевірки.
Кожну команду курсу прогнано скриптом у справжньому git 2.43.0 (Ubuntu 24.04 і Linux Mint 22.3)
на тимчасових репозиторіях, конфлікти й порятунок через reflog - справжні (18.11.2026).

## Тема 0. Почни тут: план, як вчитися, пісочниця

### Навіщо це тобі

- **Не втрачати робочий код.** Зламав ЛР3 перед здачею - повернувся до версії, де doctest проходив. В git кожен такий стан зберігається, і повернення займає одну команду.
- **Лаби не зникнуть з ноутбуком.** Копія лежить на GitHub, у приватному репо, яке бачиш лише ти (і ті, кого запросиш).
- **Показати викладачу** - посилання на коміт або тег замість «скинув файл у Telegram».
- **Так працюють програмісти в командах.** На практиці чи стажуванні дуже ймовірно почуєш «склонуй репо і зроби PR». Після курсу це не буде страшно.

У курсі Linux (День 09) ти вже бачив `git init`, `add`, `commit`, `log`. Тут те саме, але глибше, плюс GitHub: SSH-ключ, push і pull, конфлікти, Pull Request, сайт на Pages.

### План

| № | Урок | Що вмітимеш |
|---|---|---|
| 01 | Що таке git і GitHub | знімки, коміт, хеш, три зони; чим git відрізняється від GitHub |
| 02 | Встановлення на Mint і git config | поставити git і gh, підписати коміти своїм імʼям і noreply-поштою |
| 03 | SSH-ключ і вхід у GitHub | ключ, вхід без пароля, приватна пісочниця `pisochnytsia` |
| 04 | Перший репозиторій - init, clone, status, add, commit | щоденний цикл і гарні повідомлення комітів |
| 05 | Історія - log, diff, show | знайти, що і коли змінилось |
| 06 | gitignore для Python | щоб `.venv/` і `__pycache__/` не лізли в коміти |
| 07 | Гілки - branch, switch, merge | пробувати ідею, не ламаючи робочий код |
| 08 | Конфлікт і як розвʼязати руками | що робити, коли git не може злити сам |
| 09 | Віддалений репозиторій - remote, push, pull, fetch | відправити коміти на GitHub і забрати назад |
| 10 | GitHub - репозиторій, README, Issues | оформити репо і вести список задач |
| 11 | Pull Request - гілка, рев'ю, merge | як зміни приймають у командах |
| 12 | Скасувати безпечно - restore, revert, reset, reflog | відкотити помилку і нічого не втратити |
| 13 | stash - відкласти зміни | сховати недороблене на 5 хвилин |
| 14 | Теги - позначити здачу | «ось версія, яку я здав» |
| 15 | GitHub Pages | безкоштовний сайт з репо |
| 16 | gh - GitHub з терміналу | репо, Issues і PR без браузера |
| 17 | Для профі - rebase, cherry-pick, bisect, worktree, Actions | те, що вміють у командах: лінійна історія, пошук коміту-винуватця, автотести на GitHub |
| - | Лаби в git - univer-labs покроково | один приватний репо на всі ЛР1-ЛР7: коміт на крок, гілка на лабу, тег на здачу |
| - | Практика - 4 завдання | лаба з напарником, аварія перед здачею, здача з тегом і архівом, сайт на Pages |
| - | ІСПИТ-САМОПЕРЕВІРКА | 20 питань рівня іспиту і співбесіди; мета 90 % |

### Що робити першим

1. **Урок 02** - встановити git і gh, налаштувати імʼя і пошту. Без цього решта не запрацює.
2. **Урок 03** - SSH-ключ і приватний репо-пісочниця `pisochnytsia` на GitHub.
3. Далі по порядку: **01** (тепер у тебе вже є git, щоб пробувати), **04**, **05** і так далі.

Спершу перевір, чи є git на ноутбуці:
```bash
git --version
```
```text
git version 2.43.0
```
Якщо термінал каже, що команду не знайдено, - так і має бути на свіжому Mint 22.3, урок 02 це виправить.

### Як вчитися

- **15-20 хвилин на день, один урок.** Краще щодня потроху, ніж три уроки за раз перед сесією. Увесь курс - приблизно три тижні.
- **Передбач, потім запусти.** У кожному уроці є розділ «Передбач, потім запусти». Спершу сам скажи (можна вголос), що виведе команда, і лише потім відкрий відповідь і запусти. Помилився - чудово, саме так запамʼятовується найкраще.
- **Набирай руками.** Команди з блоків `bash` набирай самі, а не копіюй (крім довгого сніпета встановлення gh в уроці 02). Руки запамʼятовують краще за очі.
- **Самоперевірка** в кінці уроку - 5 питань. Відповідай, не підглядаючи, потім звір з відповідями під «Відповіді». Не знаєш 2 з 5 - перечитай «Коротко».
- **Картки бота.** До кожного уроку є картки: бот-нагадувач сам надсилатиме питання з перервами, які ростуть (сьогодні, потім через кілька днів, потім рідше) - саме тоді, коли ти вже почнеш забувати. Спершу відповідай сам, потім дивись відповідь. А тести до уроків (з варіантами) є на сайті підготовки uni-prep.
- **Вивід англійською.** Курс показує вивід git англійською, як у більшості інструкцій. Якщо в тебе git говорить українською - див. урок 02 («Мова виводу»).

**Як читати уроки:**
- блок `bash` - команди, які набираєш у терміналі дослівно;
- блок `text` - що покаже термінал, шаблони і шляхи меню на сайті;
- **хеші комітів у тебе будуть інші** (`3347fd3` і подібні): у кожен коміт входить час;
- `/home/...` у виводі - твоя домашня тека.

### Пісочниця

Вчитися треба там, де не шкода зламати. Лаби - не пісочниця.

| Де | Що це | З якого уроку |
|---|---|---|
| `~/git-urok01` | маленьке репо для першого уроку | 01 |
| `~/git-pisochnytsia` | локальне репо, без GitHub | 04-08 |
| `~/pisochnytsia` | клон твого **приватного** репо `pisochnytsia` на GitHub | 03 і далі |
| `~/druhyi-klon` | другий клон того самого репо, «ноутбук одногрупника» (у ньому `user.name` = «Друг») | 08-11 |

Зламав пісочницю так, що не розумієш, що відбувається? Можна видалити теку і склонувати заново - на GitHub усе лишиться.

**Два правила безпеки на весь курс:**
- файл `~/.ssh/id_ed25519` (приватний ключ) нікому не показуй і нікуди не вставляй (урок 03);
- небезпечні команди (наприклад, `git push --force`) в уроках стоять лише в блоках `text` з поясненням - не набирай їх «на пробу» в репо з лабами.

## Тема 1. Що таке git і GitHub

**Навіщо:** у ЛР2 ти переписав функцію, doctest упав, а як було до того, вже не памʼятаєш. git зберігає кожен робочий стан лаби, і до нього можна повернутись. GitHub потрібен, щоб ці стани жили ще й в інтернеті: не пропадуть разом з ноутбуком, і їх можна показати викладачу.

### Коротко

У Дні 09 курсу Linux ти вже робив `git init`, `add`, `commit`. Тепер розберемо, **що саме** при цьому відбувається.

- **Репозиторій (репо)** - тека проєкту плюс схована тека `.git` у ній. У `.git` git тримає всю історію.
- **Коміт** - знімок усіх файлів, за якими стежить git, у певний момент. До знімка додається: хто зробив, коли, повідомлення і посилання на попередній коміт (його називають «батько»). git зберігає саме знімки, а не список змін (Pro Git, 1.3).
- **Хеш** - імʼя коміту: 40 символів з `0-9` і `a-f`, наприклад `4528870a15aba5fc1ba92936c47546f163136254`. Він рахується з усього вмісту коміту, тому будь-яка зміна дає інший хеш. Зазвичай досить перших 7 символів: `4528870`.
- **Три зони** (Pro Git 1.3: working tree, staging area, Git directory):

```text
 робоча тека              індекс (staging area)        репозиторій (.git)
 файли, які ти правиш     що піде в наступний коміт    історія комітів

   lr1.py  ──git add──►    lr1.py  ──git commit──►    076d5fc ◄── 4528870
                                                       (батько)    (новий)
```

Аналогія: фото групи. Робоча тека - люди в кімнаті. `git add` - покликати когось у кадр (індекс). `git commit` - клацнути фото і підписати його. Альбом фото - репозиторій. Хто не став у кадр, на фото не потрапить, навіть якщо стоїть у кімнаті.

`git status --short` показує ці зони двома літерами: **ліва - індекс, права - робоча тека** (git-scm.com/docs/git-status).

| Вивід | Що значить |
|---|---|
| `?? lr1.py` | новий файл, git за ним ще не стежить |
| `A  lr1.py` | новий файл додано в індекс (A - added) |
| ` M lr1.py` | файл змінено в робочій теці, в індекс ще не додано |
| `M  lr1.py` | зміну додано в індекс, піде в коміт |
| `MM lr1.py` | частину змін додано в індекс, а потім файл змінили ще раз |

**git і GitHub - різні речі:**

| | git | GitHub |
|---|---|---|
| Що це | програма на твоєму ноутбуці | сайт, сервіс компанії GitHub |
| Інтернет | не потрібен | потрібен |
| Що робить | коміти, історія, гілки | зберігає копію репо, Issues, Pull Request, сайти (Pages) |
| Як керувати | команди `git ...` | сайт або команди `gh ...` (урок 16) |

git працює і без GitHub. GitHub - лише одне з місць, куди можна відправити копію репо (є ще GitLab, Codeberg; git той самий).

### Передбач, потім запусти

Спершу подумай, потім глянь відповідь, потім перевір у терміналі (розділ «Руками»).

1. У новому репо створили `lr1.py`. Що покаже `git status --short`?
<details markdown="1"><summary>Відповідь</summary>

```text
?? lr1.py
```
git бачить файл, але ще не стежить за ним.
</details>

2. Файл уже в коміті. Його змінили, зробили `git add lr1.py`, а потім змінили ще раз. Що покаже `git status --short`?
<details markdown="1"><summary>Відповідь</summary>

```text
MM lr1.py
```
Ліва `M` - перша зміна в індексі. Права `M` - друга зміна, лише в робочій теці.
</details>

3. У цьому стані (`MM`) робиш `git commit -m "Завдання 1"`. Що покаже `git status --short` після коміту?
<details markdown="1"><summary>Відповідь</summary>

```text
 M lr1.py
```
У коміт пішло лише те, що було в індексі. Друга зміна лишилась у робочій теці.
</details>

4. Що покаже `git remote -v` у репо, створеному через `git init`?
<details markdown="1"><summary>Відповідь</summary>

Нічого (порожньо). Репо живе лише на ноутбуці, GitHub про нього не знає. Звʼязок з GitHub - уроки 03 і 09.
</details>

### Руками

Потрібен встановлений і налаштований git (урок 02). Працюємо в окремій теці, яку не шкода.

**Крок 1. Перший знімок.**
```bash
mkdir ~/git-urok01
cd ~/git-urok01
git init
git status
printf 'print("ЛР1")\n' > lr1.py
git status --short
git add lr1.py
git status --short
git commit -m "Додай lr1.py"
```
```text
Initialized empty Git repository in /home/.../git-urok01/.git/
```
```text
On branch main

No commits yet

nothing to commit (create/copy files and use "git add" to track)
```
```text
?? lr1.py
```
```text
A  lr1.py
```
```text
[main (root-commit) 076d5fc] Додай lr1.py
 1 file changed, 1 insertion(+)
 create mode 100644 lr1.py
```
`/home/...` - твоя домашня тека. `root-commit` - перший коміт, у нього нема батька. `076d5fc` - короткий хеш. **У тебе хеші будуть інші** (у знімок входить час), так буде в усьому курсі.

**Крок 2. Три зони в дії.**
```bash
printf 'print("ЛР1, завд. 1")\n' > lr1.py
git status --short
git add lr1.py
git status --short
printf 'print("ЛР1, завд. 2")\n' >> lr1.py
git status --short
git status
```
```text
 M lr1.py
```
```text
M  lr1.py
```
```text
MM lr1.py
```
```text
On branch main
Changes to be committed:
  (use "git restore --staged <file>..." to unstage)
	modified:   lr1.py

Changes not staged for commit:
  (use "git add <file>..." to update what will be committed)
  (use "git restore <file>..." to discard changes in working directory)
	modified:   lr1.py

```
Той самий файл - у двох списках. «Changes to be committed» - індекс, «Changes not staged» - робоча тека.

```bash
git commit -m "Завдання 1"
git status --short
git log --oneline
```
```text
[main 4528870] Завдання 1
 1 file changed, 1 insertion(+), 1 deletion(-)
```
```text
 M lr1.py
```
```text
4528870 Завдання 1
076d5fc Додай lr1.py
```

**Крок 3. Що всередині коміту.**
```bash
git rev-parse HEAD
git cat-file -p HEAD
```
```text
4528870a15aba5fc1ba92936c47546f163136254
```
```text
tree 35fa5b63979c4c22106bff356b4fa98889fdefd0
parent 076d5fc68c220f4d10a4de0aa617daee0d6599ce
author Твоє Імʼя <128326252+Evge14n@users.noreply.github.com> 1794996982 +0000
committer Твоє Імʼя <128326252+Evge14n@users.noreply.github.com> 1794996982 +0000

Завдання 1
```
`HEAD` - «коміт, на якому ти зараз». `rev-parse` показує його повний хеш (40 символів). `cat-file -p` показує сам коміт: `tree` - знімок файлів, `parent` - батько (попередній коміт), далі автор, час і повідомлення. Час записано числом секунд від 1 січня 1970 року, `+0000` - часовий пояс (на ноутбуці в Україні буде `+0200`).

**Крок 4. git без GitHub.**
```bash
git remote -v
```
Вивід порожній - цей репо ніде, крім ноутбука, не існує.

**Для лаб:** кожне готове завдання ЛР - окремий коміт. Завдяки індексу можна закомітити лише `lr2.py`, а чернетку `proba.py` поруч не чіпати. А GitHub (урок 03 і далі) - щоб лаби не зникли з ноутбуком і щоб дати викладачу посилання.

### Типові помилки

**1. Команда git не в репо.**
```text
fatal: not a git repository (or any of the parent directories): .git
```
Ти в теці, де нема `.git` (наприклад, у `~`). Перейди в теку репо (`cd ~/git-urok01`) або створи репо `git init`.

**2. «Закомітив, а зміни лишились».** Після коміту `git status --short` показує ` M lr1.py`. Коміт бере лише те, що в індексі. Зроби `git add lr1.py` і ще один коміт.

**3. «Я закомітив - значить, воно на GitHub».** Ні. Коміт - на ноутбуці. У репо без звʼязку з GitHub `git push` скаже:
```text
fatal: No configured push destination.
Either specify the URL from the command-line or configure a remote repository using

    git remote add <name> <url>

and then push using the remote name

    git push <name>

```
Звʼязати репо з GitHub - уроки 03 і 09.

**4. Ctrl+O у nano - це не коміт.** nano зберігає файл у робочу теку. Щоб він потрапив в історію, потрібні `git add` і `git commit`.

### Як роблять профі

- **Спершу модель, потім команди.** MIT Missing Semester 2026 починає git саме з моделі даних: знімки, обʼєкти, хеші, посилання - бо тоді команди стають зрозумілими (missing.csail.mit.edu).
- **`git status` перед кожним `add` і `commit`** - звичка, яка рятує від «закомітив не те».
- **Малі коміти:** одна думка - один коміт («make each commit a logically separate changeset», Pro Git 5.2).
- **git один, хостингів багато:** GitHub, GitLab, Codeberg. Команди git ті самі, різниться лише сайт.
- **Pro Git є українською:** https://git-scm.com/book/uk/v2 - розділ 1.3 «Основи Git» якраз про знімки і три зони.

### Самоперевірка

1. Що таке коміт і що в нього входить, крім файлів?
2. Назви три зони git і команди, які переносять файл між ними.
3. Що означає `MM lr1.py` у `git status --short`?
4. Чим git відрізняється від GitHub? Чи можна працювати з git без інтернету?
5. Чому в тебе і в уроці різні хеші коміту «Додай lr1.py», хоча файл однаковий?

<details markdown="1"><summary>Відповіді</summary>

1. Знімок усіх відстежуваних файлів. Ще: автор, час, повідомлення і посилання на батька (попередній коміт).
2. Робоча тека → `git add` → індекс → `git commit` → репозиторій (`.git`).
3. Частина змін файлу вже в індексі (ліва `M`), а після `git add` файл змінили ще раз (права `M`).
4. git - програма на ноутбуці, GitHub - сайт, де зберігається копія репо, плюс Issues, Pull Request, Pages. З git можна працювати без інтернету; інтернет потрібен лише для обміну з GitHub.
5. Хеш рахується з усього коміту, а туди входять ще час і автор. Інший час → інший хеш.

</details>

### Джерела

- Pro Git, 1.3 «What is Git?» - https://git-scm.com/book/en/v2/Getting-Started-What-is-Git%3F (відкрито 18.11.2026)
- Pro Git українською - https://git-scm.com/book/uk/v2 (відкрито 18.11.2026)
- git status, короткий формат - https://git-scm.com/docs/git-status (відкрито 18.11.2026)
- MIT Missing Semester 2026, «Version Control and Git» - https://missing.csail.mit.edu/2026/version-control/ (відкрито 18.11.2026, за ФАКТИ-GIT)
- Pro Git, 5.2 «Contributing to a Project» - https://git-scm.com/book/en/v2/Distributed-Git-Contributing-to-a-Project (відкрито 18.11.2026)
- Вивід команд - запуск у перевірці `_перевірка/u01.sh` (git 2.43.0, Ubuntu 24.04, 18.11.2026)

## Тема 2. Встановлення на Mint і git config

**Навіщо:** перш ніж зробити перший коміт ЛР1, git має бути встановлений і знати, хто ти. Налаштування робиться один раз на ноутбук, а потім працює в усіх лабах.

### Коротко

На Linux Mint 22.3 git **не стоїть з коробки**. Ставиш його з репозиторію Mint (`apt`). Програму `gh` (GitHub з терміналу, урок 16) ставиш **з офіційного репозиторію GitHub**, а не з Mint: у Mint лежить стара версія 2.45, і вона зламана (частина команд падає з помилкою, бо GitHub прибрав старий API).

**git config** - це налаштування git. `--global` означає «для мене на цьому ноутбуці»: усе пишеться у файл `~/.gitconfig`.

| Налаштування | Що дає |
|---|---|
| `user.name "Твоє Імʼя"` | імʼя автора в кожному коміті |
| `user.email "128326252+Evge14n@users.noreply.github.com"` | пошта автора; noreply - щоб справжня пошта не світилась у публічних комітах, а GitHub все одно привʼязав коміти до `Evge14n` |
| `init.defaultBranch main` | нові репо одразу з гілкою `main`, як на GitHub (без цього буде `master` і довга підказка) |
| `core.editor nano` | коли git просить написати текст (довге повідомлення коміту), відкривається nano, а не vim |
| `pull.rebase false` | `git pull` при розбіжностях робить злиття (урок 08-09), а не падає з помилкою |
| `core.quotepath false` | кириличні назви файлів видно як `звіт.txt`, а не `"\320\267\320\262..."` |

```text
git config --global ...   →   ~/.gitconfig   (твій файл налаштувань, звичайний текст)
git config --global --list           - показати все
git config --list --show-origin      - показати все і З ЯКОГО ФАЙЛУ кожен рядок
```

Аналогія: `~/.gitconfig` - це як підпис і адреса на конверті. Один раз написав - і кожен «лист» (коміт) іде з ними.

### Передбач, потім запусти

1. Ти щойно встановив git і нічого не налаштовував. Що покаже `git config --global --list`?
<details markdown="1"><summary>Відповідь</summary>

Помилку, бо файлу `~/.gitconfig` ще нема:
```text
fatal: unable to read config file '/home/.../.gitconfig': No such file or directory
```
(`/home/...` - це твоя домашня тека.) Це не поломка: файл зʼявиться після першого `git config --global`.
</details>

2. Ти пропустив `init.defaultBranch main` і робиш `git init`. Що буде?
<details markdown="1"><summary>Відповідь</summary>

Репо створиться, але з гілкою `master` і довгою підказкою:
```text
hint: Using 'master' as the name for the initial branch. This default branch name
hint: is subject to change. To configure the initial branch name to use in all
hint: of your new repositories, which will suppress this warning, call:
hint: 
hint: 	git config --global init.defaultBranch <name>
hint: 
hint: Names commonly chosen instead of 'master' are 'main', 'trunk' and
hint: 'development'. The just-created branch can be renamed via this command:
hint: 
hint: 	git branch -m <name>
Initialized empty Git repository in /home/.../proba/.git/
```
</details>

3. Ти помилився в слові і набрав `git config --global user.nmae "Твоє Імʼя"`. git скаже помилку?
<details markdown="1"><summary>Відповідь</summary>

Ні, мовчки збереже. git не знає всіх можливих ключів, тому `user.nmae` для нього - просто ще один рядок. Видно його лише в `git config --global --list`. Як прибрати - в «Типові помилки».
</details>

4. Що покаже `git config user.name` (без `--global`)?
<details markdown="1"><summary>Відповідь</summary>

`Твоє Імʼя`. Без `--global` git читає налаштування з усіх рівнів (системний, твій, репо) і показує підсумкове значення.
</details>

### Руками

**Крок 1. git.** Пароль `sudo` - твій пароль входу в Mint (символи не видно, це нормально).
```bash
sudo apt update
sudo apt install git
git --version
```
```text
git version 2.43.0
```

**Крок 2. gh з офіційного репозиторію GitHub.** Скопіюй блок цілком (це один довгий рядок, розбитий `\`), встав у термінал (Ctrl+Shift+V) і натисни Enter. Сніпет дослівно з документації gh (`docs/install_linux.md`, 18.11.2026): він додає ключ і адресу репозиторію GitHub, а потім ставить `gh`.
```bash
(type -p wget >/dev/null || (sudo apt update && sudo apt install wget -y)) \
	&& sudo mkdir -p -m 755 /etc/apt/keyrings \
	&& out=$(mktemp) && wget -nv -O$out https://cli.github.com/packages/githubcli-archive-keyring.gpg \
	&& cat $out | sudo tee /etc/apt/keyrings/githubcli-archive-keyring.gpg > /dev/null \
	&& sudo chmod go+r /etc/apt/keyrings/githubcli-archive-keyring.gpg \
	&& sudo mkdir -p -m 755 /etc/apt/sources.list.d \
	&& echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/githubcli-archive-keyring.gpg] https://cli.github.com/packages stable main" | sudo tee /etc/apt/sources.list.d/github-cli.list > /dev/null \
	&& sudo apt update \
	&& sudo apt install gh -y
```
Перевір версію і звідки вона:
```bash
gh version
apt-cache policy gh
```
```text
gh version 2.105.0 (2026-11-17)
https://github.com/cli/cli/releases/tag/v2.105.0
```
```text
gh:
  Installed: 2.105.0
  Candidate: 2.105.0
  Version table:
 *** 2.105.0 500
        500 https://cli.github.com/packages stable/main amd64 Packages
        100 /var/lib/dpkg/status
     2.45.0-1ubuntu0.3 500
        500 http://archive.ubuntu.com/ubuntu noble-updates/universe amd64 Packages
        500 http://security.ubuntu.com/ubuntu noble-security/universe amd64 Packages
     2.45.0-1build1 500
        500 http://archive.ubuntu.com/ubuntu noble/universe amd64 Packages
```
Зірочки `***` стоять біля версії з `cli.github.com` - так і треба. Нижче видно ту саму зламану 2.45.0 з репозиторію Ubuntu (на Mint замість `archive.ubuntu.com` може бути дзеркало). Твоя версія gh може бути новішою за 2.105.0 - це нормально. Оновлюється gh потім разом з усією системою (`sudo apt upgrade` або Менеджер оновлень).

**Крок 3. Налаштування.** Спершу глянь, що їх ще нема (буде помилка з «Передбач» 1), потім шість рядків:
```bash
git config --global --list
git config --global user.name "Твоє Імʼя"
git config --global user.email "128326252+Evge14n@users.noreply.github.com"
git config --global init.defaultBranch main
git config --global core.editor nano
git config --global pull.rebase false
git config --global core.quotepath false
git config --global --list
```
```text
user.name=Твоє Імʼя
user.email=128326252+Evge14n@users.noreply.github.com
init.defaultbranch=main
core.editor=nano
core.quotepath=false
pull.rebase=false
```
Зверни увагу: `init.defaultBranch` git показує малими літерами (`defaultbranch`) - назви ключів для git нечутливі до регістру.

**Крок 4. Звідки взялось кожне налаштування.** Запускай з домашньої теки (`cd ~`), не з репо:
```bash
cd ~
git config --list --show-origin
```
```text
file:/home/.../.gitconfig	user.name=Твоє Імʼя
file:/home/.../.gitconfig	user.email=128326252+Evge14n@users.noreply.github.com
file:/home/.../.gitconfig	init.defaultbranch=main
file:/home/.../.gitconfig	core.editor=nano
file:/home/.../.gitconfig	core.quotepath=false
file:/home/.../.gitconfig	pull.rebase=false
```
Якщо запустити це всередині репо, внизу додадуться рядки `file:.git/config` - налаштування саме цього репо. `--show-origin` рятує, коли «я ж налаштував, а git робить інакше»: видно, який файл перебиває.

**Крок 5. Сам файл** - звичайний текст, його можна відкрити й у nano:
```bash
cat ~/.gitconfig
git config user.name
```
```text
[user]
	name = Твоє Імʼя
	email = 128326252+Evge14n@users.noreply.github.com
[init]
	defaultBranch = main
[core]
	editor = nano
	quotepath = false
[pull]
	rebase = false
```
```text
Твоє Імʼя
```

**Мова виводу.** Курс показує вивід git англійською (так у перевірці і в більшості інструкцій в інтернеті). Пакет git в Ubuntu 24.04 сам не містить перекладів (перевірено: `dpkg -L git` - нуль файлів `.mo`), але на Mint з українською мовою переклад може прийти з мовного пакета, і тоді git писатиме українською (не перевірено на ноутбуці). Якщо так і хочеш англійською як у курсі - додавай `LANG=C` перед командою:
```text
LANG=C git status
```

**Для лаб:** після цього уроку кожен коміт у `~/univer/labs` буде підписаний «Твоє Імʼя» і noreply-поштою, а нові репо лаб одразу будуть з гілкою `main` - такою ж, як на GitHub, тож при першому `git push` (урок 09) нічого не доведеться перейменовувати.

### Типові помилки

**1. Коміт без налаштувань - `Author identity unknown`.** Ти це вже бачив у курсі Linux (День 09). Повний текст:
```text
Author identity unknown

*** Please tell me who you are.

Run

  git config --global user.email "you@example.com"
  git config --global user.name "Your Name"

to set your account's default identity.
Omit --global to set the identity only in this repository.

fatal: empty ident name (for <evgen@DESKTOP-HM5PR7N.localdomain>) not allowed
```
Останній рядок `fatal: ...` залежить від компʼютера: на Mint там може бути `unable to auto-detect email address` (не перевірено на ноутбуці). Лікування одне - крок 3.

**2. Помилка в назві ключа.** `user.nmae` збереглося мовчки (див. «Передбач» 3). Видно в списку:
```text
user.name=Твоє Імʼя
user.email=128326252+Evge14n@users.noreply.github.com
user.nmae=Твоє Імʼя
init.defaultbranch=main
...
```
Прибрати зайвий рядок:
```bash
git config --global --unset user.nmae
```

**3. Пропустив крапку в ключі** (`git config --global user "Імʼя"`):
```text
error: key does not contain a section: user
```
Ключ завжди `розділ.назва`: `user.name`, `core.editor`.

**4. gh з репозиторію Mint.** Якщо поставити `sudo apt install gh` без кроку 2, стане 2.45.0, і, наприклад, `gh pr view` падає з `GraphQL: Projects (classic) is being deprecated ...` (перевірено 18.11.2026 у Ubuntu 24.04, див. ФАКТИ). Лікування: виконати сніпет з кроку 2 - apt сам оновить gh до версії з `cli.github.com`.

**5. Справжня пошта замість noreply.** Коміти з `user.email` = особиста пошта після `git push` у публічний репо видно всім. Постав noreply (крок 3) до першого коміту.

### Як роблять профі

- **noreply-пошта і приховування пошти.** На сайті: аватарка → Settings → Emails → галочка «Keep my email addresses private». Тоді GitHub сам підставляє noreply-адресу в коміти, зроблені на сайті (docs.github.com, «Setting your commit email address»).
- **gh лише з офіційного репозиторію** - так радять самі автори gh з листопада 2025: версії 2.45/2.46 з репозиторіїв дистрибутивів зламані (cli/cli, `docs/install_linux.md`).
- **Конфіг тримають коротким і знають, де він.** `git config --list --show-origin` - перша команда, коли щось поводиться дивно. Відкрити весь файл у редакторі: `git config --global --edit` (відкриється nano, бо `core.editor`).
- **Корисні додаткові налаштування**, які часто вмикають (обидва ключі є в git 2.43 - перевірено `git help --config`):
  - `push.autoSetupRemote true` - перший `git push` нової гілки сам звʼязує її з GitHub (в уроці 09 ти робитимеш це руками через `push -u`, щоб розуміти, що відбувається);
  - `commit.verbose true` - у nano під час коміту видно, що саме ти комітиш.
- **Одна пошта на всі репо.** Якщо пошта в комітах різна, GitHub не привʼяже частину комітів до профілю. Тому `user.email` - глобально, а не в кожному репо окремо.

### Самоперевірка

1. Чому `gh` ставлять не з репозиторію Mint, а з `cli.github.com`?
2. У який файл пише `git config --global` і як його подивитись?
3. Навіщо `init.defaultBranch main`?
4. Що робить `--show-origin` і коли він допоможе?
5. Ти випадково записав `user.nmae`. Як це помітити і як прибрати?

<details markdown="1"><summary>Відповіді</summary>

1. У Mint (Ubuntu 24.04) лежить gh 2.45.0, і він зламаний: частина команд падає, бо GitHub прибрав старий API. Автори gh радять офіційний репозиторій.
2. У `~/.gitconfig`. Подивитись: `git config --global --list` або `cat ~/.gitconfig`.
3. Щоб нові репо одразу мали гілку `main`, як на GitHub, і git не писав довгу підказку про `master`.
4. Показує біля кожного налаштування файл, з якого воно взялось. Допомагає, коли налаштування з репо (`.git/config`) перебиває твоє глобальне.
5. Видно в `git config --global --list` (зайвий рядок `user.nmae=...`). Прибрати: `git config --global --unset user.nmae`.

</details>

### Джерела

- Pro Git, 1.6 «First-Time Git Setup» - https://git-scm.com/book/en/v2/Getting-Started-First-Time-Git-Setup (відкрито 18.11.2026)
- git config - https://git-scm.com/docs/git-config (відкрито 18.11.2026)
- GitHub CLI, встановлення на Linux - https://github.com/cli/cli/blob/trunk/docs/install_linux.md (відкрито 18.11.2026)
- Setting your commit email address - https://docs.github.com/en/account-and-profile/setting-up-and-managing-your-personal-account-on-github/managing-email-preferences/setting-your-commit-email-address (відкрито 18.11.2026)
- Вивід команд - запуск у перевірці `_перевірка/u02.sh` (git 2.43.0, Ubuntu 24.04, 18.11.2026)

## Тема 3. SSH-ключ і вхід у GitHub

**Навіщо:** щоб відправляти лаби на GitHub і забирати їх звідти без пароля щоразу. Паролем від акаунта git на GitHub не пускає з 13.08.2021, тому потрібен SSH-ключ (або токен, який gh тримає сам).

### Коротко

**SSH-ключ** - це пара файлів у теці `~/.ssh`:

| Файл | Що це | Кому показувати |
|---|---|---|
| `id_ed25519` | **приватний** ключ, права `600` (читати може лише твій користувач) | **нікому і ніколи**: ні викладачу, ні в чат, ні на GitHub |
| `id_ed25519.pub` | **публічний** ключ (`.pub` = public) | GitHub, будь-кому - він не дає доступу сам по собі |

Аналогія: публічний ключ - це навісний замок, приватний - єдиний ключ від нього. Замок (`.pub`) ти вішаєш на свій акаунт GitHub. Відкрити його може лише той, у кого в кишені ключ (`id_ed25519`), тобто твій ноутбук. Копій замка можна роздати скільки завгодно - без ключа вони марні. А от хто отримав копію приватного ключа, той заходить на GitHub як ти.

**Відбиток (fingerprint)** - короткий «підпис» ключа на кшталт `SHA256:1EvICMx4...`. Довгі ключі незручно порівнювати очима, а відбитки - зручно.

Перевірка йде в обидва боки:
```text
 ноутбук                                     GitHub
 ~/.ssh/id_ed25519      ── доводить ──►      «це Evge14n» (знає твій .pub)
 ~/.ssh/known_hosts     ◄── доводить ──      «це справжній github.com»
                                             (відбиток SHA256:+DiY3wvvV6TuJJhbpZisF/zLDA0zPMSvHdkr4UvCOqU)
```

| Команда | Що робить |
|---|---|
| `ssh-keygen -t ed25519 -C "пошта"` | створити пару ключів |
| `ssh-keygen -lf ~/.ssh/id_ed25519.pub` | показати відбиток ключа |
| `cat ~/.ssh/id_ed25519.pub` | показати публічний ключ (щоб скопіювати на сайт) |
| `ssh -T git@github.com` | перевірити, чи пускає GitHub |
| `gh auth login -p ssh -w` | усе через gh: вхід у браузері + завантаження ключа |

Два шляхи: **А** - руками (ключ + сайт), **Б** - через gh. Результат однаковий, обери один.

### Передбач, потім запусти

1. Ключ створено. Які права покаже `ls -l ~/.ssh` у приватного і публічного ключа?
<details markdown="1"><summary>Відповідь</summary>

```text
-rw------- 1 ... id_ed25519
-rw-r--r-- 1 ... id_ed25519.pub
```
Приватний читає і пише лише власник (`600`), публічний можуть читати всі (`644`).
</details>

2. Що покаже `ssh-keygen -lf ~/.ssh/id_ed25519.pub`?
<details markdown="1"><summary>Відповідь</summary>

Один рядок: розмір, відбиток, коментар (твоя пошта) і тип:
```text
256 SHA256:1EvICMx4RFQiriSXCeU4r5KAe5gIDOPxXnihEQYW0Ng 128326252+Evge14n@users.noreply.github.com (ED25519)
```
Відбиток у тебе буде інший - ключ щоразу генерується випадково.
</details>

3. Ти вдруге запустив ту саму `ssh-keygen -t ed25519 ...`. Що буде?
<details markdown="1"><summary>Відповідь</summary>

```text
/home/.../.ssh/id_ed25519 already exists.
Overwrite (y/n)?
```
Відповідай `n`. Якщо `y` - старий ключ зникне, і GitHub перестане тебе пускати, поки не додаси новий.
</details>

4. `ssh -T git@github.com` написав «You've successfully authenticated». Який буде код виходу (`echo $?`)?
<details markdown="1"><summary>Відповідь</summary>

`1`. Це нормально: GitHub пустив, але не дає командного рядка (shell), тому сеанс одразу закривається з кодом 1 (docs.github.com, «Testing your SSH connection»).
</details>

### Руками

#### Шлях А. Ключ руками і сайт

**Крок 1. Створи ключ.** На всі питання тисни Enter (місце за замовчуванням і порожня пароль-фраза; про пароль-фразу - в «Як роблять профі»).
```bash
ssh-keygen -t ed25519 -C "128326252+Evge14n@users.noreply.github.com"
```
```text
Generating public/private ed25519 key pair.
Enter file in which to save the key (/home/.../.ssh/id_ed25519):
Created directory '/home/.../.ssh'.
Enter passphrase (empty for no passphrase):
Enter same passphrase again:
Your identification has been saved in /home/.../.ssh/id_ed25519
Your public key has been saved in /home/.../.ssh/id_ed25519.pub
The key fingerprint is:
SHA256:1EvICMx4RFQiriSXCeU4r5KAe5gIDOPxXnihEQYW0Ng 128326252+Evge14n@users.noreply.github.com
The key's randomart image is:
+--[ED25519 256]--+
|+O=X*..          |
|o=E+=o o o       |
|*o*o .. + o      |
|B*o + .. . .     |
|=o.+ o  S .      |
|+*. o            |
|O ..             |
|..               |
|                 |
+----[SHA256]-----+
```
`-t ed25519` - тип ключа (сучасний, короткий), `-C` - коментар, щоб на сайті було видно, чий ключ. `Created directory` буде, лише якщо теки `~/.ssh` ще не було. Пароль-фраза при наборі не видно - це нормально.

**Крок 2. Подивись, що вийшло.**
```bash
ls -l ~/.ssh
ssh-keygen -lf ~/.ssh/id_ed25519.pub
cat ~/.ssh/id_ed25519.pub
```
```text
total 8
-rw------- 1 evgen evgen 444 Nov 18 10:15 id_ed25519
-rw-r--r-- 1 evgen evgen 124 Nov 18 10:15 id_ed25519.pub
```
```text
256 SHA256:1EvICMx4RFQiriSXCeU4r5KAe5gIDOPxXnihEQYW0Ng 128326252+Evge14n@users.noreply.github.com (ED25519)
```
```text
ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIGlkZTr+dT3xLmCXdI04a813+vXMlodgm4heFoijeM3i 128326252+Evge14n@users.noreply.github.com
```
Останній рядок - це і є публічний ключ. Виділи його мишкою від `ssh-ed25519` до кінця пошти і скопіюй: у терміналі Mint це **Ctrl+Shift+C**. Файл `id_ed25519` (без `.pub`) **не відкривай і не копіюй нікуди**.

**Крок 3. Додай ключ на GitHub.**
```text
github.com → аватарка (вгорі праворуч) → Settings → розділ «Access» → SSH and GPG keys → New SSH key
  Title:     ноутбук Mint
  Key type:  Authentication Key
  Key:       встав рядок ssh-ed25519 ... (Ctrl+V у браузері)
→ Add SSH key
```
У списку ключів GitHub покаже відбиток `SHA256:...` - він має збігатися з тим, що дав `ssh-keygen -lf`.

**Крок 4. ssh-agent** - програма, яка тримає розблокований ключ у памʼяті, щоб не вводити пароль-фразу щоразу. Якщо пароль-фрази нема, цей крок можна пропустити. На Mint Cinnamon агент зазвичай уже запущений сесією (не перевірено на ноутбуці); зайвим не буде:
```bash
eval "$(ssh-agent -s)"
ssh-add ~/.ssh/id_ed25519
```

**Крок 5. Перевір вхід.**
```bash
ssh -T git@github.com
echo $?
```
Першого разу ssh не знає github.com і питає (вивід справжній, 18.11.2026):
```text
The authenticity of host 'github.com (140.82.121.4)' can't be established.
ED25519 key fingerprint is SHA256:+DiY3wvvV6TuJJhbpZisF/zLDA0zPMSvHdkr4UvCOqU.
This key is not known by any other names.
Are you sure you want to continue connecting (yes/no/[fingerprint])?
```
IP-адреса може бути інша. **Звір відбиток** з офіційним `SHA256:+DiY3wvvV6TuJJhbpZisF/zLDA0zPMSvHdkr4UvCOqU` (docs «GitHub's SSH key fingerprints»). Збігається - набери `yes` і Enter. Далі:
```text
Warning: Permanently added 'github.com' (ED25519) to the list of known hosts.
Hi Evge14n! You've successfully authenticated, but GitHub does not provide shell access.
```
```text
1
```
Відбиток github.com записано у `~/.ssh/known_hosts`, більше ssh не питатиме.

#### Шлях Б. Через gh

gh (встановлений в уроці 02) сам знайде `~/.ssh/id_ed25519.pub` і запропонує завантажити його на GitHub; якщо ключа нема - запропонує створити (cli.github.com/manual/gh_auth_login).
```bash
gh auth login -p ssh -w
gh auth status
```
`-p ssh` - git працюватиме через SSH, `-w` - вхід через браузер. gh покаже одноразовий код, відкриє github.com, ти вставиш код і натиснеш Authorize. Точні питання gh можуть трохи відрізнятись (не перевірено: курс не входить у справжній акаунт). Після цього - той самий крок 5 (`ssh -T git@github.com`).

#### Пісочниця: приватний репо pisochnytsia

Тут можна ламати що завгодно - це для вправ уроків 04-16.

На сайті:
```text
github.com → «+» вгорі праворуч (Create something new) → New repository
  Repository name:  pisochnytsia
  Visibility:       Private
  README:           увімкни «Add README» (галочка або перемикач, назва може трохи відрізнятись)
→ Create repository
```
Або одним рядком через gh:
```bash
gh repo create pisochnytsia --private --add-readme
```
Клонуй собі в домашню теку. Адресу SSH видно на сайті: зелена кнопка **Code** → вкладка **SSH**.
```bash
git clone git@github.com:Evge14n/pisochnytsia.git ~/pisochnytsia
cd ~/pisochnytsia
ls
git log --oneline
git remote -v
```
```text
Cloning into '/home/.../pisochnytsia'...
```
Далі git покаже кілька рядків про завантаження (`remote: ...`, `Receiving objects: 100% ...`).
```text
README.md
```
```text
0ee5c1c Initial commit
```
```text
origin	git@github.com:Evge14n/pisochnytsia.git (fetch)
origin	git@github.com:Evge14n/pisochnytsia.git (push)
```
`origin` - стандартне імʼя для «репо, звідки клонували» (урок 09).

**Для лаб:** у Лабах в git ти створиш так само приватний репо `univer-labs` і клонуватимеш його цією ж SSH-адресою. Ключ робиться один раз на ноутбук. Новий ноутбук або перевстановив Mint - новий ключ, а старий видали на сайті.

### Типові помилки

**1. `Permission denied (publickey)`** (перевірено 18.11.2026 справжнім підключенням з ключем, якого нема на GitHub):
```text
git@github.com: Permission denied (publickey).
```
GitHub не знайшов твій публічний ключ. Причини: не додав `.pub` на сайт (крок 3), додав інший ключ, або ssh бере не той файл. Порівняй `ssh-keygen -lf ~/.ssh/id_ed25519.pub` з відбитком у Settings → SSH and GPG keys.

**2. Права на приватний ключ.** Якщо файл `id_ed25519` можуть читати інші (наприклад, після копіювання з флешки), ssh його ігнорує:
```text
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
@         WARNING: UNPROTECTED PRIVATE KEY FILE!          @
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
Permissions 0644 for '/home/.../.ssh/id_ed25519' are too open.
It is required that your private key files are NOT accessible by others.
This private key will be ignored.
Load key "/home/.../.ssh/id_ed25519": bad permissions
```
Лікування:
```bash
chmod 600 ~/.ssh/id_ed25519
```

**3. `Overwrite (y/n)?`** - ключ уже є (див. «Передбач» 3). Відповідай `n`.

**4. Відбиток github.com не збігається** з `SHA256:+DiY3wvvV6TuJJhbpZisF/zLDA0zPMSvHdkr4UvCOqU`. **Не пиши yes.** Можливо, мережа підмінює сервер (наприклад, чужий Wi-Fi). Спробуй з іншої мережі.

**5. Клонував за HTTPS-адресою** (`https://github.com/...`). Тоді git питає логін і пароль, а пароль від акаунта не підходить. Переключи репо на SSH:
```bash
git remote set-url origin git@github.com:Evge14n/pisochnytsia.git
```

**6. Показав приватний ключ** (вставив `id_ed25519` у чат, на сайт, у скриншот). Вважай його вкраденим: видали ключ на сайті (Settings → SSH and GPG keys → Delete), створи новий і додай знову.

### Як роблять профі

- **Ed25519** - тип, який першим пропонує документація GitHub; RSA 4096 лише для старих систем, що не знають Ed25519 (docs «Generating a new SSH key»).
- **Пароль-фраза + ssh-agent.** Тоді вкрадений файл ключа без пароль-фрази марний, а вводиш її раз за сеанс (docs).
- **Один ключ на пристрій** з назвою в Title («ноутбук Mint»). Загубив пристрій - видалив один ключ, інші працюють.
- **Двофакторний вхід (2FA).** З березня 2023 GitHub вимагає 2FA від усіх, хто робить внесок кодом на github.com; основний спосіб - застосунок з одноразовими кодами (TOTP), ключ безпеки чи passkey - як запасний (docs «About mandatory two-factor authentication»).
- **Підпис комітів тим самим SSH-ключем** (git 2.34+): GitHub ставить біля таких комітів позначку «Verified» (docs «About commit signature verification»). Для лаб не обовʼязково.
- **Відбиток github.com можна перевірити заздалегідь**, ще до першого підключення:
```bash
ssh-keyscan -t ed25519 github.com | ssh-keygen -lf -
```
```text
256 SHA256:+DiY3wvvV6TuJJhbpZisF/zLDA0zPMSvHdkr4UvCOqU github.com (ED25519)
```

### Самоперевірка

1. Чим приватний ключ відрізняється від публічного і який з них іде на GitHub?
2. Які права мають бути в `~/.ssh/id_ed25519` і як їх виставити?
3. Що робити, якщо при першому `ssh -T git@github.com` відбиток не `SHA256:+DiY3...`?
4. `ssh -T git@github.com` вивів «Hi Evge14n!...» і код 1. Це помилка?
5. Ти вставив вміст `id_ed25519` в чат з одногрупником. Що робиш?

<details markdown="1"><summary>Відповіді</summary>

1. Приватний (`id_ed25519`) лишається лише на ноутбуці і доводить, що це ти. Публічний (`id_ed25519.pub`) кладеш на GitHub, він сам доступу не дає.
2. `600` (читати і писати лише власнику): `chmod 600 ~/.ssh/id_ed25519`.
3. Не писати yes, перервати (Ctrl+C), спробувати з іншої мережі і звірити з docs «GitHub's SSH key fingerprints».
4. Ні. GitHub пустив, а код 1 - бо він не дає командного рядка.
5. Видаляю цей ключ на сайті (Settings → SSH and GPG keys), створюю новий, додаю його на сайт і перевіряю `ssh -T git@github.com`.

</details>

### Джерела

- Generating a new SSH key and adding it to the ssh-agent - https://docs.github.com/en/authentication/connecting-to-github-with-ssh/generating-a-new-ssh-key-and-adding-it-to-the-ssh-agent (відкрито 18.11.2026)
- Adding a new SSH key to your GitHub account - https://docs.github.com/en/authentication/connecting-to-github-with-ssh/adding-a-new-ssh-key-to-your-github-account (відкрито 18.11.2026, за ФАКТИ-GIT)
- Testing your SSH connection - https://docs.github.com/en/authentication/connecting-to-github-with-ssh/testing-your-ssh-connection (відкрито 18.11.2026, за ФАКТИ-GIT)
- GitHub's SSH key fingerprints - https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/githubs-ssh-key-fingerprints (відкрито 18.11.2026, за ФАКТИ-GIT)
- gh auth login - https://cli.github.com/manual/gh_auth_login (відкрито 18.11.2026)
- Creating a new repository - https://docs.github.com/en/repositories/creating-and-managing-repositories/creating-a-new-repository (відкрито 18.11.2026)
- About mandatory two-factor authentication - https://docs.github.com/en/authentication/securing-your-account-with-two-factor-authentication-2fa/about-mandatory-two-factor-authentication (відкрито 18.11.2026)
- About commit signature verification - https://docs.github.com/en/authentication/managing-commit-signature-verification/about-commit-signature-verification (відкрито 18.11.2026)
- github.blog, «Token authentication requirements for Git operations» - пароль для git не приймається з 13.08.2021 (за ФАКТИ-GIT; саму сторінку не відкривав)
- Вивід команд - запуск у перевірці `_перевірка/u03.sh` (OpenSSH 9.6p1, git 2.43.0, Ubuntu 24.04, 18.11.2026)

## Тема 4. Перший репозиторій - init, clone, status, add, commit

**Навіщо:** це цикл, який ти робитимеш у кожній лабі десятки разів: змінив код → подивився `status` → `add` → `commit` з нормальним повідомленням. Через тиждень по повідомленнях буде видно, де яке завдання ЛР.

### Коротко

Репо можна отримати двома способами:
```text
git init                    нова тека → нове порожнє репо, лише на ноутбуці
git clone git@github.com:Evge14n/pisochnytsia.git ~/pisochnytsia
                            копія репо з GitHub, уже з історією і звʼязком origin
```

| Команда | Що робить |
|---|---|
| `git init` | зробити поточну теку репозиторієм (один раз) |
| `git clone АДРЕСА ТЕКА` | скопіювати репо з GitHub |
| `git status` | що змінено, що в індексі, на якій гілці |
| `git add lr1.py` | покласти файл в індекс (`git add .` - усе в поточній теці) |
| `git commit -m "Текст"` | коміт з коротким повідомленням |
| `git commit` | коміт з довгим повідомленням: відкриється nano |
| `git commit -am "Текст"` | `add` для **вже відстежуваних** файлів + коміт одним рядком |
| `git log` / `git log --oneline` | історія повністю / по рядку на коміт (детально - урок 05) |

**Гарне повідомлення коміту** (Pro Git, 5.2):
- перший рядок - до ~50 знаків, коротко **що змінено**;
- якщо треба пояснити **чому** - порожній рядок, далі текст з переносом рядків приблизно на 72 знаки;
- наказовий спосіб: «Fix bug», а не «Fixed bug». Українською: «Додай перевірку вводу в завд. 2» або безособово «Завдання 2: перевірка вводу».

| Погано | Добре |
|---|---|
| `зміни` | `Додай ввід x у ЛР1` |
| `asdf` | `ЛР2 завд. 1: сума двох чисел` |
| `виправив` | `Виправ ділення на нуль у завд. 3` |
| `ЛР3 повністю` (усе одним комітом за тиждень) | кілька комітів, по одному на завдання |

Аналогія: повідомлення коміту - як підпис під фото в альбомі. «Фото» нічого не скаже через місяць, «Захист ЛР2, 25.11» - скаже.

### Передбач, потім запусти

1. Щойно зробив коміт, нічого не змінював і знову пишеш `git commit -m "ще"`. Що буде?
<details markdown="1"><summary>Відповідь</summary>

```text
On branch main
nothing to commit, working tree clean
```
Коміту не буде (код виходу 1): немає що знімати.
</details>

2. Дописав рядок у `lr1.py`, але забув `git add` і пишеш `git commit -m "Зміни"`. Що буде?
<details markdown="1"><summary>Відповідь</summary>

```text
On branch main
Changes not staged for commit:
  (use "git add <file>..." to update what will be committed)
  (use "git restore <file>..." to discard changes in working directory)
	modified:   lr1.py

no changes added to commit (use "git add" and/or "git commit -a")
```
Індекс порожній, тож коміту нема. git підказує: `git add` або `git commit -a`.
</details>

3. Змінив `lr1.py` і створив **новий** `lr2.py`. Робиш `git commit -am "..."`. Що покаже потім `git status --short`?
<details markdown="1"><summary>Відповідь</summary>

```text
?? lr2.py
```
`-a` бере лише файли, за якими git уже стежить. Новий файл треба один раз додати руками: `git add lr2.py`.
</details>

4. У клоні `~/pisochnytsia` зробив коміт. Що напише `git status`?
<details markdown="1"><summary>Відповідь</summary>

```text
On branch main
Your branch is ahead of 'origin/main' by 1 commit.
  (use "git push" to publish your local commits)

nothing to commit, working tree clean
```
Твій `main` на 1 коміт попереду копії з GitHub. На сайті цього коміту ще нема - його треба відправити `git push` (урок 09).
</details>

### Руками

**Крок 1. Нове репо і перший коміт** (локальна пісочниця, GitHub не потрібен):
```bash
mkdir ~/git-pisochnytsia
cd ~/git-pisochnytsia
git init
printf 'print("Привіт, ЛР1")\n' > lr1.py
git status
```
```text
Initialized empty Git repository in /home/.../git-pisochnytsia/.git/
```
```text
On branch main

No commits yet

Untracked files:
  (use "git add <file>..." to include in what will be committed)
	lr1.py

nothing added to commit but untracked files present (use "git add" to track)
```
«Untracked» - git бачить файл, але не стежить за ним.
```bash
git add lr1.py
git status
git commit -m "Додай заготовку ЛР1"
git status
git log
```
```text
On branch main

No commits yet

Changes to be committed:
  (use "git rm --cached <file>..." to unstage)
	new file:   lr1.py

```
```text
[main (root-commit) 3347fd3] Додай заготовку ЛР1
 1 file changed, 1 insertion(+)
 create mode 100644 lr1.py
```
```text
On branch main
nothing to commit, working tree clean
```
```text
commit 3347fd379f6d43f5d82154561a80118b691cfeed
Author: Твоє Імʼя <128326252+Evge14n@users.noreply.github.com>
Date:   Wed Nov 18 10:29:45 2026 +0000

    Додай заготовку ЛР1
```
«working tree clean» - усе, що є в теці, вже в коміті. Хеші і час у тебе будуть інші.

**Крок 2. Забув add і `commit -am`** («Передбач» 1-3):
```bash
git commit -m "ще"
printf 'x = int(input())\n' >> lr1.py
git commit -m "Зміни"
printf 'print("ЛР2")\n' > lr2.py
git commit -am "Додай ввід x у ЛР1"
git status --short
```
```text
[main f30faf1] Додай ввід x у ЛР1
 1 file changed, 1 insertion(+)
```
```text
?? lr2.py
```
У коміт пішов лише `lr1.py`, новий `lr2.py` лишився поза git.

**Крок 3. Довге повідомлення через nano.**
```bash
git add lr2.py
git commit
```
Відкриється nano з таким текстом:
```text

# Please enter the commit message for your changes. Lines starting
# with '#' will be ignored, and an empty message aborts the commit.
#
# On branch main
# Changes to be committed:
#	new file:   lr2.py
#
```
Рядки з `#` git викине. У перший (порожній) рядок напиши:
```text
Почни ЛР2: заготовка програми

Поки що лише друк назви. Далі завдання 1 з методички:
ввід двох чисел і їхня сума.
```
Збережи **Ctrl+O**, Enter, вийди **Ctrl+X**.
```text
[main 3b15e01] Почни ЛР2: заготовка програми
 1 file changed, 1 insertion(+)
 create mode 100644 lr2.py
```
```bash
git log -n 1
git log --oneline
```
```text
commit 3b15e019a929b8b85c66f342bd15b811160bc90b
Author: Твоє Імʼя <128326252+Evge14n@users.noreply.github.com>
Date:   Wed Nov 18 10:29:45 2026 +0000

    Почни ЛР2: заготовка програми
    
    Поки що лише друк назви. Далі завдання 1 з методички:
    ввід двох чисел і їхня сума.
```
```text
3b15e01 Почни ЛР2: заготовка програми
f30faf1 Додай ввід x у ЛР1
3347fd3 Додай заготовку ЛР1
```
`--oneline` показує лише перший рядок - тому він і має бути коротким і зрозумілим сам по собі.

**Крок 4. Коміт у клоні з GitHub.** Клон `~/pisochnytsia` ти зробив в уроці 03. Якщо ще ні:
```bash
git clone git@github.com:Evge14n/pisochnytsia.git ~/pisochnytsia
```
```bash
cd ~/pisochnytsia
git status
printf 'print("Привіт з ноутбука")\n' > pryvit.py
git add pryvit.py
git commit -m "Додай pryvit.py"
git status
```
```text
On branch main
Your branch is up to date with 'origin/main'.

nothing to commit, working tree clean
```
```text
[main 7351312] Додай pryvit.py
 1 file changed, 1 insertion(+)
 create mode 100644 pryvit.py
```
```text
On branch main
Your branch is ahead of 'origin/main' by 1 commit.
  (use "git push" to publish your local commits)

nothing to commit, working tree clean
```
Різниця з `git init`: клон знає про `origin/main` (копію з GitHub) і показує, чи ти попереду. Відправиш коміт в уроці 09.

**Для лаб:** у теці лаби цикл той самий: розвʼязав завдання і doctest проходить → `git status` → `git add lr3.py` → `git commit -m "ЛР3 завд. 2: таблиця значень"`. Не роби `git add .` наосліп: спершу `git status`, щоб у коміт не потрапили `.venv/`, картинки чи чернетки (від цього захищає `.gitignore`, урок 06).

### Типові помилки

**1. Помилка в назві файлу або не та тека:**
```text
fatal: pathspec 'lr3.py' did not match any files
```
Такого файлу тут нема. Перевір `ls` і `pwd`, назву (регістр важливий: `LR3.py` ≠ `lr3.py`).

**2. Закрив nano, нічого не написавши** (або лише рядки з `#`):
```text
Aborting commit due to empty commit message.
```
Коміту нема, але файли лишились в індексі. Просто зроби `git commit` ще раз і напиши повідомлення.

**3. Клонуєш удруге в ту саму теку:**
```text
fatal: destination path '/home/.../pisochnytsia' already exists and is not an empty directory.
```
Клон уже є - просто `cd ~/pisochnytsia`. Друга копія потрібна? Дай іншу назву теки в кінці команди.

**4. Повідомлення «зміни», «фікс», «aaa».** git їх приймає, але через тиждень не зрозуміло, який коміт повертати. Пиши, що саме змінено (таблиця в «Коротко»).

### Як роблять профі

- **50/72 і наказовий спосіб** - стандарт з Pro Git 5.2, його ж чекають у більшості відкритих проєктів.
- **Один коміт - одна логічна зміна** («make each commit a logically separate changeset», Pro Git 5.2). Не «ЛР3 повністю», а коміт на завдання.
- **Conventional Commits** - у багатьох командах перший рядок має тип: `feat: ...` (нова можливість), `fix: ...` (виправлення помилки), бо з таких повідомлень програми автоматично складають список змін (conventionalcommits.org, v1.0.0). Для лаб не обовʼязково, але впізнаватимеш у чужих репо.
- **`git add -p`** - додати в індекс не весь файл, а вибрані шматки (hunk). git показує кожен шматок і питає `y` (додати) чи `n` (ні):
```bash
printf 'print(x * 2)\n' >> ~/git-pisochnytsia/lr1.py
cd ~/git-pisochnytsia
git add -p lr1.py
```
```text
diff --git a/lr1.py b/lr1.py
index b72a1f6..419e6aa 100644
--- a/lr1.py
+++ b/lr1.py
@@ -1,2 +1,3 @@
 print("Привіт, ЛР1")
 x = int(input())
+print(x * 2)
(1/1) Stage this hunk [y,n,q,a,d,e,?]? 
```
  Набери `y` і Enter. Так з одного файлу можна зробити два акуратні коміти: виправлення окремо, налагоджувальний `print` - не комітити взагалі.
- **`commit.verbose true`** (урок 02) - у nano під час коміту видно саму зміну, легше написати точне повідомлення.

### Самоперевірка

1. Чим `git init` відрізняється від `git clone`?
2. Ти змінив `lr1.py` і пишеш `git commit -m "..."` без `add`. Що буде і чому?
3. Що робить `git commit -am` і чого він НЕ робить?
4. Які правила гарного повідомлення коміту з Pro Git?
5. Що означає «Your branch is ahead of 'origin/main' by 1 commit.»?

<details markdown="1"><summary>Відповіді</summary>

1. `git init` робить нове порожнє репо на ноутбуці. `git clone` копіює вже наявне репо з GitHub разом з історією і звʼязком `origin`.
2. «no changes added to commit»: коміт бере лише індекс, а він порожній. Треба `git add lr1.py` або `git commit -am`.
3. Додає в індекс зміни вже відстежуваних файлів і робить коміт. Нові (untracked) файли не додає.
4. Перший рядок до ~50 знаків, порожній рядок, пояснення з переносом ~72; наказовий спосіб («Додай ...», «Виправ ...»).
5. На ноутбуці є 1 коміт, якого ще нема на GitHub. Його треба відправити `git push`.

</details>

### Джерела

- Pro Git, 2.2 «Recording Changes to the Repository» - https://git-scm.com/book/en/v2/Git-Basics-Recording-Changes-to-the-Repository (відкрито 18.11.2026)
- Pro Git, 5.2 «Contributing to a Project» (Commit Guidelines) - https://git-scm.com/book/en/v2/Distributed-Git-Contributing-to-a-Project (відкрито 18.11.2026)
- git commit - https://git-scm.com/docs/git-commit (відкрито 18.11.2026)
- git add (`-p`) - https://git-scm.com/docs/git-add (відкрито 18.11.2026)
- Conventional Commits 1.0.0 - https://www.conventionalcommits.org/en/v1.0.0/ (відкрито 18.11.2026)
- Вивід команд - запуск у перевірці `_перевірка/u04.sh` (git 2.43.0, Ubuntu 24.04, 18.11.2026)

## Тема 5. Історія - log, diff, show

**Навіщо:** у ЛР3 вчора все працювало, сьогодні doctest падає. Історія git відповідає на три питання: що я міняв, коли і як файл виглядав раніше. Без неї ти шукаєш помилку наосліп.

### Коротко

Коміти лежать ланцюжком: кожен знає свого «батька» (попередній коміт). `HEAD` - це «де я зараз», тобто останній коміт поточної гілки.

```text
27d6c77 ← 10bffb8 ← 228f08c ← HEAD
(double)  (README)  (triple)

HEAD~1 = на 1 коміт назад (10bffb8)
HEAD~2 = на 2 коміти назад (27d6c77)
```

| Команда | Що показує |
|---|---|
| `git log` | усі коміти: хеш, автор, дата, повідомлення (новий зверху) |
| `git log --oneline` | те саме коротко: 7 знаків хешу + повідомлення |
| `git log --oneline -n 2` | лише 2 останні коміти |
| `git log --stat -n 1` | останній коміт + які файли і скільки рядків змінено |
| `git log --oneline -- README.md` | лише коміти, які чіпали цей файл |
| `git log --oneline --graph --all` | усі гілки малюнком (знадобиться в уроці 07) |
| `git diff` | що змінено в робочій теці, але ще НЕ додано (`add`) |
| `git diff --staged` | що вже додано і піде в наступний коміт |
| `git show` | останній коміт разом з його змінами |
| `git show HEAD~2:lr1.py` | файл таким, яким він був 2 коміти тому |
| `git blame lr1.py` | для кожного рядка: який коміт і хто його написав |

Як читати `diff`: рядок з `-` прибрали, рядок з `+` додали, рядки з пробілом на початку - контекст (не змінились). `@@ -3,4 +3,4 @@` - «шматок від 3-го рядка, 4 рядки».

Аналогія: `git log` - це зміст зошита з датами, `git show` - одна сторінка, `git diff` - що ти дописав олівцем і ще не обвів ручкою.

Довгий вивід `git log` відкривається в програмі перегляду (pager): гортай стрілками або пробілом, вийти - клавіша `q`.

### Пісочниця

Нова тека лише для цього уроку, три коміти (`printf ... >>` дописує в кінець файлу):

```bash
mkdir ~/git-pisochnytsia-05
cd ~/git-pisochnytsia-05
git init
printf 'def double(x):\n    return x * 2\n' > lr1.py
git add lr1.py
git commit -m "ЛР1: функція double"
printf '# Мої лаби\n' > README.md
git add README.md
git commit -m "Додай README"
printf '\n\ndef triple(x):\n    return x * 3\n' >> lr1.py
git commit -am "ЛР1: функція triple"
```

Перший коміт пише так:

```text
[main (root-commit) 27d6c77] ЛР1: функція double
 1 file changed, 2 insertions(+)
 create mode 100644 lr1.py
```

`root-commit` - «коміт без батька», найперший. **У тебе хеші й дати будуть інші** (хеш залежить від часу й автора) - це нормально, дивись на будову виводу.

### Передбач, потім запусти

1. `git log --oneline -n 1` - який коміт покаже: перший чи останній?
<details markdown="1"><summary>Відповідь</summary>

Останній: новий завжди зверху. `(HEAD -> main)` - «ти тут, на гілці main».
```text
228f08c (HEAD -> main) ЛР1: функція triple
```
</details>

2. `git log --oneline -- README.md` - скільки рядків буде?
<details markdown="1"><summary>Відповідь</summary>

Один: README змінював лише один коміт. `--` відділяє назви файлів від решти.
```text
10bffb8 Додай README
```
</details>

3. `git show HEAD~2:lr1.py` - що виведе?
<details markdown="1"><summary>Відповідь</summary>

Файл з найпершого коміту, ще без `triple`. Робоча тека при цьому не змінюється - це лише показ.
```text
def double(x):
    return x * 2
```
</details>

### Руками

**Крок 1. Усі види log.**

```bash
git log
```
```text
commit 228f08c9c75289074d6c150c847c63d52ef76502 (HEAD -> main)
Author: Твоє Імʼя <128326252+Evge14n@users.noreply.github.com>
Date:   Wed Nov 18 14:09:00 2026 +0200

    ЛР1: функція triple

commit 10bffb830ea0342d178c79b80cac40ac20c5d1de
Author: Твоє Імʼя <128326252+Evge14n@users.noreply.github.com>
Date:   Wed Nov 18 14:06:00 2026 +0200

    Додай README

commit 27d6c77ad6890c4d92ada320eb61ca3ee8a23159
Author: Твоє Імʼя <128326252+Evge14n@users.noreply.github.com>
Date:   Wed Nov 18 14:03:00 2026 +0200

    ЛР1: функція double
```

Повний хеш - 40 знаків. Скрізь, де треба вказати коміт, вистачає перших 7 (`228f08c`).

```bash
git log --oneline
git log --stat -n 1
```
```text
228f08c (HEAD -> main) ЛР1: функція triple
10bffb8 Додай README
27d6c77 ЛР1: функція double
```
```text
commit 228f08c9c75289074d6c150c847c63d52ef76502 (HEAD -> main)
Author: Твоє Імʼя <128326252+Evge14n@users.noreply.github.com>
Date:   Wed Nov 18 14:09:00 2026 +0200

    ЛР1: функція triple

 lr1.py | 4 ++++
 1 file changed, 4 insertions(+)
```

4 рядки, бо два порожні рядки перед `def triple` теж рахуються.

**Крок 2. diff: до `add` і після.** Міняємо 3 на 4 (наче випадково):

```bash
sed -i 's/x \* 3/x * 4/' lr1.py
git diff
```
```text
diff --git a/lr1.py b/lr1.py
index c5825fd..a12de39 100644
--- a/lr1.py
+++ b/lr1.py
@@ -3,4 +3,4 @@ def double(x):
 
 
 def triple(x):
-    return x * 3
+    return x * 4
```

Тепер додай і знову спитай `git diff`:

```bash
git add lr1.py
git diff
git diff --staged
```

Перший `git diff` - **порожньо**. Зміна нікуди не зникла: вона переїхала в індекс, і її показує `git diff --staged` (той самий текст, що вище). Звідси правило: перед `git commit` глянь `git diff --staged` - побачиш рівно те, що піде в коміт.

```bash
git commit -m "ЛР1: triple множить на 4"
```

**Крок 3. show і blame.**

```bash
git show
```
```text
commit c31063a0603f59f6ed8bd5ce73761102df2a7dac (HEAD -> main)
Author: Твоє Імʼя <128326252+Evge14n@users.noreply.github.com>
Date:   Wed Nov 18 14:12:00 2026 +0200

    ЛР1: triple множить на 4

diff --git a/lr1.py b/lr1.py
index c5825fd..a12de39 100644
--- a/lr1.py
+++ b/lr1.py
@@ -3,4 +3,4 @@ def double(x):
 
 
 def triple(x):
-    return x * 3
+    return x * 4
```

Порівняти два будь-які коміти (тут: 2 коміти тому і зараз), лише список файлів:

```bash
git diff HEAD~2 HEAD --stat
```
```text
 lr1.py | 4 ++++
 1 file changed, 4 insertions(+)
```

Хто і коли написав кожен рядок:

```bash
git blame lr1.py
```
```text
^27d6c77 (Твоє Імʼя 2026-11-18 14:03:00 +0200 1) def double(x):
^27d6c77 (Твоє Імʼя 2026-11-18 14:03:00 +0200 2)     return x * 2
228f08c9 (Твоє Імʼя 2026-11-18 14:09:00 +0200 3) 
228f08c9 (Твоє Імʼя 2026-11-18 14:09:00 +0200 4) 
228f08c9 (Твоє Імʼя 2026-11-18 14:09:00 +0200 5) def triple(x):
c31063a0 (Твоє Імʼя 2026-11-18 14:12:00 +0200 6)     return x * 4
```

`^` перед хешем - це найперший коміт. Рядок 6 змінив останній коміт - ось де шукати, хто «зламав» `triple`.

І малюнок історії (поки пряма лінія, гілки будуть в уроці 07):

```bash
git log --oneline --graph --all
```
```text
* c31063a (HEAD -> main) ЛР1: triple множить на 4
* 228f08c ЛР1: функція triple
* 10bffb8 Додай README
* 27d6c77 ЛР1: функція double
```

**Для лаб:** у `~/univer/labs` (теки `lr1` ... `lr7`) історію однієї лаби дає `git log --oneline -- lr3`. Перед кожним комітом - `git diff --staged`, щоб у коміт не потрапило зайве. Якщо ЛР2 вчора працювала, а сьогодні ні - `git diff HEAD~1 HEAD` покаже, що саме ти поміняв, а `git show HEAD~1:lr2/lr2.py` - вчорашню версію файлу.

### Типові помилки

- `git log` у репо, де ще нема жодного коміту:
  ```text
  fatal: your current branch 'main' does not have any commits yet
  ```
  Це не поломка - спершу зроби перший `git commit`.
- Коміт, якого нема (комітів 4, а просиш на 9 назад):
  ```text
  fatal: ambiguous argument 'HEAD~9': unknown revision or path not in the working tree.
  Use '--' to separate paths from revisions, like this:
  'git <command> [<revision>...] -- [<file>...]'
  ```
  Глянь `git log --oneline` і порахуй, скільки комітів насправді.
- Файлу не було в тому коміті (`git show HEAD~1:lr2.py`):
  ```text
  fatal: path 'lr2.py' does not exist in 'HEAD~1'
  ```
  Перевір назву і теку (`lr2/lr2.py`, а не `lr2.py`).
- `git diff` порожній, хоча ти щось міняв - ти вже зробив `git add`. Дивись `git diff --staged`.
- Екран `git log` «завис» і внизу `(END)` або `:` - це pager. Натисни `q`.

### Як роблять профі

- Короткий псевдонім для малюнка історії - його ставлять майже всі (Pro Git, розд. 2.7 «Git Aliases»):
  ```bash
  git config --global alias.lg "log --oneline --graph --all"
  git lg -n 2
  ```
  ```text
  * c31063a (HEAD -> main) ЛР1: triple множить на 4
  * 228f08c ЛР1: функція triple
  ```
- Пошук коміту, де зʼявився або зник текст («pickaxe», `-S`): коли зламався рядок, а ти не знаєш, коли.
  ```bash
  git log -S "triple" --oneline
  ```
  ```text
  228f08c ЛР1: функція triple
  ```
- `git log -p -- lr1.py` - уся історія одного файлу разом зі змінами в кожному коміті.
- `git diff --word-diff` - різниця по словах, а не по рядках; зручно для README і звітів.
- На GitHub те саме є в браузері: у файлі кнопки **History** (log цього файлу) і **Blame** (docs.github.com, «Viewing a file»).

### Самоперевірка

1. Чим відрізняються `git diff` і `git diff --staged`?
2. Що означає `HEAD~2`?
3. Як подивитися, яким був `lr1.py` три коміти тому, не змінюючи файл у теці?
4. Як побачити лише ті коміти, що чіпали `README.md`?
5. Ти бачиш у `git log` екран з `(END)` внизу. Що робити?

<details markdown="1"><summary>Відповіді</summary>

1. `git diff` - зміни, ще не додані (`add`); `git diff --staged` - додані, ті, що підуть у коміт.
2. Коміт на 2 кроки назад від поточного (`HEAD` - поточний, `HEAD~1` - попередній).
3. `git show HEAD~3:lr1.py` - лише показ, файл у робочій теці лишається як є.
4. `git log --oneline -- README.md`.
5. Натиснути `q` - це програма перегляду (pager), вона чекає, поки ти дочитаєш.

</details>

### Джерела

- Pro Git, 2-ге вид., розд. 2.3 «Viewing the Commit History»: https://git-scm.com/book/en/v2/Git-Basics-Viewing-the-Commit-History - відкрито 18.11.2026
- Pro Git, розд. 2.7 «Git Aliases»: https://git-scm.com/book/en/v2/Git-Basics-Git-Aliases - відкрито 18.11.2026
- git log: https://git-scm.com/docs/git-log - відкрито 18.11.2026
- git diff: https://git-scm.com/docs/git-diff - відкрито 18.11.2026
- git show: https://git-scm.com/docs/git-show - відкрито 18.11.2026
- git blame: https://git-scm.com/docs/git-blame - відкрито 18.11.2026
- Як називати коміти (`HEAD~2`): https://git-scm.com/docs/gitrevisions - відкрито 18.11.2026
- GitHub, «Viewing a file» (History, Blame): https://docs.github.com/en/repositories/working-with-files/using-files/viewing-and-understanding-files - відкрито 18.11.2026

## Тема 6. gitignore для Python

**Навіщо:** у теці лаби, крім твого коду, Python сам наробить сміття: `__pycache__/`, `.venv/` з тисячею файлів, картинки-графіки. Їм не місце в git: вони великі, у кожного свої і відтворюються запуском. `.gitignore` каже git їх не помічати.

### Коротко

`.gitignore` - звичайний текстовий файл у корені репо (назва з крапкою на початку, тому `ls` без `-a` його не показує). Один рядок - один шаблон.

| Рядок у `.gitignore` | Що ігнорує |
|---|---|
| `.venv/` | теку віртуального середовища (сотні пакетних файлів) |
| `__pycache__/` | теку, куди Python кладе скомпільований код при `import` |
| `*.pyc` | окремі такі файли (`*` - будь-які символи) |
| `.pytest_cache/` | кеш pytest |
| `.mypy_cache/` | кеш перевірки типів mypy |
| `*.png` | усі картинки-результати (графіки з matplotlib) |
| `!lr3/skhema.png` | `!` - виняток: цей файл НЕ ігнорувати |
| `# коментар` | коментар, лише з `#` на початку рядка |

Шаблон з `/` у кінці - лише тека. Шаблон без `/` спереду діє в усіх підтеках (`__pycache__/` спрацює і в `lr1/`, і в `lr7/`).

| Команда | Що робить |
|---|---|
| `git check-ignore -v файл` | який рядок якого `.gitignore` ігнорує файл |
| `git rm --cached файл` | прибрати файл з git, але **лишити на диску** |
| `git status --ignored` | показати і ігноровані файли теж |

Головне правило: **`.gitignore` діє лише на файли, яких ще нема в git.** Що вже закомічене - git і далі стежить, поки не скажеш `git rm --cached`.

Аналогія: `.gitignore` - список «не пакувати у валізу». Якщо светр уже у валізі, список його не викине - треба вийняти руками.

### Пісочниця

```bash
mkdir ~/git-pisochnytsia-06
cd ~/git-pisochnytsia-06
git init
python3 -m venv .venv
printf 'def double(x):\n    return x * 2\n' > lr1.py
printf 'import lr1\nprint(lr1.double(4))\n' > main.py
python3 main.py
touch grafik.png
git status
```

`python3 main.py` надрукує `8`, а заодно створить `__pycache__/lr1.cpython-312.pyc` (бо `main.py` імпортує `lr1`). `touch grafik.png` - уяви, що це графік, який зберіг matplotlib.

```text
On branch main

No commits yet

Untracked files:
  (use "git add <file>..." to include in what will be committed)
	.venv/
	__pycache__/
	grafik.png
	lr1.py
	main.py

nothing added to commit but untracked files present (use "git add" to track)
```

У `.venv/` понад тисячу файлів (у перевірці git нарахував 1014). `git add .` зараз потягнув би їх усі.

### Передбач, потім запусти

Створи `.gitignore` (у nano впиши 5 рядків, Ctrl+O, Enter, Ctrl+X) або одним рядком через `printf`:

```bash
nano .gitignore
# або те саме без nano, одним рядком:
printf '.venv/\n__pycache__/\n*.pyc\n.pytest_cache/\n.mypy_cache/\n' > .gitignore
```

1. `git status --short` - які файли лишаться в списку?
<details markdown="1"><summary>Відповідь</summary>

`.venv/` і `__pycache__/` зникли, а сам `.gitignore` зʼявився - його теж треба комітити. `grafik.png` ще видно: правила для `*.png` поки нема.
```text
?? .gitignore
?? grafik.png
?? lr1.py
?? main.py
```
</details>

2. `git check-ignore -v __pycache__/lr1.cpython-312.pyc` - який рядок спрацює: `__pycache__/` чи `*.pyc`?
<details markdown="1"><summary>Відповідь</summary>

Рядок 2, `__pycache__/`: git ігнорує всю теку і всередину вже не дивиться. Формат: файл`:`номер рядка`:`шаблон, потім Tab і шлях.
```text
.gitignore:2:__pycache__/	__pycache__/lr1.cpython-312.pyc
```
</details>

3. `git check-ignore -v main.py` - що виведе?
<details markdown="1"><summary>Відповідь</summary>

Нічого, і код виходу 1 (`echo $?` покаже `1`): `main.py` не ігнорується. Тиша тут - добра новина.
</details>

### Руками

**Крок 1. Комітимо разом з графіком** (наче ти ще не знав про `*.png`):

```bash
git add .
git commit -m "ЛР1 і gitignore"
```
```text
[main (root-commit) bf8917a] ЛР1 і gitignore
 4 files changed, 9 insertions(+)
 create mode 100644 .gitignore
 create mode 100644 grafik.png
 create mode 100644 lr1.py
 create mode 100644 main.py
```

4 файли: `.venv/` і `__pycache__/` у коміт не пішли. (Хеш у тебе буде інший.)

**Крок 2. Пізно додали правило.** Дописуємо `*.png` і «перемальовуємо» графік:

```bash
printf '*.png\n' >> .gitignore
printf 'новий графік\n' > grafik.png
git status --short
git check-ignore -v grafik.png
```
```text
 M .gitignore
 M grafik.png
```

`grafik.png` досі в списку змінених, а `check-ignore` мовчить: файл уже в git, і правило на нього не діє.

**Крок 3. Прибрати з git, лишити на диску.**

```bash
git rm --cached grafik.png
git status --short
```
```text
rm 'grafik.png'
```
```text
 M .gitignore
D  grafik.png
```

`D` у першій колонці - «видалення з репо підготовлене до коміту». Файл на диску не чіпали.

```bash
git add .gitignore
git commit -m "Не зберігай картинки-результати"
ls
git status --short
```
```text
[main d84d1e0] Не зберігай картинки-результати
 2 files changed, 1 insertion(+)
 delete mode 100644 grafik.png
```
```text
__pycache__
grafik.png
lr1.py
main.py
```

`grafik.png` на місці, `git status --short` порожній - тепер git його справді ігнорує. Перевір: `git check-ignore -v grafik.png` → `.gitignore:6:*.png	grafik.png`.

**Для лаб:** один `.gitignore` у корені `~/univer/labs` діє на всі теки `lr1` ... `lr7`. Візьми ті самі 6 рядків (`.venv/`, `__pycache__/`, `*.pyc`, `.pytest_cache/`, `.mypy_cache/`, `*.png`). Якщо до звіту ЛР3 треба саме цю схему - допиши виняток `!lr3/skhema.png`. Зроби `.gitignore` **до** першого `git add .`, тоді `git rm --cached` не знадобиться.

### Типові помилки

- Додаєш ігнорований файл руками:
  ```text
  The following paths are ignored by one of your .gitignore files:
  grafik.png
  hint: Use -f if you really want to add them.
  hint: Turn this message off by running
  hint: "git config advice.addIgnoredFile false"
  ```
  git питає «ти впевнений?». Якщо файл справді треба - `git add -f grafik.png`, але краще виняток `!` у `.gitignore`.
- Правило написане, а файл досі в `git status` як змінений (`M`) - він закомічений раніше. Лікування - `git rm --cached файл` і коміт (крок 3).
- Закомітив цілу `.venv/` (у перевірці це 1014 файлів в одному коміті). Прибрати з git, не чіпаючи середовище (`-r` - рекурсивно, `-q` - тихо, без тисячі рядків `rm '...'`):
  ```bash
  git rm -r -q --cached .venv
  git commit -m "Прибери .venv з репо"
  ```
  Не забудь `.venv/` у `.gitignore`, інакше наступний `git add .` поверне її.
- Коментар у тому ж рядку: `*.png # картинки` **не працює** - git шукає файл, що закінчується на `.png # картинки`. `git status --short` і далі показує `?? a.png`. Коментар - лише окремим рядком з `#` на початку.
- Файл назвали `gitignore` (без крапки) або `.gitignore.txt` - git його не читає. Перевір `ls -a`: має бути рівно `.gitignore`.

### Як роблять профі

- Не пишуть з нуля, а беруть шаблон GitHub `Python.gitignore` (репо github/gitignore; 18.11.2026 у ньому 223 рядки, є `__pycache__/`, `*.py[codz]`, `.pytest_cache/`, `.venv`, `.mypy_cache/`). Його ж підставляє сайт при створенні репо (поле «Add .gitignore» → Python) і `gh`:
  ```bash
  wget -O .gitignore https://raw.githubusercontent.com/github/gitignore/main/Python.gitignore
  gh repo create pisochnytsia-py --private --gitignore Python
  ```
  Прочитай шаблон перед комітом: там є, наприклад, `lib/` і `build/` - тека `lib/` з твоїм кодом теж стане ігнорованою.
- Особисте сміття твого редактора (`*.swp`, `*~`) пишуть не в `.gitignore` проєкту, а в **глобальний** файл `~/.config/git/ignore` - він діє в усіх репо на твоєму компʼютері (git-scm.com/docs/gitignore: якщо `core.excludesFile` не задано, береться `$HOME/.config/git/ignore`):
  ```bash
  mkdir -p ~/.config/git
  printf '*.swp\n' > ~/.config/git/ignore
  touch .lr1.py.swp
  git check-ignore -v .lr1.py.swp
  ```
  ```text
  /home/.../.config/git/ignore:1:*.swp	.lr1.py.swp
  ```
  (замість `...` - твоя домашня тека.)
- `git check-ignore -v --no-index файл` - показує правило навіть для вже закоміченого файлу (без `--no-index` git про такі мовчить, як у кроці 2).
- `git status --ignored` - глянути, що саме зараз ігнорується (чи не сховав ти щось потрібне).
- Python 3.13+ сам кладе в нову `.venv/` файл `.gitignore` з `*` (docs.python.org, venv: «Changed in version 3.13: venv now creates a .gitignore file for Git by default»). На Mint 22 Python 3.12 - тому `.venv/` у свій `.gitignore` пишемо самі.

### Самоперевірка

1. Що буде з `grafik.png`, якщо він уже закомічений, а ти дописав `*.png` у `.gitignore`?
2. Чим `git rm --cached lr1.png` відрізняється від `rm lr1.png`?
3. Яка команда скаже, через який рядок `.gitignore` ігнорується файл?
4. Чому `*.png # графіки` в `.gitignore` не ігнорує `grafik.png`?
5. Що з цього писати в `.gitignore` проєкту, а що в `~/.config/git/ignore`: `__pycache__/`, `*.swp` від твого редактора?

<details markdown="1"><summary>Відповіді</summary>

1. Нічого: git і далі стежить за ним (`M grafik.png` у статусі). Треба `git rm --cached grafik.png` і коміт.
2. `git rm --cached` прибирає файл лише з git, на диску він лишається; `rm` видаляє з диска.
3. `git check-ignore -v файл` (для вже закоміченого - з `--no-index`).
4. Коментар можна лише окремим рядком; тут ` # графіки` стало частиною шаблону.
5. `__pycache__/` - у `.gitignore` проєкту (стосується всіх, хто працює з кодом); `*.swp` - у глобальний, це звичка лише твого редактора.

</details>

### Джерела

- gitignore (шаблони, `!`, `#`, глобальний файл): https://git-scm.com/docs/gitignore - відкрито 18.11.2026
- git check-ignore: https://git-scm.com/docs/git-check-ignore - відкрито 18.11.2026
- git rm (`--cached`): https://git-scm.com/docs/git-rm - відкрито 18.11.2026
- Pro Git, розд. 2.2 «Ignoring Files»: https://git-scm.com/book/en/v2/Git-Basics-Recording-Changes-to-the-Repository - відкрито 18.11.2026
- Шаблон Python.gitignore: https://github.com/github/gitignore/blob/main/Python.gitignore - відкрито 18.11.2026
- GitHub, «Ignoring files»: https://docs.github.com/en/get-started/git-basics/ignoring-files - відкрито 18.11.2026
- Python venv (3.13 створює .gitignore): https://docs.python.org/3/library/venv.html - відкрито 18.11.2026

## Тема 7. Гілки - branch, switch, merge

**Навіщо:** ЛР1 здана і працює, а ЛР2 ти лише почав і вона поки ламається. Гілка дає робити ЛР2 окремо: `main` лишається робочою, а коли ЛР2 готова - зливаєш її в `main` однією командою.

### Коротко

**Гілка** - це просто назва-ярлик, приклеєний до одного коміту. Новий коміт пересуває ярлик поточної гілки вперед. **HEAD** - «де я зараз»: на якій гілці стою. Копій файлів гілка не робить, тому вона створюється миттєво.

| Команда | Що робить |
|---|---|
| `git branch` | список гілок, `*` - поточна |
| `git switch -c lr2` | створити гілку `lr2` і перейти на неї |
| `git switch main` | перейти на `main` (файли в теці стануть як у `main`) |
| `git merge lr2` | злити `lr2` у поточну гілку |
| `git branch -d lr2` | видалити гілку (лише якщо вже злита) |
| `git log --oneline --graph --all` | малюнок усіх гілок |

Два види злиття:

```text
1) Fast-forward (перемотування): main не рухався, поки ти робив lr2
   до:     A ← B          після:  A ← B
           ↑   ↑                      ↑
         main  lr2                main, lr2
   Нового коміту нема: ярлик main просто пересунули вперед.

2) Merge-коміт: обидві гілки пішли вперед
   до:                          після:
   A ← B ← D     (main)         A ← B ← D ← M   (main)
        \                            \     /
         C       (lr3)                C ──      (lr3)
   git робить новий коміт M з ДВОМА батьками (D і C).
```

Аналогія: `main` - чистовик, гілка - чернетка. Fast-forward - коли чистовик не чіпали і чернетку просто оголосили чистовиком. Merge-коміт - коли в чистовику теж щось дописали, і треба звести обидва в одне.

Старі підручники пишуть `git checkout -b lr2` і `git checkout main` - це те саме, що `git switch -c lr2` і `git switch main` (`switch` є з git 2.23, він простіший і робить лише одне).

### Пісочниця

```bash
mkdir ~/git-pisochnytsia-07
cd ~/git-pisochnytsia-07
git init
printf 'def double(x):\n    return x * 2\n' > lr1.py
git add lr1.py
git commit -m "ЛР1 готова"
git branch
```
```text
* main
```

### Передбач, потім запусти

1. Створюємо гілку, комітимо в ній новий файл і повертаємось на `main`. Що покаже `ls`?
```bash
git switch -c lr2
printf 'print("ЛР2")\n' > lr2.py
git add lr2.py
git commit -m "ЛР2: початок"
git switch main
ls
```
<details markdown="1"><summary>Відповідь</summary>

```text
lr1.py
```
`lr2.py` зник з теки - але не з git: він у коміті гілки `lr2`. `git switch` переписує файли в теці під вибрану гілку. Повернешся на `lr2` - файл зʼявиться.
</details>

2. `git merge lr2` (зараз ти на `main`) - буде новий коміт чи ні? Запустиш у кроці 2.
<details markdown="1"><summary>Відповідь</summary>

Ні, це fast-forward: `main` не мінявся, поки ти робив `lr2`, тож git просто пересуває ярлик `main` вперед. Слово `Fast-forward` буде прямо у виводі.
</details>

3. Тепер гілка `lr3` з одним комітом, а в `main` тим часом коміт з README. Що буде при `git merge lr3`?
<details markdown="1"><summary>Відповідь</summary>

Merge-коміт: обидві гілки пішли вперед, перемотати не вийде. Деталі - у кроці 3 нижче.
</details>

### Руками

**Крок 1. Подивись на гілки до злиття.** Ти на `main`:

```bash
git log --oneline --graph --all
```
```text
* 0879f44 (lr2) ЛР2: початок
* c03fdc0 (HEAD -> main) ЛР1 готова
```
У дужках - ярлики. `HEAD -> main` значить «я на гілці main», а `lr2` на коміт попереду. Хеші в тебе будуть інші - дивись на будову.

**Крок 2. Fast-forward і прибирання.**

```bash
git merge lr2
git branch -d lr2
```
```text
Updating c03fdc0..0879f44
Fast-forward
 lr2.py | 1 +
 1 file changed, 1 insertion(+)
 create mode 100644 lr2.py
```
```text
Deleted branch lr2 (was 0879f44).
```
Коміти ЛР2 нікуди не ділись: вони тепер у `main`. Видалили лише ярлик.

**Крок 3. Merge-коміт.**

```bash
git switch -c lr3
printf 'print("ЛР3")\n' > lr3.py
git add lr3.py
git commit -m "ЛР3: початок"
git switch main
printf '# Лаби\n' > README.md
git add README.md
git commit -m "Додай README"
git log --oneline --graph --all
```
```text
* c3d4a00 (HEAD -> main) Додай README
| * 5fe4c9d (lr3) ЛР3: початок
|/
* 0879f44 ЛР2: початок
* c03fdc0 ЛР1 готова
```

Гілки розійшлись від `0879f44`. Зливаємо:

```bash
git merge lr3
```

На Mint тут відкриється **nano** з готовим повідомленням `Merge branch 'lr3'`. Нічого не міняй: Ctrl+O, Enter, Ctrl+X.

```text
Merge made by the 'ort' strategy.
 lr3.py | 1 +
 1 file changed, 1 insertion(+)
 create mode 100644 lr3.py
```

`ort` - назва алгоритму злиття за замовчуванням, на нього можна не зважати.

```bash
git log --oneline --graph --all
git log -n 1
```
```text
*   be97404 (HEAD -> main) Merge branch 'lr3'
|\
| * 5fe4c9d (lr3) ЛР3: початок
* | c3d4a00 Додай README
|/
* 0879f44 ЛР2: початок
* c03fdc0 ЛР1 готова
```
```text
commit be9740421acfc7c43e1bb2c9603d61f28df43354 (HEAD -> main)
Merge: c3d4a00 5fe4c9d
Author: Твоє Імʼя <128326252+Evge14n@users.noreply.github.com>
Date:   Wed Nov 18 16:12:00 2026 +0200

    Merge branch 'lr3'
```

Рядок `Merge: c3d4a00 5fe4c9d` - два батьки. На малюнку дві лінії сходяться в одну. Тепер `git branch -d lr3` → `Deleted branch lr3 (was 5fe4c9d).`

**Для лаб:** у `~/univer/labs` тримай `main` таким, щоб усі здані лаби працювали. Нову лабу починай гілкою: `git switch -c lr4`, комітиш крок за кроком, а коли doctest проходить - `git switch main`, `git merge lr4`, `git branch -d lr4`. Якщо посеред ЛР4 викладач просить виправити ЛР3 - `git switch main`, правиш, комітиш, і назад `git switch lr4`.

### Типові помилки

- Гілки з такою назвою нема (`git switch lr9`), код виходу 128:
  ```text
  fatal: invalid reference: lr9
  ```
  Глянь `git branch`. Створити нову - `git switch -c lr9`.
- Гілка вже є (`git switch -c main`):
  ```text
  fatal: a branch named 'main' already exists
  ```
  Перейти на неї - без `-c`: `git switch main`.
- Видаляєш гілку, яку ще не злив (`git branch -d lr4`):
  ```text
  error: the branch 'lr4' is not fully merged.
  If you are sure you want to delete it, run 'git branch -D lr4'
  ```
  Це запобіжник: її коміти ніде більше нема. Спершу `git merge lr4`. Велика `-D` видаляє силою - коміти гілки загубляться (рятувати їх - урок 12, reflog).
- Перемикаєшся, а в теці незакомічені зміни файлу, який у тій гілці інший:
  ```text
  error: Your local changes to the following files would be overwritten by checkout:
  	lr1.py
  Please commit your changes or stash them before you switch branches.
  Aborting
  ```
  git нічого не зробив і лишив тебе на місці. Закоміть зміни (або відклади - урок 13, stash), потім перемикайся.
- Незакомічені зміни **їдуть з тобою** в іншу гілку, якщо не заважають: `git switch lr4` пише
  ```text
  Switched to branch 'lr4'
  M	README.md
  ```
  `M README.md` - твоя правка з `main` тепер у теці на `lr4`. Зміна належить гілці лише після коміту. Правило: перед `git switch` - `git status` чистий.

### Як роблять профі

- Гілка живе недовго: одна задача (одна лаба, одна правка) - одна гілка, злили - видалили. Так працює GitHub flow (docs.github.com, «GitHub flow»): `main` завжди робочий, зміни - через гілки і Pull Request (урок 11).
- `git switch -` - назад на попередню гілку (як `cd -`):
  ```bash
  git switch -
  ```
- Швидкий огляд гілок і того, що вже злито (те, що в `--merged`, можна сміливо `-d`):
  ```bash
  git branch -v
  git branch --merged
  ```
  ```text
    lr4  d7d4232 ЛР4: змінна x
  * main be97404 Merge branch 'lr3'
  ```
  ```text
  * main
  ```
  `lr4` нема в `--merged` - її ще не злито.
- Деякі команди просять завжди merge-коміт, навіть коли можна перемотати, щоб в історії було видно «тут злили гілку»: `git merge --no-ff lr5`. Інші, навпаки, тримають історію прямою (rebase, squash - див. урок 11, види merge на GitHub).
- Назви гілок короткі, латиницею, без пробілів: `lr4`, `lr3-vypravlennia`, `fix-doctest`.

### Самоперевірка

1. Що таке гілка в git і чому вона створюється миттєво?
2. Коли `git merge` робить fast-forward, а коли - merge-коміт?
3. Ти на `main`, а `lr2.py` є лише в гілці `lr2`. Чому `ls` його не показує і як його побачити?
4. `git branch -d lr4` пише `not fully merged`. Що це значить і що зробиш?
5. Яка команда малює всі гілки з ярликами `HEAD -> main`?

<details markdown="1"><summary>Відповіді</summary>

1. Ярлик (назва), що вказує на один коміт. Файли не копіюються - тому миттєво.
2. Fast-forward - коли поточна гілка не мінялась після відгалуження (просто пересунути ярлик). Merge-коміт - коли обидві гілки мають нові коміти.
3. `git switch` ставить у теку файли поточної гілки. `git switch lr2` - і `lr2.py` зʼявиться.
4. У `lr4` є коміти, яких нема в `main`. Спершу `git merge lr4` (з `main`), потім `-d`. `-D` - лише якщо ці коміти справді не потрібні.
5. `git log --oneline --graph --all`.

</details>

### Джерела

- Pro Git, розд. 3.1 «Branches in a Nutshell»: https://git-scm.com/book/en/v2/Git-Branching-Branches-in-a-Nutshell - відкрито 18.11.2026
- Pro Git, розд. 3.2 «Basic Branching and Merging»: https://git-scm.com/book/en/v2/Git-Branching-Basic-Branching-and-Merging - відкрито 18.11.2026
- git switch: https://git-scm.com/docs/git-switch - відкрито 18.11.2026
- git merge (fast-forward, `--no-ff`): https://git-scm.com/docs/git-merge - відкрито 18.11.2026
- git branch (`-d`, `-D`, `--merged`): https://git-scm.com/docs/git-branch - відкрито 18.11.2026
- GitHub flow: https://docs.github.com/en/get-started/using-github/github-flow - відкрито 18.11.2026

## Тема 8. Конфлікт і як розвʼязати руками

**Навіщо:** ти в гілці поставив `g = 9.81`, а в `main` хтось (або ти сам учора) - `g = 9.80665`. git не знає, що з цього правильно для ЛР1, і питає тебе. Це і є конфлікт. Він не страшний: 4 кроки, і все.

### Коротко

**Конфлікт** - коли дві гілки по-різному змінили **ті самі рядки** одного файлу. Різні файли або різні місця файлу git зливає сам. Тут - зупиняється і просить вибрати.

git вписує у файл обидва варіанти між **маркерами**:

```text
<<<<<<< HEAD          ← початок: нижче твій варіант (поточна гілка)
g = 9.80665
=======               ← роздільник
g = 9.81
>>>>>>> tochnist      ← кінець: вище варіант з гілки tochnist
```

Що робити:

```text
1) git status            - які файли в конфлікті (both modified)
2) nano файл             - лишити правильний рядок, ВИДАЛИТИ всі три маркери
3) git add файл          - «я розвʼязав»
4) git commit            - завершити злиття
   (передумав? git merge --abort - усе як до merge)
```

| Команда | Що робить |
|---|---|
| `git status` / `git status --short` | файли в конфлікті: `both modified` / `UU` |
| `git diff` | під час конфлікту - обидва варіанти поруч |
| `git add файл` | позначити конфлікт у файлі розвʼязаним |
| `git commit` | завершити злиття (повідомлення вже готове) |
| `git merge --abort` | скасувати злиття, повернути все як було |
| `git pull` | забрати чужі коміти з GitHub і злити (детально - урок 09) |

Аналогія: двоє редагують один абзац реферату. Хтось має прочитати обидва варіанти і лишити один (або змішати). git цього за тебе не робить - і правильно.

### Пісочниця

Дві гілки міняють один і той самий рядок:

```bash
mkdir ~/git-pisochnytsia-08
cd ~/git-pisochnytsia-08
git init
printf '# ЛР1: маятник\ng = 9.8\nL = 1.0\n' > lr1.py
git add lr1.py
git commit -m "ЛР1: константи"
git switch -c tochnist
sed -i 's/g = 9.8/g = 9.81/' lr1.py
git commit -am "g точніше: 9.81"
git switch main
sed -i 's/g = 9.8/g = 9.80665/' lr1.py
git commit -am "g стандартне: 9.80665"
git log --oneline --graph --all
```
```text
* d2c6a3c (HEAD -> main) g стандартне: 9.80665
| * 679fd6f (tochnist) g точніше: 9.81
|/
* 9004942 ЛР1: константи
```
Хеші в тебе будуть інші - дивись на будову.

### Передбач, потім запусти

1. `git merge tochnist` - злиття пройде?
```bash
git merge tochnist
```
<details markdown="1"><summary>Відповідь</summary>

Ні, конфлікт. Код виходу 1 (`echo $?`).
```text
Auto-merging lr1.py
CONFLICT (content): Merge conflict in lr1.py
Automatic merge failed; fix conflicts and then commit the result.
```
</details>

2. `cat lr1.py` - що тепер у файлі?
<details markdown="1"><summary>Відповідь</summary>

Обидва варіанти з маркерами. Рядки, де згоди нема, - лише рядок з `g`; заголовок і `L` git злив сам.
```text
# ЛР1: маятник
<<<<<<< HEAD
g = 9.80665
=======
g = 9.81
>>>>>>> tochnist
L = 1.0
```
</details>

3. Зробити коміт просто зараз: `git commit -m "Злиття"` - вийде?
<details markdown="1"><summary>Відповідь</summary>

Ні, git не дасть закомітити нерозвʼязаний файл (код 128):
```text
error: Committing is not possible because you have unmerged files.
hint: Fix them up in the work tree, and then use 'git add/rm <file>'
hint: as appropriate to mark resolution and make a commit.
fatal: Exiting because of an unresolved conflict.
U	lr1.py
```
</details>

### Руками

**Крок 1. Подивись, що зламалось.**

```bash
git status
git status --short
git diff
```
```text
On branch main
You have unmerged paths.
  (fix conflicts and run "git commit")
  (use "git merge --abort" to abort the merge)

Unmerged paths:
  (use "git add <file>..." to mark resolution)
	both modified:   lr1.py

no changes added to commit (use "git add" and/or "git commit -a")
```
```text
UU lr1.py
```
```text
diff --cc lr1.py
index 7435f88,75aaf89..0000000
--- a/lr1.py
+++ b/lr1.py
@@@ -1,3 -1,3 +1,7 @@@
  # ЛР1: маятник
++<<<<<<< HEAD
 +g = 9.80665
++=======
+ g = 9.81
++>>>>>>> tochnist
  L = 1.0
```

`UU` - «unmerged» в обох. Під час конфлікту `git diff` особливий (`diff --cc`): дві колонки плюсів, бо порівнює з обома батьками.

**Крок 2. Розвʼяжи в nano.** У методичці `g = 9.81` - лишаємо його.

```bash
nano lr1.py
```

У nano: стань на рядок `<<<<<<< HEAD` і видали його (Ctrl+K вирізає цілий рядок), так само рядок `g = 9.80665`, `=======` і `>>>>>>> tochnist`. Має лишитись рівно:

```text
# ЛР1: маятник
g = 9.81
L = 1.0
```

Збережи: Ctrl+O, Enter, Ctrl+X. (Без nano те саме одним рядком:)

```bash
printf '# ЛР1: маятник\ng = 9.81\nL = 1.0\n' > lr1.py
```

**Крок 3. add і commit.**

```bash
git add lr1.py
git status
```
```text
On branch main
All conflicts fixed but you are still merging.
  (use "git commit" to conclude merge)

Changes to be committed:
	modified:   lr1.py
```

```bash
git commit
```

Відкриється nano з готовим повідомленням `Merge branch 'tochnist'` - просто Ctrl+O, Enter, Ctrl+X.

```text
[main 8d45cb3] Merge branch 'tochnist'
```
```bash
git log --oneline --graph --all
```
```text
*   8d45cb3 (HEAD -> main) Merge branch 'tochnist'
|\
| * 679fd6f (tochnist) g точніше: 9.81
* | d2c6a3c g стандартне: 9.80665
|/
* 9004942 ЛР1: константи
```

**Крок 4. Передумав - `git merge --abort`.** Новий конфлікт, тепер у рядку `L`:

```bash
git switch -c dovzhyna
sed -i 's/L = 1.0/L = 0.5/' lr1.py
git commit -am "L = 0.5"
git switch main
sed -i 's/L = 1.0/L = 2.0/' lr1.py
git commit -am "L = 2.0"
git merge dovzhyna
git merge --abort
git status
cat lr1.py
```
```text
On branch main
nothing to commit, working tree clean
```
```text
# ЛР1: маятник
g = 9.81
L = 2.0
```

Маркерів нема, файл як до `merge`. Це кнопка «назад», коли конфлікт заплутаний і хочеться спершу подумати.

**Крок 5. Конфлікт з чужим комітом (через GitHub).** Другий клон `~/druhyi-klon` грає роль одногрупника на іншому ноутбуці. Працюємо в приватній пісочниці `pisochnytsia` з уроку 03. `git push` - відправити свої коміти на GitHub, `git pull` - забрати чужі (детально - урок 09).

Ти пишеш план здачі і відправляєш:

```bash
cd ~/pisochnytsia
git pull
printf 'Здача ЛР1: 25.11\n' > plan.txt
git add plan.txt
git commit -m "План здачі"
git push
```

«Одногрупник» клонує, міняє дату і теж відправляє (якщо `~/druhyi-klon` уже є - пропусти `git clone`, натомість `cd ~/druhyi-klon` і `git pull`):

```bash
git clone git@github.com:Evge14n/pisochnytsia.git ~/druhyi-klon
cd ~/druhyi-klon
git config user.name "Друг"
sed -i 's/25.11/27.11/' plan.txt
git commit -am "Здача ЛР1 переноситься на 27.11"
git push
```

`git config` без `--global` діє лише в цьому репо - тут ти «Друг». А ти, не знаючи про це, ставиш свою дату і забираєш зміни:

```bash
cd ~/pisochnytsia
sed -i 's/25.11/26.11/' plan.txt
git commit -am "Здача ЛР1 26.11"
git pull
cat plan.txt
```
```text
From github.com:Evge14n/pisochnytsia
   9a7bcdc..89c4ae1  main       -> origin/main
Auto-merging plan.txt
CONFLICT (content): Merge conflict in plan.txt
Automatic merge failed; fix conflicts and then commit the result.
```
```text
<<<<<<< HEAD
Здача ЛР1: 26.11
=======
Здача ЛР1: 27.11
>>>>>>> 89c4ae13c81d30f023c41b734b83cd842bcec7bf
```

Те саме, що й між гілками: `git pull` = забрати + `git merge`. Замість назви гілки після `>>>>>>>` - хеш чужого коміту. Спитав одногрупника - правильно 27.11:

```bash
nano plan.txt
printf 'Здача ЛР1: 27.11\n' > plan.txt
git add plan.txt
git commit
git push
git log --format="%h %an: %s" -n 3
```

(`nano` або `printf` - щось одне.) nano для коміту запропонує `Merge branch 'main' of github.com:Evge14n/pisochnytsia` - лиши як є. Останній рядок показує, хто що зробив (`%h` - хеш, `%an` - автор, `%s` - повідомлення):

```text
5402946 Твоє Імʼя: Merge branch 'main' of github.com:Evge14n/pisochnytsia
6728730 Твоє Імʼя: Здача ЛР1 26.11
89c4ae1 Друг: Здача ЛР1 переноситься на 27.11
```

**Для лаб:** у `~/univer/labs` конфлікт найчастіше буває, коли ти правиш ЛР3 у двох гілках або на двох компʼютерах (ноутбук і ПК в аудиторії). Правило те саме: `git status` → `nano lr3/lr3.py` → прибрати маркери → `python3 -m doctest lr3/lr3.py` (перевір, що код живий!) → `git add` → `git commit`.

### Типові помилки

- Закомітив файл з маркерами (git дозволяє: `git add` не перевіряє вміст). Python падає:
  ```text
    File "/home/.../lr1.py", line 1
      <<<<<<< HEAD
      ^^
  SyntaxError: invalid syntax
  ```
  Відкрий файл у nano, прибери маркери, новий коміт. Перед `git add` став собі звичку: `git diff --check` (див. «Як роблять профі»).
- Перемикаєшся на іншу гілку посеред злиття (`git switch tochnist`):
  ```text
  fatal: cannot switch branch while merging
  Consider "git merge --quit" or "git worktree add".
  ```
  Спершу закінчи злиття (`git add` + `git commit`) або скасуй (`git merge --abort`).
- `git merge --abort`, коли злиття вже завершене або його не було:
  ```text
  fatal: There is no merge to abort (MERGE_HEAD missing).
  ```
  Скасувати вже зроблений merge-коміт - це інше (урок 12, `git revert`).
- Видалив маркери, але лишив обидва рядки `g = ...` - git не сперечатиметься, а код стане неправильним. Після розвʼязання завжди запускай doctest.
- `git clone ... ~/druhyi-klon` вдруге: `fatal: destination path '...' already exists and is not an empty directory.` Клон уже є - `cd ~/druhyi-klon` і `git pull`.

### Як роблять профі

- Перевірка на забуті маркери перед `git add`: `git diff --check`. Під час конфлікту в кроці 1 вона пише (код 2), а після розвʼязання мовчить (код 0):
  ```text
  lr1.py:2: leftover conflict marker
  lr1.py:4: leftover conflict marker
  lr1.py:6: leftover conflict marker
  ```
- Стиль `zdiff3` (у git 2.43 на Mint працює, перевірено запуском): між маркерами видно ще й **як було до обох змін** - легше зрозуміти, хто що міняв (git-scm.com/docs/git-config, `merge.conflictStyle`):
  ```bash
  git config --global merge.conflictStyle zdiff3
  ```
  Той самий конфлікт з кроку 4 тоді виглядає так (`|||||||` - спільний предок):
  ```text
  # ЛР1: маятник
  g = 9.81
  <<<<<<< HEAD
  L = 2.0
  ||||||| 8d45cb3
  L = 1.0
  =======
  L = 0.5
  >>>>>>> dovzhyna
  ```
- Узяти цілий файл з одного боку, не редагуючи: `git checkout --ours lr1.py` (наша версія) або `git checkout --theirs lr1.py` (їхня), потім `git add`. Зручно для файлів, які не правлять руками (згенеровані дані).
- Конфліктів менше, якщо: `git pull` перед початком роботи, маленькі коміти, короткі гілки, і не правити один файл удвох одночасно (Pro Git, розд. 5.2).
- На GitHub прості конфлікти в Pull Request можна розвʼязати прямо в браузері, кнопка **Resolve conflicts** (docs.github.com, «Resolving a merge conflict on GitHub»; урок 11).

### Самоперевірка

1. Коли виникає конфлікт, а коли git зливає сам?
2. Що означають `<<<<<<< HEAD`, `=======` і `>>>>>>> tochnist`?
3. Назви 4 кроки розвʼязання конфлікту.
4. Як скасувати злиття, якщо конфлікт заплутаний?
5. Чому після `git pull` теж буває конфлікт?

<details markdown="1"><summary>Відповіді</summary>

1. Конфлікт - коли дві гілки змінили ті самі рядки файлу по-різному. Різні файли чи різні місця файлу git зливає сам.
2. Від `<<<<<<< HEAD` до `=======` - твій варіант (поточна гілка), від `=======` до `>>>>>>> tochnist` - варіант з гілки `tochnist`.
3. `git status` → виправити файл у nano і прибрати маркери → `git add файл` → `git commit`.
4. `git merge --abort`.
5. `git pull` = забрати коміти з GitHub + `git merge`. Якщо хтось змінив ті самі рядки і вже відправив - це звичайний конфлікт злиття.

</details>

### Джерела

- Pro Git, розд. 3.2 «Basic Merge Conflicts»: https://git-scm.com/book/en/v2/Git-Branching-Basic-Branching-and-Merging - відкрито 18.11.2026
- Pro Git, розд. 7.8 «Advanced Merging»: https://git-scm.com/book/en/v2/Git-Tools-Advanced-Merging - відкрито 18.11.2026
- git merge (розділи «HOW CONFLICTS ARE PRESENTED», `--abort`): https://git-scm.com/docs/git-merge - відкрито 18.11.2026
- git config, `merge.conflictStyle`: https://git-scm.com/docs/git-config - відкрито 18.11.2026
- GitHub, «Resolving a merge conflict using the command line»: https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/addressing-merge-conflicts/resolving-a-merge-conflict-using-the-command-line - відкрито 18.11.2026
- GitHub, «Resolving a merge conflict on GitHub»: https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/addressing-merge-conflicts/resolving-a-merge-conflict-on-github - відкрито 18.11.2026

## Тема 9. Віддалений репозиторій - remote, push, pull, fetch

**Навіщо:** лаби лежать на ноутбуці. Ноутбук може зламатись, а в аудиторії ти сидиш за іншим ПК. GitHub - копія репо в інтернеті: `push` відправляє туди твої коміти, `pull` забирає звідти свіжі (свої з іншого компʼютера або одногрупника).

### Коротко

**Remote** (віддалений репозиторій) - адреса іншої копії того самого репо. Після `git clone` вона вже записана під назвою **origin** («звідки взяв»).

**origin/main** - це **памʼять** твого git про те, що було в `main` на GitHub, коли ти востаннє з ним говорив. Вона оновлюється лише при `fetch`, `pull` і `push`. Сам по собі git на GitHub не ходить.

```text
          GitHub (origin)
          A ← B ← C      main
            ↑         │
      push  │         │  fetch (копіює C у твій origin/main, файли НЕ чіпає)
            │         ↓
Ноутбук:  A ← B      main          origin/main → C
                      ↑
                      └─ merge origin/main  (тепер і main → C)

pull = fetch + merge
```

| Команда | Що робить |
|---|---|
| `git remote -v` | показати адреси remote |
| `git remote add origin git@github.com:Evge14n/РЕПО.git` | записати адресу (для репо, створеного `git init`) |
| `git push -u origin main` | перший пуш гілки: відправити і запамʼятати «main ↔ origin/main» |
| `git push` | відправити нові коміти (після `-u` - без аргументів) |
| `git fetch` | забрати чужі коміти в `origin/main`, свої файли не чіпати |
| `git log --oneline main..origin/main` | що є на GitHub, чого нема в мене |
| `git pull` | `fetch` + `merge` одним махом |
| `git status` | `ahead` - у мене є непушнуті коміти; `behind` - на GitHub є нові |

Аналогія: GitHub - спільна дошка оголошень. `push` - повісив свій листок. `fetch` - сфотографував дошку (у себе нічого не переписав). `pull` - сфотографував і переписав нове в зошит.

### Пісочниця

Потрібні два клони одного приватного репо: `~/pisochnytsia` (урок 03) і `~/druhyi-klon` (урок 08, там `git config user.name "Друг"`). Немає другого - `git clone git@github.com:Evge14n/pisochnytsia.git ~/druhyi-klon`, потім у ньому `git config user.name "Друг"`.

Твої хеші і кількість комітів будуть інші, ніж тут: у прикладі на GitHub спершу лише один коміт `Initial commit`.

### Передбач, потім запусти

1. Ти зробив коміт і ще не пушив. Що скаже `git status`? (Перевіриш у кроці 2.)
<details markdown="1"><summary>Відповідь</summary>

```text
Your branch is ahead of 'origin/main' by 1 commit.
  (use "git push" to publish your local commits)
```
`ahead` - ти попереду GitHub на 1 коміт.
</details>

2. Одногрупник щойно запушив коміт. Ти в `~/pisochnytsia` пишеш `git status`, без `fetch`. Що буде? (Крок 3.)
<details markdown="1"><summary>Відповідь</summary>

```text
Your branch is up to date with 'origin/main'.
```
Неправда, але чесна: git порівнює з **памʼяттю** `origin/main`, а вона стара. Щоб дізнатись правду - `git fetch`, потім `git status`.
</details>

3. І ти, і одногрупник зробили по коміту, він запушив першим. Ти пишеш `git push`. Що буде? (Крок 4.)
<details markdown="1"><summary>Відповідь</summary>

Відмова `! [rejected] ... (fetch first)`: на GitHub є коміт, якого нема в тебе, і git не дасть його затерти. Спершу `git pull`, потім `git push`.
</details>

### Руками

**Крок 1. Куди дивиться origin.**

```bash
cd ~/pisochnytsia
git remote -v
git branch -vv
```
```text
origin	git@github.com:Evge14n/pisochnytsia.git (fetch)
origin	git@github.com:Evge14n/pisochnytsia.git (push)
```
```text
* main ff89247 [origin/main] Initial commit
```

`[origin/main]` - твоя `main` «стежить» за `origin/main` (так налаштував `git clone`). Тому `git push` і `git pull` працюють без аргументів.

**Крок 2. ahead → push.**

```bash
printf 'Нотатки з git\n' > notatky.txt
git add notatky.txt
git commit -m "Нотатки"
git status
git push
```
```text
On branch main
Your branch is ahead of 'origin/main' by 1 commit.
  (use "git push" to publish your local commits)

nothing to commit, working tree clean
```
```text
To github.com:Evge14n/pisochnytsia.git
   ff89247..f405170  main -> main
```

`ff89247..f405170 main -> main` - на GitHub `main` пересунули з коміту `ff89247` на `f405170`. (У терміналі над цим ще будуть рядки прогресу `Enumerating objects...`: git показує прогрес, коли вивід іде на екран (git-scm.com/docs/git-push, `--progress`). Це нормально.) Тепер `git status` скаже `Your branch is up to date with 'origin/main'.`

**Крок 3. Одногрупник пушить → fetch → behind.**

```bash
cd ~/druhyi-klon
git pull
printf 'Привіт від друга\n' > druh.txt
git add druh.txt
git commit -m "Привіт від друга"
git push
```

Повертаємось до себе:

```bash
cd ~/pisochnytsia
git status
git fetch
git status
git log --oneline main..origin/main
```

Перший `git status` - `up to date` (див. передбачення 2). Далі:

```text
From github.com:Evge14n/pisochnytsia
   f405170..15cb00b  main       -> origin/main
```
```text
On branch main
Your branch is behind 'origin/main' by 1 commit, and can be fast-forwarded.
  (use "git pull" to update your local branch)

nothing to commit, working tree clean
```
```text
15cb00b (origin/main, origin/HEAD) Привіт від друга
```

`main..origin/main` читай «що є в origin/main, чого нема в main». Файлу `druh.txt` у теці ще нема: `fetch` лише подивився. Тепер можна спокійно вирішити, чи брати. Беремо:

```bash
git merge
```
```text
Updating f405170..15cb00b
Fast-forward
 druh.txt | 1 +
 1 file changed, 1 insertion(+)
 create mode 100644 druh.txt
```

`git merge` без назви зливає те, за чим стежить гілка, тобто `origin/main`. `fetch` + `merge` - рівно те, що робить `git pull`.

**Крок 4. `rejected` → pull → push.** Обидва комітять, одногрупник пушить першим:

```bash
cd ~/druhyi-klon
printf 'Ще рядок\n' >> druh.txt
git commit -am "Друг: ще рядок"
git push
cd ~/pisochnytsia
printf 'Ще нотатка\n' >> notatky.txt
git commit -am "Ще нотатка"
git push
```
```text
To github.com:Evge14n/pisochnytsia.git
 ! [rejected]        main -> main (fetch first)
error: failed to push some refs to 'github.com:Evge14n/pisochnytsia.git'
hint: Updates were rejected because the remote contains work that you do not
hint: have locally. This is usually caused by another repository pushing to
hint: the same ref. If you want to integrate the remote changes, use
hint: 'git pull' before pushing again.
hint: See the 'Note about fast-forwards' in 'git push --help' for details.
```

Код виходу 1, на GitHub нічого не змінилось. Цікаво: `git status` зараз усе ще пише `ahead of 'origin/main' by 1 commit` - памʼять `origin/main` стара, `push` її не оновив. Робимо як радить git:

```bash
git pull
```

Тут файли різні (`notatky.txt` і `druh.txt`), тож конфлікту нема, але гілки розійшлись - буде merge-коміт. На Mint відкриється nano з повідомленням `Merge branch 'main' of github.com:Evge14n/pisochnytsia` - Ctrl+O, Enter, Ctrl+X.

```text
From github.com:Evge14n/pisochnytsia
   15cb00b..5446a97  main       -> origin/main
Merge made by the 'ort' strategy.
 druh.txt | 1 +
 1 file changed, 1 insertion(+)
```
```bash
git log --oneline --graph -n 4
git push
```
```text
*   018be59 (HEAD -> main) Merge branch 'main' of github.com:Evge14n/pisochnytsia
|\
| * 5446a97 (origin/main, origin/HEAD) Друг: ще рядок
* | 38016dd Ще нотатка
|/
* 15cb00b Привіт від друга
```
```text
To github.com:Evge14n/pisochnytsia.git
   5446a97..018be59  main -> main
```

Якби ви правили ті самі рядки - `git pull` дав би конфлікт, і далі все як в уроці 08.

**Крок 5. Свій репо з нуля → `push -u`.** Буває навпаки: репо зроблено `git init` на ноутбуці, а на GitHub його ще нема. Створи на сайті **порожній** приватний репо `pisochnytsia-push` (кнопка **+** → **New repository**, Private, **без** README, .gitignore і ліцензії - інакше історії не збіжуться). Потім:

```bash
mkdir ~/git-pisochnytsia-09
cd ~/git-pisochnytsia-09
git init
printf 'print("ЛР1")\n' > lr1.py
git add lr1.py
git commit -m "ЛР1: початок"
git remote add origin git@github.com:Evge14n/pisochnytsia-push.git
git push -u origin main
```
```text
To github.com:Evge14n/pisochnytsia-push.git
 * [new branch]      main -> main
branch 'main' set up to track 'origin/main'.
```

`-u` (повністю `--set-upstream`) - запамʼятати звʼязок `main ↔ origin/main`. Потрібно один раз на гілку. Далі просто:

```bash
git status
git push
```
```text
On branch main
Your branch is up to date with 'origin/main'.

nothing to commit, working tree clean
```
```text
Everything up-to-date
```

**Для лаб:** репо `~/univer/labs` живе на GitHub (`univer-labs`, приватний). Ритуал: сів працювати - `git pull`; закінчив - `git add`, `git commit`, `git push`. Перед тим як іти з аудиторії, `git status` має сказати `up to date`, а не `ahead` - інакше ЛР лишилась лише на чужому ПК. Удома перед роботою `git fetch` і `git status`, щоб побачити, чи не пушив ти щось з університету.

### Типові помилки

- `! [rejected] main -> main (fetch first)` (повний текст у кроці 4) - на GitHub є коміти, яких нема в тебе. Лікування: `git pull`, за потреби розвʼязати конфлікт (урок 08), `git push`. **Не** `git push --force`: він затре чужі коміти на GitHub (урок 12).
- Перший `git push` у новому репо, без `-u`:
  ```text
  fatal: The current branch main has no upstream branch.
  To push the current branch and set the remote as upstream, use

      git push --set-upstream origin main

  To have this happen automatically for branches without a tracking
  upstream, see 'push.autoSetupRemote' in 'git help config'.
  ```
  Зроби, що написано: `git push -u origin main` (те саме, що `--set-upstream`).
- `git push`, а remote ще не додано:
  ```text
  fatal: No configured push destination.
  Either specify the URL from the command-line or configure a remote repository using

      git remote add <name> <url>

  and then push using the remote name

      git push <name>
  ```
  Спершу `git remote add origin git@github.com:Evge14n/РЕПО.git`.
- `git remote add origin ...` удруге (код 3):
  ```text
  error: remote origin already exists.
  ```
  Подивись `git remote -v`. Якщо адреса неправильна - `git remote set-url origin` і правильна адреса.
- `git pull` при розбіжних гілках, а `pull.rebase` не налаштовано (уроку 02 не робив):
  ```text
  hint: You have divergent branches and need to specify how to reconcile them.
  ...
  fatal: Need to specify how to reconcile divergent branches.
  ```
  Один раз: `git config --global pull.rebase false` (зливати, як у цьому курсі), потім знову `git pull`.

### Як роблять профі

- Не тягнуть наосліп: `git fetch`, глянути `git log --oneline main..origin/main` (і `git diff main origin/main`), потім `git merge`. Або `git pull --ff-only` - тягне, лише якщо можна просто перемотати, інакше зупиняється і нічого не зливає (git-scm.com/docs/git-pull).
  ```bash
  git pull --ff-only
  ```
- Що я ще **не** запушив: `git log --oneline origin/main..main` (порожньо - усе на GitHub).
  ```bash
  git log --oneline origin/main..main
  ```
- Щоб не писати `-u` для кожної нової гілки - `push.autoSetupRemote` (git-scm.com/docs/git-config; у git 2.43 на Mint працює, перевірено запуском):
  ```bash
  git config --global push.autoSetupRemote true
  git switch -c lr2
  git push
  ```
  ```text
  To github.com:Evge14n/pisochnytsia-push.git
   * [new branch]      lr2 -> lr2
  branch 'lr2' set up to track 'origin/lr2'.
  ```
- Створити репо на GitHub і одразу запушити поточну теку - одна команда gh (урок 16):
  ```bash
  gh repo create pisochnytsia-push --private --source=. --push
  ```
- Багато команд ставлять `pull.rebase true`, щоб історія була прямою, без merge-комітів від `pull`. Для початку `false` (злиття) зрозуміліше - його й лишаємо.
- `--force` у спільну гілку не пушать ніколи; якщо справді треба переписати свою гілку - `git push --force-with-lease` (урок 12).

### Самоперевірка

1. Що таке `origin` і що таке `origin/main`?
2. Чим `git fetch` відрізняється від `git pull`?
3. `git status` пише `ahead of 'origin/main' by 2 commits`. Що це значить і що робити?
4. Ти отримав `! [rejected] main -> main (fetch first)`. Твої дії?
5. Навіщо `-u` у `git push -u origin main` і коли його писати?

<details markdown="1"><summary>Відповіді</summary>

1. `origin` - назва адреси репо на GitHub (з `git clone` або `git remote add`). `origin/main` - памʼять твого git про `main` на GitHub з останнього `fetch`/`pull`/`push`.
2. `fetch` лише забирає нові коміти в `origin/main`, файли не чіпає. `pull` = `fetch` + `merge`, тобто ще й зливає в твою гілку.
3. У тебе 2 коміти, яких нема на GitHub. `git push`.
4. `git pull` (якщо конфлікт - розвʼязати, як в уроці 08), потім `git push`. Не `--force`.
5. Запамʼятати звʼязок гілки з `origin/main`, щоб далі писати просто `git push`/`git pull`. Один раз - при першому пуші нової гілки (після `git clone` для `main` уже зроблено).

</details>

### Джерела

- Pro Git, розд. 2.5 «Working with Remotes»: https://git-scm.com/book/en/v2/Git-Basics-Working-with-Remotes - відкрито 18.11.2026
- Pro Git, розд. 3.5 «Remote Branches»: https://git-scm.com/book/en/v2/Git-Branching-Remote-Branches - відкрито 18.11.2026
- git push: https://git-scm.com/docs/git-push - відкрито 18.11.2026
- git pull (`--ff-only`, `pull.rebase`): https://git-scm.com/docs/git-pull - відкрито 18.11.2026
- git fetch: https://git-scm.com/docs/git-fetch - відкрито 18.11.2026
- git config, `push.autoSetupRemote`: https://git-scm.com/docs/git-config - відкрито 18.11.2026
- GitHub, «Pushing commits to a remote repository»: https://docs.github.com/en/get-started/using-git/pushing-commits-to-a-remote-repository - відкрито 18.11.2026
- GitHub, «Getting changes from a remote repository»: https://docs.github.com/en/get-started/using-git/getting-changes-from-a-remote-repository - відкрито 18.11.2026
- gh repo create: https://cli.github.com/manual/gh_repo_create - відкрито 18.11.2026

## Тема 10. GitHub - репозиторій, README, Issues

**Навіщо:** репо `univer-labs` на GitHub має бути зрозумілим з першого погляду: викладач відкриває сторінку і одразу бачить, що де лежить (це робить README). А список «що ще доробити в ЛР3» зручно вести прямо на GitHub у Issues і закривати пункти комітами.

### Коротко

**Репозиторій на GitHub** - та сама тека з історією, що й у тебе на ноутбуці, тільки на сервері. Створити його можна двома способами: на сайті або командою `gh repo create`.

**README.md** - файл-опис у корені репо. GitHub сам показує його під списком файлів. `.md` значить **Markdown** - простий текст з позначками: `#` - заголовок, `-` - пункт списку і т.д.

**Issue** (читається «іш'ю») - картка-завдання в репо: «знайшов помилку», «доробити завдання 2». У кожного issue є номер: `#1`, `#2`, ... **Мітка** (label) - кольоровий ярлик на issue: `bug`, `documentation`, `enhancement`.

**«Closes #1» у коміті** - якщо такий коміт потрапить у гілку `main` на GitHub, issue #1 закриється сам.

```text
сайт: Issues → New issue        ноутбук: правиш файл               GitHub
  «#1 Описати README»   ───→   git commit -m "..." -m "Closes #1" ─→ git push у main ─→ #1 закрито
```

| Що зробити | Як |
|---|---|
| створити репо на сайті | `+` угорі праворуч → **New repository** |
| створити репо з терміналу | `gh repo create назва --private --add-readme --clone` |
| написати README | `nano README.md`, потім add, commit, push |
| створити issue | вкладка **Issues** → **New issue** або `gh issue create` |
| закрити issue комітом | у повідомленні коміту рядок `Closes #1` |

**Приватний чи публічний.** Публічний репо бачить увесь інтернет. Приватний бачиш лише ти і ті, кого ти сам запросив. Для лаб - приватний (щоб не списали). Приватні репо на GitHub Free безкоштовні.

**LICENSE** - файл з ліцензією: що іншим можна робити з твоїм кодом. Якщо ліцензії нема, діє звичайне авторське право: усі права твої, і ніхто не може копіювати чи поширювати твій код. Для лаб ліцензія не потрібна. Для відкритого проєкту - обирають на choosealicense.com (часто MIT).

Аналогія: репо - це папка-скоросшивач, README - титульний аркуш на ній, issues - стікери «доробити» на обкладинці.

### Передбач, потім запусти

1. Ти робиш коміт з двома `-m`: `git commit -m "Опиши пісочницю в README" -m "Closes #1"`. Що покаже `git log -1 --format=%B` (повний текст останнього коміту)?
<details markdown="1"><summary>Відповідь</summary>

Два абзаци з порожнім рядком між ними: кожен `-m` - окремий абзац.
```text
Опиши пісочницю в README

Closes #1

```
Перший рядок - заголовок коміту (його показує `git log --oneline`), а `Closes #1` - у тілі. GitHub шукає ключове слово в усьому тексті коміту.
</details>

2. Репо створено на сайті з галочкою README (або `gh repo create ... --add-readme`) і склоновано. Скільки комітів покаже `git log --oneline`?
<details markdown="1"><summary>Відповідь</summary>

Один - його зробив сам GitHub, коли створював README:
```text
9bfd519 Initial commit
```
(Хеш у тебе буде інший - так з усіма хешами в курсі.)
</details>

3. Як потім знайти, яким комітом закрито issue #1? Що покаже `git log --oneline --grep="Closes #1"`?
<details markdown="1"><summary>Відповідь</summary>

`--grep` шукає текст у повідомленнях комітів, зокрема в тілі. Покаже лише наш коміт:
```text
b91ce95 Опиши пісочницю в README
```
</details>

### Руками

Працюємо в пісочниці `~/pisochnytsia` (приватний репо з уроку 03).

**Крок 1. Issue на сайті.** Відкрий `github.com/Evge14n/pisochnytsia`:
```text
вкладка Issues → New issue
  (якщо спитає про шаблон - Open a blank issue)
Title:        Описати пісочницю в README
опис:         Зараз у README лише назва
праворуч Labels → documentation
Submit new issue
```
Issue отримає номер. Якщо це перше issue в репо - `#1`. Якщо в тебе інший номер, далі пиши свій.

Те саме з терміналу (gh з уроку 02):
```bash
cd ~/pisochnytsia
gh issue create --title "Описати пісочницю в README" --body "Зараз у README лише назва" --label documentation
gh issue list
```
Мітки `bug`, `documentation`, `enhancement`, `question` та інші GitHub створює в кожному новому репо сам.

**Крок 2. README.md.**
```bash
cd ~/pisochnytsia
git pull
nano README.md
```
Зітри все і набери (Ctrl+O, Enter - зберегти, Ctrl+X - вийти):

~~~markdown
# pisochnytsia

Пісочниця для вправ з **git**. Тут можна ламати.

## Що тут

- `README.md` - цей опис
- вправи з уроків 04-13

## Як почати

1. Склонувати репо
2. Змінити файл і зробити коміт

```text
git clone git@github.com:Evge14n/pisochnytsia.git
```

Підручник: [Pro Git українською](https://git-scm.com/book/uk/v2)
~~~

Що тут з Markdown:

| Пишеш | На GitHub буде |
|---|---|
| `# Назва` | великий заголовок (`##` - менший, і так до `######`) |
| `**git**` | **жирний** текст |
| `` `README.md` `` | моноширинний шрифт, як код |
| `- пункт` | маркований список |
| `1. пункт` | нумерований список |
| три зворотні лапки ``` і мова | блок коду |
| `[текст](https://...)` | посилання |

**Крок 3. Коміт, що закриває issue.**
```bash
git add README.md
git commit -m "Опиши пісочницю в README" -m "Closes #1"
git log -1 --format=%B
git push
```
Вивід коміту і пушу:
```text
[main 4f55914] Опиши пісочницю в README
 1 file changed, 18 insertions(+)
To github.com:Evge14n/pisochnytsia.git
   e231bed..4f55914  main -> main
```
Хеші в тебе будуть інші, а числа рядків можуть трохи відрізнятись (залежить, що було в README до того).
Онови сторінку репо: під файлами тепер гарний README. Відкрий Issues: #1 закрите, і в ньому посилання на твій коміт.

**Крок 4 (за бажанням). Новий репо з терміналу.**
```bash
cd ~
gh repo create proba-gh --private --add-readme --clone
cd ~/proba-gh
git log --oneline
```
`--private` - приватний, `--add-readme` - одразу з README, `--clone` - одразу склонувати в поточну теку. Без `--public` / `--private` gh почне питати в діалозі. Потім репо `proba-gh` можна видалити на сайті: Settings → унизу Danger Zone → Delete this repository (не перевірено).

### Типові помилки

**1. Створив репо на сайті з README, а код уже є на ноутбуці.** Ти зробив `git init` і коміти в `~/univer/labs`, а на сайті поставив галочку README. Тепер на GitHub свій коміт «Initial commit», а в тебе свої. Пуш:
```text
$ git push -u origin main
To github.com:Evge14n/univer-labs.git
 ! [rejected]        main -> main (fetch first)
error: failed to push some refs to 'github.com:Evge14n/univer-labs.git'
hint: Updates were rejected because the remote contains work that you do not
hint: have locally. This is usually caused by another repository pushing to
hint: the same ref. If you want to integrate the remote changes, use
hint: 'git pull' before pushing again.
hint: See the 'Note about fast-forwards' in 'git push --help' for details.
```
Звичайний `git pull origin main` теж не допоможе:
```text
fatal: refusing to merge unrelated histories
```
«unrelated histories» - дві історії без спільного предка. Лікування - дозволити злиття один раз:
```bash
git pull --allow-unrelated-histories origin main
git push -u origin main
```
Як не потрапити: якщо код уже є на ноутбуці, створюй на сайті **порожній** репо (без README, .gitignore і ліцензії). Документація GitHub прямо про це попереджає.

**2. Написав `Closes #1`, а issue не закрилось.** Коміт лежить в іншій гілці (наприклад, `lr3`). Issue закривається, лише коли коміт потрапить у гілку за замовчуванням (`main`). Злий гілку в `main` (урок 11) - тоді закриється.

**3. `gh` з репозиторію Mint.** Пакет gh 2.45 з Mint зламаний (падає на `gh issue view`). Став gh з офіційного репозиторію GitHub, як в уроці 02.

### Як роблять профі

- Пишуть `Closes #N` не в коміті, а в описі Pull Request (урок 11): issue закривається, коли PR зливають, і PR видно в issue як повʼязаний. Ключові слова: close, closes, closed, fix, fixes, fixed, resolve, resolves, resolved ([docs](https://docs.github.com/en/issues/tracking-your-work-with-issues/using-issues/linking-a-pull-request-to-an-issue)).
- README у кожному репо: що робить проєкт, як запустити, де шукати допомогу ([About READMEs](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-readmes)).
- Шаблони issue (тека `.github/ISSUE_TEMPLATE`), щоб усі писали баги в одному форматі ([docs](https://docs.github.com/en/communities/using-templates-to-encourage-useful-issues-and-pull-requests/about-issue-and-pull-request-templates)).
- Мітки і списки задач у Markdown: `- [ ] завдання 2`, `- [x] завдання 1` ([синтаксис](https://docs.github.com/en/get-started/writing-on-github/getting-started-with-writing-and-formatting-on-github/basic-writing-and-formatting-syntax)).
- Відкритий код - завжди з LICENSE у корені ([Licensing a repository](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/licensing-a-repository), [choosealicense.com](https://choosealicense.com)).

### Для лаб

**Для лаб:** один **приватний** репо `univer-labs`. Якщо тека `~/univer/labs` уже з комітами - створи на сайті порожній репо `univer-labs` (Private, без README) і запуш, як в уроці 09. Або одним рядком gh з самої теки:
```bash
gh repo create univer-labs --private --source . --remote origin --push
```
Потім README зі списком: `lr1/` - ЛР1, ... `lr7/` - ЛР7, і як запускати (`python3 lr1/main.py`). На кожне «доробити» (наприклад, «ЛР3: завдання 2 не проходить doctest») - issue з міткою `bug`, і коміт з `Closes #N`, коли виправиш. Викладача можна додати в приватний репо: Settings → Collaborators → Add people (не перевірено).

### Самоперевірка

1. Чим приватний репо відрізняється від публічного і який обрати для лаб?
2. Як зробити в README заголовок, список і посилання?
3. Що написати в коміті, щоб він закрив issue #4, і коли саме воно закриється?
4. Ти створив на сайті репо з README, а локально вже є коміти. Що побачиш при `git push` і як виправити?
5. Що буде з твоїм кодом у публічному репо без файлу LICENSE?

<details markdown="1"><summary>Відповіді</summary>

1. Публічний бачать усі в інтернеті, приватний - лише ти і запрошені. Для лаб - приватний.
2. `# Заголовок`, рядки `- пункт`, `[текст](https://адреса)`.
3. Рядок `Closes #4` (або `Fixes #4`, `Resolves #4`) у повідомленні коміту. Закриється, коли коміт потрапить у `main` (гілку за замовчуванням) на GitHub.
4. `! [rejected] main -> main (fetch first)`, а `git pull` скаже `refusing to merge unrelated histories`. Лікується `git pull --allow-unrelated-histories origin main`, потім `git push -u origin main`. Краще одразу створювати порожній репо.
5. Діє звичайне авторське право: дивитися і робити форк на GitHub можна, але копіювати і поширювати код без твого дозволу - ні.

</details>

### Джерела

- Creating a new repository - https://docs.github.com/en/repositories/creating-and-managing-repositories/creating-a-new-repository (відкрито 18.11.2026)
- About repositories (public / private) - https://docs.github.com/en/repositories/creating-and-managing-repositories/about-repositories (відкрито 18.11.2026)
- Linking a pull request to an issue - https://docs.github.com/en/issues/tracking-your-work-with-issues/using-issues/linking-a-pull-request-to-an-issue (відкрито 18.11.2026)
- Creating an issue - https://docs.github.com/en/issues/tracking-your-work-with-issues/using-issues/creating-an-issue (відкрито 18.11.2026)
- Managing labels - https://docs.github.com/en/issues/using-labels-and-milestones-to-track-work/managing-labels (відкрито 18.11.2026)
- Basic writing and formatting syntax - https://docs.github.com/en/get-started/writing-on-github/getting-started-with-writing-and-formatting-on-github/basic-writing-and-formatting-syntax (відкрито 18.11.2026)
- Licensing a repository - https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/licensing-a-repository (відкрито 18.11.2026)
- gh repo create, gh issue create - https://cli.github.com/manual/gh_repo_create, https://cli.github.com/manual/gh_issue_create (відкрито 18.11.2026; прапорці звірено з `gh --help` 2.105.0)

## Тема 11. Pull Request - гілка, рев'ю, merge

**Навіщо:** ЛР3 робиш у гілці `lr3`, а в `main` вона потрапляє через Pull Request. Так видно всі зміни лаби одним списком, одногрупник або викладач може залишити коментар до рядка, а `main` лишається робочою.

### Коротко

**Pull Request (PR)** - прохання на GitHub: «злий мою гілку `lr3` у `main`». У PR є опис, список комітів, усі зміни (вкладка **Files changed**) і коментарі. Номер PR іде в тому ж рахунку, що й issues: якщо в репо вже є issue #1, перший PR буде #2 (у docs дослівно не знайшов - не перевірено).

**Рев'ю** (review) - перевірка чужого коду. Рецензент обирає одне з трьох:
- **Comment** - просто коментар;
- **Approve** - «можна зливати»;
- **Request changes** - «спершу виправ».

Автор PR **не може** схвалити (Approve) свій власний PR. Тож Approve дає лише інша людина, наприклад одногрупник з доступом до репо.

```text
main:  A ─────────────── M        ← після злиття
        \               /
lr3:     B ── C ── (PR #2, рев'ю) 
```

| Крок | Команда або кнопка |
|---|---|
| гілка під лабу | `git switch -c lr3` |
| коміти | `git add`, `git commit` |
| гілку на GitHub | `git push -u origin lr3` |
| відкрити PR | жовта плашка **Compare & pull request** або `gh pr create` |
| рев'ю | **Files changed** → коментар до рядка → **Review changes** |
| злити | **Merge pull request** (або Squash / Rebase) |
| прибрати за собою | `git switch main`, `git pull`, `git branch -d lr3`, видалити гілку на GitHub |

**Три види злиття** на GitHub (кнопка Merge з випадним списком):

| Кнопка | Що зʼявиться в `main` | Як те саме в git |
|---|---|---|
| **Create a merge commit** | усі коміти гілки + окремий коміт злиття з двома батьками | `git merge --no-ff` |
| **Squash and merge** | один новий коміт «Назва PR (#2)», коміти гілки в `main` не потрапляють | `git merge --squash` + `git commit` |
| **Rebase and merge** | коміти гілки по одному, без коміту злиття, але з **новими** хешами | rebase + fast-forward |

Аналогія: PR - як здати чернетку лаби на перевірку. Викладач пише зауваження на полях (коментарі до рядків), ставить «зараховано» (Approve) або «переробити» (Request changes), і лише потім робота йде в чистовик (`main`).

### Передбач, потім запусти

1. `main` не рухалась, тож `git merge lr3` зробив би fast-forward (урок 07). А що зробить `git merge --no-ff lr3`?
<details markdown="1"><summary>Відповідь</summary>

Створить коміт злиття навіть там, де можна було просто пересунути вказівник. Саме так зливає кнопка «Create a merge commit»:
```text
*   2f51e50 Merge pull request #2 from Evge14n/lr3
|\  
| * c4894c4 ЛР3: завдання 2
| * 3204bab ЛР3: заготовка
|/  
* d850e97 Initial commit
```
</details>

2. `git merge --squash lr3` - чи буде одразу новий коміт?
<details markdown="1"><summary>Відповідь</summary>

Ні. Git лише складе всі зміни гілки в індекс і скаже `Squash commit -- not updating HEAD`. `git status --short` покаже `A  lr3.py`. Коміт робиш сам: `git commit -m "ЛР3 (#2)"`. В історії - один коміт замість двох:
```text
* 623fcfe ЛР3 (#2)
* d850e97 Initial commit
```
</details>

3. На GitHub гілку `lr3` після злиття видалили. Що покаже `git branch -r` у другому клоні, де не було `fetch`?
<details markdown="1"><summary>Відповідь</summary>

Досі `origin/lr3`. Git не знає про видалення, поки не спитає GitHub. Прибирає її `git fetch --prune`:
```text
From github.com:Evge14n/pisochnytsia
 - [deleted]         (none)     -> origin/lr3
```
</details>

### Руками

Пісочниця `~/pisochnytsia`. Хеші в тебе будуть інші.

**Крок 1. Гілка з двома комітами і push.**
```bash
cd ~/pisochnytsia
git switch main
git pull
git switch -c lr3
printf 'x = 3\nprint("ЛР3:", x)\n' > lr3.py
git add lr3.py
git commit -m "ЛР3: заготовка"
printf 'print("ЛР3: завдання 2")\n' >> lr3.py
git commit -am "ЛР3: завдання 2"
git push -u origin lr3
```
```text
To github.com:Evge14n/pisochnytsia.git
 * [new branch]      lr3 -> lr3
branch 'lr3' set up to track 'origin/lr3'.
```

**Крок 2. Відкрити PR на сайті.**
```text
github.com/Evge14n/pisochnytsia → жовта плашка над списком файлів → Compare & pull request
base: main  ←  compare: lr3
Title: ЛР3
опис: Заготовка і завдання 2
Create pull request
```
Або з терміналу:
```bash
gh pr create --base main --head lr3 --title "ЛР3" --body "Заготовка і завдання 2"
gh pr list
```

**Крок 3. Рев'ю.** Відкрий PR → вкладка **Files changed**. Наведи мишку на рядок `x = 3` → синя іконка коментаря → напиши «краще назвати змінну n?» → **Start a review**. Потім угорі **Review changes** → вибери Comment / Approve / Request changes → **Submit review**. Зі свого акаунта Approve не вийде - це для одногрупника.

Те, що рецензент бачить у Files changed, можна побачити і в терміналі. Другий клон (як в уроці 09; якщо його нема - `git clone git@github.com:Evge14n/pisochnytsia.git ~/druhyi-klon`):
```bash
cd ~/druhyi-klon
git fetch
git diff --stat origin/main...origin/lr3
git diff origin/main...origin/lr3
```
```text
 lr3.py | 3 +++
 1 file changed, 3 insertions(+)
diff --git a/lr3.py b/lr3.py
new file mode 100644
index 0000000..549455e
--- /dev/null
+++ b/lr3.py
@@ -0,0 +1,3 @@
+x = 3
+print("ЛР3:", x)
+print("ЛР3: завдання 2")
```
Три крапки `main...lr3` = «що змінилось у `lr3` від місця, де вона відгалузилась від `main`». Рецензія з gh (від одногрупника):
```bash
gh pr review 2 --comment -b "Глянь назву змінної x"
gh pr review 2 --approve
gh pr review 2 --request-changes -b "Додай doctest"
```

**Крок 4. Як виглядатиме історія - модель у git.** Кнопку на сайті в перевірці не натиснеш, тож змоделюємо два види злиття локально, у пробних гілках:
```bash
cd ~/pisochnytsia
git switch -c proba-merge main
git merge --no-ff lr3 -m "Merge pull request #2 from Evge14n/lr3"
git log --oneline --graph -4
git switch -c proba-squash main
git merge --squash lr3
git commit -m "ЛР3 (#2)"
git log --oneline --graph -3
git switch main
git branch -D proba-merge proba-squash
```
Виводи `log` - у пунктах 1 і 2 «Передбач». `-D` (велике) видаляє гілку навіть незлиту - тут можна, це пробні гілки. Повідомлення як на GitHub: merge-коміт - «Merge pull request #2 from Evge14n/lr3» і назва PR другим абзацом; squash - «ЛР3 (#2)» (так виглядають коміти в репо cli/cli і facebook/react, глянув 18.11.2026).

**Крок 5. Злити на сайті і прибрати.** У PR унизу **Merge pull request** → **Confirm merge** → зʼявиться кнопка **Delete branch** - натисни. Потім у терміналі:
```bash
git switch main
git pull
git log --oneline --graph -4
git branch -d lr3
git fetch --prune
git branch -a
```
```text
Deleted branch lr3 (was c4894c4).
From github.com:Evge14n/pisochnytsia
 - [deleted]         (none)     -> origin/lr3
* main
  remotes/origin/HEAD -> origin/main
  remotes/origin/main
```
Якщо на сайті **не** натиснув Delete branch - видали віддалену гілку з терміналу:
```bash
git push origin --delete lr3
```
```text
To github.com:Evge14n/pisochnytsia.git
 - [deleted]         lr3
```

### Типові помилки

**1. Після Squash and merge `git branch -d` не видаляє гілку.** Коміти `lr3` у `main` не потрапили (там лише новий squash-коміт), тож git думає, що гілка не злита:
```text
error: the branch 'lr3' is not fully merged.
If you are sure you want to delete it, run 'git branch -D lr3'
```
Якщо PR на сайті справді злитий (на сторінці PR позначка Merged, не перевірено) - видаляй силою:
```bash
git branch -D lr3
```
Дивина git 2.43: поки `origin/lr3` ще є локально (ти не робив `fetch --prune`), `-d` не падає, а пише попередження і видаляє:
```text
warning: deleting branch 'lr3' that has been merged to
         'refs/remotes/origin/lr3', but not yet merged to HEAD
Deleted branch lr3 (was 6214452).
```

**2. «Your branch is up to date», а на GitHub уже злитий PR.** Після злиття на сайті `git switch main` пише:
```text
Your branch is up to date with 'origin/main'.
```
Це неправда лише тому, що git порівнює з останнім, що знав про GitHub. Спершу `git pull`, і лише потім нова гілка `lr4` - інакше вона почнеться без ЛР3.

**3. Approve власного PR.** Документація GitHub: «Pull request authors cannot approve their own pull requests». Для схвалення потрібна друга людина з доступом до репо (Settings → Collaborators, не перевірено). Для своїх лаб досить Comment собі ж.

**4. Дописав коміт у `lr3` після злиття PR.** Ці коміти в `main` не підуть - PR уже закритий. Онови `main` (`git pull`) і зроби нову гілку і новий PR.

### Як роблять профі

- Кожна зміна - через PR, навіть у соло-проєктах: видно, що і навіщо змінено ([Creating a pull request](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/proposing-changes-to-your-work-with-pull-requests/creating-a-pull-request)).
- У налаштуваннях репо вмикають **Automatically delete head branches** (Settings → General → Pull Requests) - гілка зникає сама після злиття ([docs](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/configuring-pull-request-merges/managing-the-automatic-deletion-of-branches)).
- Захищають `main` правилами (ruleset): зливати лише через PR з Approve; сторінка документації називає плани Team і Enterprise, тож на безкоштовному плані для приватного репо, схоже, недоступно (не перевірено) ([About rulesets](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/about-rulesets)).
- Багато команд обирають Squash and merge: в `main` один акуратний коміт на PR ([About pull request merges](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/incorporating-changes-from-a-pull-request/about-pull-request-merges)).
- У описі PR пишуть `Closes #N` - issue закриється при злитті (урок 10).
- Злиття з терміналу: `gh pr merge 2 --squash --delete-branch` ([gh pr merge](https://cli.github.com/manual/gh_pr_merge)).

### Для лаб

**Для лаб:** у `univer-labs` кожна лаба - своя гілка `lr1` ... `lr7`. Коли лаба готова - PR `lr3 → main` з описом «що зроблено, які завдання проходять doctest» і `Closes #N`, якщо закриваєш issue. Перед здачею кинь викладачу посилання на PR: там видно всі зміни лаби одним списком у Files changed. Після злиття - `git switch main`, `git pull`, `git branch -d lr3`. Для лаб зручно Squash and merge: одна лаба = один коміт у `main`.

### Самоперевірка

1. Що таке Pull Request і чим він кращий за `git merge` у себе на ноутбуці?
2. Які три відповіді може дати рецензент і хто не може поставити Approve?
3. Чим відрізняється історія `main` після Create a merge commit і після Squash and merge?
4. Після squash-злиття `git branch -d lr3` пише `not fully merged`. Чому і що робити?
5. Які команди виконати на ноутбуці після злиття PR, щоб усе було чисто?

<details markdown="1"><summary>Відповіді</summary>

1. Прохання на GitHub злити гілку в `main`. Видно всі зміни (Files changed), можна обговорити кожен рядок і дати схвалення до злиття.
2. Comment, Approve, Request changes. Автор PR не може схвалити свій PR.
3. Merge commit: усі коміти гілки + коміт злиття з двома батьками. Squash: лише один новий коміт «Назва (#2)».
4. Коміти `lr3` не потрапили в `main`, там новий squash-коміт. Якщо PR злитий на сайті - `git branch -D lr3`.
5. `git switch main`, `git pull`, `git branch -d lr3`, і `git fetch --prune` (або `git push origin --delete lr3`, якщо на сайті гілку не видалив).

</details>

### Джерела

- Creating a pull request - https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/proposing-changes-to-your-work-with-pull-requests/creating-a-pull-request (відкрито 18.11.2026)
- Reviewing proposed changes in a pull request - https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/reviewing-changes-in-pull-requests/reviewing-proposed-changes-in-a-pull-request (відкрито 18.11.2026)
- Approving a pull request with required reviews («Pull request authors cannot approve their own pull requests») - https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/reviewing-changes-in-pull-requests/approving-a-pull-request-with-required-reviews (відкрито 18.11.2026)
- About pull request merges - https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/incorporating-changes-from-a-pull-request/about-pull-request-merges (відкрито 18.11.2026)
- Merging a pull request - https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/incorporating-changes-from-a-pull-request/merging-a-pull-request (відкрито 18.11.2026)
- git merge (--no-ff, --squash), git branch, git fetch --prune - https://git-scm.com/docs/git-merge, https://git-scm.com/docs/git-branch, https://git-scm.com/docs/git-fetch (відкрито 18.11.2026)
- gh pr create / review / merge - https://cli.github.com/manual/gh_pr_create, https://cli.github.com/manual/gh_pr_review, https://cli.github.com/manual/gh_pr_merge (відкрито 18.11.2026; прапорці звірено з `gh --help` 2.105.0)

## Тема 12. Скасувати безпечно - restore, revert, reset, reflog

**Навіщо:** у ЛР2 зіпсував робочу функцію, закомітив не те, або вже запушив помилку на GitHub. У git майже все можна повернути - треба лише знати, яка команда для якого випадку і яка з них небезпечна.

### Коротко

Згадай три зони з уроку 01: **робоча тека** (файли, які бачиш) → **індекс** (що піде в коміт) → **історія** (коміти). Кожна команда скасування працює зі своєю зоною:

| Команда | Що скасовує | Безпечно після push? |
|---|---|---|
| `git restore файл` | зміни в робочій теці (повертає файл як в останньому коміті) | так, коміти не чіпає |
| `git restore --staged файл` | `git add` (зміни лишаються у файлі) | так |
| `git commit --amend` | переписує **останній** коміт | **ні**, лише до push |
| `git reset --soft HEAD~1` | прибирає останній коміт, зміни лишаються в індексі | **ні**, лише до push |
| `git revert ХЕШ` | робить **новий** коміт, протилежний до старого | **так**, це і є спосіб після push |
| `git reset --hard ...` | пересуває гілку і **затирає** робочу теку | ні, і обережно |
| `git reflog` | показує, де був HEAD - звідси рятують «втрачені» коміти | - |

`HEAD~1` - «один коміт перед поточним». `HEAD@{1}` - «де HEAD був один крок тому» (з журналу reflog).

**Reflog** - журнал git: кожен коміт, перемикання, reset записується туди. Тому навіть після `reset --hard` закомічене не зникає одразу: записи reflog живуть 90 днів (а недосяжні коміти - 30), потім git може їх прибрати. Незакомічене reflog **не** рятує.

Аналогія: `revert` - як дописати в зошит «пункт 3 - помилка, правильно так», а `reset` - як вирвати сторінку. Вирвати можна лише зі свого чорновика (до push), а не з журналу, який уже бачили інші.

### Передбач, потім запусти

1. Ти зробив `git add rozrahunok.py`, а потім `git restore --staged rozrahunok.py`. Що буде з твоїми змінами у файлі? Що покаже `git status --short`?
<details markdown="1"><summary>Відповідь</summary>

Зміни лишаються у файлі, просто вже не в індексі. До: `M  rozrahunok.py` (M у першій колонці - в індексі), після: ` M rozrahunok.py` (M у другій - лише в робочій теці).
</details>

2. Останній коміт «Додай висоту» ще не запушений. Після `git reset --soft HEAD~1` - де файл `vysota.py`?
<details markdown="1"><summary>Відповідь</summary>

Коміту нема, а файл на місці і вже в індексі: `git status --short` показує `A  vysota.py`. Можна дописати і закомітити заново.
</details>

3. Коміт «Спроба: g = 0» уже на GitHub. Скільки комітів стане після `git revert --no-edit HEAD`?
<details markdown="1"><summary>Відповідь</summary>

На один **більше**: старий коміт лишається, а поверх - новий, що його скасовує.
```text
31e6c9b Revert "Спроба: g = 0"
78dc358 Спроба: g = 0
07ae21c Додай висоту h = 2.5
```
</details>

4. Після `git reset --hard HEAD~1` коміт «Важливий файл» зник з `git log`. Чи покаже його `git reflog -3`?
<details markdown="1"><summary>Відповідь</summary>

Так, другим рядком, як `HEAD@{1}`:
```text
31e6c9b HEAD@{0}: reset: moving to HEAD~1
b319df5 HEAD@{1}: commit: Важливий файл
31e6c9b HEAD@{2}: revert: Revert "Спроба: g = 0"
```
</details>

### Руками

Пісочниця `~/pisochnytsia`, гілка `main`. Хеші в тебе будуть інші.

**Крок 1. Підготовка.**
```bash
cd ~/pisochnytsia
git switch main
git pull
printf 'g = 9.8\nprint("g =", g)\n' > rozrahunok.py
git add rozrahunok.py
git commit -m "Додай розрахунок g"
```

**Крок 2. `restore` - зіпсував файл, ще не add.**
```bash
printf 'g = 100\n' > rozrahunok.py
git status --short
git restore rozrahunok.py
cat rozrahunok.py
```
```text
 M rozrahunok.py
g = 9.8
print("g =", g)
```
Увага: `git restore` затирає незакомічені зміни **назавжди**. Перед ним глянь `git diff`.

**Крок 3. `restore --staged` - зайвий add.**
```bash
printf 'print("кінець")\n' >> rozrahunok.py
git add rozrahunok.py
git status --short
git restore --staged rozrahunok.py
git status --short
git restore rozrahunok.py
```
```text
M  rozrahunok.py
 M rozrahunok.py
```

**Крок 4. `--amend` - помилка в повідомленні (до push).**
```bash
printf 'g = 9.81\nprint("g =", g)\n' > rozrahunok.py
git commit -am "Уточни g до 9.18"
git commit --amend -m "Уточни g до 9.81"
git log --oneline -2
```
```text
[main 2058b78] Уточни g до 9.81
 Date: Wed Nov 18 10:18:55 2026 +0000
 1 file changed, 1 insertion(+), 1 deletion(-)
2058b78 Уточни g до 9.81
539e4ed Додай розрахунок g
```
`--amend` не править старий коміт, а робить новий замість нього (інший хеш). Рядок `Date:` - git показує, що дата автора лишилась від старого коміту. Забув файл у коміті? `git add файл`, потім `git commit --amend --no-edit` (повідомлення те саме).

**Крок 5. `reset --soft` - переробити останній коміт (до push).**
```bash
printf 'h = 2\n' > vysota.py
git add vysota.py
git commit -m "Додай висоту"
git reset --soft HEAD~1
git status --short
printf 'h = 2.5\n' > vysota.py
git add vysota.py
git commit -m "Додай висоту h = 2.5"
git log --oneline -3
```
```text
A  vysota.py
07ae21c Додай висоту h = 2.5
2058b78 Уточни g до 9.81
539e4ed Додай розрахунок g
```

**Крок 6. `revert` - помилка вже на GitHub.**
```bash
git push
printf 'g = 0\n' > rozrahunok.py
git commit -am "Спроба: g = 0"
git push
git revert --no-edit HEAD
git log --oneline -3
cat rozrahunok.py
git push
```
```text
[main 31e6c9b] Revert "Спроба: g = 0"
 Date: Wed Nov 18 10:18:55 2026 +0000
 1 file changed, 2 insertions(+), 1 deletion(-)
...
g = 9.81
print("g =", g)
To github.com:Evge14n/pisochnytsia.git
   78dc358..31e6c9b  main -> main
```
`--no-edit` - взяти готове повідомлення `Revert "..."`. Без нього відкриється nano з цим повідомленням (Ctrl+O, Enter, Ctrl+X). Замість `HEAD` можна дати хеш будь-якого старішого коміту.

**Крок 7. `reset --hard` і порятунок через reflog.**

> **Увага.** `git reset --hard` пересуває гілку назад і **затирає** робочу теку. Коміти можна врятувати через reflog, а незакомічені зміни - ні. Тут ми робимо це навмисно, у пісочниці, з усім закоміченим.

```bash
printf 'важливо\n' > vazhlyve.txt
git add vazhlyve.txt
git commit -m "Важливий файл"
git reset --hard HEAD~1
ls vazhlyve.txt
git reflog -3
git reset --hard HEAD@{1}
cat vazhlyve.txt
git push
```
```text
HEAD is now at 31e6c9b Revert "Спроба: g = 0"
ls: cannot access 'vazhlyve.txt': No such file or directory
31e6c9b HEAD@{0}: reset: moving to HEAD~1
b319df5 HEAD@{1}: commit: Важливий файл
31e6c9b HEAD@{2}: revert: Revert "Спроба: g = 0"
HEAD is now at b319df5 Важливий файл
важливо
```
Файл повернувся з тим самим вмістом. Можна і за хешем з reflog: `git reset --hard b319df5` (у тебе свій хеш).

**Чому не `git push --force`.** Якщо зробити `reset` вже запушеного коміту, звичайний push відмовить (див. «Типові помилки»). «Пробити» його можна силою:
```text
git push --force              # НЕ в спільну гілку: GitHub стане як у тебе, а чужі коміти, яких ти не бачив, зникнуть
git push --force-with-lease   # «сила з перевіркою»: відмовить, якщо на GitHub зʼявилось щось, чого ти ще не забрав
```
Документація git про `--force`: «It can cause the remote repository to lose commits». Тому в `main` і будь-яку гілку, з якою працює ще хтось, силою не пушать взагалі - лише `revert`. `--force-with-lease` - для своєї гілки, якщо дуже треба переписати історію.

**Що сталося → чим лікувати:**

| Що сталося | Чим лікувати |
|---|---|
| зіпсував файл, ще не `add` | `git restore файл` |
| зробив `add` не того файлу | `git restore --staged файл` |
| помилка в повідомленні останнього коміту, ще не push | `git commit --amend -m "нове"` |
| забув файл в останньому коміті, ще не push | `git add файл`, `git commit --amend --no-edit` |
| хочу переробити останній коміт, ще не push | `git reset --soft HEAD~1` |
| поганий коміт уже на GitHub | `git revert --no-edit ХЕШ`, потім `git push` |
| коміт «зник» після `reset --hard` | `git reflog`, потім `git reset --hard HEAD@{N}` |
| зробив `reset` після push, і push відмовив | `git pull` (поверне коміт), потім `git revert` |

### Типові помилки

**1. `restore` нового файлу.** Файл ще ні разу не був у коміті - git про нього не знає:
```text
$ git restore novyi.txt
error: pathspec 'novyi.txt' did not match any file(s) known to git
```
Непотрібний новий файл просто видали: `rm novyi.txt`.

**2. `reset` після push - і push не проходить.**
```text
$ git push
To github.com:Evge14n/pisochnytsia.git
 ! [rejected]        main -> main (non-fast-forward)
error: failed to push some refs to 'github.com:Evge14n/pisochnytsia.git'
hint: Updates were rejected because the tip of your current branch is behind
hint: its remote counterpart. If you want to integrate the remote changes,
hint: use 'git pull' before pushing again.
hint: See the 'Note about fast-forwards' in 'git push --help' for details.
```
Не пробивай силою. `git pull` поверне коміт з GitHub (`Fast-forward`), а далі скасовуй правильно - `git revert`.

**3. `reset --hard` з незакоміченими змінами.** Дописав у файл, не закомітив, зробив `git reset --hard` - дописане зникло, і в reflog його нема (reflog знає лише коміти). Перед `--hard` завжди `git status`, а що шкода - закоміть або сховай (`git stash`, урок 13).

**4. `git revert` без `--no-edit` «завис».** Він відкрив nano з повідомленням. Збережи і вийди: Ctrl+O, Enter, Ctrl+X.

### Як роблять профі

- Після push - лише `revert`, історію спільних гілок не переписують ([Pro Git 2.4 «Undoing Things»](https://git-scm.com/book/en/v2/Git-Basics-Undoing-Things)).
- `--force-with-lease` замість `--force`, і лише у свою гілку ([git push](https://git-scm.com/docs/git-push)).
- На GitHub `main` роблять захищеною гілкою: «By default, GitHub blocks force pushes on all protected branches» (чи доступно для приватного репо на безкоштовному плані - не перевірено) ([About protected branches](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/about-protected-branches)).
- Що саме робить `reset` з трьома зонами - [Pro Git 7.7 «Reset Demystified»](https://git-scm.com/book/en/v2/Git-Tools-Reset-Demystified).
- Скасувати злитий PR на GitHub - кнопка Revert на сторінці PR, вона робить revert-PR ([Reverting a pull request](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/incorporating-changes-from-a-pull-request/reverting-a-pull-request)).

### Для лаб

**Для лаб:** перед ризикованою правкою ЛР5 (переписати функцію, запустити `black`) - коміт. Зламав і не комітив - `git restore lr5/main.py`. Закомітив з помилкою в повідомленні - `--amend`, поки не запушив. Уже на GitHub (викладач міг бачити) - тільки `git revert`. Загубив коміт після експериментів з `reset` - `git reflog` у `~/univer/labs`.

### Самоперевірка

1. Чим `git restore файл` відрізняється від `git restore --staged файл`?
2. Чому після push треба `git revert`, а не `git reset`?
3. Що робить `git reset --soft HEAD~1` і коли ним можна користуватись?
4. Ти зробив `git reset --hard HEAD~1` і загубив коміт. Як його повернути?
5. Чим `git push --force-with-lease` безпечніший за `git push --force`?

<details markdown="1"><summary>Відповіді</summary>

1. Перша повертає вміст файлу з останнього коміту (зміни зникають), друга лише виймає файл з індексу (зміни лишаються у файлі).
2. `revert` додає новий коміт і не переписує історію, яку вже бачать інші. Після `reset` push відмовить, а сила затре чужі коміти.
3. Прибирає останній коміт, а його зміни лишає в індексі. Лише до push.
4. `git reflog` - знайти рядок `commit: ...` (тут `HEAD@{1}`), потім `git reset --hard HEAD@{1}`.
5. Він відмовить, якщо на GitHub зʼявились коміти, яких ти ще не бачив, тож чужу роботу не затре.

</details>

### Джерела

- Pro Git 2.4 «Undoing Things» - https://git-scm.com/book/en/v2/Git-Basics-Undoing-Things (відкрито 18.11.2026)
- Pro Git 7.7 «Reset Demystified» - https://git-scm.com/book/en/v2/Git-Tools-Reset-Demystified (відкрито 18.11.2026)
- git restore, git revert, git reset, git reflog - https://git-scm.com/docs/git-restore, https://git-scm.com/docs/git-revert, https://git-scm.com/docs/git-reset, https://git-scm.com/docs/git-reflog (відкрито 18.11.2026)
- git gc (reflog 90 і 30 днів) - https://git-scm.com/docs/git-gc (відкрито 18.11.2026)
- git push (--force, --force-with-lease) - https://git-scm.com/docs/git-push (відкрито 18.11.2026)
- About protected branches - https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/about-protected-branches (відкрито 18.11.2026)

## Тема 13. stash - відкласти зміни

**Навіщо:** пишеш ЛР4 у гілці `lr4`, половина завдання 2 ще не працює, і тут викладач каже: «в ЛР1 помилка у виводі, виправ до пари». Комітити недописане не хочеться, а перемкнутись на `main` git не дає. `git stash` ховає недописане в схованку, а потім повертає.

### Коротко

**Stash** (схованка) - окрема полиця в git, куди можна покласти незакомічені зміни. Робоча тека стає чистою, як після коміту, і можна спокійно перемикати гілки.

```text
lr4 (брудна) ──git stash──→ полиця stash@{0}       робоча тека чиста → git switch main → виправив → git switch lr4
                                    │
lr4 (знову брудна) ←──git stash pop─┘
```

| Команда | Що робить |
|---|---|
| `git stash` | сховати зміни у відстежуваних файлах (і в індексі) |
| `git stash -u` | те саме + нові файли, яких git ще не знає (untracked) |
| `git stash list` | список схованок: `stash@{0}` - найсвіжіша |
| `git stash pop` | повернути найсвіжішу і **видалити** її з полиці |
| `git stash apply` | повернути, але **залишити** на полиці |
| `git stash drop` | видалити найсвіжішу схованку |

Аналогія: прибрав зі столу недописану лабу в шухляду, щоб звільнити місце під терміновий ЛР1. Потім дістав і продовжив. `pop` - дістав і шухляда порожня, `apply` - дістав копію, оригінал лишився в шухляді.

### Передбач, потім запусти

1. У гілці `lr4` файл `lr4.py` змінений і не закомічений. Що скаже `git switch main`, якщо в `main` файлу `lr4.py` нема?
<details markdown="1"><summary>Відповідь</summary>

Відмовить: при перемиканні git мав би прибрати `lr4.py` разом з твоїми змінами.
```text
error: Your local changes to the following files would be overwritten by checkout:
	lr4.py
Please commit your changes or stash them before you switch branches.
Aborting
```
Git сам підказує вихід: commit або stash.
</details>

2. Окрім зміненого `lr4.py`, є новий файл `chernetka.txt`, якого git ще не бачив. Що покаже `git status --short` після простого `git stash`?
<details markdown="1"><summary>Відповідь</summary>

```text
?? chernetka.txt
```
Без `-u` нові (untracked) файли не ховаються - лишаються в теці. `git stash -u` сховає і їх.
</details>

3. Після `git stash apply` - що покаже `git stash list`?
<details markdown="1"><summary>Відповідь</summary>

Схованка досі там:
```text
stash@{0}: WIP on lr4: 5bd6881 ЛР4: заготовка
```
`apply` не видаляє. Після `pop` список був би порожній. WIP = «work in progress», робота в процесі; далі - гілка і останній коміт.
</details>

4. `pop` дав конфлікт. Схованка видалилась чи ні?
<details markdown="1"><summary>Відповідь</summary>

Ні. Git пише `The stash entry is kept in case you need it again.` Розвʼяжи конфлікт, потім `git stash drop` сам.
</details>

### Руками

Пісочниця `~/pisochnytsia`. Хеші в тебе будуть інші.

**Крок 1. Гілка `lr4` із заготовкою.**
```bash
cd ~/pisochnytsia
git switch main
git pull
git switch -c lr4
printf 'def f(x):\n    return x\n' > lr4.py
git add lr4.py
git commit -m "ЛР4: заготовка"
```

**Крок 2. Недописане - і перемкнутись не виходить.**
```bash
printf '# завдання 2 - ще пишу\n' >> lr4.py
printf 'ідеї до звіту\n' > chernetka.txt
git status --short
git switch main
```
```text
 M lr4.py
?? chernetka.txt
error: Your local changes to the following files would be overwritten by checkout:
	lr4.py
Please commit your changes or stash them before you switch branches.
Aborting
```

**Крок 3. Простий `stash` і повернення.**
```bash
git stash
git status --short
git stash list
git stash pop
```
```text
Saved working directory and index state WIP on lr4: 5bd6881 ЛР4: заготовка
?? chernetka.txt
stash@{0}: WIP on lr4: 5bd6881 ЛР4: заготовка
On branch lr4
Changes not staged for commit:
...
	modified:   lr4.py
...
Dropped refs/stash@{0} (d72d50356fc7dbbcf1887bc812215b6dabce8eae)
```
`chernetka.txt` лишилась на місці - простий `stash` її не взяв.

**Крок 4. `stash -u`, термінова правка в `main`, повернення.**
```bash
git stash -u
git status --short
git switch main
printf 'print("ЛР1, виправлено")\n' > lr1.py
git add lr1.py
git commit -m "ЛР1: виправ вивід"
git switch lr4
git stash apply
git stash list
git stash drop
```
Після `stash -u` `git status --short` нічого не друкує - тека чиста, і `git switch main` проходить. Після `apply` - `lr4.py` знову змінений, `chernetka.txt` знову є, а схованка ще на полиці; `drop` її прибирає:
```text
Dropped refs/stash@{0} (65d8f24b94b7f4ebc41b4ce380162538447b0ad5)
```

**Крок 5. Справжній конфлікт при `pop`.** Ховаємо зміни, а в той самий рядок `lr4.py` комітимо інше:
```bash
git stash
printf 'def f(x):\n    return 2 * x\n' > lr4.py
git commit -am "ЛР4: подвоєння"
git stash pop
cat lr4.py
git status --short
git stash list
```
```text
Auto-merging lr4.py
CONFLICT (content): Merge conflict in lr4.py
...
The stash entry is kept in case you need it again.
def f(x):
<<<<<<< Updated upstream
    return 2 * x
=======
    return x
# завдання 2 - ще пишу
>>>>>>> Stashed changes
UU lr4.py
?? chernetka.txt
stash@{0}: WIP on lr4: 5bd6881 ЛР4: заготовка
```
Маркери як в уроці 08, тільки підписи інші: `Updated upstream` - те, що зараз у гілці, `Stashed changes` - те, що було в схованці. Відкрий `nano lr4.py` і залиш обидві частини, як треба:
```bash
nano lr4.py
```
```text
def f(x):
    return 2 * x
# завдання 2 - ще пишу
```
Потім:
```bash
git add lr4.py
git stash drop
git status --short
git commit -m "ЛР4: завдання 2, чернетка"
```
```text
Dropped refs/stash@{0} (d72d50356fc7dbbcf1887bc812215b6dabce8eae)
M  lr4.py
?? chernetka.txt
```

### Типові помилки

**1. `switch` не пускає.**
```text
error: Your local changes to the following files would be overwritten by checkout:
	lr4.py
Please commit your changes or stash them before you switch branches.
Aborting
```
`git stash` (або `git stash -u`, якщо є нові файли), потім `git switch main`. Повернувшись - `git stash pop`.

**2. Ховаєш лише новий файл.** Якщо змінених відстежуваних файлів нема, а є тільки новий `tmp.txt`:
```text
$ git stash
No local changes to save
```
Файл не сховано, він далі в теці. Потрібен `git stash -u`.

**3. Конфлікт при `pop` - і схованка «досі там».**
```text
The stash entry is kept in case you need it again.
```
Це нормально. Розвʼяжи конфлікт, `git add файл`, потім `git stash drop`. Не роби `pop` вдруге - зміни вже в файлі, лишилось тільки `drop`.

**4. `pop`, коли полиця порожня.**
```text
$ git stash pop
No stash entries found.
```
Схованку вже дістали (`pop`) або видалили. Перевір `git stash list`.

**5. Забута полиця.** Схованки не привʼязані до гілки і не йдуть на GitHub (`git push` їх не відправляє). Через тиждень у `git stash list` п'ять `WIP on lr4` - і не памʼятаєш, що де. Не тримай там нічого довго: повернувся - `pop`.

### Як роблять профі

- Підписують схованку: `git stash push -m "ЛР4 завд. 2 недописане"` - у `stash list` буде `stash@{0}: On lr4: ЛР4 завд. 2 недописане` ([git stash](https://git-scm.com/docs/git-stash)).
- Перед `pop` дивляться, що всередині: `git stash show -p` ([Pro Git 7.3 «Stashing and Cleaning»](https://git-scm.com/book/en/v2/Git-Tools-Stashing-and-Cleaning)).
- Якщо робота довга - замість stash роблять коміт «WIP» у своїй гілці і потім переробляють його (`git reset --soft HEAD~1`, урок 12): коміт не загубиться і є в reflog.
- Для довгої паралельної роботи над двома гілками - `git worktree`: друга тека з іншою гілкою того самого репо ([git worktree](https://git-scm.com/docs/git-worktree)).

### Для лаб

**Для лаб:** робиш ЛР4 у `~/univer/labs` (гілка `lr4`), а треба терміново виправити ЛР1 у `main` перед здачею: `git stash -u` → `git switch main` → правка, коміт, push → `git switch lr4` → `git stash pop`. Якщо `pop` дав конфлікт (ти міняв ту саму функцію) - як у кроці 5: nano, `git add`, `git stash drop`.

### Самоперевірка

1. Навіщо `git stash`, якщо можна просто закомітити?
2. Чим `git stash -u` відрізняється від `git stash`?
3. Чим `git stash pop` відрізняється від `git stash apply`?
4. Що робити, якщо `git stash pop` дав конфлікт?
5. Що зробиш, якщо `git switch main` пише «Your local changes ... would be overwritten by checkout»?

<details markdown="1"><summary>Відповіді</summary>

1. Щоб не робити коміт з недописаним кодом і швидко звільнити робочу теку для іншої гілки.
2. `-u` ховає ще й нові файли, яких git не відстежує (untracked).
3. `pop` повертає зміни і видаляє схованку, `apply` повертає і залишає її (видалиш потім `drop`).
4. Розвʼязати конфлікт у файлі (nano), `git add файл`, потім `git stash drop` - схованка після конфлікту лишається.
5. `git stash` (або `git stash -u`), `git switch main`, зробити справу, повернутись і `git stash pop`.

</details>

### Джерела

- Pro Git 7.3 «Stashing and Cleaning» - https://git-scm.com/book/en/v2/Git-Tools-Stashing-and-Cleaning (відкрито 18.11.2026)
- git stash - https://git-scm.com/docs/git-stash (відкрито 18.11.2026)
- git switch - https://git-scm.com/docs/git-switch (відкрито 18.11.2026)
- git worktree - https://git-scm.com/docs/git-worktree (відкрито 18.11.2026)

## Тема 14. Теги - позначити здачу

**Навіщо:** ти здав ЛР1, а через тиждень ще щось у ній підправив. Викладач питає: «А що саме ти показував мені на парі?»
Тег - це наліпка `lr1-zdano` на коміт, який ти здав. Вона не зсувається, тож відповідь завжди одна команда.

### Коротко

**Тег** - назва, яку назавжди приклеїли до одного коміту. Гілка (Урок 07) - теж назва коміту, але вона **їде вперед**
з кожним новим комітом. Тег стоїть на місці.

```text
                           lr1-zdano (тег - стоїть)
                               │
  a1b2c3d ──── 73942e5 ──── baa1934 ──── 99d1fc7
                                            │
                                          main (гілка - їде вперед з кожним комітом)
```

Аналогія: гілка - закладка, яку ти перекладаєш на сторінку, де зупинився. Тег - наліпка «здав тут» на конкретній сторінці.

Теги бувають двох видів:

| Вид | Як створити | Що зберігає | Коли брати |
|---|---|---|---|
| легкий | `git tag lr1-chernetka` | лише назву → коміт | для себе, на хвилину |
| **анотований** | `git tag -a lr1-zdano -m "ЛР1 здано"` | назву, автора, дату, повідомлення | **здача, версія** - усе, що бачать інші |

| Команда | Що робить |
|---|---|
| `git tag` | список тегів |
| `git tag -n` | список з першим рядком повідомлення |
| `git tag -a lr1-start -m "..." HEAD~1` | тег на старіший коміт (тут - на попередній) |
| `git show lr1-zdano` | хто, коли і з яким повідомленням поставив тег + сам коміт |
| `git push --follow-tags` | пушить коміти **і анотовані** теги (легкі - ні!) |
| `git push origin lr1-zdano` | пушить один тег будь-якого виду |
| `git tag -d lr1-chernetka` | видалити тег у себе |
| `git push origin --delete lr1-chernetka` | видалити тег на GitHub |
| `git checkout lr1-zdano` | подивитися файли, якими вони були на здачі (detached HEAD, нижче) |

Головне правило: **звичайний `git push` тегів не пушить.** Тег живе лише у тебе, поки ти не відправиш його окремо.

### Передбач, потім запусти

1. У тебе два нові коміти, ти їх уже запушив. Тепер `git tag -a lr1-zdano -m "ЛР1 здано викладачу"` і `git push`.
   Що напише `git push` і чи буде тег на GitHub?
   <details markdown="1"><summary>Відповідь</summary>

   ```text
   Everything up-to-date
   ```
   Тегу на GitHub **нема**: `git push` без прапорців відправляє лише гілку, а нових комітів у ній нема.
   Тег треба відправити окремо (крок 4 у «Руками»).
   </details>

2. Є легкий тег `lr1-chernetka` і анотований `lr1-zdano` на тому самому коміті. Запускаєш `git push --follow-tags`.
   Скільки тегів поїде на GitHub?
   <details markdown="1"><summary>Відповідь</summary>

   Один - `lr1-zdano`. `--follow-tags` бере лише **анотовані** теги. Легкий доведеться пушити окремо:
   `git push origin lr1-chernetka`.
   </details>

3. `git checkout lr1-zdano` - на якій гілці ти опинишся?
   <details markdown="1"><summary>Відповідь</summary>

   Ні на якій. git напише `You are in 'detached HEAD' state` - «HEAD відчеплений»: ти стоїш на коміті, а не на гілці.
   Дивитися можна, комітити - краще ні (див. «Типові помилки»). Назад: `git switch main`.
   </details>

4. Тег `lr1-zdano` уже є. Ти виправив опечатку і знову пишеш `git tag -a lr1-zdano -m "ЛР1 здано ще раз"`. Що буде?
   <details markdown="1"><summary>Відповідь</summary>

   ```text
   fatal: tag 'lr1-zdano' already exists
   ```
   Код виходу 128, нового тегу нема. Два теги з однією назвою бути не може.
   </details>

### Руками

Пісочниця - клон `~/pisochnytsia` з Уроку 03. Хеші комітів у тебе будуть інші - це нормально.
Рядок `To /home/...` у виводі нижче = у тебе буде `To github.com:Evge14n/pisochnytsia.git`.

**Крок 1. Два коміти «лаби» і push.**

```bash
cd ~/pisochnytsia
printf 'print("ЛР1, завдання 1")\n' > lr1.py
git add lr1.py
git commit -m "ЛР1: завдання 1"
printf 'print("ЛР1, завдання 2")\n' >> lr1.py
git commit -am "ЛР1: завдання 2"
git push
```

**Крок 2. Легкий і анотований тег.**

```bash
git tag lr1-chernetka
git tag -a lr1-zdano -m "ЛР1 здано викладачу"
git tag
git tag -n
```
```text
lr1-chernetka
lr1-zdano
lr1-chernetka   ЛР1: завдання 2
lr1-zdano       ЛР1 здано викладачу
```
`git tag -n` для легкого тегу показує повідомлення **коміту** (своє в нього нема), для анотованого - повідомлення **тегу**.

**Крок 3. Чим вони різні всередині.**

```bash
git show lr1-zdano --stat
```
```text
tag lr1-zdano
Tagger: Твоє Імʼя <128326252+Evge14n@users.noreply.github.com>
Date:   Wed Nov 18 10:20:11 2026 +0000

ЛР1 здано викладачу

commit baa1934646dbbd7c5cf498cb02332e01ec470396
Author: Твоє Імʼя <128326252+Evge14n@users.noreply.github.com>
Date:   Wed Nov 18 10:20:11 2026 +0000

    ЛР1: завдання 2

 lr1.py | 1 +
 1 file changed, 1 insertion(+)
```
(У терміналі після хешу коміту ще будуть дужки з гілками й тегами, як у `git log --decorate` нижче.)
Спершу йде сам тег (хто поставив, коли, навіщо), потім коміт. `git show lr1-chernetka --stat` одразу починається з
`commit` - у легкого тегу нема ні автора, ні дати.

Ще одна перевірка - якого типу обʼєкт стоїть за назвою:

```bash
git cat-file -t lr1-chernetka
git cat-file -t lr1-zdano
git log --oneline --decorate -n 2
```
```text
commit
tag
baa1934 (HEAD -> main, tag: lr1-zdano, tag: lr1-chernetka, origin/main, origin/HEAD) ЛР1: завдання 2
73942e5 ЛР1: завдання 1
```
Легкий тег - просто назва коміту. Анотований - окремий обʼєкт `tag` у репозиторії, який вказує на коміт.
`--decorate` дописує в дужках, які гілки й теги стоять на коміті (у терміналі `git log --oneline` робить це й сам).

**Крок 4. Відправити теги на GitHub.**

```bash
git push --follow-tags
git ls-remote --tags origin
```
```text
To /home/evgen/.cache/ugit.qVE6ej/u14/github/Evge14n/pisochnytsia.git
 * [new tag]         lr1-zdano -> lr1-zdano
d0e7a5c2ff6b6ed977afd50e6136c51b1a49219c	refs/tags/lr1-zdano
baa1934646dbbd7c5cf498cb02332e01ec470396	refs/tags/lr1-zdano^{}
```
`git ls-remote --tags origin` питає GitHub, які теги **там**. Є лише `lr1-zdano`: легкий `--follow-tags` не взяв.
Рядок з `^{}` - коміт, на який вказує анотований тег. Легкий відправляємо окремо:

```bash
git push origin lr1-chernetka
```
```text
To /home/evgen/.cache/ugit.qVE6ej/u14/github/Evge14n/pisochnytsia.git
 * [new tag]         lr1-chernetka -> lr1-chernetka
```

**Крок 5. Подивитися на здану версію.**

```bash
git checkout lr1-zdano
git status
```
```text
Note: switching to 'lr1-zdano'.

You are in 'detached HEAD' state. You can look around, make experimental
changes and commit them, and you can discard any commits you make in this
state without impacting any branches by switching back to a branch.

If you want to create a new branch to retain commits you create, you may
do so (now or later) by using -c with the switch command. Example:

  git switch -c <new-branch-name>

Or undo this operation with:

  git switch -

Turn off this advice by setting config variable advice.detachedHead to false

HEAD is now at baa1934 ЛР1: завдання 2
HEAD detached at lr1-zdano
nothing to commit, working tree clean
```
Переклад: «Ти у стані відчепленого HEAD. Можна дивитися і навіть комітити, але ці коміти не належать жодній гілці.
Хочеш їх зберегти - створи гілку `git switch -c назва`. Повернутися - `git switch -`».
Тут можна відкрити файли, запустити doctest - побачиш рівно те, що здавав. Назад на гілку:

```bash
git switch main
```

**Крок 6. Тег на старіший коміт.** Забув поставити тег одразу? Його можна поставити на будь-який коміт:

```bash
git tag -a lr1-start -m "Почав ЛР1" HEAD~1
git tag -l "lr1-z*"
```
`HEAD~1` - коміт перед поточним (можна і хеш з `git log --oneline`). `git tag -l "lr1-z*"` показує лише теги,
що починаються на `lr1-z`, - тут це `lr1-zdano`.

**Крок 7. Видалити тег** у себе і на GitHub:

```bash
git tag -d lr1-chernetka
git push origin --delete lr1-chernetka
```
```text
Deleted tag 'lr1-chernetka' (was baa1934)
To /home/evgen/.cache/ugit.qVE6ej/u14/github/Evge14n/pisochnytsia.git
 - [deleted]         lr1-chernetka
```
Видаляй лише свої чернеткові теги. Тег здачі, який уже бачив викладач, не чіпай (чому - у «Типових помилках»).

**Releases на GitHub (коротко).** На сторінці репо справа є **Releases** → **Draft a new release** → **Choose a tag**
(вибрати `lr1-zdano`) → назва і опис → **Publish release**. Реліз - це тег + сторінка з описом і архівами
`Source code (zip)` / `Source code (tar.gz)`. Для лаб досить тегу, реліз - для програм, які хтось завантажує.

**Для лаб:** після здачі кожної лаби - анотований тег `lr1-zdano` ... `lr7-zdano` і `git push origin lr1-zdano`.
Тоді навіть через пів року `git checkout lr3-zdano` покаже рівно те, що бачив викладач, а `git diff lr3-zdano main`
- що ти міняв після здачі. Як це вбудувати в роботу з лабами - файл «Лаби в git - univer-labs покроково».

### Типові помилки

1. **Тег не зʼявився на GitHub.** Ти зробив `git push`, а він написав `Everything up-to-date`. Звичайний push теги
   не везе. Виправлення: `git push origin lr1-zdano` (будь-який тег) або `git push --follow-tags` (лише анотовані).

2. **`fatal: tag 'lr1-zdano' already exists`** - назва зайнята. Якщо тег ще **не** пушив - `git tag -d lr1-zdano`
   і створи знову. Якщо вже на GitHub і його бачив викладач - не пересувай (його клони мають старий, і ви
   говоритимете про різні версії). Краще новий тег: `lr1-zdano-2` з повідомленням, що змінено.

3. **`git switch` на тег не працює:**
   ```text
   fatal: a branch is expected, got tag 'lr1-zdano'
   hint: If you want to detach HEAD at the commit, try again with the --detach option.
   ```
   `switch` переходить лише на гілки. На тег - `git switch --detach lr1-zdano` або `git checkout lr1-zdano`.

4. **Коміт у detached HEAD «зник».** Ти на тезі зробив коміт і пішов на `main`. git попереджає:
   ```text
   Warning: you are leaving 1 commit behind, not connected to
   any of your branches:

     99d1fc7 Правка на тезі

   If you want to keep it by creating a new branch, this may be a good time
   to do so with:

    git branch <new-branch-name> 99d1fc7
   ```
   Одразу після цього коміт ще можна врятувати гілкою: `HEAD@{1}` - «де HEAD був один крок тому» (reflog, Урок 12).
   ```bash
   git branch lr1-pravka HEAD@{1}
   ```
   Правило: хочеш щось правити у старій версії - спершу `git switch -c нова-гілка`, потім комітить.

5. **`fatal: no tag message?`** - написав `git tag -a lr1-test` без `-m`, git відкрив nano, а ти вийшов, нічого не
   написавши. Тег не створено. Пиши відразу з `-m "повідомлення"`.

### Як роблять профі

- **Версії у форматі `v1.4.2`** (Semantic Versioning): більша цифра - зламана сумісність, середня - нова можливість,
  менша - виправлення. Тег `v1.4.2` = випуск програми. https://semver.org
- **Лише анотовані теги для випусків.** Pro Git: «It's generally recommended that you create annotated tags»,
  легкі - для тимчасових міток. Профі часто ще й **підписують** тег ключем: `git tag -s` (GitHub показує «Verified»).
- **`push.followTags`** - щоб не забувати теги, один раз:
  ```bash
  git config --global push.followTags true
  ```
  Після цього звичайний `git push` сам везе нові анотовані теги (перевірено в 2.43.0).
- **Release з терміналу** через gh (Урок 16): `gh release create lr1-zdano --title "ЛР1" --notes-from-tag --verify-tag`
  - сторінка релізу з повідомленням тегу; `--verify-tag` не дасть створити реліз, якщо тегу ще нема на GitHub.
  ```bash
  gh release create lr1-zdano --title "ЛР1" --notes-from-tag --verify-tag
  ```
- **Захист тегів** у командах: правило (ruleset) на GitHub забороняє видаляти й пересувати теги `v*`
  (docs.github.com, «About rulesets»).

### Самоперевірка

1. Чим тег відрізняється від гілки?
2. Чому для здачі краще анотований тег, а не легкий?
3. Ти зробив `git tag -a lr2-zdano -m "ЛР2 здано"` і `git push`. Викладач не бачить тегу на GitHub. Чому і що зробити?
4. Що означає `detached HEAD` і як повернутися назад?
5. Як подивитися, які теги є на GitHub, не відкриваючи сайт?

<details markdown="1"><summary>Відповіді</summary>

1. Гілка їде вперед з кожним новим комітом, тег назавжди стоїть на одному коміті.
2. Анотований зберігає автора, дату і повідомлення («ЛР2 здано»), це окремий обʼєкт; його бере `git push --follow-tags`.
   Легкий - лише назва, без «хто і коли».
3. Звичайний `git push` теги не пушить. `git push origin lr2-zdano` (або `git push --follow-tags`).
4. HEAD стоїть на коміті, а не на гілці (після `git checkout тег`). Нові коміти тут не належать жодній гілці.
   Назад - `git switch main` (або `git switch -`).
5. `git ls-remote --tags origin`.

</details>

### Джерела

- Pro Git, 2.6 «Git Basics - Tagging»: https://git-scm.com/book/en/v2/Git-Basics-Tagging (відкрито 18.11.2026)
- git-scm.com/docs/git-tag: https://git-scm.com/docs/git-tag (відкрито 18.11.2026)
- git-scm.com/docs/git-push (`--follow-tags`, `--delete`): https://git-scm.com/docs/git-push (відкрито 18.11.2026)
- docs.github.com, «Managing releases in a repository»:
  https://docs.github.com/en/repositories/releasing-projects-on-github/managing-releases-in-a-repository (відкрито 18.11.2026)
- cli.github.com, `gh release create`: https://cli.github.com/manual/gh_release_create (відкрито 18.11.2026)
- docs.github.com, «About rulesets»:
  https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/about-rulesets
  (відкрито 18.11.2026)
- Semantic Versioning 2.0.0: https://semver.org (відкрито 18.11.2026)

## Тема 15. GitHub Pages

**Навіщо:** GitHub може сам показати твій файл `index.html` як сайт за адресою `https://evge14n.github.io/...`.
Так зроблено твій сайт підготовки uni-prep. Сьогодні зробиш свою першу сторінку з фізики - без сервера і без грошей.

### Коротко

**GitHub Pages** - безкоштовний хостинг **статичних** сторінок: GitHub бере HTML, CSS і JavaScript з репозиторію і
показує їх як сайт. «Статичний» - сторінка лежить готовим файлом; Python, PHP на сервері Pages не запускає
(docs: «GitHub Pages does not support server-side languages such as PHP, Ruby, or Python»).

```text
 ноутбук                       GitHub                                   інтернет
 index.html ── git push ──→  репо fizyka-storinka (main)  ── Pages ──→  https://evge14n.github.io/fizyka-storinka/
                              Settings → Pages:                         (бачать УСІ)
                              Deploy from a branch, main, / (root)
```

Аналогія: репо - твій зошит, Pages - стенд у коридорі, куди автоматично вивішується копія сторінки з зошита.
Стенд бачать усі, хто проходить повз.

| Що | Як |
|---|---|
| хто може | на GitHub Free - **лише публічний репо** (docs: «If the account that owns the repository uses GitHub Free ..., the repository must be public») |
| що показується | `index.html` (або `index.md`, `README.md`) у корені вибраної гілки й теки |
| адреса сайту проєкту | `https://evge14n.github.io/НАЗВА-РЕПО/` (логін малими літерами) |
| сайт користувача | окремий репо з назвою `evge14n.github.io` → адреса `https://evge14n.github.io/` |
| скільки чекати | «up to 10 minutes» після push (docs); на практиці частіше близько хвилини |
| де статус | вкладка **Actions** репо → запуск **pages build and deployment** (зелена галочка = готово) |

Тому сайт - **окремий** публічний репо (наприклад `fizyka-storinka`), а лаби лишаються в приватному `univer-labs`.

### Передбач, потім запусти

1. Ти створив `index.html` у клоні і нічого більше не робив. Що покаже `git status --short`?
   <details markdown="1"><summary>Відповідь</summary>

   ```text
   ?? index.html
   ```
   `??` - файл новий, git за ним ще не стежить. Pages бачить лише те, що **запушено** на GitHub.
   </details>

2. Репо створено з README (1 коміт). Ти закомітив `index.html`, запушив, потім закомітив зміну привітання і знову
   запушив. Скільки комітів у `origin/main` і яку версію покаже сайт через кілька хвилин?
   <details markdown="1"><summary>Відповідь</summary>

   Комітів 3 (перевірка: `git rev-list --count origin/main`). Сайт покаже останню запушену версію - з новим привітанням:
   Pages завжди бере те, що зараз лежить у вибраній гілці на GitHub.
   </details>

3. Ти випадково закомітив файл з паролем, а потім зробив `git rm` і ще один коміт. Пароля в репо вже нема?
   <details markdown="1"><summary>Відповідь</summary>

   Є. Його нема в **останньому** коміті, але в історії він лишився: `git show HEAD~1:parol.txt` його покаже.
   У публічному репо історію бачать усі. Тому секрети в репо не кладуть **взагалі** (див. «Типові помилки»).
   </details>

### Руками

Хеші комітів у тебе будуть інші. Рядок `To /home/...` у виводі = у тебе `To github.com:Evge14n/fizyka-storinka.git`.

**Крок 1. Публічний репо на сайті.** Справа вгорі **+** → **New repository** → Repository name: `fizyka-storinka` →
**Public** → **Add README**: On → **Create repository**. (Через gh, Урок 16: `gh repo create fizyka-storinka --public --add-readme`.)

Клонуй і створи сторінку:

```bash
git clone git@github.com:Evge14n/fizyka-storinka.git ~/fizyka-storinka
cd ~/fizyka-storinka
nano index.html
```

Набери в nano (Ctrl+O, Enter - зберегти; Ctrl+X - вийти):

```html
<!doctype html>
<html lang="uk">
<head>
  <meta charset="utf-8">
  <title>Фізика - Імʼя</title>
</head>
<body>
  <h1>Привіт! Це моя сторінка з фізики</h1>
  <p>1 курс, фізичний факультет ЛНУ.</p>
  <p>Тут будуть конспекти й корисні посилання.</p>
</body>
</html>
```

Що тут що: `<h1>` - великий заголовок, `<p>` - абзац, `<title>` - назва вкладки браузера.
`<meta charset="utf-8">` каже браузеру, що текст у UTF-8 - без нього кирилиця може стати «кракозябрами».
Подивитися локально, до GitHub:

```bash
xdg-open index.html
```

**Крок 2. Коміт і push.**

```bash
git add index.html
git commit -m "Перша сторінка"
git push
git ls-files
```
```text
[main 3db7e8b] Перша сторінка
 1 file changed, 12 insertions(+)
 create mode 100644 index.html
To /home/evgen/.cache/ugit.dCx5XY/u15/github/Evge14n/fizyka-storinka.git
   f8c0af1..3db7e8b  main -> main
README.md
index.html
```
`git ls-files` - які файли в репо. `index.html` має бути **в корені** (без теки перед назвою).

**Крок 3. Увімкнути Pages на сайті.** У репо `fizyka-storinka`:

```text
Settings → (ліве меню, розділ «Code, planning, and automation») Pages
  → Build and deployment → Source: Deploy from a branch
  → Branch: main    тека: / (root)    → Save
```
(Назви пунктів - з docs.github.com, «Configuring a publishing source for your GitHub Pages site», відкрито 18.11.2026.)

**Крок 4. Дочекатися і відкрити.** Вкладка **Actions** у репо → там зʼявиться запуск **pages build and deployment**.
Жовтий кружечок - ще йде, зелена галочка - готово, червоний хрестик - помилка (клікни, щоб побачити яку).
Документація: «It can take up to 10 minutes for changes to your site to publish after you push the changes to GitHub».
Для прикладу: у публічного репо mmistakes/minimal-mistakes такі запуски 2026 року тривали близько 50 секунд
(GitHub API, перевірено 18.11.2026). Коли готово - **Settings → Pages → Visit site**, або відкрий адресу:

```text
https://evge14n.github.io/fizyka-storinka/
```

Перевірити з терміналу, чи сайт уже живий (200 - є, 404 - ще нема):

```bash
curl -s -o /dev/null -w '%{http_code}\n' https://evge14n.github.io/fizyka-storinka/
```
Для твого uni-prep 18.11.2026 це дало `200`, а для ще не створеної `fizyka-storinka` - `404`:

```bash
curl -s -o /dev/null -w '%{http_code}\n' https://evge14n.github.io/uni-prep/
```

**Крок 5. Оновити сторінку.** Кожен push у `main` = новий запуск і нова версія сайту.

```bash
sed -i 's/Привіт!/Вітаю!/' index.html
git diff
git commit -am "Змінив привітання"
git push
```
`git diff` покаже:
```text
-  <h1>Привіт! Це моя сторінка з фізики</h1>
+  <h1>Вітаю! Це моя сторінка з фізики</h1>
```
За хвилину онови сторінку в браузері (Ctrl+Shift+R - без старої копії з кешу).

**Крок 6. `.nojekyll` (коротко).** Коли Pages публікує з гілки, він пропускає файли через **Jekyll** - програму,
що збирає сайти. Jekyll **не публікує** файли й теки, назва яких починається з `_`, `.` або `#` (docs, «About GitHub Pages
and Jekyll»). Якщо в тебе тека `_images` чи файл `_dani.json` і на сайті вони «зникли» - поклади в корінь порожній
файл `.nojekyll`, і Jekyll вимкнеться (docs: «disable the Jekyll build process by creating an empty file called `.nojekyll`
in the root of your publishing source»).

```bash
touch .nojekyll
git add .nojekyll
git commit -m "Без Jekyll"
git push
```
`touch` створює порожній файл. Крапка на початку = прихований файл: звичайний `ls` його не покаже, `ls -a` - покаже.

**Приклад - твій uni-prep.** https://evge14n.github.io/uni-prep/ - це репо `Evge14n/uni-prep`, публічне. Він публікується
не «з гілки», а другим пунктом того ж меню - **Source: GitHub Actions**, своїм файлом `.github/workflows/pages.yml`
(видно через GitHub API, 18.11.2026). Для простої сторінки «з гілки» досить, Actions потрібні, коли сайт треба спершу
зібрати програмою.

**Що НЕ класти в репо сайту** (його бачить увесь інтернет, і вся історія комітів теж):
- паролі, токени, ключі (`~/.ssh/id_ed25519` - ніколи), файли `.env`;
- оцінки, бали, списки групи, телефони й пошти одногрупників - це чужі особисті дані;
- розвʼязки лаб, поки їх не здали (одногрупник скопіює - питання будуть до обох).
Docs: «GitHub Pages sites are publicly available on the internet» і «shouldn't be used for sensitive transactions like
sending passwords or credit card numbers».

**Для лаб:** самі лаби - у приватному `univer-labs`, бо Pages на Free працює лише з публічних репо, а розвʼязки
до здачі показувати всім не можна. Pages знадобиться для іншого: сторінка-портфоліо, конспект з графіками, сайт команди
на хакатоні. Навичка та сама - `git add`, `git commit`, `git push`, і через хвилину сайт оновився.

### Типові помилки

1. **Пункту Pages нема або він просить змінити план** - репо приватний. На GitHub Free Pages лише для публічних.
   Зроби окремий публічний репо для сайту (не робити публічним `univer-labs`!).
   Точний текст на сторінці Settings → Pages для приватного репо - (не перевірено).

2. **404 «Site not found · GitHub Pages»** (так називається сторінка-заглушка, перевірено `curl` 18.11.2026). Причини:
   - сайт ще будується - глянь Actions, почекай;
   - Pages не ввімкнено (крок 3) або вибрано не ту гілку чи теку;
   - `index.html` не в корені (`git ls-files` показує `site/index.html`) або названий `Index.html` - на сервері
     великі й малі літери різні;
   - помилка в адресі: потрібна `https://evge14n.github.io/fizyka-storinka/`, а не `github.com/Evge14n/...`.

3. **Сайт не змінився - забув push.** Коміт є лише в тебе. `git status` скаже:
   ```text
   Your branch is ahead of 'origin/main' by 1 commit.
     (use "git push" to publish your local commits)
   ```
   Виправлення: `git push`, потім Actions і оновити сторінку з Ctrl+Shift+R.

4. **Видалив секрет новим комітом - а він лишився.** Перевір на локальній пісочниці (нічого не пушимо):
   ```bash
   git init ~/sekret-demo
   cd ~/sekret-demo
   printf 'пароль=qwerty123\n' > parol.txt
   git add parol.txt
   git commit -m "Додав пароль"
   git rm parol.txt
   git commit -m "Прибрав пароль"
   git show HEAD~1:parol.txt
   ```
   ```text
   пароль=qwerty123
   ```
   Файлу нема в теці, але старий коміт його памʼятає. Якщо справжній пароль чи токен потрапив на GitHub -
   **спершу зміни сам пароль/токен** (вважай його вкраденим), а вже потім думай про чистку історії.

### Як роблять профі

- **Pages через GitHub Actions** замість «з гілки»: сайт збирається програмою (Vite, Hugo, MkDocs) і публікується
  окремим кроком - як твій uni-prep. Docs, «Configuring a publishing source for your GitHub Pages site».
- **Генератори статичних сайтів:** Markdown → гарний сайт. Для документації Python-проєктів часто беруть MkDocs
  (https://www.mkdocs.org), для блогів - Jekyll або Hugo.
- **Свій домен** замість `github.io` (наприклад `evgen.dev`) - Settings → Pages → Custom domain
  (docs, «Configuring a custom domain for your GitHub Pages site»).
- **Секрети ніколи не в коді:** у публічних репо GitHub безкоштовно сам шукає токени й ключі (secret scanning:
  «Public repositories: Secret scanning runs automatically for free»), а push protection «blocks pushes that contain
  secrets» - docs, «About secret scanning» і «About push protection». Але це страховка, а не дозвіл.
- **Ліміти Pages:** сайт до 1 ГБ, мʼякий ліміт 100 ГБ трафіку на місяць і 10 збірок на годину (docs, «GitHub Pages limits»).
  Для сторінки з фізики це дуже багато.

### Самоперевірка

1. Чому сайт на Pages не можна зробити з приватного `univer-labs` на GitHub Free?
2. Де лежить файл, який Pages показує як головну сторінку, якщо вибрано `main` і `/ (root)`?
3. Яка буде адреса сайту з репо `Evge14n/fizyka-storinka`?
4. Ти запушив зміну, а сайт старий. Що перевіриш і в якому порядку?
5. Навіщо порожній файл `.nojekyll`?

<details markdown="1"><summary>Відповіді</summary>

1. На Free Pages працює лише з публічних репо, а лаби до здачі не мають бути публічними. Сайт - окремий публічний репо.
2. `index.html` у корені гілки `main` (`git ls-files` показує просто `index.html`).
3. `https://evge14n.github.io/fizyka-storinka/`.
4. `git status` (чи нема «ahead» - чи справді запушено) → вкладка Actions, запуск «pages build and deployment»
   (жовтий - чекати, червоний - помилка) → оновити сторінку з Ctrl+Shift+R.
5. Вимикає Jekyll: тоді на сайт потрапляють і файли/теки, що починаються з `_` (наприклад `_images`).

</details>

### Джерела

- docs.github.com, «Creating a GitHub Pages site»:
  https://docs.github.com/en/pages/getting-started-with-github-pages/creating-a-github-pages-site (відкрито 18.11.2026)
- docs.github.com, «Configuring a publishing source for your GitHub Pages site»:
  https://docs.github.com/en/pages/getting-started-with-github-pages/configuring-a-publishing-source-for-your-github-pages-site
  (відкрито 18.11.2026)
- docs.github.com, «What is GitHub Pages?»:
  https://docs.github.com/en/pages/getting-started-with-github-pages/about-github-pages (відкрито 18.11.2026)
- docs.github.com, «GitHub Pages limits»:
  https://docs.github.com/en/pages/getting-started-with-github-pages/github-pages-limits (відкрито 18.11.2026)
- docs.github.com, «About GitHub Pages and Jekyll»:
  https://docs.github.com/en/pages/setting-up-a-github-pages-site-with-jekyll/about-github-pages-and-jekyll (відкрито 18.11.2026)
- docs.github.com, «About Jekyll build errors for GitHub Pages sites»:
  https://docs.github.com/en/pages/setting-up-a-github-pages-site-with-jekyll/about-jekyll-build-errors-for-github-pages-sites
  (відкрито 18.11.2026)
- docs.github.com, «Viewing workflow run history»:
  https://docs.github.com/en/actions/how-tos/monitor-workflows/view-workflow-run-history (відкрито 18.11.2026)
- docs.github.com, «About secret scanning»:
  https://docs.github.com/en/code-security/secret-scanning/introduction/about-secret-scanning (відкрито 18.11.2026)
- GitHub REST API, запуски «pages build and deployment» (назва і тривалість):
  https://api.github.com/repos/mmistakes/minimal-mistakes/actions/runs?event=dynamic (відкрито 18.11.2026)

## Тема 16. gh - GitHub з терміналу

**Навіщо:** щоб створити Issue, відкрити Pull Request чи злити його, не треба йти в браузер. Пишеш лабу в терміналі -
там же й `gh pr create`. Для ЛР2 це «закінчив завдання → PR → злив» за три команди.

### Коротко

`git` працює з **репозиторієм** (коміти, гілки, push). `gh` (GitHub CLI) працює з **сайтом GitHub**: Issues, Pull Requests,
налаштування репо, Actions. gh сам дивиться в `git remote` поточної теки і розуміє, з яким репо ти працюєш.

```text
 термінал ── git push / pull ─────→  репозиторій на GitHub (коміти, гілки)
          └─ gh issue / pr / repo ─→  сайт GitHub (Issues, PR, налаштування) - через API
```

Аналогія: git - як носити зошит у деканат і назад; gh - як телефонувати в деканат: «створіть заявку», «закрийте заявку».

| Команда | Що робить |
|---|---|
| `gh auth status` | чи ти увійшов і яким акаунтом |
| `gh repo view` / `gh repo view --web` | опис і README поточного репо / те саме в браузері |
| `gh repo clone Evge14n/НАЗВА` | клонувати (коротше за `git clone git@github.com:...`) |
| `gh repo create НАЗВА --private` | створити репо (`--public`, `--add-readme`, `--clone`, `--source=. --push`) |
| `gh issue create` / `list` / `view 1` / `close 1` | Issues: створити, список, подивитися №1, закрити №1 |
| `gh pr create --fill` | PR з поточної гілки, назва й опис - з комітів |
| `gh pr list` / `view 1` / `diff 1` | список PR, PR №1, його зміни |
| `gh pr checkout 1` | забрати гілку PR №1 до себе (щоб перевірити) |
| `gh pr merge 1 --squash --delete-branch` | злити PR №1 одним комітом і видалити гілку тут і на GitHub |
| `gh browse` | відкрити репо в браузері (`gh browse lr2_1.py` - конкретний файл) |
| `gh help`, `gh pr merge --help` | довідка (англійською, з прикладами) |

**Чому gh з офіційного репо GitHub, а не з Менеджера програм Mint.** У репозиторії Mint/Ubuntu лежить gh 2.45.0, і він
зламаний: GitHub прибрав старий API, і `gh pr view` падає з помилкою «GraphQL: Projects (classic) is being deprecated ...»
(перевірено 18.11.2026). Документація cli/cli прямо радить офіційні пакети, бо «the community-distributed 2.45.x / 2.46.x
version is broken». Встановлення - Урок 02, вхід - Урок 03 (`gh auth login`).

### Передбач, потім запусти

1. На свіжому ноутбуці, де ще не було `gh auth login`, запускаєш `gh auth status`. Що буде?
   <details markdown="1"><summary>Відповідь</summary>

   ```text
   You are not logged into any GitHub hosts. To log in, run: gh auth login
   ```
   Код виходу 1. gh без входу не має доступу до твоїх репо (вхід - Урок 03).
   </details>

2. Ти в домашній теці `~` (не в репо) і пишеш `gh issue list`. Звідки gh дізнається, чиї Issues показати?
   <details markdown="1"><summary>Відповідь</summary>

   Нізвідки - він бере репо з `git remote` поточної теки, а тут репо нема:
   ```text
   failed to run git: fatal: not a git repository (or any of the parent directories): .git
   ```
   Або зайди в теку репо, або вкажи репо явно: `gh issue list -R Evge14n/pisochnytsia`.
   </details>

3. Друг запускає `gh pr checkout 1`. Що саме зміниться в його git-репо?
   <details markdown="1"><summary>Відповідь</summary>

   gh скачає гілку PR (`lr2-zavd1`) і перемкне на неї - так само, як `git fetch origin` і `git switch lr2-zavd1`.
   У `git branch` зʼявиться нова гілка `lr2-zavd1`, яка стежить за `origin/lr2-zavd1`.
   </details>

4. Ти злив PR кнопкою **Squash and merge** на сайті, потім `git switch main`, `git pull`, `git fetch --prune`.
   Що скаже `git branch -d lr2-zavd1`?
   <details markdown="1"><summary>Відповідь</summary>

   ```text
   error: the branch 'lr2-zavd1' is not fully merged.
   If you are sure you want to delete it, run 'git branch -D lr2-zavd1'
   ```
   Squash робить на `main` **новий** коміт з усіх змін гілки, тож git не бачить у `main` самих комітів гілки.
   Зміни там є - можна сміливо `git branch -D lr2-zavd1`. (`gh pr merge --delete-branch` прибирає гілку сам.)
   </details>

### Руками

Працюємо в пісочниці `~/pisochnytsia` на **справжньому** GitHub (gh не можна «підмінити» локально), тож тут - твій
репо `Evge14n/pisochnytsia` з Уроку 03. Номери Issue і PR у тебе можуть бути інші (якщо вже робив їх в Уроках 10-11) -
тоді пиши свої номери замість `1`.

**Крок 0. Версія і вхід.**

```bash
gh version
gh auth status
```
```text
gh version 2.105.0 (2026-11-17)
https://github.com/cli/cli/releases/tag/v2.105.0
```
`gh version` - те саме, що `gh --version`. Версія має бути новіша за 2.46 (у тебе може бути ще новіша). `gh auth status` після входу виводить блок `github.com`
з рядком `✓ Logged in to github.com account Evge14n (...)` і далі `- Active account: true`,
`- Git operations protocol: ssh` - це формат з коду gh (`pkg/cmd/auth/status/status.go`), сам вивід на твоєму
ноутбуці не перевірено.

**Крок 1. Репо.**

```bash
cd ~/pisochnytsia
gh repo view
gh repo view --web
gh browse
```
`gh repo view` друкує назву, опис і README. `--web` і `gh browse` відкривають сторінку репо в браузері.
Ще корисне: `gh repo list --limit 5` - пʼять твоїх останніх репо.

```bash
gh repo list --limit 5
```

**Крок 2. Issue - «завдання собі».**

```bash
gh issue create --title "ЛР2: перевірити завдання 3" --body "doctest падає на відʼємних числах"
gh issue list
gh issue view 1
gh issue close 1 --comment "Виправлено"
gh issue list --state closed
```
`issue create` друкує посилання на нову Issue. `--state closed` - показати закриті (без нього - лише відкриті).

**Крок 3. Pull Request з терміналу.** Гілка і коміт - звичайним git (Уроки 07, 09):

```bash
git switch -c lr2-zavd1
printf 'def square(number: int) -> int:\n    """\n    >>> square(3)\n    9\n    """\n    return number * number\n' > lr2_1.py
python3 -m doctest lr2_1.py
git add lr2_1.py
git commit -m "ЛР2: завдання 1"
git push -u origin lr2-zavd1
```
`python3 -m doctest` нічого не друкує - отже всі тести пройшли. Кінець виводу `git push -u`:
```text
 * [new branch]      lr2-zavd1 -> lr2-zavd1
branch 'lr2-zavd1' set up to track 'origin/lr2-zavd1'.
```
Тепер PR:

```bash
gh pr create --fill --base main
gh pr list
gh pr view 1
gh pr diff 1
```
`--fill` бере назву й опис з комітів (тут - «ЛР2: завдання 1»), `--base main` - куди зливати. Без `--fill` gh спитає
назву й опис сам. Якщо в описі написати `Closes #1`, Issue №1 закриється, коли PR зіллють (так пише `gh pr create --help`).

**Крок 4. «Друг» перевіряє PR** у своєму клоні `~/druhyi-klon` (Урок 09; якщо його нема -
`gh repo clone Evge14n/pisochnytsia ~/druhyi-klon`):

```bash
cd ~/druhyi-klon
gh pr checkout 1
python3 -m doctest lr2_1.py
git switch main
cd ~/pisochnytsia
```
Що `gh pr checkout 1` робить усередині: якби gh не було, **замість** нього (не після) можна руками:

```bash
git fetch origin
git switch lr2-zavd1
```
```text
Switched to a new branch 'lr2-zavd1'
branch 'lr2-zavd1' set up to track 'origin/lr2-zavd1'.
```

**Крок 5. Злити PR** (ти в `~/pisochnytsia`, на гілці `lr2-zavd1`):

```bash
gh pr merge 1 --squash --delete-branch
git log --oneline -n 3
```
`--squash` - усі коміти PR стають **одним** комітом на `main` (Урок 11, види merge). `--delete-branch` - видалити гілку
і на GitHub, і в тебе. Якщо ти стояв на цій гілці, gh перемкне тебе на `main` і зробить `git pull`
(так написано в коді gh 2.105, `pkg/cmd/pr/merge/merge.go`). У виводі будуть рядки за шаблоном
`✓ Squashed and merged pull request Evge14n/pisochnytsia#1 (...)`, `✓ Deleted local branch lr2-zavd1 and switched to branch main`,
`✓ Deleted remote branch lr2-zavd1` (шаблон з коду, на справжньому GitHub у цьому курсі не запускали).
`git log --oneline -n 3` покаже на `main` новий коміт з назвою PR.

**Довідка, коли забув прапорець:**

```bash
gh help
gh pr merge --help
```
Повна довідка онлайн: https://cli.github.com/manual

**Для лаб:** у `univer-labs` кожна лаба - гілка `lr2`, і коли завдання пройшли doctest:
`git push -u origin lr2` → `gh pr create --fill --base main` → `gh pr merge --squash --delete-branch` (або звичайний
merge, якщо хочеш бачити кожен коміт-завдання в історії `main`). Покроково - «Лаби в git - univer-labs покроково».

### Типові помилки

1. **Не увійшов.** `gh auth status` → `You are not logged into any GitHub hosts. To log in, run: gh auth login` (код 1),
   а будь-яка робоча команда, наприклад `gh issue list`:
   ```text
   To get started with GitHub CLI, please run:  gh auth login
   Alternatively, populate the GH_TOKEN environment variable with a GitHub API authentication token.
   ```
   Код виходу 4. Виправлення: `gh auth login` (Урок 03).

2. **Не в теці репо.** `failed to run git: fatal: not a git repository (or any of the parent directories): .git`.
   Зайди в репо (`cd ~/pisochnytsia`) або вкажи репо прапорцем:
   ```bash
   gh issue list -R Evge14n/pisochnytsia
   ```

3. **Старий gh з репо Mint.** `gh pr view` падає з `GraphQL: Projects (classic) is being deprecated ...`, а
   `gh --version` показує 2.45.0. Видали його і постав з офіційного репо (Урок 02).

4. **Злив на сайті кнопкою Squash and merge - `git branch -d` не видаляє.** Після `git fetch --prune`:
   ```text
   error: the branch 'lr2-zavd1' is not fully merged.
   If you are sure you want to delete it, run 'git branch -D lr2-zavd1'
   ```
   Переконайся, що PR справді злито (на сторінці PR фіолетова позначка Merged, або `gh pr view 1`), і видали з `-D`:
   ```bash
   git branch -D lr2-zavd1
   ```
   Незвичне (git 2.43): якщо `git fetch --prune` ще **не** робив і `origin/lr2-zavd1` у тебе лишився, `git branch -d`
   видаляє гілку з попередженням `warning: deleting branch 'lr2-zavd1' that has been merged to 'refs/remotes/origin/lr2-zavd1',
   but not yet merged to HEAD` - бо порівнює з тією віддаленою гілкою, а не з `main`.

### Як роблять профі

- **PR з Issue одним рухом:** `gh pr create --fill` + у тексті `Closes #12` - після злиття Issue закриється сама.
- **Рев'ю з терміналу:** `gh pr checkout 7` → запустити тести → `gh pr review 7 --approve` або
  `gh pr review 7 --request-changes --body "..."` (cli.github.com/manual/gh_pr_review).
- **Стежити за Actions** (той самий «pages build and deployment» з Уроку 15) без браузера:
  ```bash
  gh run list --limit 3
  ```
- **Опублікувати локальний репо одним рядком:** `gh repo create univer-labs --private --source=. --remote=origin --push`
  (створює репо на GitHub, додає `origin` і пушить; файл «Лаби в git»).
- **`gh api`** - будь-який запит до GitHub API для скриптів, напр. `gh api repos/Evge14n/uni-prep` (cli.github.com/manual/gh_api).

### Самоперевірка

1. Чим відрізняється робота `git` і `gh`?
2. Звідки `gh pr list` знає, з яким репо працювати, і як вказати інше?
3. Якою командою створити PR з поточної гілки в `main`, взявши назву з комітів?
4. Що роблять прапорці `--squash` і `--delete-branch` у `gh pr merge`?
5. Чому gh ставлять з офіційного репо GitHub, а не з Менеджера програм Mint?

<details markdown="1"><summary>Відповіді</summary>

1. `git` - коміти, гілки, push/pull з репозиторієм. `gh` - сайт GitHub: Issues, PR, налаштування, Actions (через API).
2. З `git remote` поточної теки. Інше репо - `-R Evge14n/НАЗВА`.
3. `gh pr create --fill --base main`.
4. `--squash` - усі коміти PR одним комітом на `main`; `--delete-branch` - видалити гілку на GitHub і локально
   (і перемкнути тебе на `main`).
5. У репо Mint gh 2.45.0, він зламаний (GitHub прибрав старий API). Офіційний пакет новий і оновлюється разом із системою.

</details>

### Джерела

- GitHub CLI manual: https://cli.github.com/manual (відкрито 18.11.2026); сторінки gh_pr_create, gh_pr_merge,
  gh_pr_checkout, gh_pr_review, gh_issue_create, gh_repo_create, gh_browse, gh_api
- Встановлення gh на Linux, cli/cli `docs/install_linux.md`: https://github.com/cli/cli/blob/trunk/docs/install_linux.md
  (відкрито 18.11.2026)
- Код gh: формат `gh auth status` - https://github.com/cli/cli/blob/trunk/pkg/cmd/auth/status/status.go,
  повідомлення `gh pr merge` - https://github.com/cli/cli/blob/trunk/pkg/cmd/pr/merge/merge.go (відкрито 18.11.2026)
- docs.github.com, «About GitHub CLI»: https://docs.github.com/en/github-cli/github-cli/about-github-cli (відкрито 18.11.2026)
- Pro Git, 6.2 «Contributing to a Project» (про PR на GitHub): https://git-scm.com/book/en/v2/GitHub-Contributing-to-a-Project
  (відкрито 18.11.2026)

## Тема 17. Для профі - rebase, cherry-pick, bisect, worktree, Actions

**Навіщо:** у ЛР6 ти зробив гілку, а `main` тим часом пішов уперед; накомітив п'ять «wip»; doctest учора проходив, а сьогодні падає, і незрозуміло, який коміт зламав. Для таких випадків у git є інструменти, які в командах вважаються звичними: rebase, cherry-pick, bisect, worktree, а на GitHub - автоматичні тести (Actions). Цей урок - поверх уроків 01-16, нічого з них не повторює.

### Коротко

| Команда | Що робить | Коли |
|---|---|---|
| `git rebase main` | переносить коміти твоєї гілки так, ніби ти почав її від свіжого `main` | своя гілка, ще не опублікована |
| `git rebase --continue` / `--abort` | далі після розвʼязаного конфлікту / скасувати весь rebase | під час rebase |
| `git rebase -i HEAD~3` | редагувати останні 3 коміти: злити, перейменувати, викинути | «wip»-коміти до push |
| `git cherry-pick гілка` | скопіювати ОДИН коміт (останній на гілці) у поточну гілку | потрібна одна правка, а не вся гілка |
| `git bisect start` / `bad` / `good` / `run` / `reset` | двійковий пошук коміту, що зламав код | «вчора працювало» |
| `git worktree add тека -b гілка` | друга гілка в іншій теці одночасно | терміново правиш одне, не кидаючи інше |
| `git log -S "текст"` | коміти, що додали або прибрали цей текст | «хто прибрав цю перевірку?» |
| `git grep -n "текст"` | пошук у файлах репо (лише ті, що в git) | де ця функція? |
| `git blame -L 1,6 файл` | хто і в якому коміті востаннє міняв кожен рядок | звідки цей рядок? |

**Rebase** - «перенести основу». Merge (урок 07) зводить дві гілки новим комітом з двома батьками. Rebase натомість **переписує** твої коміти заново поверх `main`: зміни ті самі, а коміти нові (інші хеші). Історія виходить прямою лінією:

```text
до:                          merge:                       rebase:
A ← B ← D     (main)         A ← B ← D ← M   (main)       A ← B ← D ← C'   (lr6)
     \                            \     /                          ↑
      C       (lr6)                C ──                           main
                                                         C' - копія C з новим хешем
```

**Золоте правило rebase** (Pro Git 3.6): «Do not rebase commits that exist outside your repository and that people may have based work on» - не перебазовуй коміти, які вже є поза твоїм компʼютером (запушені) і на які хтось міг спертися. Rebase робить нові коміти замість старих; якщо старі вже на GitHub, твоя історія і GitHub розійдуться (див. «Типові помилки», 3).

Аналогія: merge - дописати в зошит «а тут я звів дві чернетки». Rebase - переписати чернетку начисто так, ніби ти почав її вже після нового параграфа. Переписувати можна лише свою чернетку, а не ту, яку вже здав.

### Пісочниця

Окрема тека, щоб нічого не зачепити. `.gitignore` з `__pycache__/` - бо `python3 -m doctest` створює цю теку (урок 06).

```bash
mkdir ~/git-pisochnytsia-17
cd ~/git-pisochnytsia-17
git init
printf '__pycache__/\n' > .gitignore
printf 'def kvadrat(x):\n    """\n    >>> kvadrat(3)\n    9\n    """\n    return x * x\n' > lab.py
git add .gitignore lab.py
git commit -m "ЛР6: функція kvadrat"
python3 -m doctest lab.py && echo "тести ok"
```
```text
Initialized empty Git repository in /home/.../git-pisochnytsia-17/.git/
[main (root-commit) c387d25] ЛР6: функція kvadrat
 2 files changed, 7 insertions(+)
 create mode 100644 .gitignore
 create mode 100644 lab.py
тести ok
```
`python3 -m doctest lab.py` мовчить, якщо всі тести пройшли, тому `&& echo` - щоб побачити «тести ok». Хеші в тебе будуть інші.

### Передбач, потім запусти

1. Гілка `lr6-perymetr` відійшла від першого коміту, а в `main` потім зʼявився коміт «Додай README». Після `git rebase main` (крок 1): чи буде на `git log --oneline --graph --all` розгалуження? Чи лишиться хеш коміту «ЛР6: периметр» тим самим?
<details markdown="1"><summary>Відповідь</summary>

Розгалуження не буде - пряма лінія. Хеш **зміниться** (у перевірці було `6d3c8fd` → `2c7a26c`): rebase робить новий коміт з тими самими змінами, але з іншим батьком. Тому і золоте правило.
</details>

2. На гілці `eksperyment` два коміти: «Спроба: інший kvadrat» (переписує `lab.py`) і над ним «Додай тест kub(-1)». На `main` ти робиш `git cherry-pick eksperyment` (крок 4). Чи зміниться `lab.py` у `main`?
<details markdown="1"><summary>Відповідь</summary>

Ні. Назва гілки в cherry-pick означає **лише її останній коміт**. У `main` приїде тільки «Додай тест kub(-1)» (новий коміт з новим хешем), а «Спроба» лишиться на `eksperyment`. `python3 -m doctest lab.py kub.py` → `тести ok`.
</details>

3. Між добрим і поганим комітом 7 комітів. Скільки разів доведеться запускати тест, щоб `git bisect` знайшов винний (крок 5)?
<details markdown="1"><summary>Відповідь</summary>

Близько 3: щоразу git ділить відрізок навпіл (7 → 3 → 1 → 0). Після `git bisect good HEAD~7` він сам пише `Bisecting: 3 revisions left to test after this (roughly 2 steps)` - «ще приблизно 2 кроки» після цього. Для 1000 комітів було б лише близько 10 запусків.
</details>

4. Коміт «Крок 4» замінив `x * x` на `x * 2`, потім ти це виправив назад. Скільки комітів покаже `git log -S "x * 2" --oneline` (крок 6)?
<details markdown="1"><summary>Відповідь</summary>

Два: той, що **додав** `x * 2`, і той, що його **прибрав**. `-S` шукає коміти, де кількість входжень тексту змінилась.
```text
fd85200 (HEAD -> main) Виправ kvadrat: x * x
25e9cd6 Крок 4: дрібна правка
```
</details>

### Руками

**Крок 1. `rebase` - підтягнути свою гілку до свіжого `main`.**

```bash
git switch -c lr6-perymetr
printf 'def perymetr(a, b):\n    return 2 * (a + b)\n' > perymetr.py
git add perymetr.py
git commit -m "ЛР6: периметр"
git switch main
printf '# ЛР6\n' > README.md
git add README.md
git commit -m "Додай README"
git log --oneline --graph --all
```
```text
* 6d3c8fd (lr6-perymetr) ЛР6: периметр
| * efdf84a (HEAD -> main) Додай README
|/
* c387d25 ЛР6: функція kvadrat
```
Гілки розійшлись. (Яка з двох гілок намальована вище - залежить від часу комітів; у тебе може бути навпаки.) Тепер на своїй гілці - rebase на `main`:

```bash
git switch lr6-perymetr
git rebase main
git log --oneline --graph --all
```
```text
Successfully rebased and updated refs/heads/lr6-perymetr.
* 2c7a26c (HEAD -> lr6-perymetr) ЛР6: периметр
* efdf84a (main) Додай README
* c387d25 ЛР6: функція kvadrat
```
Пряма лінія, а коміт «ЛР6: периметр» тепер `2c7a26c` (був `6d3c8fd`). Злиття стає простим перемотуванням:

```bash
git switch main
git merge lr6-perymetr
git branch -d lr6-perymetr
```
```text
Updating efdf84a..2c7a26c
Fast-forward
 perymetr.py | 2 ++
 1 file changed, 2 insertions(+)
 create mode 100644 perymetr.py
Deleted branch lr6-perymetr (was 2c7a26c).
```

**Крок 2. Конфлікт під час rebase: `--abort` і `--continue`.** Обидві гілки міняють перший рядок README.

```bash
git switch -c lr6-readme
printf '# ЛР6 - квадрат і периметр\n' > README.md
git commit -am "README: що в ЛР6"
git switch main
printf '# Лабораторна 6\n' > README.md
git commit -am "README: повна назва"
git switch lr6-readme
git rebase main
```
```text
Auto-merging README.md
CONFLICT (content): Merge conflict in README.md
error: could not apply 81c95ee... README: що в ЛР6
hint: Resolve all conflicts manually, mark them as resolved with
hint: "git add/rm <conflicted_files>", then run "git rebase --continue".
hint: You can instead skip this commit: run "git rebase --skip".
hint: To abort and get back to the state before "git rebase", run "git rebase --abort".
Could not apply 81c95ee... README: що в ЛР6
```
Маркери ті самі, що в уроці 08. Увага: під час rebase **`HEAD` - це `main`** (на нього переносимо), а твій коміт - нижня частина:

```bash
cat README.md
```
```text
<<<<<<< HEAD
# Лабораторна 6
=======
# ЛР6 - квадрат і периметр
>>>>>>> 81c95ee (README: що в ЛР6)
```
Злякався - `--abort` повертає все, як було до rebase:

```bash
git rebase --abort
git log --oneline -1
```
```text
81c95ee (HEAD -> lr6-readme) README: що в ЛР6
```
Тепер по-справжньому: rebase, прибрати маркери в nano (лишити один рядок `# Лабораторна 6 - квадрат і периметр`), `add`, `--continue`.

```bash
git rebase main
nano README.md
```
Або замість nano одним рядком:
```bash
printf '# Лабораторна 6 - квадрат і периметр\n' > README.md
git add README.md
git rebase --continue
```
`--continue` відкриє nano з повідомленням коміту - не міняй, Ctrl+O, Enter, Ctrl+X.
```text
[detached HEAD 6b9e8d1] README: що в ЛР6
 1 file changed, 1 insertion(+), 1 deletion(-)
Successfully rebased and updated refs/heads/lr6-readme.
```
`detached HEAD` посеред rebase - нормально: git будує нові коміти «без гілки», а в кінці пересуває на них `lr6-readme`. Далі як у кроці 1:

```bash
git switch main
git merge lr6-readme
git branch -d lr6-readme
```

**Крок 3. Злити «wip»-коміти в один до push.** «wip» (work in progress) - «ще в роботі». Таких комітів не соромно робити, але перед push їх краще звести в один зрозумілий.

```bash
git switch -c lr6-kub
printf 'def kub(x):\n    return x ** 3\n' > kub.py
git add kub.py
git commit -m "wip"
printf '\nprint(kub(2))\n' >> kub.py
git commit -am "wip 2"
printf 'def kub(x):\n    """\n    >>> kub(2)\n    8\n    """\n    return x ** 3\n' > kub.py
git commit -am "wip 3"
git log --oneline -4
```
```text
59b1785 (HEAD -> lr6-kub) wip 3
ed5d80b wip 2
6ef0101 wip
6b9e8d1 (main) README: що в ЛР6
```
Далі **один** з двох способів.

*Спосіб А - інтерактивний rebase* (`-i`). Він відкриває nano зі списком комітів (старіший зверху):

```bash
git rebase -i HEAD~3
```
```text
pick 6ef0101 wip
pick ed5d80b wip 2
pick 59b1785 wip 3

# Rebase 6b9e8d1..59b1785 onto 6b9e8d1 (3 commands)
#
# Commands:
# p, pick <commit> = use commit
# r, reword <commit> = use commit, but edit the commit message
# e, edit <commit> = use commit, but stop for amending
# s, squash <commit> = use commit, but meld into previous commit
# f, fixup [-C | -c] <commit> = like "squash" but keep only the previous
...
# d, drop <commit> = remove commit
...
```
Заміни `pick` на `squash` у 2-му і 3-му рядках (перший лишається `pick`), Ctrl+O, Enter, Ctrl+X:
```text
pick 6ef0101 wip
squash ed5d80b wip 2
squash 59b1785 wip 3
```
Одразу відкриється друге вікно nano - повідомлення для злитого коміту:
```text
# This is a combination of 3 commits.
# This is the 1st commit message:

wip

# This is the commit message #2:

wip 2

# This is the commit message #3:

wip 3
...
```
Зітри все і напиши один рядок `ЛР6: функція kub з doctest`, збережи. Рядки з `#` git і так викине.

*Спосіб Б - без редактора* (ти вже знаєш `reset --soft` з уроку 12): прибрати 3 коміти, лишивши зміни в індексі, і закомітити заново.

```bash
git reset --soft HEAD~3
git commit -m "ЛР6: функція kub з doctest"
```
Після будь-якого способу:
```bash
git log --oneline -3
```
```text
a7feeab (HEAD -> lr6-kub) ЛР6: функція kub з doctest
6b9e8d1 (main) README: що в ЛР6
450efd4 README: повна назва
```
І злий у `main`:
```bash
git switch main
git merge lr6-kub
git branch -d lr6-kub
```
Обидва способи переписують коміти - тому **лише до push** (золоте правило).

**Крок 4. `cherry-pick` - забрати один коміт з іншої гілки.**

```bash
git switch -c eksperyment
printf 'def kvadrat(x):\n    return x ** 2\n' > lab.py
git commit -am "Спроба: інший kvadrat"
printf 'def kub(x):\n    """\n    >>> kub(2)\n    8\n    >>> kub(-1)\n    -1\n    """\n    return x ** 3\n' > kub.py
git commit -am "Додай тест kub(-1)"
git switch main
git cherry-pick eksperyment
git log --oneline --graph --all
python3 -m doctest lab.py kub.py && echo "тести ok"
```
```text
[main acdf84c] Додай тест kub(-1)
 Date: Wed Nov 18 10:54:36 2026 +0000
 1 file changed, 2 insertions(+)
* acdf84c (HEAD -> main) Додай тест kub(-1)
| * 61c1e31 (eksperyment) Додай тест kub(-1)
| * a8caffc Спроба: інший kvadrat
|/
* a7feeab ЛР6: функція kub з doctest
...
тести ok
```
(Гілки на малюнку можуть стояти в іншому порядку.) Два коміти з однаковою назвою, але різними хешами: `61c1e31` на `eksperyment` і його копія `acdf84c` у `main`. Рядок `Date:` - git каже, що дата автора взята з оригіналу. Будь-який інший коміт береш за хешем з `git log --oneline eksperyment`: `git cherry-pick a8caffc` (у тебе свій хеш) або `git cherry-pick eksperyment~1` (передостанній на гілці).

**Крок 5. `bisect` - знайти коміт, що зламав doctest.** Спершу зробимо історію, де один коміт непомітно ламає `kvadrat`:

```bash
for i in 1 2 3; do echo "# крок $i" >> lab.py; git commit -qam "Крок $i"; done
sed -i 's/x \* x/x * 2/' lab.py
git commit -qam "Крок 4: дрібна правка"
for i in 5 6 7; do echo "# крок $i" >> lab.py; git commit -qam "Крок $i"; done
python3 -m doctest lab.py
echo $?
```
```text
**********************************************************************
File "/home/.../git-pisochnytsia-17/lab.py", line 3, in lab.kvadrat
Failed example:
    kvadrat(3)
Expected:
    9
Got:
    6
**********************************************************************
1 items had failures:
   1 of   1 in lab.kvadrat
***Test Failed*** 1 failures.
1
```
`echo $?` - код виходу попередньої команди: `0` - тести пройшли, `1` - впали. Саме за цим кодом `git bisect run` вирішуватиме, добрий коміт чи ні.

```bash
git log --oneline -8
git bisect start
git bisect bad
git bisect good HEAD~7
```
```text
8961e76 (HEAD -> main) Крок 7
bf1cd7b Крок 6
efd4afc Крок 5
25e9cd6 Крок 4: дрібна правка
9bd19a1 Крок 3
3278550 Крок 2
3caf692 Крок 1
acdf84c Додай тест kub(-1)
status: waiting for both good and bad commits
status: waiting for good commit(s), bad commit known
Bisecting: 3 revisions left to test after this (roughly 2 steps)
[9bd19a18362dc2d426bee1e19dd53839d5571ab4] Крок 3
```
`bad` без хешу - «поточний коміт поганий». `good HEAD~7` - «7 комітів тому (`acdf84c`) ще працювало». Git сам перейшов на середину - «Крок 3». Перевір його вручну:

```bash
python3 -m doctest lab.py
git bisect good
```
```text
Bisecting: 1 revision left to test after this (roughly 1 step)
[efd4afc8b8c6f69ff9c126c1efb1e318aafc3fa5] Крок 5
```
Тести мовчки пройшли - тому `good` (якби впали - `git bisect bad`). Решту хай git зробить сам: `run` запускає команду на кожному кроці і дивиться на код виходу.

```bash
git bisect run python3 -m doctest lab.py
```
```text
running 'python3' '-m' 'doctest' 'lab.py'
...
***Test Failed*** 1 failures.
Bisecting: 0 revisions left to test after this (roughly 0 steps)
[25e9cd6b9bbd8f78671520491da02a405515f785] Крок 4: дрібна правка
running 'python3' '-m' 'doctest' 'lab.py'
...
25e9cd6b9bbd8f78671520491da02a405515f785 is the first bad commit
commit 25e9cd6b9bbd8f78671520491da02a405515f785
Author: Твоє Імʼя <128326252+Evge14n@users.noreply.github.com>
Date:   Wed Nov 18 10:54:39 2026 +0000

    Крок 4: дрібна правка

 lab.py | 2 +-
 1 file changed, 1 insertion(+), 1 deletion(-)
bisect found first bad commit
```
Знайшов: «Крок 4». Правило `run` (документація git bisect): код **0** - коміт добрий, **1-127** (крім 125) - поганий, **125** - «цей коміт не можна перевірити, пропусти». doctest виходить з 0 або 1 - якраз те, що треба.

Обовʼязково поверни все як було і виправ:
```bash
git bisect reset
sed -i 's/x \* 2/x * x/' lab.py
git commit -am "Виправ kvadrat: x * x"
```
```text
Previous HEAD position was 25e9cd6 Крок 4: дрібна правка
Switched to branch 'main'
[main fd85200] Виправ kvadrat: x * x
 1 file changed, 1 insertion(+), 1 deletion(-)
```

**Крок 6. Хто і коли змінив рядок: `log -S`, `grep`, `blame`.**

```bash
git log -S "x * 2" --oneline
git grep -n "def "
git blame -L 1,6 lab.py
```
```text
fd85200 (HEAD -> main) Виправ kvadrat: x * x
25e9cd6 Крок 4: дрібна правка
```
```text
kub.py:1:def kub(x):
lab.py:1:def kvadrat(x):
perymetr.py:1:def perymetr(a, b):
```
```text
^c387d25 (Твоє Імʼя 2026-11-18 10:54:28 +0000 1) def kvadrat(x):
^c387d25 (Твоє Імʼя 2026-11-18 10:54:28 +0000 2)     """
^c387d25 (Твоє Імʼя 2026-11-18 10:54:28 +0000 3)     >>> kvadrat(3)
^c387d25 (Твоє Імʼя 2026-11-18 10:54:28 +0000 4)     9
^c387d25 (Твоє Імʼя 2026-11-18 10:54:28 +0000 5)     """
fd852009 (Твоє Імʼя 2026-11-18 10:54:42 +0000 6)     return x * x
```
- `log -S "текст"` - коміти, де цей текст зʼявився або зник. Найкращий спосіб знайти «коли прибрали перевірку вводу».
- `git grep -n` - як звичайний `grep -rn`, але лише по файлах git (без `.venv`, `__pycache__`). `-n` - номер рядка.
- `blame -L 1,6` - лише рядки 1-6. `^` перед хешем - перший коміт файлу (далі назад історії нема). Хеш у рядку 6 має 8 знаків, а не 7 - git просто вирівнює стовпчик під `^`.

**Крок 7. `worktree` - друга гілка в іншій теці.** Ти посеред роботи в `main`, а треба почати ЛР7, не чіпаючи файлів тут. Замість `stash` і `switch` - друга тека з тим самим репо:

```bash
git worktree add ~/git-pisochnytsia-17-lr7 -b lr7
git worktree list
```
```text
Preparing worktree (new branch 'lr7')
HEAD is now at fd85200 Виправ kvadrat: x * x
/home/.../git-pisochnytsia-17      fd85200 [main]
/home/.../git-pisochnytsia-17-lr7  fd85200 [lr7]
```
У новій теці - гілка `lr7`. Комітиш там, як звичайно:

```bash
cd ~/git-pisochnytsia-17-lr7
printf 'print("ЛР7")\n' > lr7.py
git add lr7.py
git commit -m "ЛР7: початок"
cd ~/git-pisochnytsia-17
git log --oneline -1 lr7
git branch
```
```text
[lr7 a95b3b5] ЛР7: початок
 1 file changed, 1 insertion(+)
 create mode 100644 lr7.py
a95b3b5 (lr7) ЛР7: початок
  eksperyment
+ lr7
* main
```
Коміт з другої теки одразу видно з першої: репозиторій один, тек дві. `+` у `git branch` - «ця гілка відкрита в іншому worktree». Коли закінчив (і все закомітив):

```bash
git worktree remove ~/git-pisochnytsia-17-lr7
```
Теку прибрано, гілка `lr7` з комітом лишилась.

**Крок 8. GitHub Actions - тести самі запускаються на кожен push.** **CI** (continuous integration, «безперервна інтеграція») - сервер сам бере твій код після кожного push і запускає тести. Зламав - на GitHub червоний хрестик біля коміту. **Workflow** - файл-рецепт у теці `.github/workflows/` (документація: «You must store workflow files in the `.github/workflows` directory»). Робимо в пісочниці з GitHub (урок 03):

```bash
cd ~/pisochnytsia
git switch main
git pull
cp ~/git-pisochnytsia-17/lab.py ~/git-pisochnytsia-17/kub.py .
mkdir -p .github/workflows
nano .github/workflows/test.yml
```
Вміст (відступи - пробілами, не Tab: у YAML це важливо):
```yaml
name: Тести

on: [push]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v6
      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.12'
      - name: Doctest
        run: python -m doctest -v lab.py kub.py
```
Що тут що (ключі - з прикладу docs.github.com «Building and testing Python»):
- `name` - назва, яку видно у вкладці Actions;
- `on: [push]` - запускати на кожен push;
- `jobs` → `test` - одна робота з назвою `test`; `runs-on: ubuntu-latest` - на чистій віртуальній Ubuntu від GitHub;
- `steps` - кроки по черзі: `actions/checkout` бере код з репо, `actions/setup-python` ставить Python 3.12, `run` - звичайна команда терміналу. Якщо вона повертає не 0 (doctest впав) - робота червона.

```bash
git add lab.py kub.py .github/workflows/test.yml
git commit -m "CI: doctest на кожен push"
git push
```
```text
To github.com:Evge14n/pisochnytsia.git
   8280b43..4278603  main -> main
```
На сайті: репо → вкладка **Actions** → запуск «CI: doctest на кожен push» → `test` → крок `Doctest` з виводом `-v` (кожен тест і `Test passed.`). Біля коміту на головній сторінці - жовта крапка (йде), потім зелена галочка або червоний хрестик. З терміналу (gh, урок 16):
```bash
gh run list --limit 3
gh run watch
```
(Сам запуск на GitHub не перевірено - у перевірці курсу GitHub підмінено. Перевірено: файл - правильний YAML з цими ключами, а команда кроку `Doctest` на цих файлах виходить з 0, на зламаному `lab.py` - з 1.)

Для публічних репо Actions на звичайних раннерах безкоштовні; для приватних на GitHub Free є місячний ліміт ($12 «included compute usage», це близько 2000 хв Linux за $0.006/хв) - на doctest лаб вистачить із запасом.

### Ще кілька слів (знати, що існує)

- **Підпис комітів SSH-ключем.** GitHub ставить біля підписаного коміту позначку **Verified** - доказ, що коміт зробив саме ти. SSH-підпис - найпростіший (той самий ключ з уроку 03 можна завантажити ще раз як «Signing Key»). Налаштування з docs.github.com «Telling Git about your signing key» (у перевірці коміт справді отримав підпис; позначку на сайті не перевірено):
  ```text
  git config --global gpg.format ssh
  git config --global user.signingkey ~/.ssh/id_ed25519.pub
  git config --global commit.gpgsign true
  ```
  Потім Settings → SSH and GPG keys → New SSH key → Key type **Signing Key**. Для лаб не обовʼязково.
- **Git LFS** - для великих файлів (відео, датасети): у репо лежить маленький файл-вказівник, а сам файл - окремо. На Free до 2 GB на файл. Для лаб не треба: лаби - текст і `.py`. (Окремий пакет `git-lfs`, у перевірці не встановлювався.)
- **Submodules** - репо всередині репо (`git submodule add ...`). Складні і для лаб зайві: одного `univer-labs` досить.
- **Hooks** - скрипти в `.git/hooks/`, які git запускає сам. Напр. `pre-commit` запускається перед кожним комітом: якщо він вийде не з 0, коміт не зробиться. Туди можна покласти `python3 -m doctest ...` - тоді зламаний код навіть не закомітиш. Hooks не пушаться на GitHub, тому в командах їх часто ставлять утилітою pre-commit (pre-commit.com, не перевірено в курсі).

### Типові помилки

**1. Rebase з незакоміченими змінами.**
```text
$ git rebase main
error: cannot rebase: You have unstaged changes.
error: Please commit or stash them.
```
Закоміть або сховай (`git stash`, урок 13), потім rebase.

**2. `--continue`, не розвʼязавши конфлікт.**
```text
$ git rebase --continue
README.md: needs merge
You must edit all merge conflicts and then
mark them as resolved using git add
```
Прибери маркери в файлі, `git add README.md`, і тоді `git rebase --continue`. Заплутався - `git rebase --abort`.

**3. Rebase гілки, яку вже запушив** (порушив золоте правило). Гілку `lr6` запушив, потім `git rebase main` і `git push`:
```text
To github.com:Evge14n/pisochnytsia.git
 ! [rejected]        lr6 -> lr6 (non-fast-forward)
error: failed to push some refs to 'github.com:Evge14n/pisochnytsia.git'
hint: Updates were rejected because the tip of your current branch is behind
hint: its remote counterpart. If you want to integrate the remote changes,
hint: use 'git pull' before pushing again.
hint: See the 'Note about fast-forwards' in 'git push --help' for details.
```
А `git status` пише `Your branch and 'origin/lr6' have diverged, and have 2 and 1 different commits each, respectively.` - на GitHub старий коміт, у тебе його нова копія. **Не роби `git pull`** - отримаєш обидві копії і merge поверх. Якщо гілка лише твоя і її ніхто не брав (одногрупник не клонував, PR ніхто не рев'юїть) - можна переписати GitHub силою з перевіркою (урок 12):
```text
git push --force-with-lease
```
```text
To github.com:Evge14n/pisochnytsia.git
 + e59d82e...edd6a0c lr6 -> lr6 (forced update)
```
У `main` і будь-яку спільну гілку - ніколи. Там лише merge.

**4. Cherry-pick того самого коміту вдруге.**
```text
$ git cherry-pick eksperyment
The previous cherry-pick is now empty, possibly due to conflict resolution.
If you wish to commit it anyway, use:

    git commit --allow-empty

Otherwise, please use 'git cherry-pick --skip'
```
Ці зміни вже є в гілці, комітити нічого. `git cherry-pick --abort` - і все як було.

**5. Забув `git bisect reset`.** Після пошуку ти не на `main`, а «в повітрі»:
```text
$ git status
HEAD detached at 25e9cd6
You are currently bisecting, started from branch 'main'.
  (use "git bisect reset" to get back to the original branch)
```
Нові коміти тут не роби. `git bisect reset` поверне на `main`.

**6. `bisect run`, коли в старих комітах файлу ще нема.** Якщо `good` поставити на коміт, де `lab.py` ще не існував, doctest впаде з `ModuleNotFoundError: No module named 'lab'` і кодом 1 - git вирішить «поганий», хоча код не зламаний. Добрим називай коміт, де тест уже був і проходив.

**7. Та сама гілка у двох worktree.**
```text
$ git worktree add ~/git-pisochnytsia-17-main main
Preparing worktree (checking out 'main')
fatal: 'main' is already used by worktree at '/home/.../git-pisochnytsia-17'
```
Одна гілка - лише в одній теці (так само `git switch lr7` у першій теці дасть `fatal: 'lr7' is already used by worktree at ...`). Для другої теки бери нову гілку: `-b назва`.

### Як роблять профі

- Свою гілку перед PR підтягують до свіжого `main` через `git rebase main`, а «wip»-коміти зливають у `rebase -i`. На GitHub можна злити PR як «Squash and merge» або «Rebase and merge» (урок 11) ([Pro Git 3.6 «Rebasing»](https://git-scm.com/book/en/v2/Git-Branching-Rebasing), [Pro Git 7.6 «Rewriting History»](https://git-scm.com/book/en/v2/Git-Tools-Rewriting-History)).
- Опубліковане спільне не переписують; для своєї гілки після rebase - лише `--force-with-lease` ([git push](https://git-scm.com/docs/git-push)).
- Регресію («учора працювало») шукають `git bisect run` з тестом, а не перебором вручну ([git bisect](https://git-scm.com/docs/git-bisect), [Pro Git 7.10 «Debugging with Git»](https://git-scm.com/book/en/v2/Git-Tools-Debugging-with-Git)).
- Два завдання паралельно (рев'ю чужого PR і своя робота) - через `git worktree`, щоб не стешити ([git worktree](https://git-scm.com/docs/git-worktree)).
- Кожен push і кожен PR проходять CI: тести, лінтер (наприклад Ruff), а `main` захищена правилом «не зливати, поки тести червоні» ([Building and testing Python](https://docs.github.com/en/actions/tutorials/build-and-test-code/python)).
- Коміти підписують (Verified), особливо у відкритих проєктах ([About commit signature verification](https://docs.github.com/en/authentication/managing-commit-signature-verification/about-commit-signature-verification)).

### Для лаб

**Для лаб:** у `~/univer/labs` додай `.github/workflows/test.yml` з кроком `python -m doctest -v lr6/*.py` - кожен push сам перевіряє лаби, і викладачу можна показати зелену галочку. ЛР6 робиш у гілці `lr6`, а `main` пішов уперед (виправлення ЛР5) - `git rebase main` на `lr6`, поки не пушив. Накомітив «wip» - `git rebase -i` або `reset --soft` перед push. Doctest ЛР6 зламався і незрозуміло коли - `git bisect run python3 -m doctest lr6/main.py`. Викладач просить терміново поправити ЛР5, а ЛР6 у розпалі - `git worktree add ~/univer/labs-lr5 -b lr5-fix` замість stash.

### Самоперевірка

1. Що таке золоте правило rebase і що станеться, якщо його порушити?
2. Чим історія після `git rebase main` відрізняється від історії після `git merge`?
3. Як `git bisect run` вирішує, що коміт добрий, а що поганий?
4. Навіщо `git worktree`, якщо є `git switch` і `git stash`?
5. Де лежить workflow GitHub Actions і що в ньому означають `on: [push]` і `run:`?

<details markdown="1"><summary>Відповіді</summary>

1. Не перебазовувати коміти, які вже запушені і на які хтось міг спертися. Rebase робить нові коміти замість старих: push відмовить (non-fast-forward), а сила зламає історію тим, хто вже взяв старі.
2. Rebase дає пряму лінію без merge-коміту; твої коміти переписано (нові хеші) поверх `main`. Merge лишає розгалуження і додає коміт з двома батьками.
3. За кодом виходу команди: 0 - добрий, 1-127 крім 125 - поганий, 125 - пропустити. doctest дає 0 або 1.
4. Дві гілки відкриті одночасно в різних теках: не треба ховати незакомічене і перемикатися туди-сюди.
5. У `.github/workflows/` (напр. `test.yml`). `on: [push]` - запускати на кожен push; `run:` - команда терміналу, якщо вона повертає не 0, запуск червоний.

</details>

### Джерела

- Pro Git 3.6 «Rebasing» (золоте правило) - https://git-scm.com/book/en/v2/Git-Branching-Rebasing (відкрито 18.11.2026)
- Pro Git 7.6 «Rewriting History» (rebase -i, squash) - https://git-scm.com/book/en/v2/Git-Tools-Rewriting-History (відкрито 18.11.2026)
- Pro Git 7.10 «Debugging with Git» (blame, bisect) - https://git-scm.com/book/en/v2/Git-Tools-Debugging-with-Git (відкрито 18.11.2026)
- git rebase, git cherry-pick, git bisect (коди виходу run), git worktree, git log (-S), git grep, git blame - https://git-scm.com/docs/git-rebase, https://git-scm.com/docs/git-cherry-pick, https://git-scm.com/docs/git-bisect, https://git-scm.com/docs/git-worktree, https://git-scm.com/docs/git-log, https://git-scm.com/docs/git-grep, https://git-scm.com/docs/git-blame (відкрито 18.11.2026)
- MIT Missing Semester 2026, «Version Control and Git» - https://missing.csail.mit.edu/2026/version-control/ (відкрито 18.11.2026)
- Building and testing Python (приклад workflow, actions/checkout@v6, actions/setup-python@v5) - https://docs.github.com/en/actions/tutorials/build-and-test-code/python (відкрито 18.11.2026)
- Workflow syntax (тека `.github/workflows`) - https://docs.github.com/en/actions/reference/workflows-and-actions/workflow-syntax (відкрито 18.11.2026)
- GitHub Actions billing (публічні репо безкоштовно, Free - $12 на місяць) - https://docs.github.com/en/billing/concepts/product-billing/github-actions (відкрито 18.11.2026)
- About commit signature verification, Telling Git about your signing key - https://docs.github.com/en/authentication/managing-commit-signature-verification/about-commit-signature-verification, https://docs.github.com/en/authentication/managing-commit-signature-verification/telling-git-about-your-signing-key (відкрито 18.11.2026)
- About Git Large File Storage - https://docs.github.com/en/repositories/working-with-files/managing-large-files/about-git-large-file-storage (відкрито 18.11.2026)
- Pro Git 8.3 «Git Hooks» - https://git-scm.com/book/en/v2/Customizing-Git-Git-Hooks (відкрито 18.11.2026)

## Тема 18. Лаби в git - univer-labs покроково

**Навіщо:** усі сім лаб - в одному приватному репо на GitHub. Кожне завдання, що пройшло doctest, - окремий коміт
(зіпсуєш - повернешся). Кожна лаба - своя гілка. Кожна здача - тег. Викладачу - посилання або архів одною командою.

Перед цим файлом: Уроки 04-09 (коміти, гілки, push), 11 (PR), 14 (теги). Робоче місце - як у курсі Linux Mint:
теки `~/univer/labs/lr1` ... `~/univer/labs/lr7`, venv `~/univer/.venv` (він **поза** репо - так і має бути).
На GitHub і в повідомленнях комітів лаби звемо «ЛР1» ... «ЛР7», а теки й гілки - латиницею `lr1` ... `lr7`
(латиницю простіше набирати в терміналі).

### Як усе влаштовано

```text
GitHub: Evge14n/univer-labs (ПРИВАТНИЙ)                ноутбук: ~/univer/labs
  main ──●──────●───────────●──── ...                    .gitignore   README.md
         │      │ lr1-zdano │ lr2-zdano                  lr1/  lr1_1.py  lr1_2.py  lr1_3.py
         │      │           │                            lr2/  ...
  lr1    └─●─●─●┘           │                            ...
  lr2           └──●──●─────┘   (гілка на лабу,          lr7/
                                 коміт на завдання)
```

- **Один репо на всі лаби**, бо так простіше: один `git push`, одна історія, один `.gitignore`.
- **Гілка `lr1`** живе, поки робиш ЛР1. `main` - лише завершені лаби.
- **Коміт** - після кожного завдання, що пройшло doctest (і перед великою правкою, наприклад `black`).
- **Тег `lr1-zdano`** - на коміті, який показав викладачу (Урок 14).

Хеші комітів і шлях `/home/.../github/...` у виводах нижче - з перевірки. У тебе хеші інші, а замість шляху буде
`To github.com:Evge14n/univer-labs.git`.

### Один раз: репо univer-labs

**Крок 1. Чи є вже git у теці лаб?** Якщо ти робив Крок 8 Уроку 04 курсу Linux Mint, git там уже є.

```bash
cd ~/univer/labs
git status
```
Якщо бачиш `fatal: not a git repository (or any of the parent directories): .git` - git нема, йди у **варіант А**.
Якщо бачиш `On branch ...` - git є, йди у **варіант Б**.

**Крок 2. Порожній приватний репо на GitHub - створюєш сам.** Справа вгорі **+** → **New repository** →
Repository name: `univer-labs` → **Private** → README, .gitignore, license **не додавай** (репо має бути порожнім,
інакше перший push відхилять - див. «Що як» 5) → **Create repository**.

**Варіант А - git ще нема.**

```bash
mkdir -p ~/univer/labs/lr1
cd ~/univer/labs
git init
printf '.venv/\n__pycache__/\n*.pyc\n.pytest_cache/\n.mypy_cache/\n.ruff_cache/\n' > .gitignore
printf '# Лабораторні з програмування\n\nЛР1-ЛР7, 1 курс. Кожна лаба - тека lrN і тег lrN-zdano.\n' > README.md
git add .gitignore README.md
git commit -m "Початок: .gitignore і README"
git remote add origin git@github.com:Evge14n/univer-labs.git
git push -u origin main
```
```text
To /home/evgen/.cache/ugit.1lm8vp/laby/github/Evge14n/univer-labs.git
 * [new branch]      main -> main
branch 'main' set up to track 'origin/main'.
```
`.gitignore` (Урок 06): `.venv/` - віртуальне середовище, `__pycache__/` і `*.pyc` - скомпільований Python,
`.pytest_cache/`, `.mypy_cache/`, `.ruff_cache/` - сміття від pytest, mypy і ruff.

Замість Кроку 2 на сайті і двох останніх рядків можна одним рядком через gh (Урок 16) - він створить приватний репо,
додасть `origin` і запушить:

```bash
gh repo create univer-labs --private --source=. --remote=origin --push
```

**Варіант Б - git уже є (з курсу Linux Mint).** Подивись, що там:

```bash
git log --oneline
git branch --show-current
```
Якщо гілка називається `master` (git до налаштування з Уроку 02 так називав першу гілку) - перейменуй:

```bash
git branch -m master main
```
У `.gitignore` з курсу Linux Mint нема `.venv/` і `*.pyc` - допиши (`>>` дописує в кінець, `>` перезаписав би):

```bash
printf '.venv/\n*.pyc\n' >> .gitignore
git add .gitignore
git commit -m "gitignore: .venv і *.pyc"
git remote add origin git@github.com:Evge14n/univer-labs.git
git push -u origin main
```
Старі коміти ЛР1 так і лишаться на `main` - це нормально, гілки починай з наступної лаби.

### На кожну лабу - рецепт

```text
git switch main && git pull                     # свіжий main
git switch -c lrN                               # гілка лаби
  (заготовка в lrN/)  git add lrN  git commit -m "ЛРN: заготовки викладача"
  повтор на кожне завдання:
    nano lrN/lrN_K.py  →  doctest пройшов  →  git commit -am "ЛРN: завдання K"
git push -u origin lrN                          # копія на GitHub (і для PR)
злиття в main: або git switch main + git merge lrN + git push,
               або PR на GitHub (gh pr create --fill --base main) і Merge
git tag -a lrN-zdano -m "ЛРN здано" main  +  git push origin lrN-zdano     # коли здав
```
Чому спершу коміт **заготовки**: тоді `git diff` завжди покаже, що саме ти змінив у файлі викладача, а викладач
забороняє міняти назви функцій, параметри і doctest заготовки (див. «Вимоги викладача»).

### ЛР1 від гілки до архіву

**Гілка і заготовки.** Заготовки поклади в `~/univer/labs/lr1/` так, як у курсі Linux Mint (Урок 04 - з `.ipynb`).

```bash
git switch main
git pull
git switch -c lr1
git add lr1
git commit -m "ЛР1: заготовки викладача"
```

**Завдання 1.** Пишеш код, перевіряєш doctest, комітиш.

```bash
nano lr1/lr1_1.py
python3 -m doctest lr1/lr1_1.py
git status --short
git commit -am "ЛР1: завдання 1"
```
`python3 -m doctest` нічого не друкує - отже всі тести пройшли (для лаб з `input()` бери команду з розділу
«Перевір перед здачею» курсу Linux Mint). `git status --short` має показати лише ` M lr1/lr1_1.py`: тека
`lr1/__pycache__`, яку створив Python, не видна - її ховає `.gitignore`.

**Завдання 2** - так само:

```bash
nano lr1/lr1_2.py
python3 -m doctest lr1/lr1_2.py
git commit -am "ЛР1: завдання 2"
git push -u origin lr1
git log --oneline main..lr1
```
```text
676c781 ЛР1: завдання 2
ac98c9d ЛР1: завдання 1
09e5e28 ЛР1: заготовки викладача
```
`main..lr1` - коміти, які є в `lr1`, але ще нема в `main`. `git push -u origin lr1` - копія гілки на GitHub:
ноутбук зламався - лаба ціла.

**Лабу закінчено - у `main`.** Найпростіше - злиття в себе (Урок 07):

```bash
git switch main
git merge lr1
git push
git branch -d lr1
```
`git merge` скаже `Fast-forward`: `main` просто наздогнав `lr1`. Гілку `lr1` можна видалити - її коміти тепер у `main`
(на GitHub вона ще є, її видалиш кнопкою на сторінці гілок або `git push origin --delete lr1`).

**Здав - тег** (Урок 14):

```bash
git tag -a lr1-zdano -m "ЛР1 здано"
git push origin lr1-zdano
```
```text
To /home/evgen/.cache/ugit.1lm8vp/laby/github/Evge14n/univer-labs.git
 * [new tag]         lr1-zdano -> lr1-zdano
```

### ЛР2 через Pull Request

Те саме, але злиття - через PR (Урок 11): видно всі зміни лаби на одній сторінці, можна попросити одногрупника глянути.

```bash
git switch main
git pull
git switch -c lr2
mkdir -p lr2
python3 -m doctest lr2/lr2_1.py
git add lr2/lr2_1.py
git commit -m "ЛР2: завдання 1"
git push -u origin lr2
gh pr create --fill --base main
```
(Між `mkdir` і `doctest` - заготовка й `nano`, як у ЛР1.) Без gh: на сторінці репо зʼявиться жовта смуга
з кнопкою **Compare & pull request** (Урок 11). На сторінці PR → **Merge pull request** → **Confirm merge**. Потім у себе:

```bash
git switch main
git pull
git log --oneline --graph -n 3
git tag -a lr2-zdano -m "ЛР2 здано" main
git push origin lr2-zdano
```
```text
*   0e746e0 Merge pull request #1 from Evge14n/lr2
|\
| * 90a7770 ЛР2: завдання 1
|/
* 676c781 ЛР1: завдання 2
```
`main` у кінці рядка з тегом - тег саме на `main`, навіть якщо ти вже на іншій гілці. Список здач:

```bash
git tag -n
```
```text
lr1-zdano       ЛР1 здано
lr2-zdano       ЛР2 здано
```

### Як показати викладачу

**Спосіб 1. Посилання на репо.** Приватний репо бачать лише запрошені. Запросити: у репо **Settings** → розділ
«Access» → **Collaborators** → **Add people** → логін викладача → **Add ... to univer-labs**. Йому прийде лист,
доступ буде після того, як він прийме запрошення (docs.github.com, «Inviting collaborators to a personal repository»,
відкрито 18.11.2026). **Увага:** у приватному репо особистого акаунта співавтор отримує доступ **на запис**:
«repository owners can only grant write access to collaborators. Collaborators can't have read-only access»
(docs, «Permission levels for a personal account repository»). Тобто викладач зможе і пушити. Після семестру
прибери доступ там само (Collaborators → Remove). Посилання на конкретну здачу:
`https://github.com/Evge14n/univer-labs/tree/lr1-zdano/lr1`.

**Спосіб 2. Архів zip** - коли викладач хоче файли (вимога з консультації: тека з назвою «прізвище, ім'я, група,
рік»; точний формат архіву уточни на парі). `git archive` бере файли **з тегу**, а не з теки на диску, тому в архів
потрапляє рівно здана версія і лише те, що в git: без `.venv`, `__pycache__`, `.pytest_cache`.

```bash
mkdir -p ~/univer/zdacha
git archive --format=zip --prefix=Прізвище_Імʼя_Група_2026/ -o ~/univer/zdacha/lr1.zip lr1-zdano lr1
python3 -m zipfile -l ~/univer/zdacha/lr1.zip
```
```text
File Name                                             Modified             Size
Прізвище_Імʼя_Група_2026/                    2026-11-18 10:35:20            0
Прізвище_Імʼя_Група_2026/lr1/                2026-11-18 10:35:20            0
Прізвище_Імʼя_Група_2026/lr1/lr1_1.py        2026-11-18 10:35:20          114
Прізвище_Імʼя_Група_2026/lr1/lr1_2.py        2026-11-18 10:35:20          105
```
Що тут що: `--format=zip` - zip, а не tar; `--prefix=.../` - тека, в яку все покладуть усередині архіву (скісна
риска в кінці обовʼязкова); `-o` - куди писати архів; `lr1-zdano` - з якого тегу брати; `lr1` - лише ця тека, а не
весь репо. Перевірено: у тій самій теці на диску лежали `.venv/`, `lr1/__pycache__/`, `lr1/.pytest_cache/` - в архів
не потрапило нічого з цього, і `.gitignore` теж. Кирилиця в назвах збережена з UTF-8-позначкою zip.
`python3 -m zipfile -l` показує вміст архіву (окремої програми `unzip` не треба). Для ЛР2:

```bash
git archive --format=zip --prefix=Прізвище_Імʼя_Група_2026/ -o ~/univer/zdacha/lr2.zip lr2-zdano lr2
```

**Спосіб 3. «Download ZIP» на сайті.** У репо → **Releases** → вгорі **Tags** → біля `lr1-zdano` посилання **zip**
(docs, «Downloading source code archives»). Це архів **усього** репо на момент тегу (усі лаби до тієї, і README),
а тека всередині названа за назвою репо - тож для здачі однієї лаби зручніший `git archive`.

### Що як ...

**1. Почав лабу на `main` без гілки** (кілька комітів, ще не пушив). `git status` каже
`Your branch is ahead of 'origin/main' by 2 commits.` Перенеси коміти в гілку і поверни `main` назад:

```bash
git switch -c lr3
git branch -f main origin/main
git log --oneline main..lr3
```
```text
branch 'main' set up to track 'origin/main'.
10107b7 ЛР3: завдання 2
549cce4 ЛР3: завдання 1
```
`git switch -c lr3` - нова гілка там, де ти стоїш, з усіма комітами. `git branch -f main origin/main` - «постав `main`
туди, де він на GitHub»; файли не чіпає, бо ти вже на `lr3`. Перший рядок виводу - не помилка: git заодно нагадує,
що `main` стежить за `origin/main`. Якщо ж забудеш перейти на `lr3`, git не дасть пересунути поточну гілку:
`fatal: cannot force update the branch 'main' used by worktree at '...'` (далі - шлях до твоєї теки).
Якщо коміти на `main` уже **запушив** - не виправляй історію силою; просто продовжуй, наступну лабу почни з гілки.

**2. Забув поставити тег**, а вже робиш наступну лабу. Тег можна поставити заднім числом на будь-який коміт:

```bash
git tag -a lr2-zdano -m "ЛР2 здано" main
git push origin lr2-zdano
```
Якщо `main` уже пішов далі, знайди потрібний коміт у `git log --oneline` і постав тег на його хеш:
```text
git tag -a lr2-zdano -m "ЛР2 здано" ХЕШ
```

**3. Закомітив `.venv`** (або `__pycache__`). Прибери з git, лишивши на диску:

```bash
git rm -r --cached .venv
git commit -m "Прибрав .venv з git"
git ls-files .venv
git check-ignore -v .venv
```
```text
rm '.venv/pyvenv.cfg'
.gitignore:1:.venv/	.venv
```
`--cached` - лише з git, файли на диску лишаються. `git ls-files .venv` після цього нічого не друкує.
`git check-ignore -v` показує, яке правило `.gitignore` тепер ховає `.venv` (рядок 1). Якщо в `.gitignore` правила нема -
спершу допиши його (`printf '.venv/\n*.pyc\n' >> .gitignore`, варіант Б). Старі коміти з `.venv` в історії лишаться -
для лаб це лише зайвий розмір, не біда.

**4. Не знаєш, що ти змінив після здачі:** `git diff lr1-zdano main -- lr1` (Уроки 05, 14).

**5. Створив репо на сайті З README - перший push відхилено.**
```text
 ! [rejected]        main -> main (fetch first)
error: failed to push some refs to '...'
hint: Updates were rejected because the remote contains work that you do not
hint: have locally.
```
На GitHub є коміт з README, якого нема в тебе, а історії зовсім різні, тому звичайний `git pull` скаже
`fatal: refusing to merge unrelated histories`. Обʼєднай явно і запуш:

```bash
git pull --allow-unrelated-histories origin main
git push -u origin main
```
`git pull` відкриє nano з повідомленням злиття - просто Ctrl+X.

**Для лаб** - цей файл і є «для лаб»: ЛР1-ЛР7 за одним рецептом, викладачу - посилання або архів з тегу.

### Самоперевірка

1. Чому один приватний репо `univer-labs`, а не публічний, і чому не сім окремих?
2. Коли робити коміт під час лаби і навіщо перший коміт - із заготовкою?
3. Ти закінчив ЛР3 на гілці `lr3`. Які команди - злити в `main`, поставити тег здачі і відправити все на GitHub?
4. Чому в архіві `git archive ... lr1-zdano lr1` нема `.venv` і `__pycache__`, хоч вони лежать у теці?
5. Ти дав викладачу доступ Collaborator до приватного репо. Що він може робити і що зробити після семестру?

<details markdown="1"><summary>Відповіді</summary>

1. Приватний - бо розвʼязки до здачі не мають бачити одногрупники. Один - бо простіше: один `.gitignore`, один push,
   уся історія лаб разом; лаби розділяють теки `lr1`...`lr7`, гілки і теги.
2. Після кожного завдання, що пройшло doctest (і перед великою правкою). Перший коміт із заготовкою - щоб `git diff`
   показував, що саме ти змінив у файлі викладача.
3. `git switch main`, `git merge lr3`, `git push`, `git tag -a lr3-zdano -m "ЛР3 здано"`, `git push origin lr3-zdano`
   (або PR на GitHub, потім `git pull` і тег).
4. `git archive` бере файли з коміту під тегом, а в коміти вони не потрапляють - їх ховає `.gitignore`.
5. Читати і пушити: у приватному репо особистого акаунта доступ співавтора лише «на запис». Після семестру -
   Settings → Collaborators → Remove.

</details>

### Джерела

- Pro Git, 3.2 «Basic Branching and Merging»: https://git-scm.com/book/en/v2/Git-Branching-Basic-Branching-and-Merging
  (відкрито 18.11.2026)
- git-scm.com/docs/git-archive: https://git-scm.com/docs/git-archive (відкрито 18.11.2026)
- docs.github.com, «Inviting collaborators to a personal repository»:
  https://docs.github.com/en/account-and-profile/setting-up-and-managing-your-personal-account-on-github/managing-access-to-your-personal-repositories/inviting-collaborators-to-a-personal-repository
  (відкрито 18.11.2026)
- docs.github.com, «Permission levels for a personal account repository»:
  https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/repository-access-and-collaboration/permission-levels-for-a-personal-account-repository
  (відкрито 18.11.2026)
- docs.github.com, «Downloading source code archives»:
  https://docs.github.com/en/repositories/working-with-files/using-files/downloading-source-code-archives (відкрито 18.11.2026)
- cli.github.com, `gh repo create`: https://cli.github.com/manual/gh_repo_create (відкрито 18.11.2026)
- Файл вимог викладача в теці `05_Програмування` (тека з назвою «прізвище, ім'я, група, рік»);
  курс Linux Mint, Урок 04 (теки `lr1`, заготовки, «Перевір перед здачею»)
- docs.github.com, «Creating a pull request» (жовта смуга «Compare & pull request»):
  https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/proposing-changes-to-your-work-with-pull-requests/creating-a-pull-request
  (відкрито 18.11.2026)
- docs.github.com, «Merging a pull request»:
  https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/incorporating-changes-from-a-pull-request/merging-a-pull-request
  (відкрито 18.11.2026)
