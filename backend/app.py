import os
from dotenv import load_dotenv
from flask import Flask, render_template, session, redirect, url_for
from backend.utils.db import conectar
from backend.controllers.auth import auth_bp

def create_app():
    load_dotenv()

    app = Flask(
        __name__,
        template_folder=os.path.join("..", "frontend", "templates"),
        static_folder=os.path.join("..", "frontend", "static")
    )

    app.secret_key = os.getenv("SECRET_KEY", "troque_em_producao")
    app.register_blueprint(auth_bp, url_prefix="/auth")

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

    @app.route("/menu/puzzle", methods=["GET"])
    def puzzle():
        return render_template("menu/puzzle.html")

    # Quiz routes
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

    # Perfil routes
    @app.route("/perfil", methods=["GET"])
    def perfil():
        return render_template("perfil/home-perfil.html")

    @app.route("/perfil/follower", methods=["GET"])
    def perfil_follower():
        return render_template("perfil/follower.html")

    @app.route("/perfil/atividade", methods=["GET"])
    def perfil_atividade():
        return render_template("perfil/atividade-perfil.html")

    # Menu/Profile subroutes
    @app.route("/menu/perfil", methods=["GET"])
    def perfil_overview():
        return render_template("menu/profile_overview.html")

    @app.route("/menu/locais", methods=["GET"])
    def locais():
        return render_template("menu/locais.html")

    @app.route("/menu/lojas", methods=["GET"])
    def lojas():
        return render_template("menu/lojas.html")

    @app.route("/menu/perfil/comentarios", methods=["GET"])
    def perfil_comments():
        comments = [
            {
                'user_avatar': 'avatar1.jpg',
                'place_name':  'Rede Andrade Hangar Hotel',
                'text':        'Achei o lugar muito confortável e agradável...',
                'place_img':   'hotel1.jpg'
            },
        ]
        return render_template("menu/profile_comments.html", comments=comments)

    @app.route("/menu/perfil/seguindo", methods=["GET"])
    def perfil_follows():
        follows = [
            {'avatar': 'renata.jpg', 'name': 'Renata Cariana', 'subtitle': 'Paraense'},
            {'avatar': 'olivia.jpg', 'name': 'Olivia Marquês', 'subtitle': 'Americana'},
        ]
        return render_template("menu/profile_follows.html", follows=follows)

    @app.errorhandler(404)
    def not_found(e):
        return render_template("404.html"), 404

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
