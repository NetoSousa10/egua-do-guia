const CACHE_NAME = 'egua-do-guia-v1';
const SHELL_ASSETS = [
  '/',
  '/manifest.json',
  '/static/css/style.css',
  '/static/js/home.js',
  '/static/js/locais.js',
  '/static/assets/img/logo.png'
];

// Instalando e pré-cacheando o shell com redirect: 'follow'
self.addEventListener('install', event => {
  event.waitUntil((async () => {
    const cache = await caches.open(CACHE_NAME);
    for (const url of SHELL_ASSETS) {
      try {
        // força seguir redirects
        const response = await fetch(url, { redirect: 'follow' });
        if (response.ok) {
          await cache.put(url, response.clone());
        }
      } catch (err) {
        console.warn(`Falha ao cachear ${url}:`, err);
      }
    }
    await self.skipWaiting();
  })());
});

// Ativando e limpando caches antigos
self.addEventListener('activate', event => {
  event.waitUntil((async () => {
    const keys = await caches.keys();
    await Promise.all(
      keys.filter(key => key !== CACHE_NAME)
          .map(key => caches.delete(key))
    );
    await self.clients.claim();
  })());
});

// Interceptando requisições
self.addEventListener('fetch', event => {
  const url = event.request.url;

  // Runtime caching para imagens, vídeos e API
  if (url.includes('/static/assets/img/') ||
      url.includes('/static/video/') ||
      url.includes('/api/')) {
    event.respondWith((async () => {
      const cache = await caches.open(CACHE_NAME);
      const cached = await cache.match(event.request);
      if (cached) return cached;
      try {
        const networkRes = await fetch(event.request, { redirect: 'follow' });
        if (networkRes.ok) {
          cache.put(event.request, networkRes.clone());
        }
        return networkRes;
      } catch {
        return cached || Response.error();
      }
    })());
    return;
  }

  // Shell: cache first, depois rede com redirect follow
  event.respondWith((async () => {
    const cache = await caches.open(CACHE_NAME);
    const cached = await cache.match(event.request);
    if (cached) return cached;
    return fetch(event.request, { redirect: 'follow' });
  })());
});
