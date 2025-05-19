document.addEventListener('DOMContentLoaded', () => {
  const banner = document.getElementById('activities-banner');
  const closeBtn = document.getElementById('banner-close-btn');
  const tabs = document.querySelectorAll('.tab-btn');
  const items = document.querySelectorAll('.activity-item');

  // Mostrar/ocultar banner
  if (localStorage.getItem('activitiesBannerClosed') === 'true') {
    banner.style.display = 'none';
  }
  closeBtn.addEventListener('click', () => {
    banner.style.display = 'none';
    localStorage.setItem('activitiesBannerClosed', 'true');
  });

  // função de filtragem
  function filterBy(tab) {
    const filtro = tab.dataset.tab;
    items.forEach(item => {
      item.style.display = item.dataset.tab === filtro ? 'flex' : 'none';
    });
  }

  // registra eventos de click
  tabs.forEach(tab => {
    tab.addEventListener('click', () => {
      tabs.forEach(t => t.classList.remove('active'));
      tab.classList.add('active');
      filterBy(tab);
    });
  });

  // filtra logo na inicialização, usando a aba já marcada como active
  const activeTab = document.querySelector('.tab-btn.active');
  if (activeTab) filterBy(activeTab);
  
});
