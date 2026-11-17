"""Чи підтягується нова версія в уже встановлений сайт (service worker).
1) відкриває сайт, запамʼятовує версію кешу; 2) чекає, поки на Pages зʼявиться інша версія
precache.json (або одразу, якщо --expect <версія>); 3) перезавантажує сторінку і перевіряє, що
кеш тепер нової версії, а старий видалено; 4) офлайн після оновлення - теж працює.
python -P -E tools/update_check.py <url> <стара_версія>
"""
import sys
import time
import urllib.request

from playwright.sync_api import sync_playwright


def live_version(url):
    with urllib.request.urlopen(url + "precache.json?" + str(time.time())) as r:
        import json
        return json.load(r)["version"]


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    url, old = sys.argv[1], sys.argv[2]
    with sync_playwright() as p:
        br = p.chromium.launch(headless=True)
        ctx = br.new_context(viewport={"width": 390, "height": 844}, is_mobile=True)
        pg = ctx.new_page()
        pg.goto(url, wait_until="networkidle")
        pg.evaluate("navigator.serviceWorker.ready")
        pg.wait_for_timeout(1500)
        before = pg.evaluate("caches.keys()")
        print("кеш до:", before)
        if len(sys.argv) > 3:  # команда, що викладає нову версію (напр. git push)
            import subprocess
            subprocess.run(sys.argv[3], shell=True, check=True)
        for _ in range(90):
            v = live_version(url)
            if v != old:
                break
            time.sleep(5)
        print("на Pages версія:", v)
        for _ in range(3):
            pg.reload(wait_until="networkidle")
            pg.wait_for_timeout(2500)
        after = pg.evaluate("caches.keys()")
        print("кеш після:", after)
        ok = after == ["uniprep-" + v]
        ctx.set_offline(True)
        pg.reload()
        pg.wait_for_selector(".unit")
        print("офлайн після оновлення: OK")
        br.close()
    print("ОНОВЛЕННЯ:", "OK" if ok else "НЕ підтягнулось")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
