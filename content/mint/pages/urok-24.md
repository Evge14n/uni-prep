# Урок 24. git і GitHub з ssh-ключем

[← Усі уроки](#/u/mint/uroky)

**Навіщо:** git - «збереження гри» для коду: зламав лабу - за секунду назад до робочої версії. GitHub - копія
твоїх лаб у хмарі (приватна), з якої їх можна дістати на будь-якому компʼютері.

## Коротко

git запамʼятовує **коміти** - знімки теки з підписом «що змінив». Шлях файлу до коміту:

```text
правиш файл  ──git add──►  вибрано в коміт  ──git commit──►  історія (git log)
(робоча тека)              (staging)                         │
                                                             └──git push──► GitHub (origin)
                                                  git pull ◄──────────────┘
```

| Команда | Що робить |
|---|---|
| `git init` | зробити теку репозиторієм (один раз) |
| `git status` | що змінено, що вибрано в коміт (`--short` - коротко) |
| `git add файл` | вибрати файл у наступний коміт (`git add .` - усе в теці) |
| `git commit -m "опис"` | зробити коміт |
| `git log --oneline` | історія, по рядку на коміт |
| `git diff` | що змінено і ще не вибрано (вийти - `q`) |
| `git restore файл` | **викинути** незакомічені зміни файлу (назавжди!) |
| `git switch -c назва` / `git switch main` | нова гілка / повернутись на main |
| `git merge назва` | влити гілку в поточну |
| `git remote add origin адреса` | запамʼятати адресу GitHub під імʼям `origin` |
| `git push` / `git pull` | відправити коміти / забрати чужі (свої з іншого компʼютера) |
| `git clone адреса` | скопіювати весь репозиторій (на новому компʼютері) |

**`.gitignore`** - список того, що git не бачить. Для лаб:

```text
.venv/
__pycache__/
.mypy_cache/
.pytest_cache/
.ruff_cache/
```

**Гілка** (branch) - окрема лінія комітів. `main` - основна. Хочеш спробувати інший розвʼязок, не ламаючи
робочий, - `git switch -c sproba`, комітиш там, а якщо вдалось - `git merge` у main.

**GitHub і ключ.** GitHub приймає `git push` по ssh-ключу з уроку 21: ти один раз даєш GitHub свій **публічний**
ключ (`~/.ssh/id_ed25519.pub`), і далі паролі не потрібні. Адреса репозиторію для ssh має вигляд
`git@github.com:Evge14n/labs.git`.

**Чесність.** Репозиторій з розвʼязками лаб - **приватний** (Private). Публічний репозиторій з розвʼязками до
дедлайну - це те саме, що дати списати всій групі. Після здачі можна, але спершу спитай викладача.

## Передбач, потім запусти

1. На новому компʼютері git ще не знає, хто ти. Що буде на першому коміті?

```bash
git commit -m "Функція double"
```

<details markdown="1"><summary>Відповідь</summary>

Відмова. Вивід з **тестової** Mint 22.3 (імʼя компʼютера в ньому замінено на `evgen-laptop`):

```text
Author identity unknown

*** Please tell me who you are.

Run

  git config --global user.email "you@example.com"
  git config --global user.name "Твоє Імʼя Прізвище"

to set your account's default identity.
Omit --global to set the identity only in this repository.

fatal: empty ident name (for <evgen@evgen-laptop.localdomain>) not allowed
```

На ноутбуці **останній рядок буде інший**. У тестовій системі в користувача порожнє повне імʼя, тому git скаржиться
на імʼя. А на ноутбуці повне імʼя ти ввів, коли ставив Mint, - git його візьме, але не зможе вгадати пошту:

```text
fatal: unable to auto-detect email address (got 'evgen@evgen-laptop.(none)')
```

(на ноутбуці не перевірено; так git пише, коли в імені компʼютера нема домену). Українською перші рядки -
`Особистість автора невідома` і `*** Будь ласка, скажіть мені, хто ви.`, а останній - `fatal: не вдалося
автоматично визначити адресу електронної пошти (отримано "evgen@evgen-laptop.(none)")`. Лікується кроком 1
(`git config --global user.name` і `user.email`).

</details>

2. Ти змінив `lab.py` (`x * 2` → `x * 3`) і створив новий файл `чернетка.py`. Що скаже `git status`?

<details markdown="1"><summary>Відповідь</summary>

```text
On branch main
Changes not staged for commit:
  (use "git add <file>..." to update what will be committed)
  (use "git restore <file>..." to discard changes in working directory)
	modified:   lab.py

Untracked files:
  (use "git add <file>..." to include in what will be committed)
	чернетка.py

no changes added to commit (use "git add" and/or "git commit -a")
```

`modified` - файл, який git уже знає, змінено. `Untracked` - git цей файл ще ніколи не бачив. Українська назва
показана нормально, бо `core.quotepath false` (крок 1).

</details>

3. Після `python3 -m venv .venv` у теці репозиторію `git status --short` показує `?? .venv/`. Що зміниться, коли
   створиш `.gitignore` з рядком `.venv/`?

<details markdown="1"><summary>Відповідь</summary>

`.venv/` зникне зі списку - git його більше не бачить. Замість нього зʼявиться сам `.gitignore` (його треба
закомітити):

```text
?? .gitignore
?? чернетка.py
```

</details>

4. Ти на гілці `sproba` дописав функцію і закомітив. Потім `git switch main`. Чи є ця функція в `lab.py`?

<details markdown="1"><summary>Відповідь</summary>

Нема: `grep -c triple lab.py` дасть `0`. Файли в теці завжди показують ту гілку, на якій ти стоїш. Після
`git merge sproba` функція зʼявиться і в main.

</details>

## Руками

**Крок 1. Налаштувати git (один раз на компʼютер).** git є не на свіжій Mint, а після уроку 03
(`sudo apt install git`). Імʼя - як на GitHub:

```bash
git config --global user.name "Твоє Імʼя Прізвище"
git config --global init.defaultBranch main
git config --global core.quotepath false
```

Пошта: на GitHub відкрий Settings → Emails, увімкни «Keep my email addresses private» і скопіюй адресу виду
`...@users.noreply.github.com` - тоді справжня пошта не потрапить у коміти. Команда (встав свою адресу):

```text
git config --global user.email "скопійована_адреса@users.noreply.github.com"
```

Перевір: `git config --global --list`. `init.defaultBranch main` - щоб основна гілка звалась `main`, а не `master`
(без цього `git init` друкує довгу підказку `hint: Using 'master' as the name for the initial branch`).
`ustanovka-mint.sh` з уроку 03 два останні рядки вже зробив.

**Крок 2. Тренувальний репозиторій.**

```bash
mkdir -p ~/univer/praktyka/git24 && cd ~/univer/praktyka/git24
git init
printf 'def double(x: int) -> int:\n    """\n    >>> double(4)\n    8\n    """\n    return x * 2\n' > lab.py
git status
git add lab.py
git commit -m "Функція double"
git log --oneline
```

Кінець виводу:

```text
[main (root-commit) a4fbd19] Функція double
 1 file changed, 6 insertions(+)
 create mode 100644 lab.py
a4fbd19 Функція double
```

`a4fbd19` - початок «імені» коміту (хеша). У тебе він буде інший: хеш залежить від автора і часу.

**Крок 3. Зламати і повернути.**

```bash
sed -i 's/x \* 2/x * 3/' lab.py
printf 'print("чернетка")\n' > чернетка.py
git status
git diff
git restore lab.py
git status --short
```

`git diff` показує, що саме змінено (`-` було, `+` стало):

```text
diff --git a/lab.py b/lab.py
index add341c..1d9cbaf 100644
--- a/lab.py
+++ b/lab.py
@@ -3,4 +3,4 @@ def double(x: int) -> int:
     >>> double(4)
     8
     """
-    return x * 2
+    return x * 3
```

Після `git restore lab.py` у `git status --short` лишиться тільки `?? чернетка.py` - зміна в `lab.py` зникла.

**Крок 4. .gitignore.**

```bash
python3 -m venv .venv
git status --short
printf '.venv/\n__pycache__/\n.mypy_cache/\n.pytest_cache/\n.ruff_cache/\n' > .gitignore
git status --short
git add .gitignore чернетка.py
git commit -m "gitignore і чернетка"
```

**Крок 5. Гілка.**

```bash
git switch -c sproba
printf '\n\ndef triple(x: int) -> int:\n    return x * 3\n' >> lab.py
git commit -am "Спроба: triple"
git switch main
grep -c triple lab.py
git merge sproba
git log --oneline
git branch -d sproba
```

`-am` = `git add` для вже відомих файлів + `-m`. Справжній вивід злиття і історії:

```text
Updating 8806241..632cd09
Fast-forward
 lab.py | 4 ++++
 1 file changed, 4 insertions(+)
632cd09 Спроба: triple
8806241 gitignore і чернетка
a4fbd19 Функція double
```

`Fast-forward` - main просто «пересунули вперед» на коміти з гілки, бо в main за цей час нічого нового не було.

**Крок 6. Репозиторій на GitHub (у браузері).** github.com → зайди → `+` угорі праворуч → **New repository**:
назва `labs`, **Private**, README / .gitignore / license **не** додавай (у тебе вже є локальний репозиторій) →
**Create repository**. (Кроки - з документації GitHub; назви кнопок можуть трохи змінитись.)

**Крок 7. Дати GitHub свій ssh-ключ.** Ключ з уроку 21:

```bash
cat ~/.ssh/id_ed25519.pub
```

Скопіюй рядок (виділи і Ctrl+Shift+C). GitHub → аватар → **Settings** → **SSH and GPG keys** → **New SSH key** →
Title: `Mint laptop`, Key type: Authentication Key, вставити → **Add SSH key**. Перевір:

```bash
ssh -T git@github.com
```

За документацією GitHub має бути (замість USERNAME - твій логін):

```text
Hi USERNAME! You've successfully authenticated, but GitHub does not
provide shell access.
```

(Цей вивід не перевірено в тестовій Mint: її ключа на GitHub нема, там справжня відповідь -
`git@github.com: Permission denied (publickey).`, як в уроці 21. Код виходу навіть при успіху - 1, так пише
GitHub.)

**Крок 8. Відправити лаби.** Репозиторій лаб - `~/univer/labs` з уроку 04. Якщо ти робив необовʼязковий крок 8
уроку 04, там уже є `git init` і коміти. Не робив (`git status` пише `fatal: not a git repository`) - спершу:

```bash
cd ~/univer/labs
git init
printf '.mypy_cache/\n.ruff_cache/\n.pytest_cache/\n__pycache__/\n' > .gitignore
git add .
git commit -m "Лаби на початок"
```

Далі - відправити:

```bash
cd ~/univer/labs
git status
git remote add origin git@github.com:Evge14n/labs.git
git push -u origin main
```

`-u` запамʼятовує, що `main` іде в `origin/main`, і далі досить `git push` і `git pull`. У тестовій Mint замість
GitHub був локальний «сервер» (`git init --bare`), і `git push -u` надрукував:

```text
To /home/evgen/labs.git
 * [new branch]      main -> main
branch 'main' set up to track 'origin/main'.
```

З GitHub буде `To github.com:Evge14n/labs.git` і ще кілька рядків прогресу (`Enumerating objects...`) - не
перевірено. Онови сторінку репозиторію в браузері - файли там.

**Крок 9. Щодня.**

```bash
cd ~/univer/labs
git add .
git commit -m "ЛР2: завдання 1"
git push
```

На іншому компʼютері: `git clone git@github.com:Evge14n/labs.git` (раз), далі `git pull` перед роботою і
`git push` після. Справжній `git pull` у тестовій Mint, коли на «сервері» був новий коміт:

```text
Updating 632cd09..adc7f34
Fast-forward
 nove.py | 1 +
 1 file changed, 1 insertion(+)
 create mode 100644 nove.py
```

## Далі - за бажанням

Крок 10 - інший шлях до того самого (програма `gh`). Якщо кроки 6-9 вийшли, він не потрібен.

**Крок 10 (інший шлях). `gh` - офіційна програма GitHub.** Вміє сама зробити ключ, залогінитись і створити
репозиторій.

**Увага: `sudo apt install gh` з репозиторію Mint дає стару версію 2.45, і вона зламана** - `gh pr view` і
`gh issue view` падають з «GraphQL: Projects (classic) is being deprecated». Розробники gh пишуть прямо: «the
community-distributed 2.45.x / 2.46.x version is broken» (cli/cli, docs/install_linux.md, 18.11.2026). Тому став gh
з **офіційного репозиторію GitHub** - це довгий рядок, копіюй його цілим (він додає ключ і репозиторій GitHub, потім
gh оновлюватиметься разом з системою через Диспетчер оновлень):

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

Перевір: `gh --version` має показати 2.100 чи новішу, а не 2.45. Потім вхід:

```bash
gh auth login -p ssh -w
```

`-p ssh` - працювати через ssh, `-w` - увійти через браузер (gh покаже одноразовий код, його вставляєш на сайті).
Створити приватний репозиторій з поточної теки і одразу відправити:

```bash
cd ~/univer/labs
gh repo create labs --private --source=. --push
```

(Опції перевірено в `gh --help` у тестовій Mint; сам вхід - ні, там нема браузера й акаунта. Сніпет офіційного
репозиторію перевірила сесія курсу git: встановився gh 2.105.0, `gh pr view` працює.)

**Хочеш git глибше** (гілки, конфлікти, Pull Request, теги для здачі, GitHub Pages, повний розбір gh) - окремий
курс `05_Програмування\Git-GitHub\` (уроки 01-16 і «Лаби в git - univer-labs покроково»), робоче місце там те саме:
`~/univer/labs/lr1`...`lr7`.

## Типові помилки

git перекладено: якщо Mint українською, повідомлення git теж українською (у дужках - справжній запуск з перекладом
`language-pack-uk-base`); відповіді GitHub (`remote: ...`) і ssh - англійською. Англійський текст для пошуку:
`LC_ALL=C git ...`.

- **`Author identity unknown`** (`Особистість автора невідома`) - передбачення 1, крок 1.
- **`hint: Using 'master' as the name for the initial branch`** (`Використання "master" як назви початкової
  гілки`) - не задано `init.defaultBranch main` до `git init`. Для вже створеного: `git branch -m main`.
- **`error: src refspec main does not match any`** (`error: визначник посилання джерела main не збігається з
  жодним`) при push - у репозиторії ще нема жодного коміту (або гілка зветься `master`). `git log --oneline`,
  `git branch`.
- **`git@github.com: Permission denied (publickey).`** - GitHub не знає твій ключ (крок 7) або ssh бере інший.
- **`remote: Support for password authentication was removed`** - адреса `https://...`, а не `git@github.com:...`
  (не перевірено в тестовій Mint). Виправити: `git remote set-url origin git@github.com:Evge14n/labs.git`.
- **`! [rejected] main -> main (fetch first)`** (українською `[відхилено]`) - на GitHub є коміти, яких нема в тебе (пушив з іншого компʼютера).
  Спершу `git pull`, потім `git push` (текст не перевірено в тестовій Mint).
- **Закомітив `.venv`** - тисячі файлів. Спершу `.gitignore`, потім `git rm -r --cached .venv` і коміт.
- **Закомітив пароль чи токен** - вважай, що він уже витік: **зміни пароль / відклич токен**. `git rm --cached
  файл` прибирає файл лише з наступних комітів, у старих він лишається. Секрети тримай поза репозиторієм і
  додавай їхні файли в `.gitignore`.
- **`git restore` стер потрібне** - він не питає і не має «назад». Перед ним глянь `git diff`.
- **`git commit` без `-m`** відкриє редактор (у Mint - nano): напиши опис, Ctrl+S, Ctrl+X.

## Як роблять профі

- **Маленькі коміти з людським описом.** Одне завдання або одна правка - один коміт. Книга Pro Git і курс
  MIT «Missing Semester» (лекція Version Control) вчать саме так.
- **Гілка на кожну спробу**, main завжди робочий.
- **ssh-ключ з паролем або gh**, а не паролі: GitHub не приймає пароль акаунта для git з 13.08.2021 (блог GitHub;
  для https - лише токени).
- **Приватний noreply-email** у комітах - щоб пошта не потрапила в публічну історію.
- **Секрети - ніколи в git.** Навіть у приватному репозиторії: його можуть зробити публічним, а історія лишиться.

## Самоперевірка

1. Назви по порядку команди, якими новий файл потрапляє на GitHub.
2. Чим `git restore lab.py` небезпечний і що зробити перед ним?
3. Навіщо `.gitignore` і що в ньому має бути для лаб на Python?
4. Ти пушиш з ноутбука, а git пише `Permission denied (publickey)`. Що перевірити?
5. Чому репозиторій з лабами має бути приватним?

<details markdown="1"><summary>Відповіді</summary>

1. `git add файл`, `git commit -m "опис"`, `git push` (перший раз - `git push -u origin main` після
   `git remote add origin ...`).
2. Він назавжди викидає незакомічені зміни файлу, без питань. Спершу `git diff` (або коміт).
3. Щоб git не зберігав те, що можна перестворити або що секретне: `.venv/`, `__pycache__/`, кеші
   `.mypy_cache/`, `.pytest_cache/`, `.ruff_cache/`.
4. Чи доданий `~/.ssh/id_ed25519.pub` на GitHub (Settings → SSH and GPG keys), чи `ssh -T git@github.com` вітає
   тебе, чи адреса `origin` має вигляд `git@github.com:...` (`git remote -v`).
5. Академічна чесність: публічні розвʼязки до дедлайну можуть списати інші, а відповідати будеш і ти. Викладач
   перевіряє розуміння.

</details>

## Джерела

- Pro Git - https://git-scm.com/book/en/v2 , українською - https://git-scm.com/book/uk/v2 - відкрито 18.11.2026
- GitHub, вимога токенів замість паролів з 13.08.2021 -
  https://github.blog/security/application-security/token-authentication-requirements-for-git-operations/ -
  відкрито 18.11.2026
- GitHub: створення репозиторію - https://docs.github.com/en/repositories/creating-and-managing-repositories/creating-a-new-repository ;
  додати ssh-ключ - https://docs.github.com/en/authentication/connecting-to-github-with-ssh/adding-a-new-ssh-key-to-your-github-account ;
  перевірка (`Hi USERNAME!`, код виходу 1) - https://docs.github.com/en/authentication/connecting-to-github-with-ssh/testing-your-ssh-connection -
  відкрито 18.11.2026
- GitHub CLI `gh auth login` - https://cli.github.com/manual/gh_auth_login - відкрито 18.11.2026
- MIT Missing Semester, Version Control (Git) - https://missing.csail.mit.edu/ - відкрито 18.11.2026
- Версії в Mint 22.3: git 2.43.0 (ФАКТИ), gh 2.45.0-1ubuntu0.3 (`apt-cache policy gh` у тестовій Mint), 18.11.2026
- Усі показані виводи git - запуском у тестовій Mint 22.3 (git 2.43.0), 18.11.2026; виводи GitHub - лише з
  документації, позначено
