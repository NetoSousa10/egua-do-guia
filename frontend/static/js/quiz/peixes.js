// perguntas para o Quiz de Peixes
const questionsPeixes = [
  {
    pergunta: "Qual é o prato típico de Belém que utiliza o peixe tucunaré?",
    opcoes: ["Maniçoba", "Pato no tucupi", "Tacacá", "Filhote na brasa"],
    correta: 3  // "Filhote na brasa"
  },
  {
    pergunta: "O que é a \"caldeirada\", prato típico que pode incluir peixe ou frutos do mar e é cozido com legumes e especiarias?",
    opcoes: [
      "Uma sopa de peixe",
      "Uma mistura de carne com feijão",
      "Um prato à base de arroz e peixe",
      "Um ensopado com peixe ou frutos do mar"
    ],
    correta: 3  // "Um ensopado com peixe..."
  },
  {
    pergunta: "Qual prato tradicional de Belém utiliza o \"jambu\", uma erva que provoca uma sensação de dormência na boca?",
    opcoes: ["Pato no Tucupi", "Maniçoba", "Tacacá", "Feijão verde com arroz"],
    correta: 2  // "Tacacá"
  }
];

// inicia o quiz: 10 XP por acerto e volta para /menu/puzzle ao final
startQuiz(questionsPeixes, {
  xpPerCorrect: 10,
  redirectTo: '/menu/puzzle'
});
