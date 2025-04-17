/**
 * form-validation.js
 * – Validação de formulário
 * – Exibe toast de sucesso e redireciona para /login
 * – Limpa a mensagem de erro em tempo real (oninput/onchange)
 */

document.addEventListener('DOMContentLoaded', () => {
  const form = document.querySelector('.formulario');
  const fields = Array.from(
    form.querySelectorAll('input[required], select[required]')
  );
  const checkbox = form.querySelector('input[type="checkbox"][required]');

  // 1) Adiciona listener para remover mensagem ao digitar/mudar
  fields.forEach(field => {
    const clearError = () => {
      const box = field.closest('.input-box') || field.closest('.checkbox-group');
      const msg = box.querySelector('.error-message');
      if (msg) msg.remove();
    };

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

  // 2) Submissão
  form.addEventListener('submit', function (e) {
    let isValid = true;

    // Limpa todas as mensagens antigas
    form.querySelectorAll('.error-message').forEach(el => el.remove());

    // Valida inputs e selects
    if (validateInputs(form))   isValid = false;
    // Valida o checkbox
    if (validateCheckbox(form)) isValid = false;

    if (!isValid) {
      e.preventDefault();
      return;
    }

    // Para testes locais (remova em produção)
    e.preventDefault();
    showToast('Cadastro realizado com sucesso!');
    // Depois, no callback do fetch/redirect do Flask:
    // window.location.href = '/login';
  });

  function validateInputs(form) {
    let invalid = false;
    form.querySelectorAll('input[required], select[required]').forEach(field => {
      const isSelect = field.tagName === 'SELECT';
      const isEmpty = isSelect
        ? field.value === '' || field.selectedIndex === 0
        : field.value.trim() === '';

      if (isEmpty) {
        invalid = true;
        const container = field.closest('.input-box');
        if (!container.querySelector('.error-message')) {
          container.appendChild(createErrorMsg());
        }
      }
    });
    return invalid;
  }

  function validateCheckbox(form) {
    const cb = form.querySelector('input[type="checkbox"][required]');
    if (cb && !cb.checked) {
      const wrapper = cb.closest('.checkbox-group');
      if (!wrapper.querySelector('.error-message')) {
        // injeta como irmão, para ficar abaixo
        wrapper.appendChild(createErrorMsg());
      }
      return true;
    }
    return false;
  }

  function createErrorMsg() {
    const msg = document.createElement('div');
    msg.className = 'error-message';
    msg.textContent = 'Este campo é obrigatório.';
    return msg;
  }
});
