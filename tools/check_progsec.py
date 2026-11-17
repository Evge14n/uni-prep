"""Перевірка розділу «Python + безпека» (prog-sec, UPROGSEC1).

  python -X utf8 -P -E tools/check_progsec.py            # перевірка
  python -X utf8 -P -E tools/check_progsec.py --mutate   # + мутаційний тест (зіпсовані дані мусять впасти)

1. Кожен ```python у content/prog-sec/*.md запускається ТАК САМО, як у браузері (той самий формат помилки,
   що в site/py-worker.js), і вивід порівнюється рядок у рядок з наступним ```text.
   Блоки «# не запускати: ...» теж запускаються тут, якщо модуль є на ПК (argon2-cffi), інакше лише compile.
2. Задачі (є doctest.testmod(verbose=True)): заготовка (`pass`) - doctest червоний, розвʼязок - зелений.
3. Заборонені символи (LaTeX, довгі тире), приватне (шляхи D:\\, назва особистої теки, прізвища), ширина
   рядків шпаргалки ≤ 40 (телефон 390 px).
"""
import contextlib
import doctest
import io
import re
import sys
import traceback
import types
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
UNIT = ROOT / "content" / "prog-sec"
FENCE = re.compile(r"^```(\w*)\n(.*?)^```", re.M | re.S)
BAD = ["$$", "\\frac", "begin{", "\u2014", "\u2013"]
# приватне: локальні шляхи, особисті теки «Моє-...», імена - зі списку поза репо (у публічному репо імен нема)
_NF = Path(r"D:\Універ\00_Загальне\_імена-не-на-сайт.txt")
PRIVATE = ["D:\\", "D:/", "C:\\Users", "Моє-"] + (
    [x.strip() for x in _NF.read_text(encoding="utf-8").split(",") if x.strip()] if _NF.exists() else [])


def run_like_browser(code):
    """Копія логіки _uniprep_run з site/py-worker.js (mode=run)."""
    buf = io.StringIO()
    lines = code.split("\n")
    mod = types.ModuleType("__main__")
    old = sys.modules.get("__main__")
    sys.modules["__main__"] = mod
    try:
        with contextlib.redirect_stdout(buf), contextlib.redirect_stderr(buf):
            try:
                exec(compile(code, "<код>", "exec"), mod.__dict__)
            except SystemExit:
                pass
            except SyntaxError as e:
                print(f'  File "<код>", line {e.lineno}')
                if e.text:
                    print("    " + e.text.strip())
                print(f"{type(e).__name__}: {e.msg}")
            except BaseException as e:  # noqa: BLE001 - як у браузері
                frames = [f for f in traceback.extract_tb(e.__traceback__) if f.filename == "<код>"]
                print("Traceback (most recent call last):")
                for f in frames:
                    print(f'  File "<код>", line {f.lineno}')
                    if f.lineno and f.lineno <= len(lines):
                        print("    " + lines[f.lineno - 1].strip())
                print(f"{type(e).__name__}: {e}")
    finally:
        sys.modules["__main__"] = old
    return buf.getvalue()


def doctest_module(code):
    """Виконати модуль без __main__-блоку і прогнати doctest. Повертає (attempted, failed)."""
    mod = types.ModuleType("zadacha")
    body = code.split('if __name__ == "__main__":')[0]
    sys.modules["zadacha"] = mod
    exec(compile(body, "<задача>", "exec"), mod.__dict__)
    with contextlib.redirect_stdout(io.StringIO()):
        res = doctest.testmod(mod, verbose=False)
    return res.attempted, res.failed


def norm(s):
    lines = [x.rstrip() for x in s.replace("\r\n", "\n").split("\n")]
    while lines and not lines[-1]:
        lines.pop()
    return lines


def blocks(text):
    """[(lang, code, expected_or_None)] - expected = ```text одразу після ```python."""
    out = []
    ms = list(FENCE.finditer(text))
    for i, m in enumerate(ms):
        if m.group(1) != "python":
            continue
        exp = None
        if i + 1 < len(ms) and ms[i + 1].group(1) == "text" and not text[m.end():ms[i + 1].start()].strip():
            exp = ms[i + 1].group(2)
        out.append((m.group(1), m.group(2), exp))
    return out


def check(files):
    errs, stats = [], {"run": 0, "compared": 0, "skip_compile": 0, "tasks_stub": 0, "tasks_sol": 0}
    for name, text in files.items():
        for ch in BAD:
            if ch in text:
                errs.append(f"{name}: заборонене {ch!r}")
        for p in PRIVATE:
            if p in text:
                errs.append(f"{name}: приватне {p!r}")
        if name == "shpargalka.md":
            for m in FENCE.finditer(text):
                for ln in m.group(2).split("\n"):
                    if len(ln) > 40:
                        errs.append(f"{name}: рядок шпаргалки > 40 символів: {ln!r}")
        for _, code, exp in blocks(text):
            head = "\n".join(code.split("\n")[:3])
            if "doctest.testmod(verbose=True)" in code:
                stub = bool(re.search(r"^\s+pass\s*$", code, re.M))
                att, fail = doctest_module(code)
                if att == 0:
                    errs.append(f"{name}: задача без прикладів doctest")
                if stub:
                    stats["tasks_stub"] += 1
                    if fail == 0:
                        errs.append(f"{name}: заготовка пройшла doctest: {code[:60]!r}")
                else:
                    stats["tasks_sol"] += 1
                    if fail:
                        errs.append(f"{name}: розвʼязок червоний ({fail} з {att}): {code[:60]!r}")
                continue
            if "# не запускати" in head:
                try:
                    out = run_like_browser(code)
                except Exception:  # noqa: BLE001
                    out = None
                if out is None or "ModuleNotFoundError" in out:
                    compile(code, "<код>", "exec")
                    stats["skip_compile"] += 1
                    continue
            else:
                out = run_like_browser(code)
            stats["run"] += 1
            if exp is None:
                continue
            stats["compared"] += 1
            if norm(out) != norm(exp):
                errs.append(f"{name}: вивід не збігся\n  код: {code.strip().splitlines()[0]!r}\n"
                            f"  очікувалось: {norm(exp)[:6]}\n  є: {norm(out)[:6]}")
    return errs, stats


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    files = {p.name: p.read_text(encoding="utf-8") for p in sorted(UNIT.glob("*.md"))}
    errs, stats = check(files)
    print("статистика:", stats)
    for e in errs:
        print("ПОМИЛКА:", e)
    if "--mutate" in sys.argv:
        t = files["teoriya.md"]
        muts = {
            "вивід уроку": ("'abc' -> None", "'abc' -> 0"),
            "інʼєкція": ("[('anna', 's-111'), ('bob', 's-222')]", "[]"),
        }
        z = files["zadachi.md"]
        for label, (a, b) in muts.items():
            m_errs, _ = check({"teoriya.md": t.replace(a, b, 1)})
            print(f"мутація «{label}»:", "впала - OK" if m_errs else "НЕ ВПАЛА")
            if not m_errs:
                errs.append(f"мутація {label} не впала")
        # розвʼязок задачі 3 без перевірки межі - мусить стати червоним
        bad = z.replace("    if not path.is_relative_to(root):\n        raise ValueError(\"вихід за межі теки\")\n", "", 1)
        m_errs, _ = check({"zadachi.md": bad})
        print("мутація «розвʼязок без перевірки»:", "впала - OK" if m_errs else "НЕ ВПАЛА")
        if not m_errs:
            errs.append("мутація розвʼязку не впала")
        m_errs, _ = check({"teoriya.md": t + "\nтут — тире\n"})
        print("мутація «тире»:", "впала - OK" if m_errs else "НЕ ВПАЛА")
        if not m_errs:
            errs.append("мутація тире не впала")
    if errs:
        print(f"ПОМИЛОК {len(errs)}")
        sys.exit(1)
    print("OK")


if __name__ == "__main__":
    main()
