// perguntas para o Quiz Musical
const questionsMusical = [
  {
    pergunta: "Qual estilo musical é considerado um dos mais tradicionais de Belém e faz parte da cultura local?",
    opcoes: ["Sertanejo", "Frevo", "Carimbó", "Forró"],
    correta: 2  // índice 2 → "Carimbó"
  },
  {
    pergunta: "O que caracteriza a música \"siriá\", um estilo musical muito popular em Belém?",
    opcoes: [
      "Ritmos rápidos e dançantes com influência do samba",
      "Sons de marimbas e tambores de origem africana",
      "Canções de tema religioso e de louvação",
      "Uso de instrumentos de corda e sons da floresta amazônica"
    ],
    correta: 1  // índice 1 → "Sons de marimbas e tambores..."
  },
  {
    pergunta: "O que caracteriza a \"música paraense\" no contexto das suas influências?",
    opcoes: [
      "Influência do blues e rock",
      "Uso predominante de guitarras elétricas",
      "Mistura dos sons indígenas, africanos e portugueses",
      "Predominância de instrumentos de sopro"
    ],
    correta: 2  // índice 2 → "Mistura dos sons..."
  }
];

// inicializa o quiz: 10 XP por acerto, e volta para /menu/puzzle ao final
startQuiz(questionsMusical, {
  xpPerCorrect: 10,
  redirectTo: '/menu/puzzle'
});
