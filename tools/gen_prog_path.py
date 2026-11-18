"""UPROGONE (18.11.2026): один розділ «Програмування» - модуль на кожну лабу ЛР1-ЛР7 (+ «після ЛР7»).

Частини (Python - prog, Linux Mint - mint, Git - git, безпечний код - prog-sec, Linux у WSL - linux) лишаються
джерелами зі своїми генераторами і quiz.json (id питань не міняються - бот і статистика), а цей скрипт складає з них
шлях: content/prog/pages/m1..m8.md, shlyakh.md (вкладка «Шлях»), vse.md («Усе»), shpargalky.md («Шпаргалки»),
pages/lab-4.md (розбір ЛР4 з підказками, без прізвищ) і moduli-data.json (для сайту: питання модулів, модуль сторінки).

Запуск: python -P -E tools/gen_prog_path.py  (tools/build.py викликає його сам перед збиранням)
Перевіряє: кожен урок частини - рівно в одному модулі; кожне питання частин - рівно в одному модулі;
кожне відео з moduli.json є в графіку; якір кожного посилання на розділ сторінки існує.
"""
import json
import math
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
C = ROOT / "content"
PROG = C / "prog"
LR4 = Path(r"D:\Універ\05_Програмування\Лабораторні\ЛР4\ЛР4 - розбір по завданнях.md")
UNIV_PROG = Path(r"D:\Універ\05_Програмування")

# сторінки частин усередині prog (так само називає build.py)
PART_PREFIX = {"mint": "mint", "git": "git", "linux": "linux", "prog-sec": "sec"}


class GenError(Exception):
    pass


def read(p):
    return Path(p).read_text(encoding="utf-8")


def md_ids(text):
    """Заголовки -> id так, як їх дасть build.py (той самий markdown + toc)."""
    sys.path.insert(0, str(ROOT / "tools"))
    from build import md_to_html  # noqa: E402
    html = md_to_html(text)
    res = []
    for m in re.finditer(r'<h([1-6]) id="([^"]+)">(.*?)</h\1>', html, flags=re.S):
        res.append((re.sub(r"<[^>]+>", "", m.group(3)).strip(), m.group(2)))
    return res


def anchor(ids, pattern):
    hits = [i for t, i in ids if re.search(pattern, t)]
    if len(hits) != 1:
        raise GenError(f"якір «{pattern}»: знайдено {len(hits)}")
    return hits[0]


# ---------- уроки частин ----------
def python_lessons():
    res = {}
    for m in re.finditer(r"^\| \[(\d+)\. ([^\]]+)\]\(#/u/prog/urok-(\d+)\) \| (.+?) \|$", read(PROG / "uroky.md"), re.M):
        n = int(m.group(1))
        t = re.search(r"Час: (\d+) хв", m.group(4))
        lec = re.match(r"(.+?), потрібно для", m.group(4))
        res[n] = {"title": m.group(2), "page": f"urok-{n:02d}", "min": int(t.group(1)) if t else 30,
                  "what": lec.group(1) if lec else ""}
    return res


def mint_lessons():
    res = {}
    for m in re.finditer(r"^\| \[(\d+)\. ([^\]]+)\]\(#/u/mint/urok-(\d+)\) \| (.+?) \| (.+?) \|$", read(C / "mint" / "uroky.md"), re.M):
        n = int(m.group(1))
        res[n] = {"title": m.group(2), "page": f"mint-{n:02d}", "what": m.group(4), "time": m.group(5)}
    return res


def git_lessons():
    text = read(C / "git" / "teoriya.md")
    res = {}
    for m in re.finditer(r"^\| (\d\d) \| ([^|]+?) \| ([^|]+?) \|$", text, re.M):
        n = int(m.group(1))
        res[n] = {"title": m.group(2), "page": f"git-{n:02d}", "what": m.group(3)}
    m = re.search(r"^## Тема 18\. (.+)$", text, re.M)
    if m:
        res[18] = {"title": m.group(1), "page": "git-18", "what": "один приватний репо на всі ЛР1-ЛР7: коміт на крок, гілка на лабу, тег на здачу"}
    return res


def themes(path, prefix):
    res = {}
    for m in re.finditer(r"^## Тема (\d+)\. (.+)$", read(path), re.M):
        n = int(m.group(1))
        res[n] = {"title": m.group(2).strip(), "page": prefix if n == 0 else f"{prefix}-{n:02d}"}
    return res


def sec_tasks():
    text = read(C / "prog-sec" / "zadachi.md")
    ids = md_ids(text)
    res = {}
    for m in re.finditer(r"^## Задача (\d+)\. (.+)$", text, re.M):
        n = int(m.group(1))
        res[n] = {"title": m.group(2).strip(), "page": "sec-zadachi/" + anchor(ids, rf"^Задача {n}\. ")}
    return res


def bugs(ids):
    res = {}
    for m in re.finditer(r"^### bug_(\d)\.py - (.+)$", read(C / "mint" / "zadachi.md"), re.M):
        n = int(m.group(1))
        res[n] = {"title": f"bug_{n}.py - {m.group(2).strip()}", "page": "mint-zadachi/" + anchor(ids, rf"^bug_{n}\.py - ")}
    return res


# ---------- графік (відео) ----------
def grafik_units():
    p = C / "grafik" / "grafik.json"
    if not p.exists():
        return {}
    return json.loads(read(p))["units"]


def mmss(s):
    s = int(s or 0)
    return f"{s // 60}:{s % 60:02d}"


def vmin(v):
    return max(1, math.ceil((v.get("watch_s") or 60) / 60))


def item_min(g, prefix):
    """Хвилини пункту графіка разом з його заходами (lm04 + lm04b ...)."""
    return sum(u.get("min", 0) for k, u in g.items() if re.fullmatch(re.escape(prefix) + r"[b-z]?", k))


# ---------- питання ----------
def load_quiz(uid):
    return json.loads(read(C / uid / "quiz.json"))["questions"]


def lnk(title, page):
    return f"[{title}](#/u/prog/{page})"


def q_word(n):
    a, b = n % 10, n % 100
    return "питання" if 2 <= a <= 4 and not 12 <= b <= 14 else ("питання" if a == 1 and b != 11 else "питань")


# урок Python, без якого питання не розвʼязати: «Лекція N» = урок N; теми конспекту UNI2 - теж уроки
UNI2_LESSON = {1: 1, 2: 2, 3: 3, 4: 4, 5: 4, 6: 6, 7: 7, 8: 8, 9: 9}


def need_lesson(src):
    m = re.search(r"Лекці[яї] (\d+)", src or "")
    if m:
        return int(m.group(1))
    m = re.search(r"UNI2 тема (\d+)", src or "")
    return UNI2_LESSON.get(int(m.group(1))) if m else None


def fold_levels(text):
    """Розбір ЛР4: «**Рівень N.**» до наступного рівня чи заголовка - у згорнутий блок (відкривати по черзі)."""
    out, cur, fence = [], None, False
    for ln in text.split("\n"):
        if re.match(r"^\s*(```|~~~)", ln):
            fence = not fence
        m = None if fence else re.match(r"^\*\*Рівень (\d)\.\*\*\s*(.*)$", ln)
        end = not fence and (m or ln.startswith("#") or ln.strip() == "---")
        if end and cur is not None:
            out += ["", "</details>", ""]
            cur = None
        if m:
            cur = m.group(1)
            out += [f'<details markdown="1"><summary>Рівень {cur}</summary>', ""]
            if m.group(2).strip():
                out.append(m.group(2))
            continue
        out.append(ln)
    if cur is not None:
        out += ["", "</details>"]
    return "\n".join(out)


def fmt_h(m):
    h, mm = divmod(int(m), 60)
    return (f"{h} год " if h else "") + (f"{mm} хв" if mm else "").strip()


def main(quiet=False):
    say = (lambda *a: None) if quiet else print
    spec = json.loads(read(PROG / "moduli.json"))
    mods = spec["modules"]
    PY, MI, GI = python_lessons(), mint_lessons(), git_lessons()
    LI = themes(C / "linux" / "teoriya.md", "linux")
    SE = themes(C / "prog-sec" / "teoriya.md", "sec")
    SEt = sec_tasks()
    mint_z = read(C / "mint" / "zadachi.md")
    mz_ids = md_ids(mint_z)
    BU = bugs(mz_ids)
    G = grafik_units()
    errors = []

    # 1. кожен урок частини - рівно в одному модулі
    def cover(name, allk, field_lists):
        seen = {}
        for m in mods:
            for f in field_lists:
                v = m.get(f)
                for x in (v if isinstance(v, list) else ([v] if v else [])):
                    if x in seen:
                        errors.append(f"{name} {x}: і в модулі {seen[x]}, і в модулі {m['n']}")
                    seen[x] = m["n"]
        for k in allk:
            if k not in seen:
                errors.append(f"{name} {k}: нема в жодному модулі")
        for k in seen:
            if k not in allk:
                errors.append(f"{name} {k}: нема такого уроку")
        return seen
    mod_py = cover("Python урок", PY.keys(), ["python"])
    mod_mi = cover("Mint урок", MI.keys(), ["mint", "lab_mint", "debug_mint", "mint_extra"])
    mod_gi = cover("Git урок", GI.keys(), ["git"])
    mod_li = cover("Linux день", LI.keys(), ["linux"])
    mod_se = cover("Безпека тема", SE.keys(), ["sec"])
    cover("Безпека задача", SEt.keys(), ["sec_tasks"])
    cover("bug", BU.keys(), ["bug"])
    if len(PY) != 9 or len(MI) != 27 or len(GI) != 18 or len(LI) != 11 or len(SE) != 10 or len(SEt) != 10 or len(BU) != 7:
        errors.append(f"не всі уроки розпізнано: python {len(PY)}, mint {len(MI)}, git {len(GI)}, linux {len(LI)}, sec {len(SE)}, задач {len(SEt)}, bug {len(BU)}")

    # 2. питання -> модуль
    keys = {m["n"]: [] for m in mods}
    qmod = {}
    for uid in ["prog", "prog-sec", "mint", "git", "linux"]:
        for q in load_quiz(uid):
            t = q["topic"]
            n = None
            if uid == "prog":
                n = next((m["n"] for m in mods if t in m["quiz_prog"]), None)
                need = need_lesson(q.get("src"))
                if n is not None and need in mod_py and mod_py[need] > n:
                    n = mod_py[need]  # напр. «Лекція 8» у темі модуля 2 - лише після уроку 8
            elif uid == "prog-sec":
                n = next((m["n"] for m in mods if t in m["quiz_sec"]), None)
            else:
                mm = re.match(r"(\d+)\.", t)
                num = int(mm.group(1)) if mm else None
                n = {"mint": mod_mi, "git": mod_gi, "linux": mod_li}[uid].get(num)
            if n is None:
                errors.append(f"питання {uid}/{q['id']} (тема «{t}») не потрапило в жоден модуль")
                continue
            keys[n].append(f"{uid}/{q['id']}")
            qmod[f"{uid}/{q['id']}"] = n
    for m in mods:
        for t in m["quiz_prog"] + m["quiz_sec"]:
            if not any(t == q["topic"] for uid in ("prog", "prog-sec") for q in load_quiz(uid)):
                errors.append(f"модуль {m['n']}: теми «{t}» нема в тестах")

    # 3. відео з графіка
    for m in mods:
        for v in m["videos"]:
            if v not in G:
                errors.append(f"модуль {m['n']}: пункту графіка {v} нема")
    if errors:
        raise GenError("\n".join(errors))

    # ---------- сторінки модулів ----------
    page_mod = {}
    out = {}
    lab4 = LR4.exists()
    for i, m in enumerate(mods):
        n = m["n"]
        L = [f"# Модуль {n}. {m['title']}", "", m["about"], ""]
        tot = 0
        steps = []

        # крок 1 - відео
        vs, seen_v = [], set()
        for gid in m["videos"]:
            u = G[gid]
            v = u.get("video")
            if not v or (v["id"], v.get("start")) in seen_v:
                continue
            seen_v.add((v["id"], v.get("start")))
            frm = (f"з {mmss(v['start'])}" if v.get("start") else "з початку") + (f" до {mmss(v['end'])}" if v.get("end") and not v.get("watch_cut") else "")
            lang = " · англійською" if v.get("lang") == "en" else ""
            vs.append(f"- [{v['title']}](#/video/{gid}) - до пункту «{u['short']}», {v.get('channel', '')}, {frm}, ≈ {vmin(v)} хв{lang}")
            tot += vmin(v)
        steps.append(("Відео", ["Спершу подивись - потім роби сам. Кожне посилання відкриває сторінку «дивись → повтори → зроби сам → перевір себе» з таймкодом. Відео відкриваються з інтернетом.", ""] + vs))

        # крок 2 - Python
        body = []
        for k in m["python"]:
            p = PY[k]
            body.append(f"- {lnk(f'Урок {k}. {p["title"]}', p['page'])} - {p['what']}, ≈ {p['min']} хв")
            tot += p["min"]
            page_mod[p["page"]] = n
        if m["python_repeat"]:
            body.append("- Повтори: " + ", ".join(lnk(f"урок {k}", PY[k]["page"]) for k in m["python_repeat"]))
        if m["python_note"]:
            body.append("")
            body.append(m["python_note"] + ". Незнайома функція - у " + lnk("Довіднику", "dovidnyk") + ".")
        steps.append(("Урок Python (лекція викладача)", body or ["У цьому модулі нового уроку Python нема."]))

        # крок 3 - Mint і Git
        body = []
        if m["mint"]:
            body += ["**Linux Mint:**", ""]
            for k in m["mint"]:
                p = MI[k]
                gm = item_min(G, f"lm{k:02d}")
                body.append(f"- {lnk(f'Урок {k:02d}. {p["title"]}', p['page'])} - {p['time']} · [відео](#/video/lm{k:02d})")
                tot += gm or 30
                page_mod[p["page"]] = n
            body.append("")
        if m["git"]:
            body += ["**Git і GitHub:**", ""]
            for k in m["git"]:
                p = GI[k]
                gid = "glabs" if k == 18 else f"g{k:02d}"
                gm = item_min(G, gid)
                body.append(f"- {lnk(f'Урок {k:02d}. {p["title"]}' if k != 18 else p['title'], p['page'])} - {p['what']} · [відео](#/video/{gid})")
                tot += gm or 25
                page_mod[p["page"]] = n
            if m["git_note"]:
                body.append("")
                body.append(m["git_note"] + ".")
            body.append("")
        if m.get("linux_alt"):
            body.append("Нема під рукою ноутбука з Mint? Те саме на ПК з Windows (Ubuntu у WSL): " +
                        ", ".join(lnk(LI[k]["title"].split(":")[0], LI[k]["page"]) for k in m["linux_alt"]) + ".")
            for k in m["linux_alt"]:
                page_mod.setdefault(LI[k]["page"], n)
        if not body:
            body = ["Нового з Mint і Git для цієї лаби нема - вистачає вже вивченого."]
        steps.append(("Linux Mint і Git - саме те, що треба для цієї лаби", body))

        # крок 4 - лаба в терміналі
        body = []
        if m["lab_mint"]:
            p = MI[m["lab_mint"]]
            body.append(f"- {lnk(f'Урок {m["lab_mint"]:02d}. {p["title"]}', p['page'])} - {p['what']}")
            tot += item_min(G, f"lm{m['lab_mint']:02d}") or 40
            page_mod[p["page"]] = n
            if m.get("lab_page") == "lab-4" and lab4:
                body.append(f"- {lnk('ЛР4 - розбір по завданнях: підказки трьома рівнями', 'lab-4')}")
                page_mod["lab-4"] = n
            gid = f"lab{n}"
            if gid in G:
                body.append(f"- Сама лаба: [{G[gid]['title']}](#/video/{gid}) - {G[gid].get('do', '')}; перевір: {G[gid].get('check', '')}")
                tot += G[gid].get("min", 50)
            if m["lab_note"]:
                body.append("")
                body.append(m["lab_note"] + ".")
            steps.append(("Лаба в терміналі (розбір з підказками)", body))

        # крок 5 - налагодження
        body = []
        for k in m["debug_mint"]:
            p = MI[k]
            body.append(f"- {lnk(f'Урок {k:02d}. {p["title"]}', p['page'])} - {p['time']}")
            tot += item_min(G, f"lm{k:02d}") or 40
            page_mod[p["page"]] = n
        if m["bug"]:
            b = BU[m["bug"]]
            body.append(f"- Зламана програма: {lnk(b['title'], b['page'])} - {re.sub(r'^bug_\d\.py - ', '', m['debug_note'])}. Знайди помилку {'способом з уроку 05 (traceback, print, assert, breakpoint)' if n == 1 else 'способом з уроків 05-06 (traceback, print, assert, pdb)'}, потім звір з розбором під програмою.")
            tot += 15
        if body and n > 2:
            body.append("")
            body.append("Нагадування pdb: `python3 -m pdb файл.py`, далі `n` (рядок), `s` (усередину функції), `p змінна`, `c` (далі), `q`; після падіння - `python3 -m pdb -c continue файл.py` (post-mortem). Детально - " + lnk("урок 06", "mint-06") + ".")
        if body:
            steps.append(("Налагодження (pdb)", body))

        # крок 6 - безпечний код
        body = [m["sec_intro"], ""] if m.get("sec_intro") else []
        for k in m["sec"]:
            body.append(f"- {lnk(f'Тема {k}. {SE[k]["title"]}', SE[k]['page'])}")
            tot += 20
            page_mod[SE[k]["page"]] = n
        for k in m["sec_tasks"]:
            body.append(f"- {lnk(f'Задача {k}. {SEt[k]["title"]}', SEt[k]['page'])}")
            tot += 15
        if m["sec_note"]:
            body.append("")
            body.append(("Чому саме тут: " + m["sec_note"][0].lower() + m["sec_note"][1:]) if m["sec"] else m["sec_note"])
            body[-1] += "."
        if body:
            steps.append(("Безпечне програмування", body))

        # модуль 8 - практика й іспити замість лаби
        if n == 8:
            body = []
            for k in m["mint"]:
                p = MI[k]
                body.append(f"- {lnk(f'Linux Mint, урок {k:02d}. {p["title"]}', p['page'])} - {p['time']} · [відео](#/video/lm{k:02d})")
                page_mod[p["page"]] = n
            body += ["", "**Linux у WSL - запасний шлях на ПК з Windows** (той самий термінал, але Ubuntu; по 15 хв на день):", ""]
            for k in m["linux"]:
                body.append(f"- {lnk(LI[k]['title'], LI[k]['page'])}")
                page_mod.setdefault(LI[k]["page"], n)
            steps[2] = ("Коли знадобиться", body)
            prak = [
                lnk("Linux Mint: 4 практичні завдання", "mint-zadachi/" + anchor(mz_ids, r"^Практика: 4 завдання")),
                lnk("Git: 4 практичні завдання", "git-zadachi/" + anchor(md_ids(read(C / "git" / "zadachi.md")), r"^Чотири завдання")),
                lnk("Linux у WSL: 3 практичні завдання", "linux-zadachi/" + anchor(md_ids(read(C / "linux" / "zadachi.md")), r"^Три завдання")),
            ]
            ex = [
                lnk("іспит Linux Mint, 60 питань", "mint-zadachi/" + anchor(mz_ids, r"^Іспит-самоперевірка")),
                lnk("іспит Git, 20 питань", "git-zadachi/" + anchor(md_ids(read(C / "git" / "zadachi.md")), r"^Іспит-самоперевірка")),
                lnk("іспит Linux, 20 питань", "linux-zadachi/" + anchor(md_ids(read(C / "linux" / "zadachi.md")), r"^Іспит-самоперевірка")),
            ]
            steps.append(("Практика як у справжній роботі", ["- " + x for x in prak]))
            steps.append(("Іспити-самоперевірки і пробний залік", ["- " + x for x in ex] + [
                "- [Пробний залік з Python: 25 питань, 30 хв](#/q/prog/real) - лише Python, як на заліку",
                "- " + lnk("Тренажер безпечного коду на ПК", "sec") + " (розділ «Тренажер» наприкінці)"]))

        # крок 7 - картки й тест
        nq = len(keys[n])
        if nq:
            steps.append(("Картки й тест модуля", [
                f"<div class=\"links\"><a class=\"btn primary\" href=\"#/q/prog/m{n}\">Тест модуля: {nq} {q_word(nq)}</a> "
                f"<a class=\"btn\" href=\"#/q/prog/k{n}\">Картки модуля (пригадай сам)</a></div>", "",
                "Питання з усіх частин модуля впереміш: Python, Mint, Git, безпека; після кожної відповіді - пояснення і з якого уроку питання. "
                "Бот у Telegram сам повторює картки колоди «програмування» з перервами, що ростуть; колоди Linux Mint, Git і Linux вимкнені - "
                "увімкнути: напиши боту «увімкни колоду мінт», «увімкни колоду git» чи «увімкни колоду лінукс»."]))
            tot += 10

        # збирання сторінки
        days = max(1, round(tot / 40))
        L.append(f"Кроки по порядку - кожен наступний спирається на попередній. Разом ≈ {fmt_h(tot)} роботи, це ≈ {days} "
                 f"{'день' if days == 1 else 'дні' if days in (2, 3, 4) else 'днів'} по 30-40 хв (орієнтовно). "
                 "[Графік](#/grafik) і бот розкладають це по днях у межах 30-40 хв: першими лаби і Linux Mint, частина уроків Git - "
                 "після ЛР7, уроків Python і безпеки в графіку нема. Встигаєш більше - іди по модулю.")
        L.append("")
        for j, (title, body) in enumerate(steps, 1):
            L.append(f"## Крок {j}. {title}")
            L.append("")
            L += body
            L.append("")
        if m["mint_extra"]:
            L.append("## Ще з Linux Mint (за бажанням)")
            L.append("")
            L.append("Для лаби не обовʼязково, але це твій ноутбук - по уроку, коли є 30 хв:")
            L.append("")
            for k in m["mint_extra"]:
                p = MI[k]
                L.append(f"- {lnk(f'Урок {k:02d}. {p["title"]}', p['page'])} - {p['time']} · [відео](#/video/lm{k:02d})")
                page_mod[p["page"]] = n
            L.append("")
        nav = []
        if i > 0:
            nav.append(lnk(f"← Модуль {mods[i - 1]['n']}", f"m{mods[i - 1]['n']}"))
        nav.append(lnk("Усі модулі", "shlyakh"))
        if i + 1 < len(mods):
            nav.append(lnk(f"Модуль {mods[i + 1]['n']} →", f"m{mods[i + 1]['n']}"))
        L.append(" · ".join(nav))
        out[f"pages/m{n}.md"] = "\n".join(L) + "\n"
        sq = []
        for title, key in re.findall(r"\[([^\]]+)\]\(#/u/prog/([^)]+)\)", "\n".join(L)):
            if key in ("dovidnyk", "shlyakh") or re.fullmatch(r"m\d+", key) or any(k == key for _, k in sq):
                continue
            sq.append((title, key))
        m["_seq"] = sq
        m["_min"] = tot
        page_mod[f"m{n}"] = n

    # частини, що лишились без модуля сторінки (покажчики)
    for k, v in {"mint": 1, "git": 1, "sec": 1, "linux": 8, "mint-start": 1}.items():
        page_mod.setdefault(k, v)
    for k, p in GI.items():
        page_mod.setdefault(p["page"], mod_gi[k])

    # ---------- «Шлях» ----------
    S = ["# Програмування - один шлях по лабах", "",
         "Python, Linux Mint, Git і безпечний код - не окремі предмети, а один шлях: **модуль = одна лаба**. "
         "У кожному модулі ті самі кроки по порядку:", "",
         "1. **відео** - подивись, як це роблять;",
         "2. **урок Python** - лекція викладача, з кодом, який можна запустити тут;",
         "3. **Linux Mint і Git** - рівно те, що треба для цієї лаби;",
         "4. **лаба в терміналі** - розбір з підказками, код пишеш сам;",
         "5. **налагодження** - pdb і зламана програма;",
         "6. **безпечний код** - тема, що стосується цієї лаби;",
         "7. **картки й тест модуля** - перевір, що памʼятаєш.", "",
         "**Почни тут:** [Модуль 1, крок 1](#/u/prog/m1). Йди по модулях по черзі; день за днем - у [Графіку](#/grafik) і в боті.", "",
         '<div class="units mods">']
    for m in mods:
        n = m["n"]
        parts = []
        if m["python"]:
            parts.append("Python " + ", ".join(str(k) for k in m["python"]))
        mi = [k for k in m["mint"] + ([m["lab_mint"]] if m["lab_mint"] else []) + m["debug_mint"]]
        if mi:
            parts.append("Mint " + ", ".join(f"{k:02d}" for k in sorted(mi)))
        if m["git"]:
            parts.append("Git " + ", ".join(f"{k:02d}" if k != 18 else "лаби в git" for k in m["git"]))
        if m["sec"]:
            parts.append("безпека " + ", ".join(str(k) for k in m["sec"]))
        S.append(f'<a class="card unit mod" data-mod="{n}" href="#/u/prog/m{n}"><div><span class="badge z">Модуль {n}</span>'
                 f'<h3>{m["title"]}</h3><div class="row"><span>{" · ".join(parts) or "практика, іспити, залік"}</span></div>'
                 f'<div class="row"><span>{len(keys[n])} {q_word(len(keys[n]))}</span><span>≈ {fmt_h(m["_min"])}</span></div></div></a>')
    S += ["</div>", "",
          "## Де що лежить", "",
          "- **Уроки Python** - 9 уроків за лекціями, код запускається просто тут, і без інтернету.",
          "- **Довідник** - 254 функції й конструкції з лекцій і лаб.",
          "- **Шпаргалки** - Python, Linux Mint, Git, безпечний код і Linux у WSL на одній сторінці.",
          "- **Усе** - кожен урок кожної частини і в якому він модулі.",
          "- **Тести** - усі питання впереміш, пробний залік з Python, тести модулів і частин.", "",
          "> Раніше тут було 5 окремих розділів (Програмування, Python + безпека, Linux, Linux Mint, Git). "
          "Увесь їхній зміст тут, твої відповіді й прогрес нікуди не ділись, старі посилання ведуть сюди."]
    out["shlyakh.md"] = "\n".join(S) + "\n"

    # ---------- «Усе» ----------
    V = ["# Усе в розділі", "",
         "Кожен урок і кожна сторінка всіх частин. Число в дужках - модуль, у якому цей урок у шляху.", ""]
    V += ["## Python (уроки за лекціями)", "", lnk("Як вчити і план уроків", "uroky") + " · " + lnk("Довідник функцій", "dovidnyk") + " · " +
          lnk("Теорія до заліку", "teoriya") + " · " + lnk("Означення", "oznachennya") + " · " + lnk("Задачі з розвʼязанням", "zadachi") + " · " +
          lnk("Шпаргалка", "shpargalka"), ""]
    V += [f"- {lnk(f'Урок {k}. {p["title"]}', p['page'])} ({mod_py[k]})" for k, p in sorted(PY.items())]
    V += ["", "## Linux Mint (ноутбук)", "", lnk("Почни тут", "mint-start") + " · " + lnk("Список уроків", "mint") + " · " +
          lnk("Зламані програми, практика, іспит", "mint-zadachi") + " · " + lnk("Шпаргалка", "mint-shpargalka"), ""]
    V += [f"- {lnk(f'Урок {k:02d}. {p["title"]}', p['page'])} ({mod_mi[k]})" for k, p in sorted(MI.items())]
    V += ["", "## Git і GitHub", "", lnk("Почни тут: план і пісочниця", "git") + " · " + lnk("Практика й іспит", "git-zadachi") + " · " +
          lnk("Шпаргалка", "git-shpargalka"), ""]
    V += [f"- {lnk((f'Урок {k:02d}. ' if k != 18 else '') + p['title'], p['page'])} ({mod_gi[k]})" for k, p in sorted(GI.items())]
    V += ["", "## Безпечний код (Python + безпека)", "", lnk("Як читати, тренажер, джерела", "sec") + " · " + lnk("10 задач", "sec-zadachi") + " · " +
          lnk("Шпаргалка", "sec-shpargalka"), ""]
    V += [f"- {lnk(f'Тема {k}. {p["title"]}', p['page'])} ({mod_se[k]})" for k, p in sorted(SE.items())]
    V += ["", "## Linux у WSL (ПК з Windows)", "", "Той самий термінал, але в Ubuntu на ПК. Для ноутбука з Mint - курс Linux Mint вище.", "",
          lnk("Встановлення (День 0)", "linux") + " · " + lnk("Практика й іспит", "linux-zadachi") + " · " + lnk("Шпаргалка", "linux-shpargalka"), ""]
    V += [f"- {lnk(p['title'], p['page'])} ({mod_li[k]})" for k, p in sorted(LI.items()) if k]
    if lab4:
        V += ["", "## Розбори лаб", "", f"- {lnk('ЛР4 - розбір по завданнях (підказки, без готового коду)', 'lab-4')} (4)",
              "- Інші лаби - уроки Linux Mint «ЛРN у терміналі» (модулі 1-7)."]
    out["vse.md"] = "\n".join(V) + "\n"

    # ---------- «Шпаргалки» ----------
    H = ["# Шпаргалки", "", "Усе на одній сторінці. Розгорни потрібну.", ""]
    for i, (title, src) in enumerate([("Python", PROG / "shpargalka.md"), ("Linux Mint", C / "mint" / "shpargalka.md"),
                                      ("Git і GitHub", C / "git" / "shpargalka.md"), ("Безпечний код", C / "prog-sec" / "shpargalka.md"),
                                      ("Linux у WSL", C / "linux" / "shpargalka.md")]):
        body = read(src).strip().split("\n")
        if body and body[0].startswith("# "):
            body = body[1:]
        H += [f'<details markdown="1"{" open" if i == 0 else ""}><summary>{title}</summary>', ""] + body + ["", "</details>", ""]
    out["shpargalky.md"] = "\n".join(H) + "\n"

    # ---------- розбір ЛР4 (без прізвищ, чатів і локальних шляхів) ----------
    if lab4:
        t = read(LR4)
        tn = list(UNIV_PROG.glob("Вимоги викладача (*).md"))
        sur = re.match(r"Вимоги викладача \((\S+)", tn[0].name).group(1) if tn else None
        # прибрати: шлях до умови з чату, посилання на мої готові розвʼязки (локальна тека), прізвище викладача
        lines = [ln for ln in t.split("\n") if not ln.startswith("Умова: `") and not ln.startswith("Є готові варіанти для звірки")
                 and not ln.startswith("`ЛР4\\_перевірка")]
        t = "\n".join(lines)
        t = re.sub(r" ?\(файл `Вимоги викладача[^`]*`\)", "", t)
        t = t.replace(" (у теці з чату їх нема)", "")
        if sur:
            t = t.replace(sur + "а", "викладача").replace(sur, "викладач")
        bad = [w for w in ["з чату", "з-чату", "D:\\", "C:\\", "Універ\\", "Євген"] if w in t]
        if sur and sur[:5] in t:
            bad.append("прізвище")
        if bad:
            raise GenError(f"lab-4: лишилось {bad}")
        t = t.replace("(оновлено 18.11, ULINUX2: на ноутбуці Linux Mint)", "(на ноутбуці Linux Mint)")
        t = t.replace("курс `Linux-Mint`, «Урок 09 - ЛР4 у терміналі (turtle)»", "[урок Linux Mint 09 - ЛР4 у терміналі](#/u/prog/mint-09)")
        t = t.replace("(перевірено в уроці 09\n  курсу Linux-Mint)", "(перевірено в [уроці Mint 09](#/u/prog/mint-09))")
        t = t.replace("**Каркас файлу у твоєму стилі** (як ЛР3:", "**Каркас файлу** (як у ЛР3:")
        if "ULINUX2" in t:
            raise GenError("lab-4: лишилась службова мітка ULINUX2")
        out["pages/lab-4.md"] = fold_levels(t).rstrip() + "\n"

    data = {"modules": [{"n": m["n"], "lab": m["lab"], "title": m["title"], "keys": keys[m["n"]], "min": m["_min"],
                         "seq": [[k, tt] for tt, k in m["_seq"]]} for m in mods],
            "pageModule": page_mod}
    out["moduli-data.json"] = json.dumps(data, ensure_ascii=False, separators=(",", ":"))

    changed = 0
    for name, text in out.items():
        p = PROG / name
        p.parent.mkdir(exist_ok=True)
        if not p.exists() or p.read_text(encoding="utf-8") != text:
            p.write_text(text, encoding="utf-8")
            changed += 1
    say(f"gen_prog_path: модулів {len(mods)}, питань у модулях {sum(len(v) for v in keys.values())} "
        f"({', '.join(f'м{k}: {len(v)}' for k, v in keys.items())}), файлів змінено {changed}")
    return data


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    try:
        main()
    except GenError as e:
        print("ПОМИЛКА:", e)
        sys.exit(1)
