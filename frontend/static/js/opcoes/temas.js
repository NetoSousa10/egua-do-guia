document.addEventListener("DOMContentLoaded", () => {
  let saldo = 100;
  const saldoEl = document.getElementById("saldo");
  saldoEl.textContent = saldo;

  const modal = document.getElementById("modal");
  const modalText = document.getElementById("modal-text");
  const btnCancelar = document.getElementById("btn-cancelar");
  const btnConfirmar = document.getElementById("btn-confirmar");

  let precoSelecionado = 0;
  let temaSelecionado = "";

  document.querySelectorAll(".tema-card").forEach(card => {
    card.addEventListener("click", () => {
      const preco = parseInt(card.querySelector(".preco span").textContent);
      temaSelecionado = card.querySelector("img").alt;
      precoSelecionado = preco;

      modalText.textContent = `Deseja comprar ${temaSelecionado} por ${preco} moedas?`;
      modal.classList.add("active");
    });
  });

  btnCancelar.addEventListener("click", () => {
    modal.classList.remove("active");
  });

  btnConfirmar.addEventListener("click", () => {
    if (saldo >= precoSelecionado) {
      saldo -= precoSelecionado;
      saldoEl.textContent = saldo;
      alert(`Compra de ${temaSelecionado} confirmada!`);
    } else {
      alert("Você não tem moedas suficientes.");
    }
    modal.classList.remove("active");
  });

  const backBtn = document.getElementById("back-btn");
  if (backBtn) {
    backBtn.addEventListener("click", () => {
      window.location.href = "/menu/lojas";
    });
  }
});
