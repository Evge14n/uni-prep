"""UPLAN1: e2e розділів «Графік» (#/grafik) і «Відео-уроки» (#/video) - headless, 390 і 1440 px.

python -P -E tools/grafik_e2e.py [--shots DIR]
Перевіряє: стан з посилання бота (#/grafik/<код>) зберігається і код зникає з адреси; борги на «сьогодні»
(годинник браузера ставиться на 25.11.2026); галочка відкриває t.me/<бот>?start=g_<id> і ставить «чекає бота»;
кожна сторінка відео має 4 кроки в порядку «дивись -> повтори -> зроби сам -> перевір себе»; без помилок
консолі, без 4xx, без горизонтальної прокрутки, цілі ≥ 44 px; офлайн після service worker.
"""
import base64
import functools
import http.server
import json
import sys
import threading
from datetime import datetime, timezone
from pathlib import Path

from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parent.parent
SITE = ROOT / "site"
PLAN = json.loads((SITE / "data" / "grafik.json").read_text(encoding="utf-8"))


def code(done, res=()):
    n = len(PLAN["ids"])

    def bits(ids):
        b = bytearray((n + 7) // 8)
        for i in ids:
            k = PLAN["units"][i]["idx"]
            b[k // 8] |= 1 << (k % 8)
        return base64.urlsafe_b64encode(bytes(b)).decode().rstrip("=")
    return f"{bits(done)}.{bits(res)}.{PLAN['version']}"


def serve():
    h = functools.partial(http.server.SimpleHTTPRequestHandler, directory=str(SITE))
    http.server.SimpleHTTPRequestHandler.log_message = lambda *a, **k: None
    srv = http.server.ThreadingHTTPServer(("127.0.0.1", 0), h)
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    return srv, f"http://127.0.0.1:{srv.server_address[1]}/"


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    shots = Path(sys.argv[sys.argv.index("--shots") + 1]) if "--shots" in sys.argv else None
    if shots:
        shots.mkdir(parents=True, exist_ok=True)
    srv, base = serve()
    errs, checks = [], 0
    first_day = PLAN["units"]["h6"]["day"]  # 19.11
    done = [i for i, u in PLAN["units"].items() if u["day"] <= "2026-11-21" and i != "an-t1"]
    with sync_playwright() as pw:
        br = pw.chromium.launch(headless=True)
        for w, h in ((390, 844), (1440, 900)):
            ctx = br.new_context(viewport={"width": w, "height": h}, locale="uk-UA")
            page = ctx.new_page()
            page.clock.install(time=datetime(2026, 11, 25, 9, 0, tzinfo=timezone.utc))
            bad = []
            page.on("console", lambda m: bad.append(m.text) if m.type == "error" else None)
            page.on("response", lambda r: bad.append(f"{r.status} {r.url}") if r.status >= 400 else None)
            opened = []
            page.context.on("page", lambda pg: opened.append(pg))
            page.goto(base + "#/grafik/" + code(done))
            page.wait_for_selector("#app[data-route]")
            page.wait_for_function("location.hash === '#/grafik'")
            checks += 1
            st = page.evaluate("JSON.parse(localStorage.getItem('uniprep:grafik'))")
            if not st or st.get("code") != code(done):
                errs.append(f"{w}: стан з посилання не збережено")
            txt = page.inner_text("#app")
            for need in ("Сьогодні, ср 25.11", "борг з 20.11", "Графік у календар телефона", "Відео-уроки"):
                checks += 1
                if need not in txt:
                    errs.append(f"{w}: нема «{need}»")
            # галочка першого незробленого пункту сьогодні -> бот
            b = page.locator(".gday.today .gchk[aria-pressed='false']").first
            gid = b.get_attribute("data-g")
            b.scroll_into_view_if_needed()
            hit = page.evaluate("""id => { const e = document.querySelector(`.gday.today .gchk[data-g="${id}"]`);
                const r = e.getBoundingClientRect(); const t = document.elementFromPoint(r.x + r.width / 2, r.y + r.height / 2);
                return t === e || e.contains(t); }""", gid)
            if not hit:
                errs.append(f"{w}: галочку {gid} перекриває інший елемент")
            b.click()
            page.wait_for_timeout(500)
            checks += 1
            urls = [pg.url for pg in opened]
            if not any(f"t.me/{PLAN['bot']}?start=g_{gid}" in u for u in urls):
                errs.append(f"{w}: галочка не відкрила бота ({urls})")
            for pg in opened:
                pg.close()
            if "чекає бота" not in page.inner_text(".gday.today"):
                errs.append(f"{w}: нема «чекає бота» після галочки")
            # розміри і прокрутка
            for route in ("#/", "#/grafik", "#/video", "#/video/lm01", "#/video/z1", "#/video/g11", "#/video/an-t1"):
                page.goto(base + route)
                page.wait_for_function(f"document.querySelector('#app').dataset.route === '{route}'")
                checks += 1
                sw = page.evaluate("document.documentElement.scrollWidth - innerWidth")
                if sw > 1:
                    errs.append(f"{w} {route}: горизонтальна прокрутка {sw}px")
                small = page.evaluate("""[...document.querySelectorAll('#app .gchk, #app .vlist a')]
                    .filter(e => e.offsetParent && (e.getBoundingClientRect().height < 44)).length""")
                if small:
                    errs.append(f"{w} {route}: {small} цілей < 44 px")
                t = page.inner_text("#app")
                for bad_s in ("undefined", "NaN", "null", "$$", "\\frac"):
                    if bad_s in t:
                        errs.append(f"{w} {route}: у тексті «{bad_s}»")
                if route.startswith("#/video/"):
                    hs = page.locator(".vsteps > li h2").all_inner_texts()
                    want = ["Дивись", "Повтори", "Зроби сам", "Перевір себе"]
                    if [x.strip() for x in hs] != want:
                        errs.append(f"{w} {route}: кроки {hs}")
                if shots:
                    page.wait_for_timeout(700)  # View Transitions
                    page.screenshot(path=str(shots / f"{w}{route.replace('#/', '_').replace('/', '-')}.png"), full_page=False)
            # усі сторінки відео відкриваються (лише 1440, щоб не дублювати)
            if w == 1440:
                for uid in PLAN["units"]:
                    page.goto(base + f"#/video/{uid}")
                    page.wait_for_function(f"document.querySelector('#app').dataset.route === '#/video/{uid}'")
                    checks += 1
                    href = page.locator(".vsteps a.btn.primary").first.get_attribute("href")
                    v = PLAN["units"][uid]["video"]
                    if not href or v["id"] not in href or (v.get("start") and f"t={v['start']}s" not in href):
                        errs.append(f"#/video/{uid}: посилання на відео {href}")
            # вкладка «Відео» розділу не має підмінятись сторінкою графіка (рецензент UPLAN1 №1)
            page.goto(base + "#/u/an-k1/video")
            page.wait_for_function("document.querySelector('#app').dataset.route === '#/u/an-k1/video'")
            checks += 1
            if "Відео-уроки" in page.inner_text("#app h1") or not page.locator(".tabs a[aria-current]").count():
                errs.append(f"{w}: #/u/an-k1/video показує не вкладку розділу")
            # офлайн після SW
            page.goto(base + "#/grafik")
            page.wait_for_function("navigator.serviceWorker && navigator.serviceWorker.controller !== null || true")
            page.evaluate("navigator.serviceWorker.ready")
            page.wait_for_timeout(2500)
            page.reload()
            page.wait_for_timeout(1500)
            ctx.set_offline(True)
            page.goto(base + "#/video/lm02")
            page.wait_for_function("document.querySelector('#app').dataset.route === '#/video/lm02'")
            checks += 1
            if "Дивись" not in page.inner_text("#app"):
                errs.append(f"{w}: офлайн #/video/lm02 не відкрився")
            ctx.set_offline(False)
            bad = [b for b in bad if "youtube" not in b and "t.me" not in b]
            if bad:
                errs.append(f"{w}: консоль/мережа: {bad[:5]}")
            ctx.close()
        br.close()
    srv.shutdown()
    print(f"перевірок {checks}, помилок {len(errs)}")
    for e in errs:
        print("  ", e)
    sys.exit(1 if errs else 0)


if __name__ == "__main__":
    main()
