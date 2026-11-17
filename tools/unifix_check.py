"""UNIFIX1 (17.11.2026): перевірка правок за прийомом UNIFINAL1F і режиму довгої памʼяті на сайті.

  python -P -E tools/unifix_check.py            # локально (http.server на site/)
  python -P -E tools/unifix_check.py https://... # живий сайт

Що перевіряє (headless Chromium, 390 і 1440, консоль/4xx):
 п.2  k2-055: 1,718 зараховано, 1,72 - ні (функція isRight сторінки);
 п.7  відео: «частини» дають потрібне відео/хвилину (мінор -> ЛА03 0:27, гіпербола -> АГ08, кут пряма-площина -> нічого),
      усі 6 головних відео аналітичної мають таймкод > 0;
 п.8  вкладки розділу на 390: усі в межах екрана, активна видна;
 п.10 «Сьогодні» бере тему з черги плану (колонки без дня тижня);
 п.11 старт тесту в розділах без відео - без запиту videos.json;
 памʼять: «знаю сьогодні» / «памʼятаю надовго» (правильно через ≥ 20 год), «Пригадай сам» = 20 карток з «поясни/виведи»,
      сусідні картки з різних тем, неділя = тест тижня, тест тижня проходиться до результату, «через місяць» через 4 тижні.
Скріни - tools/e2e-shots/unifix-*.png.
"""
import json
import sys
import time
from datetime import datetime
from pathlib import Path

from playwright.sync_api import sync_playwright

sys.path.insert(0, str(Path(__file__).resolve().parent))
from e2e import serve  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
SHOTS = ROOT / "tools" / "e2e-shots"
DAY = 86400000


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    base = sys.argv[1] if len(sys.argv) > 1 else serve()
    if not base.endswith("/"):
        base += "/"
    fails, ok = [], []

    def check(cond, label):
        (ok if cond else fails).append(label)
        print(("OK  " if cond else "FAIL") + " " + label)

    with sync_playwright() as p:
        br = p.chromium.launch(headless=True)
        for w, h, mobile in ((390, 844, True), (1440, 900, False)):
            ctx = br.new_context(viewport={"width": w, "height": h}, is_mobile=mobile, has_touch=mobile,
                                 device_scale_factor=2 if mobile else 1, reduced_motion="reduce")
            page = ctx.new_page()
            errs, reqs = [], []
            page.on("console", lambda m: errs.append(m.text) if m.type in ("error", "warning") else None)
            page.on("pageerror", lambda e: errs.append(str(e)))
            page.on("response", lambda r: errs.append(f"HTTP {r.status} {r.url}") if r.status >= 400 and "youtube" not in r.url else None)
            page.on("request", lambda r: reqs.append(r.url))

            def go(hash_, clock=None):
                page.goto(base + hash_)
                page.wait_for_function("(h) => document.querySelector('#app').dataset.route === h", arg=hash_ or "")
                page.wait_for_timeout(200)

            tag = f"[{w}]"
            go("#/")
            # п.2
            r = page.evaluate("""async () => { const d = await (await fetch('data/ma-k2/quiz.json')).json();
                const q = d.questions.find(x => x.id === 'k2-055');
                return [isRight(q, '1,718'), isRight(q, '1,7183'), isRight(q, '1,72'), isRight(q, '1,7')]; }""")
            check(r == [True, True, False, False], f"{tag} п.2 k2-055: 1,718 і 1,7183 так, 1,72 і 1,7 ні -> {r}")
            # п.7
            r = page.evaluate("""async () => {
                UNITS = UNITS.length ? UNITS : await getJSON('data/units.json');
                const v = await loadVideos(['an-k1']);
                const d = await (await fetch('data/an-k1/quiz.json')).json();
                const pick = (id) => { const q = Object.assign({_unit: 'an-k1'}, d.questions.find(x => x.id === id));
                    const x = pickVideo(v['an-k1|' + q.topic], q); return x ? x.id + '@' + (x.start || 0) : null; };
                const mains = Object.values(v).map(e => e.main.start || 0);
                return {k023: pick('k-023'), k026: pick('k-026'), k115: pick('k-115'), k104: pick('k-104'), k100: pick('k-100'),
                        k088: pick('k-088'), zero: mains.filter(s => !s).length, n: mains.length}; }""")
            check(r["k023"] == "kFre7PapVTM@27" and r["k026"] == "MrZ6mkdmwBE@525" and r["k115"] == "06Bjl9Qhu0Y@18"
                  and r["k104"] is None and r["k100"] == "IrAt9Kb7uhk@1686" and r["k088"] == "IrAt9Kb7uhk@256",
                  f"{tag} п.7 відео-частини: {r}")
            check(r["zero"] == 0, f"{tag} п.7 головні відео аналітичної з таймкодом: без таймкоду {r['zero']} з {r['n']}")
            # п.8
            go("#/u/an-k1/test")
            r = page.evaluate("""() => [...document.querySelectorAll('.tabs a')].map(a => { const b = a.getBoundingClientRect();
                return [a.textContent.trim(), b.left >= 0 && b.right <= innerWidth + 0.5, a.getAttribute('aria-current') === 'page']; })""")
            check(all(x[1] for x in r) and any(x[2] for x in r), f"{tag} п.8 вкладки в межах екрана, активна є: {r}")
            # п.11
            for uid in ("prog", "zfp", "hist", "eng"):
                reqs.clear()
                go(f"#/q/{uid}/train")
                page.wait_for_timeout(300)
                check(not any("videos.json" in u for u in reqs), f"{tag} п.11 {uid}: videos.json не просимо")
            # п.10: «Сьогодні» - тема з черги плану (не «Аналітична К1»)
            page.evaluate("() => { localStorage.clear(); }")
            go("#/")
            planq = page.evaluate("async () => (await planData()).queue.slice(0, 3)")
            check(planq[0]["topic"] == "Матриці, обернена, ранг" and planq[0]["unit"] == "an-k1" and planq[1]["unit"] == "ma-k2",
                  f"{tag} п.10 черга плану читається без колонки дня: {[(x['n'], x['unit'], x['topic']) for x in planq]}")
            # памʼять: «знаю сьогодні» vs «памʼятаю надовго»
            r = page.evaluate("""async () => {
                const d = await (await fetch('data/an-k1/quiz.json')).json();
                const q = Object.assign({_unit: 'an-k1'}, d.questions[0]);
                localStorage.clear(); STORE = {q: {}, d: {}};
                const real = Date.now; let t = real.call(Date);
                Date.now = () => t;
                record('an-k1', q, true, 'train'); const a = memStats('an-k1');
                t += 6 * 3600e3; record('an-k1', q, true, 'train'); const b = memStats('an-k1');
                t += 20 * 3600e3; record('an-k1', q, true, 'train'); const c = memStats('an-k1');
                t += 48 * 3600e3; record('an-k1', q, false, 'train'); const e = memStats('an-k1');
                Date.now = real; return [a, b, c, e]; }""")
            check([x["today"] for x in r] == [1, 1, 0, 0] and [x["long"] for x in r] == [0, 0, 1, 0],
                  f"{tag} памʼять: той самий день - «сьогодні», через 20 год - «надовго», помилка знімає: {r}")
            # «Пригадай сам»: 20 карток, є «поясни/виведи», сусідні з різних тем
            page.evaluate("() => { localStorage.clear(); sessionStorage.clear(); STORE = {q: {}, d: {}}; }")
            go("#/q/ma-k2/recall")
            r = page.evaluate("() => ({n: S_CUR.qs.length, gen: S_CUR.qs.filter(q => q.type === 'gen').length, "
                              "same: S_CUR.qs.filter((q, i) => i && q.topic === S_CUR.qs[i-1].topic).length})")
            check(r["n"] == 20, f"{tag} «Пригадай сам» 20 карток: {r}")
            # з історією: картки, на які відповів учора, - першими; і є «поясни/виведи»
            page.evaluate("""async () => { const d = await (await fetch('data/ma-k2/quiz.json')).json();
                const g = await (await fetch('data/ma-k2/gen.json')).json();
                const now = Date.now(); STORE = {q: {}, d: {}};
                d.questions.slice(0, 30).forEach((q, i) => STORE.q['ma-k2/' + q.id] = {r: 1, w: 0, t: q.topic, last: 1, f: now - 2 * 86400e3, ts: now - 26 * 3600e3});
                g.cards.slice(0, 6).forEach(q => STORE.q['ma-k2/' + q.id] = {r: 1, w: 0, t: q.topic, last: 1, f: now - 2 * 86400e3, ts: now - 26 * 3600e3, g: 1});
                save(STORE); sessionStorage.clear(); }""")
            go("#/")
            go("#/q/ma-k2/recall")
            r = page.evaluate("() => ({gen: S_CUR.qs.filter(q => q.type === 'gen').length, due: S_CUR.qs.filter(q => STORE.q['ma-k2/' + q.id]).length,"
                              " same: S_CUR.qs.filter((q, i) => i && q.topic === S_CUR.qs[i-1].topic).length, n: S_CUR.qs.length})")
            check(r["due"] == 20 and r["gen"] >= 1 and r["same"] <= 2,
                  f"{tag} «Пригадай сам»: спершу «пора перевірити через добу», є «поясни/виведи», теми впереміш: {r}")
            # картка «поясни/виведи»: підказка і відповідь з <pre>
            page.evaluate("""() => { const i = S_CUR.qs.findIndex(q => q.type === 'gen'); S_CUR.i = i; renderRecall(S_CUR); }""")
            tip = page.inner_text(".tip")
            page.click("#show")
            page.wait_for_timeout(200)
            check(("своїми словами" in tip or "без підказки" in tip), f"{tag} картка «поясни/виведи»: підказка «{tip}»")
            vt = page.evaluate("() => { const q = S_CUR.qs[S_CUR.i]; return [document.querySelector('.face.bk .verdict').textContent.trim(), q.a]; }")
            check(len(vt[0]) > len("Відповідь: ") + 10 and vt[1][:20] in vt[0], f"{tag} картка «поясни/виведи»: відповідь на звороті «{vt[0][:60]}»")
            page.screenshot(path=str(SHOTS / f"unifix-gen-card-{w}.png"))
            # неділя: тест тижня на «Сьогодні»
            page.evaluate("() => sessionStorage.clear()")
            ctx2 = br.new_context(viewport={"width": w, "height": h}, is_mobile=mobile, has_touch=mobile,
                                  device_scale_factor=2 if mobile else 1, reduced_motion="reduce")
            pg = ctx2.new_page()
            pg.on("console", lambda m: errs.append(m.text) if m.type in ("error", "warning") else None)
            pg.on("pageerror", lambda e: errs.append(str(e)))
            pg.clock.install(time=datetime(2026, 11, 22, 11, 0, 0))  # неділя
            pg.goto(base + "#/")
            pg.wait_for_function("() => document.querySelector('#app').dataset.route === '#/'")
            pg.evaluate("""async () => { const d = await (await fetch('data/an-k1/quiz.json')).json();
                const now = Date.now(); const s = {q: {}, d: {}};
                d.questions.slice(0, 40).forEach((q, i) => s.q['an-k1/' + q.id] = {r: 1, w: i % 5 ? 0 : 1, t: q.topic, last: i % 5 ? 1 : 0, f: now - 5 * 86400e3, ts: now - 2 * 86400e3, lt: i % 3 ? 1 : 0});
                localStorage.setItem('uniprep:v1', JSON.stringify(s)); location.hash = '#/'; }""")
            pg.reload()  # STORE читається при старті сторінки
            pg.wait_for_function("() => document.querySelector('#app').dataset.route === '#/'")
            pg.wait_for_timeout(300)
            t = pg.inner_text("#app")
            check("Тест тижня" in t and "памʼятаю надовго" in t, f"{tag} неділя: плитка «Тест тижня» і рядок памʼяті на «Сьогодні»")
            pg.screenshot(path=str(SHOTS / f"unifix-sunday-{w}.png"))
            pg.click("#goW")
            pg.wait_for_function("() => document.querySelector('#app').dataset.route === '#/w/week'")
            n = pg.evaluate("() => S_CUR.qs.length")
            for _ in range(n):
                pg.click("#show")
                pg.click("#knew" if pg.evaluate("() => S_CUR.i % 4") else "#didnt")
                pg.wait_for_timeout(50)
                if pg.locator("#go").count():
                    pg.click("#go")
            pg.wait_for_timeout(300)
            t = pg.inner_text("#app")
            check("Тест тижня: результат" in t and n == 12, f"{tag} тест тижня: {n} карток пройдено до результату")
            pg.screenshot(path=str(SHOTS / f"unifix-week-result-{w}.png"))
            # «через місяць»: через 4 тижні після перших відповідей
            pg.evaluate("""() => { const s = JSON.parse(localStorage.getItem('uniprep:v1')); for (const v of Object.values(s.q)) v.f -= 30 * 86400e3;
                localStorage.setItem('uniprep:v1', JSON.stringify(s)); location.hash = '#/'; }""")
            pg.reload()  # STORE читається при старті сторінки
            pg.wait_for_function("() => document.querySelector('#app').dataset.route === '#/'")
            t = pg.inner_text("#app")
            check("через місяць" in t, f"{tag} неділя через 4 тижні: «Тест «через місяць»»")
            # план: «чому так» і без колонки дня
            go("#/plan")
            t = page.inner_text("#app")
            check("Чому вчимо так" in t and "Rowland 2014" in t and "День тижня" not in t, f"{tag} план: «чому так» з джерелом, черга без дня тижня")
            ctx2.close()
            check(not errs, f"{tag} консоль і мережа без помилок: {errs[:5]}")
            ctx.close()
        br.close()
    print(f"\nOK {len(ok)}, FAIL {len(fails)}")
    for f in fails:
        print("  FAIL:", f)
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
