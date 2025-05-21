// static/js/places.js

// garante que PLACES exista antes de iniciar
window.PLACES = null;

document.addEventListener('DOMContentLoaded', async () => {
  try {
    // 1) busca o array direto do endpoint Flask
    const resp = await fetch('/api/places');
    if (!resp.ok) throw new Error(`HTTP ${resp.status}`);
    let places = await resp.json();

    // 2) normaliza cada imgUrl e limpa as features
    places = places.map(p => {
      // --- normaliza url da imagem ---
      let url = null;
      if (
        p.imgUrl &&
        typeof p.imgUrl === 'string' &&
        p.imgUrl.trim() !== ''
      ) {
        url = p.imgUrl.startsWith('/')
          ? p.imgUrl
          : `/static/${p.imgUrl.replace(/^\/+/, '')}`;
      }

      // --- limpa bullets/pontos iniciais em cada feature ---
      const featuresClean = Array.isArray(p.features)
        ? p.features.map(f =>
            f
              // remove • · – - . e quaisquer símbolos/pontos/espaços iniciais
              .replace(/^[\u2022\u00B7\.\-\–\s]+/, '')
              .trim()
          )
        : [];

      return {
        ...p,
        imgUrl: url,
        features: featuresClean
      };
    });

    // 3) expõe globalmente e sinaliza que está pronto
    window.PLACES = places;
    document.dispatchEvent(new Event('placesReady'));
  } catch (err) {
    console.error('Erro ao carregar /api/places', err);
  }
});
