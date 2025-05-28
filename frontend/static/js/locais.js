// static/js/locais.js
;(function(){
  function initLocaisApp() {
    const list       = document.querySelector('.locais-list');
    const filterBtns = document.querySelectorAll('.locais-filters button');
    if (!list) return;

    // Renderização dos cards
    function renderAll(items) {
      list.innerHTML = '';
      items.forEach(p => {
        const imgSrc = p.img_url || '/static/assets/img/default.jpg';

        // Features
        const featuresHtml = Array.isArray(p.features) && p.features.length
          ? `<ul class="place-features">
               ${p.features.map(f => {
                 const clean = String(f).replace(/^[\W_]+/, '').trim();
                 return `<li>${clean}</li>`;
               }).join('')}
             </ul>`
          : '';

        const stars = [1,2,3,4,5]
          .map(i => i <= p.rating ? '★' : '☆')
          .join(' ');
        const distance = p.distance_km != null
          ? `${p.distance_km.toFixed(1)} km`
          : '';
        const reviewsCount = p.reviews != null
          ? p.reviews.toLocaleString()
          : '0';

        const link = document.createElement('a');
        link.href = `/menu/detalhes/${p.id}`;
        link.className = 'place-link block no-underline';
        link.setAttribute('aria-label', `Detalhes de ${p.name}`);

        const card = document.createElement('div');
        card.className   = 'place-card';
        card.dataset.cat = p.categories && p.categories[0] || p.category || '';
               console.log()
        card.innerHTML = `
          <div class="place-img-wrapper">
            <img class="place-img" src="${imgSrc}" alt="${p.name}">
          </div>
          <div class="place-info">
            <h3 class="place-title">${p.name}</h3>
            <div class="place-rating">
              ${stars}
              <span class="reviews">(${reviewsCount})</span>
            </div>
            ${featuresHtml}
            <div class="place-meta">
              ${distance ? `<span class="place-distance">${distance}</span>` : ''}
            </div>
          </div>
        `;

        link.appendChild(card);
        list.appendChild(link);
      });
    }

    // Inicialmente exibe todos
    renderAll(window.PLACES);

    // Filtros de categoria
    filterBtns.forEach(btn => {
      btn.addEventListener('click', () => {
        filterBtns.forEach(b => b.classList.remove('active'));
        btn.classList.add('active');
        const cat = btn.dataset.cat;
        const filtered = (cat === 'all')
          ? window.PLACES
          : window.PLACES.filter(p => p.categories && p.categories.includes(cat));
        renderAll(filtered);
      });
    });

    // Navbar inferior
    document.querySelectorAll('.nav-btn').forEach(btn => {
      btn.addEventListener('click', () => {
        document.querySelectorAll('.nav-btn')
          .forEach(b => b.classList.remove('active'));
        btn.classList.add('active');
        window.location.href = btn.dataset.href;
      });
    });

    // Marca aba ativa
    const path = window.location.pathname;
    document.querySelectorAll('.nav-btn').forEach(btn => {
      btn.classList.toggle('active', btn.dataset.href === path);
    });
  }

  if (window.PLACES) {
    document.addEventListener('DOMContentLoaded', initLocaisApp);
  } else {
    document.addEventListener('placesReady', initLocaisApp);
  }
})();