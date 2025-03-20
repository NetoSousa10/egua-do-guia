from flask import Blueprint, request, jsonify, session
from utils.db import conectar
from werkzeug.security import generate_password_hash, check_password_hash

auth_bp = Blueprint('auth', __name__)

# Rota de cadastro
@auth_bp.route("/cadastro", methods=["POST"])
def cadastro():
    dados = request.get_json()
    nome = dados.get("nome")
    email = dados.get("email")
    senha = generate_password_hash(dados.get("senha"))

    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("SELECT id FROM usuarios WHERE email = %s", (email,))
    if cursor.fetchone():
        return jsonify({"erro": "Email já cadastrado."}), 400

    cursor.execute("INSERT INTO usuarios (nome, email, senha) VALUES (%s, %s, %s)", (nome, email, senha))
    conexao.commit()
    cursor.close()
    conexao.close()

    return jsonify({"mensagem": "Usuário cadastrado com sucesso!"}), 201
