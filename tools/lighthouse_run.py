"""Lighthouse (мобільний) + перевірка встановлюваності PWA через CDP + знімок темної теми.
python -P -E tools/lighthouse_run.py https://evge14n.github.io/uni-prep/
Chromium з Playwright запускається з портом налагодження (так Lighthouse працює на цьому ПК),
після прогону закривається. Звіти - у tools/e2e-shots/ (не в репо).
"""
import json
import subprocess
import sys
import tempfile
import time
from pathlib import Path

from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "tools" / "e2e-shots"
OUT.mkdir(exist_ok=True)


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    url = sys.argv[1]
    with sync_playwright() as p:
        exe = p.chromium.executable_path
        # встановлюваність і темна тема
        br = p.chromium.launch(headless=True)
        ctx = br.new_context(viewport={"width": 390, "height": 844}, is_mobile=True, has_touch=True,
                             device_scale_factor=2, color_scheme="dark")
        pg = ctx.new_page()
        pg.goto(url, wait_until="networkidle")
        pg.wait_for_selector(".unit")
        pg.evaluate("navigator.serviceWorker.ready")
        cdp = ctx.new_cdp_session(pg)
        inst = cdp.send("Page.getInstallabilityErrors")
        man = cdp.send("Page.getAppManifest")
        print("installability errors:", inst.get("installabilityErrors"))
        print("manifest errors:", man.get("errors"))
        bg = pg.evaluate("getComputedStyle(document.body).backgroundColor")
        print("темна тема, тло body:", bg)
        pg.screenshot(path=str(OUT / "dark-390-home.png"))
        pg.goto(url + "#/u/ma-k2/oznachennya")
        pg.wait_for_selector("h1")
        pg.wait_for_timeout(300)
        pg.screenshot(path=str(OUT / "dark-390-ma-k2-oznachennya.png"))
        br.close()
    prof = tempfile.mkdtemp(prefix="lh-")
    chrome = subprocess.Popen([exe, "--headless=new", "--remote-debugging-port=9334", f"--user-data-dir={prof}",
                               "--no-first-run", "about:blank"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    try:
        time.sleep(3)
        rep = OUT / "lighthouse.json"
        cmd = f'npx -y lighthouse@12 "{url}" --port=9334 --output=json --output-path="{rep}" --quiet --form-factor=mobile ' \
              '--only-categories=performance,accessibility,best-practices,seo'
        r = subprocess.run(cmd, shell=True, capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=400)
        if r.returncode != 0:
            print("lighthouse помилка:", r.stderr[-1500:])
            return 1
        d = json.loads(rep.read_text(encoding="utf-8"))
        for k, v in d["categories"].items():
            print(f"{k}: {round(v['score'] * 100)}")
        for aid, a in d["audits"].items():
            if a.get("score") is not None and a["score"] < 0.9 and a.get("scoreDisplayMode") in ("binary", "numeric"):
                print("  ⚠", aid, a.get("score"), a.get("displayValue", ""))
    finally:
        chrome.kill()
    return 0


if __name__ == "__main__":
    sys.exit(main())
