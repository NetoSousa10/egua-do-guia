# backend/controllers/profile.py

from flask import Blueprint, render_template, session, request, jsonify, redirect, url_for
from functools import wraps
from backend.utils.db import conectar

# Copia do seu decorator de app.py
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('user_id'):
            return redirect(url_for('login_form'))
        return f(*args, **kwargs)
    return decorated_function

profile_bp = Blueprint('profile', __name__, url_prefix='/profile')


@profile_bp.route('/', methods=['GET'])
@login_required
def overview():
    user_id = session['user_id']
    conn = conectar()
    cur = conn.cursor()

    # 1) Dados básicos
    cur.execute("SELECT nome, avatar_url FROM usuarios WHERE id = %s", (user_id,))
    row = cur.fetchone() or ("Usuário", None)
    user = {"name": row[0], "avatar": row[1]}

    # 2) Estatísticas
    cur.execute("SELECT COUNT(*) FROM visits WHERE user_id = %s", (user_id,))
    user["places_visited"] = cur.fetchone()[0]
    cur.execute("SELECT COUNT(*) FROM quiz_results WHERE user_id = %s", (user_id,))
    user["quiz_count"] = cur.fetchone()[0]
    cur.execute("SELECT COALESCE(SUM(xp),0) FROM quiz_results WHERE user_id = %s", (user_id,))
    user["total_xp"] = cur.fetchone()[0]

    # 3) Lugar favorito
    cur.execute("""
        SELECT p.title, p.img_url, COUNT(v.*) AS visits
          FROM visits v
          JOIN places p ON p.id = v.place_id
         WHERE v.user_id = %s
      GROUP BY p.id
      ORDER BY visits DESC
         LIMIT 1
    """, (user_id,))
    fav = cur.fetchone()
    if fav:
        user.update({
            "favorite_place":        fav[0],
            "favorite_place_img":    fav[1],
            "favorite_place_visits": fav[2]
        })
    else:
        user.update({
            "favorite_place":        None,
            "favorite_place_img":    None,
            "favorite_place_visits": 0
        })

    # 4) Comentários e rank
    cur.execute("SELECT COUNT(*) FROM comments WHERE user_id = %s", (user_id,))
    user["comments_count"] = cur.fetchone()[0]
    cur.execute("SELECT rank_name FROM user_ranks WHERE user_id = %s", (user_id,))
    rk = cur.fetchone()
    user["rank"] = rk[0] if rk else "—"

    cur.close()
    conn.close()

    return render_template("menu/profile_overview.html", user=user)


@profile_bp.route('/avatar', methods=['POST'])
@login_required
def update_avatar():
    """Recebe JSON { avatar: 'assets/img/foo.png' } e salva em usuarios.avatar_url."""
    user_id = session['user_id']
    data = request.get_json(force=True) or {}
    avatar = data.get('avatar')

    if not avatar:
        return jsonify({'error': 'Nenhum avatar informado'}), 400

    try:
        conn = conectar()
        cur = conn.cursor()
        cur.execute(
            "UPDATE usuarios SET avatar_url = %s WHERE id = %s",
            (avatar, user_id)
        )
        conn.commit()
        cur.close()
        conn.close()
        return jsonify({'status': 'ok', 'avatar': avatar}), 200

    except Exception as e:
        import traceback; traceback.print_exc()
        return jsonify({
            'error': 'Não foi possível atualizar o avatar',
            'detail': str(e)
        }), 500
