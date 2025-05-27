// static/js/home.js

// Atacha listeners para iniciar o mapa assim que tivermos o DOM e os dados de places
console.log('Attach listeners for initMapApp');
document.addEventListener('DOMContentLoaded', () => {
  if (window.PLACES) {
    initMapApp();
  }
});
// Caso places.js carregue *depois* do DOM
document.addEventListener('placesReady', initMapApp);

function initMapApp() {
  console.log('initMapApp executado');
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

  // 1) Inicializa o mapa
  const map = L.map('map').setView([-1.4550, -48.4900], 13);
  L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '&copy; OpenStreetMap contributors'
  }).addTo(map);

  // 2) Geolocalização
  if (navigator.geolocation) {
    navigator.geolocation.getCurrentPosition(
      pos => {
        console.log('Geolocalização obtida');
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

  // 3) Cria ícone customizado
  function createIcon(cat) {
    return L.icon({
      iconUrl:    ICON_MAP[cat] || ICON_MAP.hotel,
      iconSize:   [56, 56],
      iconAnchor: [28, 56],
      popupAnchor:[0, -48],
      className:  'custom-marker-icon'
    });
  }

  // 4) Abre a sidebar e preenche dados
  function openSidebar(data) {
    console.log('openSidebar chamado para id', data.id);

    // Clona e reseta o explore-link para remover listeners antigos
    const oldLink = document.getElementById('explore-link');
    if (oldLink) {
      const newLink = oldLink.cloneNode(true);
      oldLink.parentNode.replaceChild(newLink, oldLink);
    }

    // Preenche os campos da sidebar
    document.getElementById('sidebar-title').textContent   = data.title;
    document.getElementById('sidebar-img').src             = data.imgUrl;
    document.getElementById('sidebar-img').alt             = data.title;
    let stars = '';
    for (let i = 1; i <= 5; i++) stars += (i <= data.rating ? '★' : '☆');
    document.getElementById('sidebar-rating').textContent  = stars;
    document.getElementById('sidebar-hours').textContent   = data.hours;
    document.getElementById('sidebar-address').textContent = data.address;
    document.getElementById('sidebar-phone').textContent   = data.phone || '';
    document.getElementById('sidebar-price').textContent   = data.price;

    // Configura o link EXPLORAR
    const exploreLink = document.getElementById('explore-link');
    if (exploreLink) {
      const url = `/menu/detalhes/${data.id}`;
      console.log('Configurando exploreLink para', url);
      exploreLink.href = url;
      exploreLink.addEventListener('click', e => {
        e.preventDefault();
        console.log('Clicou em Explorar, navegando para', url);
        window.location.href = url;
      });
    }

    // Exibe a sidebar
    document.body.classList.add('sidebar-open');
    sidebarOpen = true;

    // Traça rota até o lugar
    routeTo({ lat: data.lat, lng: data.lng });
  }

  // 5) Fecha a sidebar
  function closeSidebar() {
    document.body.classList.remove('sidebar-open');
    sidebarOpen = false;
  }
  window.closeSidebar = closeSidebar;

  // 6) Função de roteamento
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
  }

  // 7) Cria marcadores no mapa
  points.forEach(pt => {
    L.marker([pt.lat, pt.lng], { icon: createIcon(pt.category) })
      .on('click', () => sidebarOpen ? closeSidebar() : openSidebar(pt))
      .addTo(map);
  });

  // Fecha sidebar ao clicar no mapa
  map.on('click', () => sidebarOpen && closeSidebar());

  // 8) Navegação inferior
  document.querySelectorAll('.bottom-nav .nav-btn').forEach(btn => {
    btn.addEventListener('click', () => {
      document.querySelectorAll('.bottom-nav .nav-btn')
        .forEach(b => b.classList.remove('active'));
      btn.classList.add('active');
      window.location.href = btn.dataset.href;
    });
  });

  // 9) Filtro lateral de categorias
  document.querySelectorAll('#category-panel button').forEach(btn => {
    btn.addEventListener('click', () => {
      const cat = btn.dataset.category;
      const wasActive = btn.classList.contains('active');
      document.querySelectorAll('#category-panel button')
        .forEach(b => b.classList.remove('active'));
      if (!wasActive) {
        btn.classList.add('active');
        // Exibe apenas marcadores da categoria
        points.forEach(pt => {
          pt.marker && (pt.category === cat
            ? pt.marker.addTo(map)
            : pt.marker.remove());
        });
      } else {
        // Se clicar de novo, mostra tudo
        points.forEach(pt => {
          pt.marker && pt.marker.addTo(map);
        });
      }
    });
  });
}
