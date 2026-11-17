// Офлайн: при першому відкритті кешує весь сайт (тексти, тести, картинки).
// Версія міняється при кожній збірці, старий кеш видаляється.
const VERSION = "__VERSION__";
const CACHE = "uniprep-" + VERSION;
const FILES = __FILES__;
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
