import os
from flask import Flask, render_template
from backend.controllers.auth import auth_bp
from backend.controllers.lugares import lugares_bp

def create_app():
    app = Flask(
        __name__,
        template_folder=os.path.join("..", "frontend", "templates"),
        static_folder=os.path.join("..", "frontend", "static")
    )

    # SECRET_KEY para sessões (troque por uma variável de ambiente em produção!)
    app.secret_key = os.environ.get("SECRET_KEY", "troque_isto_em_producao")

    # Registra blueprints de API com prefixos
    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(lugares_bp, url_prefix="/lugares")

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

    # Exemplo de handler de erro (opcional)
    @app.errorhandler(404)
    def not_found(e):
        return render_template("404.html"), 404

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
