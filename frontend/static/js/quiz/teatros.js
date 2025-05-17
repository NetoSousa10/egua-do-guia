// perguntas para o Quiz de Teatros
const questionsTeatros = [
  {
    pergunta: "Qual é o nome do teatro mais antigo de Belém, que é considerado um dos principais marcos da arquitetura da cidade?",
    opcoes: [
      "Theatro da Paz",
      "Teatro Amazonas",
      "Teatro Maria Sylvia Nunes",
      "Teatro de Arena"
    ],
    correta: 0  // Theatro da Paz
  },
  {
    pergunta: "A 'Estação das Docas' é um complexo turístico e gastronômico de Belém. Que tipo de estilo arquitetônico foi utilizado para reformar os antigos armazéns de carga que deram origem ao local?",
    opcoes: [
      "Estilo colonial",
      "Estilo neoclássico",
      "Estilo industrial",
      "Estilo barroco"
    ],
    correta: 2  // Estilo industrial
  },
  {
    pergunta: "Qual elemento arquitetônico é amplamente utilizado nas construções de Belém devido ao clima quente e úmido da região amazônica?",
    opcoes: [
      "Telhados de vidro",
      "Paredes espessas e telhados baixos",
      "Grandes janelas e aberturas para ventilação natural",
      "Prédios com estruturas de concreto"
    ],
    correta: 2  // Grandes janelas e aberturas para ventilação natural
  }
];

// inicia o quiz: 10 XP por acerto e volta para /menu/puzzle ao final
startQuiz(questionsTeatros, {
  xpPerCorrect: 10,
  redirectTo: '/menu/puzzle'
});
