"""UPLAN1: кожен пункт графіка має відео, і воно справді є на YouTube і вбудовується (oEmbed 200),
назва в графіку = назва з oEmbed, таймкод у межах тривалості.

python -P -E tools/check_grafik_videos.py
"""
import json
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PLAN = json.loads((ROOT / "content" / "grafik" / "grafik.json").read_text(encoding="utf-8"))


def dur(s):
    v = 0
    for x in (s or "0").split(":"):
        v = v * 60 + int(x)
    return v


def norm(t):
    return " ".join(t.replace("—", "-").replace("–", "-").split()).lower()


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    errs, cache = [], {}
    for uid, u in PLAN["units"].items():
        v = u.get("video")
        if not v or not v.get("id"):
            errs.append(f"{uid}: нема відео")
            continue
        if v["id"] not in cache:
            url = "https://www.youtube.com/oembed?format=json&url=" + urllib.parse.quote(f"https://www.youtube.com/watch?v={v['id']}")
            try:
                with urllib.request.urlopen(url, timeout=20) as r:
                    cache[v["id"]] = (r.status, json.loads(r.read()))
            except urllib.error.HTTPError as e:
                cache[v["id"]] = (e.code, {})
            except Exception as e:
                cache[v["id"]] = (0, {"error": str(e)})
            time.sleep(0.4)
        code, meta = cache[v["id"]]
        if code != 200:
            errs.append(f"{uid}: oEmbed {code} для {v['id']}")
            continue
        if norm(meta.get("title", "")) != norm(v["title"]):
            errs.append(f"{uid}: назва не збігається: «{meta.get('title')}» ≠ «{v['title']}»")
        d = dur(v.get("duration"))
        if d and (int(v.get("start") or 0) >= d or (v.get("end") and v["end"] > d + 1)):
            errs.append(f"{uid}: таймкод поза тривалістю {v.get('start')}-{v.get('end')} / {d}")
    print(f"пунктів {len(PLAN['units'])}, різних відео {len(cache)}, помилок {len(errs)}")
    for e in errs:
        print("  ", e)
    sys.exit(1 if errs else 0)


if __name__ == "__main__":
    main()
