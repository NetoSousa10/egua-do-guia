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
        return render_template("tutorial/tutorial.html")
    
    @app.route('/tutorial/etapa2')
    def tutorial_etapa2():
        return render_template('tutorial/tutorial_etapa2.html')
    
    @app.route('/tutorial/etapa3')
    def tutorial_etapa3():
        return render_template('tutorial/tutorial_etapa3.html')

    @app.route('/tutorial/etapa4')
    def tutorial_etapa4():
        return render_template('tutorial/tutorial_etapa4.html')
    
    @app.route("/tutorial/etapa5")
    def tutorial_etapa5():
        return render_template("tutorial/tutorial_etapa5.html")

    @app.route("/reward")
    def reward():
        return render_template("reward.html")
    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
