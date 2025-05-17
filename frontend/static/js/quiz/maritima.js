// perguntas para o Quiz Marítima
const questionsMaritima = [
  {
    pergunta: "Qual é o prato típico de Belém que utiliza o peixe tucunaré?",
    opcoes: ["Maniçoba", "Pato no tucupi", "Tacacá", "Filhote na brasa"],
    correta: 3  // "Filhote na brasa"
  },
  {
    pergunta: "O que é a maniçoba, prato tradicional da culinária paraense?",
    opcoes: [
      "Uma sopa de peixe",
      "Um prato feito com carne de sol e arroz",
      "Uma iguaria feita com folhas de mandioca brava cozidas por vários dias",
      "Uma sobremesa à base de chocolate e frutas tropicais"
    ],
    correta: 2  // "iguaria feita com folhas de mandioca brava..."
  },
  {
    pergunta: "Qual é o ingrediente do \"Tacacá\", uma sopa típica do Pará?",
    opcoes: ["Peixe", "Pato", "Camarão", "Jambu"],
    correta: 2  // "Camarão"
  }
];

// inicia o quiz: 10 XP por acerto e volta para /menu/puzzle ao final
startQuiz(questionsMaritima, {
  xpPerCorrect: 10,
  redirectTo: '/menu/puzzle'
});
