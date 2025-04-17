$(document).ready(function () {
    // Formata nacionalidade com bandeira
    function formatCountry(state) {
      if (!state.id) return state.text;
  
      const code = state.element.value.toLowerCase();
      const flagUrl = `https://flagcdn.com/24x18/${code}.png`;
  
      const $element = $(`
        <span>
          <img src="${flagUrl}" class="img-flag" onerror="this.style.display='none'" />
          ${state.text}
        </span>
      `);
  
      return $element;
    }
  
    // Ativa Select2 com bandeiras (nacionalidade)
    $('#nacionalidade').select2({
      templateResult: formatCountry,
      templateSelection: formatCountry,
      minimumResultsForSearch: -1,
      width: '100%'
    });
  
    // Ativa Select2 para o gênero (sem bandeiras)
    $('#genero').select2({
      minimumResultsForSearch: -1,
      width: '100%'
    });
  });
  