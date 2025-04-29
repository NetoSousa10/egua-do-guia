/**
 * form-validation.js
 * – Validação de formulário
 * – Limpa a mensagem de erro em tempo real (oninput/onchange)
 * – Em caso de sucesso, permite o submit normal para o backend
 */

document.addEventListener('DOMContentLoaded', () => {
  const form = document.querySelector('.formulario');
  if (!form) return;

  // Regex simples para e-mail
  const emailRegex = /^[^@\s]+@[^@\s]+\.[^@\s]+$/;

  const fields   = Array.from(form.querySelectorAll('input[required], select[required]'));
  const checkbox = form.querySelector('input[type="checkbox"][required]');

  // 1) Remove mensagens antigas enquanto o usuário digita/muda valor
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

  // 2) Submissão: apenas previne se houver erro; caso contrário, permite o envio
  form.addEventListener('submit', function (e) {
    let isValid = true;

    // limpa erros antigos
    form.querySelectorAll('.error-message').forEach(el => el.remove());

    // 2.1) Validação de e-mail
    const emailField = form.querySelector('input[name="email"]');
    if (emailField && !emailRegex.test(emailField.value.trim())) {
      isValid = false;
      const container = emailField.closest('.input-box');
      container.appendChild(createErrorMsg("E-mail inválido."));
    }

    // 2.2) Validação de senha mínima
    const pwdField = form.querySelector('input[name="senha"]');
    if (pwdField && pwdField.value.trim().length < 6) {
      isValid = false;
      const container = pwdField.closest('.input-box');
      container.appendChild(createErrorMsg("Senha deve ter ao menos 6 caracteres."));
    }

    // 2.3) checa inputs e selects obrigatórios
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

    // 2.4) checa checkbox
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
    // se isValid == true, NÃO chamamos preventDefault:
    // o form submeterá normalmente ao backend
  });

  // agora recebe texto customizado opcionalmente
  function createErrorMsg(text = "Este campo é obrigatório.") {
    const msg = document.createElement('div');
    msg.className = 'error-message';
    msg.textContent = text;
    return msg;
  }
});
