// perguntas para o Quiz de Frutas
const questionsFrutas = [
  {
    pergunta: "O \"cupuaçu\", fruto muito utilizado na culinária paraense, é conhecido por qual sabor característico?",
    opcoes: [
      "Sabor ácido e refrescante",
      "Sabor amargo com notas de café",
      "Sabor doce e levemente azedo, com uma textura cremosa",
      "Sabor picante e picante"
    ],
    correta: 2  // "Sabor doce e levemente azedo..."
  },
  {
    pergunta: "O que é o \"bacuri\", um dos frutos típicos do Pará, usado para fazer sucos e sobremesas?",
    opcoes: [
      "Uma fruta tropical com casca espessa e polpa doce e azeda",
      "Uma fruta com casca macia e polpa cremosa",
      "Uma fruta pequena e ácida",
      "Uma fruta amarga e oleosa"
    ],
    correta: 0  // "fruta tropical com casca espessa..."
  },
  {
    pergunta: "Qual é a planta típica da Amazônia usada na gastronomia paraense, especialmente no prato \"tacacá\"?",
    opcoes: ["Jambu", "Guaraná", "Bacuri", "Maracujá"],
    correta: 0  // "Jambu"
  }
];

// inicializa o quiz: 10 XP por acerto, volta para /menu/puzzle ao final
startQuiz(questionsFrutas, {
  xpPerCorrect: 10,
  redirectTo: '/menu/puzzle'
});
