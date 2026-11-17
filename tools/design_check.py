"""Перевірка вигляду і руху (UNIDESIGN1).

python -P -E tools/design_check.py [base-url] [тека-для-відео]

1) 404/консоль: старт тренування в КОЖНОМУ розділі (раніше prog/zfp/hist/eng просили videos.json -> 404).
2) CLS: головна, сторінка розділу, відповідь у тесті, переворот і свайп картки - PerformanceObserver layout-shift
   (окремо зсуви без недавнього вводу - саме вони йдуть у CLS).
3) Цілі дотику на 390: кнопки, навігація, вкладки, варіанти, чипи >= 44x44 CSS px.
4) Шрифти: Fira Sans/Literata/DejaVu Mono справді застосовані до кирилиці (ширина рядка в canvas != фолбек).
5) prefers-reduced-motion: після дій нема запущених анімацій і конфеті.
6) Відновлення тесту після перезавантаження (відповіді й номер питання на місці).
7) Плавність під 4x CPU throttling: кадри rAF під час перевороту, свайпу, конфеті - p95 і частка кадрів > 20 мс.
8) Відео проходу на 390 (тест -> святкування, картка-свайп) - webm, далі ffmpeg у gif.
"""
import functools
import http.server
import json
import statistics
import sys
import threading
from pathlib import Path

from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parent.parent

CLS_OBS = """
window.__ls = [];
new PerformanceObserver((l) => { for (const e of l.getEntries()) window.__ls.push({v: e.value, r: e.hadRecentInput, t: e.startTime,
  src: (e.sources || []).map(s => s.node ? (s.node.className || s.node.nodeName) : '?').join(',')}); }).observe({type: 'layout-shift', buffered: true});
"""
FRAMES = """
window.__fr = []; window.__frOn = false;
(function loop(t){ if (window.__frOn) { if (window.__frLast) window.__fr.push(t - window.__frLast); window.__frLast = t; } else window.__frLast = 0; requestAnimationFrame(loop); })(performance.now());
"""


class Quiet(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *a):
        pass


def serve():
    h = functools.partial(Quiet, directory=str(ROOT / "site"))
    srv = http.server.ThreadingHTTPServer(("127.0.0.1", 0), h)
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    return f"http://127.0.0.1:{srv.server_address[1]}/"


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    base = sys.argv[1] if len(sys.argv) > 1 and sys.argv[1] != "local" else serve()
    if not base.endswith("/"):
        base += "/"
    vid_dir = Path(sys.argv[2]) if len(sys.argv) > 2 else None
    units = json.loads((ROOT / "site" / "data" / "units.json").read_text(encoding="utf-8"))
    fails, info = [], {}

    def hgo(pg, url, **kw):
        pg.goto(url, **kw)
        pg.wait_for_function("document.querySelector('#app').dataset.route === location.hash")
    with sync_playwright() as p:
        br = p.chromium.launch(headless=True)
        mob = dict(viewport={"width": 390, "height": 844}, is_mobile=True, has_touch=True, device_scale_factor=2)

        # 1) 404 і консоль у кожному розділі
        ctx = br.new_context(**mob)
        pg = ctx.new_page()
        errs = []
        pg.on("console", lambda m: errs.append(f"{m.type}: {m.text}") if m.type in ("error", "warning") else None)
        pg.on("pageerror", lambda e: errs.append(f"pageerror: {e}"))
        pg.on("response", lambda r: errs.append(f"HTTP {r.status} {r.url}") if r.status >= 400 and "youtube" not in r.url else None)
        pg.goto(base, wait_until="networkidle")
        for u in units:
            if not u["nq"]:
                continue
            for mode in ("train", "recall", "real"):
                hgo(pg, f"{base}#/q/{u['id']}/{mode}")
                pg.wait_for_selector(".q, #show, #timer")
                pg.wait_for_timeout(120)
            # одна неправильна відповідь - показ відео-підказки
            hgo(pg, f"{base}#/q/{u['id']}/train")
            pg.wait_for_selector(".q")
            if pg.locator(".opt").count():
                pg.locator(".opt").last.click()
                if pg.locator("#check").count():
                    pg.locator("#check").click()
            else:
                pg.fill("#inp", "123456")
                pg.locator("#check").click()
            pg.wait_for_selector(".verdict")
        for key in ("", "subjects", "plan", "stats", "glossary", "about"):
            hgo(pg, f"{base}#/{key}")
            pg.wait_for_timeout(200)
        info["розділів з тестами пройдено"] = sum(1 for u in units if u["nq"])
        if errs:
            fails += [f"консоль/мережа: {e}" for e in errs]
        info["помилок консолі і 4xx"] = len(errs)

        # 2) CLS
        pg.add_init_script(CLS_OBS)
        cls = {}
        for label, url, act in (
            ("головна", base, None),
            ("розділ", base + "#/u/an-k1/teoriya", None),
            ("тест: відповідь і пояснення", base + "#/q/ma-k2/train", "answer"),
            ("картка: переворот і свайп", base + "#/q/an-k1/recall", "card"),
        ):
            pg.goto("about:blank")
            hgo(pg, url, wait_until="networkidle")
            pg.wait_for_timeout(400)
            if act == "answer":
                for _ in range(3):
                    if pg.locator(".opt").count():
                        pg.locator(".opt").first.click()
                        if pg.locator("#check").count():
                            pg.locator("#check").click()
                    else:
                        pg.fill("#inp", "1")
                        pg.locator("#check").click()
                    pg.wait_for_selector(".verdict")
                    pg.wait_for_timeout(500)
                    pg.locator("#next").click()
                    pg.wait_for_timeout(400)
            if act == "card":
                for _ in range(2):
                    pg.locator("#show").click()
                    pg.wait_for_timeout(500)
                    box = pg.locator("#drag").bounding_box()
                    cx, cy = box["x"] + box["width"] / 2, box["y"] + box["height"] / 2
                    pg.mouse.move(cx, cy)
                    pg.mouse.down()
                    for k in range(1, 11):
                        pg.mouse.move(cx + k * 22, cy + 2)
                        pg.wait_for_timeout(16)
                    # картка справді їде за пальцем (не «стоїть» під анімацією появи)
                    tx = pg.evaluate("new DOMMatrix(getComputedStyle(document.querySelector('#drag')).transform).m41")
                    info.setdefault("зсув картки під час свайпу, px", []).append(round(tx))
                    if tx < 100:
                        fails.append(f"свайп: картка не рухається (translateX {tx})")
                    pg.mouse.up()
                    pg.wait_for_selector("#show", timeout=4000)
                    pg.wait_for_timeout(400)
            ls = pg.evaluate("window.__ls")
            v = sum(e["v"] for e in ls if not e["r"])
            cls[label] = round(v, 4)
            if v > 0.01:
                fails.append(f"CLS {label} = {v:.4f}: {[e for e in ls if not e['r']][:3]}")
        info["CLS"] = cls

        # 3) цілі дотику на 390
        small = []
        for url in (base, base + "#/subjects", base + "#/u/an-k1/test", base + "#/q/an-k1/train", base + "#/q/an-k1/recall"):
            hgo(pg, url)
            pg.wait_for_timeout(500)
            small += pg.evaluate("""(u) => [...document.querySelectorAll('.btn, .bnav a, .tabs a, .opt, .chiplink, .tile, .icon-btn, .back, .qhead a, .filter label, summary')]
               .filter(e => e.offsetParent !== null).map(e => { const r = e.getBoundingClientRect(); return [u, e.className || e.tagName, Math.round(r.width), Math.round(r.height), (e.textContent||'').trim().slice(0,30)]; })
               .filter(x => x[2] < 44 || x[3] < 44)""", url)
        info["цілей дотику < 44 px"] = len(small)
        fails += [f"мала ціль дотику: {s}" for s in small]

        # 4) шрифти справді застосовані (ширина кириличного рядка в canvas проти фолбеку)
        pg.goto(base)
        pg.wait_for_timeout(600)
        fonts = pg.evaluate("""async () => { await document.fonts.ready;
          const c = document.createElement('canvas').getContext('2d'); const t = 'Похідна функції в точці: ґанок, їжак, Δ → φ';
          const w = (f) => { c.font = f; return c.measureText(t).width; };
          return { fira: [w('16px "Fira Sans"'), w('16px Arial')], literata: [w('600 20px Literata'), w('600 20px Georgia')],
                   mono: [w('14px "DejaVu Mono"'), w('14px Consolas')],
                   loaded: [...document.fonts].filter(f => f.status === 'loaded').map(f => f.family + ' ' + f.weight) }; }""")
        info["шрифти"] = fonts
        for k in ("fira", "literata", "mono"):
            a, b = fonts[k]
            if abs(a - b) < 0.5:
                fails.append(f"шрифт {k}: ширина як у фолбеку ({a} / {b})")
        ff = pg.evaluate("getComputedStyle(document.querySelector('h1')).fontFamily")
        info["h1 font-family"] = ff
        ctx.close()

        # 5) reduced motion
        ctx = br.new_context(**mob, reduced_motion="reduce")
        pg = ctx.new_page()
        hgo(pg, base + "#/q/an-k1/real", wait_until="networkidle")
        pg.wait_for_selector("#timer")
        for _ in range(25):
            if pg.locator("#fin").count():
                pg.locator("#fin").click()
                break
            pg.locator(".opt").first.click() if pg.locator(".opt").count() else pg.fill("#inp", "1")
            pg.locator("#next").click()
        pg.wait_for_selector(".score")
        pg.wait_for_timeout(300)
        rm = pg.evaluate("({anims: document.getAnimations().filter(a => a.playState === 'running' && a.effect && a.effect.getComputedTiming().duration > 1).length, confetti: !!document.querySelector('#confetti'), vt: false})")
        info["reduced-motion"] = rm
        if rm["anims"] or rm["confetti"]:
            fails.append(f"reduced-motion: є рух {rm}")
        ctx.close()

        # 6) відновлення тесту після перезавантаження
        ctx = br.new_context(**mob)
        pg = ctx.new_page()
        hgo(pg, base + "#/q/an-k1/real", wait_until="networkidle")
        pg.wait_for_selector("#timer")
        first_q = pg.inner_text(".q > p")
        for _ in range(3):
            pg.locator(".opt").first.click() if pg.locator(".opt").count() else pg.fill("#inp", "7")
            pg.locator("#next").click()
        q4 = pg.inner_text(".q > p")
        pg.reload()
        pg.wait_for_selector("#timer")
        q4b = pg.inner_text(".q > p")
        counter = pg.inner_text(".qhead .num")
        pg.locator("#prev").click(); pg.locator("#prev").click(); pg.locator("#prev").click()
        q1b = pg.inner_text(".q > p")
        resumed = q4 == q4b and first_q == q1b and counter.startswith("4 /")
        info["відновлення тесту після перезавантаження"] = resumed
        if not resumed:
            fails.append(f"тест не відновився: {counter}")
        ctx.close()

        # 7) плавність під 4x CPU throttling
        ctx = br.new_context(**mob)
        pg = ctx.new_page()
        pg.add_init_script(FRAMES)
        cdp = ctx.new_cdp_session(pg)
        hgo(pg, base + "#/q/an-k1/recall", wait_until="networkidle")
        pg.wait_for_selector("#show")
        cdp.send("Emulation.setCPUThrottlingRate", {"rate": 4})
        fps = {}

        def measure(label, fn, ms):
            pg.evaluate("window.__fr = []; window.__frOn = true")
            fn()
            pg.wait_for_timeout(ms)
            fr = pg.evaluate("window.__frOn = false, window.__fr")
            fr = fr[2:] if len(fr) > 4 else fr
            if not fr:
                fps[label] = "нема кадрів"
                return
            fr.sort()
            p95 = fr[int(len(fr) * 0.95) - 1]
            long_ = sum(1 for f in fr if f > 20) / len(fr)
            fps[label] = {"кадрів": len(fr), "медіана мс": round(statistics.median(fr), 1), "p95 мс": round(p95, 1),
                          "кадрів > 20 мс %": round(100 * long_, 1), "fps": round(1000 / statistics.mean(fr), 1),
                          "довгі кадри мс": [round(f) for f in fr if f > 20]}

        measure("переворот картки", lambda: pg.locator("#show").click(), 700)

        def swipe():
            box = pg.locator("#drag").bounding_box()
            cx, cy = box["x"] + box["width"] / 2, box["y"] + box["height"] / 2
            pg.mouse.move(cx, cy)
            pg.mouse.down()
            for k in range(1, 13):
                pg.mouse.move(cx + k * 20, cy)
                pg.wait_for_timeout(16)
            pg.mouse.up()
        measure("свайп картки і виліт", swipe, 900)
        hgo(pg, base + "#/q/an-k1/real")
        pg.wait_for_selector("#timer")
        for _ in range(25):
            if pg.locator("#fin").count():
                break
            pg.locator(".opt").first.click() if pg.locator(".opt").count() else pg.fill("#inp", "1")
            pg.locator("#next").click()
        measure("результат: конфеті, кільце, лічильник", lambda: pg.locator("#fin").click(), 1600)
        hgo(pg, base + "#/subjects")
        pg.wait_for_selector(".unit")
        measure("перехід між екранами", lambda: pg.locator(".bnav a[href='#/']").click(), 700)
        cdp.send("Emulation.setCPUThrottlingRate", {"rate": 1})
        info["кадри під 4x CPU"] = fps
        ctx.close()

        # 8) відео проходу
        if vid_dir:
            vid_dir.mkdir(parents=True, exist_ok=True)
            ctx = br.new_context(**mob, record_video_dir=str(vid_dir), record_video_size={"width": 390, "height": 844})
            pg = ctx.new_page()
            pg.goto(base, wait_until="networkidle")
            pg.wait_for_timeout(1500)
            hgo(pg, base + "#/q/ma-k2/train")
            pg.wait_for_selector(".q")
            for k in range(4):
                if pg.locator(".opt").count():
                    pg.locator(".opt").nth(k % pg.locator(".opt").count()).click()
                    if pg.locator("#check").count():
                        pg.locator("#check").click()
                else:
                    pg.fill("#inp", "2")
                    pg.locator("#check").click()
                pg.wait_for_timeout(1100)
                pg.locator("#next").click() if k < 3 else None
                pg.wait_for_timeout(400)
            pg.locator("#fin").click() if pg.locator("#fin").count() else None
            hgo(pg, base + "#/q/ma-k2/real")
            pg.wait_for_selector("#timer")
            for _ in range(20):
                if pg.locator("#fin").count():
                    break
                pg.locator(".opt").first.click() if pg.locator(".opt").count() else pg.fill("#inp", "1")
                pg.locator("#next").click()
            pg.locator("#fin").click()
            pg.wait_for_timeout(2200)
            hgo(pg, base + "#/q/an-k1/recall")
            pg.wait_for_selector("#show")
            pg.wait_for_timeout(700)
            for right in (True, False, True):
                pg.locator("#show").click()
                pg.wait_for_timeout(900)
                box = pg.locator("#drag").bounding_box()
                cx, cy = box["x"] + box["width"] / 2, box["y"] + box["height"] / 2
                pg.mouse.move(cx, cy)
                pg.mouse.down()
                for k in range(1, 15):
                    pg.mouse.move(cx + (k * 16 if right else -k * 16), cy + k)
                    pg.wait_for_timeout(22)
                pg.mouse.up()
                pg.wait_for_timeout(900)
                if pg.locator("#go").count():
                    pg.locator("#go").click()
                    pg.wait_for_timeout(600)
            info["відео"] = pg.video.path()
            ctx.close()
        br.close()
    print(json.dumps(info, ensure_ascii=False, indent=1))
    if fails:
        print(f"ПРОБЛЕМ {len(fails)}:")
        for f in fails[:60]:
            print("  ", f)
        return 1
    print("OK: усі перевірки вигляду і руху пройдено")
    return 0


if __name__ == "__main__":
    sys.exit(main())
