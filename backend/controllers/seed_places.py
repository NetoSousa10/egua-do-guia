# backend/controllers/seed_places.py

from pathlib import Path
import json
from backend.utils.db import conectar

def seed_places():
    # 1) Conecta
    conn = conectar()
    if conn is None:
        print("🚫 Sem conexão, abortando.")
        return
    cur = conn.cursor()

    # 2) Acha o JSON
    project_root = Path(__file__).parents[2]
    json_path    = project_root / 'frontend' / 'static' / 'data' / 'places.json'

    print(f"🔍 Carregando JSON de: {json_path}")
    if not json_path.exists():
        print("❌ Arquivo não existe:", json_path)
        return

    # 3) Lê tudo
    with json_path.open(encoding='utf-8') as f:
        places = json.load(f)

    # 4) Insere no banco, agora incluindo features
    for p in places:
        cur.execute("""
            INSERT INTO places
              (title, category, img_url, address, phone,
               price, hours, rating, reviews, features, lat, lng)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (title) DO UPDATE
              SET
                category = EXCLUDED.category,
                img_url  = EXCLUDED.img_url,
                address  = EXCLUDED.address,
                phone    = EXCLUDED.phone,
                price    = EXCLUDED.price,
                hours    = EXCLUDED.hours,
                rating   = EXCLUDED.rating,
                reviews  = EXCLUDED.reviews,
                features = EXCLUDED.features,
                lat      = EXCLUDED.lat,
                lng      = EXCLUDED.lng;
        """, (
            p['title'],
            p['category'],
            p['imgUrl'],
            p.get('address'),
            p.get('phone'),
            p.get('price'),
            p.get('hours'),
            p.get('rating'),
            p.get('reviews'),
            p.get('features', []),
            p['lat'],
            p['lng'],
        ))

    conn.commit()
    cur.close()
    conn.close()
    print("✅ Places semeados com sucesso.")

if __name__ == '__main__':
    seed_places()
