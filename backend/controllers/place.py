# backend/controllers/place.py
import os
import json
import traceback
from datetime import datetime
from flask import Blueprint, jsonify, request, session, url_for, current_app as app
from dotenv import load_dotenv

from backend.utils.db import conectar
from backend.controllers.profile import login_required

# ————— Configuração do CrewAI + Gemini —————
from crewai import Crew, Agent, Task, Process, LLM

# Carrega variáveis do .env
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Instância do LLM Gemini
gemini_llm = LLM(
    model="gemini/gemini-1.5-flash",
    api_key=GEMINI_API_KEY,
    temperature=0.0
)

# Agente de recomendação
recommend_agent = Agent(
    role="Recomendador Inteligente de Lojas",
    goal="Ordenar lojas considerando distância e rating",
    backstory="Você sugere as melhores lojas",
    llm=gemini_llm,
    verbose=False
)

# Tarefa do agente com schema de output
recommend_task = Task(
    description="""
    Você recebeu:
    - preferences: lista de categorias que o usuário prefere (vazia = sem preferência).
    - stores: lista de objetos com {id, name, categories, distance_km, rating}.

    **Se preferences estiver vazio**, retorne **todas** as stores ordenadas por:
      1. Menor distance_km
      2. Maior rating
    **Se preferences não estiver vazio**, ordene por:
      1. Quantidade de categorias em comum com preferences (maior primeiro)
      2. Menor distance_km
      3. Maior rating

    Retorne APENAS um JSON válido:
    {
      "sorted_stores": [
        { "id": 1, "name": "Loja X", "categories": [...], "distance_km": 1.23, "rating": 4.5 },
        ...
      ]
    }
    """,
    agent=recommend_agent,
    expected_output=json.dumps({
        "type": "object",
        "properties": {
            "sorted_stores": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "id":           { "type": "number" },
                        "name":         { "type": "string" },
                        "categories":   { "type": "array", "items": { "type": "string" } },
                        "distance_km":  { "type": "number" },
                        "rating":       { "type": "number" }
                    },
                    "required": ["id","name","categories","distance_km","rating"]
                }
            }
        },
        "required": ["sorted_stores"]
    })
)

# Crew que roda a tarefa
recommend_crew = Crew(
    agents=[recommend_agent],
    tasks=[recommend_task],
    process=Process.sequential,
    verbose=False
)
# ——————————————————————————————————————————————

place_bp = Blueprint('place', __name__, url_prefix='/api/places')

# Obtém dados completos de um place
def get_place_data(place_id: int) -> dict:
    conn = conectar()
    cur = conn.cursor()
    cur.execute("""
        SELECT
            p.id, p.title, p.category, p.img_url, p.address,
            p.phone, p.hours, p.price, p.lat, p.lng, p.about,
            COALESCE(r.count_reviews, 0) AS reviews,
            COALESCE(r.avg_rating, 0)  AS rating,
            p.features
        FROM places p
        LEFT JOIN (
            SELECT place_id,
                   COUNT(*) AS count_reviews,
                   ROUND(AVG(score)::numeric, 1) AS avg_rating
            FROM ratings
            WHERE place_id = %s
            GROUP BY place_id
        ) r ON r.place_id = p.id
        WHERE p.id = %s;
    """, (place_id, place_id))
    row = cur.fetchone()
    cur.close()
    conn.close()
    if not row:
        return {}

    cols = [
        'id', 'title', 'category', 'img_url', 'address',
        'phone', 'hours', 'price', 'lat', 'lng', 'about',
        'reviews', 'rating', 'features'
    ]
    place = dict(zip(cols, row))

    feats = place.get('features')
    if isinstance(feats, str):
        try:
            place['features'] = json.loads(feats)
        except json.JSONDecodeError:
            place['features'] = [feats]
    elif feats is None:
        place['features'] = []

    conn = conectar()
    cur = conn.cursor()
    cur.execute("""
        SELECT u.nome, u.avatar_url, r.score, r.comment
          FROM ratings r
          JOIN usuarios u ON u.id = r.user_id
         WHERE r.place_id = %s
      ORDER BY r.created_at DESC;
    """, (place_id,))
    reviews = cur.fetchall()
    cur.close()
    conn.close()

    reviews_list = []
    for user_name, avatar_url, score, comment in reviews:
        base = avatar_url.split('/')[-1] if avatar_url else 'avatar1'
        name = base.split('.')[0]
        svg_name = f"{name}.svg"
        avatar_full_url = url_for('static', filename='icons/' + svg_name)
        reviews_list.append({
            'user_name': user_name,
            'user_avatar_url': avatar_full_url,
            'score': score,
            'comment': comment
        })
    place['reviews_list'] = reviews_list
    place['reviews_text'] = reviews_list[0]['comment'] if reviews_list else None
    return place

@place_bp.route('/<int:place_id>', methods=['GET'])
def api_get_place(place_id):
    data = get_place_data(place_id)
    if not data:
        return jsonify({'error': 'Place not found'}), 404
    return jsonify(data)

@place_bp.route('/<int:place_id>/reviews', methods=['POST'])
@login_required
def api_post_review(place_id):
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({'error': 'Usuário não autenticado'}), 401
    data = request.get_json() or request.form
    try:
        score = int(data.get('score'))
        comment = data.get('comment', '').strip()
    except (TypeError, ValueError):
        return jsonify({'error': 'Dados inválidos'}), 400
    if score < 1 or score > 5 or not comment:
        return jsonify({'error': 'Nota ou comentário inválido'}), 400

    conn = conectar()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO ratings (user_id, place_id, score, comment, created_at)
        VALUES (%s, %s, %s, %s, %s)
        ON CONFLICT (user_id, place_id)
          DO UPDATE SET
            score      = EXCLUDED.score,
            comment    = EXCLUDED.comment,
            created_at = EXCLUDED.created_at
        RETURNING id;
    """, (user_id, place_id, score, comment, datetime.utcnow()))
    conn.commit()
    new_id = cur.fetchone()[0]
    cur.close()
    conn.close()
    return jsonify({'success': True, 'review_id': new_id}), 201

@place_bp.route('/recommend', methods=['POST'])
def api_recommend_places():
    try:
        data = request.get_json()
        prefs = data.get('preferences', [])
        stores = data.get('stores', [])

        # Só chama CrewAI se houver filtro
        if prefs:
            execution = recommend_crew.kickoff(inputs={
                "preferences": prefs,
                "stores":      stores
            })
            # extrai JSON da IA
            try:
                if getattr(execution, 'json_dict', None):
                    result = execution.json_dict
                else:
                    raw = getattr(execution, 'output', str(execution))
                    idx = raw.find('{')
                    result = json.loads(raw[idx:])
                # Se IA devolver vazio, força fallback:
                if not result.get('sorted_stores'):
                    raise ValueError("IA retornou vazio")
            except Exception as ai_err:
                app.logger.warning("IA falhou (%s), usando fallback local", ai_err)
                # fallback local: mescla stores originais já ordenados
                sorted_list = sorted(
                    stores,
                    key=lambda x: (x['distance_km'], -x['rating'])
                )
                result = {"sorted_stores": sorted_list}
        else:
            # sem filtro: fallback local direto
            sorted_list = sorted(
                stores,
                key=lambda x: (x['distance_km'], -x['rating'])
            )
            result = {"sorted_stores": sorted_list}

        return jsonify({"status": "success", "result": result})
    except Exception as e:
        app.logger.exception("Erro em /api/places/recommend")
        return jsonify({"status": "error", "message": str(e)}), 500
