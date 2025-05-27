// ─── frontend/static/js/detalhes.js ───

// 1) pega o place_id do atributo data-place-id
const PLACE_ID = Number(
  document.querySelector('.detalhes-screen').dataset.placeId
);

document.addEventListener("DOMContentLoaded", () => {
  // ——— 1) ABAS ———
  const abas     = document.querySelectorAll(".aba");
  const conteudo = document.querySelectorAll(".conteudo-aba");
  abas.forEach((aba, idx) => {
    aba.addEventListener("click", () => {
      abas.forEach(a => a.classList.remove("active"));
      conteudo.forEach(c => c.style.display = "none");
      aba.classList.add("active");
      conteudo[idx].style.display = "block";
    });
  });

  // ——— 2) VISÃO GERAL ———
  // (se você ainda usar aquele bloco de avaliação geral com id="estrelas")
  const estrelasGerais = document.querySelectorAll("#estrelas span");
  let notaGeral = 3;
  function updateEstGerais(n) {
    estrelasGerais.forEach(star => {
      const v = parseInt(star.dataset.valor, 10);
      star.classList.toggle("selecionada", v <= n);
    });
  }
  // inicializa
  updateEstGerais(notaGeral);
  // clique para mudar nota geral
  estrelasGerais.forEach(star => {
    star.addEventListener("click", () => {
      notaGeral = parseInt(star.dataset.valor, 10);
      updateEstGerais(notaGeral);
      alert(`Nota geral: ${notaGeral} estrelas.`);
    });
  });

  // campo de comentário simples na aba geral
  const inpComent = document.getElementById("comentario");
  const btnComent = document.getElementById("enviar-comentario");
  const boxComent = document.getElementById("comentario-exibido");
  btnComent?.addEventListener("click", () => {
    const txt = inpComent.value.trim();
    if (!txt) return alert("Escreva algo.");
    boxComent.textContent = txt;
    boxComent.style.display = "block";
    inpComent.value = "";
  });

  // ——— 3) AVALIAÇÕES DO USUÁRIO ———
  // estrelas interativas (id="user-rating")
  const estrelasAva = document.querySelectorAll("#user-rating span");
  let notaAva = 3;
  function updateEstAva(n) {
    estrelasAva.forEach(star => {
      const v = parseInt(star.dataset.value, 10);
      star.classList.toggle("selecionada", v <= n);
    });
  }
  // inicializa
  updateEstAva(notaAva);
  // clique nas estrelas
  estrelasAva.forEach(star => {
    star.addEventListener("click", () => {
      notaAva = parseInt(star.dataset.value, 10);
      updateEstAva(notaAva);
    });
  });

  // botão de envio da review
  const btnAvaliar = document.getElementById("submit-review");
  btnAvaliar?.addEventListener("click", () => {
    const commentField = document.getElementById("new-comment");
    const commentText  = commentField.value.trim();
    if (notaAva < 1 || !commentText) {
      return alert("Selecione uma nota e escreva seu comentário.");
    }
    fetch(`/api/places/${PLACE_ID}/reviews`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ score: notaAva, comment: commentText })
    })
    .then(res => {
      if (!res.ok) return res.json().then(e => Promise.reject(e.error||"Erro"));
      return res.json();
    })
    .then(() => location.reload())
    .catch(err => alert("Falha ao enviar: " + err));
  });

});
