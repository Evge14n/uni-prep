"""Self-hosted шрифти сайту (woff2, підмножини під наш зміст). Жодних CDN: шрифти лежать
у site/fonts/ і йдуть у кеш service worker разом з усім сайтом.

python -P -E tools/make_fonts.py <тека-з-ttf>

У теці мають бути (OFL / вільна ліцензія DejaVu, копії ліцензій кладемо поруч з woff2):
  FiraSans-Regular.ttf, FiraSans-SemiBold.ttf, FiraSans-Bold.ttf, FiraSans-Italic.ttf
      https://github.com/google/fonts/tree/main/ofl/firasans
  Literata[opsz,wght].ttf   https://github.com/google/fonts/tree/main/ofl/literata
  DejaVuSansMono.ttf, DejaVuSans.ttf  (є в matplotlib: mpl-data/fonts/ttf)

Набір символів = базова латиниця + кирилиця + грецька + усе, що реально є в site/data і app.js.
Що Fira Sans не має (√ ∀ ⇒ ₙ ⎛ ─ ...), бере «UniMath» - підмножина DejaVu Sans лише з цих символів,
тож формули в тексті мають один вигляд на всіх телефонах. Шрифт формул (<pre>) - DejaVu Sans Mono:
у ньому є ─ │ ⎛ ⎝ ⎡ ⎣, тому багаторядкові дроби з CLAUDE.md стоять рівно.
"""
import io
import pathlib
import shutil
import sys

from fontTools import subset
from fontTools.ttLib import TTFont
from fontTools.varLib import instancer

ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = ROOT / "site" / "fonts"

BASE = set(range(0x20, 0x7F)) | set(range(0xA0, 0x100)) | set(range(0x400, 0x460)) | {0x490, 0x491} \
    | set(range(0x391, 0x3AA)) | set(range(0x3B1, 0x3CA)) | {0x3D1, 0x3D5, 0x3F5} \
    | set(range(0x2010, 0x2027)) | {0x2030, 0x2032, 0x2033, 0x2039, 0x203A, 0x2116, 0x20B4, 0x2212, 0x2026, 0x02BC}
FEATURES = ["kern", "liga", "calt", "ccmp", "locl", "mark", "mkmk", "tnum", "lnum", "pnum", "case", "sups", "subs"]


def content_chars():
    s = set()
    for p in (ROOT / "site" / "data").rglob("*"):
        if p.suffix in (".html", ".json"):
            s |= set(p.read_text(encoding="utf-8"))
    for name in ("app.js", "index.html"):
        s |= set((ROOT / "site" / name).read_text(encoding="utf-8"))
    return {ord(c) for c in s if ord(c) > 0x20}


def make(font, unicodes, out_name):
    opts = subset.Options()
    opts.flavor = "woff2"
    opts.layout_features = FEATURES
    opts.name_IDs = [0, 1, 2, 3, 4, 5, 6]
    opts.notdef_outline = True
    opts.hinting = False
    opts.desubroutinize = True
    cmap = font.getBestCmap()
    keep = sorted(u for u in unicodes if u in cmap)
    sub = subset.Subsetter(opts)
    sub.populate(unicodes=keep)
    sub.subset(font)
    path = OUT / out_name
    font.flavor = "woff2"
    font.save(path)
    print(f"{out_name}: {len(keep)} символів, {path.stat().st_size // 1024} КБ")
    return set(keep)


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    src = pathlib.Path(sys.argv[1])
    OUT.mkdir(parents=True, exist_ok=True)
    want = BASE | content_chars()
    fira_cmap = set(TTFont(src / "FiraSans-Regular.ttf").getBestCmap())
    for f, out in (("FiraSans-Regular.ttf", "fira-400.woff2"), ("FiraSans-SemiBold.ttf", "fira-600.woff2"),
                   ("FiraSans-Bold.ttf", "fira-700.woff2"), ("FiraSans-Italic.ttf", "fira-400i.woff2")):
        make(TTFont(src / f), want, out)
    # Literata: заголовки, один статичний інстанс (менше байтів, ніж змінний шрифт)
    lit = TTFont(src / "Literata[opsz,wght].ttf")
    lit = instancer.instantiateVariableFont(lit, {"wght": 600, "opsz": 30})
    buf = io.BytesIO()
    lit.save(buf)
    buf.seek(0)
    make(TTFont(buf), want, "literata-600.woff2")
    mono = make(TTFont(src / "DejaVuSansMono.ttf"), want, "dvmono-400.woff2")
    # UniMath: лише те, чого нема у Fira Sans або в моноширинному
    rest = {u for u in want if u not in fira_cmap or u not in mono} - BASE
    make(TTFont(src / "DejaVuSans.ttf"), rest, "unimath-400.woff2")
    for lic in ("OFL-FiraSans.txt", "OFL-Literata.txt", "LICENSE-DejaVu.txt"):
        if (src / lic).exists():
            shutil.copy(src / lic, OUT / lic)


if __name__ == "__main__":
    main()
