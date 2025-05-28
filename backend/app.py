# backend/app.py

import os
from functools import wraps
from datetime import datetime
from dotenv import load_dotenv
from flask import (
    Flask, render_template, jsonify, session, redirect,
    url_for, send_from_directory, request
)
from backend.utils.db import conectar
from backend.controllers.auth import auth_bp
from backend.controllers.api import api as api_bp
from backend.controllers.profile import profile_bp
from backend.controllers.store import store_bp
from backend.controllers.tutorial import tutorial_bp
from backend.controllers.place import place_bp, get_place_data
from backend.controllers.distance import distance_bp  # Blueprint para distância via Google API

# Caminhos absolutos
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FRONTEND_DIR = os.path.join(BASE_DIR, '..', 'frontend')

# Instancia o app Flask
app = Flask(
    __name__,
    template_folder=os.path.join(FRONTEND_DIR, 'templates'),
    static_folder=os.path.join(FRONTEND_DIR, 'static'),
    static_url_path='/static'
)

# ————— Desativa cache de arquivos estáticos —————
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

# ————— No-cache em todas as respostas —————
@app.after_request
def add_no_cache_headers(response):
    response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, public, max-age=0'
    response.headers['Pragma']        = 'no-cache'
    response.headers['Expires']       = '0'
    return response

# ————— Override do url_for para cache-busting automático —————
@app.context_processor
def override_url_for():
    return dict(url_for=dated_url_for)


def dated_url_for(endpoint, **values):
    if endpoint == 'static' and 'filename' in values:
        fn = values['filename']
        file_path = os.path.join(app.static_folder, fn)
        try:
            mtime = int(os.path.getmtime(file_path))
            values['v'] = mtime
        except OSError:
            pass
    return url_for(endpoint, **values)

# Decorator para rotas que exigem login
def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not session.get('user_id'):
            return redirect(url_for('login_form'))
        return f(*args, **kwargs)
    return decorated


def create_app():
    load_dotenv()
    app.secret_key = os.getenv("SECRET_KEY", "troque_em_producao")

    # ——— Registra blueprints ———
    app.register_blueprint(auth_bp,       url_prefix="/auth")
    app.register_blueprint(api_bp)
    app.register_blueprint(profile_bp)
    app.register_blueprint(store_bp)
    app.register_blueprint(tutorial_bp)
    app.register_blueprint(place_bp)
    app.register_blueprint(distance_bp,    url_prefix="/api/distance")

    # ——— Rotas públicas e protegidas ———
    @app.route("/", methods=["GET"])
    @app.route("/splash", methods=["GET"])
    def splash():
        return render_template("login/splash.html")

    @app.route("/start", methods=["GET"])
    def login_start():
        if session.get('user_id'):
            return redirect(url_for('home'))
        return render_template("login/login_start.html")

    @app.route("/cadastro", methods=["GET"])
    def cadastro_form():
        if session.get('user_id'):
            return redirect(url_for('home'))
        return render_template("login/cadastro.html")

    @app.route("/login", methods=["GET"])
    def login_form():
        if session.get('user_id'):
            return redirect(url_for('home'))
        return render_template("login/login.html")

    @app.route("/logout")
    @login_required
    def logout():
        session.clear()
        return redirect(url_for('login_form'))

    # ——— Tutorial ———
    @app.route("/tutorial", methods=["GET"])
    @login_required
    def tutorial():
        return render_template("tutorial/tutorial_etapa1.html")

    @app.route("/tutorial/etapa2", methods=["GET"])
    @login_required
    def tutorial_etapa2():
        return render_template("tutorial/tutorial_etapa2.html")

    @app.route("/tutorial/etapa3", methods=["GET"])
    @login_required
    def tutorial_etapa3():
        return render_template("tutorial/tutorial_etapa3.html")

    @app.route("/tutorial/etapa4", methods=["GET"])
    @login_required
    def tutorial_etapa4():
        return render_template("tutorial/tutorial_etapa4.html")

    @app.route("/tutorial/etapa5", methods=["GET"])
    @login_required
    def tutorial_etapa5():
        return render_template("tutorial/tutorial_etapa5.html")

    @app.route("/tutorial/etapa6", methods=["GET"])
    @login_required
    def tutorial_etapa6():
        return render_template("tutorial/tutorial_etapa6.html")

    @app.route("/reward", methods=["GET"])
    @login_required
    def reward():
        return render_template("reward.html")

    # ——— Menu principal ———

    @app.route("/menu/home", methods=["GET"])
    @login_required
    def home():
        # 1) busca todos os campos que você quer exibir:
        conn = conectar()
        cur = conn.cursor()
        cur.execute("""
            SELECT
              p.id,
              p.title,
              p.category,
              p.lat,
              p.lng,
              p.img_url,
              p.hours,
              p.address,
              p.phone,
              p.price,
              COALESCE(r.avg_rating, 0) AS rating
            FROM places p
            LEFT JOIN (
              SELECT place_id, ROUND(AVG(score)::numeric,1) AS avg_rating
              FROM ratings
              GROUP BY place_id
            ) r ON r.place_id = p.id;
        """)
        rows = cur.fetchall()
        cur.close()
        conn.close()

        # 2) monta o JSON completo (incluindo hours, address, phone, price)
        raw_places = [
            {
                "id": row[0],
                "name": row[1],
                "category": row[2],
                "lat": float(row[3]),
                "lng": float(row[4]),
                "img_url": row[5],
                "hours": row[6] or "",
                "address": row[7] or "",
                "phone": row[8] or "",
                "price": row[9] or "",
                "rating": float(row[10])
            }
            for row in rows
        ]

        # 3) injeta no template home.html
        return render_template(
            "menu/home.html",
            raw_places=raw_places
        )

    @app.route("/menu/puzzle", methods=["GET"])
    @login_required
    def puzzle():
        return render_template("menu/puzzle.html")

    # ——— Quiz ———
    @app.route("/quiz/festivais", methods=["GET"])
    @login_required
    def quiz_festivais():
        return render_template("quiz/festivais.html")

    @app.route("/quiz/musical", methods=["GET"])
    @login_required
    def quiz_musical():
        return render_template("quiz/musical.html")

    @app.route("/quiz/folclore", methods=["GET"])
    @login_required
    def quiz_folclore():
        return render_template("quiz/folclore.html")

    @app.route("/quiz/artesanato", methods=["GET"])
    @login_required
    def quiz_artesanato():
        return render_template("quiz/artesanato.html")

    @app.route("/quiz/maritima", methods=["GET"])
    @login_required
    def quiz_maritima():
        return render_template("quiz/maritima.html")

    @app.route("/quiz/peixes", methods=["GET"])
    @login_required
    def quiz_peixes():
        return render_template("quiz/peixes.html")

    @app.route("/quiz/frutas", methods=["GET"])
    @login_required
    def quiz_frutas():
        return render_template("quiz/frutas.html")

    @app.route("/quiz/teatros", methods=["GET"])
    @login_required
    def quiz_teatros():
        return render_template("quiz/teatros.html")

    @app.route("/quiz/bairros", methods=["GET"])
    @login_required
    def quiz_bairros():
        return render_template("quiz/bairros.html")

    # ——— Locais ———
    @app.route("/menu/locais", methods=["GET"])
    @login_required
    def locais():
        conn = conectar()
        cur = conn.cursor()
        cur.execute("""
            SELECT
              p.id, p.title, p.category, p.lat, p.lng, p.img_url,
              COALESCE(r.avg_rating, 0) AS rating
            FROM places p
            LEFT JOIN (
              SELECT place_id, ROUND(AVG(score)::numeric,1) AS avg_rating
              FROM ratings
              GROUP BY place_id
            ) r ON r.place_id = p.id;
        """
        )
        rows = cur.fetchall()
        cur.close()
        conn.close()

        raw_places = [
            {"id":row[0], "name":row[1], "categories":[row[2]],
             "lat":float(row[3]), "lng":float(row[4]),
             "img_url":row[5], "rating":float(row[6])}
            for row in rows
        ]

        return render_template(
            "menu/locais.html",
            raw_places=raw_places
        )

    @app.route("/menu/lojas", methods=["GET"])
    def lojas():
        return render_template("menu/lojas.html")

    # ——— Detalhes ———
    @app.route('/menu/detalhes/<int:place_id>', methods=['GET'])
    @login_required
    def detalhes(place_id):
        place = get_place_data(place_id)
        if not place:
            return render_template('404.html'), 404
        is_open = False
        hours = place.get('hours') or ""
        try:
            open_str, close_str = hours.split('–')
            now = datetime.now().time()
            open_t = datetime.strptime(open_str.strip(), "%H:%M").time()
            close_t= datetime.strptime(close_str.strip(), "%H:%M").time()
            is_open = open_t <= now <= close_t
        except:
            is_open = False
        return render_template(
            'menu/detalhes.html', place=place, is_open=is_open
        )

    # ——— Perfil ———
    @app.route("/perfil", methods=["GET"])
    @login_required
    def perfil():
        return render_template("perfil/home-perfil.html")

    @app.route("/perfil/follower", methods=["GET"])
    @login_required
    def perfil_follower():
        return render_template("perfil/follower.html")

    @app.route("/perfil/atividade", methods=["GET"])
    @login_required
    def perfil_atividade():
        return render_template("perfil/atividade-perfil.html")

    @app.route("/menu/perfil", methods=["GET"])
    @login_required
    def perfil_overview():
        user_id = session['user_id']
        conn = conectar()
        cur = conn.cursor()
        cur.execute("""
            SELECT name, avatar, places_count, quiz_count, total_xp,
                   comments_count, places_visited,
                   favorite_place, favorite_place_img,
                   favorite_place_visits, favorite_place_rating, rank
              FROM user_profile
             WHERE id = %s
        """, (user_id,))
        cols = [d[0] for d in cur.description]
        row = cur.fetchone() or [None]*len(cols)
        user = dict(zip(cols, row))
        cur.close()
        conn.close()
        return render_template("menu/profile_overview.html", user=user)

    @app.route("/menu/perfil/comentarios", methods=["GET"])
    @login_required
    def perfil_comments():
        user_id = session['user_id']
        conn = conectar()
        cur = conn.cursor()
        cur.execute("""
            SELECT p.title AS place_name,
                   p.img_url AS place_img,
                   c.content AS text,
                   c.criado_em
              FROM comments c
              JOIN places p ON p.id = c.place_id
             WHERE c.user_id = %s
          ORDER BY c.criado_em DESC;
        """, (user_id,))
        comments = [
            {'place_name':r[0], 'place_img':r[1], 'text':r[2], 'date':r[3].strftime("%d/%m/%Y %H:%M")} for r in cur.fetchall()
        ]
        cur.close()
        conn.close()
        return render_template("menu/profile_comments.html", comments=comments)

    # ——— PWA ———
    @app.route('/service-worker.js')
    def service_worker():
        return send_from_directory(app.static_folder, 'service-worker.js')

    @app.route('/manifest.json')
    def manifest():
        return send_from_directory(app.static_folder, 'manifest.json', mimetype='application/manifest+json')

    @app.errorhandler(404)
    def not_found(e):
        return render_template("404.html"), 404

    return app

if __name__ == "__main__":
    create_app().run(debug=True)
