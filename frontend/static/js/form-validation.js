/**
 * form-validation.js
 * – Validação de formulário
 * – Limpa a mensagem de erro em tempo real (oninput/onchange)
 * – Em caso de sucesso, permite o submit normal para o backend
 */

document.addEventListener('DOMContentLoaded', () => {
  const form = document.querySelector('.formulario');
  if (!form) return;

  const fields   = Array.from(form.querySelectorAll('input[required], select[required]'));
  const checkbox = form.querySelector('input[type="checkbox"][required]');

  // 1) Remove mensagens antigas enquanto o usuário digita/muda valor
  fields.forEach(field => {
    const clearError = () => {
      const box = field.closest('.input-box') || field.closest('.checkbox-group');
      const msg = box.querySelector('.error-message');
      if (msg) msg.remove();
    };
    // substituído o assignment inválido por addEventListener
    if (field.tagName === 'SELECT') {
      field.addEventListener('change', clearError);
    } else {
      field.addEventListener('input', clearError);
    }
  });

  if (checkbox) {
    checkbox.addEventListener('change', () => {
      const wrapper = checkbox.closest('.checkbox-group');
      const msg = wrapper.querySelector('.error-message');
      if (msg) msg.remove();
    });
  }

  // 2) Submissão: apenas previne se houver erro; caso contrário, permite o envio
  form.addEventListener('submit', function (e) {
    let isValid = true;

    // limpa erros antigos
    form.querySelectorAll('.error-message').forEach(el => el.remove());

    // checa inputs e selects
    form.querySelectorAll('input[required], select[required]').forEach(field => {
      const isSelect = field.tagName === 'SELECT';
      const isEmpty = isSelect
        ? field.value === '' || field.selectedIndex === 0
        : field.value.trim() === '';

      if (isEmpty) {
        isValid = false;
        const container = field.closest('.input-box');
        if (!container.querySelector('.error-message')) {
          container.appendChild(createErrorMsg());
        }
      }
    });

    // checa checkbox
    if (checkbox && !checkbox.checked) {
      isValid = false;
      const wrapper = checkbox.closest('.checkbox-group');
      if (!wrapper.querySelector('.error-message')) {
        wrapper.appendChild(createErrorMsg());
      }
    }

    if (!isValid) {
      e.preventDefault();
    }
    // se isValid == true, NÃO chamamos preventDefault: form submeterá normalmente
  });

  function createErrorMsg() {
    const msg = document.createElement('div');
    msg.className = 'error-message';
    msg.textContent = 'Este campo é obrigatório.';
    return msg;
  }
});
