"use strict";
// Сайт підготовки: маршрути #/..., сторінки з data/, тести з таймером, статистика в localStorage.

const $ = (s, el = document) => el.querySelector(s);
const app = $("#app");
const KEY = "uniprep:v1";
let UNITS = [];

// ---------- сховище ----------
function load() {
  try { return JSON.parse(localStorage.getItem(KEY)) || { q: {} }; } catch (e) { return { q: {} }; }
}
function save(st) {
  try { localStorage.setItem(KEY, JSON.stringify(st)); } catch (e) { /* приватний режим */ }
}
let STORE = load();

function record(unit, q, ok) {
  const id = unit + "/" + q.id;
  const r = STORE.q[id] || { r: 0, w: 0, t: q.topic };
  if (ok) r.r++; else r.w++;
  r.last = ok ? 1 : 0;
  r.t = q.topic;
  STORE.q[id] = r;
  save(STORE);
}
function unitStats(unit) {
  let r = 0, w = 0, seen = 0, wrongNow = 0;
  const topics = {};
  for (const [id, v] of Object.entries(STORE.q)) {
    if (!id.startsWith(unit + "/")) continue;
    seen++; r += v.r; w += v.w; if (v.last === 0) wrongNow++;
    const t = topics[v.t] || (topics[v.t] = { r: 0, w: 0 });
    t.r += v.r; t.w += v.w;
  }
  return { r, w, seen, wrongNow, topics };
}

// ---------- утиліти ----------
function esc(s) {
  return String(s ?? "").replace(/[&<>"']/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]));
}
// текст питання: екрануємо, потім [[a // b]] -> дріб, переноси рядків
function rich(s) {
  return esc(s)
    .replace(/\[\[(.+?)\/\/(.+?)\]\]/g, (m, a, b) => `<span class="fr"><span>${a.trim()}</span><span>${b.trim()}</span></span>`)
    .replace(/\n/g, "<br>");
}
function shuffle(a) {
  for (let i = a.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [a[i], a[j]] = [a[j], a[i]];
  }
  return a;
}
const cache = {};
async function getJSON(url) {
  if (!cache[url]) cache[url] = fetch(url).then((r) => { if (!r.ok) throw new Error(r.status); return r.json(); });
  return cache[url];
}
async function getText(url) {
  const r = await fetch(url);
  if (!r.ok) throw new Error(r.status);
  return r.text();
}
function kindBadge(u) {
  if (u.kind === "colloquium") return '<span class="badge k">Колоквіум</span>';
  if (u.kind === "exam") return '<span class="badge">Іспит</span>';
  return '<span class="badge z">Залік</span>';
}
function setTitle(t) { document.title = t ? t + " - Підготовка до сесії" : "Підготовка до сесії"; }
function focusMain() { app.focus({ preventScroll: true }); window.scrollTo(0, 0); }

// ---------- тема ----------
const themeBtn = $("#theme");
function applyTheme(t) {
  if (t === "light" || t === "dark") document.documentElement.dataset.theme = t;
  else delete document.documentElement.dataset.theme;
  themeBtn.setAttribute("aria-label", "Тема: " + ({ light: "світла", dark: "темна" }[t] || "авто"));
  themeBtn.textContent = { light: "☀", dark: "☾" }[t] || "◐";
}
let theme = "auto";
try { theme = localStorage.getItem(KEY + ":theme") || "auto"; } catch (e) { /* */ }
applyTheme(theme);
themeBtn.addEventListener("click", () => {
  theme = { auto: "light", light: "dark", dark: "auto" }[theme];
  try { localStorage.setItem(KEY + ":theme", theme); } catch (e) { /* */ }
  applyTheme(theme);
});

// ---------- мережа / офлайн ----------
const net = $("#net");
let offlineReady = false;
function showNet() {
  if (!navigator.onLine) { net.textContent = "офлайн"; net.className = "net"; }
  else if (offlineReady) { net.textContent = "✓ є офлайн"; net.className = "net ok"; }
  else { net.textContent = ""; net.className = "net"; }
}
window.addEventListener("online", () => { showNet(); route(); });
window.addEventListener("offline", () => { showNet(); });
if ("serviceWorker" in navigator) {
  navigator.serviceWorker.register("sw.js").then(() => navigator.serviceWorker.ready).then(() => {
    offlineReady = true; showNet();
  }).catch(() => { /* без офлайну */ });
}
let installEvt = null;
window.addEventListener("beforeinstallprompt", (e) => { e.preventDefault(); installEvt = e; const b = $("#install"); if (b) b.hidden = false; });

// ---------- сторінки ----------
async function home() {
  setTitle("");
  const card = (u) => {
    const s = unitStats(u.id);
    const tot = s.r + s.w;
    const pct = tot ? Math.round((100 * s.r) / tot) : 0;
    return `<a class="card unit" href="#/u/${u.id}">
      ${kindBadge(u)}
      <h3>${esc(u.title)}</h3>
      <div class="row"><span>Дата: ${esc(u.date)}</span><span>${esc(u.points)}</span></div>
      <div class="row"><span>${u.nq} питань у тестах</span>${u.nv ? `<span>${u.nv} відео</span>` : ""}${tot ? `<span>правильно ${pct} %</span>` : ""}</div>
      ${tot ? `<div class="bar" aria-hidden="true"><i style="width:${pct}%"></i></div>` : ""}
    </a>`;
  };
  const kol = UNITS.filter((u) => u.kind === "colloquium").map(card).join("");
  const ex = UNITS.filter((u) => u.kind === "exam").map(card).join("");
  const zl = UNITS.filter((u) => u.kind === "zalik").map(card).join("");
  app.innerHTML = `
    <h1>Підготовка до колоквіумів і сесії</h1>
    <p class="muted">Перший семестр, 1 курс фізфаку. Зараз - лише два колоквіуми, 30-40 хв на день. Іспити і заліки - після них. Після першого відкриття все працює без інтернету (крім відео).</p>
    <div class="links">
      <a class="btn primary" href="#/plan">План до колоквіумів</a>
      <a class="btn" href="#/stats">Мої слабкі теми</a>
      <a class="btn" href="#/glossary">Словник EN-UA</a>
      <a class="btn" href="#/about">Як користуватись</a>
    </div>
    <button id="install" class="btn" type="button" hidden>Встановити на телефон</button>
    <h2>Зараз: колоквіуми</h2>
    <div class="units">${kol}</div>
    <details class="later"><summary>Після колоквіумів: 4 іспити</summary><div class="units">${ex}</div></details>
    <details class="later"><summary>Заліки</summary><div class="units">${zl}</div></details>
    <p><a href="kalendar.ics" download>Календар .ics (лише відомі дати колоквіумів і іспитів)</a></p>
    <p class="footer">Власні конспекти, задачі й тести. Числові відповіді перевірені скриптом. Дати, яких нема в джерелах, позначені «спитати в групі».</p>`;
  const b = $("#install");
  if (installEvt) b.hidden = false;
  b.addEventListener("click", async () => { if (!installEvt) return; installEvt.prompt(); await installEvt.userChoice; installEvt = null; b.hidden = true; });
}

async function staticPage(key, title) {
  setTitle(title);
  try {
    const html = await getText(`data/${key}.html`);
    app.innerHTML = `<p><a href="#/">← На головну</a></p><article class="doc">${html}</article>`;
  } catch (e) {
    app.innerHTML = `<p>Сторінку не вдалося відкрити (${esc(e.message)}). Якщо ти офлайн - відкрий сайт раз з інтернетом.</p>`;
  }
}

function unitTabs(u, cur) {
  return `<nav class="tabs" aria-label="Розділи">${u.pages.map((p) =>
    `<a href="#/u/${u.id}/${p.key}"${p.key === cur ? ' aria-current="page"' : ""}>${esc(p.title)}</a>`).join("")}</nav>`;
}

async function unitPage(id, page) {
  const u = UNITS.find((x) => x.id === id);
  if (!u) return notFound();
  if (!page) page = u.pages[0] ? u.pages[0].key : "test";
  setTitle(u.title);
  const head = `<p><a href="#/">← Усі предмети</a></p>
    ${kindBadge(u)}<h1>${esc(u.title)}</h1>
    <p class="muted">Дата: ${esc(u.date)}. ${esc(u.points)}. ${esc(u.format || "")}</p>
    ${unitTabs(u, page)}`;
  if (page === "test") return testStart(u, head);
  if (page === "video") return videoPage(u, head);
  try {
    const html = await getText(`data/${u.id}/${page}.html`);
    app.innerHTML = head + `<article class="doc">${html}</article>`;
  } catch (e) {
    app.innerHTML = head + `<p>Не вдалося відкрити (${esc(e.message)}).</p>`;
  }
}

async function videoPage(u, head) {
  const vd = await getJSON(`data/${u.id}/videos.json`);
  const online = navigator.onLine;
  const html = vd.topics.map((t) => `
    <h2>${esc(t.topic)}</h2>
    ${t.videos.map((v, i) => `
      <div class="card vid">
        <strong>${esc(v.title)}</strong>
        <div class="meta">${esc(v.author)} · ${esc(v.duration)} · ${v.lang === "en" ? "англійською (слова - у Словнику EN-UA)" : "українською"}</div>
        ${v.why ? `<div class="meta">${esc(v.why)}</div>` : ""}
        ${online
          ? `<button class="btn play" type="button" data-id="${esc(v.id)}" data-start="${v.start || 0}">▶ Дивитись тут</button>`
          : `<p class="offline-note">Офлайн: відео відкриється, коли буде інтернет.</p>`}
        <p><a href="https://www.youtube.com/watch?v=${esc(v.id)}${v.start ? "&t=" + v.start + "s" : ""}" target="_blank" rel="noopener">Відкрити на YouTube</a></p>
      </div>`).join("")}`).join("");
  app.innerHTML = head + `<p class="muted">Кожне відео перевірене: існує і саме про цю тему (${esc(vd.checked || "")}). Відео не зберігаються офлайн.</p>` + html;
  app.querySelectorAll(".play").forEach((b) => b.addEventListener("click", () => {
    const f = document.createElement("div");
    f.className = "frame";
    const start = Number(b.dataset.start) || 0;
    f.innerHTML = `<iframe src="https://www.youtube-nocookie.com/embed/${encodeURIComponent(b.dataset.id)}?autoplay=1${start ? "&start=" + start : ""}" title="Відео" allow="autoplay; encrypted-media; picture-in-picture; fullscreen" allowfullscreen loading="lazy"></iframe>`;
    b.replaceWith(f);
  }));
}

async function testStart(u, head) {
  const pool = await loadPool(u);
  const st = unitStats(u.id);
  const wrongIds = pool.filter((q) => (STORE.q[q._unit + "/" + q.id] || {}).last === 0);
  const topics = [...new Set(pool.map((q) => q.topic))];
  const weak = Object.entries(st.topics)
    .map(([t, v]) => ({ t, p: v.r / (v.r + v.w), n: v.r + v.w }))
    .filter((x) => x.n > 0).sort((a, b) => a.p - b.p).slice(0, 5);
  const t = u.test || {};
  app.innerHTML = head + `
    <div class="card">
      <h2 style="margin-top:4px">Тести: ${pool.length} питань</h2>
      <p>${esc(t.note || "")}</p>
      <div class="btn-row">
        <a class="btn primary" href="#/q/${u.id}/real">Як на справжньому${t.timer ? ` (${t.count} пит., ${t.timer} хв)` : ""}</a>
        <a class="btn" href="#/q/${u.id}/train">Тренування з поясненнями</a>
        <a class="btn" href="#/q/${u.id}/recall">Пригадай сам (картки)</a>
        <a class="btn" href="#/q/${u.id}/wrong"${wrongIds.length ? "" : ' aria-disabled="true"'}>Лише помилки (${wrongIds.length})</a>
      </div>
      <details><summary>Тренувати лише вибрані теми</summary>
        <div class="filter">${topics.map((tp, i) => `<label><input type="checkbox" value="${i}"> ${esc(tp)}</label>`).join("")}</div>
        <button class="btn" type="button" id="byTopic">Почати по вибраних темах</button>
      </details>
    </div>
    ${weak.length ? `<div class="card"><h3 style="margin-top:4px">Найслабші теми</h3><ul class="topics">${weak.map((w) => `<li>${esc(w.t)} - <span class="chip">${Math.round(w.p * 100)} % з ${w.n}</span></li>`).join("")}</ul></div>` : ""}`;
  $("#byTopic").addEventListener("click", () => {
    const sel = [...app.querySelectorAll(".filter input:checked")].map((x) => topics[+x.value]);
    if (!sel.length) return;
    sessionStorage.setItem("uniprep:topics", JSON.stringify(sel));
    location.hash = `#/q/${u.id}/topics`;
  });
}

async function loadPool(u) {
  const ids = [u.id, ...(u.include || [])];
  const out = [];
  const seen = new Set();
  for (const id of ids) {
    let d;
    try { d = await getJSON(`data/${id}/quiz.json`); } catch (e) { continue; }
    for (const q of d.questions) {
      const k = id + "/" + q.id;
      if (seen.has(k)) continue;
      seen.add(k);
      out.push(Object.assign({ _unit: id }, q));
    }
  }
  return out;
}

// ---------- тест ----------
let timerId = null;
async function quiz(id, mode) {
  const u = UNITS.find((x) => x.id === id);
  if (!u) return notFound();
  setTitle("Тест: " + u.title);
  let pool = await loadPool(u);
  const t = u.test || {};
  if (mode === "wrong") pool = pool.filter((q) => (STORE.q[q._unit + "/" + q.id] || {}).last === 0);
  if (mode === "topics") {
    let sel = [];
    try { sel = JSON.parse(sessionStorage.getItem("uniprep:topics")) || []; } catch (e) { /* */ }
    pool = pool.filter((q) => sel.includes(q.topic));
  }
  if (!pool.length) {
    app.innerHTML = `<p><a href="#/u/${id}/test">← Назад</a></p><p>Тут поки нема питань${mode === "wrong" ? " - помилок немає 🎉" : ""}.</p>`;
    return;
  }
  shuffle(pool);
  const real = mode === "real";
  if (real && t.count) pool = pool.slice(0, t.count);
  const qs = pool.map((q) => {
    const c = Object.assign({}, q);
    if (q.options) {
      const order = shuffle(q.options.map((_, i) => i));
      if (q.keepOrder) order.sort((a, b) => a - b);
      c._order = order;
    }
    return c;
  });
  const S = { u, mode, real, qs, i: 0, ans: new Array(qs.length).fill(null), done: false, end: real && t.timer ? Date.now() + t.timer * 60000 : 0 };
  S.vids = await loadVideos([u.id, ...(u.include || [])]);
  clearInterval(timerId);
  if (S.end) timerId = setInterval(() => tick(S), 1000);
  if (mode === "recall") { S.known = 0; return renderRecall(S); }
  renderQ(S);
}

// головне відео теми (з таймкодом) - показуємо лише після неправильної відповіді
async function loadVideos(ids) {
  const m = {};
  for (const id of ids) {
    let d;
    try { d = await getJSON(`data/${id}/videos.json`); } catch (e) { continue; }
    for (const t of d.topics) {
      const v = t.videos.find((x) => x.main) || t.videos[0];
      if (v) m[id + "|" + t.topic] = v;
    }
  }
  return m;
}
function mmss(sec) { sec = Number(sec) || 0; return Math.floor(sec / 60) + ":" + String(sec % 60).padStart(2, "0"); }
function videoHint(S, q) {
  const v = S.vids && S.vids[q._unit + "|" + q.topic];
  if (!v) return "";
  if (!navigator.onLine) return `<p class="offline-note">Є відео з розвʼязанням цієї теми - відкриється, коли буде інтернет.</p>`;
  const url = `https://www.youtube.com/watch?v=${encodeURIComponent(v.id)}${v.start ? "&t=" + v.start + "s" : ""}`;
  return `<p class="vhint">▶ <a href="${url}" target="_blank" rel="noopener">Відео: ${esc(v.title)}${v.start ? " (з " + mmss(v.start) + ")" : ""}</a>${v.lang === "en" ? ' <span class="muted">англ., слова - у <a href="#/glossary">Словнику</a></span>' : ""}</p>`;
}

// режим «пригадай сам»: питання без варіантів -> показати відповідь -> знав / не знав
function renderRecall(S) {
  if (S.i >= S.qs.length) {
    const n = S.qs.length;
    app.innerHTML = `<p><a href="#/u/${S.u.id}/test">← До тестів</a></p><h1>Пригадування: результат</h1>
      <div class="card"><div class="score">Знав ${S.known} з ${n}</div>
      <div class="btn-row"><a class="btn primary" href="#/q/${S.u.id}/recall" id="again">Ще раз</a><a class="btn" href="#/q/${S.u.id}/wrong">Лише помилки</a></div></div>`;
    $("#again").addEventListener("click", (e) => { e.preventDefault(); quiz(S.u.id, "recall"); });
    return focusMain();
  }
  const q = S.qs[S.i];
  const shown = S.shown;
  app.innerHTML = `<div class="qhead"><a href="#/u/${S.u.id}/test">✕ Вийти</a><span>${S.i + 1} / ${S.qs.length}</span><span>пригадування</span></div>
    <div class="card q"><div class="topic">${esc(q.topic)}</div><p>${rich(q.q)}</p>${q.pre ? `<pre>${esc(q.pre)}</pre>` : ""}
    ${shown ? `<div class="verdict">Відповідь: ${rich(answerText(q))}</div>
      <div class="exp">${rich(q.explain || "")}${q.explainPre ? `<pre>${esc(q.explainPre)}</pre>` : ""}${q.src ? `<div class="src">Джерело: ${esc(q.src)}</div>` : ""}</div>` : `<p class="muted">Скажи або запиши відповідь сам, потім відкрий.</p>`}
    </div>
    <div class="btn-row">${shown
      ? `<button class="btn primary" type="button" id="knew">✓ Знав</button><button class="btn" type="button" id="didnt">✗ Не знав</button>`
      : `<button class="btn primary" type="button" id="show">Показати відповідь</button>`}</div>
    <div id="vh"></div>`;
  const on = (sel, fn) => { const el = $(sel); if (el) el.addEventListener("click", fn); };
  on("#show", () => { S.shown = true; renderRecall(S); });
  const next = (ok) => {
    record(q._unit, q, ok);
    if (ok) S.known++;
    if (!ok && !S.hinted) { S.hinted = true; const h = videoHint(S, q); if (h) { app.querySelector(".btn-row").remove(); $("#vh").innerHTML = h + `<button class="btn" type="button" id="go">Далі →</button>`; on("#go", () => { S.hinted = false; S.shown = false; S.i++; renderRecall(S); focusMain(); }); return; } }
    S.hinted = false; S.shown = false; S.i++; renderRecall(S); focusMain();
  };
  on("#knew", () => next(true));
  on("#didnt", () => next(false));
}

function tick(S) {
  const el = $("#timer");
  const left = Math.max(0, Math.round((S.end - Date.now()) / 1000));
  if (el) {
    el.textContent = `${Math.floor(left / 60)}:${String(left % 60).padStart(2, "0")}`;
    el.classList.toggle("low", left < 60);
  }
  if (left <= 0 && !S.done) { clearInterval(timerId); finish(S, true); }
}

function isRight(q, a) {
  if (a == null) return false;
  if (q.type === "single") return a === q.answer;
  if (q.type === "multi") {
    const x = [...a].sort().join(","), y = [...q.answer].sort().join(",");
    return x === y;
  }
  if (q.type === "number") {
    const v = parseNum(a);
    if (v == null) return false;
    const tol = q.tol ?? 0.01;
    return Math.abs(v - q.answer) <= tol * Math.abs(q.answer) + (q.atol ?? 1e-9);
  }
  if (q.type === "short") {
    const n = norm(a);
    return (q.accept || [q.answer]).some((x) => norm(x) === n);
  }
  return false;
}
function parseNum(s) {
  s = String(s).trim().replace(/\s/g, "").replace(",", ".").replace("−", "-");
  const m = s.match(/^(-?\d+(?:\.\d+)?)\/(\d+(?:\.\d+)?)$/);
  if (m) return Number(m[1]) / Number(m[2]);
  const v = Number(s);
  return s === "" || Number.isNaN(v) ? null : v;
}
function norm(s) {
  return String(s).toLowerCase().replace(/[ʼ’'`]/g, "'").replace(/[.,;:!?«»"()]/g, " ").replace(/\s+/g, " ").trim();
}
function answerText(q) {
  if (q.type === "single") return q.options[q.answer];
  if (q.type === "multi") return q.answer.map((i) => q.options[i]).join("; ");
  if (q.type === "number") return String(q.answerText || q.answer).replace(".", ",");
  return q.answer;
}

function renderQ(S) {
  const q = S.qs[S.i];
  const a = S.ans[S.i];
  const answered = a != null && a.locked;
  const head = `<div class="qhead"><a href="#/u/${S.u.id}/test">✕ Вийти</a>
    <span>${S.i + 1} / ${S.qs.length}</span>
    ${S.end ? `<span class="timer" id="timer" role="timer" aria-label="Залишилось часу"></span>` : `<span>${{ wrong: "помилки", recall: "пригадування" }[S.mode] || "тренування"}</span>`}</div>`;
  let body = `<div class="card q"><div class="topic">${esc(q.topic)}</div><p>${rich(q.q)}</p>${q.pre ? `<pre>${esc(q.pre)}</pre>` : ""}`;
  if (q.type === "single" || q.type === "multi") {
    body += `<div class="opts" role="${q.type === "single" ? "radiogroup" : "group"}">` + q._order.map((oi) => {
      const sel = a && (q.type === "single" ? a.v === oi : (a.v || []).includes(oi));
      let cls = "opt" + (q.type === "multi" ? " multi" : "");
      if (answered && !S.real) {
        const correct = q.type === "single" ? oi === q.answer : q.answer.includes(oi);
        if (correct) cls += " right"; else if (sel) cls += " wrong";
      }
      return `<button type="button" class="${cls}" data-o="${oi}" aria-pressed="${sel ? "true" : "false"}"${answered && !S.real ? " disabled" : ""}><span class="mk" aria-hidden="true"></span><span>${rich(q.options[oi])}</span></button>`;
    }).join("") + `</div>`;
    if (q.type === "multi" && !(answered && !S.real)) body += `<p class="muted">Кілька правильних варіантів.</p>`;
  } else {
    const val = a ? esc(a.v) : "";
    body += `<form class="inp" id="inpf"><label class="sr" for="inp">Відповідь</label><input id="inp" autocomplete="off" ${q.type === "number" ? 'inputmode="decimal"' : ""} value="${val}" placeholder="${q.type === "number" ? "число, напр. 2,5 або 5/2" : "відповідь"}"${answered && !S.real ? " disabled" : ""}></form>`;
  }
  if (answered && !S.real) {
    const ok = isRight(q, a.v);
    body += `<div class="verdict ${ok ? "ok" : "bad"}">${ok ? "✓ Правильно" : "✗ Неправильно"}</div>
      ${ok ? "" : `<div>Правильна відповідь: <strong>${rich(answerText(q))}</strong></div>${videoHint(S, q)}`}
      <div class="exp">${rich(q.explain || "")}${q.explainPre ? `<pre>${esc(q.explainPre)}</pre>` : ""}${q.src ? `<div class="src">Джерело: ${esc(q.src)}</div>` : ""}</div>`;
  }
  body += `</div>`;
  const last = S.i === S.qs.length - 1;
  let nav = `<div class="btn-row">`;
  if (S.real) {
    if (S.i > 0) nav += `<button class="btn" type="button" id="prev">← Назад</button>`;
    nav += last ? `<button class="btn primary" type="button" id="fin">Завершити</button>` : `<button class="btn primary" type="button" id="next">Далі →</button>`;
  } else if (!answered) {
    nav += `<button class="btn primary" type="button" id="check">Перевірити</button>`;
  } else {
    nav += last ? `<button class="btn primary" type="button" id="fin">Результат</button>` : `<button class="btn primary" type="button" id="next">Далі →</button>`;
  }
  nav += `</div>`;
  app.innerHTML = head + body + nav;
  if (S.end) tick(S);

  app.querySelectorAll(".opt").forEach((b) => b.addEventListener("click", () => {
    const oi = +b.dataset.o;
    let cur = S.ans[S.i] || { v: q.type === "multi" ? [] : null };
    if (q.type === "single") cur.v = oi;
    else cur.v = cur.v.includes(oi) ? cur.v.filter((x) => x !== oi) : [...cur.v, oi];
    S.ans[S.i] = cur;
    if (q.type === "single" && !S.real) return lockAnswer(S);
    renderQ(S);
  }));
  const inp = $("#inp");
  if (inp) {
    inp.addEventListener("input", () => { S.ans[S.i] = { v: inp.value }; });
    $("#inpf").addEventListener("submit", (e) => { e.preventDefault(); if (S.real) go(S, 1); else lockAnswer(S); });
  }
  const on = (sel, fn) => { const el = $(sel); if (el) el.addEventListener("click", fn); };
  on("#check", () => lockAnswer(S));
  on("#next", () => go(S, 1));
  on("#prev", () => go(S, -1));
  on("#fin", () => finish(S, false));
}

function lockAnswer(S) {
  const q = S.qs[S.i];
  const a = S.ans[S.i];
  if (!a || a.v == null || (Array.isArray(a.v) && !a.v.length) || a.v === "") return;
  a.locked = true;
  record(q._unit, q, isRight(q, a.v));
  renderQ(S);
}
function go(S, d) { S.i = Math.min(S.qs.length - 1, Math.max(0, S.i + d)); renderQ(S); focusMain(); }

function finish(S, timeUp) {
  if (S.done) return;
  S.done = true;
  clearInterval(timerId);
  let right = 0;
  const items = S.qs.map((q, i) => {
    const a = S.ans[i];
    const ok = a ? isRight(q, a.v) : false;
    if (S.real) record(q._unit, q, ok);
    else if (a && !a.locked) record(q._unit, q, ok);
    if (ok) right++;
    let given = "-";
    if (a && a.v != null) {
      if (q.type === "single") given = q.options[a.v];
      else if (q.type === "multi") given = a.v.map((x) => q.options[x]).join("; ") || "-";
      else given = a.v;
    }
    return `<div class="res-item ${ok ? "ok" : "bad"}"><div class="muted">${i + 1}. ${esc(q.topic)}</div>
      <p>${rich(q.q)}</p>${q.pre ? `<pre>${esc(q.pre)}</pre>` : ""}
      <div>Твоя відповідь: ${rich(given)} ${ok ? "✓" : "✗"}</div>
      ${ok ? "" : `<div>Правильно: <strong>${rich(answerText(q))}</strong></div>${videoHint(S, q)}`}
      <div class="exp">${rich(q.explain || "")}${q.explainPre ? `<pre>${esc(q.explainPre)}</pre>` : ""}${q.src ? `<div class="src">Джерело: ${esc(q.src)}</div>` : ""}</div></div>`;
  }).join("");
  const pct = Math.round((100 * right) / S.qs.length);
  const pts = S.u.test && S.u.test.points ? ` ≈ ${(S.u.test.points * right / S.qs.length).toFixed(1).replace(".", ",")} з ${S.u.test.points} балів` : "";
  app.innerHTML = `<p><a href="#/u/${S.u.id}/test">← До тестів</a></p>
    <h1>${timeUp ? "Час вийшов. " : ""}Результат</h1>
    <div class="card"><div class="score">${right} / ${S.qs.length} (${pct} %)</div><div class="muted">${pts}</div>
    <div class="btn-row"><a class="btn primary" href="#/q/${S.u.id}/${S.mode}" id="again">Ще раз</a><a class="btn" href="#/q/${S.u.id}/wrong">Лише помилки</a></div></div>
    ${items}`;
  $("#again").addEventListener("click", (e) => { e.preventDefault(); quiz(S.u.id, S.mode); });
  focusMain();
}

async function statsPage() {
  setTitle("Слабкі теми");
  const rows = UNITS.map((u) => {
    const s = unitStats(u.id);
    const list = Object.entries(s.topics).map(([t, v]) => ({ t, p: v.r / (v.r + v.w), n: v.r + v.w }))
      .sort((a, b) => a.p - b.p);
    if (!list.length) return "";
    return `<div class="card"><h3 style="margin-top:4px">${esc(u.title)}</h3>
      <p class="muted">Відповідей ${s.r + s.w}, правильно ${Math.round((100 * s.r) / (s.r + s.w))} %, зараз у помилках ${s.wrongNow}</p>
      <ul class="topics">${list.map((x) => `<li>${esc(x.t)} - <span class="chip">${Math.round(x.p * 100)} % з ${x.n}</span></li>`).join("")}</ul>
      <a class="btn" href="#/q/${u.id}/wrong">Перерозвʼязати помилки</a></div>`;
  }).join("");
  app.innerHTML = `<p><a href="#/">← На головну</a></p><h1>Мої слабкі теми</h1>
    <p class="muted">Статистика зберігається лише на цьому пристрої.</p>
    ${rows || "<p>Ще нема відповідей. Пройди будь-який тест.</p>"}
    <button class="btn" type="button" id="reset">Скинути статистику</button>`;
  $("#reset").addEventListener("click", () => {
    if (!confirm("Скинути всю статистику на цьому пристрої?")) return;
    STORE = { q: {} }; save(STORE); statsPage();
  });
}

function notFound() { app.innerHTML = `<p>Сторінки нема. <a href="#/">На головну</a></p>`; }

async function route() {
  clearInterval(timerId);
  const h = decodeURIComponent(location.hash.replace(/^#\/?/, "")).split("/");
  try {
    if (!UNITS.length) UNITS = await getJSON("data/units.json");
    if (!h[0]) await home();
    else if (h[0] === "u") await unitPage(h[1], h[2]);
    else if (h[0] === "q") await quiz(h[1], h[2] || "train");
    else if (h[0] === "plan") await staticPage("plan", "План підготовки");
    else if (h[0] === "glossary") await staticPage("glossary", "Словник EN-UA");
    else if (h[0] === "about") await staticPage("about", "Як користуватись");
    else if (h[0] === "stats") await statsPage();
    else notFound();
  } catch (e) {
    app.innerHTML = `<p>Помилка завантаження (${esc(e.message)}). Якщо ти офлайн, а сайт ще не відкривався з інтернетом, - відкрий раз онлайн.</p>`;
  }
  if (h[0] !== "q") focusMain();
}
window.addEventListener("hashchange", route);
showNet();
route();
