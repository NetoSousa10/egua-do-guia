// service-worker.js

const CACHE_NAME = 'egua-do-guia-v5';
const SHELL_ASSETS = [
  '/',
  '/manifest.json',
  '/static/css/style.css',
  '/static/js/home.js',
  '/static/js/locais.js',
  '/static/assets/img/logo.png'
];

self.addEventListener('install', event => {
  event.waitUntil((async () => {
    const cache = await caches.open(CACHE_NAME);
    await Promise.all(
      SHELL_ASSETS.map(url =>
        cache.add(url).catch(err =>
          console.warn(`Falha ao cachear ${url}:`, err)
        )
      )
    );
    await self.skipWaiting();
  })());
});

self.addEventListener('activate', event => {
  event.waitUntil((async () => {
    const keys = await caches.keys();
    await Promise.all(
      keys
        .filter(key => key !== CACHE_NAME)
        .map(key => caches.delete(key))
    );
    await self.clients.claim();
  })());
});

self.addEventListener('fetch', event => {
  const req = event.request;
  const url = new URL(req.url);

  // 1) Network-first para API — sempre tenta a rede antes do cache
  if (url.pathname.startsWith('/api/')) {
    event.respondWith((async () => {
      const cache = await caches.open(CACHE_NAME);
      try {
        const response = await fetch(req);
        if (response.ok) {
          cache.put(req, response.clone());
        }
        return response;
      } catch (err) {
        const cached = await cache.match(req);
        return cached || new Response(null, { status: 504, statusText: 'Gateway Timeout' });
      }
    })());
    return;
  }

  // 2) Cache-first apenas para o shell (CSS, JS, manifesto, logo)
  event.respondWith((async () => {
    const cache = await caches.open(CACHE_NAME);
    const cached = await cache.match(req);
    return cached || fetch(req);
  })());
});
