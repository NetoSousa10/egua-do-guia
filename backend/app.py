# backend/app.py
import os
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

# Configura o Flask com caminhos absolutos para templates e estáticos
app = Flask(
    __name__,
    template_folder=os.path.join(FRONTEND_DIR, 'templates'),
    static_folder=os.path.join(FRONTEND_DIR, 'static'),
    static_url_path='/static'   # mantém /static para todos os assets
)

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
        return render_template("login/login_start.html")

    @app.route("/cadastro", methods=["GET"])
    def cadastro_form():
        return render_template("login/cadastro.html")

    @app.route("/login", methods=["GET"])
    def login_form():
        return render_template("login/login.html")

    # ——— Tutorial ———
    @app.route("/tutorial", methods=["GET"])
    def tutorial():
        return render_template("tutorial/tutorial.html")

    @app.route("/tutorial/etapa2", methods=["GET"])
    def tutorial_etapa2():
        return render_template("tutorial/tutorial_etapa2.html")

    @app.route("/tutorial/etapa3", methods=["GET"])
    def tutorial_etapa3():
        return render_template("tutorial/tutorial_etapa3.html")

    @app.route("/tutorial/etapa4", methods=["GET"])
    def tutorial_etapa4():
        return render_template("tutorial/tutorial_etapa4.html")

    @app.route("/tutorial/etapa5", methods=["GET"])
    def tutorial_etapa5():
        return render_template("tutorial/tutorial_etapa5.html")

    @app.route("/reward", methods=["GET"])
    def reward():
        return render_template("reward.html")

    # ——— Menu principal ———
    @app.route("/menu/home", methods=["GET"])
    def home():
        return render_template("menu/home.html")

    @app.route("/menu/puzzle", methods=["GET"])
    def puzzle():
        return render_template("menu/puzzle.html")

    @app.route("/menu/locais", methods=["GET"])
    def locais():
        return render_template("menu/locais.html")

    @app.route("/menu/lojas", methods=["GET"])
    def lojas():
        return render_template("menu/lojas.html")

    # ——— Quiz ———
    @app.route("/quiz/festivais", methods=["GET"])
    def quiz_festivais():
        return render_template("quiz/festivais.html")

    @app.route("/quiz/musical", methods=["GET"])
    def quiz_musical():
        return render_template("quiz/musical.html")

    @app.route("/quiz/folclore", methods=["GET"])
    def quiz_folclore():
        return render_template("quiz/folclore.html")

    @app.route("/quiz/artesanato", methods=["GET"])
    def quiz_artesanato():
        return render_template("quiz/artesanato.html")

    @app.route("/quiz/maritima", methods=["GET"])
    def quiz_maritima():
        return render_template("quiz/maritima.html")

    @app.route("/quiz/peixes", methods=["GET"])
    def quiz_peixes():
        return render_template("quiz/peixes.html")

    @app.route("/quiz/frutas", methods=["GET"])
    def quiz_frutas():
        return render_template("quiz/frutas.html")

    @app.route("/quiz/teatros", methods=["GET"])
    def quiz_teatros():
        return render_template("quiz/teatros.html")

    @app.route("/quiz/bairros", methods=["GET"])
    def quiz_bairros():
        return render_template("quiz/bairros.html")

    # ——— Perfil ———
    @app.route("/perfil", methods=["GET"])
    def perfil():
        return render_template("perfil/home-perfil.html")

    @app.route("/perfil/follower", methods=["GET"])
    def perfil_follower():
        return render_template("perfil/follower.html")

    @app.route("/perfil/atividade", methods=["GET"])
    def perfil_atividade():
        return render_template("perfil/atividade-perfil.html")

    # ——— Menu ➔ Perfil ———
    @app.route("/menu/perfil", methods=["GET"])
    def perfil_overview():
        return render_template("menu/profile_overview.html")

    @app.route("/menu/perfil/comentarios", methods=["GET"])
    def perfil_comments():
        user_id = session.get('user_id')
        if not user_id:
            return redirect(url_for('login_form'))

        conn = conectar()
        cur  = conn.cursor()
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
    def perfil_follows():
        user_id = session.get('user_id')
        if not user_id:
            return redirect(url_for('login_form'))

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

    # ——— PWA: exposição do SW e do manifest na raiz ———
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
