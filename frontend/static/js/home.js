// static/js/home.js

// 1) Puxa o array criado em places.js
const points = window.PLACES;

// 0) Estado
let userLocation   = null;
let routingControl = null;
let sidebarOpen    = false;

// 1) Ícones por categoria
const ICON_MAP = {
  hotel:      '/static/icons/hotel.svg',
  restaurant: '/static/icons/restaurant.svg',
  praca:      '/static/icons/praca.svg',
  cultura:    '/static/icons/cultura.svg',
  loja:       '/static/icons/loja.svg',
  mall:       '/static/icons/mall.svg',
};

// 2) Inicializa o mapa
const map = L.map('map').setView([-1.4550, -48.4900], 13);
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
  attribution: '&copy; OpenStreetMap contributors'
}).addTo(map);

// 3) Geolocalização de alta precisão
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

// 5) Cria ícone customizado
function createIcon(category) {
  return L.icon({
    iconUrl:    ICON_MAP[category] || ICON_MAP.hotel,
    iconSize:   [56, 56],
    iconAnchor: [28, 56],
    popupAnchor:[0, -48],
    className:  'custom-marker-icon'
  });
}

// 6) Abre / fecha sidebar
function openSidebar(data) {
  document.body.classList.add('sidebar-open');
  sidebarOpen = true;
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
  routeTo({ lat: data.lat, lng: data.lng });
}
function closeSidebar() {
  document.body.classList.remove('sidebar-open');
  sidebarOpen = false;
}

// 7) Roteamento (Leaflet Routing Machine)
function routeTo(destination) {
  if (!userLocation) {
    alert('Não foi possível obter sua localização.');
    return;
  }
  if (routingControl) {
    map.removeControl(routingControl);
    routingControl = null;
  }
  routingControl = L.Routing.control({
    waypoints: [
      userLocation,
      L.latLng(destination.lat, destination.lng)
    ],
    lineOptions: { styles: [{ color: '#0075B7', weight: 5 }] },
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

// 10) Bottom-nav
document.querySelectorAll('.bottom-nav .nav-btn')
  .forEach(btn => btn.addEventListener('click', () => {
    document.querySelectorAll('.bottom-nav .nav-btn')
      .forEach(b => b.classList.remove('active'));
    btn.classList.add('active');
  }));

// 11) Filtro no painel lateral (categoria-panel)
document.querySelectorAll('#category-panel button')
  .forEach(btn => btn.addEventListener('click', () => {
    const cat       = btn.dataset.category;
    const wasActive = btn.classList.contains('active');
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
  }));
