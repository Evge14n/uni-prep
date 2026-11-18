"""Генератор розділу «mint» (навичка: Linux Mint - повністю), ULINUX2 18.11.2026.

Джерело - курс у D:\\Універ\\05_Програмування\\Linux-Mint\\ (його пише ULINUX2):
  «Урок NN - ...md»                          → content/mint/pages/urok-NN.md (сторінки у вкладці «Уроки»)
  таблиця уроків                              → content/mint/uroky.md
  00 «Почни тут» + «Вище за університет»      → content/mint/teoriya.md
  «Практика», «зламані програми», «Іспит»     → content/mint/zadachi.md
  _У_ЗОШИТ\\Linux Mint - шпаргалка.md         → content/mint/shpargalka.md
  _джерело/quiz.json                          → content/mint/quiz.json (поле sh лишається для --mint)
  ustanovka-mint.sh                           → site/files/ustanovka-mint.sh (wget на ноутбук)

Запуск:
    python -P -E tools/gen_mint.py                - записати файли розділу
    python -P -E tools/gen_mint.py --check [файл] - звірити quiz.json (або копію) з джерелом
    python -P -E tools/gen_mint.py --mint         - прогнати в тестовій Linux Mint 22.3 (WSL Mint22) команди питань з sh
"""
import json
import re
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "content" / "mint"
COURSE = Path(r"D:\Універ\05_Програмування\Linux-Mint")
SHPARG = Path(r"D:\Універ\_У_ЗОШИТ\Linux Mint - шпаргалка.md")
NAMES_FILE = Path(r"D:\Універ\00_Загальне\_імена-не-на-сайт.txt")
SANITIZE = [
    (r"\b[^\W\d_]+_[^\W\d_]+_[^\W\d_]+-\d+_20\d\d\b", "Прізвище_Імʼя_Група_2026"),
    (r'(git config --global user\.name )"[^"]*"', r'\1"Твоє Імʼя Прізвище"'),
]


def private_names() -> list:
    if not NAMES_FILE.exists():
        return []
    return [w.strip() for w in re.split(r"[,\n]", NAMES_FILE.read_text(encoding="utf-8"))
            if len(w.strip()) >= 4 and not w.strip().startswith("#")]


def clean(s: str) -> str:
    for a, b in SANITIZE:
        s = re.sub(a, b, s)
    for w in private_names():
        s = re.sub(r"\b" + re.escape(w) + r"[а-яіїєґʼ']*", "Прізвище", s)
    s = s.replace("<details><summary>", '<details markdown="1"><summary>')
    return s


def body(md: str, shift: bool = True) -> str:
    """Без заголовка # і (якщо shift) з заголовками на рівень нижче."""
    lines = md.splitlines()
    if lines and lines[0].startswith("# "):
        lines = lines[1:]
    out, fence = [], False
    for ln in lines:
        if ln.startswith("```"):
            fence = not fence
        if shift and not fence and re.match(r"#{2,5} ", ln):
            ln = "#" + ln
        out.append(ln)
    return "\n".join(out).strip() + "\n"


def lessons() -> list:
    return sorted(COURSE.glob("Урок [0-9][0-9] - *.md"))


def first_line_info(p: Path):
    t = p.read_text(encoding="utf-8")
    h = t.splitlines()[0]
    m = re.match(r"# Урок (\d\d)\. (.*?) \(([^()]*хв[^()]*)\)\s*$", h)
    title, time = (m.group(2), m.group(3)) if m else (p.stem.split(" - ", 1)[1], "")
    why = re.search(r"\*\*Навіщо:\*\*\s*(.*?)(?:\n\n|\n## )", t, flags=re.S)
    why = re.sub(r"\s+", " ", why.group(1)).strip() if why else ""
    return title, time, why


def build_pages() -> dict:
    res = {}
    rows = ["Курс для ноутбука зі **справжньою Linux Mint 22.x** (Cinnamon). Спершу - те, що потрібно для лаб: знімок системи,",
            "оновлення, термінал, ЛР1 з нуля без VS Code, налагодження; далі лаби ЛР2-ЛР7 і вся система по уроку на день.",
            "Кожну команду курсу прогнано в тестовій Linux Mint 22.3 (офіційний образ команди Mint + пакети з репозиторію",
            "Mint), понад тисячу перевірок, 18.11.2026. Як почати - вкладка «Теорія», розділ «Почни тут».",
            "",
            "| Урок | Що вмітимеш | Час |", "|---|---|---|"]
    for p in lessons():
        n = p.name[5:7]
        title, time, why = first_line_info(p)
        rows.append(f"| [{int(n)}. {title}](#/u/mint/urok-{n}) | {why} | {time} |")
        page = [f"# Урок {n}. {title}", "", f"[← Усі уроки](#/u/mint/uroky)", "",
                body(p.read_text(encoding="utf-8"), shift=False)]
        res[f"pages/urok-{n}.md"] = clean("\n".join(page))
    rows += ["", "Ще: «Задачі» - 7 зламаних програм для тренування налагодження, 4 практичні завдання з розвʼязками і "
             "іспит на 60 питань; «Шпаргалка» - на одну сторінку; «Тести» - самоперевірка з відповідями.", ""]
    res["uroky.md"] = clean("\n".join(rows))
    start = (COURSE / "00 - Почни тут.md").read_text(encoding="utf-8")
    vyshche = next(COURSE.glob("ВИЩЕ ЗА УНІВЕРСИТЕТ*.md")).read_text(encoding="utf-8")
    prog = (COURSE / "ПРОГРАМА.md").read_text(encoding="utf-8")
    res["teoriya.md"] = clean("\n".join([
        "# Linux Mint - повністю", "",
        "## Почни тут", "", body(start),
        "## Вище за університет: досвід практиків", "", body(vyshche),
        '<details markdown="1"><summary>Програма курсу: звірка з MIT, Cambridge, Stanford, Berkeley, LPI, ЛНУ, КПІ</summary>', "",
        body(prog), "", "</details>", ""]))
    zl = COURSE / "Налагодження - зламані програми"
    bugs = ["## Тренування: 7 зламаних програм", "",
            "Збережи кожну програму у файл з такою ж назвою (наприклад `nano bug_1.py`, встав, Ctrl+O, Enter, Ctrl+X) і шукай",
            "помилку способом, який підказує завдання (уроки 05-06).", ""]
    for f in sorted(zl.glob("bug_*.py")):
        bugs += [f'<details markdown="1"><summary>{f.name}</summary>', "", "```python",
                 f.read_text(encoding="utf-8").rstrip(), "```", "", "</details>", ""]
    bugs += [body((zl / "ЗАВДАННЯ.md").read_text(encoding="utf-8"))]
    prak = next(COURSE.glob("Практика - 4 завдання.md")).read_text(encoding="utf-8")
    exam = (COURSE / "ІСПИТ-САМОПЕРЕВІРКА.md").read_text(encoding="utf-8")
    res["zadachi.md"] = clean("\n".join(["# Задачі, практика й іспит", ""] + bugs +
                                        ["## Практика: 4 завдання як у справжній роботі", "", body(prak),
                                         "## Іспит-самоперевірка: 60 питань", "", body(exam)]))
    sh = SHPARG.read_text(encoding="utf-8")
    res["shpargalka.md"] = clean("\n".join(ln for ln in sh.splitlines() if not ln.startswith("→")))
    return res


META = {
    "id": "mint",
    "title": "Навичка - Linux Mint повністю (ноутбук)",
    "kind": "skill",
    "subject": "Linux Mint 22.x: система, термінал, лаби з Python без VS Code, налагодження, оновлення, порятунок",
    "date": "без дати - по уроку на день у своєму темпі; першими уроки 01-06",
    "points": "Балів не дає. Потрібно, щоб упевнено працювати на своєму ноутбуці і робити лаби в терміналі",
    "format": "27 уроків: тема, вправи руками в терміналі Mint, «передбач, потім запусти», 5 питань самоперевірки; "
              "7 зламаних програм, 4 практичні завдання, іспит на 60 питань.",
    "include": [],
    "test": {"timer": 15, "count": 15,
             "note": "самоперевірка за курсом; частину відповідей перевірено запуском команд у Linux Mint 22.3"},
}


def load_quiz() -> list:
    src = COURSE / "_джерело" / "quiz.json"
    if not src.exists():
        return []
    qs = []
    for q in json.loads(src.read_text(encoding="utf-8")):
        q = dict(q)
        if "sh" in q:
            q["_sh"] = q.pop("sh")
        qs.append(q)
    return qs


def scrub(v):
    if isinstance(v, str):
        return clean(v)
    if isinstance(v, list):
        return [scrub(x) for x in v]
    return v


def unticks(k, v):
    """Сайт і бот показують q/explain/options як текст - без сирих бектиків."""
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
            errs.append(f"{q['id']}: тип {q['type']} - тут лише single/short")
        for k in ("q", "explain"):
            if "\u2014" in q.get(k, "") or "\u2013" in q.get(k, ""):
                errs.append(f"{q['id']}: довге/середнє тире в {k}")
    blob = path.read_text(encoding="utf-8")
    for f in list(path.parent.glob("*.md")) + list((path.parent / "pages").glob("*.md")):
        blob += f.read_text(encoding="utf-8")
    for w in private_names():
        if re.search(r"\b" + re.escape(w), blob):
            errs.append(f"на сайт іде приватне імʼя (з {NAMES_FILE.name})")
    for bad in ("Моє-Python", "WSL", "PowerShell"):
        if bad in blob:
            errs.append(f"на сайті «{bad}»")
    return errs


def mint_check() -> list:
    """Кожен sh - у власній порожній теці тестової Mint 22.3 (WSL Mint22); stdout == очікуване."""
    items = [q for q in load_quiz() if "_sh" in q]
    lines = ["#!/bin/bash", "export LANG=C.UTF-8 LC_ALL=C.UTF-8", "B=$(mktemp -d -p ~/.cache gmint.XXXX)"]
    for q in items:
        qid = q["id"]
        lines += [f"mkdir -p \"$B/{qid}\"", f"echo '@@{qid}'", f"( cd \"$B/{qid}\" && {q['_sh'][0]} ) 2>/dev/null"]
    lines += ["cd ~ && rm -rf \"$B\""]
    with tempfile.NamedTemporaryFile("w", suffix=".sh", delete=False, encoding="utf-8", newline="\n") as f:
        f.write("\n".join(lines) + "\n")
        p = f.name
    wp = "/mnt/" + p[0].lower() + p[2:].replace("\\", "/")
    r = subprocess.run(["wsl.exe", "-d", "Mint22", "--", "bash", wp], capture_output=True, timeout=600)
    out = r.stdout.decode("utf-8", "replace")
    got = {}
    for chunk in out.split("@@")[1:]:
        qid, _, rest = chunk.partition("\n")
        got[qid.strip()] = rest.rstrip("\n")
    errs = [f"{q['id']}: чекав {q['_sh'][1]!r}, Mint дала {got.get(q['id'])!r}"
            for q in items if got.get(q["id"]) != q["_sh"][1]]
    print(f"Mint 22.3: {len(items) - len(errs)} з {len(items)} команд дали очікуване")
    return errs


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    if "--check" in sys.argv:
        i = sys.argv.index("--check")
        path = Path(sys.argv[i + 1]) if len(sys.argv) > i + 1 else OUT / "quiz.json"
        errs = check(path)
        print("\n".join(errs) if errs else f"OK: {len(load_quiz())} питань збігаються з джерелом")
        sys.exit(1 if errs else 0)
    if "--mint" in sys.argv:
        errs = mint_check()
        print("\n".join(errs))
        sys.exit(1 if errs else 0)
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "pages").mkdir(exist_ok=True)
    for name, text in build_pages().items():
        (OUT / name).write_text(text, encoding="utf-8", newline="\n")
    (OUT / "meta.json").write_text(json.dumps(META, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    qs = load_quiz()
    (OUT / "quiz.json").write_text(json.dumps({"questions": quiz(qs)}, ensure_ascii=False, indent=1) + "\n",
                                   encoding="utf-8")
    files = ROOT / "site" / "files"
    files.mkdir(exist_ok=True)
    (files / "ustanovka-mint.sh").write_bytes((COURSE / "ustanovka-mint.sh").read_bytes().replace(b"\r\n", b"\n"))
    errs = check(OUT / "quiz.json")
    print(f"mint: {len(list(lessons()))} уроків, {len(qs)} питань, з них {sum(1 for q in qs if '_sh' in q)} "
          f"з перевіркою в Mint; " + ("OK" if not errs else "; ".join(errs)))


if __name__ == "__main__":
    main()
