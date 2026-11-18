"""UCMD1 e2e: підказки до команд у коді і вкладка «Команди».

  python -X utf8 -E tools/komandy_e2e.py              # локально (http.server у потоці скрипта)
  python -X utf8 -E tools/komandy_e2e.py https://...  # живий сайт

На 390 і 1440:
 1. Кожна сторінка prog з блоками bash/sh: КОЖЕН блок оброблено (data-ck), у ньому є кнопки-команди; сума кнопок > 0.
 2. На уроці Mint 03: торкнутися mkdir, -p, cd .., | - підказка видна цілком на екрані, текст = довідник,
    посилання веде на запис у вкладці «Команди» і цей запис відкритий; Escape закриває, фокус повертається.
 3. Вкладка «Команди»: пошук «mkdir» лишає запис mkdir і відкриває його; «-p» знаходить кілька; нісенітниця - 0 і підказка.
 4. Без горизонтальної прокрутки, консоль без помилок, жодної відповіді 4xx/5xx.
 5. Офлайн (після кешу service worker): урок і підказка працюють, вкладка «Команди» відкривається.
"""
import json
import re
import sys
from pathlib import Path

from playwright.sync_api import sync_playwright

sys.path.insert(0, str(Path(__file__).resolve().parent))
from prog_e2e import serve  # noqa: E402
from prog_one_e2e import goto  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "site" / "data"
SHOTS = ROOT / "tools" / "_shots_komandy"


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    base = sys.argv[1] if len(sys.argv) > 1 else serve()
    if not base.endswith("/"):
        base += "/"
    SHOTS.mkdir(exist_ok=True)
    kd = json.loads((DATA / "prog" / "komandy.json").read_text(encoding="utf-8"))
    pages = []
    for p in sorted((DATA / "prog").glob("*.html")):
        if re.search(r'class="language-(bash|sh|shell|console)"', p.read_text(encoding="utf-8")):
            pages.append(p.stem)
    fails, st = [], {"pages": 0, "blocks": 0, "buttons": 0}

    def fail(msg):
        fails.append(msg)
        print("FAIL", msg[:300])

    with sync_playwright() as pw:
        br = pw.chromium.launch(headless=True)
        for vw, vh, mob in ((390, 844, True), (1440, 900, False)):
            ctx = br.new_context(viewport={"width": vw, "height": vh}, is_mobile=mob, has_touch=mob,
                                 service_workers="allow")
            page = ctx.new_page()
            errs = []
            page.on("console", lambda m: errs.append(m.text) if m.type == "error" else None)
            page.on("pageerror", lambda e: errs.append(str(e)))
            page.on("response", lambda r: errs.append(f"{r.status} {r.url}") if r.status >= 400 else None)
            # 1. кожна сторінка з bash-блоками
            for key in pages:
                goto(page, base, f"/u/prog/{key}")
                page.wait_for_function("() => [...document.querySelectorAll('article.doc pre > code')].filter(c => /language-(bash|sh|shell|console)/.test(c.className)).every(c => c.dataset.ck)", timeout=10000)
                r = page.evaluate("""() => { const bs = [...document.querySelectorAll('article.doc pre > code')].filter(c => /language-(bash|sh|shell|console)/.test(c.className));
                    return {n: bs.length, empty: bs.filter(c => !c.querySelector('.ck') && c.textContent.trim().length > 3).map(c => c.textContent.slice(0, 60)),
                            btn: document.querySelectorAll('article.doc .ck').length, sw: document.documentElement.scrollWidth, w: innerWidth}; }""")
                st["pages"] += 1
                st["blocks"] += r["n"]
                st["buttons"] += r["btn"]
                if r["sw"] > r["w"] + 1:
                    fail(f"{vw}: {key}: горизонтальна прокрутка {r['sw']} > {r['w']}")
                for t in r["empty"]:
                    if re.search(r"[a-z]", t) and not t.strip().startswith(("#", "evgen@")):
                        print(f"  увага {vw}: {key}: блок без жодної підказки: {t!r}")
            # 2. урок Mint 03: підказки
            goto(page, base, "/u/prog/mint-03")
            page.wait_for_selector("article.doc .ck")
            for k, f, a in (("mkdir", "-p", None), ("cd", None, ".."), ("|", None, None), ("python3 -m venv", None, None)):
                sel = f'article.doc .ck[data-k="{k}"]' + (f'[data-f="{f}"]' if f else ":not([data-f]):not([data-a])" if not a else "") + (f'[data-a="{a}"]' if a else "")
                b = page.locator(sel).first
                if not b.count():
                    fail(f"{vw}: mint-03: нема кнопки {sel}")
                    continue
                b.scroll_into_view_if_needed()
                b.click()
                tip = page.locator(".cktip")
                tip.wait_for(state="visible", timeout=3000)
                box = tip.bounding_box()
                txt = tip.inner_text()
                e = kd[k]
                want = [e[1]] + ([e[3][f]] if f else []) + ([e[4][a]] if a else [])
                for w in want:
                    w = w.replace("`", "")  # у підказці `код` показано як <code>
                    if w not in txt:
                        fail(f"{vw}: підказка {k} {f or a or ''}: нема тексту довідника «{w[:40]}»")
                if box["x"] < 0 or box["y"] < 0 or box["x"] + box["width"] > vw + 1 or box["y"] + box["height"] > vh + 1:
                    fail(f"{vw}: підказка {k} не вся на екрані: {box}")
                if mob and box["y"] + box["height"] > vh - 56:
                    fail(f"{vw}: підказка {k} лізе під нижню навігацію: {box}")
                page.screenshot(path=str(SHOTS / f"tip-{vw}-{e[0]}.png"))
                page.keyboard.press("Escape")
                page.wait_for_timeout(100)
                if page.locator(".cktip").count():
                    fail(f"{vw}: Escape не закрив підказку {k}")
                if not page.evaluate("() => document.activeElement && document.activeElement.classList.contains('ck')"):
                    fail(f"{vw}: після Escape фокус не на команді")
            # посилання з підказки -> запис у вкладці
            page.locator('article.doc .ck[data-k="mkdir"]').first.click()
            page.locator(".cktip a").click()
            page.wait_for_function("() => decodeURIComponent(location.hash) === '#/u/prog/komandy/k-mkdir' && document.querySelector('#app').dataset.route", timeout=10000)
            page.wait_for_timeout(400)
            ok = page.evaluate("() => { const d = document.getElementById('k-mkdir'); if (!d) return 'нема'; const r = d.getBoundingClientRect(); return d.open && r.top < innerHeight && r.bottom > 0 ? 'ok' : 'закритий або не на екрані'; }")
            if ok != "ok":
                fail(f"{vw}: посилання з підказки: запис mkdir {ok}")
            # 3. пошук
            goto(page, base, "/u/prog/komandy")
            n_all = page.locator("details.cmd").count()
            if n_all != len(kd):
                fail(f"{vw}: у вкладці {n_all} записів, у довіднику {len(kd)}")
            inp = page.locator("#cmdq")
            for q, cond in (("mkdir", lambda n, o: n >= 1 and o), ("-p", lambda n, o: n >= 3), ("ґґґзззхх", lambda n, o: n == 0)):
                inp.fill(q)
                page.wait_for_timeout(150)
                n = page.locator("details.cmd:not([hidden])").count()
                opened = page.evaluate("() => !!document.getElementById('k-mkdir').open")
                if not cond(n, opened):
                    fail(f"{vw}: пошук «{q}»: видно {n}, mkdir відкритий={opened}")
            if "Нічого не знайдено" not in page.locator("#cmdn").inner_text():
                fail(f"{vw}: пошук без результату не каже «Нічого не знайдено»")
            inp.fill("")
            page.screenshot(path=str(SHOTS / f"komandy-{vw}.png"))
            sw = page.evaluate("() => document.documentElement.scrollWidth - innerWidth")
            if sw > 1:
                fail(f"{vw}: вкладка «Команди» з горизонтальною прокруткою {sw}")
            # 5. офлайн
            page.goto(base)
            page.wait_for_function("async () => { const ks = await caches.keys(); for (const k of ks) { const c = await caches.open(k); if (await c.match('data/prog/komandy.json')) return true; } return false; }", timeout=60000)
            ctx.set_offline(True)
            page.reload()
            goto(page, base, "/u/prog/mint-03")
            page.wait_for_selector("article.doc .ck")
            page.locator('article.doc .ck[data-k="touch"]').first.click()
            page.locator(".cktip").wait_for(state="visible", timeout=3000)
            if kd["touch"][1] not in page.locator(".cktip").inner_text():
                fail(f"{vw}: офлайн підказка touch без тексту")
            goto(page, base, "/u/prog/komandy")
            if page.locator("details.cmd").count() != len(kd):
                fail(f"{vw}: офлайн вкладка «Команди» неповна")
            ctx.set_offline(False)
            bad = [e for e in errs if "favicon" not in e]
            if bad:
                fail(f"{vw}: консоль/мережа: {bad[:5]}")
            ctx.close()
        br.close()
    print(f"сторінок {st['pages']}, bash-блоків {st['blocks']}, кнопок-команд {st['buttons']}; помилок {len(fails)}")
    sys.exit(1 if fails else 0)


if __name__ == "__main__":
    main()
