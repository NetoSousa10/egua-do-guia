# backend/app.py
import os
from functools import wraps
from dotenv import load_dotenv
from flask import (
    Flask, render_template, jsonify, session, redirect,
    url_for, send_from_directory, request
)
from backend.utils.db import conectar
from backend.controllers.auth import auth_bp
from backend.controllers.api import api as api_bp   # Blueprint unificado com /api/routes

# Define caminhos absolutos
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FRONTEND_DIR = os.path.join(BASE_DIR, '..', 'frontend')

# Inicializa o Flask com caminhos absolutos para templates e estáticos
app = Flask(
    __name__,
    template_folder=os.path.join(FRONTEND_DIR, 'templates'),
    static_folder=os.path.join(FRONTEND_DIR, 'static'),
    static_url_path='/static'
)

def login_required(f):
    """Decorator para exigir sessão ativa."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('user_id'):
            return redirect(url_for('login_form'))
        return f(*args, **kwargs)
    return decorated_function

@app.after_request
def add_no_cache_headers(response):
    """Evita cache das páginas protegidas."""
    response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, public, max-age=0'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    return response

def create_app():
    load_dotenv()
    app.secret_key = os.getenv("SECRET_KEY", "troque_em_producao")

    # ——— Autenticação ———
    app.register_blueprint(auth_bp, url_prefix="/auth")

    # ——— Todas as rotas de API ———
    app.register_blueprint(api_bp)

    # ——— Rotas públicas ———
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
    # Se já estiver logado, redireciona
        if session.get('user_id'):
            return redirect(url_for('home'))
        return render_template("login/login.html")


    @app.route("/logout")
    @login_required
    def logout():
        session.clear()
        return redirect(url_for('login_form'))

    # ——— Tutorial (protegido) ———
    @app.route("/tutorial", methods=["GET"])
    @login_required
    def tutorial():
        return render_template("tutorial/tutorial.html")

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

    @app.route("/reward", methods=["GET"])
    @login_required
    def reward():
        return render_template("reward.html")

    # ——— Menu principal (protegido) ———
    @app.route("/menu/home", methods=["GET"])
    @login_required
    def home():
        return render_template("menu/home.html")

    @app.route("/menu/puzzle", methods=["GET"])
    @login_required
    def puzzle():
        return render_template("menu/puzzle.html")

    @app.route("/menu/locais", methods=["GET"])
    @login_required
    def locais():
        return render_template("menu/locais.html")

    @app.route("/menu/lojas", methods=["GET"])
    @login_required
    def lojas():
        return render_template("menu/lojas.html")

    # ——— Quiz (protegido) ———
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

    # ——— Perfil (protegido) ———
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

    # ——— Menu ➔ Perfil (protegido) ———
    @app.route("/menu/perfil", methods=["GET"])
    @login_required
    def perfil_overview():
        return render_template("menu/profile_overview.html")

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
            {
                'place_name': row[0],
                'place_img':  row[1],
                'text':       row[2],
                'date':       row[3].strftime("%d/%m/%Y %H:%M")
            }
            for row in cur.fetchall()
        ]
        cur.close()
        conn.close()
        return render_template("menu/profile_comments.html", comments=comments)

    @app.route("/menu/perfil/seguindo", methods=["GET"])
    @login_required
    def perfil_follows():
        user_id = session['user_id']
        conn = conectar()
        cur  = conn.cursor()
        cur.execute("""
          SELECT u.id,
                 u.nome          AS name,
                 u.nacionalidade AS subtitle
            FROM followers f
            JOIN usuarios u ON u.id = f.followee_id
           WHERE f.follower_id = %s
        ORDER BY u.nome;
        """, (user_id,))
        follows = [
            {'id': row[0], 'name': row[1], 'subtitle': row[2]}
            for row in cur.fetchall()
        ]
        cur.close()
        conn.close()
        return render_template("menu/profile_follows.html", follows=follows)

    # ——— PWA: exposição do SW e do manifest （público） ———
    @app.route('/service-worker.js')
    def service_worker():
        return send_from_directory(app.static_folder, 'service-worker.js')

    @app.route('/manifest.json')
    def manifest():
        return send_from_directory(
            app.static_folder, 'manifest.json',
            mimetype='application/manifest+json'
        )

    @app.errorhandler(404)
    def not_found(e):
        return render_template("404.html"), 404

    return app

if __name__ == "__main__":
    create_app().run(debug=True)
