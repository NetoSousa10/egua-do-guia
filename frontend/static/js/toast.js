// toast.js
/**
 * Exibe um toast de informação ou erro.
 * @param {string} message — texto do toast.
 * @param {object} [options]
 * @param {'info'|'error'} [options.type='info'] — estilo do toast.
 * @param {number} [options.duration=4000] — duração em ms.
 */
function showToast(message, { type = 'info', duration = 4000 } = {}) {
  let container = document.getElementById('toast-container');
  if (!container) {
    container = document.createElement('div');
    container.id = 'toast-container';
    document.body.appendChild(container);
  }

  const toast = document.createElement('div');
  toast.className = `toast toast--${type}`;
  toast.innerHTML = `
    <span class="toast__icon">${type === 'error' ? '❌' : '✅'}</span>
    <span class="toast__msg">${message}</span>
  `;
  container.appendChild(toast);

  // dispara fade‑out via CSS custom property de duração
  toast.style.setProperty('--toast-duration', `${duration}ms`);

  // remove do DOM após terminar a animação
  setTimeout(() => toast.remove(), duration + 500);
}

window.showToast = showToast;
