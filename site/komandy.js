/* UCMD1 18.11.2026: торкнись команди в коді уроку - коротка підказка з довідника «Команди»;
   пошук у вкладці «Команди». Дані - data/prog/komandy.json (є в офлайн-кеші). */
"use strict";
const Cmd = (() => {
  let D = null, loading = null, tip = null, opener = null;
  const PREFIX = new Set(["sudo", "time", "nohup", "exec", "env", "timeout", "watch", "xargs", "nice", "command"]);
  const LANGS = /\blanguage-(bash|sh|shell|console|zsh)\b/;
  const OPS = ["2>&1", "&>>", "&>", "2>>", "2>", "<<<", "<<-", "<<", ">>", "||", "&&", "|&", "|", ">", "<", "&", ";", "(", ")"];
  const SYM = { "|": "|", "||": "||", "&&": "&&", ";": ";", "&": "&", ">": ">", ">>": ">>", "2>": "2>", "2>>": "2>",
    "2>&1": "2>&1", "<": "<", "<<": "<<", "<<-": "<<" };
  const escH = (s) => String(s).replace(/[&<>"]/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]));

  function load() {
    if (D) return Promise.resolve(D);
    if (!loading) loading = fetch("data/prog/komandy.json").then((r) => (r.ok ? r.json() : {})).catch(() => ({})).then((j) => (D = j));
    return loading;
  }

  // лексер bash: слова (лапки - частина слова), оператори, коментарі, нові рядки; тіло heredoc пропускається
  function lex(src) {
    const t = [];
    const n = src.length;
    let i = 0, hd = null;
    while (i < n) {
      const c = src[i];
      if (c === "\n") {
        t.push({ ty: "nl", s: i, e: i + 1 });
        i++;
        if (hd) { // <<EOF ... EOF - не команди
          const re = new RegExp("^[ \\t]*" + hd.replace(/[.*+?^${}()|[\]\\]/g, "\\$&") + "[ \\t]*$", "m");
          const m = re.exec(src.slice(i));
          i = m ? i + m.index + m[0].length : n;
          hd = null;
        }
        continue;
      }
      if (c === " " || c === "\t") { i++; continue; }
      if (c === "\\" && src[i + 1] === "\n") { i += 2; continue; }
      if (c === "#") { let j = src.indexOf("\n", i); if (j < 0) j = n; i = j; continue; }
      const op = OPS.find((o) => src.startsWith(o, i));
      if (op) { t.push({ ty: "op", v: op, s: i, e: i + op.length }); i += op.length; continue; }
      let j = i, q = null;
      while (j < n) {
        const d = src[j];
        if (q) { if (d === "\\" && q === '"') { j += 2; continue; } if (d === q) q = null; j++; continue; }
        if (d === "'" || d === '"') { q = d; j++; continue; }
        if (d === "\\") { j += 2; continue; }
        if (d === "$" && src[j + 1] === "(") {
          let depth = 0;
          while (j < n) { if (src[j] === "(") depth++; else if (src[j] === ")" && --depth === 0) { j++; break; } j++; }
          continue;
        }
        if (/[\s;&|()<>]/.test(d)) break;
        j++;
      }
      if (j === i) { i++; continue; }
      const w = { ty: "w", v: src.slice(i, j), s: i, e: j };
      const prev = t[t.length - 1];
      if (prev && prev.ty === "op" && /^<<-?$/.test(prev.v)) hd = w.v.replace(/['"]/g, "");
      t.push(w);
      i = j;
    }
    return t;
  }

  function marks(tokens, d) {
    const out = [];
    let cmd = [], skip = false;
    const flush = () => { if (cmd.length) analyze(cmd, d, out); cmd = []; };
    for (const tk of tokens) {
      if (tk.ty === "w") { if (skip) { skip = false; continue; } cmd.push(tk); continue; }
      if (tk.ty === "op") {
        const k = SYM[tk.v];
        if (k && d[k]) out.push({ s: tk.s, e: tk.e, k });
        if (/^(\d|&)?[<>]/.test(tk.v) && tk.v !== "2>&1") { skip = true; continue; } // далі - імʼя файлу
        if (tk.v === "2>&1" || tk.v === "|&") { if (tk.v === "|&") flush(); continue; }
        flush();
        continue;
      }
      flush();
    }
    flush();
    return out;
  }

  function flagMarks(key, ws, from, d, out) {
    const e = d[key];
    if (!e) return;
    const fl = e[3] || {}, ar = e[4] || {};
    for (let j = from; j < ws.length; j++) {
      const v = ws[j].v;
      if (v === "--") break;
      if (key === "find" && v === "-exec") { if (fl[v]) out.push({ s: ws[j].s, e: ws[j].e, k: key, f: v }); break; }
      if (v.length > 1 && v[0] === "-" && !/^-\d+(\.\d+)?$/.test(v)) {
        const f = v.split("=")[0];
        if (fl[f] || (/^-[A-Za-z]{2,}$/.test(f) && [...f.slice(1)].every((c) => fl["-" + c]))) out.push({ s: ws[j].s, e: ws[j].s + f.length, k: key, f });
        else if (ar[v]) out.push({ s: ws[j].s, e: ws[j].e, k: key, a: v }); // ssh -T, chmod -w - описані як аргументи
      } else if (ar[v]) out.push({ s: ws[j].s, e: ws[j].e, k: key, a: v });
    }
  }

  function analyze(ws, d, out) {
    let i = 0;
    while (i < ws.length && /^[A-Za-z_][A-Za-z0-9_]*=/.test(ws[i].v)) i++;
    while (i < ws.length && PREFIX.has(ws[i].v)) {
      const pk = ws[i].v;
      if (d[pk]) out.push({ s: ws[i].s, e: ws[i].e, k: pk });
      i++;
      const st = i;
      while (i < ws.length && ws[i].v[0] === "-") i++;
      flagMarks(pk, ws.slice(0, i), st, d, out);
      if (pk === "timeout" && i < ws.length && /^\d/.test(ws[i].v)) i++;
      while (pk === "env" && i < ws.length && ws[i].v.includes("=")) i++;
    }
    if (i >= ws.length) return;
    const w0 = ws[i].v;
    if (/^python3?(\.\d+)?$/.test(w0)) {
      if (d.python3) out.push({ s: ws[i].s, e: ws[i].e, k: "python3" });
      let j = i + 1;
      while (j < ws.length && ws[j].v[0] === "-") {
        const f = ws[j].v;
        if (f === "-m" && j + 1 < ws.length) {
          flagMarks("python3", ws.slice(0, j + 1), j, d, out);
          let mk = "python3 -m " + ws[j + 1].v, me = j + 1;
          if (j + 2 < ws.length && d[mk + " " + ws[j + 2].v]) { mk += " " + ws[j + 2].v; me = j + 2; }
          if (d[mk]) { out.push({ s: ws[j + 1].s, e: ws[me].e, k: mk }); flagMarks(mk, ws, me + 1, d, out); }
          return;
        }
        flagMarks("python3", ws.slice(0, j + 1), j, d, out);
        j += f === "-c" ? 2 : 1;
      }
      return;
    }
    let key = null, end = i;
    for (const len of [3, 2, 1]) {
      if (i + len > ws.length) continue;
      const k = ws.slice(i, i + len).map((w) => w.v).join(" ");
      if (d[k]) { key = k; end = i + len - 1; break; }
    }
    if (!key && w0 === "git") { // git -C тека log: прапорці git перед підкомандою
      let j = i + 1;
      while (j + 1 < ws.length && /^-[Cc]$/.test(ws[j].v)) j += 2;
      if (j < ws.length && d["git " + ws[j].v]) {
        if (d.git) flagMarks("git", ws.slice(0, j), i + 1, d, out);
        out.push({ s: ws[i].s, e: ws[i].e, k: "git " + ws[j].v }, { s: ws[j].s, e: ws[j].e, k: "git " + ws[j].v });
        flagMarks("git " + ws[j].v, ws, j + 1, d, out);
        return;
      }
    }
    if (!key) { // ip -br a, apt -y install: прапорці перед підкомандою
      let j = i + 1;
      while (j < ws.length && ws[j].v[0] === "-") j++;
      if (j > i + 1 && j < ws.length && d[w0 + " " + ws[j].v]) {
        const k2 = w0 + " " + ws[j].v;
        out.push({ s: ws[i].s, e: ws[i].e, k: k2 }, { s: ws[j].s, e: ws[j].e, k: k2 });
        flagMarks(k2, ws.slice(0, j), i + 1, d, out);
        flagMarks(k2, ws, j + 1, d, out);
        return;
      }
    }
    if (!key) {
      if (/^(\.{0,2}|~)\/[\w.-]/.test(w0) && d["./скрипт"]) out.push({ s: ws[i].s, e: ws[i].e, k: "./скрипт" });
      return;
    }
    out.push({ s: ws[i].s, e: ws[end].e, k: key });
    flagMarks(key, ws, end + 1, d, out);
  }

  function wrap(code, d) {
    const src = code.textContent;
    const ms = marks(lex(src), d).sort((a, b) => a.s - b.s);
    let html = "", pos = 0;
    for (const m of ms) {
      if (m.s < pos) continue;
      html += escH(src.slice(pos, m.s));
      const attrs = ` data-k="${escH(m.k)}"` + (m.f ? ` data-f="${escH(m.f)}"` : "") + (m.a ? ` data-a="${escH(m.a)}"` : "");
      html += `<button type="button" class="ck"${attrs} aria-haspopup="dialog">${escH(src.slice(m.s, m.e))}</button>`;
      pos = m.e;
    }
    html += escH(src.slice(pos));
    code.innerHTML = html;
    code.dataset.ck = "1";
  }

  async function enhance(root) {
    if (!root) return;
    const blocks = [...root.querySelectorAll("pre > code")].filter((c) => LANGS.test(c.className) && !c.dataset.ck);
    if (!blocks.length) return;
    const d = await load();
    if (!d || !Object.keys(d).length) return;
    blocks.forEach((b) => { try { wrap(b, d); } catch (e) { /* підказки - не головне, код лишається як був */ } });
  }

  // текст довідника: `код` -> <code>
  const rt = (s) => escH(s).replace(/`([^`]+)`/g, "<code>$1</code>");
  function close(back = true) {
    if (!tip) return;
    tip.remove();
    tip = null;
    if (back && opener && document.contains(opener)) opener.focus({ preventScroll: true });
    opener = null;
  }
  function show(btn) {
    const d = D || {};
    const e = d[btn.dataset.k];
    if (!e) return;
    close(false);
    opener = btn;
    const [id, short, name, fl, ar] = e;
    let body = `<p class="cks"><code>${escH(btn.dataset.k)}</code> - ${rt(short)}.</p><p class="muted ckn">Назва: ${rt(name)}</p>`;
    const f = btn.dataset.f;
    if (f) {
      const parts = fl[f] ? [[f, fl[f]]] : [...f.slice(1)].map((c) => ["-" + c, fl["-" + c] || "дивись у довіднику"]);
      if (!fl[f] && parts.length > 1) body += `<p class="muted">${escH(f)} = ${parts.map((p) => escH(p[0])).join(" ")} (короткі прапорці можна склеювати)</p>`;
      body += parts.map(([k, w]) => `<p><code>${escH(k)}</code> - ${rt(w)}</p>`).join("");
    }
    if (btn.dataset.a && ar[btn.dataset.a]) body += `<p><code>${escH(btn.dataset.a)}</code> - ${rt(ar[btn.dataset.a])}</p>`;
    const onPage = /#\/u\/prog\/komandy(\/|$)/.test(location.hash);
    const link = onPage ? `<a href="#/u/prog/komandy/${id}" data-cklink>До запису в довіднику</a>`
      : `<a href="#/u/prog/komandy/${id}">Усе про ${escH(btn.dataset.k)}: приклади, як скасувати</a>`;
    tip = document.createElement("div");
    tip.className = "cktip";
    tip.setAttribute("role", "dialog");
    tip.setAttribute("aria-label", "Підказка: " + btn.dataset.k);
    tip.tabIndex = -1;
    const x = typeof icon === "function" ? icon("x") : "×";
    tip.innerHTML = `<button type="button" class="icon-btn ckx" aria-label="Закрити підказку">${x}</button>${body}<p class="ckl">${link}</p>`;
    document.body.appendChild(tip);
    const narrow = window.innerWidth < 640;
    if (narrow) tip.classList.add("sheet");
    else {
      const r = btn.getBoundingClientRect();
      const w = tip.offsetWidth, h = tip.offsetHeight;
      let left = Math.min(Math.max(8, r.left), window.innerWidth - w - 8);
      let top = r.bottom + 6;
      if (top + h > window.innerHeight - 8 && r.top - h - 6 > 8) top = r.top - h - 6;
      tip.style.left = left + window.scrollX + "px";
      tip.style.top = top + window.scrollY + "px";
    }
    tip.querySelector(".ckx").addEventListener("click", () => close());
    tip.querySelector("a").addEventListener("click", () => close(false));
    tip.focus({ preventScroll: true });
  }

  document.addEventListener("click", (ev) => {
    const b = ev.target.closest && ev.target.closest(".ck");
    if (b) { ev.preventDefault(); if (tip && opener === b) close(); else load().then(() => show(b)); return; }
    if (tip && !tip.contains(ev.target)) close(false);
  });
  document.addEventListener("keydown", (ev) => { if (ev.key === "Escape" && tip) close(); });
  window.addEventListener("hashchange", () => close(false));

  // вкладка «Команди»: пошук по назві, прапорцю, словах пояснення
  function searchPage(root) {
    const inp = root && root.querySelector("#cmdq");
    if (!inp) return;
    const items = [...root.querySelectorAll("details.cmd")];
    const heads = [...root.querySelectorAll("h2.cmdg")];
    const cnt = root.querySelector("#cmdn");
    const run = () => {
      const q = inp.value.trim().toLowerCase();
      const ws = q.split(/\s+/).filter(Boolean);
      let n = 0;
      for (const it of items) {
        const ok = !ws.length || ws.every((w) => it.dataset.s.includes(w));
        it.hidden = !ok;
        if (ok) n++;
        if (q && it.dataset.k.toLowerCase() === q) it.open = true;
      }
      for (const h of heads) {
        let el = h.nextElementSibling, vis = false;
        while (el && !el.matches("h2.cmdg")) { if (el.matches("details.cmd") && !el.hidden) { vis = true; break; } el = el.nextElementSibling; }
        h.hidden = !vis;
      }
      if (cnt) cnt.textContent = ws.length ? (n ? `Знайдено: ${n}` : "Нічого не знайдено. Спробуй назву команди або слово з пояснення.") : `Усього команд: ${items.length}`;
    };
    inp.addEventListener("input", run);
    run();
  }

  return { enhance, searchPage, lex, marks, load };
})();
