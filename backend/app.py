from flask import Flask
from dotenv import load_dotenv
import os
from backend.controllers.auth import auth_bp
from flask import Flask, render_template, redirect, url_for

load_dotenv()

from flask import Flask
import os

app = Flask(
    __name__,
    template_folder=os.path.join("..", "frontend", "templates"),
    static_folder=os.path.join("..", "frontend", "static")
)

app.secret_key = os.getenv("SECRET_KEY")
app.register_blueprint(auth_bp, url_prefix="/auth")

@app.route("/")
def home():
    return redirect(url_for("splash"))

@app.route("/splash")
def splash():
    return render_template("splash.html")

@app.route("/tutorial")
def tutorial():
    return render_template("tutorial.html")


if __name__ == "__main__":
    app.run(debug=True)
