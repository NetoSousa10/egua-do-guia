// static/js/places.js

// garante que PLACES exista antes de iniciar
window.PLACES = null;

document.addEventListener('DOMContentLoaded', async () => {
  try {
    // 1) busca o array direto do endpoint Flask
    const resp = await fetch('/api/places');
    if (!resp.ok) throw new Error(`HTTP ${resp.status}`);
    let places = await resp.json();

    // 2) normaliza cada imgUrl:
    //    - se veio do banco e não é string vazia, garante que comece com '/'
    //    - se não veio, deixa null (para não renderizar imagem)
    places = places.map(p => {
      let url = null;
      if (p.imgUrl && typeof p.imgUrl === 'string' && p.imgUrl.trim() !== '') {
        url = p.imgUrl.startsWith('/')
          ? p.imgUrl
          : `/static/${p.imgUrl.replace(/^\/+/, '')}`;
      }
      return {
        ...p,
        imgUrl: url
      };
    });

    // 3) expõe globalmente e sinaliza que está pronto
    window.PLACES = places;
    document.dispatchEvent(new Event('placesReady'));
  } catch (err) {
    console.error('Erro ao carregar /api/places', err);
  }
});
