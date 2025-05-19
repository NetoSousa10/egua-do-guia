// perguntas para o Quiz de Bairros
const questionsBairros = [
  {
    pergunta: "Belém é famosa por suas praças e áreas de lazer históricas. Qual é o nome da praça mais conhecida de Belém, localizada no centro da cidade, cercada por construções históricas como a Catedral da Sé e o Palácio Lauro Sodré?",
    opcoes: ["Praça da República", "Praça Dom Pedro II", "Praça da Palmeira", "Praça de Nazaré"],
    correta: 1  // índice 1 → Praça Dom Pedro II
  },
  {
    pergunta: "A cidade de Belém tem uma característica única quando se fala sobre suas ruas. O que as ruas do centro histórico de Belém têm em comum em relação à sua pavimentação?",
    opcoes: ["São feitas de paralelepípedos", "São pavimentadas com blocos de pedra", "São pavimentadas com ladrilhos de cerâmica", "Têm pisos de madeira, como nas ruas antigas"],
    correta: 1  // índice 1 → blocos de pedra
  },
  {
    pergunta: "A Estação das Docas, um importante centro de lazer e turismo em Belém, foi originalmente construída para qual finalidade?",
    opcoes: ["Mercado de peixe", "Terminal portuário", "Estádio de futebol", "Fabricação de produtos têxteis"],
    correta: 1  // índice 1 → Terminal portuário
  }
];

// inicia o quiz: 10 XP por acerto e volta para /menu/puzzle ao final
startQuiz(questionsBairros, {
  xpPerCorrect: 10,
  redirectTo: '/menu/puzzle'
});
