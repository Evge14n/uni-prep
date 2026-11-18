"""E2E розділу «Python + безпека» (prog-sec, UPROGSEC1). Функції - з tools/prog_e2e.py (UNIPROG1).

  python -X utf8 -E tools/progsec_e2e.py              # локально (http.server на site/ у потоці)
  python -X utf8 -E tools/progsec_e2e.py https://...  # живий сайт

1. Предмети (#/subjects): картка prog-sec у групі «Навички», веде в розділ.
2. Кожна вкладка (Теорія, Задачі, Шпаргалка, Тести) на 390 і 1440: консоль без помилок, нема 4xx, нема
   горизонтальної прокрутки, LaTeX і довгих тире; усі вкладки видно на 390 px.
3. Теорія: «Запустити» на кожному прикладі - вивід у браузері = написаному (SQL-інʼєкція у sqlite3 теж);
   блок argon2 показує пояснення «запускай у терміналі», а не кнопку.
4. Задачі: заготовка - doctest червоний, розвʼязок - зелений (у браузері).
5. Тест: старт, 15 питань, на кожне відповісти за ключем (частину навмисно хибно) - бал зійшовся.
6. Офлайн: перше відкриття розділу, «Завантажити Python», мережу вимкнути, перезавантажити - теорія,
   задачі, тест відкриваються, приклад з sqlite3 запускається.
"""
import json
import re
import sys
import time
from pathlib import Path

from playwright.sync_api import sync_playwright

sys.path.insert(0, str(Path(__file__).resolve().parent))
from prog_e2e import BAD, ERR, PAIRS_JS, SHOTS, goto, norm, run_block, serve  # noqa: E402

U = "prog-sec"
# UPROGONE: теорія розрізана на теми всередині prog (sec = вступ, sec-01 ... sec-10)
TABS = ["sec"] + [f"sec-{n:02d}" for n in range(1, 11)] + ["sec-zadachi", "sec-shpargalka", "test"]
CODE = ["sec"] + [f"sec-{n:02d}" for n in range(1, 11)] + ["sec-zadachi"]


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    base = sys.argv[1] if len(sys.argv) > 1 else serve()
    if not base.endswith("/"):
        base += "/"
    fails, st = [], {"states": 0, "compared": 0, "stub_red": 0, "sol_green": 0, "skip_notes": 0, "test_q": 0}

    def fail(msg):
        fails.append(msg)
        print("FAIL", msg[:500])

    with sync_playwright() as p:
        br = p.chromium.launch(headless=True)
        # ---- 1-2. предмети і вкладки на 390/1440 ----
        for w, h, mob in ((390, 844, True), (1440, 900, False)):
            ctx = br.new_context(viewport={"width": w, "height": h}, is_mobile=mob, has_touch=mob, service_workers="block")
            page = ctx.new_page()
            errs = []
            page.on("console", lambda m: errs.append(m.text) if m.type == "error" else None)
            page.on("pageerror", lambda e: errs.append(str(e)))
            page.on("response", lambda r: errs.append(f"{r.status} {r.url}") if r.status >= 400 else None)
            goto(page, base, "/subjects")
            # UPROGONE: окремого розділу нема - лише «Програмування», де ця частина всередині
            info = page.evaluate("""() => ({old: document.querySelectorAll('a[href="#/u/prog-sec"]').length,
                prog: document.querySelectorAll('a.unit[href="#/u/prog"]').length})""")
            if info["old"] or info["prog"] != 1:
                fail(f"{w}px: у «Предметах» старий розділ або нема «Програмування»: {info}")
            for tab in TABS:
                goto(page, base, f"/u/prog/{tab}")
                st["states"] += 1
                if tab == "test":
                    page.wait_for_timeout(300)
                txt = page.inner_text("#app")
                for b in BAD:
                    if b in txt:
                        fail(f"{w}px {tab}: заборонене {b!r}")
                sw = page.evaluate("document.documentElement.scrollWidth - innerWidth")
                if sw > 1:
                    fail(f"{w}px {tab}: горизонтальна прокрутка {sw}px")
                hidden_tabs = page.evaluate("""() => [...document.querySelectorAll('.tabs a, nav.tabs a, .utabs a')]
                    .filter(a => { const r = a.getBoundingClientRect(); return r.right > innerWidth + 1 || r.left < -1; }).map(a => a.textContent)""")
                if hidden_tabs:
                    fail(f"{w}px {tab}: вкладки за краєм екрана: {hidden_tabs}")
                if tab == "sec-02":
                    page.screenshot(path=str(SHOTS / f"progsec-teoriya-{w}.png"))
            if errs:
                fail(f"{w}px: помилки консолі/мережі: {errs[:5]}")
            ctx.close()

        # ---- 3-4. код у браузері ----
        ctx = br.new_context(viewport={"width": 1440, "height": 900}, service_workers="block")
        page = ctx.new_page()
        perrs = []
        page.on("pageerror", lambda e: perrs.append(str(e)))
        t0 = time.time()
        for tab in CODE:
            goto(page, base, f"/u/prog/{tab}")
            for b in page.evaluate(PAIRS_JS):
                code = b["text"]
                head = "\n".join(code.split("\n")[:3])
                if "# не запускати" in head:
                    note = page.evaluate("""(i) => { const pre = [...document.querySelectorAll('article.doc pre:not(.pyout)')][i];
                        const n = pre.nextElementSibling && pre.nextElementSibling.querySelector('.pynote'); return n ? n.textContent : null; }""", b["i"])
                    st["skip_notes"] += 1
                    if not note or "терміналі" not in note or "turtle" in note:
                        fail(f"{tab} блок {b['i']}: замість пояснення «{note}»")
                    continue
                if "doctest.testmod(verbose=True)" in code:
                    out = run_block(page, b["i"], "doctest -v")
                    stub = bool(re.search(r"^\s+pass\s*$", code, re.M))
                    passed = "Test passed." in out and "__BAD__" not in out
                    if stub:
                        st["stub_red"] += 1
                        if passed:
                            fail(f"{tab}: заготовка пройшла doctest")
                    else:
                        st["sol_green"] += 1
                        if not passed:
                            fail(f"{tab}: розвʼязок червоний у браузері: {out[-400:]}")
                    continue
                out = run_block(page, b["i"], "Запустити")
                if out == "__NOBUTTON__":
                    fail(f"{tab} блок {b['i']}: нема кнопки")
                    continue
                if b["expected"] is None:
                    continue
                st["compared"] += 1
                got = norm(out.replace("\n__BAD__", ""))
                exp = norm(b["expected"])
                if got != exp:
                    fail(f"{tab} блок {b['i']}: вивід не збігся\nочікувалось {exp[:6]}\nє {got[:6]}")
        print(f"код у браузері: {time.time() - t0:.0f} с")

        # ---- 5. тест за ключем ----
        quiz = json.loads(page.evaluate(f"fetch('data/{U}/quiz.json').then(r => r.text())"))
        bank = {}
        for q in quiz["questions"]:
            bank.setdefault(q["q"], []).append(q)
        goto(page, base, "/u/prog/test")
        goto(page, base, f"/q/{U}/real")
        page.wait_for_selector(".card.q", timeout=10000)
        right_planned = 0
        for i in range(15):
            page.wait_for_function("i => document.querySelector('.qhead .num') && document.querySelector('.qhead .num').textContent.trim().startsWith((i + 1) + ' /')", arg=i, timeout=10000)
            qtext = page.evaluate("""() => { const p = document.querySelector('.card.q p'); const t = document.createElement('textarea'); t.innerHTML = p.innerHTML.replace(/<br>/g, '\\n'); return t.value; }""")
            pre = page.evaluate("(document.querySelector('.card.q pre') || {}).textContent || ''")
            cands = [q for q in bank.get(qtext, []) if (q.get("pre") or "") == pre]
            if len(cands) != 1:
                fail(f"тест: питання {i + 1} не знайдено в банку: {qtext[:60]!r}")
                break
            q = cands[0]
            st["test_q"] += 1
            want_right = i % 3 != 2
            right_planned += want_right
            if q["type"] in ("single", "multi"):
                idxs = q["answer"] if q["type"] == "multi" else [q["answer"]]
                if not want_right:
                    idxs = [next(k for k in range(len(q["options"])) if k not in idxs)]
                for k in idxs:
                    page.click(f'.card.q .opts button[data-o="{k}"]')
            else:
                page.fill("#inp", q["answer"] if want_right else "не знаю")
            if i < 14:
                page.click("#next")
            else:
                page.click("#fin")
        page.wait_for_selector("#cnt", timeout=10000)
        page.wait_for_timeout(1500)  # countUp
        got = page.evaluate("[document.querySelector('#cnt').textContent, document.querySelector('.score').textContent]")
        print(f"тест: відповів на {st['test_q']} питань, правильних за планом {right_planned}; на екрані {got[1]!r}")
        if int(got[0]) != right_planned or "/ 15" not in got[1]:
            fail(f"тест: бал не зійшовся (план {right_planned}): {got}")
        page.screenshot(path=str(SHOTS / "progsec-test-result.png"))
        if perrs:
            fail(f"pageerror: {perrs[:3]}")
        ctx.close()

        # ---- 6. офлайн ----
        ctx = br.new_context(viewport={"width": 390, "height": 844}, is_mobile=True, has_touch=True, service_workers="allow")
        page = ctx.new_page()
        goto(page, base, "/u/prog/sec")
        page.wait_for_function("navigator.serviceWorker.controller !== null", timeout=30000)
        page.wait_for_function("""async () => { const k = await caches.keys(); const n = k.find(x => x.startsWith('uniprep-'));
            if (!n) return false; const c = await caches.open(n); return (await c.keys()).length > 90; }""", timeout=60000)
        page.click(".pyget")
        page.wait_for_function("document.querySelector('#pybox').textContent.includes('працює без інтернету')", timeout=120000)
        ctx.set_offline(True)
        page.reload()
        goto(page, base, "/u/prog/sec-02")
        sql_idx = page.evaluate("""() => [...document.querySelectorAll('article.doc pre:not(.pyout)')]
            .findIndex(p => p.textContent.includes("OR '1'='1") && p.textContent.includes('f"SELECT'))""")
        out = run_block(page, sql_idx, "Запустити", timeout=90000)
        ok_sql = "('anna', 's-111'), ('bob', 's-222')" in out
        goto(page, base, "/u/prog/sec-zadachi")
        n_det = page.evaluate("document.querySelectorAll('article.doc details').length")
        goto(page, base, "/u/prog/test")
        has_test = page.locator(f'a[href="#/q/{U}/train"]').count() > 0
        page.screenshot(path=str(SHOTS / "progsec-offline-test.png"))
        print(f"офлайн: sqlite3-інʼєкція -> {ok_sql}; розвʼязків задач {n_det}; тест відкрився {has_test}")
        if not ok_sql or n_det < 10 or not has_test:
            fail(f"офлайн не працює повністю: {out[:200]!r}")
        ctx.close()
        br.close()
    print("Статистика:", st)
    if fails:
        print(f"ПРОБЛЕМ: {len(fails)}")
        sys.exit(1)
    print("OK")


if __name__ == "__main__":
    main()
