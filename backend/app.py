from flask import Flask
from dotenv import load_dotenv
import os
from controllers.auth import auth_bp

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")
app.register_blueprint(auth_bp, url_prefix="/auth")

@app.route("/")
def home():
    return "✅ API Égua do Guia rodando!"

if __name__ == "__main__":
    app.run(debug=True)
