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
    ("uroky", "Уроки"),  # UNIPROG1: курс програмування з нуля (лише prog)
    ("teoriya", "Теорія"),
    ("oznachennya", "Означення і теореми"),
    ("zadachi", "Задачі"),
    ("shpargalka", "Шпаргалка"),
    ("dovidnyk", "Довідник"),  # UNIPROG1: довідник функцій (лише prog)
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
    # ULINUX2: у .md LaTeX шукаємо поза кодом - `\(` у bash (grep 'str\(', назва файлу з дужками) не LaTeX
    plain = re.sub(r"```.*?```", lambda m: "\n" * m.group(0).count("\n"), text, flags=re.S)
    plain = re.sub(r"``[^\n]+?``", "", plain)  # ``код з ` усередині``
    plain = re.sub(r"`[^`\n]*`", "", plain)
    for pat, name in FORBIDDEN:
        src = plain if (name.startswith("LaTeX") and where.endswith(".md")) else text
        if pat in src:
            line = src[: src.index(pat)].count("\n") + 1
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


# ---------- UPROGONE: частини одного розділу (mint, git, linux, prog-sec живуть у prog) ----------
def split_themes(text, prefix):
    """Великий teoriya.md частини -> покажчик (вступ, Тема 0, інші ##) + сторінка на кожну «## Тема N.»."""
    chunks = {prefix: []}
    cur = prefix
    fence = False
    for ln in text.split("\n"):
        if re.match(r"^\s*(```|~~~)", ln):
            fence = not fence
        elif not fence and ln.startswith("## "):
            m = re.match(r"^## Тема (\d+)\. ", ln)
            cur = prefix if (not m or int(m.group(1)) == 0) else f"{prefix}-{int(m.group(1)):02d}"
            chunks.setdefault(cur, [])
            if cur != prefix:
                ln = "# " + ln[3:]
        chunks[cur].append(ln)
    return {k: "\n".join(v).strip() + "\n" for k, v in chunks.items()}


def part_pages(pid, cfg, udir):
    """Сторінки частини (ключ у prog -> Markdown) і куди веде кожна стара адреса #/u/<pid>/<ключ>."""
    pre = cfg["prefix"]
    pages, moved = {}, {"": pre, "test": "test", "video": "shlyakh"}
    for fname, key in cfg.get("files", {}).items():
        src = udir / f"{fname}.md"
        if src.exists():
            pages[key] = src.read_text(encoding="utf-8")
            moved[fname] = key
    if cfg.get("split"):
        for key, md in split_themes((udir / f"{cfg['split']}.md").read_text(encoding="utf-8"), pre).items():
            if cfg.get("pybox") and key != pre:
                first, _, rest = md.partition("\n")
                md = first + '\n\n<div class="pybox" id="pybox"></div>\n' + rest
            pages[key] = md
        moved[cfg["split"]] = pre
    if (udir / "pages").exists():
        for src in sorted((udir / "pages").glob("urok-*.md")):
            key = f"{pre}-{src.stem.split('-')[1]}"
            pages[key] = src.read_text(encoding="utf-8")
            moved[src.stem] = key
    return pages, moved


MOVED = {}  # стара частина -> {старий ключ: новий ключ у prog}
OLD_LINK = re.compile(r'href="#/u/([a-z-]+)(?:/([^"/]*))?"')


def rewrite_links(html):
    """Посилання на старі розділи -> сторінки всередині prog (щоб не ходити через перенаправлення)."""
    def sub(m):
        pid, key = m.group(1), m.group(2) or ""
        if pid not in MOVED:
            return m.group(0)
        new = MOVED[pid].get(key, MOVED[pid][""])
        return f'href="#/u/prog/{new}"'
    return OLD_LINK.sub(sub, html)


def main():
    errors = []
    units = json.loads((CONTENT / "units.json").read_text(encoding="utf-8"))
    index = []
    files = []
    # UPROGONE: шлях по лабах (модулі, «Шлях», «Усе», «Шпаргалки») складається з частин перед збиранням
    try:
        sys.path.insert(0, str(ROOT / "tools"))
        import gen_prog_path
        gen_prog_path.main(quiet=True)
    except Exception as e:  # noqa: BLE001 - будь-яка помилка шляху = помилка збирання
        errors.append(f"gen_prog_path: {e}")
    parts_cfg = json.loads((CONTENT / "prog" / "meta.json").read_text(encoding="utf-8")).get("parts", {})
    part_out = {}
    for pid, cfg in parts_cfg.items():
        part_out[pid] = part_pages(pid, cfg, CONTENT / pid)
        MOVED[pid] = part_out[pid][1]
    for uid in units:
        udir = CONTENT / uid
        if uid in parts_cfg:
            # частина: тести лишаються в data/<частина>/quiz.json (id не міняються - статистика і бот),
            # сторінки - у data/prog/<префікс>-..., старі адреси сайт перенаправляє (meta.moved)
            meta = json.loads((udir / "meta.json").read_text(encoding="utf-8"))
            out = DATA / uid
            out.mkdir(parents=True, exist_ok=True)
            for old in out.glob("*.html"):
                old.unlink()
            qtext = (udir / "quiz.json").read_text(encoding="utf-8")
            check_text(qtext, f"{uid}/quiz.json", errors)
            qd = json.loads(qtext)
            (out / "quiz.json").write_text(json.dumps(qd, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
            files.append(f"data/{uid}/quiz.json")
            for f in sorted((out / "zadachi").glob("*.py")) if (out / "zadachi").exists() else []:
                files.append(f"data/{uid}/zadachi/{f.name}")
            pdir = DATA / "prog"
            pdir.mkdir(parents=True, exist_ok=True)
            for key, text in part_out[uid][0].items():
                check_text(text, f"{uid}->prog/{key}.md", errors)
                (pdir / f"{key}.html").write_text(rewrite_links(md_to_html(text)), encoding="utf-8")
                files.append(f"data/prog/{key}.html")
            meta.update({"parent": "prog", "moved": MOVED[uid], "ptitle": parts_cfg[uid].get("title", meta["title"]), "pages": [{"key": "test", "title": "Тести"}],
                         "nq": len(qd["questions"]), "nv": 0, "ng": 0})
            index.append(meta)
            continue
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
        # UPROGONE: розділ може задати свої вкладки (meta.tabs = [[ключ, назва], ...]); решта сторінок - поза вкладками
        tabs = meta.get("tabs")
        keys = [k for k, _ in PAGES] + [k for k, _ in (tabs or []) if k not in dict(PAGES)]
        for key in keys:
            src = udir / f"{key}.md"
            if not src.exists():
                continue
            text = src.read_text(encoding="utf-8")
            check_text(text, f"{uid}/{key}.md", errors)
            html = rewrite_links(md_to_html(text))
            (out / f"{key}.html").write_text(html, encoding="utf-8")
            files.append(f"data/{uid}/{key}.html")
            if not tabs:
                pages.append({"key": key, "title": dict(PAGES)[key]})
        if tabs:
            for key, title in tabs:
                if not (udir / f"{key}.md").exists():
                    errors.append(f"{uid}: вкладка {key} без файлу")
                pages.append({"key": key, "title": title})
        # сторінки поза вкладками (UNIPROG1: уроки prog) - content/<id>/pages/*.md -> data/<id>/<імʼя>.html
        for src in sorted((udir / "pages").glob("*.md")) if (udir / "pages").exists() else []:
            text = src.read_text(encoding="utf-8")
            check_text(text, f"{uid}/pages/{src.name}", errors)
            (out / f"{src.stem}.html").write_text(rewrite_links(md_to_html(text)), encoding="utf-8")
            files.append(f"data/{uid}/{src.stem}.html")
        # UPROGONE: модулі шляху (питання модуля, модуль кожної сторінки) - tools/gen_prog_path.py
        if (udir / "moduli-data.json").exists():
            (out / "moduli.json").write_text((udir / "moduli-data.json").read_text(encoding="utf-8"), encoding="utf-8")
            files.append(f"data/{uid}/moduli.json")
        # файли для скачування (заготовки задач prog) - теж у офлайн-кеш
        for f in sorted((out / "zadachi").glob("*.py")) if (out / "zadachi").exists() else []:
            files.append(f"data/{uid}/zadachi/{f.name}")
        nq = 0
        quiz = udir / "quiz.json"
        if quiz.exists():
            qtext = quiz.read_text(encoding="utf-8")
            check_text(qtext, f"{uid}/quiz.json", errors)
            qd = json.loads(qtext)
            nq = len(qd["questions"])
            (out / "quiz.json").write_text(json.dumps(qd, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
            files.append(f"data/{uid}/quiz.json")
        # UNIFIX1: картки на генерацію («поясни, чому / виведи / задача без підказки») - tools/gen_recall.py
        gen = udir / "gen.json"
        ng = 0
        if gen.exists():
            gtext = gen.read_text(encoding="utf-8")
            check_text(gtext, f"{uid}/gen.json", errors)
            gd = json.loads(gtext)
            ng = len(gd["cards"])
            (out / "gen.json").write_text(json.dumps(gd, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
            files.append(f"data/{uid}/gen.json")
        meta["ng"] = ng
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
            (DATA / f"{key}.html").write_text(rewrite_links(md_to_html(text)), encoding="utf-8")
            files.append(f"data/{key}.html")

    # UPLAN1: графік навчання (генерує uni-nagad/plan_gen.py у content/grafik) - дані і календар.
    # kalendar.ics (старе посилання) = той самий календар графіка: порожній VCALENDAR без VEVENT Google Календар
    # на Android не відкриває («Не вдається запустити подію», 18.11), а в графіку події є завжди.
    gdir = CONTENT / "grafik"
    if (gdir / "grafik.json").exists():
        gj = (gdir / "grafik.json").read_text(encoding="utf-8")
        check_text(gj, "grafik/grafik.json", errors)
        (DATA / "grafik.json").write_text(gj, encoding="utf-8")
        files.append("data/grafik.json")
        cal = (gdir / "grafik.ics").read_bytes()
        if b"BEGIN:VEVENT" not in cal:
            errors.append("grafik.ics без жодної події")
        (SITE / "grafik.ics").write_bytes(cal)
        (SITE / "kalendar.ics").write_bytes(cal)
        files += ["grafik.ics", "kalendar.ics"]
    # календар: лише відомі дати колоквіумів і іспитів (якщо графіка нема)
    dj = json.loads((CONTENT / "dates.json").read_text(encoding="utf-8"))
    ics = ["BEGIN:VCALENDAR", "VERSION:2.0", "PRODID:-//uni-prep//UK", "CALSCALE:GREGORIAN", "X-WR-CALNAME:Колоквіуми і іспити"]
    for ev in dj["events"]:
        if not ev.get("date"):
            continue
        d = ev["date"].replace("-", "")
        ics += ["BEGIN:VEVENT", f"UID:{ev['id']}-{d}@uni-prep", f"DTSTAMP:{d}T000000Z", f"DTSTART;VALUE=DATE:{d}",
                f"SUMMARY:{ev['title']}", "BEGIN:VALARM", "TRIGGER:-P1D", "ACTION:DISPLAY", f"DESCRIPTION:{ev['title']}", "END:VALARM", "END:VEVENT"]
    ics.append("END:VCALENDAR")
    if "kalendar.ics" not in files and "BEGIN:VEVENT" in ics:  # порожній календар не віддаємо (UPLAN1)
        (SITE / "kalendar.ics").write_bytes(("\r\n".join(ics) + "\r\n").encode("utf-8"))
        files.append("kalendar.ics")

    # UPROGONE: скільки питань у розділі разом з частинами (include) - для кільця прогресу і картки розділу
    by_id = {u["id"]: u for u in index}
    for u in index:
        if u.get("include") and not u.get("parent"):
            u["nqAll"] = u["nq"] + sum(by_id[i]["nq"] for i in u["include"] if i in by_id)
            u["parts"] = [i for i in u["include"] if by_id.get(i, {}).get("parent") == u["id"]]
    (DATA / "units.json").write_text(json.dumps(index, ensure_ascii=False, indent=1), encoding="utf-8")
    files.append("data/units.json")

    shell = ["./", "index.html", "grafik.js", "app.js", "pyrun.js", "py-worker.js", "style.css", "manifest.webmanifest",
             "icons/icon-192.png", "icons/icon-512.png", "icons/maskable-512.png", "icons/favicon.svg"]
    # шрифти (self-hosted, tools/make_fonts.py) - теж у кеш, щоб офлайн був той самий вигляд
    shell += sorted("fonts/" + f.name for f in (SITE / "fonts").glob("*.woff2"))
    for s in shell + files:
        p = SITE / (s if s != "./" else "index.html")
        if not p.exists():
            errors.append(f"нема файлу {s}")
    for s in ["index.html", "grafik.js", "app.js", "pyrun.js", "py-worker.js", "style.css"]:
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
