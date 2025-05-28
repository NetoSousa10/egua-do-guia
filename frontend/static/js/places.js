// static/js/places.js

// Fallback Haversine para distância em linha reta
function haversineDist(a, b) {
  const toRad = d => d * Math.PI / 180;
  const R = 6371;
  const dLat = toRad(b.lat - a.lat);
  const dLon = toRad(b.lng - a.lng);
  const la = toRad(a.lat), lb = toRad(b.lat);
  const h = Math.sin(dLat/2)**2 + Math.cos(la) * Math.cos(lb) * Math.sin(dLon/2)**2;
  return parseFloat((2 * R * Math.atan2(Math.sqrt(h), Math.sqrt(1 - h))).toFixed(2));
}

// Lê o JSON raw injetado no HTML
function getRawPlaces() {
  const el = document.getElementById('raw-places-data');
  if (!el) return [];
  try {
    return JSON.parse(el.textContent || '[]');
  } catch (e) {
    console.error('Erro parseando raw_places JSON:', e);
    return [];
  }
}

// Obtém localização do usuário
async function getUserLocation() {
  return new Promise((resolve, reject) => {
    if (!navigator.geolocation) return reject(new Error('Geolocalização não disponível'));
    navigator.geolocation.getCurrentPosition(
      pos => resolve({ lat: pos.coords.latitude, lng: pos.coords.longitude }),
      err => reject(err),
      { enableHighAccuracy: true, timeout: 10000, maximumAge: 0 }
    );
  });
}

// Calcula distância via Google Distance Matrix; fallback Haversine
async function computeDistance(user, place) {
  try {
    const params = new URLSearchParams({
      lat1: user.lat, lng1: user.lng,
      lat2: place.lat, lng2: place.lng
    });
    const resp = await fetch(`/api/distance?${params}`);
    const data = await resp.json();
    if (resp.ok && data.distance_km != null) return data.distance_km;
    throw new Error('Distance Matrix retornou null');
  } catch (e) {
    console.warn('Distance Matrix falhou:', e.message, '; usando Haversine.');
    return haversineDist(user, place);
  }
}

// Ordenação local por distância asc e rating desc
function sortByDistThenRating(arr) {
  return arr.slice().sort((a, b) => {
    if (a.distance_km !== b.distance_km) return a.distance_km - b.distance_km;
    return b.rating - a.rating;
  });
}

// Ordenação local por rating desc e distância asc (para 'Populares')
function sortByRatingThenDist(arr) {
  return arr.slice().sort((a, b) => {
    if (b.rating !== a.rating) return b.rating - a.rating;
    return a.distance_km - b.distance_km;
  });
}

// Busca, filtra e ordena localmente
async function fetchRecommendedPlaces(preferences) {
  const rawPlaces = getRawPlaces();
  if (!rawPlaces.length) {
    window.PLACES = [];
    document.dispatchEvent(new Event('placesReady'));
    return;
  }

  // Calcula distâncias e mantém reviews
  const user = await getUserLocation();
  const withDist = await Promise.all(
    rawPlaces.map(async p => ({
      ...p,
      distance_km: await computeDistance(user, p)
    }))
  );

  let output;
  // Todos
  if (preferences.length === 0) {
    output = sortByDistThenRating(withDist);

  // Populares
  } else if (preferences.length === 1 && preferences[0] === 'popular') {
    output = sortByRatingThenDist(withDist);

  // Categoria específica
  } else {
    const cat = preferences[0];
    const filtered = withDist.filter(p => p.categories.includes(cat));
    output = sortByDistThenRating(filtered);
  }

  window.PLACES = output;
  document.dispatchEvent(new Event('placesReady'));
}

// Inicia ao carregar o DOM
document.addEventListener('DOMContentLoaded', () => {
  fetchRecommendedPlaces([]);
  document.querySelectorAll('.locais-filters button').forEach(btn => {
    btn.addEventListener('click', () => {
      document.querySelectorAll('.locais-filters button')
        .forEach(b => b.classList.remove('active'));
      btn.classList.add('active');
      const cat = btn.dataset.cat;
      const prefs = (cat === 'all') ? [] : [cat];
      fetchRecommendedPlaces(prefs);
    });
  });
});
