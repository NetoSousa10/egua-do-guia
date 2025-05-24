// frontend/static/js/lojas.js

let pendingAmount = 0;

function closeModal(id) {
  const el = document.getElementById(id);
  if (el) el.classList.add('hidden');
}

function showMissionModal() {
  const el = document.getElementById('mission-modal');
  if (el) el.classList.remove('hidden');
}

function showPurchaseModal(text) {
  const textEl = document.getElementById('purchase-text');
  const modal  = document.getElementById('purchase-modal');
  if (textEl) textEl.textContent = text;
  if (modal) modal.classList.remove('hidden');
}

function confirmPurchase() {
  fetch('/store/grant_coins', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ amount: pendingAmount })
  })
  .then(res => res.json())
  .then(json => {
    if (json.error) {
      alert(json.error);
    } else {
      const saldoLojaEl = document.getElementById('saldo-loja');
      if (saldoLojaEl) saldoLojaEl.textContent = json.new_balance;
      alert("Moedas adicionadas com sucesso!");
    }
    closeModal('purchase-modal');
  })
  .catch(err => {
    console.error(err);
    alert("Não foi possível processar a compra.");
    closeModal('purchase-modal');
  });
}

document.addEventListener("DOMContentLoaded", () => {
  const grid = document.getElementById('grid-categorias');

  // 1) Atualiza e exibe o saldo na Loja (se existir o elemento)
  const saldoLojaEl = document.getElementById('saldo-loja');
  if (saldoLojaEl) {
    fetch('/store/balance')
      .then(res => res.json())
      .then(json => { saldoLojaEl.textContent = json.coins; })
      .catch(err => console.error('Erro ao carregar saldo:', err));
  }

  // 2) Popula categorias (se existir a grid)
  if (grid) {
    fetch('/store/categories')
      .then(res => res.json())
      .then(cats => {
        grid.innerHTML = cats.map(cat => `
          <a href="/store/opcoes/${cat.slug}" class="shop-item ${cat.slug}">
            <div class="item-img">
              <img src="${cat.img}" alt="${cat.name}">
            </div>
            <span class="item-label">${cat.name}</span>
          </a>
        `).join('');
      })
      .catch(err => {
        console.error('Erro ao carregar categorias:', err);
        grid.innerHTML = '<p class="error">Não foi possível carregar a loja.</p>';
      });
  }

  // 3) Inicializa missões e compra de moedas (se houver botões)
  document.querySelectorAll('.missions-list .mission-btn').forEach(btn => {
    if (btn.textContent.includes('R$')) {
      btn.addEventListener('click', () => {
        const xpText = btn.parentElement.querySelector('.mission-xp').textContent;
        pendingAmount = parseInt(xpText.replace(/\D+/g, ''), 10);
        showPurchaseModal(`Deseja comprar ${pendingAmount} moedas por ${btn.textContent.trim()}?`);
      });
    } else {
      btn.addEventListener('click', showMissionModal);
    }
  });

  // 4) Ligar botões do modal **somente se existirem**
  const btnConfirmar = document.getElementById('btn-confirmar');
  if (btnConfirmar) btnConfirmar.addEventListener('click', confirmPurchase);

  const btnCancelar = document.getElementById('btn-cancelar');
  if (btnCancelar) btnCancelar.addEventListener('click', () => closeModal('purchase-modal'));
});
