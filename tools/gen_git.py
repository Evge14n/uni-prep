"""Генератор розділу «git» (навичка: Git і GitHub у терміналі Linux Mint), UGIT1 18.11.2026.

Джерело - курс у D:\\Універ\\05_Програмування\\Git-GitHub\\ (його пише UGIT1):
  00 + уроки 01-17 + «Лаби в git» → content/git/teoriya.md
  «Практика - 4 завдання» + «ІСПИТ-САМОПЕРЕВІРКА» → content/git/zadachi.md
  _У_ЗОШИТ\\Git - шпаргалка.md → content/git/shpargalka.md
  _джерело/quiz/*.json → content/git/quiz.json (поле sh прибирається, лишається для --wsl)

Запуск:
    python -P -E tools/gen_git.py                 - записати файли розділу
    python -P -E tools/gen_git.py --check [файл]  - звірити quiz.json (або копію) з джерелом
    python -P -E tools/gen_git.py --wsl           - прогнати в Ubuntu (WSL) команди питань з полем sh
                                                    (порожня тека, чистий HOME з git config як в уроці 02)
"""
import json
import re
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "content" / "git"
COURSE = Path(r"D:\Універ\05_Програмування\Git-GitHub")
SHPARG = Path(r"D:\Універ\_У_ЗОШИТ\Git - шпаргалка.md")

# на публічний сайт не йдуть ПІБ і група (шаблонами, щоб самих імен не було в коді публічного репо)
# список імен - локальний файл поза репо (як у gen_zfp.py); імʼя студента → «Імʼя», решта → «Прізвище»
NAMES_FILE = Path(r"D:\Універ\00_Загальне\_імена-не-на-сайт.txt")
# латинське імʼя для git config береться з локальної перевірки курсу (who_am_i у run.sh), не з коду репо
RUN_SH = COURSE / "_перевірка" / "run.sh"


def git_user() -> str:
    m = re.search(r'git config --global user\.name "([^"]+)"', RUN_SH.read_text(encoding="utf-8"))
    return m.group(1) if m else "Student"


GIT_USER = git_user()
SANITIZE = [
    (r"\b[^\W\d_]+_[^\W\d_]+_[^\W\d_]+-\d+_20\d\d", "Прізвище_Імʼя_Група_2026"),
    (re.escape(GIT_USER), "Твоє Імʼя"),
    (r"\b" + re.escape(GIT_USER.split()[0]) + r"\b", "Імʼя"),
]


def private_names() -> list:
    if not NAMES_FILE.exists():
        return []
    return [w.strip() for w in re.split(r"[,\n]", NAMES_FILE.read_text(encoding="utf-8")) if w.strip()]


def lessons() -> list:
    return sorted(COURSE.glob("Урок [0-9][0-9] - *.md"))


def lesson_title(p: Path) -> str:
    return p.stem.split(" - ", 1)[1]


def topic_of(src_file: str) -> str:
    """u08 → «08. Конфлікт і як розвʼязати руками»; laby → «Лаби в git»."""
    if src_file == "laby":
        return "18. Лаби в git - univer-labs"
    n = src_file[1:]
    for p in lessons():
        if p.name.startswith(f"Урок {n} "):
            return f"{n}. {lesson_title(p)}"
    raise SystemExit(f"нема уроку для {src_file}")


def load_quiz() -> list:
    qs = []
    for f in sorted((COURSE / "_джерело" / "quiz").glob("*.json")):
        top = topic_of(f.stem)
        for q in json.loads(f.read_text(encoding="utf-8")):
            q = dict(q)
            q["topic"] = top
            if "sh" in q:
                q["_sh"] = q.pop("sh")
            qs.append(q)
    return qs


def clean(s: str) -> str:
    for a, b in SANITIZE:
        s = re.sub(a, b, s)
    for w in private_names():
        s = re.sub(r"\b" + re.escape(w) + r"[а-яіїєґʼ']*", "Імʼя" if w.endswith("ген") else "Прізвище", s)
    s = s.replace("<details><summary>", '<details markdown="1"><summary>')
    return s


def body(md: str) -> str:
    """Без заголовка # і з заголовками на рівень нижче (## → ###)."""
    lines = md.splitlines()
    if lines and lines[0].startswith("# "):
        lines = lines[1:]
    out, fence = [], False
    for ln in lines:
        if ln.startswith("```") or ln.startswith("~~~"):
            fence = not fence
        if not fence and re.match(r"#{2,5} ", ln):
            ln = "#" + ln
        out.append(ln)
    return "\n".join(out).strip() + "\n"


def build_pages() -> dict:
    start = (COURSE / "00 - Почни тут.md").read_text(encoding="utf-8")
    teor = ["# Git і GitHub з нуля - у терміналі Linux Mint",
            "",
            "17 уроків по 15-20 хв: 5 хв прочитати, 10 хв зробити руками в терміналі, 5 питань самоперевірки.",
            "Кожну команду курсу прогнано скриптом у справжньому git 2.43.0 (Ubuntu 24.04 і Linux Mint 22.3)",
            "на тимчасових репозиторіях, конфлікти й порятунок через reflog - справжні (18.11.2026).",
            "",
            "## Тема 0. Почни тут: план, як вчитися, пісочниця",
            "",
            body(start)]
    for p in lessons():
        n = p.name[5:7]
        teor += [f"## Тема {int(n)}. {lesson_title(p)}", "", body(p.read_text(encoding="utf-8"))]
    laby = next(COURSE.glob("Лаби в git*.md"))
    teor += ["## Тема 18. Лаби в git - univer-labs покроково", "", body(laby.read_text(encoding="utf-8"))]
    prak = next(COURSE.glob("Практика*.md")).read_text(encoding="utf-8")
    exam = (COURSE / "ІСПИТ-САМОПЕРЕВІРКА.md").read_text(encoding="utf-8")
    qpart, apart = re.split(r"^## Відповіді\s*$", exam, maxsplit=1, flags=re.M)
    zad = ["# Практика і підсумковий іспит", "",
           "## Чотири завдання як у справжній роботі", "", body(prak),
           "## Іспит-самоперевірка: 20 питань", "", body(qpart),
           '<details markdown="1"><summary>Відповіді</summary>', "", body("# x\n" + apart), "", "</details>", ""]
    sh = SHPARG.read_text(encoding="utf-8")
    sh = "\n".join(ln for ln in sh.splitlines() if not ln.startswith("→"))
    return {"teoriya.md": clean("\n".join(teor)), "zadachi.md": clean("\n".join(zad)), "shpargalka.md": clean(sh)}


META = {
    "id": "git",
    "title": "Навичка - Git і GitHub (термінал, Linux Mint)",
    "kind": "skill",
    "subject": "Git і GitHub для лаб: коміти, гілки, конфлікти, Pull Request, порятунок через reflog",
    "date": "без дати - вчи по 15-20 хв на день у своєму темпі",
    "points": "Балів не дає. Потрібно, щоб лаби не губились і щоб здавати їх посиланням або архівом з тегу",
    "format": "17 уроків по 15-20 хв: тема, вправи руками в терміналі (пісочниця pisochnytsia), 5 питань самоперевірки; "
              "далі «Лаби в git», 4 практичні завдання й іспит на 20 питань.",
    "include": [],
    "test": {"timer": 15, "count": 15,
             "note": "самоперевірка за курсом; більш як половину відповідей перевірено запуском git 2.43 в Ubuntu"},
}


def scrub(v):
    """Ті самі заміни імен, що й у тексті, для полів тесту (рядки, списки)."""
    if isinstance(v, str):
        for a, b in SANITIZE:
            v = re.sub(a, b, v)
        for w in private_names():
            v = re.sub(r"\b" + re.escape(w) + r"[а-яіїєґʼ']*", "Імʼя" if w.endswith("ген") else "Прізвище", v)
        return v
    if isinstance(v, list):
        return [scrub(x) for x in v]
    return v


def unticks(k, v):
    """Сайт (rich() в app.js) і бот показують q/explain/options як текст: `код` дав би сирі бектики (видно на 390 px)."""
    if k in ("q", "explain", "options"):
        if isinstance(v, list):
            return [re.sub(r"`([^`]+)`", r"\1", x) for x in v]
        return re.sub(r"`([^`]+)`", r"\1", v)
    return v


def quiz(qs=None) -> list:
    return [{k: unticks(k, scrub(v)) for k, v in q.items() if not k.startswith("_")} for q in (qs or load_quiz())]


def check(path: Path) -> list:
    errs = []
    qs = load_quiz()
    data = json.loads(path.read_text(encoding="utf-8"))["questions"]
    want = {q["id"]: q for q in quiz(qs)}
    got = {q["id"]: q for q in data}
    if set(want) != set(got):
        errs.append(f"різні id: {sorted(set(want) ^ set(got))}")
    for i, q in want.items():
        g = got.get(i)
        if g and json.dumps(g, sort_keys=True, ensure_ascii=False) != json.dumps(q, sort_keys=True, ensure_ascii=False):
            errs.append(f"{i}: quiz.json не збігається з джерелом курсу")
    ids = [q["id"] for q in qs]
    if len(ids) != len(set(ids)):
        errs.append("повтор id")
    for q in qs:
        if q["type"] == "single":
            if not isinstance(q["answer"], int) or not (0 <= q["answer"] < len(q["options"])) \
                    or len(set(q["options"])) != len(q["options"]):
                errs.append(f"{q['id']}: answer не індекс варіанта або повтор варіанта")
        elif q["type"] == "short":
            if q["answer"] not in q["accept"]:
                errs.append(f"{q['id']}: answer нема в accept")
        else:
            errs.append(f"{q['id']}: тип {q['type']} - сайт знає лише single/short тут")
        for k in ("q", "explain"):
            if "\u2014" in q.get(k, "") or "\u2013" in q.get(k, ""):
                errs.append(f"{q['id']}: довге/середнє тире в {k}")
    blob = path.read_text(encoding="utf-8")
    for f in ("teoriya.md", "zadachi.md", "shpargalka.md"):
        if (path.parent / f).exists():
            blob += (path.parent / f).read_text(encoding="utf-8")
    for w in private_names() + [GIT_USER]:
        if re.search(r"\b" + re.escape(w), blob):
            errs.append(f"на сайт іде приватне імʼя (з {NAMES_FILE.name})")
    return errs


def wsl_check() -> list:
    """Кожен sh - у власній порожній теці Ubuntu з чистим HOME і git config як в уроці 02; stdout == очікуване."""
    items = [q for q in load_quiz() if "_sh" in q]
    lines = ["#!/bin/bash", "export LANG=C.UTF-8 LC_ALL=C.UTF-8 LANGUAGE= GIT_EDITOR=true GIT_CONFIG_NOSYSTEM=1",
             "B=$(mktemp -d -p ~/.cache ggit.XXXX)"]
    for q in items:
        cmd, _ = q["_sh"]
        qid = q["id"]
        lines += [f"mkdir -p \"$B/{qid}/h\" \"$B/{qid}/w\"",
                  f"echo '@@{qid}'",
                  "( export HOME=\"$B/" + qid + "/h\"; cd \"$B/" + qid + "/w\"; "
                  f"git config --global user.name '{GIT_USER}'; "
                  "git config --global user.email '128326252+Evge14n@users.noreply.github.com'; "
                  "git config --global init.defaultBranch main; git config --global pull.rebase false; "
                  "git config --global core.quotepath false; "
                  "git config --global log.decorate short; "  # як у терміналі: ярлики (HEAD -> main)
                  f"( {cmd} ) 2>/dev/null )"]
    lines += ["cd ~ && rm -rf \"$B\""]
    with tempfile.NamedTemporaryFile("w", suffix=".sh", delete=False, encoding="utf-8", newline="\n") as f:
        f.write("\n".join(lines) + "\n")
        p = f.name
    wp = subprocess.run(["wsl.exe", "-d", "Ubuntu", "--", "wslpath", "-u", p.replace("\\", "/")],
                        capture_output=True, text=True).stdout.strip()
    r = subprocess.run(["wsl.exe", "-d", "Ubuntu", "--cd", "~", "--", "bash", wp], capture_output=True, timeout=600)
    out = r.stdout.decode("utf-8", "replace")
    got = {}
    for chunk in out.split("@@")[1:]:
        qid, _, rest = chunk.partition("\n")
        got[qid.strip()] = rest.rstrip("\n")
    errs = []
    for q in items:
        exp = q["_sh"][1]
        if got.get(q["id"]) != exp:
            errs.append(f"{q['id']}: чекав {exp!r}, Ubuntu дала {got.get(q['id'])!r}")
    print(f"WSL: {len(items) - len(errs)} з {len(items)} команд дали очікуване")
    return errs


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    if "--check" in sys.argv:
        i = sys.argv.index("--check")
        path = Path(sys.argv[i + 1]) if len(sys.argv) > i + 1 else OUT / "quiz.json"
        errs = check(path)
        print("\n".join(errs) if errs else f"OK: {len(load_quiz())} питань збігаються з джерелом")
        sys.exit(1 if errs else 0)
    if "--wsl" in sys.argv:
        errs = wsl_check()
        print("\n".join(errs))
        sys.exit(1 if errs else 0)
    OUT.mkdir(parents=True, exist_ok=True)
    for name, text in build_pages().items():
        (OUT / name).write_text(text, encoding="utf-8", newline="\n")
    (OUT / "meta.json").write_text(json.dumps(META, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    qs = load_quiz()
    (OUT / "quiz.json").write_text(json.dumps({"questions": quiz(qs)}, ensure_ascii=False, indent=1) + "\n",
                                   encoding="utf-8")
    errs = check(OUT / "quiz.json")
    print(f"git: {len(qs)} питань, з них {sum(1 for q in qs if '_sh' in q)} з перевіркою в Ubuntu; "
          + ("OK" if not errs else "; ".join(errs)))


if __name__ == "__main__":
    main()
