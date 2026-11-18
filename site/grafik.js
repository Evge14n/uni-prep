// UPLAN1 (18.11.2026): борги графіка навчання - той самий алгоритм, що в боті (uni-nagad/grafik.py).
// Чисті функції без DOM: працюють і в браузері (window.GRAFIK), і в Node (тест паритету test_grafik.py).
(function (root) {
  "use strict";
  const DAY = 86400000;
  const toD = (iso) => Date.UTC(+iso.slice(0, 4), +iso.slice(5, 7) - 1, +iso.slice(8, 10));
  const iso = (t) => new Date(t).toISOString().slice(0, 10);
  const addDays = (s, n) => iso(toD(s) + n * DAY);
  const pyWd = (s) => (new Date(toD(s)).getUTCDay() + 6) % 7; // пн = 0, як у Python
  const cmp = (a, b) => {
    for (let i = 0; i < a.length; i++) {
      if (a[i] < b[i]) return -1;
      if (a[i] > b[i]) return 1;
    }
    return 0;
  };
  const has = (s, id) => (s instanceof Set ? s.has(id) : Object.prototype.hasOwnProperty.call(s || {}, id));

  function room(plan, day) { return +plan.debt_room[String(pyWd(day))]; }
  function debtKey(plan, id) {
    const u = plan.units[id];
    return [u.hard ? 0 : 1, u.hard || "", u.prio, u.day, u.idx];
  }
  function overdue(plan, done, res, today) {
    const ids = Object.keys(plan.units).filter((id) => plan.units[id].day < today && !has(done, id) && !has(res, id));
    return ids.sort((a, b) => cmp(debtKey(plan, a), debtKey(plan, b)));
  }
  function view(plan, done, res, today, ndays) {
    ndays = ndays || 7;
    const od = overdue(plan, done, res, today);
    const hard = od.filter((i) => plan.units[i].hard);
    let soft = od.filter((i) => !plan.units[i].hard);
    const late = hard.filter((i) => plan.units[i].hard < today);
    const days = [];
    for (let k = 0; k < ndays; k++) {
      const key = addDays(today, k);
      const n = room(plan, key);
      const debts = (k === 0 ? hard : []).concat(soft.slice(0, n));
      soft = soft.slice(n);
      const dd = plan.days[key] || {};
      const items = (dd.items || []).filter((i) => !has(res, i));
      const undone = items.filter((i) => !has(done, i));
      days.push({ day: key, debts, items: undone, done: items.filter((i) => has(done, i)), events: dd.events || [],
        min: debts.concat(undone).reduce((s, i) => s + plan.units[i].min, 0) });
    }
    return { days, waiting: soft, late };
  }
  function autoReserve(plan, done, res, today) {
    const soft = overdue(plan, done, res, today).filter((i) => !plan.units[i].hard);
    const key = (i) => [plan.units[i].prio, plan.units[i].day, plan.units[i].idx];
    const order = soft.slice().sort((a, b) => cmp(key(b), key(a)));
    const out = [];
    let left = soft.length;
    for (const i of order) {
      if (left <= plan.debt_cap) break;
      if (plan.units[i].prio >= 2) { out.push(i); left--; }
    }
    for (const i of order) {
      if (left <= plan.debt_cap_all) break;
      if (!out.includes(i)) { out.push(i); left--; }
    }
    return out;
  }
  function bits(plan, ids) {
    const n = plan.ids.length;
    const b = new Uint8Array(Math.ceil(n / 8));
    for (const id of ids) {
      const u = plan.units[id];
      if (!u) continue;
      b[u.idx >> 3] |= 1 << (u.idx & 7);
    }
    let s = "";
    for (const x of b) s += String.fromCharCode(x);
    const b64 = typeof btoa === "function" ? btoa(s) : Buffer.from(s, "binary").toString("base64");
    return b64.replace(/\+/g, "-").replace(/\//g, "_").replace(/=+$/, "");
  }
  function unbits(plan, s) {
    const out = new Set();
    if (!s) return out;
    let b64 = s.replace(/-/g, "+").replace(/_/g, "/");
    while (b64.length % 4) b64 += "=";
    let bin;
    try { bin = typeof atob === "function" ? atob(b64) : Buffer.from(b64, "base64").toString("binary"); } catch (e) { return out; }
    const byIdx = {};
    for (const [id, u] of Object.entries(plan.units)) byIdx[u.idx] = id;
    for (let i = 0; i < bin.length * 8; i++) {
      if ((bin.charCodeAt(i >> 3) >> (i & 7)) & 1 && byIdx[i] !== undefined) out.add(byIdx[i]);
    }
    return out;
  }
  function code(plan, done, res) {
    const ids = (s) => (s instanceof Set ? [...s] : Object.keys(s || {}));
    return `${bits(plan, ids(done))}.${bits(plan, ids(res))}.${plan.version}`;
  }
  function decode(plan, s) {
    const [a, b, v] = (String(s || "") + "..").split(".");
    return { done: unbits(plan, a), res: unbits(plan, b), version: v || "" };
  }
  const api = { view, overdue, autoReserve, code, decode, addDays, pyWd };
  if (typeof module !== "undefined" && module.exports) module.exports = api;
  else root.GRAFIK = api;
})(typeof window !== "undefined" ? window : this);
