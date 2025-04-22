# auth.py
from flask import Blueprint, request, jsonify, session
from backend.utils.db import conectar
from werkzeug.security import generate_password_hash, check_password_hash

auth_bp = Blueprint('auth', __name__)

# Rota de cadastro
@auth_bp.route("/cadastro", methods=["POST"])
def cadastro():
    dados = request.get_json()
    nome = dados.get("nome", "").strip()
    email = dados.get("email", "").strip()
    senha_raw = dados.get("senha", "").strip()

    if not nome or not email or not senha_raw:
        return jsonify({"erro": "Todos os campos são obrigatórios."}), 400

    conexao = conectar()
    cursor = conexao.cursor()

    # verifica se já existe
    cursor.execute("SELECT id FROM usuarios WHERE email = %s", (email,))
    if cursor.fetchone():
        cursor.close()
        conexao.close()
        return jsonify({"erro": "E‑mail já cadastrado."}), 400

    # insere
    senha_hash = generate_password_hash(senha_raw)
    cursor.execute(
        "INSERT INTO usuarios (nome, email, senha) VALUES (%s, %s, %s)",
        (nome, email, senha_hash)
    )
    conexao.commit()
    cursor.close()
    conexao.close()

    return jsonify({"mensagem": "Usuário cadastrado com sucesso!"}), 201


# Rota de login
@auth_bp.route("/login", methods=["POST"])
def login():
    dados = request.get_json()
    email = dados.get("email", "").strip()
    senha_raw = dados.get("senha", "").strip()

    if not email or not senha_raw:
        return jsonify({"erro": "E‑mail e senha são obrigatórios."}), 400

    conexao = conectar()
    cursor = conexao.cursor(dictionary=True)

    cursor.execute("SELECT id, nome, senha FROM usuarios WHERE email = %s", (email,))
    user = cursor.fetchone()
    cursor.close()
    conexao.close()

    if user is None or not check_password_hash(user["senha"], senha_raw):
        return jsonify({"erro": "Credenciais inválidas."}), 401

    # Exemplo simples de sessão
    session.clear()
    session["user_id"] = user["id"]
    session["user_nome"] = user["nome"]

    return jsonify({"mensagem": "Login realizado com sucesso!", "user": {"id": user["id"], "nome": user["nome"]}}), 200


# Rota de logout (opcional)
@auth_bp.route("/logout", methods=["POST"])
def logout():
    session.clear()
    return jsonify({"mensagem": "Logout efetuado."}), 200
