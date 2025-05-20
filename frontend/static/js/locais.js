// static/js/locais.js
document.addEventListener('DOMContentLoaded', () => {
  const list       = document.querySelector('.locais-list');
  const filterBtns = document.querySelectorAll('.locais-filters button');

  // 1) Renderiza todos os cards
  function renderAll() {
    list.innerHTML = '';
    window.PLACES.forEach(p => {
      const card = document.createElement('div');
      card.className   = 'place-card';
      card.dataset.cat = p.category;

      card.innerHTML = `
        <img class="place-img"
             src="${p.imgUrl}"
             alt="${p.title}">
        <div class="place-info">
          <h3 class="place-title">${p.title}</h3>
          <div class="place-rating">
            ${[1,2,3,4,5]
              .map(i => i <= p.rating ? '★' : '☆')
              .join('')}
            <span class="reviews">(${p.reviews})</span>
          </div>
          ${p.features?.length
            ? `<ul class="place-features">
                ${p.features.map(f => `<li>• ${f}</li>`).join('')}
               </ul>`
            : ``
          }
        </div>
      `;
      list.appendChild(card);
    });
  }

  renderAll();

  // 2) Filtro por categoria
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

  // 3) Navegação inferior
  document.querySelectorAll('.nav-btn').forEach(btn => {
    btn.addEventListener('click', () => {
      window.location.href = btn.dataset.href;
    });
  });
});
