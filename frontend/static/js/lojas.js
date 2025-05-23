function closeModal(id) {
  document.getElementById(id).classList.add('hidden');
}

function showMissionModal() {
  document.getElementById('mission-modal').classList.remove('hidden');
}

function showPurchaseModal(text) {
  document.getElementById('purchase-text').textContent = text;
  document.getElementById('purchase-modal').classList.remove('hidden');
}

function confirmPurchase() {
  alert("Compra realizada com sucesso!"); // substitua por integração real no futuro
  closeModal('purchase-modal');
}

// Ao carregar a página
document.addEventListener("DOMContentLoaded", () => {
  document.querySelectorAll('.missions-list .mission-btn').forEach((btn) => {
    const isCompra = btn.textContent.includes('R$');
    if (isCompra) {
      btn.addEventListener('click', () => {
        const moeda = btn.parentElement.querySelector('.mission-xp')?.textContent;
        const preco = btn.textContent;
        showPurchaseModal(`Deseja comprar ${moeda} por ${preco}?`);
      });
    } else {
      btn.addEventListener('click', () => {
        showMissionModal();
      });
    }
  });
});
