document.addEventListener('DOMContentLoaded', function() {
    const buttons = document.querySelectorAll('.btn');
    
    buttons.forEach(button => {
      // Quando o botão é pressionado
      button.addEventListener('mousedown', function() {
        // Aplica o efeito de recuo
        button.style.transform = 'scale(0.95) translateY(2px)';
        // Remove a sombra definida, se houver (caso queira que a sombra desapareça)
        button.style.boxShadow = 'none';
      });
      
      // Quando o botão é liberado
      button.addEventListener('mouseup', function() {
        // Restaura o estado normal
        button.style.transform = 'none';
        // Remove o estilo inline da box-shadow para que o CSS assuma o controle novamente
        button.style.boxShadow = '';
      });
      
      // Caso o cursor saia do botão enquanto pressionado
      button.addEventListener('mouseleave', function() {
        button.style.transform = 'none';
        button.style.boxShadow = '';
      });
    });
  });
  