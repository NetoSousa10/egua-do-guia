document.addEventListener('DOMContentLoaded', () => {
  const body = document.body;

  // Quando pressionar (mouse, touch, pen)
  body.addEventListener('pointerdown', e => {
    const btn = e.target.closest('.btn');
    if (btn) btn.classList.add('btn--pressed');
  });

  // Quando soltar ou cancelar o pointer
  body.addEventListener('pointerup',   removePress);
  body.addEventListener('pointercancel', removePress);
  body.addEventListener('pointerout',   removePress);

  function removePress(e) {
    const btn = e.target.closest('.btn');
    if (btn) btn.classList.remove('btn--pressed');
  }

  // Ativar via teclado (Enter ou Space)
  body.addEventListener('keydown', e => {
    const btn = e.target.closest('.btn');
    if (!btn) return;
    if (e.key === 'Enter' || e.key === ' ') {
      btn.classList.add('btn--pressed');
    }
  });
  body.addEventListener('keyup', e => {
    const btn = e.target.closest('.btn');
    if (!btn) return;
    if (e.key === 'Enter' || e.key === ' ') {
      btn.classList.remove('btn--pressed');
      btn.click();  // dispara o click programaticamente
    }
  });

  // Navegação para botões com data-href (e que não sejam submit)
  body.addEventListener('click', e => {
    const btn = e.target.closest('.btn[data-href]');
    if (!btn || btn.getAttribute('type') === 'submit') return;
    e.preventDefault();
    document.body.classList.add('fade-out');
    setTimeout(() => {
      window.location.href = btn.dataset.href;
    }, 300);
  });
});
