import os
from dotenv import load_dotenv
from flask import Flask, render_template, g, session, redirect, url_for
from backend.utils.db import conectar
from backend.controllers.auth   import auth_bp
from backend.controllers.lugares import lugares_bp

def create_app():
    load_dotenv()

    app = Flask(
        __name__,
        template_folder=os.path.join("..", "frontend", "templates"),
        static_folder=os.path.join("..", "frontend", "static")
    )

    app.secret_key = os.getenv("SECRET_KEY", "troque_em_producao")
    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(lugares_bp, url_prefix="/lugares")

    @app.before_request
    def check_profile_completion():
        g.profile_incomplete = False
        user_id = session.get('user_id')
        if user_id:
            conn = conectar()
            cur  = conn.cursor()
            cur.execute(
                "SELECT nacionalidade, genero FROM usuarios WHERE id = %s",
                (user_id,)
            )
            row = cur.fetchone()
            cur.close()
            conn.close()
            if row:
                nacional, genero = row
                if not nacional or not genero:
                    g.profile_incomplete = True

    # Rotas de GET só para renderizar templates
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

    @app.route("/menu/home", methods=["GET"])
    def home():
        return render_template("menu/home.html")

    # Exemplo de handler de erro (opcional)
    @app.errorhandler(404)
    def not_found(e):
        return render_template("404.html"), 404

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
