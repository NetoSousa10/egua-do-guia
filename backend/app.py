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
    
    # Configurações (caso tenha .env com secret_key etc)
    app.config.from_pyfile("config.py", silent=True)

    # Registrar blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(lugares_bp)

    # Rota da splash screen
    @app.route("/splash")
    def splash():
        return render_template("splash.html")

    # Rota do tutorial
    @app.route("/tutorial")
    def tutorial():
        return render_template("tutorial.html")

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
