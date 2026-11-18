"""Вкладка «Команди» розділу «Програмування» і підказки до команд у коді (UCMD1, 18.11.2026).

Джерело - довідник у D:\\Універ\\05_Програмування\\_команди\\ (dovidnyk/*.json → build_dovidnyk.py → komandy.json):
  komandy.json → content/prog/komandy.md        (вкладка з пошуком: кожна команда - розгортний блок з якорем)
               → content/prog/komandy-data.json (стисло для підказок; build.py кладе в data/prog/komandy.json)
Запуск: python -P -E tools/gen_komandy.py
"""
import json
import re
import sys
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = Path(r"D:\Універ\05_Програмування\_команди")
OUT = ROOT / "content" / "prog"
sys.path.insert(0, str(SRC))
from build_dovidnyk import entry_md, ordered  # noqa: E402
from check import GROUPS  # noqa: E402
from annotate import name_part  # noqa: E402  (UCMD1: «Назва:» лише там, де вона щось додає)

NAMES_FILE = Path(r"D:\Універ\00_Загальне\_імена-не-на-сайт.txt")

INTRO = """# Команди

Кожна команда з уроків Linux Mint, Git, Linux і Python: звідки назва, що робить, кожен прапорець, приклади з тим,
що побачиш на екрані (справжній вивід з Linux Mint 22.3 українською), як перевірити, як скасувати і типова помилка.
**В уроках можна торкнутися будь-якої команди в коді** - вискочить коротка підказка звідси.

ВЕЛИКІ літери в «Як пишеться» - що підставити своє; `[дужки]` - необовʼязкове; `-p` - прапорець, короткі можна
склеювати (`ls -la` = `ls -l -a`).

<div class="cmdsearch"><label for="cmdq">Знайти команду</label>
<input id="cmdq" type="search" autocomplete="off" spellcheck="false" placeholder="mkdir, -p, видалити, git commit...">
<p id="cmdn" class="muted" aria-live="polite"></p></div>
"""


def private_names():
    if not NAMES_FILE.exists():
        return []
    return [w.strip() for w in re.split(r"[,\n]", NAMES_FILE.read_text(encoding="utf-8"))
            if len(w.strip()) >= 4 and not w.strip().startswith("#")]


def main():
    entries = ordered(json.loads((SRC / "komandy.json").read_text(encoding="utf-8")))
    L = [INTRO]
    data = {}
    for g in GROUPS:
        es = [e for e in entries if e["group"] == g]
        if not es:
            continue
        L += [f'<h2 class="cmdg">{escape(g)}</h2>', ""]
        for e in es:
            words = [e["key"], e["short"], e["name_from"], e["what"], g] + [
                f"{f['flag']} {f.get('long', '')} {f['what']}" for f in e.get("flags", [])]
            s = escape(" ".join(words).lower(), quote=True)
            L.append(f'<details class="cmd" id="{e["id"]}" data-k="{escape(e["key"], quote=True)}" data-s="{s}" markdown="1">'
                     f'<summary><span><code>{escape(e["key"])}</code> - {escape(e["short"])}</span></summary>')
            L.append("")
            L.append(entry_md(e, h=None))
            L.append("</details>")
            L.append("")
            fl = {}
            for f in e.get("flags", []):
                fl[f["flag"]] = f["what"]
                if f.get("long"):
                    fl[f["long"]] = f["what"]
            data[e["key"]] = [e["id"], e["short"], name_part(e), fl, {a["arg"]: a["what"] for a in e.get("args", [])}]
    md = "\n".join(L)
    js = json.dumps(data, ensure_ascii=False, separators=(",", ":"))
    for w in private_names():  # сайт публічний: імена з прикладів (echo "Привіт, ...") - нейтральні, як у gen_mint
        rx = re.compile(r"\b" + re.escape(w) + r"[а-яіїєґʼ']*")
        md, js = rx.sub("Студент", md), rx.sub("Студент", js)
        assert w not in md and w not in js, "прізвище в довіднику"
    (OUT / "komandy.md").write_text(md, encoding="utf-8")
    (OUT / "komandy-data.json").write_text(js, encoding="utf-8")
    print(f"команд {len(data)}: content/prog/komandy.md ({len(md) // 1024} КБ), komandy-data.json ({len(js) // 1024} КБ)")


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    main()
