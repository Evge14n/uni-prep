"""Кадри розділу prog-sec на 390 px для перевірки очима (UPROGSEC1): предмети, приклад SQL після запуску,
задача, шпаргалка, питання тесту з кодом. python -X utf8 -E tools/progsec_shots.py [base]"""
import sys
from pathlib import Path

from playwright.sync_api import sync_playwright

sys.path.insert(0, str(Path(__file__).resolve().parent))
from prog_e2e import SHOTS, goto, run_block, serve  # noqa: E402


def main():
    base = sys.argv[1] if len(sys.argv) > 1 else serve()
    if not base.endswith("/"):
        base += "/"
    with sync_playwright() as p:
        br = p.chromium.launch(headless=True)
        ctx = br.new_context(viewport={"width": 390, "height": 844}, is_mobile=True, has_touch=True, service_workers="block")
        page = ctx.new_page()
        goto(page, base, "/subjects")
        page.evaluate("document.querySelectorAll('details.later').forEach(d => d.open = true)")
        page.locator('a[href="#/u/prog-sec"]').scroll_into_view_if_needed()
        page.screenshot(path=str(SHOTS / "progsec-subjects-390.png"))
        goto(page, base, "/u/prog-sec/teoriya")
        i = page.evaluate("""() => [...document.querySelectorAll('article.doc pre:not(.pyout)')]
            .findIndex(p => p.textContent.includes("OR '1'='1") && p.textContent.includes('f"SELECT'))""")
        run_block(page, i, "Запустити")
        page.evaluate("i => [...document.querySelectorAll('article.doc pre:not(.pyout)')][i].scrollIntoView()", i)
        page.screenshot(path=str(SHOTS / "progsec-sql-run-390.png"))
        goto(page, base, "/u/prog-sec/zadachi")
        run_block(page, 0, "doctest -v")
        page.evaluate("document.querySelector('article.doc h2').scrollIntoView()")
        page.screenshot(path=str(SHOTS / "progsec-zadacha-390.png"), full_page=False)
        goto(page, base, "/u/prog-sec/shpargalka")
        page.screenshot(path=str(SHOTS / "progsec-shpargalka-390.png"), full_page=True)
        goto(page, base, "/u/prog-sec/test")
        page.click('a[href="#/q/prog-sec/train"]')
        page.wait_for_selector(".card.q")
        for _ in range(15):
            if page.locator(".card.q pre").count():
                break
            page.click(".card.q .opts button >> nth=0") if page.locator(".card.q .opts button").count() else page.fill("#inp", "x")
            if page.locator("#check").count():
                page.click("#check")
            page.click("#next")
        page.screenshot(path=str(SHOTS / "progsec-test-code-390.png"))
        br.close()
    print("кадри в", SHOTS)


if __name__ == "__main__":
    main()
