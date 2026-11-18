"""E2E розділу «Linux Mint - повністю» (mint, ULINUX2 18.11.2026). Помічники - з tools/prog_e2e.py (UNIPROG1).

  python -X utf8 -E tools/mint_e2e.py              # локально (http.server на site/ у потоці)
  python -X utf8 -E tools/mint_e2e.py https://...  # живий сайт

1. Предмети: картка mint у групі «Навички».
2. Вкладки (Уроки, Теорія, Задачі, Шпаргалка, Тести) і ВСІ 27 сторінок уроків на 390 і 1440: консоль чиста, нема 4xx,
   нема горизонтальної прокрутки сторінки, LaTeX, довгих тире, сирого Markdown у <details>; на сторінці уроку
   активна вкладка «Уроки». Знімки - tools/e2e-shots/mint-*.png.
3. files/ustanovka-mint.sh віддається (200) і байт у байт = курс.
4. Тест: 15 питань за ключем (кожне третє навмисно хибно) - бал зійшовся.
5. Офлайн: дочекатися кешу, вимкнути мережу, перезавантажити - усі вкладки, усі 27 уроків і тест працюють.
"""
import json
import sys
import urllib.request
from pathlib import Path

from playwright.sync_api import sync_playwright

sys.path.insert(0, str(Path(__file__).resolve().parent))
from prog_e2e import SHOTS, goto, serve  # noqa: E402

U = "mint"
TABS = ["uroky", "teoriya", "zadachi", "shpargalka", "test"]
# UPROGONE: частина живе в prog - стара вкладка -> сторінка prog
NEW = {"uroky": "mint", "teoriya": "mint-start", "zadachi": "mint-zadachi", "shpargalka": "mint-shpargalka", "test": "test"}


def new(key):
    return NEW.get(key) or "mint-" + key.split("-")[1]

COURSE_SH = Path(r"D:\Універ\05_Програмування\Linux-Mint\ustanovka-mint.sh")
CHECK_JS = """() => {
  const doc = document.querySelector('article.doc') || document.body;
  const t = doc.innerText;
  return {
    hscroll: document.documentElement.scrollWidth > window.innerWidth + 1,
    latex: /\\$\\$|\\\\frac|begin\\{/.test(t),
    dash: /[\\u2013\\u2014]/.test(t),
    rawmd: [...doc.querySelectorAll('details')].some(d => /^\\s*(```|#{2,} |\\*\\*[^*]+\\*\\*)/m.test(d.innerText)),
    len: t.length,
    h1: (document.querySelector('article.doc h1') || {}).textContent || '',
    links: [...doc.querySelectorAll('a[href^="#/u/prog/mint-"]')].filter(a => /^#\\/u\\/prog\\/mint-\\d\\d$/.test(a.getAttribute('href'))).length,
    cur: (document.querySelector('nav.tabs a[aria-current="page"]') || {}).textContent || '',
    tabsVisible: [...document.querySelectorAll('nav.tabs a')].every(a => a.getBoundingClientRect().right <= window.innerWidth + 1),
  };
}"""


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    base = sys.argv[1] if len(sys.argv) > 1 else serve()
    if not base.endswith("/"):
        base += "/"
    fails, st = [], {"states": 0, "test_q": 0}

    def fail(msg):
        fails.append(msg)
        print("FAIL", msg[:500])

    # 3. скрипт для wget
    try:
        got = urllib.request.urlopen(base + "files/ustanovka-mint.sh", timeout=30).read()
        want = COURSE_SH.read_bytes().replace(b"\r\n", b"\n")
        print(f"files/ustanovka-mint.sh: {len(got)} байт, = курс: {got == want}")
        if got != want:
            fail("files/ustanovka-mint.sh не збігається з курсом")
    except Exception as e:  # noqa: BLE001
        fail(f"files/ustanovka-mint.sh: {e}")

    uroky = [f"urok-{n:02d}" for n in range(1, 28)]
    with sync_playwright() as p:
        br = p.chromium.launch(headless=True)
        for w, h, mob in ((390, 844, True), (1440, 900, False)):
            ctx = br.new_context(viewport={"width": w, "height": h}, is_mobile=mob, has_touch=mob, service_workers="block")
            page = ctx.new_page()
            errs = []
            page.on("console", lambda m: errs.append(m.text) if m.type == "error" else None)
            page.on("pageerror", lambda e: errs.append(str(e)))
            page.on("response", lambda r: errs.append(f"{r.status} {r.url}") if r.status >= 400 else None)
            goto(page, base, "/subjects")
            # UPROGONE: окремого розділу нема - лише «Програмування», де ця частина всередині
            info = page.evaluate("""() => ({old: document.querySelectorAll('a[href="#/u/mint"]').length,
                prog: document.querySelectorAll('a.unit[href="#/u/prog"]').length})""")
            if info["old"] or info["prog"] != 1:
                fail(f"{w}px: у «Предметах» старий розділ або нема «Програмування»: {info}")
            for key in TABS + uroky:
                goto(page, base, f"/u/prog/{new(key)}")
                page.wait_for_timeout(250)
                st["states"] += 1
                r = page.evaluate(CHECK_JS)
                if key in TABS or key in ("urok-01", "urok-04", "urok-06"):
                    page.screenshot(path=str(SHOTS / f"mint-{key}-{w}.png"), full_page=False)
                for k in ("hscroll", "latex", "dash", "rawmd"):
                    if r[k]:
                        fail(f"{w}px {key}: {k}")
                if not r["tabsVisible"]:
                    fail(f"{w}px {key}: вкладка за краєм екрана")
                if key == "uroky" and r["links"] != 27:
                    fail(f"{w}px уроки: посилань на уроки {r['links']}, чекав 27")
                if key.startswith("urok-"):
                    if r["cur"].strip() != "Шлях":
                        fail(f"{w}px {key}: активна вкладка {r['cur']!r}, чекав «Шлях»")
                    if r["len"] < 3000:
                        fail(f"{w}px {key}: замало тексту ({r['len']})")
                if key == "zadachi" and r["len"] < 20000:
                    fail(f"{w}px задачі: замало тексту ({r['len']})")
            if errs:
                fail(f"{w}px: консоль/4xx: {errs[:5]}")
            ctx.close()

        # 4. тест за ключем (390)
        ctx = br.new_context(viewport={"width": 390, "height": 844}, is_mobile=True, has_touch=True, service_workers="block")
        page = ctx.new_page()
        perrs = []
        page.on("pageerror", lambda e: perrs.append(str(e)))
        goto(page, base, "/u/prog/test")
        quiz = json.loads(page.evaluate(f"fetch('data/{U}/quiz.json').then(r => r.text())"))
        bank = {}
        for q in quiz["questions"]:
            bank.setdefault(q["q"], []).append(q)
        goto(page, base, f"/q/{U}/real")
        page.wait_for_selector(".card.q", timeout=10000)
        right_planned = 0
        for i in range(15):
            page.wait_for_function("i => document.querySelector('.qhead .num') && document.querySelector('.qhead .num').textContent.trim().startsWith((i + 1) + ' /')", arg=i, timeout=10000)
            qtext = page.evaluate("""() => { const p = document.querySelector('.card.q p'); const t = document.createElement('textarea'); t.innerHTML = p.innerHTML.replace(/<br>/g, '\\n'); return t.value; }""")
            cands = bank.get(qtext, [])
            if len(cands) != 1:
                plain = page.evaluate("document.querySelector('.card.q p').innerText")
                cands = [q for q in quiz["questions"] if q["q"].replace("`", "") == plain]
            if len(cands) != 1:
                fail(f"тест: питання {i + 1} не знайдено в банку: {qtext[:80]!r}")
                break
            q = cands[0]
            st["test_q"] += 1
            want_right = i % 3 != 2
            right_planned += want_right
            if q["type"] == "single":
                k = q["answer"] if want_right else next(j for j in range(len(q["options"])) if j != q["answer"])
                page.click(f'.card.q .opts button[data-o="{k}"]')
            else:
                page.fill("#inp", q["answer"] if want_right else "не знаю")
            if i == 0:
                page.screenshot(path=str(SHOTS / "mint-test-q1-390.png"))
            page.click("#next" if i < 14 else "#fin")
        page.wait_for_selector("#cnt", timeout=10000)
        page.wait_for_timeout(1800)
        got = page.evaluate("[document.querySelector('#cnt').textContent, document.querySelector('.score').textContent]")
        print(f"тест: питань {st['test_q']}, правильних за планом {right_planned}; на екрані {got[1]!r}")
        if int(got[0]) != right_planned or "/ 15" not in got[1]:
            fail(f"тест: бал не зійшовся (план {right_planned}): {got}")
        page.screenshot(path=str(SHOTS / "mint-test-result-390.png"))
        if perrs:
            fail(f"pageerror: {perrs[:3]}")
        ctx.close()

        # 5. офлайн
        ctx = br.new_context(viewport={"width": 390, "height": 844}, is_mobile=True, has_touch=True, service_workers="allow")
        page = ctx.new_page()
        goto(page, base, "/u/prog/mint")
        page.wait_for_function("navigator.serviceWorker.controller !== null", timeout=30000)
        page.wait_for_function("""async () => { const k = await caches.keys(); const n = k.find(x => x.startsWith('uniprep-'));
            if (!n) return false; const c = await caches.open(n); return (await c.keys()).length > 140; }""", timeout=90000)
        ctx.set_offline(True)
        page.reload()
        short = {}
        for key in TABS[:-1] + uroky:
            goto(page, base, f"/u/prog/{new(key)}")
            page.wait_for_timeout(200)
            n = page.evaluate("(document.querySelector('article.doc') || document.body).innerText.length")
            if n < 2000:
                short[key] = n
        goto(page, base, f"/q/{U}/real")
        page.wait_for_selector(".card.q", timeout=10000)
        page.screenshot(path=str(SHOTS / "mint-offline-test-390.png"))
        print(f"офлайн: {len(TABS) - 1 + len(uroky)} сторінок відкрито, коротких: {short}; тест стартував")
        if short:
            fail(f"офлайн: порожні сторінки {short}")
        ctx.close()
        br.close()
    print("Статистика:", st)
    if fails:
        print(f"ПРОБЛЕМ: {len(fails)}")
        sys.exit(1)
    print("OK")


if __name__ == "__main__":
    main()
