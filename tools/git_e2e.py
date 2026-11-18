"""E2E розділу «Git і GitHub» (git, UGIT1 18.11.2026). Помічники - з tools/prog_e2e.py (UNIPROG1).

  python -X utf8 -E tools/git_e2e.py              # локально (http.server на site/ у потоці)
  python -X utf8 -E tools/git_e2e.py https://...  # живий сайт

1. Предмети: картка git у групі «Навички».
2. Вкладки (Теорія, Задачі, Шпаргалка, Тести) на 390 і 1440: консоль чиста, нема 4xx, нема горизонтальної прокрутки,
   нема LaTeX, довгих тире, сирого Markdown у <details>; у Теорії 19 тем (0-18), у Задачах 4 завдання і 20 питань іспиту.
   Знімки - tools/e2e-shots/git-*.png.
3. Тест: старт, 15 питань, відповісти за ключем (кожне третє навмисно хибно) - бал зійшовся.
4. Офлайн: відкрити, дочекатися кешу, вимкнути мережу, перезавантажити - теорія, задачі, шпаргалка і тест працюють.
"""
import json
import sys
from pathlib import Path

from playwright.sync_api import sync_playwright

sys.path.insert(0, str(Path(__file__).resolve().parent))
from prog_e2e import SHOTS, goto, serve  # noqa: E402

U = "git"
TABS = ["teoriya", "zadachi", "shpargalka", "test"]
CHECK_JS = """() => {
  const doc = document.querySelector('article.doc') || document.body;
  const t = doc.innerText;
  return {
    hscroll: document.documentElement.scrollWidth > window.innerWidth + 1,
    latex: /\\$\\$|\\\\frac|begin\\{/.test(t),
    dash: /[\\u2013\\u2014]/.test(t),
    rawmd: [...doc.querySelectorAll('details')].some(d => /^\\s*(```|#{2,} |\\*\\*[^*]+\\*\\*)/m.test(d.innerText)),
    h2: [...doc.querySelectorAll('h2')].map(h => h.textContent.trim()),
    h3: [...doc.querySelectorAll('h3')].map(h => h.textContent.trim()),
    tabsVisible: [...document.querySelectorAll('nav.tabs a, .tabs a')].every(a => a.getBoundingClientRect().right <= window.innerWidth + 1),
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
            info = page.evaluate("""() => { const a = document.querySelector('a[href="#/u/git"]');
                if (!a) return null; const d = a.closest('details'); return {sum: d ? d.querySelector('summary').textContent : '', text: a.textContent}; }""")
            if not info or "Git" not in info["text"]:
                fail(f"{w}px: картки git у «Предметах» нема: {info}")
            else:
                print(f"{w}px: картка: {info['text'].strip()[:70]!r} у групі {info['sum'].strip()[:30]!r}")
            for tab in TABS:
                goto(page, base, f"/u/{U}/{tab}")
                page.wait_for_timeout(400)
                st["states"] += 1
                r = page.evaluate(CHECK_JS)
                page.screenshot(path=str(SHOTS / f"git-{tab}-{w}.png"), full_page=False)
                for k in ("hscroll", "latex", "dash", "rawmd"):
                    if r[k]:
                        fail(f"{w}px {tab}: {k}")
                if not r["tabsVisible"]:
                    fail(f"{w}px {tab}: вкладка за краєм екрана")
                if tab == "teoriya":
                    tem = [x for x in r["h2"] if x.startswith("Тема ")]
                    if len(tem) != 19:
                        fail(f"{w}px теорія: тем {len(tem)}, чекав 19: {tem[:3]}...")
                if tab == "zadachi":
                    blob = " ".join(r["h2"] + r["h3"])
                    if "Іспит" not in blob or "Чотири завдання" not in blob:
                        fail(f"{w}px задачі: нема розділів практики/іспиту: {r['h2']}")
            if errs:
                fail(f"{w}px: консоль/4xx: {errs[:5]}")
            ctx.close()

        # ---- 3. тест за ключем (390, як телефон) ----
        ctx = br.new_context(viewport={"width": 390, "height": 844}, is_mobile=True, has_touch=True, service_workers="block")
        page = ctx.new_page()
        perrs = []
        page.on("pageerror", lambda e: perrs.append(str(e)))
        goto(page, base, f"/u/{U}/test")
        quiz = json.loads(page.evaluate(f"fetch('data/{U}/quiz.json').then(r => r.text())"))
        bank = {}
        for q in quiz["questions"]:
            bank.setdefault(q["q"], []).append(q)
        page.click(f'a[href="#/q/{U}/real"]')
        page.wait_for_selector(".card.q", timeout=10000)
        right_planned = 0
        for i in range(15):
            page.wait_for_function("i => document.querySelector('.qhead .num') && document.querySelector('.qhead .num').textContent.trim().startsWith((i + 1) + ' /')", arg=i, timeout=10000)
            qtext = page.evaluate("""() => { const p = document.querySelector('.card.q p'); const t = document.createElement('textarea'); t.innerHTML = p.innerHTML.replace(/<br>/g, '\\n'); return t.value; }""")
            cands = bank.get(qtext, [])
            if len(cands) != 1:
                # питання з кодом у тексті рендериться з <code> - звіряємо без розмітки
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
                page.screenshot(path=str(SHOTS / "git-test-q1-390.png"))
            page.click("#next" if i < 14 else "#fin")
        page.wait_for_selector("#cnt", timeout=10000)
        page.wait_for_timeout(1800)  # анімація countUp
        got = page.evaluate("[document.querySelector('#cnt').textContent, document.querySelector('.score').textContent]")
        print(f"тест: питань {st['test_q']}, правильних за планом {right_planned}; на екрані {got[1]!r}")
        if int(got[0]) != right_planned or "/ 15" not in got[1]:
            fail(f"тест: бал не зійшовся (план {right_planned}): {got}")
        page.screenshot(path=str(SHOTS / "git-test-result-390.png"))
        if perrs:
            fail(f"pageerror: {perrs[:3]}")
        ctx.close()

        # ---- 4. офлайн ----
        ctx = br.new_context(viewport={"width": 390, "height": 844}, is_mobile=True, has_touch=True, service_workers="allow")
        page = ctx.new_page()
        goto(page, base, f"/u/{U}/teoriya")
        page.wait_for_function("navigator.serviceWorker.controller !== null", timeout=30000)
        page.wait_for_function("""async () => { const k = await caches.keys(); const n = k.find(x => x.startsWith('uniprep-'));
            if (!n) return false; const c = await caches.open(n); return (await c.keys()).length > 90; }""", timeout=60000)
        ctx.set_offline(True)
        page.reload()
        ok = {}
        for tab in TABS:
            goto(page, base, f"/u/{U}/{tab}")
            page.wait_for_timeout(300)
            ok[tab] = page.evaluate("(document.querySelector('article.doc') || document.body).innerText.length")
        page.click(f'a[href="#/q/{U}/real"]')
        page.wait_for_selector(".card.q", timeout=10000)
        ok["test_started"] = True
        page.screenshot(path=str(SHOTS / "git-offline-test-390.png"))
        print(f"офлайн: довжина тексту вкладок {ok}")
        if min(v for k, v in ok.items() if k != "test_started") < 200:
            fail(f"офлайн: порожня вкладка {ok}")
        ctx.close()
        br.close()
    print("Статистика:", st)
    if fails:
        print(f"ПРОБЛЕМ: {len(fails)}")
        sys.exit(1)
    print("OK")


if __name__ == "__main__":
    main()
