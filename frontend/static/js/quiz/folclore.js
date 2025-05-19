// perguntas para o Quiz de Folclore
const questionsFolclore = [
  {
    pergunta: "Qual figura mitológica paraense é conhecida por seu canto encantador e por atrair os homens para as águas do rio?",
    opcoes: ["Iara", "Curupira", "Boto", "Mapinguari"],
    correta: 0  // "Iara"
  },
  {
    pergunta: "Quem é o Curupira, uma figura popular no folclore amazônico?",
    opcoes: [
      "Um monstro que vive na floresta e devora quem desrespeita a natureza",
      "Uma mulher que canta para seduzir pescadores",
      "Uma criatura com os pés virados para trás que protege as florestas e animais",
      "Um ser invisível que aparece apenas à noite"
    ],
    correta: 2  // "pés virados para trás..."
  },
  {
    pergunta: "O que é o \"Boi Bumbá\", uma das manifestações culturais mais importantes do folclore paraense?",
    opcoes: [
      "Uma festa religiosa de origem católica",
      "Um evento que celebra a caça e pesca na Amazônia",
      "Uma dança folclórica em que se representa a morte e ressurreição de um boi",
      "Uma festa dedicada à colheita de açaí"
    ],
    correta: 2  // "dança folclórica..."
  }
];

// inicia o quiz: 10 XP por acerto e volta para /menu/puzzle ao final
startQuiz(questionsFolclore, {
  xpPerCorrect: 10,
  redirectTo: '/menu/puzzle'
});
