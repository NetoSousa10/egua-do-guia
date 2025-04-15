from flask import Flask, render_template
from backend.controllers.auth import auth_bp
from backend.controllers.lugares import lugares_bp
import os

def create_app():
    app = Flask(
        __name__,
        template_folder=os.path.join("..", "frontend", "templates"),
        static_folder=os.path.join("..", "frontend", "static")
    )
    
    app.config.from_pyfile("config.py", silent=True)

    # Registrar blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(lugares_bp)

    # Rota da splash screen
    @app.route("/splash", methods=["GET"])
    def splash():
        return render_template("login/splash.html")
    
    @app.route("/start", methods=["GET"])
    def login_start():
        return render_template("login/login_start.html")

    @app.route("/cadastro", methods=["GET"])
    def cadastro_form():
        return render_template("login/cadastro.html")  # HTML com o formulário

    # Rota do tutorial
    @app.route("/tutorial", methods=["GET"])
    def tutorial():
        return render_template("tutorial/tutorial.html")
    
    @app.route('/tutorial/etapa2', methods=["GET"])
    def tutorial_etapa2():
        return render_template('tutorial/tutorial_etapa2.html')
    
    @app.route('/tutorial/etapa3', methods=["GET"])
    def tutorial_etapa3():
        return render_template('tutorial/tutorial_etapa3.html')

    @app.route('/tutorial/etapa4', methods=["GET"])
    def tutorial_etapa4():
        return render_template('tutorial/tutorial_etapa4.html')
    
    @app.route("/tutorial/etapa5", methods=["GET"])
    def tutorial_etapa5():
        return render_template("tutorial/tutorial_etapa5.html")

    @app.route("/reward", methods=["GET"])
    def reward():
        return render_template("reward.html")
    
    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
