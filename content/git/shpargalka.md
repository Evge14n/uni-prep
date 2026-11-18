# Git і GitHub - шпаргалка (1 сторінка)


## Один раз на ноутбуці (уроки 02-03)
```
sudo apt install git
git config --global user.name "Твоє Імʼя"
git config --global user.email "128326252+Evge14n@users.noreply.github.com"
git config --global init.defaultBranch main
git config --global core.editor nano
git config --global pull.rebase false
git config --global core.quotepath false
ssh-keygen -t ed25519 -C "128326252+Evge14n@users.noreply.github.com"
ssh -T git@github.com            (відповідь: Hi Evge14n! You've successfully authenticated...)
gh auth login -p ssh -w
```

## Три зони
```
робоча тека  --git add-->  індекс (staging)  --git commit-->  репозиторій  --git push-->  GitHub
             <-git restore-                   <-restore --staged-                  <-git pull--
```

## Щодня (уроки 04-06)
| Команда | Що робить |
|---|---|
| `git status` | що змінено і що піде в коміт |
| `git add файл` / `git add .` | вибрати в коміт |
| `git commit -m "Завд. 2: перевірка вводу"` | знімок; перший рядок ≤ 50 знаків, що змінено |
| `git log --oneline --graph --all` | історія з гілками |
| `git diff` / `git diff --staged` | що змінено / що вже в індексі |
| `git show HEAD` | останній коміт повністю |
| `.gitignore` | `.venv/` `__pycache__/` `*.pyc` `.pytest_cache/` |
| `git rm --cached -r .venv` | прибрати з git, лишити на диску |

## Гілки і конфлікт (уроки 07-08)
| Команда | Що робить |
|---|---|
| `git switch -c lr3` | нова гілка і перейти |
| `git switch main` | назад на main |
| `git merge lr3` | злити lr3 у поточну |
| `git branch -d lr3` | видалити злиту гілку |
| `git merge --abort` | скасувати злиття з конфліктом |
```
<<<<<<< HEAD          ← твоя версія
=======
>>>>>>> lr3           ← версія з гілки
```
- Конфлікт: відкрив у nano, лишив правильне, прибрав маркери, `git add файл`, `git commit`.

## GitHub (уроки 09-11, 16)
| Команда | Що робить |
|---|---|
| `git clone git@github.com:Evge14n/univer-labs.git` | скачати репо |
| `git push -u origin lr3` | перший пуш гілки |
| `git push` / `git pull` | відправити / забрати і злити |
| `git fetch` | лише забрати, не зливати |
| `gh pr create --fill` | Pull Request з гілки |
| `gh pr merge --squash --delete-branch` | злити PR |
- «rejected (fetch first)» = на GitHub є нове: `git pull`, потім `git push`.
- «Closes #3» у коміті закриває issue 3, коли коміт потрапить у main.

## Скасувати (уроки 12-13)
| Сталося | Лікування |
|---|---|
| зіпсував файл, не комітив | `git restore файл` |
| додав у індекс зайве | `git restore --staged файл` |
| помилка в останньому коміті, ще не push | `git commit --amend` або `git reset --soft HEAD~1` |
| поганий коміт уже на GitHub | `git revert хеш` (новий коміт) |
| «загубив» коміт після reset --hard | `git reflog`, потім `git reset --hard HEAD@{1}` |
| треба терміново на іншу гілку | `git stash`, потім повернувся - `git stash pop` |
- `git push --force` у спільну гілку - НІКОЛИ. Якщо дуже треба у своїй: `--force-with-lease`.

## Здача ЛР (урок 14, «Лаби в git»)
```
git switch -c lr3            (на початку лаби)
git status                   (подивись, що змінено)
git add lr3 && git commit -m "Завд. 1: ..."   (після кожного завдання з зеленим doctest)
git switch main && git merge lr3
git tag -a lr3-zdano -m "ЛР3 здано"
git push origin main lr3-zdano
```
- `--follow-tags` везе лише анотовані теги (`-a`). GitHub Pages на безкоштовному плані - лише з публічного репо.