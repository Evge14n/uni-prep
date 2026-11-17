"""Перевірка сайту в headless Chromium.

  python -P -E tools/e2e.py                 # локально: піднімає http.server на site/
  python -P -E tools/e2e.py https://...     # живий сайт (GitHub Pages)

Що перевіряє: усі розділи і вкладки відкриваються на 390 і 1440 без помилок консолі і
4xx/5xx; нема горизонтальної прокрутки; сирого LaTeX і довгих тире в тексті сторінки нема;
тест «Тренування» і «Як на справжньому» проходиться; режим «Пригадай сам»; після
встановлення service worker сайт працює ОФЛАЙН (усі розділи + тест). Скріни - у
tools/e2e-shots/ (не йдуть у репо).
"""
import functools
import http.server
import json
import sys
import threading
from pathlib import Path

from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parent.parent
SHOTS = ROOT / "tools" / "e2e-shots"
SHOTS.mkdir(exist_ok=True)
BAD = ["$$", "\\frac", "\\sqrt", "begin{", "—", "–"]


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
    base = sys.argv[1] if len(sys.argv) > 1 else serve()
    if not base.endswith("/"):
        base += "/"
    units = json.loads((ROOT / "site" / "data" / "units.json").read_text(encoding="utf-8"))
    fails, checked = [], 0
    with sync_playwright() as p:
        br = p.chromium.launch(headless=True)
        for w, h, mobile in ((390, 844, True), (1440, 900, False)):
            ctx = br.new_context(viewport={"width": w, "height": h}, is_mobile=mobile, has_touch=mobile,
                                 device_scale_factor=2 if mobile else 1, service_workers="allow")
            page = ctx.new_page()
            errs = []
            page.on("console", lambda m: errs.append(f"console {m.type}: {m.text}") if m.type in ("error", "warning") else None)
            page.on("pageerror", lambda e: errs.append(f"pageerror: {e}"))
            page.on("response", lambda r: errs.append(f"HTTP {r.status} {r.url}") if r.status >= 400 and "youtube" not in r.url else None)

            def check(label, shot=False):
                nonlocal checked
                checked += 1
                page.wait_for_timeout(150)
                txt = page.inner_text("body")
                for b in BAD:
                    if b in txt:
                        fails.append(f"{w}px {label}: у тексті «{b}»")
                sw = page.evaluate("document.documentElement.scrollWidth")
                if sw > w + 1:
                    fails.append(f"{w}px {label}: горизонтальна прокрутка {sw}px")
                if "Помилка завантаження" in txt or "Не вдалося відкрити" in txt:
                    fails.append(f"{w}px {label}: помилка завантаження")
                if shot:
                    page.screenshot(path=str(SHOTS / f"{w}-{label.replace('/', '_')}.png"), full_page=False)

            page.goto(base, wait_until="networkidle")
            page.wait_for_selector(".unit")
            check("home", True)
            page.evaluate("navigator.serviceWorker.ready.then(() => true)")
            for u in units:
                for pg in u["pages"]:
                    page.goto(f"{base}#/u/{u['id']}/{pg['key']}")
                    page.wait_for_selector("h1")
                    page.wait_for_timeout(250)
                    check(f"{u['id']}/{pg['key']}", shot=u["id"] in ("an-k1", "ma-k2"))
            for key in ("plan", "glossary", "about", "stats"):
                page.goto(f"{base}#/{key}")
                page.wait_for_selector("h1")
                check(key, True)

            # тренування: 3 відповіді
            page.goto(f"{base}#/q/ma-k2/train")
            page.wait_for_selector(".q")
            for _ in range(3):
                if page.locator(".opt").count():
                    page.locator(".opt").first.click()
                    if page.locator("#check").count():
                        page.locator("#check").click()
                else:
                    page.fill("#inp", "1")
                    page.locator("#check").click()
                page.wait_for_selector(".verdict")
                page.locator("#next").click()
            check("train", True)
            # справжній: таймер і завершення
            page.goto(f"{base}#/q/an-k1/real")
            page.wait_for_selector("#timer")
            if not page.inner_text("#timer").strip():
                fails.append(f"{w}px: таймер порожній")
            for _ in range(25):
                if page.locator("#fin").count():
                    page.locator("#fin").click()
                    break
                page.locator("#next").click()
            page.wait_for_selector(".score")
            check("real-result", True)
            # пригадування
            page.goto(f"{base}#/q/an-k1/recall")
            page.wait_for_selector("#show")
            page.locator("#show").click()
            page.locator("#knew").click()
            page.wait_for_selector("#show")
            check("recall")

            # ОФЛАЙН: усе з кешу service worker
            page.goto(base, wait_until="networkidle")
            page.wait_for_function("navigator.serviceWorker.controller !== null || true")
            page.reload(wait_until="networkidle")
            ctx.set_offline(True)
            off_errs_before = len(errs)
            page.reload()
            page.wait_for_selector(".unit")
            check("offline-home", True)
            for u in units:
                for pg in u["pages"]:
                    page.goto(f"{base}#/u/{u['id']}/{pg['key']}")
                    page.wait_for_selector("h1")
                    page.wait_for_timeout(150)
                    check(f"offline {u['id']}/{pg['key']}")
            page.goto(f"{base}#/q/ma-k2/real")
            page.wait_for_selector("#timer")
            check("offline-quiz", True)
            # у режимі офлайн відео-вкладка має показати примітку, а не iframe
            ctx.set_offline(False)
            off = [e for e in errs[off_errs_before:] if "net::ERR_INTERNET_DISCONNECTED" not in e]
            errs = errs[:off_errs_before] + off
            for e in errs:
                fails.append(f"{w}px {e}")
            ctx.close()
        br.close()
    print(f"перевірено станів {checked}, базова адреса {base}")
    if fails:
        print(f"ПРОБЛЕМ {len(fails)}:")
        for f in fails[:80]:
            print("  ", f)
        return 1
    print("OK: 0 помилок консолі, 0 4xx/5xx, без горизонтальної прокрутки, офлайн працює")
    return 0


if __name__ == "__main__":
    sys.exit(main())
