"""UPROGONE: жодного битого посилання - усі href на сайті, у картках бота і в графіку.

  python -P -E tools/links_check.py

Перевіряє (без браузера, за зібраним site/):
- кожне `href="#/..."` у site/data/**/*.html і в app.js-шаблонах не веде в нікуди: розділ є, сторінка є
  (файл data/<розділ>/<сторінка>.html або вкладка test/video), якір (#/u/р/с/<якір>) є в цій сторінці,
  режим тесту відомий (m/k - модуль існує і має питання), відео графіка (#/video/<id>) є в grafik.json;
- старі адреси розділів-частин (mint, git, linux, prog-sec) перенаправляються на існуючі сторінки;
- посилання карток бота (D:/Універ/00_Загальне/_картки.json, поле site) і пунктів графіка (site);
- href на файли (data/..., files/...) існують.
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SITE = ROOT / "site"
DATA = SITE / "data"
CARDS = Path(r"D:\Універ\00_Загальне\_картки.json")
MODES = {"real", "train", "recall", "wrong", "topics"}
TOP = {"", "subjects", "plan", "glossary", "about", "stats", "grafik", "video", "w"}

units = {u["id"]: u for u in json.loads((DATA / "units.json").read_text(encoding="utf-8"))}
grafik = json.loads((DATA / "grafik.json").read_text(encoding="utf-8"))["units"] if (DATA / "grafik.json").exists() else {}
moduli = json.loads((DATA / "prog" / "moduli.json").read_text(encoding="utf-8"))
ids_cache = {}


def page_ids(unit, page):
    k = (unit, page)
    if k not in ids_cache:
        p = DATA / unit / f"{page}.html"
        ids_cache[k] = set(re.findall(r'id="([^"]+)"', p.read_text(encoding="utf-8"))) if p.exists() else None
    return ids_cache[k]


def resolve(h, depth=0):
    """Повертає None, якщо адреса веде на існуючий екран, або текст проблеми."""
    h = h.split("?")[0]
    parts = h.lstrip("#").lstrip("/").split("/")
    top = parts[0]
    if top == "u":
        if len(parts) < 2 or parts[1] not in units:
            return "нема розділу"
        u = units[parts[1]]
        page = parts[2] if len(parts) > 2 else ""
        if u.get("parent"):
            if depth:
                return "перенаправлення по колу"
            to = u["moved"].get(page) or u["moved"].get("")
            if page and page not in u["moved"]:
                to = u["moved"][""]  # невідомий старий ключ - на покажчик частини
            return resolve(f"#/u/{u['parent']}/{to}", depth + 1)
        if not page:
            return None
        if page == "test":
            return None if u.get("nq") else "вкладка Тести без питань"
        if page == "video":
            return None if u.get("nv") else "вкладка Відео без відео"
        ids = page_ids(u["id"], page)
        if ids is None:
            return f"нема сторінки data/{u['id']}/{page}.html"
        if len(parts) > 3 and parts[3] and parts[3] not in ids:
            return f"нема якоря {parts[3]} у {page}"
        return None
    if top == "q":
        if len(parts) < 2 or parts[1] not in units:
            return "тест: нема розділу"
        mode = parts[2] if len(parts) > 2 else "train"
        m = re.fullmatch(r"([mk])(\d+)", mode)
        if m:
            if parts[1] != "prog":
                return "тест модуля лише в prog"
            mm = next((x for x in moduli["modules"] if x["n"] == int(m.group(2))), None)
            return None if mm and mm["keys"] else "модуля нема або без питань"
        return None if mode in MODES else f"невідомий режим {mode}"
    if top == "video":
        return None if len(parts) < 2 or not parts[1] or parts[1] in grafik else f"нема пункту графіка {parts[1]}"
    if top == "w":
        return None if len(parts) > 1 and parts[1] in ("week", "month") else "тест тижня: невідомий вид"
    return None if top in TOP else f"невідомий маршрут {top}"


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    bad, n = [], 0
    for f in sorted(DATA.rglob("*.html")):
        text = f.read_text(encoding="utf-8")
        for h in re.findall(r'href="(#/[^"]*)"', text):
            n += 1
            r = resolve(h)
            if r:
                bad.append(f"{f.relative_to(SITE)}: {h} - {r}")
        for h in re.findall(r'href="((?:data|files|py)/[^"#]+)"', text):
            n += 1
            if not (SITE / h).exists():
                bad.append(f"{f.relative_to(SITE)}: {h} - файлу нема")
    # сталі адреси в коді сайту (без шаблонних ${...})
    js = (SITE / "app.js").read_text(encoding="utf-8")
    for h in sorted(set(re.findall(r'href="(#/[^"$`]*)"', js))):
        n += 1
        r = resolve(h)
        if r:
            bad.append(f"app.js: {h} - {r}")
    # старі адреси частин
    old = 0
    for u in units.values():
        if u.get("parent"):
            for key in list(u["moved"]) + ["невідома-сторінка"]:
                old += 1
                r = resolve(f"#/u/{u['id']}/{key}" if key else f"#/u/{u['id']}")
                if r:
                    bad.append(f"стара адреса #/u/{u['id']}/{key}: {r}")
    # картки бота і графік
    nc = 0
    if CARDS.exists():
        cj = json.loads(CARDS.read_text(encoding="utf-8"))
        for c in cj["cards"]:
            s = c.get("site")
            if s and s.startswith("#/"):
                nc += 1
                r = resolve(s)
                if r:
                    bad.append(f"картка {c['id']}: {s} - {r}")
    ng = 0
    for gid, g in grafik.items():
        s = g.get("site")
        if s:
            ng += 1
            r = resolve(s)
            if r:
                bad.append(f"графік {gid}: {s} - {r}")
    print(f"посилань на сторінках і в коді {n}, старих адрес {old}, карток бота {nc}, пунктів графіка з посиланням {ng}")
    if bad:
        print(f"БИТИХ: {len(bad)}")
        for b in bad[:60]:
            print("  ", b)
        sys.exit(1)
    print("OK: битих посилань нема")


if __name__ == "__main__":
    main()
