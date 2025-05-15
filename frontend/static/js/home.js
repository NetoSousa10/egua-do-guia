// home.js

// 0) Variáveis de estado
let userLocation     = null;
let routingControl   = null;
let sidebarOpen      = false;

// 1) Mapeamento de ícones por categoria
const ICON_MAP = {
  hotel:      '/static/icons/hotel.svg',
  restaurant: '/static/icons/restaurant.svg',
  praca:      '/static/icons/praca.svg',
  cultura:    '/static/icons/cultura.svg',
  loja:       '/static/icons/loja.svg',
};

// 2) Inicializa o mapa
const map = L.map('map').setView([-1.4550, -48.4900], 13);
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
  attribution: '&copy; OpenStreetMap contributors'
}).addTo(map);

// 3) Tenta obter a localização do usuário com alta precisão e recentra o mapa
if (navigator.geolocation) {
  navigator.geolocation.getCurrentPosition(
    pos => {
      // 3.1) captura lat/lng
      userLocation = L.latLng(pos.coords.latitude, pos.coords.longitude);

      // 3.2) recentra o mapa nessa posição com zoom 15
      map.setView(userLocation, 15);

      // 3.3) marca no mapa
      L.circle(userLocation, { radius: 10, color: '#0075B7' })
        .addTo(map)
        .bindPopup('Você está aqui')
        .openPopup();
    },
    err => {
      console.warn('Erro geolocalização:', err);
    },
    {
      enableHighAccuracy: true,  // pede GPS de alta precisão
      timeout: 10000,            // espera até 10s por resposta
      maximumAge: 0              // não usa cache de localização
    }
  );
}

// 4) Pontos hard-coded para o MVP
const points = [
  {
    lat:      -1.4550,
    lng:      -48.4900,
    category: 'hotel',
    imgUrl:   '/static/assets/img/hotel1.jpg',
    title:    'Hotel Alphaville',
    rating:   4,
    hours:    'Open – Closes 23:00',
    address:  'Rod. BR-316, Km 4, 4500 Shopping Metrópoles – Coqueiro, Ananindeua – PA',
    phone:    '(91) 1234-5678',
    price:    'R$ 225,00 ~ R$ 820,00'
  },
  {
    lat:      -1.4540,
    lng:      -48.4905,
    category: 'loja',
    imgUrl:   '/static/assets/img/mall1.jpg',
    title:    'Shopping Metrópoles',
    rating:   4,
    hours:    'Aberto – Fecha às 23:00',
    address:  'Rod. BR-316, Km 4, 4500 Shopping Metrópoles – Coqueiro, Ananindeua – PA',
    phone:    '(91) 7456-1235',
    price:    'R$ 225,00 ~ R$ 820,00'
  },
  {
    lat:      -1.4617,
    lng:      -48.4902,
    category: 'praca',
    imgUrl:   '/static/assets/img/praca-republica.png',
    title:    'Praça da República',
    rating:   4,
    hours:    'Aberto 24h',
    address:  'Praça da República, Umarizal, Belém – PA, 66063-010',
    price:    'Gratuito'
  }
];

// 5) Função que cria ícone customizado
function createIcon(category) {
  return L.icon({
    iconUrl:    ICON_MAP[category] || ICON_MAP.hotel,
    iconSize:   [56, 56],
    iconAnchor: [28, 56],
    popupAnchor:[0, -48],
    className:  'custom-marker-icon'
  });
}

// 6) Funções de sidebar
function openSidebar(data) {
  document.body.classList.add('sidebar-open');
  sidebarOpen = true;

  // Preenche conteúdo
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
  document.getElementById('sidebar-phone').textContent   = data.phone || '';
  document.getElementById('sidebar-price').textContent   = data.price;

  // Traça a rota até este ponto
  routeTo({ lat: data.lat, lng: data.lng });
}

function closeSidebar() {
  document.body.classList.remove('sidebar-open');
  sidebarOpen = false;
}

// 7) Função de roteamento (Leaflet Routing Machine)
function routeTo(destination) {
  if (!userLocation) {
    alert('Não foi possível obter sua localização.');
    return;
  }
  // remove rota anterior
  if (routingControl) {
    map.removeControl(routingControl);
    routingControl = null;
  }
  // desenha nova rota
  routingControl = L.Routing.control({
    waypoints: [
      userLocation,
      L.latLng(destination.lat, destination.lng)
    ],
    lineOptions: {
      styles: [{ color: '#0075B7', weight: 5 }]
    },
    createMarker: () => null,
    fitSelectedRoutes: true,
    show: false
  }).addTo(map);
}

// 8) Plota marcadores e guarda para filtro
const allMarkers = [];
points.forEach(pt => {
  const m = L.marker([pt.lat, pt.lng], { icon: createIcon(pt.category) })
    .on('click', () => sidebarOpen ? closeSidebar() : openSidebar(pt))
    .addTo(map);
  allMarkers.push({ marker: m, category: pt.category });
});

// 9) Fecha sidebar ao clicar no mapa
map.on('click', () => sidebarOpen && closeSidebar());

// 10) Bottom-nav (se usado)
document.querySelectorAll('.bottom-nav .nav-btn').forEach(btn => {
  btn.addEventListener('click', () => {
    document.querySelectorAll('.bottom-nav .nav-btn')
      .forEach(b => b.classList.remove('active'));
    btn.classList.add('active');
  });
});

// 11) Filtro por categoria no painel
document.querySelectorAll('#category-panel button').forEach(btn => {
  btn.addEventListener('click', () => {
    const cat       = btn.getAttribute('data-category');
    const wasActive = btn.classList.contains('active');
    // limpa todos
    document.querySelectorAll('#category-panel button')
      .forEach(b => b.classList.remove('active'));

    if (!wasActive) {
      btn.classList.add('active');
      allMarkers.forEach(({ marker, category }) => {
        if (category === cat) map.addLayer(marker);
        else                  map.removeLayer(marker);
      });
    } else {
      allMarkers.forEach(({ marker }) => map.addLayer(marker));
    }
  });
});
