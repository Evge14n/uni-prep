# Схема розділу «Програмування» (UPROGONE, 18.11.2026)

Один розділ замість п'яти: Python (`prog`), Linux Mint (`mint`), Git (`git`), безпечний код (`prog-sec`),
Linux у WSL (`linux`). На сайті є лише `#/u/prog`; решта - **частини**: їхні теки в `content/` лишились
джерелами з власними генераторами (`tools/gen_<частина>.py`), але окремих розділів у «Предметах» нема.

## Що НЕ міняти (бот і статистика)
- `content/<частина>/quiz.json` і **id питань** - бот UniNagad будує картки за id, сайт зберігає відповіді
  як `<частина>/<id>`. Нові питання - лише дописувати з новими id.
- Імена тек частин і назви файлів уроків курсів (`Урок NN - ...md`) - графік UPLAN1 і генератори частин.

## Куди класти новий зміст
| Що | Куди | Як потрапить на сайт |
|---|---|---|
| урок Python | `content/prog/pages/urok-NN.md` (з курсу `Курс/`, `tools/build_kurs`) | сторінка `#/u/prog/urok-NN`, вкладка «Уроки Python» |
| урок Linux Mint | курс `Linux-Mint/Урок NN - ...md` → `tools/gen_mint.py` → `content/mint/pages/urok-NN.md` | `#/u/prog/mint-NN` |
| урок Git | курс `Git-GitHub/` → `tools/gen_git.py` → `content/git/teoriya.md` («## Тема N.») | `#/u/prog/git-NN` (build.py ріже теорію за «## Тема N.») |
| тема безпеки | `content/prog-sec/teoriya.md` («## Тема N.») | `#/u/prog/sec-NN` |
| день Linux у WSL | `content/linux/teoriya.md` («## Тема N.») | `#/u/prog/linux-NN` |
| задачі, практика, іспит частини | `content/<частина>/zadachi.md` | `#/u/prog/<префікс>-zadachi` |
| шпаргалка частини | `content/<частина>/shpargalka.md` | `#/u/prog/<префікс>-shpargalka` + вкладка «Шпаргалки» |
| розбір лаби з підказками (без готового коду) | `content/prog/pages/lab-N.md` або генератор | `#/u/prog/lab-N` |
| **у якому модулі урок** | `content/prog/moduli.json` | модулі `#/u/prog/m1` ... `m8`, «Шлях», «Усе» |

Префікси частин: `mint`, `git`, `sec` (prog-sec), `linux` - у `content/prog/meta.json` → `parts`.

## Модулі (`content/prog/moduli.json`)
Модуль = лаба (1-7) + «після ЛР7» (8). Кроки по порядку: відео (пункти графіка `videos`) → урок Python
(`python`, `python_repeat`) → Linux Mint і Git для цієї лаби (`mint`, `git`, `linux_alt`) → лаба в терміналі
(`lab_mint`, `lab_page`) → налагодження (`debug_mint`, `bug`) → безпечний код (`sec`, `sec_tasks`) →
картки й тест модуля (питання за темами: `quiz_prog`, `quiz_sec`; Mint/Git/Linux - за номером уроку в темі «NN. ...»).
`mint_extra` - уроки Mint «за бажанням» цього тижня.

**Новий урок у частині = рядок у moduli.json**, інакше збирання впаде: `tools/gen_prog_path.py` вимагає, щоб
кожен урок і кожне питання частин були рівно в одному модулі.

## Перевірки (усе зелене перед пушем)
```
python -P -E tools/gen_<частина>.py           # якщо міняв частину
python -P -E tools/build.py                   # сам запускає gen_prog_path.py
python -P -E tools/verify_quizzes.py
python -P -E tools/links_check.py             # жодного битого посилання, старі адреси, картки бота, графік
python -X utf8 -E tools/prog_one_e2e.py       # розділ на 390/1440, перенаправлення, тести модулів, офлайн
python -X utf8 -E tools/e2e.py
```
Старі адреси (`#/u/mint/urok-05`, `#/u/git/test`, ...) сайт перенаправляє за `units.json` → `moved`
(будує `tools/build.py`), посилання в Markdown build.py переписує на нові сам.
