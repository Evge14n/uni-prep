// Python у браузері для розділу «Програмування» (UNIPROG1).
// Pyodide 0.29.5 (Python 3.13) лежить у py/ на цьому ж сайті; service worker кешує його окремо (pyodide-*),
// тому після першого завантаження працює без інтернету. Кожен запуск - свіжий модуль __main__.
importScripts("py/pyodide.js");

let ready = null;
let outBuf = "";
const dec = new TextDecoder();
const LIMIT = 20000;

const PRELUDE = `
import builtins, sys, types, traceback, doctest


def _uniprep_run(code, inputs, mode):
    feed = list(inputs)

    def fake_input(prompt=""):
        print(prompt, end="")
        if not feed:
            raise EOFError("нема вводу: впиши значення в поле «Ввід» (кожне з нового рядка)")
        value = feed.pop(0)
        print(value)
        return value

    builtins.input = fake_input
    mod = types.ModuleType("__main__")
    sys.modules["__main__"] = mod
    lines = code.split("\\n")
    try:
        if mode == "session":
            test = doctest.DocTestParser().get_doctest(code, mod.__dict__, "приклад", "<код>", 0)
            runner = doctest.DocTestRunner(verbose=False)
            runner.run(test)
            res = runner.summarize(verbose=False)
            ok = res.attempted - res.failed
            print(f"doctest: пройшло {ok} з {res.attempted}" + (" - усе зелене" if not res.failed else ""))
        else:
            exec(compile(code, "<код>", "exec"), mod.__dict__)
            if mode == "doctest":
                res = doctest.testmod(mod, verbose=True)
    except SystemExit:
        pass
    except SyntaxError as e:
        print(f'  File "<код>", line {e.lineno}')
        if e.text:
            print("    " + e.text.strip())
        print(f"{type(e).__name__}: {e.msg}")
    except BaseException as e:
        frames = [f for f in traceback.extract_tb(e.__traceback__) if f.filename == "<код>"]
        print("Traceback (most recent call last):")
        for f in frames:
            print(f'  File "<код>", line {f.lineno}')
            if f.lineno and f.lineno <= len(lines):
                print("    " + lines[f.lineno - 1].strip())
        print(f"{type(e).__name__}: {e}")
        if isinstance(e, ModuleNotFoundError) and e.name in ("turtle", "tkinter", "matplotlib", "numpy"):
            print(f"(Модуль {e.name} у браузері не працює - цей код запускай у терміналі: python3 файл.py)")
    finally:
        # print(..., end="") без переносу лишається в буфері - без flush він вилізе в НАСТУПНОМУ запуску
        sys.stdout.flush()
        sys.stderr.flush()
`;

function boot() {
  if (!ready) {
    ready = loadPyodide({ indexURL: new URL("py/", self.location.href).href }).then((py) => {
      const w = { write: (buf) => { if (outBuf.length < LIMIT) outBuf += dec.decode(buf, { stream: true }); return buf.length; } };
      py.setStdout(w);
      py.setStderr(w);
      py.runPython(PRELUDE);
      return py;
    });
  }
  return ready;
}

self.onmessage = async (ev) => {
  const m = ev.data;
  if (m.type === "boot") {
    try { await boot(); self.postMessage({ type: "ready" }); } catch (e) { self.postMessage({ type: "error", text: String(e) }); }
    return;
  }
  if (m.type !== "run") return;
  let py;
  try {
    py = await boot();
  } catch (e) {
    ready = null;
    self.postMessage({ type: "error", id: m.id, text: "Python не завантажився: " + e + ". Відкрий сторінку раз з інтернетом." });
    return;
  }
  self.postMessage({ type: "started", id: m.id });
  outBuf = "";
  const t0 = performance.now();
  try {
    const run = py.globals.get("_uniprep_run");
    run(m.code, py.toPy(m.inputs || []), m.mode);
    run.destroy();
  } catch (e) {
    outBuf += "\n[помилка запуску] " + e;
  }
  let out = outBuf + dec.decode();
  if (out.length >= LIMIT) out = out.slice(0, LIMIT) + "\n... (вивід обрізано)";
  self.postMessage({ type: "done", id: m.id, out, ms: Math.round(performance.now() - t0) });
};
