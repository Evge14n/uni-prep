// Офлайн: при першому відкритті кешує весь сайт (тексти, тести, картинки).
// Версія міняється при кожній збірці, старий кеш видаляється.
const VERSION = "220ecc149482";
const CACHE = "uniprep-" + VERSION;
const FILES = ["./", "index.html", "app.js", "pyrun.js", "py-worker.js", "style.css", "manifest.webmanifest", "icons/icon-192.png", "icons/icon-512.png", "icons/maskable-512.png", "icons/favicon.svg", "fonts/dvmono-400.woff2", "fonts/fira-400.woff2", "fonts/fira-400i.woff2", "fonts/fira-600.woff2", "fonts/fira-700.woff2", "fonts/literata-600.woff2", "fonts/unimath-400.woff2", "data/an-k1/teoriya.html", "data/an-k1/oznachennya.html", "data/an-k1/zadachi.html", "data/an-k1/shpargalka.html", "data/an-k1/quiz.json", "data/an-k1/gen.json", "data/an-k1/videos.json", "data/ma-k2/teoriya.html", "data/ma-k2/oznachennya.html", "data/ma-k2/zadachi.html", "data/ma-k2/shpargalka.html", "data/ma-k2/quiz.json", "data/ma-k2/gen.json", "data/ma-k2/videos.json", "data/ma/teoriya.html", "data/ma/oznachennya.html", "data/ma/zadachi.html", "data/ma/shpargalka.html", "data/ma/quiz.json", "data/ma/videos.json", "data/an/teoriya.html", "data/an/oznachennya.html", "data/an/zadachi.html", "data/an/shpargalka.html", "data/an/quiz.json", "data/an/videos.json", "data/mech/teoriya.html", "data/mech/oznachennya.html", "data/mech/zadachi.html", "data/mech/shpargalka.html", "data/mech/quiz.json", "data/mech/videos.json", "data/mol/teoriya.html", "data/mol/oznachennya.html", "data/mol/zadachi.html", "data/mol/shpargalka.html", "data/mol/quiz.json", "data/mol/videos.json", "data/prog/uroky.html", "data/prog/teoriya.html", "data/prog/oznachennya.html", "data/prog/zadachi.html", "data/prog/shpargalka.html", "data/prog/dovidnyk.html", "data/prog/urok-01.html", "data/prog/urok-02.html", "data/prog/urok-03.html", "data/prog/urok-04.html", "data/prog/urok-05.html", "data/prog/urok-06.html", "data/prog/urok-07.html", "data/prog/urok-08.html", "data/prog/urok-09.html", "data/prog/zadachi/urok01.py", "data/prog/zadachi/urok02.py", "data/prog/zadachi/urok03.py", "data/prog/zadachi/urok04.py", "data/prog/zadachi/urok05.py", "data/prog/zadachi/urok06.py", "data/prog/zadachi/urok07.py", "data/prog/zadachi/urok08.py", "data/prog/zadachi/urok09.py", "data/prog/quiz.json", "data/zfp/teoriya.html", "data/zfp/oznachennya.html", "data/zfp/zadachi.html", "data/zfp/shpargalka.html", "data/zfp/quiz.json", "data/hist/teoriya.html", "data/hist/oznachennya.html", "data/hist/zadachi.html", "data/hist/shpargalka.html", "data/hist/quiz.json", "data/eng/teoriya.html", "data/eng/zadachi.html", "data/eng/shpargalka.html", "data/eng/slovnyk.html", "data/eng/quiz.json", "data/linux/teoriya.html", "data/linux/zadachi.html", "data/linux/shpargalka.html", "data/linux/quiz.json", "data/git/teoriya.html", "data/git/zadachi.html", "data/git/shpargalka.html", "data/git/quiz.json", "data/prog-sec/teoriya.html", "data/prog-sec/zadachi.html", "data/prog-sec/shpargalka.html", "data/prog-sec/quiz.json", "data/plan.html", "data/glossary.html", "data/about.html", "kalendar.ics", "data/units.json"];
const PYCACHE = "pyodide-0.29.5"; // той самий, що в pyrun.js

self.addEventListener("install", (e) => {
  e.waitUntil(
    caches.open(CACHE).then((c) => c.addAll(FILES.map((f) => new Request(f, { cache: "reload" }))))
  );
  self.skipWaiting();
});

self.addEventListener("activate", (e) => {
  e.waitUntil(
    caches.keys().then((keys) =>
      Promise.all(keys.filter((k) => k.startsWith("uniprep-") && k !== CACHE).map((k) => caches.delete(k)))
    ).then(() => self.clients.claim())
  );
});

self.addEventListener("fetch", (e) => {
  const url = new URL(e.request.url);
  if (e.request.method !== "GET" || url.origin !== self.location.origin) return; // YouTube - лише онлайн
  // Python у браузері (UNIPROG1): py/ - окремий кеш, який не стирається при новій версії сайту (12 МБ)
  if (url.pathname.includes("/py/")) {
    e.respondWith(caches.open(PYCACHE).then((c) => c.match(e.request, { ignoreSearch: true }).then((hit) =>
      hit || fetch(e.request).then((r) => { if (r.ok) c.put(e.request, r.clone()); return r; }))));
    return;
  }
  e.respondWith(
    caches.match(e.request, { ignoreSearch: true }).then((hit) => {
      if (hit) return hit;
      return fetch(e.request).catch(() =>
        e.request.mode === "navigate" ? caches.match("index.html") : Response.error()
      );
    })
  );
});
