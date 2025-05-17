// perguntas para o Quiz de Artesanato
const questionsArtesanato = [
  {
    pergunta: "O que é o \"marajoara\", um estilo de artesanato típico da região de Belém?",
    opcoes: [
      "Pinturas feitas com tintas naturais em telas",
      "Esculturas em madeira de formas geométricas",
      "Cerâmica decorada com desenhos tradicionais e figuras de animais",
      "Tecidos feitos à mão com fibras vegetais"
    ],
    correta: 2  // índice 2 → "Cerâmica decorada..."
  },
  {
    pergunta: "O que significa a técnica de \"marchetaria\", comum no artesanato de Belém?",
    opcoes: [
      "Pintura em tecido usando tintas naturais da região",
      "Criação de mosaicos com pedras e metais",
      "Arte de entalhar madeira e criar padrões com diferentes tipos de madeira",
      "Costura de tecidos para criar padrões florais"
    ],
    correta: 2  // índice 2 → "Arte de entalhar madeira..."
  },
  {
    pergunta: "O \"cestário paraense\" é conhecido pela produção de peças de qual material?",
    opcoes: [
      "Madeira de mogno",
      "Palha de buriti e tucumã",
      "Fibras sintéticas e plásticas",
      "Pedra-sabão"
    ],
    correta: 1  // índice 1 → "Palha de buriti e tucumã"
  }
];

// inicia o quiz: 10 XP por acerto e volta para /menu/puzzle ao final
startQuiz(questionsArtesanato, {
  xpPerCorrect: 10,
  redirectTo: '/menu/puzzle'
});
