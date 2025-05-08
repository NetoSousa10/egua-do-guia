// 1) Inicia o mapa
const map = L.map('map').setView([-1.4550, -48.4900], 13);
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
  attribution: '&copy; OpenStreetMap contributors'
}).addTo(map);

// 2) Agora cada ponto deve ter estas propriedades:
const points = [
  {
    lat:      -1.4550,
    lng:      -48.4900,
    iconUrl:  "/static/icons/marker-hotel.png",    // ícone do mapa
    imgUrl:   "/static/assets/img/hotel1.jpg",          // banner da sidebar
    title:    "Hotel Alphaville",
    rating:   4,                           
    hours:    "Open - Closes 23:00",
    address:  "Rod. BR-316, Km 4, 4500 Shopping Metrópoles - Coqueiro, Ananindeua - PA, 67113-970",
    phone:    "(91) 1234-5678",
    price:    "R$ 225,00 ~ R$ 820,00"
  },
  {
    lat:      -1.4540,   // ajuste para a latitude real do Mall
    lng:      -48.4905,  // ajuste para a longitude real do Mall
    iconUrl:  "/static/icons/marker-mall.png",        // crie um ícone em static/icons/marker-mall.png
    imgUrl:   "/static/assets/img/mall1.jpg",         // coloque a foto em static/assets/img/mall1.jpg
    title:    "Shopping Metrópoles",
    rating:   4,
    hours:    "Open - Closes 23:00",
    address:  "Rod. BR-316, Km 4, 4500 Shopping Metrópoles - Coqueiro, Ananindeua - PA, 67113-970",
    phone:    "(91) 7456-1235",
    price:    "R$ 225,00 ~ R$ 820,00",
    category: "mall"
  }
];

// 3) Estado da sidebar
let sidebarOpen = false;
function openSidebar(data) {
  document.body.classList.add('sidebar-open');
  sidebarOpen = true;

  // preenche DOM
  document.getElementById('sidebar-title').textContent = data.title;
  document.getElementById('sidebar-img').src         = data.imgUrl;
  document.getElementById('sidebar-img').alt         = data.title;

  // estrelas
  let stars = "";
  for (let i=1; i<=5; i++) {
    stars += (i <= data.rating)
      ? "★"
      : "☆";
  }
  document.getElementById('sidebar-rating').textContent = stars;

  document.getElementById('sidebar-hours').textContent   = data.hours;
  document.getElementById('sidebar-address').textContent = data.address;
  document.getElementById('sidebar-phone').textContent   = data.phone;
  document.getElementById('sidebar-price').textContent   = data.price;
}

function closeSidebar() {
  document.body.classList.remove('sidebar-open');
  sidebarOpen = false;
}

// 4) cria ícone
function createIcon(url) {
  return L.icon({
    iconUrl: url,
    iconSize:   [56, 56],      //  tamanho maior
    iconAnchor: [28, 56],      //  centra pelo meio inferior
    popupAnchor:[0, -48],
    className:  'custom-marker-icon',
  });
}

// 5) plota marcadores
points.forEach(pt => {
  const m = L.marker([pt.lat, pt.lng], { icon: createIcon(pt.iconUrl) })
    .addTo(map)
    .on('click', () => {
      sidebarOpen ? closeSidebar() : openSidebar(pt);
    });
});

// fecha sidebar ao clicar no mapa
map.on('click', () => sidebarOpen && closeSidebar());

// ativa/desativa botões da barra inferior
document.querySelectorAll('.bottom-nav .nav-btn')
  .forEach(btn => btn.addEventListener('click', () => {
    document.querySelectorAll('.bottom-nav .nav-btn')
      .forEach(b => b.classList.remove('active'));
    btn.classList.add('active');
  }));
