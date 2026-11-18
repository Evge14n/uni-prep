"use strict";
// Сайт підготовки: маршрути #/..., сторінки з data/, тести з таймером, статистика в localStorage.
// Вигляд «зошит фізика» і рух - UNIDESIGN1 (17.11.2026).

const $ = (s, el = document) => el.querySelector(s);
const app = $("#app");
const KEY = "uniprep:v1";
let UNITS = [];
const RM = window.matchMedia ? matchMedia("(prefers-reduced-motion: reduce)") : { matches: false };
const motion = () => !RM.matches;

// ---------- сховище ----------
function load() {
  try { return JSON.parse(localStorage.getItem(KEY)) || { q: {} }; } catch (e) { return { q: {} }; }
}
function save(st) {
  try { localStorage.setItem(KEY, JSON.stringify(st)); } catch (e) { /* приватний режим */ }
}
let STORE = load();
if (!STORE.d) STORE.d = {};

function dayKey(d = new Date()) {
  return d.getFullYear() + "-" + String(d.getMonth() + 1).padStart(2, "0") + "-" + String(d.getDate()).padStart(2, "0");
}
// UNIFIX1: «памʼятаю надовго» = остання відповідь правильна і дана через ≥ 20 год (≈ добу) після попередньої;
// правильно того ж дня - лише «знаю сьогодні» (коротка памʼять обманює). Та сама межа, що в боті.
const LONG_MS = 20 * 3600 * 1000;
function record(unit, q, ok, mode) {
  const id = unit + "/" + q.id;
  const r = STORE.q[id] || { r: 0, w: 0, t: q.topic };
  const now = Date.now();
  if (ok) r.r++; else r.w++;
  r.last = ok ? 1 : 0;
  r.t = q.topic;
  if (!r.f) r.f = now;                       // коли вперше відповів
  if (!ok) r.lt = 0;
  else if (r.ts && now - r.ts >= LONG_MS) r.lt = 1;
  r.ts = now;                                // остання відповідь
  if (q.type === "gen") r.g = 1;             // картка «поясни / виведи / задача» - не тестове питання
  STORE.q[id] = r;
  // день: скільки відповідей, скільки з карток, скільки по кожній темі (для «Сьогодні» і серії днів)
  const k = dayKey();
  const d = STORE.d[k] || (STORE.d[k] = { n: 0, r: 0, t: {} });
  d.n++;
  if (mode === "recall") d.r++;
  if (mode === "week" || mode === "month") d.w = (d.w || 0) + 1;
  const tk = unit + "|" + q.topic;
  d.t[tk] = (d.t[tk] || 0) + 1;
  const keys = Object.keys(STORE.d).sort();
  while (keys.length > 70) delete STORE.d[keys.shift()];
  save(STORE);
}
function unitStats(unit) {
  let r = 0, w = 0, seen = 0, wrongNow = 0, rightNow = 0;
  const topics = {};
  for (const [id, v] of Object.entries(STORE.q)) {
    if (!id.startsWith(unit + "/") || v.g) continue;
    seen++; r += v.r; w += v.w; if (v.last === 0) wrongNow++; if (v.last === 1) rightNow++;
    const t = topics[v.t] || (topics[v.t] = { r: 0, w: 0 });
    t.r += v.r; t.w += v.w;
  }
  return { r, w, seen, wrongNow, rightNow, topics };
}
// «знаю сьогодні» / «памʼятаю надовго» по розділу (тестові питання + картки «поясни/виведи»)
function memStats(unit) {
  let today = 0, long = 0, seen = 0;
  for (const [id, v] of Object.entries(STORE.q)) {
    if (!id.startsWith(unit + "/")) continue;
    seen++;
    if (v.last === 1 && v.lt) long++;
    else if (v.last === 1) today++;
  }
  return { today, long, seen };
}
function memLine(unit) {
  const m = memStats(unit);
  if (!m.seen) return "";
  return `<span class="mem"><b class="num">${m.long}</b> памʼятаю надовго · <b class="num">${m.today}</b> знаю сьогодні</span>`;
}
function streak() {
  const d = new Date();
  let n = 0;
  if (!(STORE.d[dayKey(d)] || {}).n) d.setDate(d.getDate() - 1);
  while ((STORE.d[dayKey(d)] || {}).n) { n++; d.setDate(d.getDate() - 1); }
  return n;
}
function daysWord(n) {
  const a = n % 10, b = n % 100;
  if (a === 1 && b !== 11) return "день";
  if (a >= 2 && a <= 4 && (b < 12 || b > 14)) return "дні";
  return "днів";
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
  return cache[url].catch((e) => { delete cache[url]; throw e; });
}
const tcache = {};
async function getText(url) {
  if (!tcache[url]) tcache[url] = fetch(url).then((r) => { if (!r.ok) throw new Error(r.status); return r.text(); });
  return tcache[url].catch((e) => { delete tcache[url]; throw e; });
}
function setTitle(t) { document.title = t ? t + " - Підготовка до сесії" : "Підготовка до сесії"; }
function focusMain() { app.focus({ preventScroll: true }); window.scrollTo(0, 0); }

// ---------- іконки (власні, лінійні; без емодзі) ----------
const IC = {
  today: '<rect x="3" y="5" width="18" height="16" rx="3"/><path d="M8 3v4M16 3v4M3 10h18"/><path d="m9 15 2 2 4-4"/>',
  book: '<path d="M5 4h11a3 3 0 0 1 3 3v13H8a3 3 0 0 1-3-3z"/><path d="M5 17a3 3 0 0 1 3-3h11"/><path d="M9 8h6"/>',
  plan: '<path d="M9 6h11M9 12h11M9 18h11"/><path d="m3.5 6 1 1 2-2M3.5 12l1 1 2-2"/><circle cx="5" cy="18" r="1.2"/>',
  chart: '<path d="M3 20h18"/><path d="M6 16v-5M11 16V6M16 16v-8"/>',
  x: '<path d="M18 6 6 18M6 6l12 12"/>',
  check: '<path d="m5 12.5 4.5 4.5L19 7"/>',
  left: '<path d="m14.5 18-6-6 6-6"/>',
  right: '<path d="m9.5 18 6-6-6-6"/>',
  play: '<path d="M8 5.5v13l10-6.5z"/>',
  flame: '<path d="M12 2.8c.6 3.3 4.8 5.2 4.8 10a4.8 4.8 0 0 1-9.6 0c0-2.6 1.4-4 2.3-5.6.6 1.2 1.2 2 2 2.6.6-2.2.8-4.4.5-7z"/>',
  sun: '<circle cx="12" cy="12" r="4"/><path d="M12 2.5v2M12 19.5v2M4.6 4.6 6 6M18 18l1.4 1.4M2.5 12h2M19.5 12h2M4.6 19.4 6 18M18 6l1.4-1.4"/>',
  moon: '<path d="M20 14.5A8 8 0 0 1 9.5 4a8 8 0 1 0 10.5 10.5z"/>',
  auto: '<circle cx="12" cy="12" r="8.5"/><path d="M12 3.5v17a8.5 8.5 0 0 0 0-17z" fill="currentColor"/>',
  clock: '<circle cx="12" cy="13" r="8"/><path d="M12 9v4l2.5 2M9.5 2.5h5"/>',
  cards: '<rect x="3" y="7" width="13" height="14" rx="2.5"/><path d="M8 3.5h10.5A2.5 2.5 0 0 1 21 6v11"/>',
  pen: '<path d="M4 20h4L19 9a2.8 2.8 0 0 0-4-4L4 16z"/><path d="m13.5 6.5 4 4"/>',
  redo: '<path d="M3.5 12a8.5 8.5 0 1 0 2.6-6.1L3.5 8.5"/><path d="M3.5 3.5v5h5"/>',
  target: '<circle cx="12" cy="12" r="8.5"/><circle cx="12" cy="12" r="4.5"/><circle cx="12" cy="12" r=".8"/>',
  down: '<path d="M12 4v15M6 13l6 6 6-6"/>',
  wifi: '<path d="M5 12.5a10 10 0 0 1 14 0M8.5 16a5 5 0 0 1 7 0M2 9a15 15 0 0 1 20 0"/><circle cx="12" cy="19.5" r=".8"/>',
  off: '<path d="M8.5 16a5 5 0 0 1 7 0M5 12.5a10 10 0 0 1 4-2.4M14.8 10.2a10 10 0 0 1 4.2 2.3M2 9a15 15 0 0 1 5-3M11 5a15 15 0 0 1 11 4M3 3l18 18"/>',
  sheet: '<path d="M6 3h8.5L19 7.5V21H6z"/><path d="M14 3v5h5M9 13h7M9 17h7"/>',
  video: '<rect x="2.5" y="5.5" width="14" height="13" rx="2.5"/><path d="m16.5 10 5-3v10l-5-3"/>',
  dict: '<path d="M4 5.5A2.5 2.5 0 0 1 6.5 3H20v15H6.5A2.5 2.5 0 0 0 4 20.5z"/><path d="M4 20.5A2.5 2.5 0 0 0 6.5 23H20v-5"/><path d="m8 13 2.5-6 2.5 6M8.8 11h3.4"/>',
  help: '<circle cx="12" cy="12" r="8.5"/><path d="M9.6 9.5a2.5 2.5 0 1 1 3.6 2.2c-.8.4-1.2 1-1.2 1.8v.5"/><circle cx="12" cy="17" r=".8"/>',
  cal: '<rect x="3" y="5" width="18" height="16" rx="3"/><path d="M8 3v4M16 3v4M3 10h18M8 14h2M14 14h2M8 17.5h2"/>',
  dl: '<path d="M12 4v11M7 10.5l5 5 5-5M5 20h14"/>',
};
const icon = (n, cls = "") => `<svg class="i ${cls}" viewBox="0 0 24 24" aria-hidden="true">${IC[n] || ""}</svg>`;

// колір предмета
const SUBJ = { "an-k1": "an", an: "an", "ma-k2": "ma", ma: "ma", mech: "mech", mol: "mol", prog: "prog", zfp: "zfp", hist: "hist", eng: "eng", linux: "prog", git: "prog", "prog-sec": "prog" };
const sk = (id) => SUBJ[id] || "an";
function kindBadge(u) {
  if (u.kind === "colloquium") return '<span class="badge k">Колоквіум</span>';
  if (u.kind === "exam") return '<span class="badge">Іспит</span>';
  if (u.kind === "skill") return '<span class="badge z">Навичка</span>'; // ULINUX1
  return '<span class="badge z">Залік</span>';
}
// частка питань розділу, на які остання відповідь правильна
function mastery(u) {
  const s = unitStats(u.id);
  return u.nq ? Math.min(1, s.rightNow / u.nq) : 0;
}

// кільце прогресу: SVG; заповнення анімується в animateRings()
function ring(p, size = 52, stroke = 6, label = "", cls = "") {
  const r = (size - stroke) / 2, c = 2 * Math.PI * r, h = size / 2;
  const off = c * (1 - Math.max(0, Math.min(1, p)));
  return `<span class="ring ${cls}" style="width:${size}px;height:${size}px"><svg width="${size}" height="${size}" viewBox="0 0 ${size} ${size}" aria-hidden="true">` +
    `<circle class="trk" cx="${h}" cy="${h}" r="${r}" fill="none" stroke-width="${stroke}"/>` +
    `<circle class="val" cx="${h}" cy="${h}" r="${r}" fill="none" stroke-width="${stroke}" stroke-dasharray="${c.toFixed(2)}" stroke-dashoffset="${off.toFixed(2)}" data-c="${c.toFixed(2)}"${p <= 0 ? ' opacity="0"' : ""}/>` +
    `</svg>${label}</span>`;
}
function animateRings(root = app) {
  if (!motion()) return;
  root.querySelectorAll(".ring .val").forEach((el, i) => {
    if (el.getAttribute("opacity") === "0" || !el.animate) return;
    const c = +el.dataset.c, to = +el.getAttribute("stroke-dashoffset");
    el.animate([{ strokeDashoffset: c }, { strokeDashoffset: to }], { duration: 900, delay: 120 + i * 60, easing: "cubic-bezier(.2,.8,.2,1)", fill: "backwards" });
  });
}
// каскадна поява дітей .stagger
function stagger(root = app) {
  if (!motion()) return;
  root.querySelectorAll(".stagger").forEach((box) => {
    [...box.children].forEach((ch, i) => ch.style.setProperty("--i", Math.min(i, 12)));
  });
}
// лічильник, що «набігає»
function countUp(el, to, ms = 900) {
  if (!el) return;
  if (!motion() || !to) { el.textContent = to; return; }
  const t0 = performance.now();
  const step = (t) => {
    const k = Math.min(1, (t - t0) / ms);
    el.textContent = Math.round(to * (1 - Math.pow(1 - k, 3)));
    if (k < 1) requestAnimationFrame(step);
  };
  el.textContent = 0;
  requestAnimationFrame(step);
}
// конфеті: canvas поверх сторінки, ~1,3 с, лише transform на canvas-шарі
function confetti(colors) {
  if (!motion()) return;
  const old = $("#confetti");
  if (old) old.remove();
  const c = document.createElement("canvas");
  c.id = "confetti";
  c.setAttribute("aria-hidden", "true");
  document.body.appendChild(c);
  const dpr = Math.min(2, window.devicePixelRatio || 1);
  const W = innerWidth, H = innerHeight;
  c.width = W * dpr; c.height = H * dpr;
  const g = c.getContext("2d");
  g.scale(dpr, dpr);
  const P = [];
  for (let i = 0; i < 90; i++) {
    P.push({ x: W / 2 + (Math.random() - 0.5) * W * 0.35, y: H * 0.38, vx: (Math.random() - 0.5) * 11, vy: -(Math.random() * 10 + 6),
      r: Math.random() * 6.28, vr: (Math.random() - 0.5) * 0.4, w: 6 + Math.random() * 5, h: 9 + Math.random() * 6, c: colors[i % colors.length] });
  }
  const t0 = performance.now();
  let last = t0;
  const frame = (t) => {
    const dt = Math.min(2.5, (t - last) / 16.7);
    last = t;
    const k = (t - t0) / 1300;
    g.clearRect(0, 0, W, H);
    g.globalAlpha = k > 0.75 ? Math.max(0, (1 - k) * 4) : 1;
    for (const p of P) {
      p.vy += 0.34 * dt; p.vx *= Math.pow(0.99, dt);
      p.x += p.vx * dt; p.y += p.vy * dt; p.r += p.vr * dt;
      g.save(); g.translate(p.x, p.y); g.rotate(p.r); g.fillStyle = p.c; g.fillRect(-p.w / 2, -p.h / 2, p.w, p.h * Math.abs(Math.cos(p.r * 1.7))); g.restore();
    }
    if (k < 1) requestAnimationFrame(frame); else c.remove();
  };
  requestAnimationFrame(frame);
}
function cssVar(name, el = app) { return getComputedStyle(el).getPropertyValue(name).trim(); }
function celebrate() {
  confetti([cssVar("--s") || cssVar("--pen"), cssVar("--ok"), cssVar("--flame"), cssVar("--pen"), "#f2c94c"]);
}
// хвиля від дотику на кнопках
document.addEventListener("pointerdown", (e) => {
  if (!motion()) return;
  const b = e.target.closest(".btn, .opt, .tile, .chiplink");
  if (!b || b.disabled || b.getAttribute("aria-disabled") === "true") return;
  const r = b.getBoundingClientRect();
  const d = Math.max(r.width, r.height) * 2;
  const s = document.createElement("span");
  s.className = "ripple";
  s.style.cssText = `width:${d}px;height:${d}px;left:${e.clientX - r.left - d / 2}px;top:${e.clientY - r.top - d / 2}px`;
  b.appendChild(s);
  const a = s.animate([{ transform: "scale(0)", opacity: 0.22 }, { transform: "scale(1)", opacity: 0 }], { duration: 520, easing: "cubic-bezier(.2,.8,.2,1)" });
  a.onfinish = () => s.remove();
}, { passive: true });

// ---------- навігація ----------
const NAV = [["#/", "today", "Сьогодні"], ["#/grafik", "cal", "Графік"], ["#/subjects", "book", "Предмети"], ["#/plan", "plan", "План"], ["#/stats", "chart", "Слабкі теми"]];
function drawNav() {
  const items = NAV.map(([h, ic, t]) => `<a href="${h}" data-nav="${h}">${icon(ic)}<span>${t}</span></a>`).join("");
  $(".bnav").innerHTML = items;
  $(".dnav").innerHTML = items;
}
function markNav(h0) {
  const cur = !h0 || h0 === "w" ? "#/" : h0 === "video" ? "#/grafik" : (h0 === "u" || h0 === "q" || h0 === "subjects" || h0 === "glossary" || h0 === "about") ? "#/subjects" : "#/" + h0;
  document.querySelectorAll("[data-nav]").forEach((a) => {
    if (a.dataset.nav === cur) a.setAttribute("aria-current", "page"); else a.removeAttribute("aria-current");
  });
}
drawNav();

// ---------- тема ----------
const themeBtn = $("#theme");
function applyTheme(t) {
  if (t === "light" || t === "dark") document.documentElement.dataset.theme = t;
  else delete document.documentElement.dataset.theme;
  themeBtn.setAttribute("aria-label", "Тема: " + ({ light: "світла", dark: "темна" }[t] || "авто"));
  themeBtn.innerHTML = icon({ light: "sun", dark: "moon" }[t] || "auto");
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
  if (!navigator.onLine) { net.innerHTML = icon("off") + "<span>офлайн</span>"; net.className = "net"; }
  else if (offlineReady) { net.innerHTML = icon("check") + "<span>є офлайн</span>"; net.className = "net ok"; }
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
function bindInstall() {
  const b = $("#install");
  if (!b) return;
  if (installEvt) b.hidden = false;
  b.addEventListener("click", async () => { if (!installEvt) return; installEvt.prompt(); await installEvt.userChoice; installEvt = null; b.hidden = true; });
}

// ---------- план (з data/plan.html - одне джерело, сайт не веде окремого розкладу) ----------
let PLAN = null;
async function planData() {
  if (PLAN) return PLAN;
  const html = await getText("data/plan.html");
  const doc = new DOMParser().parseFromString(html, "text/html");
  const t = doc.querySelectorAll("table");
  const cells = (tr) => [...tr.querySelectorAll("td")];
  const days = t[0] ? [...t[0].querySelectorAll("tbody tr")].map((tr) => {
    const c = cells(tr);
    return { d: c[0].textContent.trim(), what: c[1].textContent.trim(), min: parseInt(c[2].textContent, 10) || 0 };
  }) : [];
  const queue = t[1] ? [...t[1].querySelectorAll("tbody tr")].map((tr) => {
    const c = cells(tr);
    const a = tr.querySelector('a[href^="#/u/"]');
    const m = a ? a.getAttribute("href").match(/#\/u\/([^/]+)/) : null;
    // UNIFIX1 п.10: черга без колонки «День тижня»: № | Колоквіум | Тема | Задачі | Де
    return { n: parseInt(c[0].textContent, 10), coll: c[1].textContent.trim(), topic: c[2].textContent.trim(), unit: m ? m[1] : "" };
  }) : [];
  PLAN = { days, queue };
  return PLAN;
}
function topicCount(unit, topic) {
  const t = unitStats(unit).topics[topic];
  return t ? t.r + t.w : 0;
}
function startTopic(unit, topic) {
  try { sessionStorage.setItem("uniprep:topics", JSON.stringify([topic])); } catch (e) { /* */ }
  clearRun();
  location.hash = `#/q/${unit}/topics`;
}

// ---------- сторінки ----------
function unitCard(u) {
  const p = mastery(u);
  return `<a class="card unit" data-s="${sk(u.id)}" href="#/u/${u.id}">
      <div>
        ${kindBadge(u)}
        <h3>${esc(u.title)}</h3>
        <div class="row"><span>Дата: ${esc(u.date)}</span><span>${esc(u.points)}</span></div>
        <div class="row"><span>${u.nq} питань у тестах</span>${u.nv ? `<span>${u.nv} відео</span>` : ""}</div>
        ${memLine(u.id) ? `<div class="row">${memLine(u.id)}</div>` : ""}
      </div>
      ${ring(p, 56, 6, `<b>${Math.round(p * 100)}%</b>`)}
    </a>`;
}

const WD = ["нд", "пн", "вт", "ср", "чт", "пт", "сб"];
async function home() {
  setTitle("");
  delete app.dataset.s;
  let plan = { days: [], queue: [] };
  try { plan = await planData(); } catch (e) { /* без плану - лише картки */ }
  const now = new Date();
  const wd = WD[now.getDay()];
  const day = plan.days.find((d) => d.d === wd) || { what: "", min: 0 };
  const rec = STORE.d[dayKey()] || { n: 0, r: 0, t: {} };
  const next = plan.queue.find((x) => topicCount(x.unit, x.topic) < 8) || null;
  const bDone = plan.queue.find((x) => (rec.t[x.unit + "|" + x.topic] || 0) >= 8) || null;
  const aDone = rec.r >= 10;
  const coll = UNITS.filter((u) => u.kind === "colloquium");
  const aUnit = (next && UNITS.find((u) => u.id === next.unit)) || coll[0] || UNITS[0];
  const st = streak();
  const firstTime = !Object.keys(STORE.q).length;
  const dateStr = now.toLocaleDateString("uk-UA", { weekday: "long", day: "numeric", month: "long" });

  const tiles = [];
  const tile = (o) => `<a class="tile${o.main ? " main" : ""}${o.done ? " done" : ""}" data-s="${o.s}" href="${o.href}"${o.id ? ` id="${o.id}"` : ""}>
      <span class="ic">${icon(o.done ? "check" : o.ic)}</span>
      <span><small>${o.k}</small><strong>${o.t}</strong></span>
      <span class="go">${icon("right")}</span></a>`;
  const hasB = /блок Б/.test(day.what);
  if (wd === "нд") {
    // UNIFIX1: неділя - тест тижня з усього вивченого (раз на 4 тижні - «через місяць»); поки вивченого мало - шпаргалка
    const ck = cumulKind();
    const wDone = (rec.w || 0) > 0;
    if (ck) {
      tiles.push(tile({ s: "an", href: `#/w/${ck}`, ic: "redo", k: `${ck === "month" ? "Раз на 4 тижні" : "Неділя"} · ≈ 10 хв · теми впереміш`, t: ck === "month" ? "Тест «через місяць»" : "Тест тижня: усе вивчене", main: !wDone, done: wDone, id: "goW" }));
      tiles.push(tile({ s: sk(aUnit.id), href: `#/q/${aUnit.id}/recall`, ic: "cards", k: "Блок А · 5 хв", t: aDone ? "Картки на сьогодні є" : "Пригадай сам: картки", done: aDone, id: "goA" }));
    } else {
      const weak = coll.slice().sort((a, b) => mastery(a) - mastery(b))[0] || aUnit;
      tiles.push(tile({ s: sk(weak.id), href: `#/u/${weak.id}/shpargalka`, ic: "sheet", k: `${day.min || 10} хв · неділя`, t: "Перечитати шпаргалку: " + esc(weak.title), main: true }));
    }
  } else {
    tiles.push(tile({ s: sk(aUnit.id), href: `#/q/${aUnit.id}/recall`, ic: "cards", k: "Блок А · 10-15 хв · повторення", t: aDone ? "Картки на сьогодні є" : "Пригадай сам: картки", done: aDone, main: !hasB && wd !== "сб" && !aDone, id: "goA" }));
    if (hasB) {
      if (bDone) {
        tiles.push(tile({ s: sk(bDone.unit), href: `#/u/${bDone.unit}/teoriya`, ic: "check", k: "Блок Б · виконано", t: esc(bDone.topic), done: true }));
      } else if (next) {
        tiles.push(tile({ s: sk(next.unit), href: `#/u/${next.unit}/teoriya`, ic: "pen", k: `Блок Б · 20-25 хв · тема ${next.n} з ${plan.queue.length}`, t: esc(next.topic), main: true, id: "goB" }) +
          `<div class="tile-actions"><a class="chiplink" href="#/u/${next.unit}/zadachi">${icon("pen")}Задача письмово</a><button class="chiplink" type="button" id="goTopic">${icon("target")}Тест на тему</button></div>`);
      }
    }
    if (wd === "сб") {
      const best = coll.slice().sort((a, b) => mastery(b) - mastery(a))[0] || aUnit;
      tiles.push(tile({ s: sk(best.id), href: `#/q/${best.id}/real`, ic: "clock", k: "Пробний тест з таймером", t: "Як на справжньому: " + esc(best.title), main: true }));
    }
  }
  const allDone = (wd === "пн" && aDone) || (hasB && aDone && bDone);
  app.innerHTML = `
    <div class="today-grid">
      <section>
        <div class="kicker">${esc(dateStr.charAt(0).toUpperCase() + dateStr.slice(1))}</div>
        <div class="today-head"><h1>Сьогодні</h1>${day.min ? `<span class="mins num">${day.min} хв</span>` : ""}</div>
        <p class="muted" style="margin:4px 0 10px">${day.what ? esc(day.what.charAt(0).toUpperCase() + day.what.slice(1)) + ". " : ""}Норма 30-40 хв на день.</p>
        <span class="streak${st ? " on" : ""}" id="streak">${icon("flame")}${st ? `<span class="num">${st}</span> ${daysWord(st)} поспіль` : "Серія почнеться з першої відповіді"}</span>
        ${allDone ? `<p class="note-done pop">${icon("check")}План на сьогодні виконано. Можна відпочити.</p>` : ""}
        ${firstTime ? `<div class="hint" id="hint">${icon("down")}Почни звідси</div>` : ""}
        <div class="tasks stagger">${tiles.join("")}</div>
        <button id="install" class="btn" type="button" hidden>${icon("dl")}Встановити на телефон</button>
      </section>
      <section>
        <h2>Колоквіуми</h2>
        <div class="colls stagger">${coll.map(unitCard).join("")}</div>
        <p><a class="chiplink" href="#/subjects">${icon("book")}Усі предмети: іспити й заліки</a></p>
      </section>
    </div>`;
  bindInstall();
  const gt = $("#goTopic");
  if (gt && next) gt.addEventListener("click", () => startTopic(next.unit, next.topic));
  stagger(); animateRings();
  const s = $("#streak");
  if (st && sessionStorage.getItem("uniprep:lit") !== dayKey()) { s.classList.add("lit"); try { sessionStorage.setItem("uniprep:lit", dayKey()); } catch (e) { /* */ } }
  if (allDone && !rec.cele) { rec.cele = 1; STORE.d[dayKey()] = rec; save(STORE); setTimeout(celebrate, 250); }
}

async function subjects() {
  setTitle("Предмети");
  delete app.dataset.s;
  const kol = UNITS.filter((u) => u.kind === "colloquium").map(unitCard).join("");
  const ex = UNITS.filter((u) => u.kind === "exam").map(unitCard).join("");
  const zl = UNITS.filter((u) => u.kind === "zalik").map(unitCard).join("");
  const skl = UNITS.filter((u) => u.kind === "skill").map(unitCard).join(""); // ULINUX1: навички без дати (Linux)
  app.innerHTML = `
    <h1>Підготовка до колоквіумів і сесії</h1>
    <p class="muted">Перший семестр, 1 курс фізфаку. Зараз - лише два колоквіуми, 30-40 хв на день. Іспити і заліки - після них. Після першого відкриття все працює без інтернету (крім відео).</p>
    <div class="links">
      <a class="btn primary" href="#/plan">${icon("plan")}План до колоквіумів</a>
      <a class="btn" href="#/stats">${icon("chart")}Мої слабкі теми</a>
      <a class="btn" href="#/glossary">${icon("dict")}Словник EN-UA</a>
      <a class="btn" href="#/about">${icon("help")}Як користуватись</a>
    </div>
    <h2>Зараз: колоквіуми</h2>
    <div class="units stagger">${kol}</div>
    <details class="later"><summary>Після колоквіумів: 4 іспити</summary><div class="units">${ex}</div></details>
    <details class="later"><summary>Заліки</summary><div class="units">${zl}</div></details>
    ${skl ? `<details class="later"><summary>Навички: Linux, Python + безпека</summary><div class="units">${skl}</div></details>` : ""}
    <p><a class="chiplink" href="#/grafik">${icon("cal")}Графік навчання і календар для телефона</a></p>
    <p class="footer">Власні конспекти, задачі й тести. Числові відповіді тестів перевірені скриптом. Дати, яких нема в джерелах, позначені «спитати в групі».</p>`;
  stagger(); animateRings();
  app.querySelectorAll("details.later").forEach((d) => d.addEventListener("toggle", () => { if (d.open) animateRings(d); }));
}

async function staticPage(key, title) {
  setTitle(title);
  delete app.dataset.s;
  try {
    const html = await getText(`data/${key}.html`);
    app.innerHTML = `<a class="back" href="#/">${icon("left")}На головну</a><article class="doc">${html}</article>`;
  } catch (e) {
    app.innerHTML = `<p>Сторінку не вдалося відкрити (${esc(e.message)}). Якщо ти офлайн - відкрий сайт раз з інтернетом.</p>`;
  }
}

const TAB_IC = { teoriya: "book", oznachennya: "sheet", zadachi: "pen", shpargalka: "sheet", slovnyk: "dict", video: "video", test: "target" };
function unitTabs(u, cur) {
  if (cur && cur.startsWith("urok-")) cur = "uroky"; // уроки prog - сторінки всередині вкладки «Уроки»
  return `<nav class="tabs" aria-label="Розділи">${u.pages.map((p) =>
    `<a href="#/u/${u.id}/${p.key}"${p.key === cur ? ' aria-current="page"' : ""}>${esc(p.title)}</a>`).join("")}</nav>`;
}

async function unitPage(id, page) {
  const u = UNITS.find((x) => x.id === id);
  if (!u) return notFound();
  if (!page) page = u.pages[0] ? u.pages[0].key : "test";
  setTitle(u.title);
  app.dataset.s = sk(u.id);
  const p = mastery(u);
  const head = `<a class="back" href="#/subjects">${icon("left")}Усі предмети</a>
    <div class="uhead"><div>${kindBadge(u)}<h1>${esc(u.title)}</h1>
    <p class="muted">Дата: ${esc(u.date)}. ${esc(u.points)}. ${esc(u.format || "")}</p>${memLine(u.id) ? `<p class="muted">${memLine(u.id)}</p>` : ""}</div>
    ${ring(p, 64, 7, `<b>${Math.round(p * 100)}%</b>`)}</div>
    ${unitTabs(u, page)}`;
  if (page === "test") { await testStart(u, head); return animateRings(); }
  if (page === "video") { await videoPage(u, head); return animateRings(); }
  try {
    const html = await getText(`data/${u.id}/${page}.html`);
    app.innerHTML = head + `<article class="doc">${html}</article>`;
    if ((u.id === "prog" || u.id === "prog-sec") && window.PyRun) { // UNIPROG1: «Запустити» під кодом, Python офлайн
      PyRun.enhance(app.querySelector("article.doc"));
      PyRun.box(app.querySelector("#pybox"));
    }
  } catch (e) {
    app.innerHTML = head + `<p>Не вдалося відкрити (${esc(e.message)}).</p>`;
  }
  animateRings();
}

async function videoPage(u, head) {
  const vd = await getJSON(`data/${u.id}/videos.json`);
  const online = navigator.onLine;
  const html = vd.topics.map((t) => `
    <h2>${esc(t.topic)}</h2>
    ${t.videos.map((v) => `
      <div class="card vid">
        <strong>${esc(v.title)}</strong>
        <div class="meta">${esc(v.author)} · ${esc(v.duration)} · ${v.lang === "en" ? "англійською (слова - у Словнику EN-UA)" : "українською"}</div>
        ${v.why ? `<div class="meta">${esc(v.why)}</div>` : ""}
        ${online
          ? `<button class="btn play" type="button" data-id="${esc(v.id)}" data-start="${v.start || 0}">${icon("play")}Дивитись тут</button>`
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
  const s = sk(u.id);
  const mt = (href, ic, title, sub, extra = "", main = false) => `<a class="tile${main ? " main" : ""}" data-s="${s}" href="${href}"${extra}>
      <span class="ic">${icon(ic)}</span><span><strong>${title}</strong><small>${sub}</small></span><span class="go">${icon("right")}</span></a>`;
  app.innerHTML = head + `
    <h2 style="margin-top:14px">Тести: <span class="num">${pool.length}</span> питань</h2>
    ${t.note ? `<p class="muted">${esc(t.note)}</p>` : ""}
    <div class="modes stagger">
      ${mt(`#/q/${u.id}/real`, "clock", "Як на справжньому", t.timer ? `${t.count} пит., ${t.timer} хв, без підказок` : "без підказок до кінця", "", true)}
      ${mt(`#/q/${u.id}/train`, "pen", "Тренування з поясненнями", "одразу видно, чому так")}
      ${mt(`#/q/${u.id}/recall`, "cards", "Пригадай сам (картки)", u.ng ? `${RECALL_N} карток: спершу ті, що пора перевірити через добу; є «поясни» і «виведи»` : `${RECALL_N} карток: спершу ті, що пора перевірити через добу`)}
      ${mt(`#/q/${u.id}/wrong`, "redo", `Лише помилки (${wrongIds.length})`, wrongIds.length ? "перерозвʼязати те, що не вийшло" : "поки помилок нема", wrongIds.length ? "" : ' aria-disabled="true"')}
    </div>
    <details class="card picker"><summary>${icon("target")}Тренувати лише вибрані теми</summary>
      <div class="filter">${topics.map((tp, i) => `<label><input type="checkbox" value="${i}"> ${esc(tp)}</label>`).join("")}</div>
      <button class="btn subject" type="button" id="byTopic">Почати по вибраних темах</button>
    </details>
    ${weak.length ? `<div class="card"><h3 style="margin-top:2px">Найслабші теми</h3><ul class="topics">${weak.map((w) => `<li><span>${esc(w.t)}</span><span class="chip">${Math.round(w.p * 100)} % з ${w.n}</span></li>`).join("")}</ul></div>` : ""}`;
  stagger();
  $("#byTopic").addEventListener("click", () => {
    const sel = [...app.querySelectorAll(".filter input:checked")].map((x) => topics[+x.value]);
    if (!sel.length) return;
    sessionStorage.setItem("uniprep:topics", JSON.stringify(sel));
    clearRun();
    location.hash = `#/q/${u.id}/topics`;
  });
}

async function loadPool(u, withGen = false) {
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
    // UNIFIX1: у «Пригадай сам» - ще й картки «поясни, чому / виведи / задача без підказки» (data/<розділ>/gen.json)
    const un = UNITS.find((x) => x.id === id);
    if (withGen && un && un.ng) {
      try {
        const g = await getJSON(`data/${id}/gen.json`);
        for (const q of g.cards) out.push(Object.assign({ _unit: id }, q));
      } catch (e) { /* без карток на генерацію */ }
    }
  }
  return out;
}

// ---------- довга памʼять (UNIFIX1): порядок карток, перемежування, тест тижня і «через місяць» ----------
function recKey(q) { return q._unit + "/" + q.id; }
// сусідні картки - з різних тем (interleaving); групи в порядку появи, всередині порядок зберігається
function interleave(list) {
  const groups = new Map();
  for (const q of list) {
    const k = q._unit + "|" + q.topic;
    if (!groups.has(k)) groups.set(k, []);
    groups.get(k).push(q);
  }
  const out = [];
  let last = null;
  while (out.length < list.length) {
    const ks = [...groups.keys()].filter((k) => groups.get(k).length).sort((a, b) => groups.get(b).length - groups.get(a).length);
    const k = ks.find((x) => x !== last) || ks[0];
    out.push(groups.get(k).shift());
    last = k;
  }
  return out;
}
// «Пригадай сам»: спершу те, що пора перевірити через добу (ще не «надовго»), потім помилки, потім нові
// («Закінчити речення» першими, «поясни/виведи» після питань своєї теми), «надовго» - в кінці
function recallOrder(pool) {
  const now = Date.now();
  const topicPos = new Map();
  pool.forEach((q) => { const k = q._unit + "|" + q.topic; if (!topicPos.has(k)) topicPos.set(k, topicPos.size); });
  const pr = (q) => {
    const r = STORE.q[recKey(q)];
    if (!r) return 2;
    if (r.lt && r.last === 1) return 3;
    if (r.last === 0) return 1;
    return now - (r.ts || 0) >= LONG_MS ? 0 : 4; // правильно сьогодні - лише в самому кінці
  };
  const items = shuffle(pool.slice()).map((q) => ({ q, p: pr(q), s: /^Закінчіть речення/.test(q.q) ? 0 : 1, t: topicPos.get(q._unit + "|" + q.topic), g: q.type === "gen" ? 1 : 0 }));
  items.sort((a, b) => a.p - b.p || (a.p === 2 ? (a.s - b.s || a.t - b.t || a.g - b.g) : 0));
  const head = items.slice(0, RECALL_N).map((x) => x.q);
  return interleave(head);
}
const RECALL_N = 20;
const MONTH_MS = 28 * 86400000;
// пул для тесту тижня / місяця: усе вивчене в усіх розділах; тиждень - що відповідав ≥ 20 год тому;
// місяць - що вперше вчив ≥ 4 тижні тому
function cumulKeys(kind) {
  const now = Date.now();
  return Object.entries(STORE.q).filter(([, v]) => v.f && (kind === "month" ? now - v.f >= MONTH_MS : now - (v.ts || 0) >= LONG_MS)).map(([k]) => k);
}
function cumulKind() {
  const lm = STORE.m || 0;
  if (Date.now() - lm >= MONTH_MS && cumulKeys("month").length >= 5) return "month";
  return cumulKeys("week").length >= 5 ? "week" : null;
}
async function cumulTest(kind) {
  if (kind !== "week" && kind !== "month") return notFound();
  setTitle(kind === "month" ? "Тест «через місяць»" : "Тест тижня");
  delete app.dataset.s;
  clearInterval(timerId);
  const keys = new Set(cumulKeys(kind));
  const units = [...new Set([...keys].map((k) => k.split("/")[0]))];
  let pool = [];
  for (const id of units) {
    const u = UNITS.find((x) => x.id === id);
    if (u) pool = pool.concat((await loadPool({ id, include: [] }, true)).filter((q) => keys.has(recKey(q))));
  }
  if (pool.length < 5) {
    app.innerHTML = `<a class="back" href="#/">${icon("left")}На головну</a><div class="card"><p>Поки замало вивченого для тесту (треба хоча б 5 карток, на які ти відповідав учора або раніше).</p></div>`;
    return;
  }
  // спершу те, що ще не доведено «надовго», далі решта; 12 (тиждень) або 15 (місяць) карток, теми впереміш
  pool = shuffle(pool).sort((a, b) => (STORE.q[recKey(a)].lt ? 1 : 0) - (STORE.q[recKey(b)].lt ? 1 : 0));
  const qs = interleave(pool.slice(0, kind === "month" ? 15 : 12));
  const u = { id: "all", title: kind === "month" ? "Тест «через місяць»" : "Тест тижня", include: [] };
  const S = { u, mode: kind, real: false, qs, i: 0, ans: new Array(qs.length).fill(null), done: false, end: 0, enter: true, known: 0, back: "#/", cumul: kind };
  S.vids = await loadVideos(units);
  S_CUR = S;
  renderRecall(S);
}

// ---------- тест: збереження посеред проходу (назад/перезавантаження не губить відповіді) ----------
const RUN = "uniprep:run";
function saveRun(S) {
  if (S.cumul) return; // тест тижня/місяця не відновлюємо - його пул залежить від дати
  try {
    sessionStorage.setItem(RUN, JSON.stringify({ id: S.u.id, mode: S.mode, keys: S.qs.map((q) => q._unit + "/" + q.id),
      orders: S.qs.map((q) => q._order || null), ans: S.ans, i: S.i, end: S.end, known: S.known || 0 }));
  } catch (e) { /* */ }
}
function clearRun() { try { sessionStorage.removeItem(RUN); } catch (e) { /* */ } }
function loadRun(id, mode) {
  try {
    const r = JSON.parse(sessionStorage.getItem(RUN));
    if (r && r.id === id && r.mode === mode) return r;
  } catch (e) { /* */ }
  return null;
}

let timerId = null;
async function quiz(id, mode, fresh) {
  const u = UNITS.find((x) => x.id === id);
  if (!u) return notFound();
  setTitle("Тест: " + u.title);
  app.dataset.s = sk(u.id);
  let pool = await loadPool(u, mode === "recall");
  const t = u.test || {};
  clearInterval(timerId);
  S_CUR = null;
  const saved = fresh ? null : loadRun(id, mode);
  let S;
  if (saved) {
    const by = new Map(pool.map((q) => [q._unit + "/" + q.id, q]));
    const qs = saved.keys.map((k, i) => { const q = by.get(k); return q ? Object.assign({}, q, saved.orders[i] ? { _order: saved.orders[i] } : {}) : null; });
    if (qs.every(Boolean)) {
      S = { u, mode, real: mode === "real", qs, i: Math.min(saved.i, qs.length), ans: saved.ans, done: false, end: saved.end, known: saved.known, enter: true };
    }
  }
  if (!S) {
    if (mode === "wrong") pool = pool.filter((q) => (STORE.q[q._unit + "/" + q.id] || {}).last === 0);
    if (mode === "topics") {
      let sel = [];
      try { sel = JSON.parse(sessionStorage.getItem("uniprep:topics")) || []; } catch (e) { /* */ }
      pool = pool.filter((q) => sel.includes(q.topic));
    }
    if (!pool.length) {
      app.innerHTML = `<a class="back" href="#/u/${id}/test">${icon("left")}Назад</a><div class="card"><p>Тут поки нема питань${mode === "wrong" ? ". Помилок немає - так тримати." : "."}</p></div>`;
      return;
    }
    if (mode === "recall") pool = recallOrder(pool); // UNIFIX1: довга памʼять + перемежування, 20 карток
    else shuffle(pool);
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
    S = { u, mode, real, qs, i: 0, ans: new Array(qs.length).fill(null), done: false, end: real && t.timer ? Date.now() + t.timer * 60000 : 0, enter: true };
    if (mode === "recall") S.known = 0;
    saveRun(S);
  }
  S.vids = await loadVideos([u.id, ...(u.include || [])]);
  S_CUR = S;
  if (S.end) timerId = setInterval(() => tick(S), 1000);
  if (mode === "recall") return renderRecall(S);
  renderQ(S);
}
let S_CUR = null;

// головне відео теми (з таймкодом) - показуємо лише після неправильної відповіді.
// UNIFIX1 п.7: «частини» теми (parts) - питання про мінор, гіперболу тощо відкривають інше відео або іншу хвилину.
async function loadVideos(ids) {
  const m = {};
  for (const id of ids) {
    const un = UNITS.find((x) => x.id === id);
    if (!un || !un.nv) continue; // у розділі нема відео - не просимо файл (інакше 404 у консолі)
    let d;
    try { d = await getJSON(`data/${id}/videos.json`); } catch (e) { continue; }
    for (const t of d.topics) {
      const v = t.videos.find((x) => x.main) || t.videos[0];
      if (v) m[id + "|" + t.topic] = { main: v, videos: t.videos, parts: t.parts || [] };
    }
  }
  return m;
}
function pickVideo(e, q) {
  if (!e) return null;
  for (const p of e.parts) {
    let ok = false;
    try { ok = new RegExp(p.re, "i").test(q.q || ""); } catch (er) { ok = false; }
    if (!ok) continue;
    if (!p.id) return null; // до цього питання в лекціях-відео нема фрагмента - лише теорія
    const v = e.videos.find((x) => x.id === p.id);
    return v ? Object.assign({}, v, { start: p.start || 0 }) : null;
  }
  return e.main;
}
function mmss(sec) { sec = Number(sec) || 0; return Math.floor(sec / 60) + ":" + String(sec % 60).padStart(2, "0"); }
function videoHint(S, q) {
  const v = pickVideo(S.vids && S.vids[q._unit + "|" + q.topic], q);
  if (!v) return "";
  if (!navigator.onLine) return `<p class="offline-note">Є відео з розвʼязанням цієї теми - відкриється, коли буде інтернет.</p>`;
  const url = `https://www.youtube.com/watch?v=${encodeURIComponent(v.id)}${v.start ? "&t=" + v.start + "s" : ""}`;
  return `<p class="vhint">${icon("play")}<span><a href="${url}" target="_blank" rel="noopener">Відео: ${esc(v.title)}${v.start ? " (з " + mmss(v.start) + ")" : ""}</a>${v.lang === "en" ? ' <span class="muted">англ., слова - у <a href="#/glossary">Словнику</a></span>' : ""}</span></p>`;
}
function progressBar(S, done) {
  const n = S.qs.length;
  const v = Math.min(1, (S.i + (done ? 1 : 0)) / n);
  const prev = S.prog ?? v;
  S.prog = v;
  return `<div class="qprog" aria-hidden="true"><i style="transform:scaleX(${prev})" data-to="${v}"></i></div>`;
}
function settleProgress() {
  const i = $(".qprog i");
  if (i) requestAnimationFrame(() => requestAnimationFrame(() => { i.style.transform = `scaleX(${i.dataset.to})`; }));
}

// режим «пригадай сам»: картка -> переворот -> знав / не знав (кнопки або свайп)
function renderRecall(S) {
  if (S.i >= S.qs.length) return recallResult(S);
  const q = S.qs[S.i];
  const exp = `${rich(q.explain || "")}${q.explainPre ? `<pre>${esc(q.explainPre)}</pre>` : ""}${q.src ? `<div class="src">Джерело: ${esc(q.src)}</div>` : ""}`;
  const tip = q.type === "gen"
    ? (q.kind === "task" ? "Розвʼяжи в зошиті без підказки, потім переверни." : "Поясни своїми словами - вголос або в зошит, потім переверни.")
    : "Скажи або запиши відповідь сам, потім переверни картку.";
  app.innerHTML = `${progressBar(S)}<div class="qhead"><a href="${S.back || `#/u/${S.u.id}/test`}" id="exit">${icon("x")}Вийти</a><span class="num">${S.i + 1} / ${S.qs.length}</span><span>${S.cumul ? esc(S.u.title) : "картки"}</span></div>
    <div class="flash${S.enter && motion() ? " enter" : ""}" id="flash">
      <div class="drag" id="drag">
        <span class="stamp yes" aria-hidden="true">знав</span><span class="stamp no" aria-hidden="true">не знав</span>
        <div class="flip" id="flip">
          <div class="face front"><div class="topic">${esc(q.topic)}</div><p class="qtext">${rich(q.q)}</p>${q.pre ? `<pre>${esc(q.pre)}</pre>` : ""}
            <div class="tip">${icon("redo")}${tip}</div></div>
          <div class="face bk" aria-hidden="true"><div class="topic">${esc(q.topic)}</div>
            <div class="verdict">Відповідь: ${rich(answerText(q))}</div>${q.apre ? `<pre>${esc(q.apre)}</pre>` : ""}<div class="exp">${exp}</div></div>
        </div>
      </div>
    </div>
    <p class="swipe-tip" id="stip" hidden>Свайп вправо - знав, вліво - не знав</p>
    <div class="qnav" id="rnav"><button class="btn primary" type="button" id="show">${icon("redo")}Показати відповідь</button></div>
    <div id="vh"></div>`;
  S.enter = false;
  settleProgress();
  $("#exit").addEventListener("click", clearRun);
  const flash = $("#flash"), drag = $("#drag"), flip = $("#flip");
  let open = false, busy = false;
  const doOpen = () => {
    if (open) return;
    open = true;
    flash.classList.add("open");
    flash.querySelector(".front").setAttribute("aria-hidden", "true");
    flash.querySelector(".bk").removeAttribute("aria-hidden");
    $("#rnav").innerHTML = `<button class="btn ghost-bad" type="button" id="didnt">${icon("x")}Не знав</button><button class="btn good" type="button" id="knew">${icon("check")}Знав</button>`;
    $("#stip").hidden = false;
    $("#knew").addEventListener("click", () => fly(true));
    $("#didnt").addEventListener("click", () => fly(false));
    $("#knew").focus({ preventScroll: true });
  };
  $("#show").addEventListener("click", doOpen);
  flip.addEventListener("click", () => { if (!open) doOpen(); });
  const stamps = { yes: flash.querySelector(".stamp.yes"), no: flash.querySelector(".stamp.no") };
  const next = (ok) => {
    record(q._unit, q, ok, S.cumul || "recall");
    if (ok) S.known++;
    S.i++;
    saveRun(S);
    const h = ok ? "" : videoHint(S, q);
    if (h) {
      drag.style.transform = ""; drag.style.opacity = ""; stamps.yes.style.opacity = 0; stamps.no.style.opacity = 0;
      $("#rnav").innerHTML = "";
      $("#vh").innerHTML = h + `<div class="qnav"><button class="btn primary" type="button" id="go">Далі${icon("right")}</button></div>`;
      $("#go").addEventListener("click", () => { S.enter = true; renderRecall(S); focusMain(); });
      return;
    }
    S.enter = true;
    renderRecall(S);
    focusMain();
  };
  // виліт картки вбік; без руху - одразу далі
  function fly(ok) {
    if (busy) return;
    busy = true;
    if (!motion()) return next(ok);
    const w = flash.offsetWidth || 360;
    stamps[ok ? "yes" : "no"].style.opacity = 1;
    drag.classList.remove("held");
    drag.style.transition = "transform .28s cubic-bezier(.4,0,.8,.6), opacity .28s";
    drag.style.transform = `translateX(${ok ? w + 140 : -(w + 140)}px) rotate(${ok ? 22 : -22}deg)`;
    drag.style.opacity = "0";
    setTimeout(() => next(ok), 260);
  }
  // свайп з інерцією: відпустив далеко або швидко - вилітає, інакше пружно повертається
  let x0 = 0, y0 = 0, dx = 0, pid = null, dragging = false, hist = [];
  drag.addEventListener("pointerdown", (e) => {
    if (!open || busy || (e.pointerType === "mouse" && e.button !== 0)) return;
    pid = e.pointerId; x0 = e.clientX; y0 = e.clientY; dx = 0; dragging = false; hist = [[e.timeStamp, 0]];
  });
  drag.addEventListener("pointermove", (e) => {
    if (e.pointerId !== pid) return;
    const ddx = e.clientX - x0, ddy = e.clientY - y0;
    if (!dragging) {
      if (Math.abs(ddx) < 8 || Math.abs(ddx) < Math.abs(ddy)) { if (Math.abs(ddy) > 12) pid = null; return; }
      dragging = true;
      drag.setPointerCapture(pid);
      drag.classList.add("held");
    }
    dx = ddx;
    hist.push([e.timeStamp, dx]);
    if (hist.length > 6) hist.shift();
    drag.style.transform = `translateX(${dx}px) rotate(${dx / 16}deg)`;
    stamps.yes.style.opacity = Math.max(0, Math.min(1, dx / 90));
    stamps.no.style.opacity = Math.max(0, Math.min(1, -dx / 90));
  });
  const release = (e) => {
    if (e.pointerId !== pid) return;
    pid = null;
    if (!dragging) return;
    dragging = false;
    const [t1, x1] = hist[0], [t2, x2] = hist[hist.length - 1];
    const v = (x2 - x1) / Math.max(1, t2 - t1); // px/мс
    const w = flash.offsetWidth || 360;
    if (Math.abs(dx) > w * 0.32 || (Math.abs(v) > 0.55 && Math.sign(v) === Math.sign(dx))) return fly(dx > 0);
    drag.classList.remove("held");
    drag.style.transform = "";
    stamps.yes.style.opacity = 0; stamps.no.style.opacity = 0;
  };
  drag.addEventListener("pointerup", release);
  drag.addEventListener("pointercancel", release);
}
function recallResult(S) {
  clearRun();
  const n = S.qs.length;
  const p = n ? S.known / n : 0;
  if (S.cumul) {
    // UNIFIX1: тест тижня / «через місяць» - результат і окремо «памʼятаю надовго»
    const k = dayKey();
    if (S.cumul === "month") STORE.m = Date.now();
    const log = STORE.c || (STORE.c = []);
    log.push({ d: k, k: S.cumul, ok: S.known, n });
    while (log.length > 20) log.shift();
    save(STORE);
    const coll = UNITS.filter((u) => u.kind === "colloquium");
    app.innerHTML = `<a class="back" href="#/">${icon("left")}На головну</a><h1>${esc(S.u.title)}: результат</h1>
      <div class="card result">${ring(p, 150, 12, `<b class="score"><span id="cnt">${S.known}</span><small>знав з ${n}</small></b>`, "big")}
      <div class="pts">${Math.round(p * 100)} % памʼятаєш через добу і більше</div>${streakLine()}
      <p class="muted">Те, що не згадав, - у «Лише помилки» свого розділу. Так і тренується довга памʼять.</p>
      ${coll.map((u) => memLine(u.id) ? `<p>${esc(u.title)}: ${memLine(u.id)}</p>` : "").join("")}</div>`;
    countUp($("#cnt"), S.known);
    animateRings();
    if (n) setTimeout(celebrate, 200);
    focusMain();
    return;
  }
  app.innerHTML = `<a class="back" href="#/u/${S.u.id}/test">${icon("left")}До тестів</a><h1>Картки: результат</h1>
    <div class="card result">${ring(p, 150, 12, `<b class="score"><span id="cnt">${S.known}</span><small>знав з ${n}</small></b>`, "big")}
    <div class="pts">${Math.round(p * 100)} % згадав сам</div>${streakLine()}
    ${memLine(S.u.id) ? `<p>${memLine(S.u.id)}</p>` : ""}
    <div class="btn-row" style="width:100%"><a class="btn primary" href="#/q/${S.u.id}/recall" id="again">${icon("redo")}Ще ${RECALL_N}</a><a class="btn" href="#/q/${S.u.id}/wrong">Лише помилки</a></div></div>`;
  $("#again").addEventListener("click", (e) => { e.preventDefault(); quiz(S.u.id, "recall", true); });
  countUp($("#cnt"), S.known);
  animateRings();
  if (n) setTimeout(celebrate, 200);
  focusMain();
}
function streakLine() {
  const st = streak();
  return st ? `<div class="streak on lit">${icon("flame")}<span class="num">${st}</span> ${daysWord(st)} поспіль</div>` : "";
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
// число без хвоста з 16 цифр: 1,4142135623730951 -> 1,41421
function fmtNum(x) {
  if (typeof x !== "number" || !isFinite(x)) return String(x);
  if (Number.isInteger(x)) return String(x);
  return String(Number(x.toPrecision(6))).replace(".", ",");
}
function answerText(q) {
  if (q.type === "gen") return q.a || "";
  if (q.type === "single") return q.options[q.answer];
  if (q.type === "multi") return q.answer.map((i) => q.options[i]).join("; ");
  if (q.type === "number") return q.answerText ? String(q.answerText).replace(".", ",") : fmtNum(q.answer);
  return q.answer;
}

const LET = "АБВГДЕЄЖЗИ";
function renderQ(S) {
  const q = S.qs[S.i];
  const a = S.ans[S.i];
  const answered = a != null && a.locked;
  const show = answered && !S.real;
  const fx = S.fx && motion();
  S.fx = false;
  const head = `${progressBar(S, show)}<div class="qhead"><a href="#/u/${S.u.id}/test" id="exit">${icon("x")}Вийти</a>
    <span class="num">${S.i + 1} / ${S.qs.length}</span>
    ${S.end ? `<span class="timer" id="timer" role="timer" aria-label="Залишилось часу"></span>` : `<span>${{ wrong: "помилки", recall: "пригадування", topics: "теми" }[S.mode] || "тренування"}</span>`}</div>`;
  let body = `<div class="card q${S.enter && motion() ? " qin" : ""}${fx ? " fx" : ""}"><div class="topic">${esc(q.topic)}</div><p>${rich(q.q)}</p>${q.pre ? `<pre>${esc(q.pre)}</pre>` : ""}`;
  S.enter = false;
  let ok = false;
  if (show) ok = isRight(q, a.v);
  if (q.type === "single" || q.type === "multi") {
    body += `<div class="opts" role="${q.type === "single" ? "radiogroup" : "group"}">` + q._order.map((oi, k) => {
      const sel = a && (q.type === "single" ? a.v === oi : (a.v || []).includes(oi));
      let cls = "opt" + (q.type === "multi" ? " multi" : "");
      if (show) {
        const correct = q.type === "single" ? oi === q.answer : q.answer.includes(oi);
        if (correct) cls += " right"; else if (sel) cls += " wrong";
      }
      return `<button type="button" class="${cls}" data-o="${oi}" aria-pressed="${sel ? "true" : "false"}"${show ? " disabled" : ""}><span class="mk" aria-hidden="true">${LET[k] || k + 1}</span><span>${rich(q.options[oi])}</span></button>`;
    }).join("") + `</div>`;
    if (q.type === "multi" && !show) body += `<p class="muted">Кілька правильних варіантів.</p>`;
  } else {
    const val = a ? esc(a.v) : "";
    body += `<form class="inp${show ? (ok ? " right" : " wrong") : ""}" id="inpf"><label class="sr" for="inp">Відповідь</label><input id="inp" autocomplete="off" ${q.type === "number" ? 'inputmode="decimal"' : ""} value="${val}" placeholder="${q.type === "number" ? "число, напр. 2,5 або 5/2" : "відповідь"}"${show ? " disabled" : ""}></form>`;
  }
  if (show) {
    body += `<div class="verdict ${ok ? "ok" : "bad"}">${icon(ok ? "check" : "x")}${ok ? "Правильно" : "Неправильно"}</div>
      <div class="feedback">${ok ? "" : `<div>Правильна відповідь: <strong>${rich(answerText(q))}</strong></div>${videoHint(S, q)}`}
      <div class="exp">${rich(q.explain || "")}${q.explainPre ? `<pre>${esc(q.explainPre)}</pre>` : ""}${q.src ? `<div class="src">Джерело: ${esc(q.src)}</div>` : ""}</div></div>`;
  }
  body += `</div>`;
  const last = S.i === S.qs.length - 1;
  let nav = `<div class="qnav">`;
  if (S.real) {
    if (S.i > 0) nav += `<button class="btn" type="button" id="prev">${icon("left")}Назад</button>`;
    nav += last ? `<button class="btn subject" type="button" id="fin">${icon("check")}Завершити</button>` : `<button class="btn subject" type="button" id="next">Далі${icon("right")}</button>`;
  } else if (!answered) {
    nav += `<button class="btn subject" type="button" id="check">Перевірити</button>`;
  } else {
    nav += last ? `<button class="btn subject" type="button" id="fin">Результат</button>` : `<button class="btn subject" type="button" id="next">Далі${icon("right")}</button>`;
  }
  nav += `</div>`;
  app.innerHTML = head + body + nav;
  settleProgress();
  if (S.end) tick(S);
  $("#exit").addEventListener("click", clearRun);

  app.querySelectorAll(".opt").forEach((b) => b.addEventListener("click", () => {
    const oi = +b.dataset.o;
    let cur = S.ans[S.i] || { v: q.type === "multi" ? [] : null };
    if (q.type === "single") cur.v = oi;
    else cur.v = cur.v.includes(oi) ? cur.v.filter((x) => x !== oi) : [...cur.v, oi];
    S.ans[S.i] = cur;
    saveRun(S);
    if (q.type === "single" && !S.real) return lockAnswer(S);
    renderQ(S);
  }));
  const inp = $("#inp");
  if (inp) {
    inp.addEventListener("input", () => { S.ans[S.i] = { v: inp.value }; saveRun(S); });
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
  record(q._unit, q, isRight(q, a.v), S.mode);
  saveRun(S);
  S.fx = true;
  renderQ(S);
}
function go(S, d) {
  const ni = Math.min(S.qs.length - 1, Math.max(0, S.i + d));
  if (ni === S.i) return;
  S.i = ni; S.enter = true;
  saveRun(S);
  renderQ(S);
  focusMain();
}

function finish(S, timeUp) {
  if (S.done) return;
  S.done = true;
  clearInterval(timerId);
  clearRun();
  let right = 0;
  const items = S.qs.map((q, i) => {
    const a = S.ans[i];
    const ok = a ? isRight(q, a.v) : false;
    if (S.real) record(q._unit, q, ok, S.mode);
    else if (a && !a.locked) record(q._unit, q, ok, S.mode);
    if (ok) right++;
    let given = "-";
    if (a && a.v != null) {
      if (q.type === "single") given = q.options[a.v];
      else if (q.type === "multi") given = a.v.map((x) => q.options[x]).join("; ") || "-";
      else given = a.v;
    }
    return `<div class="res-item ${ok ? "ok" : "bad"}"><span class="mark" aria-hidden="true">${icon(ok ? "check" : "x")}</span><div class="muted">${i + 1}. ${esc(q.topic)}</div>
      <p>${rich(q.q)}</p>${q.pre ? `<pre>${esc(q.pre)}</pre>` : ""}
      <div>Твоя відповідь: ${rich(given)} <span class="sr">${ok ? "правильно" : "неправильно"}</span></div>
      ${ok ? "" : `<div>Правильно: <strong>${rich(answerText(q))}</strong></div>${videoHint(S, q)}`}
      <div class="exp">${rich(q.explain || "")}${q.explainPre ? `<pre>${esc(q.explainPre)}</pre>` : ""}${q.src ? `<div class="src">Джерело: ${esc(q.src)}</div>` : ""}</div></div>`;
  }).join("");
  const n = S.qs.length;
  const pct = Math.round((100 * right) / n);
  const pts = S.u.test && S.u.test.points ? `≈ ${(S.u.test.points * right / n).toFixed(1).replace(".", ",")} з ${S.u.test.points} балів` : "";
  app.innerHTML = `<a class="back" href="#/u/${S.u.id}/test">${icon("left")}До тестів</a>
    <h1>${timeUp ? "Час вийшов. " : ""}Результат</h1>
    <div class="card result">${ring(right / n, 150, 12, `<b class="score"><span id="cnt">${right}</span> / ${n}<small>${pct} %</small></b>`, "big")}
    ${pts ? `<div class="pts">${pts}</div>` : ""}${streakLine()}
    <div class="btn-row" style="width:100%"><a class="btn subject" href="#/q/${S.u.id}/${S.mode}" id="again">${icon("redo")}Ще раз</a><a class="btn" href="#/q/${S.u.id}/wrong">Лише помилки</a></div></div>
    <div class="stagger">${items}</div>`;
  $("#again").addEventListener("click", (e) => { e.preventDefault(); quiz(S.u.id, S.mode, true); });
  countUp($("#cnt"), right);
  stagger(); animateRings();
  if (right > 0) setTimeout(celebrate, 200);
  focusMain();
}

async function statsPage() {
  setTitle("Слабкі теми");
  delete app.dataset.s;
  const rows = UNITS.map((u) => {
    const s = unitStats(u.id);
    const list = Object.entries(s.topics).map(([t, v]) => ({ t, p: v.r / (v.r + v.w), n: v.r + v.w }))
      .sort((a, b) => a.p - b.p);
    if (!list.length) return "";
    const p = (s.r) / (s.r + s.w);
    return `<div class="card" data-s="${sk(u.id)}"><div class="uhead"><div><h3 style="margin:2px 0 4px">${esc(u.title)}</h3>
      <p class="muted">Відповідей ${s.r + s.w}, правильно ${Math.round(100 * p)} %, зараз у помилках ${s.wrongNow}</p>${memLine(u.id) ? `<p class="muted">${memLine(u.id)}</p>` : ""}</div>${ring(p, 52, 6, `<b>${Math.round(p * 100)}%</b>`)}</div>
      <ul class="topics">${list.map((x) => `<li><span>${esc(x.t)}</span><span class="chip">${Math.round(x.p * 100)} % з ${x.n}</span></li>`).join("")}</ul>
      <a class="btn subject" href="#/q/${u.id}/wrong">${icon("redo")}Перерозвʼязати помилки</a></div>`;
  }).join("");
  const st = streak();
  app.innerHTML = `<a class="back" href="#/">${icon("left")}На головну</a><h1>Мої слабкі теми</h1>
    <p class="muted">Статистика зберігається лише на цьому пристрої. «Памʼятаю надовго» - остання відповідь правильна і дана через добу або більше після попередньої; «знаю сьогодні» - правильно, але ще не перевірено через добу.</p>
    ${(STORE.c || []).length ? `<div class="card"><h3 style="margin-top:2px">Тести тижня і місяця</h3><ul class="topics">${STORE.c.slice(-6).reverse().map((c) => `<li><span>${esc(c.d.split("-").reverse().slice(0, 2).join("."))} ${c.k === "month" ? "через місяць" : "тиждень"}</span><span class="chip">${c.ok} з ${c.n}</span></li>`).join("")}</ul></div>` : ""}
    ${st ? `<p>${streakLine()}</p>` : ""}
    <div class="stagger">${rows || "<div class='card'><p>Ще нема відповідей. Пройди будь-який тест.</p></div>"}</div>
    <button class="btn" type="button" id="reset">Скинути статистику</button>`;
  stagger(); animateRings();
  $("#reset").addEventListener("click", () => {
    if (!confirm("Скинути всю статистику на цьому пристрої?")) return;
    STORE = { q: {}, d: {} }; save(STORE); statsPage();
  });
}

// ---------- UPLAN1: графік навчання і відео-уроки ----------
// Стан «зроблено» веде бот UniNagad (один стан). Сайт бере його з посилання бота #/grafik/<код>,
// а галочка тут відкриває бота (t.me/<бот>?start=g_<id>), щоб записав він; до відповіді - позначка «чекає бота».
const GKEY = "uniprep:grafik";
const GTRACK = { lab: "Лаби в терміналі Mint", mint: "Linux Mint", git: "Git і GitHub", "an-k1": "Колоквіум 1, аналітична",
  "ma-k2": "Колоквіум 2, матан", zfp: "ЗФП молекулярна", hist: "Історія", eng: "Англійська" };
const GORDER = ["an-k1", "ma-k2", "zfp", "hist", "eng", "lab", "mint", "git"];
const WDL = ["пн", "вт", "ср", "чт", "пт", "сб", "нд"];
function gLoad() { try { return JSON.parse(localStorage.getItem(GKEY)) || {}; } catch (e) { return {}; } }
function gSave(g) { try { localStorage.setItem(GKEY, JSON.stringify(g)); } catch (e) { /* приватне вікно */ } }
function todayIso() { const d = new Date(); return `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, "0")}-${String(d.getDate()).padStart(2, "0")}`; }
const dm = (iso) => `${iso.slice(8, 10)}.${iso.slice(5, 7)}`;
function gState(p) {
  const g = gLoad();
  const dec = g.code ? GRAFIK.decode(p, g.code) : { done: new Set(), res: new Set(), version: "" };
  const local = g.local || {};
  for (const id of Object.keys(local)) if (dec.done.has(id)) delete local[id]; // бот уже записав
  const done = new Set([...dec.done, ...Object.keys(local)]);
  return { g, done, res: dec.res, botDone: dec.done, local, stale: !!(g.code && dec.version && dec.version !== p.version) };
}
function ytUrl(v) { return `https://www.youtube.com/watch?v=${v.id}${v.start ? "&t=" + v.start + "s" : ""}`; }
function vMin(v) { return Math.max(1, Math.ceil((v.watch_s || 60) / 60)); }
function gItem(p, id, S, kind) {
  const u = p.units[id];
  const isDone = S.done.has(id);
  const wait = isDone && !S.botDone.has(id);
  const pre = kind === "held" ? (u.after || []).filter((a) => p.units[a] && !S.done.has(a)).map((a) => esc(p.units[a].short)).join(", ") : "";
  const meta = [kind === "debt" ? `<b class="gdebt">борг з ${dm(u.day)}</b>` : "", pre ? `<span class="muted">спершу: ${pre}</span>` : "", esc(u.time), `${u.min} хв`, `пріоритет ${u.prio}`,
    u.hard ? `<b class="gred">дедлайн ${dm(u.hard)}</b>` : ""].filter(Boolean).join(" · ");
  return `<li class="gi${u.hard ? " hard" : ""}${isDone ? " done" : ""}">
    <button class="gchk" type="button" data-g="${id}" aria-pressed="${isDone}" aria-label="${isDone ? "Зроблено" : "Позначити зроблене"}: ${esc(u.short)}">${isDone ? icon("check") : ""}</button>
    <div class="gbody"><div class="gmeta">${meta}${wait ? ' · <span class="muted">чекає бота</span>' : ""}</div>
    <a class="gtitle" href="#/video/${id}">${esc(u.title)}</a>
    <div class="gsteps muted">${u.video ? `${icon("play")}відео ≈${vMin(u.video)} хв` : "без відео"} → повтори → зроби сам → перевір себе</div></div></li>`;
}
function gBind(p, rerender) {
  app.querySelectorAll(".gchk").forEach((b) => b.addEventListener("click", () => {
    const id = b.dataset.g;
    const S = gState(p);
    if (S.botDone.has(id)) { alert("Записано в боті. Зняти позначку - напиши боту: «не зроблено " + id + "»."); return; }
    const g = S.g;
    g.local = g.local || {};
    if (g.local[id]) { delete g.local[id]; gSave(g); rerender(); return; }
    g.local[id] = Date.now();
    gSave(g);
    rerender();
    window.open(`https://t.me/${p.bot}?start=g_${encodeURIComponent(id)}`, "_blank", "noopener"); // бот запише сам
  }));
}
async function grafikPage(codeArg) {
  setTitle("Графік");
  delete app.dataset.s;
  const p = await getJSON("data/grafik.json");
  if (codeArg) { // посилання з бота: зберегти стан і прибрати код з адреси
    const g = gLoad();
    g.code = codeArg; g.at = Date.now();
    gSave(g);
    history.replaceState(null, "", "#/grafik");
  }
  const draw = () => {
    const S = gState(p);
    const today = todayIso();
    const v = GRAFIK.view(p, S.done, S.res, today, 7);
    const day0 = v.days[0];
    // позначене сьогодні (борг чи пункт іншого дня) не зникає зі «Сьогодні», а стоїть зробленим - «чекає бота»
    for (const id of Object.keys(S.local)) if (p.units[id] && !day0.items.includes(id) && !day0.done.includes(id)) day0.done.push(id);
    const dayCard = (d, i) => {
      const wd = WDL[GRAFIK.pyWd(d.day)];
      const ev = d.events.map((e) => `<li class="gev${e.hard ? " hard" : ""}">${e.hard ? '<b class="gred">дедлайн</b> · ' : ""}${esc(e.time || "")} ${esc(e.title)}</li>`).join("");
      const rows = d.debts.map((id) => gItem(p, id, S, "debt")).join("") + d.items.map((id) => gItem(p, id, S, "item")).join("") + (d.held || []).map((id) => gItem(p, id, S, "held")).join("") +
        d.done.map((id) => gItem(p, id, S, "done")).join("");
      const empty = !rows ? `<li class="muted">${GRAFIK.pyWd(d.day) === 0 ? "Лише картки (4 пари + ЛР - день легкий)." : "Лише картки в боті (10-15 хв)."}</li>` : "";
      return `<section class="card gday${i === 0 ? " today" : ""}"><h2>${i === 0 ? "Сьогодні, " : ""}${wd} ${dm(d.day)} <span class="muted">≈ ${d.min} хв</span></h2>
        <ul class="glist">${ev}${rows}${empty}</ul></section>`;
    };
    const lateMsg = v.late.length ? `<p class="gwarn">${icon("clock")}Дедлайн минув: ${v.late.map((i) => esc(p.units[i].short)).join(", ")}. Якщо здав - познач; якщо ні - спитай викладача, чи можна дописати.</p>` : "";
    const waitMsg = v.waiting.length ? `<p class="muted">Ще ${v.waiting.length} боргів чекають своєї черги (по одному на день, у нд - два). Відкласти в резерв - кнопкою в боті.</p>` : "";
    // увесь графік по тижнях
    const weeks = {};
    for (const [k, dd] of Object.entries(p.days)) {
      if (!dd.items.length) continue;
      const wk = GRAFIK.addDays(k, -GRAFIK.pyWd(k));
      (weeks[wk] = weeks[wk] || []).push([k, dd]);
    }
    const all = Object.entries(weeks).map(([wk, ds]) => {
      const n = ds.reduce((s, [, dd]) => s + dd.items.length, 0);
      const nd = ds.reduce((s, [, dd]) => s + dd.items.filter((i) => S.done.has(i)).length, 0);
      return `<details class="later"><summary>${dm(wk)} - ${dm(GRAFIK.addDays(wk, 6))}${wk > p.sem_end ? " · після семестру" : ""} <span class="muted">(${nd} з ${n})</span></summary><ul class="glist">${
        ds.map(([k, dd]) => `<li class="gwday">${WDL[GRAFIK.pyWd(k)]} ${dm(k)}</li>` + dd.items.map((id) => gItem(p, id, S, S.done.has(id) ? "done" : (k < today ? "debt" : "item"))).join("")).join("")}</ul></details>`;
    }).join("");
    const res = [...S.res].filter((i) => p.units[i]);
    const syncInfo = S.g.code ? `Стан з бота: ${new Date(S.g.at).toLocaleString("uk-UA", { day: "2-digit", month: "2-digit", hour: "2-digit", minute: "2-digit" })}.` :
      "Стан ще не підтягнуто: відкрий посилання «Графік і відео-уроки» з ранкового повідомлення бота.";
    const cal = new URL("grafik.ics", location.href).href;
    app.innerHTML = `<h1>Графік навчання</h1>
      <p class="muted">${syncInfo} Галочка відкриває бота - він записує (стан один, у боті). Незроблене саме переходить боргом угорі наступного дня.</p>
      ${S.stale ? `<p class="gwarn">${icon("redo")}У боті новіша версія графіка (змінилась дата чи дедлайн). Точний список дня - у боті («графік»); сайт оновиться з наступним оновленням.</p>` : ""}
      ${lateMsg}
      <div class="links"><a class="btn primary" href="#/video">${icon("video")}Відео-уроки: дивись, повтори, зроби сам</a></div>
      ${v.days.map(dayCard).join("")}
      ${waitMsg}
      ${res.length ? `<details class="later"><summary>Резерв (${res.length}) - відкладене, не загублене</summary><ul class="glist">${res.map((id) => gItem(p, id, S, "item")).join("")}</ul><p class="muted">Повернути - у боті: «резерв».</p></details>` : ""}
      <h2>Увесь графік</h2>${all}
      <section class="card"><h2>${icon("cal")}Графік у календар телефона</h2>
        <p class="muted">Календар оновлюється сам (підписка за посиланням), борги бачить лише бот.</p>
        <ol class="gcal"><li>На телефоні відкрий у браузері calendar.google.com, меню браузера - «Версія для ПК» (у застосунку Календар підписатися за посиланням не можна).</li>
        <li>Ліворуч «Інші календарі» - «+» - «З URL-адреси» - встав посилання нижче - «Додати календар».</li>
        <li>У застосунку Google Календар: Налаштування - «Графік навчання» - увімкни «Синхронізація».</li></ol>
        <p><code class="gurl">${esc(cal)}</code></p>
        <div class="btn-row"><button class="btn" type="button" id="gcopy">${icon("dl")}Скопіювати посилання</button><a class="btn" href="${esc(cal.replace(/^https?:/, "webcal:"))}">${icon("cal")}Інший календар (webcal)</a></div>
      </section>`;
    gBind(p, draw);
    const cp = $("#gcopy");
    if (cp) cp.addEventListener("click", async () => { try { await navigator.clipboard.writeText(cal); cp.textContent = "Скопійовано"; } catch (e) { prompt("Скопіюй:", cal); } });
  };
  draw();
}
async function gVideoPage(id) {
  const p = await getJSON("data/grafik.json");
  delete app.dataset.s;
  const S = gState(p);
  if (id && p.units[id]) {
    const u = p.units[id];
    const v = u.video;
    setTitle(u.short);
    const gl = v && v.glossary && v.glossary.length ? `<details><summary>Словничок (відео англійською)</summary><ul>${v.glossary.map((x) => `<li>${esc(x)}</li>`).join("")}</ul></details>` : "";
    const from = v ? (v.start ? `з ${mmss(v.start)}` : "з початку") + (v.end && !v.watch_cut ? ` до ${mmss(v.end)}` : "") + (v.watch_cut ? `, перші ≈${vMin(v)} хв` : "") : "";
    app.innerHTML = `<a class="back" href="#/video">${icon("left")}Усі відео-уроки</a>
      <h1>${esc(u.title)}</h1>
      <p class="muted">${esc(GTRACK[u.track] || u.track)} · у графіку: ${WDL[GRAFIK.pyWd(u.day)]} ${dm(u.day)}, ${esc(u.time)} · ${u.min} хв${u.hard ? ` · <b class="gred">дедлайн ${dm(u.hard)}</b>` : ""}</p>
      <ol class="vsteps">
        <li><h2>${icon("play")}Дивись</h2>${v ? `<p><a class="btn primary" href="${ytUrl(v)}" target="_blank" rel="noopener">${icon("video")}${esc(v.title)}</a></p>
          <p class="muted">${esc(v.channel || "")} · ${esc(v.duration || "")} · ${from}${v.lang === "en" ? " · англійською" : ""}</p><p>${esc(v.why || "")}</p>${gl}` : "<p>Відео до цього пункту нема.</p>"}</li>
        <li><h2>${icon("redo")}Повтори</h2><p>${esc(u.repeat)}</p></li>
        <li><h2>${icon("pen")}Зроби сам</h2><p>${esc(u.do)}</p>${u.site ? `<p><a class="chiplink" href="${esc(u.site)}">${icon("book")}Відкрити на сайті</a></p>` : ""}</li>
        <li><h2>${icon("target")}Перевір себе</h2><p>${esc(u.check)}</p></li>
      </ol>
      <ul class="glist">${gItem(p, id, S, "item")}</ul>`;
    gBind(p, () => gVideoPage(id));
    return;
  }
  setTitle("Відео-уроки");
  const by = {};
  for (const [uid, u] of Object.entries(p.units)) (by[u.track] = by[u.track] || []).push([uid, u]);
  app.innerHTML = `<a class="back" href="#/grafik">${icon("left")}Графік</a><h1>Відео-уроки</h1>
    <p class="muted">Для кожного уроку, лаби і типу задачі - одне відео (українською, якщо є; англійською - з таймкодом і словничком). Порядок: <b>дивись → повтори → зроби сам → перевір себе</b>. Відео відкриваються з інтернетом.</p>
    ${GORDER.filter((t) => by[t]).map((t) => `<details class="later"${t === "an-k1" ? " open" : ""}><summary>${esc(GTRACK[t])} <span class="muted">(${by[t].length})</span></summary><ul class="vlist">${
      by[t].sort((a, b) => (a[1].day < b[1].day ? -1 : a[1].day > b[1].day ? 1 : a[1].idx - b[1].idx)).map(([uid, u]) => `<li><a href="#/video/${uid}"><span class="vday">${dm(u.day)}</span><span>${esc(u.title)}</span><span class="muted">${u.video ? `${icon("play")}${vMin(u.video)} хв${u.video.lang === "en" ? " · англ." : ""}` : ""}${S.done.has(uid) ? " · ✓" : ""}</span></a></li>`).join("")}</ul></details>`).join("")}`;
}

function notFound() { delete app.dataset.s; app.innerHTML = `<p>Сторінки нема. <a href="#/">На головну</a></p>`; }

const SKEL = `<div class="sk" aria-hidden="true"><i class="h"></i><i></i><i style="width:80%"></i><i class="b"></i><i class="b"></i></div>`;
async function route() {
  clearInterval(timerId);
  const h = decodeURIComponent(location.hash.replace(/^#\/?/, "")).split("/");
  markNav(h[0]);
  const skT = setTimeout(() => { app.innerHTML = SKEL; }, 160);
  try {
    if (!UNITS.length) UNITS = await getJSON("data/units.json");
    if (!h[0]) await home();
    else if (h[0] === "u") await unitPage(h[1], h[2]);
    else if (h[0] === "q") await quiz(h[1], h[2] || "train");
    else if (h[0] === "subjects") await subjects();
    else if (h[0] === "plan") await staticPage("plan", "План підготовки");
    else if (h[0] === "glossary") await staticPage("glossary", "Словник EN-UA");
    else if (h[0] === "about") await staticPage("about", "Як користуватись");
    else if (h[0] === "stats") await statsPage();
    else if (h[0] === "grafik") await grafikPage(h[1]);
    else if (h[0] === "video") await gVideoPage(h[1]);
    else if (h[0] === "w") await cumulTest(h[1]);
    else notFound();
  } catch (e) {
    app.innerHTML = `<p>Помилка завантаження (${esc(e.message)}). Якщо ти офлайн, а сайт ще не відкривався з інтернетом, - відкрий раз онлайн.</p>`;
  }
  clearTimeout(skT);
  app.dataset.route = location.hash; // маркер «екран готовий» (для тестів)
  if (h[0] !== "q") focusMain();
}
// переходи між екранами: View Transitions (плавна зміна), без них - просто рендер
function navigate() {
  if (document.startViewTransition && motion() && document.visibilityState === "visible") {
    document.startViewTransition(() => route());
  } else route();
}
window.addEventListener("hashchange", navigate);
showNet();
route();
