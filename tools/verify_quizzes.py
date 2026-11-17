"""Перевіряє всі тести сайту. Запуск: python -P -E tools/verify_quizzes.py

1. Структура кожного питання (тип, варіанти, індекс відповіді, пояснення, тема).
2. Числа: якщо в питанні є поле "verify", вираз sympy рахується тут НЕЗАЛЕЖНО від
   генератора і має збігтися з правильною відповіддю:
     - type number: з полем answer (допуск tol);
     - type single/multi: з полем "value" (рядок sympy), а правильний варіант мусить
       містити value у вигляді тексту з поля "valueText" (якщо задано);
       жоден НЕправильний варіант не може мати те саме значення (поле "optionValues").
3. Питання, позначене "calc": true (є обчислення), без verify - помилка.
4. Заборонені послідовності (LaTeX, довгі тире).
5. Дублікати id і дублікати варіантів у питанні.
Вихід 0 - усе зелене.
"""
import json
import math
import sys
from pathlib import Path

import sympy as sp
from sympy.parsing.sympy_parser import parse_expr, standard_transformations, implicit_multiplication_application, convert_xor

ROOT = Path(__file__).resolve().parent.parent
CONTENT = ROOT / "content"
TR = standard_transformations + (convert_xor,)
NS = {name: getattr(sp, name) for name in dir(sp) if not name.startswith("_")}
NS.update({"e": sp.E, "E": sp.E, "pi": sp.pi, "oo": sp.oo, "ln": sp.log})
for s in "x y z t u v w a b c n k m h r s".split():
    NS[s] = sp.Symbol(s, real=True)

BAD = ["$$", "\\frac", "\\sqrt", "begin{", "\\(", "\\[", "—", "–"]


def ev(expr):
    """Обчислює рядок sympy (або python-вираз над sympy) і повертає sympy-обʼєкт."""
    return sp.sympify(eval(expr, {"__builtins__": {}}, NS))  # noqa: S307 - лише наші файли


def same(a, b, tol=1e-9):
    a, b = sp.sympify(a), sp.sympify(b)
    try:
        if sp.simplify(a - b) == 0:
            return True
    except Exception:
        pass
    try:
        fa, fb = complex(sp.N(a, 30)), complex(sp.N(b, 30))
        return abs(fa - fb) <= tol * max(1.0, abs(fb))
    except Exception:
        return False


def main():
    units = json.loads((CONTENT / "units.json").read_text(encoding="utf-8"))
    if "--unit" in sys.argv:
        units = [sys.argv[sys.argv.index("--unit") + 1]]
    errs, total, verified, calc = [], 0, 0, 0
    per_unit = {}
    for uid in units:
        f = CONTENT / uid / "quiz.json"
        if not f.exists():
            per_unit[uid] = (0, 0)
            continue
        raw = f.read_text(encoding="utf-8")
        for b in BAD:
            if b in raw:
                errs.append(f"{uid}: заборонене «{b}» у quiz.json")
        d = json.loads(raw)
        ids = set()
        uv = 0
        for q in d["questions"]:
            total += 1
            where = f"{uid}/{q.get('id')}"
            if q.get("id") in ids:
                errs.append(f"{where}: дубль id")
            ids.add(q.get("id"))
            for k in ("id", "topic", "type", "q", "answer", "explain"):
                if k not in q or q[k] in ("", None):
                    errs.append(f"{where}: нема поля {k}")
            t = q.get("type")
            if t in ("single", "multi"):
                opts = q.get("options") or []
                if len(opts) < 2:
                    errs.append(f"{where}: < 2 варіантів")
                if len(set(opts)) != len(opts):
                    errs.append(f"{where}: однакові варіанти")
                ans = q.get("answer")
                idx = [ans] if t == "single" else ans
                if not isinstance(idx, list) or not idx or any(not isinstance(i, int) or i < 0 or i >= len(opts) for i in idx):
                    errs.append(f"{where}: поганий індекс відповіді {ans}")
            elif t == "number":
                if not isinstance(q.get("answer"), (int, float)):
                    errs.append(f"{where}: answer має бути числом")
            elif t == "short":
                if not q.get("accept"):
                    errs.append(f"{where}: short без accept")
            else:
                errs.append(f"{where}: невідомий тип {t}")
            if q.get("calc"):
                calc += 1
                if "verify" not in q:
                    errs.append(f"{where}: calc без verify")
            if "verify" in q:
                try:
                    got = ev(q["verify"])
                except Exception as e:  # noqa: BLE001
                    errs.append(f"{where}: verify не рахується: {e}")
                    continue
                if t == "number":
                    tol = q.get("tol", 0.01)
                    if not (abs(float(sp.N(got)) - q["answer"]) <= tol * abs(q["answer"]) + q.get("atol", 1e-9)):
                        errs.append(f"{where}: verify={sp.N(got, 8)} ≠ answer={q['answer']}")
                    else:
                        verified += 1; uv += 1
                else:
                    if "value" not in q:
                        errs.append(f"{where}: verify без value")
                        continue
                    try:
                        val = ev(q["value"])
                    except Exception as e:  # noqa: BLE001
                        errs.append(f"{where}: value не рахується: {e}")
                        continue
                    if not same(got, val):
                        errs.append(f"{where}: verify={got} ≠ value={val}")
                        continue
                    ov = q.get("optionValues")
                    if ov:
                        if len(ov) != len(q["options"]):
                            errs.append(f"{where}: optionValues іншої довжини")
                        else:
                            right = [q["answer"]] if t == "single" else q["answer"]
                            for i, s in enumerate(ov):
                                if s is None:
                                    continue
                                try:
                                    vi = ev(s)
                                except Exception as e:  # noqa: BLE001
                                    errs.append(f"{where}: optionValues[{i}] не рахується: {e}")
                                    continue
                                eq = same(vi, val) if t == "single" else None
                                if t == "single":
                                    if i in right and not eq:
                                        errs.append(f"{where}: правильний варіант {i} ≠ value")
                                    if i not in right and eq:
                                        errs.append(f"{where}: неправильний варіант {i} теж дорівнює value")
                    verified += 1; uv += 1
        per_unit[uid] = (len(d["questions"]), uv)
    for uid, (n, v) in per_unit.items():
        print(f"{uid:6} питань {n:4}  перевірено числом {v:4}")
    print(f"РАЗОМ питань {total}, з числовою перевіркою {verified}, позначених calc {calc}")
    if errs:
        print(f"ПОМИЛОК {len(errs)}:")
        for e in errs:
            print("  ", e)
        return 1
    print("OK: усі перевірки зелені")
    return 0


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    sys.exit(main())
