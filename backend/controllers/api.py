# backend/controllers/api.py

from flask import Blueprint, jsonify, request, session
from backend.utils.db import conectar

# Blueprint único para todas as rotas de API (places e XP)
api = Blueprint('api', __name__, url_prefix='/api')

@api.route('/places', methods=['GET'])
def get_places():
    conn = conectar()
    cur  = conn.cursor()
    cur.execute("""
      SELECT
        p.id,
        p.title,
        p.category,
        p.img_url       AS "imgUrl",
        p.address,
        p.lat,
        p.lng,
        -- total de avaliações definidas em ratings
        COUNT(r.*)                       AS reviews,
        -- média de score arredondada para inteiro (1–5)
        COALESCE(ROUND(AVG(r.score))::INT, 0) AS rating,
        p.features
      FROM places p
      LEFT JOIN ratings r ON r.place_id = p.id
      GROUP BY p.id
      ORDER BY p.title;
    """)
    cols = [d.name for d in cur.description]
    data = [dict(zip(cols, row)) for row in cur.fetchall()]
    cur.close()
    conn.close()
    return jsonify(data)

@api.route('/user_stats/xp', methods=['POST'])
def update_xp():
    # Garante que o usuário está logado
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({'error': 'Não autenticado'}), 401

    body = request.get_json() or {}
    xp = int(body.get('xp', 0))

    conn = conectar()
    cur  = conn.cursor()

    # Upsert: cria stats se não existir, ou atualiza total_xp e aumenta quiz_count em 1
    cur.execute("""
      INSERT INTO user_stats (user_id, total_xp, quiz_count, places_count)
      VALUES (%s, %s, 1, 0)
      ON CONFLICT (user_id) DO UPDATE
        SET total_xp   = user_stats.total_xp + EXCLUDED.total_xp,
            quiz_count = user_stats.quiz_count + 1;
    """, (user_id, xp))

    # Retorna estatísticas atualizadas
    cur.execute("""
      SELECT total_xp, quiz_count, places_count
      FROM user_stats
      WHERE user_id = %s
    """, (user_id,))
    total_xp, quiz_count, places_count = cur.fetchone()

    conn.commit()
    cur.close()
    conn.close()

    return jsonify({
      'total_xp': total_xp,
      'quiz_count': quiz_count,
      'places_count': places_count
    })
