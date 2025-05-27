# backend/controllers/profile.py

from flask import Blueprint, render_template, session, request, jsonify, redirect, url_for, current_app
from functools import wraps
from werkzeug.utils import secure_filename
from backend.utils.db import conectar
import os

# Decorator de login
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
    user = {"name": row[0], "avatar": row[1]}  # avatar será só 'arquivo.svg' ou None

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
    """
    Aceita:
      1) JSON { "avatar": "icons/nome.svg" } vindo do modal de seleção;
      2) multipart/form-data com campo 'avatar' para upload de arquivo.
    """
    user_id = session['user_id']

    # --- Caso JSON vindo do modal (avatar já existente em static/icons/) ---
    if request.is_json:
        data = request.get_json(force=True) or {}
        avatar = data.get('avatar')  # ex: "icons/trophy-ouro.svg"
        if not avatar:
            return jsonify({'error': 'Nenhum avatar informado no JSON'}), 400

        # Extrai só o nome do arquivo
        filename = avatar.split('/')[-1]

        try:
            conn = conectar()
            cur = conn.cursor()
            cur.execute(
                "UPDATE usuarios SET avatar_url = %s WHERE id = %s",
                (filename, user_id)
            )
            conn.commit()
            cur.close()
            conn.close()
        except Exception as e:
            return jsonify({'error': 'Falha ao atualizar avatar no banco', 'detail': str(e)}), 500

        avatar_url = url_for('static', filename='icons/' + filename)
        return jsonify({'status': 'ok', 'avatar_url': avatar_url}), 200

    # --- Caso upload de arquivo via form ---
    if 'avatar' not in request.files:
        return jsonify({'error': 'Nenhum arquivo de avatar enviado'}), 400

    avatar_file = request.files['avatar']
    if avatar_file.filename == '':
        return jsonify({'error': 'Nome de arquivo inválido'}), 400

    # Gera nome seguro e salva no disco
    filename = secure_filename(f'user_{user_id}_' + avatar_file.filename)
    icons_dir = os.path.join(current_app.static_folder, 'icons')
    os.makedirs(icons_dir, exist_ok=True)
    avatar_file.save(os.path.join(icons_dir, filename))

    try:
        conn = conectar()
        cur = conn.cursor()
        cur.execute(
            "UPDATE usuarios SET avatar_url = %s WHERE id = %s",
            (filename, user_id)
        )
        conn.commit()
        cur.close()
        conn.close()
    except Exception as e:
        return jsonify({'error': 'Falha ao salvar no banco', 'detail': str(e)}), 500

    avatar_url = url_for('static', filename='icons/' + filename)
    return jsonify({'status': 'ok', 'avatar_url': avatar_url}), 200
