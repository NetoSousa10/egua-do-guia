// perguntas para o quiz de Festivais
const questionsFestivais = [
  {
    pergunta: "Qual é a principal religião praticada em Belém do Pará, especialmente em relação à festa de Círio de Nazaré?",
    opcoes: ["Catolicismo", "Evangelismo", "Espírita", "Protestantismo"],
    correta: 0
  },
  {
    pergunta: "Qual é o nome da festa tradicional que acontece no mês de junho, reunindo quadrilhas e celebrações típicas no Pará?",
    opcoes: ["Festa de São João", "Festa do Divino", "Festa de Nossa Senhora de Nazaré", "Carimbó"],
    correta: 0
  },
  {
    pergunta: "Qual é o costume da cidade de Belém durante o 'Dia de São João', celebrado no mês de junho?",
    opcoes: ["Fazer uma grande procissão", "Organizar uma festa com quadrilhas", "Realizar uma queima de fogos em toda a cidade", "Comer doces típicos e dançar carimbó"],
    correta: 1
  }
];

// inicia o quiz: 10XP por acerto, volta para /menu/puzzle ao final
startQuiz(questionsFestivais, {
  xpPerCorrect: 10,
  redirectTo: '/menu/puzzle'
});
