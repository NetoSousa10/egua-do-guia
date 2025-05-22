const CACHE_NAME = 'egua-do-guia-v1';
const SHELL_ASSETS = [
  '/',                     // HTML principal
  '/manifest.json',        // Manifest
  '/static/css/style.css', // CSS principal
  '/static/js/home.js',    // JS essencial
  '/static/js/locais.js',  // JS essencial
  '/static/assets/img/logo.png' // Ícone do app
];

// Instalando e pré-cacheando o shell
self.addEventListener('install', event => {
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then(cache => cache.addAll(SHELL_ASSETS))
      .then(() => self.skipWaiting())
  );
});

// Ativando e limpando caches antigos
self.addEventListener('activate', event => {
  event.waitUntil(
    caches.keys().then(keys =>
      Promise.all(
        keys
          .filter(key => key !== CACHE_NAME)
          .map(key => caches.delete(key))
      )
    ).then(() => self.clients.claim())
  );
});

// Interceptando requisições
self.addEventListener('fetch', event => {
  const url = event.request.url;

  // 1) Se for requisição para API ou assets grandes (imagens/vídeo), usar runtime caching
  if (url.includes('/static/assets/img/') ||
      url.includes('/static/video/') ||
      url.includes('/api/')) {
    event.respondWith(
      caches.match(event.request).then(cached => {
        if (cached) return cached;
        return fetch(event.request).then(networkRes => {
          return caches.open(CACHE_NAME).then(cache => {
            cache.put(event.request, networkRes.clone());
            return networkRes;
          });
        });
      })
    );
    return;
  }

  // 2) Para todos os outros, primeiro tentar cache (shell), depois rede
  event.respondWith(
    caches.match(event.request).then(cached => {
      return cached || fetch(event.request);
    })
  );
});
