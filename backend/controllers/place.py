# backend/controllers/place.py

from flask import Blueprint, jsonify, request, session
from backend.utils.db import conectar
from backend.controllers.profile import login_required
import json
from datetime import datetime

place_bp = Blueprint('place', __name__, url_prefix='/api/places')


def get_place_data(place_id: int) -> dict:
    """
    Consulta no banco os dados de um place específico, incluindo:
      - Campos principais de places (id, title, category, img_url, address, phone, hours, price, lat, lng, about)
      - Contagem e média de ratings
      - Lista de features
      - Lista de avaliações completas (comentário, nota, usuário, avatar com fallback)
    Retorna um dicionário pronto para Jinja ou JSON.
    """
    conn = conectar()
    cur = conn.cursor()

    # 1) Busca dados gerais + média e contagem de avaliações
    cur.execute("""
        SELECT
            p.id,
            p.title,
            p.category,
            p.img_url,
            p.address,
            p.phone,
            p.hours,
            p.price,
            p.lat,
            p.lng,
            p.about,
            COALESCE(r.count_reviews, 0)    AS reviews,
            COALESCE(r.avg_rating, 0)       AS rating,
            p.features
        FROM places p
        LEFT JOIN (
            SELECT
                place_id,
                COUNT(*)             AS count_reviews,
                ROUND(AVG(score)::numeric, 1) AS avg_rating
            FROM ratings
            WHERE place_id = %s
            GROUP BY place_id
        ) AS r ON r.place_id = p.id
        WHERE p.id = %s;
    """, (place_id, place_id))
    row = cur.fetchone()
    if not row:
        cur.close()
        conn.close()
        return {}

    cols = [
        'id', 'title', 'category', 'img_url', 'address',
        'phone', 'hours', 'price',
        'lat', 'lng', 'about',
        'reviews', 'rating', 'features'
    ]
    place = dict(zip(cols, row))

    # Garante que features seja lista Python
    feats = place.get('features')
    if isinstance(feats, str):
        try:
            place['features'] = json.loads(feats)
        except json.JSONDecodeError:
            place['features'] = [feats]
    elif feats is None:
        place['features'] = []

    # 2) Busca lista completa de avaliações (comentários) juntando com 'usuarios'
    cur.execute("""
        SELECT u.nome       AS user_name,
               u.avatar_url AS user_avatar_url,
               r.score,
               r.comment
          FROM ratings r
          JOIN usuarios u
            ON u.id = r.user_id
         WHERE r.place_id = %s
      ORDER BY r.created_at DESC;
    """, (place_id,))
    reviews = cur.fetchall()
    cur.close()
    conn.close()

    # 3) Monta a lista de reviews, aplicando fallback 'avatar1.png' quando necessário
    place['reviews_list'] = [
        {
            'user_name':       r[0],
            'user_avatar_url': r[1] or 'avatar1.png',
            'score':           r[2],
            'comment':         r[3]
        }
        for r in reviews
    ]

    # Comentário mais recente como texto de destaque
    place['reviews_text'] = place['reviews_list'][0]['comment'] if place['reviews_list'] else None

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
    # Upsert para evitar duplicação de avaliações
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
