// frontend/static/js/avatar.js

document.addEventListener("DOMContentLoaded", () => {
  // Quantidade de opções em cada categoria
  const categorias = {
    corpo: 3,
    boca: 3,
    olhos: 3,
    cabelo: 3,
    camisa: 3
  };

  // Estado atual (índice de cada variação)
  let selecionados = {
    corpo: 1,
    boca: 1,
    olhos: 1,
    cabelo: 1,
    camisa: 1
  };

  // Mapeamento das IDs de cada camada
  const avatarIds = {
    corpo:  "avatar-corpo",
    bracos: "avatar-bracos",
    cabelo: "avatar-cabelo",
    camisa: "avatar-camisa",
    olhos:  "avatar-olhos",
    boca:   "avatar-boca"
  };

  const botoesCat = document.querySelectorAll(".categoria-icons button");
  const opcoesDiv = document.getElementById("opcoes-avatar");

  // Renderiza as miniaturas para a categoria 'cat'
  function renderOpcoes(cat) {
    opcoesDiv.innerHTML = "";
    const total = categorias[cat];

    for (let i = 1; i <= total; i++) {
      const mini = document.createElement("img");
      mini.src = `/static/assets/avatar/${cat}${i}.svg`;
      mini.alt = `${cat} ${i}`;
      mini.classList.toggle("selected", i === selecionados[cat]);

      mini.addEventListener("click", () => {
        // Atualiza a escolha para essa categoria
        selecionados[cat] = i;

        // Se for 'corpo', sincroniza também os 'braços'
        if (cat === "corpo") {
          selecionados["bracos"] = i;
        }

        atualizarAvatar();
        renderOpcoes(cat);
      });

      opcoesDiv.appendChild(mini);
    }
  }

  // Atualiza cada camada do avatar de acordo com 'selecionados'
  function atualizarAvatar() {
    // 1) Corpo
    document
      .getElementById(avatarIds["corpo"])
      .setAttribute("src", `/static/assets/avatar/corpo${selecionados.corpo}.svg`);

    // 2) Braços (mesma variação do corpo)
    document
      .getElementById(avatarIds["bracos"])
      .setAttribute("src", `/static/assets/avatar/bracos${selecionados.bracos}.svg`);

    // 3) Camisa
    document
      .getElementById(avatarIds["camisa"])
      .setAttribute("src", `/static/assets/avatar/camisa${selecionados.camisa}.svg`);

    // 4) Cabelo
    document
      .getElementById(avatarIds["cabelo"])
      .setAttribute("src", `/static/assets/avatar/cabelo${selecionados.cabelo}.svg`);

    // 5) Olhos
    document
      .getElementById(avatarIds["olhos"])
      .setAttribute("src", `/static/assets/avatar/olhos${selecionados.olhos}.svg`);

    // 6) Boca
    document
      .getElementById(avatarIds["boca"])
      .setAttribute("src", `/static/assets/avatar/boca${selecionados.boca}.svg`);
  }

  // Alterna a categoria ativa e renderiza opções
  botoesCat.forEach(btn => {
    btn.addEventListener("click", () => {
      botoesCat.forEach(b => b.classList.remove("active"));
      btn.classList.add("active");
      renderOpcoes(btn.dataset.cat);
    });
  });

  // Render inicial: mostra opções de ‘corpo’
  renderOpcoes("corpo");

  // Ao clicar em “Finalizar”, volta ao perfil
  document.getElementById("btn-finalizar").addEventListener("click", () => {
    alert("Avatar finalizado!");
    window.location.href = "/menu/perfil"; // Ajuste conforme sua rota real
  });
});
