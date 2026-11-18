"""UPROGONE e2e: один розділ «Програмування» (Python + Linux Mint + Git + безпечний код + Linux у WSL).

  python -X utf8 -E tools/prog_one_e2e.py              # локально (http.server у потоці скрипта)
  python -X utf8 -E tools/prog_one_e2e.py https://...  # живий сайт

На 390 і 1440:
 1. «Усі предмети»: рівно один розділ програмування, жодного посилання на старі mint/git/linux/prog-sec.
 2. КОЖНА сторінка data/prog/*.html: без помилок завантаження, без горизонтальної прокрутки, без LaTeX і довгих тире,
    активна вкладка є і видна на екрані; на сторінках Python і безпеки є «Запустити», на Mint/Git/Linux - нема.
 3. Старі адреси (усі ключі meta.moved частин + невідома сторінка) перенаправляють на сторінку в prog.
 4. Якір #/u/prog/<сторінка>/<id>: потрібний заголовок на екрані, його <details> відкриті.
 5. Тест модуля (#/q/prog/mN): питання лише цього модуля, «Вийти» веде в модуль; картки модуля (kN) працюють.
 6. «Як на справжньому»: лише питання Python (залік).
 7. Прогрес зі старих розділів (ключі mint/..., git/... у localStorage) видно в кільці розділу, модуля, у «Слабких темах».
 8. Офлайн: після кешу service worker - усі сторінки prog, тест модуля і перенаправлення.
Консоль без помилок, жодної відповіді 4xx/5xx.
"""
import json
import re
import sys
import time
from pathlib import Path

from playwright.sync_api import sync_playwright

sys.path.insert(0, str(Path(__file__).resolve().parent))
from prog_e2e import BAD, SHOTS, serve  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "site" / "data"


def wait_route(page, hash_):
    # кириличні якорі location.hash віддає закодованими - порівнюємо розкодоване
    page.wait_for_function("h => { const a = document.querySelector('#app'); return a && a.dataset.route && decodeURIComponent(a.dataset.route) === h; }",
                           arg=hash_, timeout=20000)
    page.wait_for_timeout(150)


def goto(page, base, hash_):
    page.goto(base + "#" + hash_)
    wait_route(page, "#" + hash_)


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    base = sys.argv[1] if len(sys.argv) > 1 else serve()
    if not base.endswith("/"):
        base += "/"
    units = {u["id"]: u for u in json.loads((DATA / "units.json").read_text(encoding="utf-8"))}
    moduli = json.loads((DATA / "prog" / "moduli.json").read_text(encoding="utf-8"))
    keys = sorted(p.stem for p in (DATA / "prog").glob("*.html"))
    prog_q = {f"prog/{q['id']}" for q in json.loads((DATA / "prog" / "quiz.json").read_text(encoding="utf-8"))["questions"]}
    parts = [u for u in units.values() if u.get("parent") == "prog"]
    fails, st = [], {"pages": 0, "redirects": 0, "anchors": 0, "offline": 0}

    def fail(msg):
        fails.append(msg)
        print("FAIL", msg[:300])

    with sync_playwright() as p:
        br = p.chromium.launch(headless=True)
        for w, h, mob in ((390, 844, True), (1440, 900, False)):
            ctx = br.new_context(viewport={"width": w, "height": h}, is_mobile=mob, has_touch=mob, service_workers="allow")
            page = ctx.new_page()
            errs = []
            page.on("console", lambda m: errs.append(f"console {m.type}: {m.text}") if m.type == "error" else None)
            page.on("pageerror", lambda e: errs.append(f"pageerror: {e}"))
            page.on("response", lambda r: errs.append(f"HTTP {r.status} {r.url}") if r.status >= 400 and "youtube" not in r.url else None)

            # 1. «Усі предмети»
            goto(page, base, "/subjects")
            info = page.evaluate("""() => ({
              prog: document.querySelectorAll('a.unit[href="#/u/prog"]').length,
              old: [...document.querySelectorAll('a[href^="#/u/"]')].map(a => a.getAttribute('href')).filter(h => /^#\\/u\\/(mint|git|linux|prog-sec)(\\/|$)/.test(h)),
              text: (document.querySelector('a.unit[href="#/u/prog"]') || {}).innerText || ''})""")
            if info["prog"] != 1 or info["old"]:
                fail(f"{w}px subjects: розділів prog {info['prog']}, старі посилання {info['old']}")
            nall = units["prog"].get("nqAll")
            if f"{nall} питань" not in info["text"]:
                fail(f"{w}px subjects: у картці нема «{nall} питань»: {info['text'][:120]}")
            if w == 390:
                page.screenshot(path=str(SHOTS / "uprogone-subjects-390.png"), full_page=True)

            # 2. кожна сторінка prog
            for key in keys:
                if key in ("quiz", "moduli"):
                    continue
                goto(page, base, f"/u/prog/{key}")
                st["pages"] += 1
                r = page.evaluate("""() => {
                  const cur = document.querySelector('.tabs a[aria-current]');
                  const rc = cur ? cur.getBoundingClientRect() : null;
                  return {sw: document.documentElement.scrollWidth - innerWidth, txt: document.querySelector('#app').innerText,
                    tab: cur ? cur.textContent : null, vis: rc ? (rc.left >= 0 && rc.right <= innerWidth + 1) : false,
                    run: [...document.querySelectorAll('article.doc .pybtn')].filter(b => b.textContent === 'Запустити').length,
                    pre: document.querySelectorAll('article.doc pre code.language-python').length,
                    crumb: (document.querySelector('.crumb a') || {}).textContent || ''}; }""")
                if r["sw"] > 1:
                    fail(f"{w}px {key}: горизонтальна прокрутка {r['sw']}px")
                for b in BAD:
                    if b in r["txt"]:
                        fail(f"{w}px {key}: у тексті «{b}»")
                if "Не вдалося відкрити" in r["txt"] or "Помилка завантаження" in r["txt"]:
                    fail(f"{w}px {key}: сторінка не відкрилась")
                if not r["tab"] or not r["vis"]:
                    fail(f"{w}px {key}: активна вкладка {r['tab']!r}, видна {r['vis']}")
                term = re.match(r"^(mint|git|linux)(-|$)", key)
                if term and r["run"]:
                    fail(f"{w}px {key}: на сторінці термінала є «Запустити» ({r['run']})")
                if not term and r["pre"] and not r["run"] and key not in ("shpargalky", "vse"):
                    # блоки з turtle/matplotlib мають лише «Копіювати» - тоді хоч одна кнопка Копіювати мусить бути
                    if not page.evaluate("document.querySelectorAll('article.doc .pybar').length"):
                        fail(f"{w}px {key}: Python-код без кнопок")
                if key in moduli["pageModule"] and not re.match(r"^m\d$", key) and not r["crumb"].startswith("Модуль"):
                    fail(f"{w}px {key}: нема «Модуль N» над сторінкою")
                if w == 390 and key in ("shlyakh", "m1", "m8", "mint-04", "git-07", "sec-01", "vse", "shpargalky"):
                    page.screenshot(path=str(SHOTS / f"uprogone-{key}-390.png"), full_page=False)
            goto(page, base, "/u/prog/test")
            n_mod = page.evaluate("document.querySelectorAll('.topics.mods a').length")
            if n_mod != sum(1 for m in moduli["modules"] if m["keys"]):
                fail(f"{w}px test: тестів модулів {n_mod}")
            if w == 390:
                page.screenshot(path=str(SHOTS / "uprogone-test-390.png"), full_page=True)

            # 3. старі адреси
            for u in parts:
                for old, new in list(u["moved"].items()) + [("невідома", u["moved"][""])]:
                    src = f"#/u/{u['id']}" + (f"/{old}" if old else "")
                    page.goto(base + src)
                    try:
                        wait_route(page, f"#/u/prog/{new}")
                        st["redirects"] += 1
                    except Exception:
                        fail(f"{w}px {src} -> очікував #/u/prog/{new}, а маю {page.evaluate('location.hash')}")

            # 4. якорі з модулів
            for m in moduli["modules"]:
                html = (DATA / "prog" / f"m{m['n']}.html").read_text(encoding="utf-8")
                for href in re.findall(r'href="#/u/prog/([\w-]+/[^"]+)"', html)[:3]:
                    goto(page, base, f"/u/prog/{href}")
                    pg, anc = href.split("/", 1)
                    r = page.evaluate("""a => { const el = document.getElementById(a); if (!el) return null;
                       const rc = el.getBoundingClientRect(); const d = el.closest('details');
                       return {top: rc.top, open: d ? d.open : true, y: scrollY}; }""", anc)
                    st["anchors"] += 1
                    if not r or not (-5 <= r["top"] <= h * 0.6) or not r["open"]:
                        fail(f"{w}px якір {href}: {r}")

            # 5. тест і картки модуля
            for m in moduli["modules"][:3]:
                goto(page, base, f"/q/prog/m{m['n']}")
                page.wait_for_selector(".qhead")
                head = page.inner_text(".qhead")
                exit_href = page.get_attribute("#exit", "href")
                run = page.evaluate("JSON.parse(sessionStorage.getItem('uniprep:run') || 'null')")
                ks = set(run["keys"]) if run else set()
                if f"/ {len(m['keys'])}" not in head.replace("\n", " ") or exit_href != f"#/u/prog/m{m['n']}" or not ks or not ks <= set(m["keys"]):
                    fail(f"{w}px тест модуля {m['n']}: {head!r} вихід {exit_href} ключі поза модулем {len(ks - set(m['keys']))}")
                # відповісти на одне питання
                if page.locator(".opt").count():
                    page.locator(".opt").first.click()
                    if page.locator("#check").count():
                        page.locator("#check").click()
                elif page.locator("#inp").count():
                    page.fill("#inp", "1")
                    page.locator("#check").click()
                page.wait_for_selector(".verdict")
            goto(page, base, "/q/prog/k2")
            page.wait_for_selector("#show")
            if page.get_attribute("#exit", "href") != "#/u/prog/m2":
                fail(f"{w}px картки модуля 2: вихід {page.get_attribute('#exit', 'href')}")

            # 6. «як на справжньому» - лише Python
            goto(page, base, "/q/prog/real")
            page.wait_for_selector("#timer")
            run = page.evaluate("JSON.parse(sessionStorage.getItem('uniprep:run'))")
            if not run or len(run["keys"]) != units["prog"]["test"]["count"] or not set(run["keys"]) <= prog_q:
                fail(f"{w}px справжній тест: {len(run['keys']) if run else 0} питань, не з Python: {len(set(run['keys']) - prog_q) if run else '?'}")

            # 7. прогрес зі старих розділів
            mq = json.loads((DATA / "mint" / "quiz.json").read_text(encoding="utf-8"))["questions"][:6]
            gq = json.loads((DATA / "git" / "quiz.json").read_text(encoding="utf-8"))["questions"][:3]
            now = int(time.time() * 1000)
            seed = {"q": {**{f"mint/{q['id']}": {"r": 1, "w": 0, "t": q["topic"], "last": 1, "f": now - 2 * 86400000, "ts": now - 86400000, "lt": 1} for q in mq},
                          **{f"git/{q['id']}": {"r": 0, "w": 1, "t": q["topic"], "last": 0, "f": now, "ts": now} for q in gq}}, "d": {}}
            page.evaluate("s => { sessionStorage.clear(); localStorage.setItem('uniprep:v1', JSON.stringify(s)); }", seed)
            page.reload()
            goto(page, base, "/subjects")
            txt = page.inner_text('a.unit[href="#/u/prog"]')
            if "6 памʼятаю надовго" not in txt.replace("\n", " ") or "0%" in txt.replace(" ", ""):
                fail(f"{w}px прогрес mint не видно в розділі: {txt[:200]!r}")
            goto(page, base, "/u/prog/shlyakh")
            m1 = page.inner_text('[data-mod="1"]')
            if not re.search(r"[1-9]\d*%", m1.replace(" ", "")):
                fail(f"{w}px кільце модуля 1 порожнє: {m1[-40:]!r}")
            goto(page, base, "/u/prog/test")
            wrong = page.inner_text('a[href="#/q/prog/wrong"]')
            if "(3)" not in wrong:
                fail(f"{w}px «Лише помилки» не бачить git: {wrong!r}")
            goto(page, base, "/stats")
            cards = page.evaluate("[...document.querySelectorAll('#app .card h3')].map(x => x.textContent)")
            if any(re.search(r"Linux Mint|Git і GitHub", c) and "Програмування" not in c for c in cards) or not any("Програмування" in c for c in cards):
                fail(f"{w}px stats: картки {cards}")
            page.evaluate("() => { localStorage.removeItem('uniprep:v1'); sessionStorage.clear(); }")

            # 8. офлайн
            goto(page, base, "/u/prog/shlyakh")
            page.wait_for_function("navigator.serviceWorker.controller !== null", timeout=30000)
            page.wait_for_function("""async () => { const k = await caches.keys(); const n = k.find(x => x.startsWith('uniprep-'));
                if (!n) return false; const c = await caches.open(n); return (await c.keys()).length > 150; }""", timeout=90000)
            ctx.set_offline(True)
            page.reload()
            off_from = len(errs)
            for key in keys:
                if key in ("quiz", "moduli"):
                    continue
                goto(page, base, f"/u/prog/{key}")
                st["offline"] += 1
                if "Не вдалося відкрити" in page.inner_text("#app"):
                    fail(f"{w}px офлайн {key}: не відкрилась")
            goto(page, base, "/q/prog/m4")
            page.wait_for_selector(".qhead")
            page.goto(base + "#/u/git/teoriya")
            wait_route(page, "#/u/prog/git")
            ctx.set_offline(False)
            errs[off_from:] = [e for e in errs[off_from:] if "ERR_INTERNET_DISCONNECTED" not in e]
            if errs:
                fail(f"{w}px помилки консолі/мережі: {errs[:5]}")
            ctx.close()
        br.close()
    print("Статистика:", st)
    if fails:
        print(f"ПРОБЛЕМ: {len(fails)}")
        sys.exit(1)
    print("OK")


if __name__ == "__main__":
    main()
