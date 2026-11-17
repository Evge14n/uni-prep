"""Кадри до/після редизайну: 5 екранів x 390/1440 x світла/темна.

python -P -E tools/design_shots.py <base-url|local> <тека-виходу>
Math.random засіяний, тож тест і картки - ті самі питання в обох прогонах.
"""
import functools
import http.server
import sys
import threading
from pathlib import Path

from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parent.parent

SEED = """
(() => { let s = 20261117; Math.random = () => { s = (s * 1664525 + 1013904223) >>> 0; return s / 4294967296; }; })();
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
    base = sys.argv[1]
    if base == "local":
        base = serve()
    if not base.endswith("/"):
        base += "/"
    out = Path(sys.argv[2])
    out.mkdir(parents=True, exist_ok=True)
    with sync_playwright() as p:
        br = p.chromium.launch(headless=True)
        for w, h, mob in ((390, 844, True), (1440, 900, False)):
            for scheme in ("light", "dark"):
                ctx = br.new_context(viewport={"width": w, "height": h}, is_mobile=mob, has_touch=mob,
                                     device_scale_factor=2 if mob else 1, color_scheme=scheme,
                                     reduced_motion="reduce", service_workers="block")
                ctx.add_init_script(SEED)
                pg = ctx.new_page()
                tag = f"{w}-{scheme}"

                def shot(name):
                    pg.wait_for_timeout(450)
                    pg.screenshot(path=str(out / f"{tag}-{name}.png"))

                pg.goto(base, wait_until="networkidle")
                pg.wait_for_selector(".unit, .today, h1")
                shot("1-home")
                pg.goto(base + "#/u/an-k1/teoriya")
                pg.wait_for_selector("h1")
                shot("2-unit")
                pg.goto(base + "#/q/ma-k2/train")
                pg.wait_for_selector(".q")
                if pg.locator(".opt").count():
                    pg.locator(".opt").nth(1).click()
                    if pg.locator("#check").count():
                        pg.locator("#check").click()
                else:
                    pg.fill("#inp", "1")
                    pg.locator("#check").click()
                pg.wait_for_selector(".verdict")
                shot("3-test")
                pg.goto(base + "#/q/an-k1/recall")
                pg.wait_for_selector("#show")
                shot("4a-card")
                pg.locator("#show").click()
                pg.wait_for_selector("#knew")
                shot("4b-card-open")
                pg.goto(base + "#/plan")
                pg.wait_for_selector("h1")
                shot("5-plan")
                ctx.close()
        br.close()
    print("кадри:", out)


if __name__ == "__main__":
    main()
