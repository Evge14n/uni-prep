"""Перевірка content/<id>/videos.json.

python -P -E tools/check_videos.py           - структура
python -P -E tools/check_videos.py --online  - ще й oEmbed YouTube (200 = відео є і вставляється)
"""
import json
import re
import sys
import time
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CONTENT = ROOT / "content"
ID_RE = re.compile(r"^[A-Za-z0-9_-]{11}$")
DUR_RE = re.compile(r"^(?:(\d+):)?(\d{1,2}):(\d{2})$")
LANGS = {"uk", "en"}
FORBIDDEN = ["$$", "\\frac", "\\sqrt", "begin{", "\\(", "\\[", "—", "–"]


def dur_sec(s):
    m = DUR_RE.match(s or "")
    if not m:
        return None
    h, mi, se = m.groups()
    return int(h or 0) * 3600 + int(mi) * 60 + int(se)


def check_unit(udir, errors):
    uid = udir.name
    vpath = udir / "videos.json"
    text = vpath.read_text(encoding="utf-8")
    for pat in FORBIDDEN:
        if pat in text:
            errors.append(f"{uid}: заборонене {pat!r}")
    try:
        vd = json.loads(text)
    except json.JSONDecodeError as e:
        errors.append(f"{uid}: не JSON ({e})")
        return []
    qpath = udir / "quiz.json"
    if not qpath.exists():
        errors.append(f"{uid}: нема quiz.json - нема з чим звіряти теми")
        quiz_topics = set()
    else:
        quiz_topics = {q["topic"] for q in json.loads(qpath.read_text(encoding="utf-8"))["questions"]}
    if not isinstance(vd.get("checked"), str) or not vd["checked"]:
        errors.append(f"{uid}: нема поля checked")
    ids = []
    seen_topics = set()
    for t in vd.get("topics", []):
        name = t.get("topic")
        where = f"{uid} / {name}"
        if name not in quiz_topics:
            errors.append(f"{where}: такої теми нема серед topic у quiz.json")
        if name in seen_topics:
            errors.append(f"{where}: тема повторюється")
        seen_topics.add(name)
        vids = t.get("videos") or []
        if not vids:
            errors.append(f"{where}: порожній список відео")
        if len(vids) > 3:
            errors.append(f"{where}: більше 3 відео (1 головне + до 2 запасних)")
        mains = [v for v in vids if v.get("main") is True]
        if len(mains) != 1:
            errors.append(f"{where}: головних відео {len(mains)}, треба рівно 1")
        vid_ids = [v.get("id") for v in vids]
        if len(set(vid_ids)) != len(vid_ids):
            errors.append(f"{where}: одне відео двічі")
        for v in vids:
            w = f"{where} / {v.get('id')}"
            if not isinstance(v.get("id"), str) or not ID_RE.match(v["id"]):
                errors.append(f"{w}: id має бути 11 символів [A-Za-z0-9_-]")
            for f in ("title", "author", "why"):
                if not isinstance(v.get(f), str) or not v[f].strip():
                    errors.append(f"{w}: порожнє поле {f}")
            if v.get("lang") not in LANGS:
                errors.append(f"{w}: lang має бути uk або en")
            d = dur_sec(v.get("duration"))
            if d is None:
                errors.append(f"{w}: duration не у форматі м:сс або г:хх:сс")
            s = v.get("start")
            if not isinstance(s, int) or isinstance(s, bool) or s < 0:
                errors.append(f"{w}: start має бути цілим ≥ 0")
            elif d is not None and s >= d:
                errors.append(f"{w}: start {s} не менший за тривалість {d}")
            if "main" in v and v["main"] is not True:
                errors.append(f"{w}: main або true, або нема поля")
            ids.append(v.get("id"))
    return ids


def oembed(vid):
    url = "https://www.youtube.com/oembed?url=https://www.youtube.com/watch?v=" + vid + "&format=json"
    req = urllib.request.Request(url, headers={"User-Agent": "uni-site check_videos"})
    try:
        with urllib.request.urlopen(req, timeout=20) as r:
            return r.status
    except urllib.error.HTTPError as e:
        return e.code
    except Exception as e:  # мережа
        return str(e)


def main():
    online = "--online" in sys.argv
    errors = []
    all_ids = []
    units = sorted(p.parent for p in CONTENT.glob("*/videos.json"))
    for udir in units:
        ids = check_unit(udir, errors)
        all_ids += ids
        print(f"{udir.name}: тем {len(json.loads((udir / 'videos.json').read_text(encoding='utf-8'))['topics'])}, відео {len(ids)}")
    if online:
        uniq = sorted({i for i in all_ids if isinstance(i, str)})
        bad = 0
        for n, vid in enumerate(uniq):
            if n:
                time.sleep(1)
            st = oembed(vid)
            if st != 200:
                errors.append(f"oEmbed {vid}: {st}")
                bad += 1
        print(f"oEmbed: перевірено {len(uniq)} унікальних id, не 200: {bad}")
    if errors:
        print(f"ПОМИЛОК: {len(errors)}")
        for e in errors:
            print("  " + e)
        sys.exit(1)
    print("OK: помилок 0")


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    main()
