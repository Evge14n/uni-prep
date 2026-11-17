"""Збирає сайт: content/<unit>/*.md -> site/data/<unit>/*.html, quiz.json, meta,
список файлів для офлайн-кешу (site/precache.json) і версію кешу в sw.js.

Запуск: python -P -E tools/build.py
"""
import hashlib
import json
import re
import sys
from pathlib import Path

import markdown

ROOT = Path(__file__).resolve().parent.parent
CONTENT = ROOT / "content"
SITE = ROOT / "site"
DATA = SITE / "data"

# сторінки розділу: файл -> назва вкладки (порядок = порядок вкладок)
PAGES = [
    ("teoriya", "Теорія"),
    ("oznachennya", "Означення і теореми"),
    ("zadachi", "Задачі"),
    ("shpargalka", "Шпаргалка"),
    ("slovnyk", "Словник"),
]

# заборонене в усьому, що бачить Євген: сирий LaTeX і довгі тире
FORBIDDEN = [
    ("$$", "LaTeX $$"),
    ("\\frac", "LaTeX frac"),
    ("\\sqrt", "LaTeX sqrt"),
    ("begin{", "LaTeX begin"),
    ("\\(", "LaTeX \\("),
    ("\\[", "LaTeX \\["),
    ("—", "довге тире"),
    ("–", "середнє тире"),
]


def check_text(text, where, errors):
    for pat, name in FORBIDDEN:
        if pat in text:
            line = text[: text.index(pat)].count("\n") + 1
            errors.append(f"{where}:{line}: {name}")


FRAC = re.compile(r"\[\[(.+?)//(.+?)\]\]")


def mini_markup(html):
    """[[чисельник // знаменник]] -> дріб у HTML (у тексті поза блоками коду)."""
    parts = re.split(r"(<pre>.*?</pre>)", html, flags=re.S)
    out = []
    for p in parts:
        if p.startswith("<pre>"):
            out.append(p)
        else:
            out.append(FRAC.sub(
                lambda m: '<span class="fr"><span>' + m.group(1).strip() + "</span><span>" + m.group(2).strip() + "</span></span>",
                p))
    return "".join(out)


def md_to_html(text):
    html = markdown.markdown(
        text,
        extensions=["tables", "fenced_code", "sane_lists", "md_in_html", "attr_list", "toc"],
        extension_configs={"toc": {"slugify": slug_uk}},
        output_format="html5",
    )
    # таблиці - у прокручуваній обгортці (щоб не було горизонтальної прокрутки сторінки)
    html = html.replace("<table>", '<div class="tw"><table>').replace("</table>", "</table></div>")
    return mini_markup(html)


def slug_uk(value, separator="-"):
    v = re.sub(r"[^\w\s-]", "", value, flags=re.U).strip().lower()
    return re.sub(r"[\s_-]+", separator, v)[:60]


def main():
    errors = []
    units = json.loads((CONTENT / "units.json").read_text(encoding="utf-8"))
    index = []
    files = []
    for uid in units:
        udir = CONTENT / uid
        if not (udir / "meta.json").exists():
            if "--strict" in sys.argv:
                errors.append(f"нема {uid}/meta.json")
            else:
                print(f"пропускаю {uid}: ще нема meta.json")
            continue
        meta = json.loads((udir / "meta.json").read_text(encoding="utf-8"))
        assert meta["id"] == uid, uid
        check_text(json.dumps(meta, ensure_ascii=False), f"{uid}/meta.json", errors)
        out = DATA / uid
        out.mkdir(parents=True, exist_ok=True)
        pages = []
        for key, title in PAGES:
            src = udir / f"{key}.md"
            if not src.exists():
                continue
            text = src.read_text(encoding="utf-8")
            check_text(text, f"{uid}/{key}.md", errors)
            html = md_to_html(text)
            (out / f"{key}.html").write_text(html, encoding="utf-8")
            files.append(f"data/{uid}/{key}.html")
            pages.append({"key": key, "title": title})
        nq = 0
        quiz = udir / "quiz.json"
        if quiz.exists():
            qtext = quiz.read_text(encoding="utf-8")
            check_text(qtext, f"{uid}/quiz.json", errors)
            qd = json.loads(qtext)
            nq = len(qd["questions"])
            (out / "quiz.json").write_text(json.dumps(qd, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
            files.append(f"data/{uid}/quiz.json")
        vids = udir / "videos.json"
        nv = 0
        if vids.exists():
            vtext = vids.read_text(encoding="utf-8")
            check_text(vtext, f"{uid}/videos.json", errors)
            vd = json.loads(vtext)
            nv = sum(len(t["videos"]) for t in vd["topics"])
            (out / "videos.json").write_text(json.dumps(vd, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
            files.append(f"data/{uid}/videos.json")
            pages.append({"key": "video", "title": "Відео"})
        if nq:
            pages.append({"key": "test", "title": "Тести"})
        meta["pages"] = pages
        meta["nq"] = nq
        meta["nv"] = nv
        index.append(meta)

    # спільні сторінки
    for key in ["plan", "glossary", "about"]:
        src = CONTENT / f"{key}.md"
        if src.exists():
            text = src.read_text(encoding="utf-8")
            check_text(text, f"{key}.md", errors)
            (DATA / f"{key}.html").write_text(md_to_html(text), encoding="utf-8")
            files.append(f"data/{key}.html")

    # календар: лише відомі дати колоквіумів і іспитів
    dj = json.loads((CONTENT / "dates.json").read_text(encoding="utf-8"))
    ics = ["BEGIN:VCALENDAR", "VERSION:2.0", "PRODID:-//uni-prep//UK", "CALSCALE:GREGORIAN", "X-WR-CALNAME:Колоквіуми і іспити"]
    for ev in dj["events"]:
        if not ev.get("date"):
            continue
        d = ev["date"].replace("-", "")
        ics += ["BEGIN:VEVENT", f"UID:{ev['id']}-{d}@uni-prep", f"DTSTAMP:{d}T000000Z", f"DTSTART;VALUE=DATE:{d}",
                f"SUMMARY:{ev['title']}", "BEGIN:VALARM", "TRIGGER:-P1D", "ACTION:DISPLAY", f"DESCRIPTION:{ev['title']}", "END:VALARM", "END:VEVENT"]
    ics.append("END:VCALENDAR")
    (SITE / "kalendar.ics").write_bytes(("\r\n".join(ics) + "\r\n").encode("utf-8"))
    files.append("kalendar.ics")

    (DATA / "units.json").write_text(json.dumps(index, ensure_ascii=False, indent=1), encoding="utf-8")
    files.append("data/units.json")

    shell = ["./", "index.html", "app.js", "style.css", "manifest.webmanifest",
             "icons/icon-192.png", "icons/icon-512.png", "icons/maskable-512.png", "icons/favicon.svg"]
    for s in shell + files:
        p = SITE / (s if s != "./" else "index.html")
        if not p.exists():
            errors.append(f"нема файлу {s}")
    for s in ["index.html", "app.js", "style.css"]:
        t = (SITE / s).read_text(encoding="utf-8")
        for ch, name in (("—", "довге тире"), ("–", "середнє тире")):
            if ch in t:
                errors.append(f"{s}: {name}")

    all_files = shell + files
    h = hashlib.sha256()
    for s in all_files:
        p = SITE / (s if s != "./" else "index.html")
        if p.exists():
            h.update(s.encode())
            h.update(p.read_bytes())
    version = h.hexdigest()[:12]
    (SITE / "precache.json").write_text(json.dumps({"version": version, "files": all_files}, ensure_ascii=False, indent=0), encoding="utf-8")
    sw = (ROOT / "tools" / "sw.template.js").read_text(encoding="utf-8")
    sw = sw.replace("__VERSION__", version).replace("__FILES__", json.dumps(all_files, ensure_ascii=False))
    (SITE / "sw.js").write_text(sw, encoding="utf-8")

    if errors:
        print("ПОМИЛКИ:")
        for e in errors:
            print("  ", e)
        sys.exit(1)
    total_q = sum(u["nq"] for u in index)
    print(f"OK: {len(index)} розділів, {len(all_files)} файлів у кеші, питань {total_q}, версія {version}")


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    main()
