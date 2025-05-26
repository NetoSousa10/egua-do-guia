document.addEventListener("DOMContentLoaded", () => {
  // Abas e conteúdo
  const abas = document.querySelectorAll(".aba");
  const conteudos = document.querySelectorAll(".conteudo-aba");

  abas.forEach((aba, index) => {
    aba.addEventListener("click", () => {
      abas.forEach(a => a.classList.remove("active"));
      conteudos.forEach(c => c.style.display = "none");

      aba.classList.add("active");
      conteudos[index].style.display = "block";
    });
  });

  // Estrelas de "visão geral"
  const estrelas = document.querySelectorAll("#estrelas span");
  let notaGeral = 3;

  function atualizarEstrelas(nota) {
    estrelas.forEach(star => {
      const valor = parseInt(star.dataset.valor);
      star.classList.toggle("selecionada", valor <= nota);
    });
  }

  atualizarEstrelas(notaGeral);

  estrelas.forEach(star => {
    star.addEventListener("click", () => {
      notaGeral = parseInt(star.dataset.valor);
      atualizarEstrelas(notaGeral);
      alert(`Você avaliou com ${notaGeral} estrelas!`);
    });
  });

  // Comentário simples
  const comentarioInput = document.getElementById("comentario");
  const enviarBtn = document.getElementById("enviar-comentario");
  const comentarioExibido = document.getElementById("comentario-exibido");

  if (enviarBtn) {
    enviarBtn.addEventListener("click", () => {
      const texto = comentarioInput.value.trim();
      if (texto) {
        comentarioExibido.textContent = texto;
        comentarioExibido.style.display = "block";
        comentarioInput.value = "";
      }
    });
  }

  // Estrelas de "Aba Avaliações"
  const estrelasAvaliacao = document.querySelectorAll("#estrelas-avaliacao span");
  let notaAvaliacao = 3;

  function atualizarEstrelasAvaliacao(nota) {
    estrelasAvaliacao.forEach(star => {
      const valor = parseInt(star.dataset.valor);
      star.classList.toggle("selecionada", valor <= nota);
    });
  }

  atualizarEstrelasAvaliacao(notaAvaliacao);

  estrelasAvaliacao.forEach(star => {
    star.addEventListener("click", () => {
      notaAvaliacao = parseInt(star.dataset.valor);
      atualizarEstrelasAvaliacao(notaAvaliacao);
    });
  });

  const btnAvaliar = document.querySelector(".btn-avaliar");
  if (btnAvaliar) {
    btnAvaliar.addEventListener("click", () => {
      alert(`Você avaliou com ${notaAvaliacao} estrelas!`);
    });
  }
});
