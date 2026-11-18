"""E2E розділу «Програмування» (UNIPROG1): уроки, довідник, Python у браузері, офлайн.

  python -X utf8 -E tools/prog_e2e.py              # локально (http.server на site/ у потоці)
  python -X utf8 -E tools/prog_e2e.py https://...  # живий сайт

1. Кожен урок і довідник на 390 і 1440: консоль без помилок, нема 4xx, нема горизонтальної прокрутки,
   нема LaTeX і довгих тире.
2. У КОЖНОМУ уроці натискає «Запустити» на кожному блоці, після якого є блок з виводом, і порівнює вивід
   браузера з написаним (як check_kurs.py, але в Pyodide); doctest-сесії мусять бути зелені (крім # БАГ);
   заготовка задачі - doctest червоний, розвʼязок - зелений.
3. Довідник: кожен приклад-doctest - «Перевірити doctest» зелений.
4. Нескінченний цикл зупиняється за ≈ 10 с; input() бере значення з поля «Ввід».
5. Офлайн: відкрити розділ з інтернетом, «Завантажити Python», вимкнути мережу, перезавантажити -
   уроки, довідник і запуск коду працюють.
"""
import functools
import http.server
import re
import sys
import threading
import time
from pathlib import Path

from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parent.parent
SHOTS = ROOT / "tools" / "e2e-shots"
SHOTS.mkdir(exist_ok=True)
BAD = ["$$", "\\frac", "begin{", "—", "–"]
LESSONS = [f"urok-{n:02d}" for n in range(1, 10)]


class Quiet(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *a):
        pass


def serve():
    h = functools.partial(Quiet, directory=str(ROOT / "site"))
    srv = http.server.ThreadingHTTPServer(("127.0.0.1", 0), h)
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    return f"http://127.0.0.1:{srv.server_address[1]}/"


def norm(s):
    lines = [x.rstrip() for x in s.replace("\r\n", "\n").split("\n")]
    while lines and not lines[-1]:
        lines.pop()
    return lines


ERR = re.compile(r"^[A-Za-z_]*(Error|Exception|Interrupt|Exit|Iteration)\b")

# JS: знайти блоки python і їх очікуваний вивід (наступний pre з language-text до наступного python)
PAIRS_JS = """() => {
  const pres = [...document.querySelectorAll('article.doc pre:not(.pyout)')];
  const out = [];
  pres.forEach((p, i) => {
    const c = p.querySelector('code.language-python');
    if (!c) return;
    // очікуваний вивід - як у check_kurs.py: одразу після блоку (крім кнопок), або перший блок у наступному
    // <details>, або після короткого абзацу «Вивід:»
    let e = p.nextElementSibling;
    while (e && (e.classList.contains('pybar') || e.classList.contains('pyin') || e.classList.contains('pyout'))) e = e.nextElementSibling;
    if (e && e.tagName === 'P' && /^(Вивід|Відповідь|Результат|Що виведе)/.test(e.textContent.trim()) && e.textContent.trim().length < 40) e = e.nextElementSibling;
    if (e && e.tagName === 'DETAILS') e = [...e.children].find(x => x.tagName !== 'SUMMARY');
    const t = e && e.tagName === 'PRE' && e.querySelector('code.language-text') ? e.querySelector('code.language-text').textContent : null;
    out.push({i, text: c.textContent, expected: t});
  });
  return out;
}"""


def goto(page, base, hash_):
    page.goto(base + "#" + hash_)
    page.wait_for_function("h => document.querySelector('#app') && document.querySelector('#app').dataset.route === h",
                           arg="#" + hash_, timeout=20000)
    page.wait_for_timeout(200)


def run_block(page, idx, button_text, timeout=60000):
    """Натиснути кнопку під idx-м python-блоком і дочекатись результату. Повертає текст виводу."""
    return page.evaluate("""async ([idx, label, timeout]) => {
      const pres = [...document.querySelectorAll('article.doc pre:not(.pyout)')];
      const pre = pres[idx];
      const d = pre.closest('details'); if (d) d.open = true;
      const bar = pre.nextElementSibling;
      const b = [...bar.querySelectorAll('button')].find(x => x.textContent === label);
      if (!b) return '__NOBUTTON__';
      let out = bar.nextElementSibling; while (out && !out.classList.contains('pyout')) out = out.nextElementSibling;
      b.click();
      const t0 = Date.now();
      await new Promise(r => setTimeout(r, 30));
      while (Date.now() - t0 < timeout) {
        if (!b.disabled && !out.hidden && !/^(Завантажую|Виконую)/.test(out.textContent)) break;
        await new Promise(r => setTimeout(r, 40));
      }
      return out.textContent + (out.classList.contains('bad') ? '\\n__BAD__' : '');
    }""", [idx, button_text, timeout])


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    base = sys.argv[1] if len(sys.argv) > 1 else serve()
    if not base.endswith("/"):
        base += "/"
    fails, stats = [], {"pages": 0, "compared": 0, "sessions": 0, "tasks": 0, "dov": 0}

    def fail(msg):
        fails.append(msg)
        print("FAIL", msg[:400])

    with sync_playwright() as p:
        br = p.chromium.launch(headless=True)
        # ---- 1. вигляд на 390 і 1440 ----
        for w, h, mob in ((390, 844, True), (1440, 900, False)):
            ctx = br.new_context(viewport={"width": w, "height": h}, is_mobile=mob, has_touch=mob,
                                 service_workers="block")
            page = ctx.new_page()
            errs = []
            page.on("console", lambda m: errs.append(f"console {m.type}: {m.text}") if m.type == "error" else None)
            page.on("pageerror", lambda e: errs.append(f"pageerror: {e}"))
            page.on("response", lambda r: errs.append(f"HTTP {r.status} {r.url}") if r.status >= 400 else None)
            for key in ["uroky", "dovidnyk"] + LESSONS:
                goto(page, base, f"/u/prog/{key}")
                stats["pages"] += 1
                sw = page.evaluate("document.documentElement.scrollWidth - window.innerWidth")
                if sw > 1:
                    fail(f"{w}px {key}: горизонтальна прокрутка {sw}px")
                txt = page.inner_text("#app")
                for b in BAD:
                    if b in txt:
                        fail(f"{w}px {key}: у тексті '{b}'")
                cur = page.evaluate("(document.querySelector('.tabs a[aria-current]')||{}).textContent")
                if key.startswith("urok") and cur not in ("Уроки", "Уроки Python"):  # UPROGONE: вкладка «Уроки Python»
                    fail(f"{key}: активна вкладка {cur}, а не Уроки")
                if key == "urok-01":
                    page.screenshot(path=str(SHOTS / f"prog-{key}-{w}.png"))
            if errs:
                fail(f"{w}px: помилки консолі/мережі: {errs[:5]}")
            ctx.close()

        # ---- 2-4. запуск коду ----
        ctx = br.new_context(viewport={"width": 1440, "height": 900}, service_workers="block")
        page = ctx.new_page()
        perrs = []
        page.on("pageerror", lambda e: perrs.append(str(e)))
        t_boot = time.time()
        for key in LESSONS:
            goto(page, base, f"/u/prog/{key}")
            blocks = page.evaluate(PAIRS_JS)
            for b in blocks:
                code = b["text"]
                head = "\n".join(code.split("\n")[:3])
                if "# не запускати" in head or re.search(r"^\s*(>>>\s*)?(import|from)\s+(turtle|matplotlib|numpy|tkinter)", code, re.M):
                    continue
                is_bug = "# БАГ" in head
                first = next((x for x in code.split("\n") if x.strip() and not x.strip().startswith("#")), "")
                if first.startswith(">>>"):
                    out = run_block(page, b["i"], "Перевірити doctest")
                    stats["sessions"] += 1
                    green = "усе зелене" in out
                    if green == is_bug:
                        fail(f"{key} блок {b['i']}: doctest-сесія {'зелена, а це БАГ' if is_bug else 'не зелена'}: {out[-300:]}")
                    continue
                is_task = "doctest.testmod(verbose=True)" in code and "def " in code
                if is_task:
                    out = run_block(page, b["i"], "doctest -v")
                    stats["tasks"] += 1
                    stub = bool(re.search(r"^\s+pass\s*$", code, re.M))
                    passed = "Test passed." in out and "__BAD__" not in out
                    if stub and passed:
                        fail(f"{key}: заготовка задачі пройшла doctest")
                    if not stub and not passed:
                        fail(f"{key}: розвʼязок задачі не пройшов doctest у браузері: {out[-400:]}")
                    continue
                out = run_block(page, b["i"], "Запустити")
                if out == "__NOBUTTON__":
                    fail(f"{key} блок {b['i']}: нема кнопки Запустити")
                    continue
                if b["expected"] is None or is_bug:
                    continue
                stats["compared"] += 1
                got = norm(out.replace("\n__BAD__", ""))
                if got == ["(нічого не надруковано - програма нічого не виводить через print)"]:
                    got = []
                exp = norm(b["expected"])
                if exp and ERR.match(exp[-1]):
                    body = [x for x in exp[:-1] if not x.startswith("Traceback") and not x.startswith("  ")]
                    got_body = got[:got.index("Traceback (most recent call last):")] if "Traceback (most recent call last):" in got else got[:-1]
                    if not got or got[-1].strip() != exp[-1].strip() or got_body != body:
                        fail(f"{key} блок {b['i']}: помилка/вивід не збігається\nочікувалось {exp[-4:]}\nє {got[-6:]}")
                elif got != exp:
                    fail(f"{key} блок {b['i']}: вивід не збігається\nочікувалось {exp[:6]}\nє {got[:6]}")
        print(f"запуск уроків: {time.time() - t_boot:.0f} с")

        # нескінченний цикл і input()
        goto(page, base, "/u/prog/urok-01")
        page.evaluate("""() => { const c = document.querySelector('article.doc pre code.language-python');
            c.textContent = 'count = 0\\nwhile True:\\n    count += 1'; }""")
        t0 = time.time()
        out = run_block(page, 0, "Запустити", timeout=20000)
        dt = time.time() - t0
        if "Зупинено" not in out or dt > 15:
            fail(f"нескінченний цикл: {out[:100]} за {dt:.1f} с")
        page.evaluate("""() => { const c = document.querySelector('article.doc pre code.language-python');
            c.textContent = 'name = input(\"Імʼя: \")\\nage = int(input(\"Вік: \"))\\nprint(f\"{name}, через рік {age + 1}\")';
            const ta = document.querySelector('.pyin textarea'); if (ta) { ta.value = 'Євген\\n18'; } }""")
        has_ta = page.evaluate("!!document.querySelector('article.doc pre')?.nextElementSibling?.nextElementSibling?.querySelector('textarea')")
        page.evaluate("""() => { const ta = document.querySelector('article.doc pre').nextElementSibling.nextElementSibling.querySelector('textarea');
            ta.value = 'Євген\\n18'; }""")
        out = run_block(page, 0, "Запустити")
        if norm(out) != ["Імʼя: Євген", "Вік: 18", "Євген, через рік 19"]:
            fail(f"input(): {norm(out)} (поле вводу є: {has_ta})")
        print(f"нескінченний цикл зупинено за {dt:.1f} с; input ок")

        # ---- 3. довідник ----
        goto(page, base, "/u/prog/dovidnyk")
        blocks = page.evaluate(PAIRS_JS)
        for b in blocks:
            first = next((x for x in b["text"].split("\n") if x.strip() and not x.strip().startswith("#")), "")
            if not first.startswith(">>>") or re.search(
                    r"^\s*(>>>\s*)?(import|from)\s+(turtle|matplotlib|numpy)", b["text"], re.M):
                continue
            out = run_block(page, b["i"], "Перевірити doctest")
            stats["dov"] += 1
            if "усе зелене" not in out:
                fail(f"довідник блок {b['i']}: {out[-300:]}")
        if perrs:
            fail(f"pageerror: {perrs[:3]}")
        ctx.close()

        # ---- 5. офлайн ----
        ctx = br.new_context(viewport={"width": 390, "height": 844}, is_mobile=True, has_touch=True,
                             service_workers="allow")
        page = ctx.new_page()
        goto(page, base, "/u/prog/uroky")
        page.wait_for_function("navigator.serviceWorker.controller !== null", timeout=30000)
        page.wait_for_function("""async () => { const k = await caches.keys(); if (!k.some(x => x.startsWith('uniprep-'))) return false;
            const c = await caches.open(k.find(x => x.startsWith('uniprep-'))); return (await c.keys()).length > 90; }""", timeout=60000)
        page.click(".pyget")
        page.wait_for_function("document.querySelector('#pybox').textContent.includes('працює без інтернету')", timeout=120000)
        ctx.set_offline(True)
        page.reload()
        goto(page, base, "/u/prog/urok-03")
        out = run_block(page, 0, "Запустити", timeout=90000)
        ok_run = "Python не" not in out and "__NOBUTTON__" not in out and out.strip() != ""
        goto(page, base, "/u/prog/dovidnyk")
        n_dov = page.evaluate("document.querySelectorAll('article.doc details').length")
        goto(page, base, "/u/prog/urok-09")
        n9 = page.evaluate("document.querySelectorAll('article.doc pre').length")
        print(f"офлайн: запуск уроку 3 -> {out[:80]!r}; довідник статей {n_dov}; урок 9 блоків {n9}")
        if not ok_run or n_dov < 250 or n9 < 10:
            fail("офлайн не працює повністю")
        page.screenshot(path=str(SHOTS / "prog-offline-urok-09.png"))
        ctx.close()
        br.close()
    print("Статистика:", stats)
    if fails:
        print(f"ПРОБЛЕМ: {len(fails)}")
        sys.exit(1)
    print("OK")


if __name__ == "__main__":
    main()
