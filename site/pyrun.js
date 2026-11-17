// Кнопки «Запустити / Змінити / Копіювати» під кодом у розділі «Програмування» (UNIPROG1).
// Код виконує py-worker.js (Pyodide). Нескінченний цикл: через 10 с воркер зупиняється і створюється новий.
(function () {
  "use strict";
  const PYVER = "0.29.5";
  const PYCACHE = "pyodide-" + PYVER;
  const PYFILES = ["py/pyodide.js", "py/pyodide.asm.js", "py/pyodide.asm.wasm", "py/python_stdlib.zip", "py/pyodide-lock.json"];
  const LIMIT_MS = 10000;
  let worker = null, isReady = false, seq = 0;
  const pending = new Map();

  function getWorker() {
    if (worker) return worker;
    worker = new Worker("py-worker.js");
    isReady = false;
    worker.onmessage = (ev) => {
      const m = ev.data;
      if (m.type === "ready") { isReady = true; return; }
      const p = pending.get(m.id);
      if (m.type === "started" && p) {
        isReady = true;
        p.status("Виконую...");
        p.timer = setTimeout(() => {
          worker.terminate(); worker = null;
          pending.delete(m.id);
          p.resolve({ out: "Зупинено: код працював понад 10 с. Схоже на нескінченний цикл (умова while ніколи не стає False?).", stopped: true });
        }, LIMIT_MS);
        return;
      }
      if ((m.type === "done" || m.type === "error") && p) {
        clearTimeout(p.timer);
        pending.delete(m.id);
        p.resolve({ out: m.type === "done" ? m.out : m.text, ms: m.ms, error: m.type === "error" });
      }
    };
    worker.onerror = (e) => {
      for (const [, p] of pending) { clearTimeout(p.timer); p.resolve({ out: "Python не запустився: " + (e.message || e), error: true }); }
      pending.clear();
      worker = null;
    };
    return worker;
  }

  function run(code, inputs, mode, status) {
    return new Promise((resolve) => {
      const id = ++seq;
      pending.set(id, { resolve, status, timer: null });
      if (!isReady) status("Завантажую Python (перший раз ≈ 12 МБ, далі з памʼяті телефона)...");
      getWorker().postMessage({ type: "run", id, code, inputs, mode });
    });
  }

  function kindOf(code) {
    const t = code.trim();
    const head = t.split("\n").slice(0, 3).join("\n");
    if (/^# не запускати/m.test(head)) return "skip";
    if (/^\s*(>>>\s*)?(import|from)\s+(turtle|matplotlib|tkinter|numpy)\b/m.test(t)) return "skip";
    const firstReal = t.split("\n").find((l) => l.trim() && !l.trim().startsWith("#")) || "";
    if (firstReal.startsWith(">>>")) return "session";
    if (t.includes(">>>")) return "module-doctest";
    return "prog";
  }

  function presetInputs(code) {
    const m = code.split("\n").slice(0, 3).join("\n").match(/^#\s*ввід:\s*(.*)$/m);
    return m ? m[1].split(" | ").map((s) => s.trim()).join("\n") : "";
  }

  function btn(label, cls) {
    const b = document.createElement("button");
    b.type = "button";
    b.className = "btn pybtn" + (cls ? " " + cls : "");
    b.textContent = label;
    return b;
  }

  function enhance(root) {
    if (!root) return;
    root.querySelectorAll('a[href$=".py"]').forEach((a) => a.setAttribute("download", ""));
    root.querySelectorAll("pre > code.language-python").forEach((code) => {
      const pre = code.parentElement;
      if (pre.dataset.py) return;
      pre.dataset.py = "1";
      const original = code.textContent;
      const kind = kindOf(original);
      const bar = document.createElement("div");
      bar.className = "pybar";
      const copy = btn("Копіювати");
      copy.addEventListener("click", async () => {
        try { await navigator.clipboard.writeText(code.innerText); copy.textContent = "Скопійовано"; }
        catch (e) { copy.textContent = "Не вдалося"; }
        setTimeout(() => { copy.textContent = "Копіювати"; }, 1500);
      });
      if (kind === "skip") {
        const note = document.createElement("span");
        note.className = "pynote";
        note.textContent = "Цей код відкриває вікно (turtle/matplotlib) - запускай у терміналі.";
        bar.append(copy, note);
        pre.after(bar);
        return;
      }
      const runB = btn(kind === "session" ? "Перевірити doctest" : "Запустити", "primary");
      const dtB = kind === "module-doctest" ? btn("doctest -v") : null;
      const editB = btn("Змінити");
      const resetB = btn("Скинути");
      resetB.hidden = true;
      const inWrap = document.createElement("label");
      inWrap.className = "pyin";
      const needsInput = /\binput\s*\(/.test(original);
      inWrap.hidden = !needsInput;
      inWrap.innerHTML = '<span>Ввід (кожне значення з нового рядка):</span>';
      const inArea = document.createElement("textarea");
      inArea.rows = 2;
      inArea.spellcheck = false;
      inArea.value = presetInputs(original);
      inWrap.append(inArea);
      const out = document.createElement("pre");
      out.className = "pyout";
      out.hidden = true;
      out.setAttribute("aria-live", "polite");
      bar.append(runB);
      if (dtB) bar.append(dtB);
      bar.append(editB, resetB, copy);
      pre.after(bar);
      bar.after(inWrap);
      inWrap.after(out);

      editB.addEventListener("click", () => {
        const on = code.getAttribute("contenteditable") !== "plaintext-only";
        if (on) {
          code.setAttribute("contenteditable", "plaintext-only");
          code.spellcheck = false;
          code.setAttribute("autocapitalize", "off");
          pre.classList.add("editing");
          code.focus();
          editB.textContent = "Готово";
          resetB.hidden = false;
        } else {
          code.removeAttribute("contenteditable");
          pre.classList.remove("editing");
          editB.textContent = "Змінити";
        }
      });
      code.addEventListener("keydown", (e) => {
        if (e.key === "Tab" && code.isContentEditable) { e.preventDefault(); document.execCommand("insertText", false, "    "); }
      });
      resetB.addEventListener("click", () => { code.textContent = original; resetB.hidden = true; });

      async function go(mode, b) {
        const src = code.innerText.replace(/ /g, " ");
        const inputs = inArea.value ? inArea.value.split("\n") : [];
        out.hidden = false;
        out.classList.remove("bad");
        out.textContent = "";
        const st = (t) => { out.textContent = t; };
        runB.disabled = true; if (dtB) dtB.disabled = true;
        const r = await run(src, inputs, mode, st);
        runB.disabled = false; if (dtB) dtB.disabled = false;
        const text = (r.out || "").replace(/\s+$/, "");
        out.textContent = text || "(нічого не надруковано - програма нічого не виводить через print)";
        if (r.error || r.stopped || /^\w*(Error|Exception)\b/m.test(text) || /\*{20,}/.test(text)) out.classList.add("bad");
        b.focus({ preventScroll: true });
      }
      runB.addEventListener("click", () => go(kind === "session" ? "session" : "prog", runB));
      if (dtB) dtB.addEventListener("click", () => go("doctest", dtB));
    });
  }

  async function pyCached() {
    if (!("caches" in window)) return false;
    try {
      const c = await caches.open(PYCACHE);
      const hits = await Promise.all(PYFILES.map((f) => c.match(f)));
      return hits.every(Boolean);
    } catch (e) { return false; }
  }

  async function box(el) {
    if (!el) return;
    const draw = async () => {
      const ok = await pyCached();
      el.innerHTML = ok
        ? '<strong>Python у браузері: збережено, працює без інтернету.</strong> Під кожним прикладом у уроках є «Запустити» і «Змінити».'
        : '<strong>Python у браузері</strong> - кнопка «Запустити» під кожним прикладом. Щоб працювало й без інтернету, завантаж один раз (≈ 12 МБ, далі з памʼяті): <button type="button" class="btn primary pyget">Завантажити Python</button>';
      const b = el.querySelector(".pyget");
      if (b) b.addEventListener("click", async () => {
        b.disabled = true; b.textContent = "Завантажую...";
        try {
          const c = await caches.open(PYCACHE);
          await c.addAll(PYFILES);
          await draw();
        } catch (e) { b.disabled = false; b.textContent = "Не вдалося - спробуй з інтернетом"; }
      });
    };
    await draw();
  }

  window.PyRun = { enhance, box, pyCached, PYCACHE, PYFILES };
})();
