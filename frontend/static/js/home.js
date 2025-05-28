function initMapApp() {
  // 1) Lê os lugares injetados no HTML
  let points = [];
  const rawEl = document.getElementById('raw-places-data');
  if (rawEl) {
    try {
      points = JSON.parse(rawEl.textContent);
    } catch (e) {
      console.error('Erro parseando raw-places-data:', e);
    }
  }
  if (!points.length) {
    console.warn('Nenhum ponto para exibir no mapa');
    return;
  }

  let userLocation = null;
  let routingControl = null;
  let sidebarOpen = false;

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

  // Geolocalização via Leaflet
  map.locate({ setView: true, maxZoom: 15, enableHighAccuracy: true });
  map.on('locationfound', e => {
    userLocation = e.latlng;
    L.circle(userLocation, { radius: 10, color: '#0075B7' })
      .addTo(map)
      .bindPopup('Você está aqui')
      .openPopup();
  });
  map.on('locationerror', err => {
    console.warn('Erro geolocalização (Leaflet):', err.message);
    alert('Não foi possível obter sua localização.');
  });

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
    document.body.classList.add('sidebar-open');
    sidebarOpen = true;

    document.getElementById('sidebar').dataset.placeId = data.id;
    document.getElementById('sidebar-img').src         = data.img_url;
    document.getElementById('sidebar-img').alt         = data.name;
    document.getElementById('sidebar-title').textContent = data.name;

    // Rating
    const stars = Array.from({length:5}, (_,i) => i < data.rating ? '★' : '☆').join('');
    document.getElementById('sidebar-rating').textContent = stars;

    // Outros campos
    document.getElementById('sidebar-hours').textContent   = data.hours   || '—';
    document.getElementById('sidebar-address').textContent = data.address || '—';
    document.getElementById('sidebar-phone').textContent   = data.phone   || '—';
    document.getElementById('sidebar-price').textContent   = data.price   || '—';

    document.getElementById('sidebar-distance').textContent = 'Calculando distância…';
    routeTo({ lat: data.lat, lng: data.lng });
  }

  function closeSidebar() {
    document.body.classList.remove('sidebar-open');
    sidebarOpen = false;
  }
  window.closeSidebar = closeSidebar;

  // Traça rota e exibe distância
  function routeTo(dest) {
    if (!userLocation) {
      alert('Não foi possível obter sua localização.');
      return;
    }
    if (routingControl) {
      map.removeControl(routingControl);
      routingControl = null;
    }
    routingControl = L.Routing.control({
      waypoints: [ userLocation, L.latLng(dest.lat, dest.lng) ],
      lineOptions: { styles: [{ color: '#0075B7', weight: 5 }] },
      createMarker: () => null,
      fitSelectedRoutes: true,
      show: false
    }).addTo(map);

    routingControl.on('routesfound', e => {
      const km = (e.routes[0].summary.totalDistance / 1000).toFixed(2);
      document.getElementById('sidebar-distance').textContent = `Distância: ${km} km`;
    });
    routingControl.on('routingerror', () => {
      document.getElementById('sidebar-distance').textContent = 'Não foi possível calcular a rota.';
    });
  }

  // Adiciona marcadores
  const allMarkers = [];
  points.forEach(pt => {
    const m = L.marker([pt.lat, pt.lng], { icon: createIcon(pt.category) })
      .on('click', () => sidebarOpen ? closeSidebar() : openSidebar(pt))
      .addTo(map);
    allMarkers.push({ marker: m, category: pt.category });
  });

  map.on('click', () => sidebarOpen && closeSidebar());

  // Botão EXPLORAR
  document.getElementById('explore-link')?.addEventListener('click', () => {
    const placeId = document.getElementById('sidebar').dataset.placeId;
    if (placeId) window.location.href = `/menu/detalhes/${placeId}`;
  });

  // Navegação inferior
  document.querySelectorAll('.bottom-nav .nav-btn').forEach(btn => {
    btn.addEventListener('click', () => {
      document.querySelectorAll('.bottom-nav .nav-btn').forEach(b => b.classList.remove('active'));
      btn.classList.add('active');
      window.location.href = btn.dataset.href;
    });
  });

  // Filtro lateral
  document.querySelectorAll('#category-panel button').forEach(btn => {
    btn.addEventListener('click', () => {
      const cat = btn.dataset.category;
      const wasActive = btn.classList.contains('active');
      document.querySelectorAll('#category-panel button').forEach(b => b.classList.remove('active'));
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

// Inicia quando o DOM estiver pronto
document.addEventListener('DOMContentLoaded', initMapApp);
