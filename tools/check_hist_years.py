"""Звірка років і дат розділу hist з файлами-джерелами історії.

Запуск: python -P -E tools/check_hist_years.py [--dir шлях/до/content/hist]

Джерела (лише вже звірені файли):
  D:/Універ/07_Історія-України/UNI2 - модуль 2 і залік, теми, питання з відповідями.md
  D:/Універ/_У_ЗОШИТ/Історія*.md

Що перевіряє у content/hist/*.md, quiz.json, meta.json:
1. Кожен рік (4 цифри поспіль) є в джерелах.
2. Кожна повна дата (16.09.1658 або «16 вересня 1658») є в джерелах - у будь-якому з двох записів.
3. Кожна пара день.місяць без року (17.04, «2 травня») є в джерелах.
Друкує список років з кількістю згадок. Вихід 0 - 0 невідповідностей.
"""
import re
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SOURCES = [Path(r"D:\Універ\07_Історія-України\UNI2 - модуль 2 і залік, теми, питання з відповідями.md")]
SOURCES += sorted(Path(r"D:\Універ\_У_ЗОШИТ").glob("Історія*.md"))

MONTHS = ["січня", "лютого", "березня", "квітня", "травня", "червня", "липня", "серпня",
          "вересня", "жовтня", "листопада", "грудня"]
MON_RE = "|".join(MONTHS)

YEAR = re.compile(r"(?<!\d)(\d{4})(?!\d)")
NUM_DATE = re.compile(r"(?<![\d.])(\d{1,2})\.(\d{2})\.(\d{4})(?!\d)")
WORD_DATE = re.compile(rf"(?<!\d)(\d{{1,2}}) ({MON_RE}) (\d{{4}})(?!\d)")
NUM_DM = re.compile(r"(?<![\d.])(\d{1,2})\.(\d{2})(?![\d]|\.\d)")
WORD_DM = re.compile(rf"(?<!\d)(\d{{1,2}}) ({MON_RE})(?! \d{{4}})")


def clean(text):
    return text.replace("**", "")


def facts(text):
    text = clean(text)
    years = YEAR.findall(text)
    dates = {(int(d), int(m), int(y)) for d, m, y in NUM_DATE.findall(text)}
    dates |= {(int(d), MONTHS.index(m) + 1, int(y)) for d, m, y in WORD_DATE.findall(text)}
    dm = {(int(d), int(m)) for d, m in NUM_DM.findall(text) if 1 <= int(m) <= 12}
    dm |= {(int(d), MONTHS.index(m) + 1) for d, m in WORD_DM.findall(text)}
    dm |= {(d, m) for d, m, _ in dates}
    return years, dates, dm


def main():
    unit = ROOT / "content" / "hist"
    if "--dir" in sys.argv:
        unit = Path(sys.argv[sys.argv.index("--dir") + 1])
    missing_src = [p for p in SOURCES if not p.exists()]
    if missing_src or len(SOURCES) < 2:
        print("Нема файлів-джерел:", missing_src)
        return 1
    src_years, src_dates, src_dm = set(), set(), set()
    for p in SOURCES:
        y, d, dm = facts(p.read_text(encoding="utf-8"))
        src_years |= set(y)
        src_dates |= d
        src_dm |= dm
    print(f"Джерела ({len(SOURCES)}): " + "; ".join(p.name for p in SOURCES))
    print(f"У джерелах: {len(src_years)} різних років, {len(src_dates)} повних дат, {len(src_dm)} пар день.місяць")

    targets = sorted(unit.glob("*.md")) + [unit / "quiz.json", unit / "meta.json"]
    year_count = Counter()
    bad = []
    n_dates = n_dm = 0
    for f in targets:
        if not f.exists():
            bad.append(f"нема файлу {f}")
            continue
        text = f.read_text(encoding="utf-8")
        years, dates, dm = facts(text)
        year_count.update(years)
        for y in years:
            if y not in src_years:
                bad.append(f"{f.name}: рік {y} - нема в джерелах")
        for d in sorted(dates):
            n_dates += 1
            if d not in src_dates:
                bad.append(f"{f.name}: дата {d[0]}.{d[1]:02d}.{d[2]} - нема в джерелах")
        for d in sorted(dm):
            n_dm += 1
            if d not in src_dm:
                bad.append(f"{f.name}: день.місяць {d[0]}.{d[1]:02d} - нема в джерелах")

    print(f"\nРоки в розділі hist ({len(year_count)} різних, {sum(year_count.values())} згадок):")
    line = []
    for y in sorted(year_count):
        mark = "" if y in src_years else " НЕМА!"
        line.append(f"{y}×{year_count[y]}{mark}")
    for i in range(0, len(line), 10):
        print("  " + "  ".join(line[i:i + 10]))
    print(f"Повних дат перевірено {n_dates}, пар день.місяць {n_dm}")
    if bad:
        print(f"\nНЕВІДПОВІДНОСТЕЙ {len(bad)}:")
        for b in sorted(set(bad)):
            print("  ", b)
        return 1
    print("\nOK: 0 невідповідностей - кожен рік і кожна дата є у файлах-джерелах")
    return 0


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    sys.exit(main())
