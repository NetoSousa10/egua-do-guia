// static/js/home.js

function initMapApp() {
  const points = window.PLACES;
  if (!points) {
    console.error('❌ window.PLACES ainda não está definido');
    return;
  }

  let userLocation   = null;
  let routingControl = null;
  let sidebarOpen    = false;

  const ICON_MAP = {
    hotel:      '/static/icons/hotel.svg',
    restaurant: '/static/icons/restaurant.svg',
    praca:      '/static/icons/praca.svg',
    cultura:    '/static/icons/cultura.svg',
    loja:       '/static/icons/loja.svg',
    mall:       '/static/icons/mall.svg',
  };

  // Inicializa o mapa
  const map = L.map('map').setView([-1.4550, -48.4900], 13);
  L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '&copy; OpenStreetMap contributors'
  }).addTo(map);

  // Obtém localização do usuário
  if (navigator.geolocation) {
    navigator.geolocation.getCurrentPosition(
      pos => {
        userLocation = L.latLng(pos.coords.latitude, pos.coords.longitude);
        map.setView(userLocation, 15);
        L.circle(userLocation, { radius: 10, color: '#0075B7' })
          .addTo(map)
          .bindPopup('Você está aqui')
          .openPopup();
      },
      err => console.warn('Erro geolocalização:', err),
      { enableHighAccuracy: true, timeout: 10000, maximumAge: 0 }
    );
  }

  // Cria ícone customizado
  function createIcon(cat) {
    return L.icon({
      iconUrl:    ICON_MAP[cat] || ICON_MAP.hotel,
      iconSize:   [56, 56],
      iconAnchor: [28, 56],
      popupAnchor:[0, -48],
      className:  'custom-marker-icon'
    });
  }

  // Abre sidebar com os dados do ponto
  function openSidebar(data) {
    console.log('openSidebar:', data);
    document.body.classList.add('sidebar-open');
    sidebarOpen = true;

    document.getElementById('sidebar-title').textContent   = data.title;
    document.getElementById('sidebar-img').src             = data.imgUrl;
    document.getElementById('sidebar-img').alt             = data.title;

    let stars = '';
    for (let i = 1; i <= 5; i++) {
      stars += (i <= data.rating ? '★' : '☆');
    }
    document.getElementById('sidebar-rating').textContent  = stars;
    document.getElementById('sidebar-hours').textContent   = data.hours;
    document.getElementById('sidebar-address').textContent = data.address;
    document.getElementById('sidebar-phone').textContent   = data.phone  || '';
    document.getElementById('sidebar-price').textContent   = data.price;

    // Define texto inicial para distância
    const distEl = document.getElementById('sidebar-distance');
    if (distEl) {
      distEl.textContent = 'Calculando distância…';
    }

    // Traça rota e exibe distância
    routeTo({ lat: data.lat, lng: data.lng });
  }

  function closeSidebar() {
    document.body.classList.remove('sidebar-open');
    sidebarOpen = false;
  }
  window.closeSidebar = closeSidebar;

  // Traça rota e captura distância pela rota
  function routeTo(dest) {
    console.log('routeTo para:', dest);

    if (!userLocation) {
      console.warn('userLocation não definida ainda');
      alert('Não foi possível obter sua localização.');
      return;
    }
    console.log('userLocation:', userLocation);

    if (routingControl) {
      map.removeControl(routingControl);
      routingControl = null;
    }

    routingControl = L.Routing.control({
      waypoints: [
        userLocation,
        L.latLng(dest.lat, dest.lng)
      ],
      lineOptions: { styles: [{ color: '#0075B7', weight: 5 }] },
      createMarker: () => null,
      fitSelectedRoutes: true,
      show: false
    })
    .addTo(map);

    // Quando a rota é encontrada, atualiza distância
    routingControl.on('routesfound', e => {
      const summary = e.routes[0].summary;
      const d = summary.totalDistance;             // em metros
      const km = (d / 1000).toFixed(2);            // em km

      console.log(`Distância: ${d.toFixed(0)} m (${km} km)`);

      const distEl = document.getElementById('sidebar-distance');
      if (distEl) {
        distEl.textContent = `Distância: ${km} km`;
      }
    });

    routingControl.on('routingerror', err => {
      console.error('Erro no roteamento:', err);
      const distEl = document.getElementById('sidebar-distance');
      if (distEl) {
        distEl.textContent = 'Não foi possível calcular a rota.';
      }
    });
  }

  // Adiciona os marcadores no mapa
  const allMarkers = [];
  points.forEach(pt => {
    const m = L.marker([pt.lat, pt.lng], { icon: createIcon(pt.category) })
      .on('click', () => sidebarOpen ? closeSidebar() : openSidebar(pt))
      .addTo(map);
    allMarkers.push({ marker: m, category: pt.category });
  });

  // Fecha sidebar ao clicar no mapa
  map.on('click', () => sidebarOpen && closeSidebar());

  // Navegação inferior
  document.querySelectorAll('.bottom-nav .nav-btn').forEach(btn => {
    btn.addEventListener('click', () => {
      document.querySelectorAll('.bottom-nav .nav-btn')
        .forEach(b => b.classList.remove('active'));
      btn.classList.add('active');
      window.location.href = btn.dataset.href;
    });
  });

  // Filtro lateral por categoria
  document.querySelectorAll('#category-panel button').forEach(btn => {
    btn.addEventListener('click', () => {
      const cat = btn.dataset.category;
      const wasActive = btn.classList.contains('active');
      document.querySelectorAll('#category-panel button')
        .forEach(b => b.classList.remove('active'));
      if (!wasActive) {
        btn.classList.add('active');
        allMarkers.forEach(({ marker, category }) => {
          category === cat ? map.addLayer(marker) : map.removeLayer(marker);
        });
      } else {
        allMarkers.forEach(({ marker }) => map.addLayer(marker));
      }
    });
  });
}

// Inicia quando PLACES estiver pronto
if (window.PLACES) {
  document.addEventListener('DOMContentLoaded', initMapApp);
} else {
  document.addEventListener('placesReady', initMapApp);
}
