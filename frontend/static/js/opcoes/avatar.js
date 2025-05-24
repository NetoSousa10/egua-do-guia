// frontend/static/js/opcoes/avatar.js

document.addEventListener("DOMContentLoaded", () => {
  let saldo = 0;
  const saldoEl      = document.getElementById("saldo");
  const modal        = document.getElementById("modal");
  const modalText    = document.getElementById("modal-text");
  const btnCancelar  = document.getElementById("btn-cancelar");
  const btnConfirmar = document.getElementById("btn-confirmar");
  const backBtn      = document.getElementById("back-btn");

  let precoSelecionado   = 0;
  let itemSelecionado    = "";
  let itemIdSelecionado  = null;

  // 1) Busca e exibe o saldo
  fetch("/store/balance")
    .then(res => res.json())
    .then(json => {
      saldo = json.coins;
      saldoEl.textContent = saldo;
    })
    .catch(err => {
      console.error("Erro ao carregar saldo:", err);
      saldoEl.textContent = "—";
    });

  // 2) Configura clique em cada avatar-card
  document.querySelectorAll(".avatar-card").forEach(card => {
    card.addEventListener("click", () => {
      itemIdSelecionado  = +card.dataset.id;
      itemSelecionado    = card.querySelector(".nome").textContent;
      precoSelecionado   = +card.querySelector(".preco span").textContent;

      modalText.textContent =
        `Deseja comprar ${itemSelecionado} por ${precoSelecionado} moedas?`;
      modal.classList.add("active");
    });
  });

  // 3) Cancelar modal
  if (btnCancelar) {
    btnCancelar.addEventListener("click", () => {
      modal.classList.remove("active");
    });
  }

  // 4) Confirmar compra (persistida no backend)
  if (btnConfirmar) {
    btnConfirmar.addEventListener("click", () => {
      if (saldo < precoSelecionado) {
        alert("Você não tem moedas suficientes.");
        modal.classList.remove("active");
        return;
      }

      fetch("/store/purchase", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ item_id: itemIdSelecionado })
      })
      .then(res => res.json())
      .then(json => {
        if (json.error) {
          alert(json.error);
        } else {
          saldo = json.new_balance;
          saldoEl.textContent = saldo;
          alert(`Compra de ${itemSelecionado} confirmada!`);
        }
        modal.classList.remove("active");
      })
      .catch(err => {
        console.error("Erro ao processar compra:", err);
        alert("Não foi possível processar a compra.");
        modal.classList.remove("active");
      });
    });
  }

  // 5) Voltar
  if (backBtn) {
    backBtn.addEventListener("click", () => window.history.back());
  }
});
