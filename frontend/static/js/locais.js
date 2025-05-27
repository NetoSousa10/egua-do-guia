// static/js/locais.js
;(function(){
  function initLocaisApp() {
    const list       = document.querySelector('.locais-list');
    const filterBtns = document.querySelectorAll('.locais-filters button');
    if (!list) return;

    function renderAll() {
      list.innerHTML = '';
      window.PLACES.forEach(p => {
        const hasImg = p.imgUrl && p.imgUrl.trim() !== '';
        const imgSrc = hasImg
          ? p.imgUrl
          : '/static/assets/img/default.jpg';

        // monta bullets a partir de p.features (array de strings),
        // mas removendo qualquer símbolo inicial e deixando o <li> SEM "• "
        const featuresHtml = Array.isArray(p.features) && p.features.length
          ? `<ul class="place-features">
               ${p.features
                 .map(f => {
                   const clean = String(f).replace(/^[\W_]+/, '').trim();
                   return `<li>${clean}</li>`;
                 })
                 .join('')}
             </ul>`
          : '';

        const stars = [1,2,3,4,5]
          .map(i => i <= p.rating ? '★' : '☆')
          .join(' ');

        // Cria o link que envolve o cartão
        const link = document.createElement('a');
        link.href = `/menu/detalhes/${p.id}`;
        link.className = 'place-link block no-underline';
        link.setAttribute('aria-label', `Detalhes de ${p.title}`);

        const card = document.createElement('div');
        card.className   = 'place-card';
        card.dataset.cat = p.category;

        card.innerHTML = `
          <div class="place-img-wrapper">
            <img class="place-img" src="${imgSrc}" alt="${p.title}">
          </div>
          <div class="place-info">
            <h3 class="place-title">${p.title}</h3>
            <div class="place-rating">
              ${stars}
              <span class="reviews">(${p.reviews.toLocaleString()})</span>
            </div>
            ${featuresHtml}
          </div>
        `;

        // Anexa o card dentro do link, e o link na lista
        link.appendChild(card);
        list.appendChild(link);
      });
    }

    renderAll();

    // filtros de categoria
    filterBtns.forEach(btn => {
      btn.addEventListener('click', () => {
        filterBtns.forEach(b => b.classList.remove('active'));
        btn.classList.add('active');
        const cat = btn.dataset.cat;
        document.querySelectorAll('.place-link').forEach(link => {
          const card = link.querySelector('.place-card');
          link.style.display =
            (cat === 'all' || card.dataset.cat === cat) ? 'flex' : 'none';
        });
      });
    });

    // navbar inferior
    document.querySelectorAll('.nav-btn').forEach(btn => {
      btn.addEventListener('click', () => {
        document.querySelectorAll('.nav-btn')
          .forEach(b => b.classList.remove('active'));
        btn.classList.add('active');
        window.location.href = btn.dataset.href;
      });
    });

    // marca ativo na nav
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
