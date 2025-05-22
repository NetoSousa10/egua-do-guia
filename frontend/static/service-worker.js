const CACHE_NAME = 'egua-do-guia-v1';
const SHELL_ASSETS = [
  '/',
  '/manifest.json',
  '/static/css/style.css',
  '/static/js/home.js',
  '/static/js/locais.js',
  '/static/assets/img/logo.png'
];

// Instalando e pré-cacheando o shell, mas ignorando URLs que falhem
self.addEventListener('install', event => {
  event.waitUntil((async () => {
    const cache = await caches.open(CACHE_NAME);
    for (const url of SHELL_ASSETS) {
      try {
        await cache.add(url);
      } catch (err) {
        console.warn(`Falha ao cachear ${url}:`, err);
      }
    }
    // Força o SW a ativar imediatamente
    await self.skipWaiting();
  })());
});

// Ativando e limpando caches antigos
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

// Interceptando requisições
self.addEventListener('fetch', event => {
  const url = event.request.url;

  // Runtime cache para API, imagens e vídeos
  if (url.includes('/static/assets/img/') ||
      url.includes('/static/video/') ||
      url.includes('/api/')) {
    event.respondWith((async () => {
      const cache = await caches.open(CACHE_NAME);
      const cached = await cache.match(event.request);
      if (cached) return cached;
      try {
        const networkRes = await fetch(event.request);
        // Só cacheia se status OK
        if (networkRes.ok) {
          cache.put(event.request, networkRes.clone());
        }
        return networkRes;
      } catch (err) {
        // Se der erro de rede, retornamos o cache (mesmo que vazio)
        return cached || Response.error();
      }
    })());
    return;
  }

  // Para todo o resto (shell): cache primeiro, depois rede
  event.respondWith((async () => {
    const cache = await caches.open(CACHE_NAME);
    const cached = await cache.match(event.request);
    return cached || fetch(event.request);
  })());
});

// Permite o skipWaiting via postMessage
self.addEventListener('message', event => {
  if (event.data && event.data.type === 'SKIP_WAITING') {
    self.skipWaiting();
  }
});
