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
          : '/static/assets/img/default.jpg';  // seu placeholder real

        const card = document.createElement('div');
        card.className   = 'place-card';
        card.dataset.cat = p.category;
        card.innerHTML = `
          <img class="place-img" src="${imgSrc}" alt="${p.title}">
          <div class="place-info">
            <h3 class="place-title">${p.title}</h3>
            <div class="place-rating">
              ${[1,2,3,4,5].map(i => i <= p.rating ? '★' : '☆').join('')}
              <span class="reviews">(${p.reviews})</span>
            </div>
            ${p.features?.length
              ? `<ul class="place-features">
                   ${p.features.map(f => `<li>• ${f}</li>`).join('')}
                 </ul>` 
              : ''
            }
          </div>
        `;
        list.appendChild(card);
      });
    }
    renderAll();

    filterBtns.forEach(btn => {
      btn.addEventListener('click', () => {
        filterBtns.forEach(b => b.classList.remove('active'));
        btn.classList.add('active');
        const cat = btn.dataset.cat;
        document.querySelectorAll('.place-card').forEach(card => {
          card.style.display =
            (cat === 'all' || card.dataset.cat === cat) ? 'flex' : 'none';
        });
      });
    });

    // navbar
    document.querySelectorAll('.nav-btn').forEach(btn => {
      btn.addEventListener('click', () => window.location.href = btn.dataset.href);
    });

    // marca ativo
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
