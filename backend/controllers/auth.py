from flask import (
    Blueprint, request, jsonify, session,
    redirect, url_for, flash
)
from backend.utils.db import conectar
from werkzeug.security import generate_password_hash, check_password_hash

auth_bp = Blueprint('auth', __name__)

@auth_bp.route("/cadastro", methods=["POST"])
def cadastro():
    dados = request.get_json(silent=True) or request.form

    nome          = dados.get("nome","").strip()
    email         = dados.get("email","").strip()
    senha_raw     = dados.get("senha","").strip()
    nacionalidade = dados.get("nacionalidade","").strip()
    genero        = dados.get("genero","").strip()
    maior14       = bool(dados.get("maior14"))

    if not all([nome, email, senha_raw, nacionalidade, genero, maior14]):
        msg = "Todos os campos são obrigatórios e você deve ter mais de 14 anos."
        if request.is_json:
            return jsonify({"erro": msg}), 400
        flash(msg, "error")
        return redirect(url_for("cadastro_form"))

    conn   = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM usuarios WHERE email = %s", (email,))
    if cursor.fetchone():
        cursor.close(); conn.close()
        msg = "E-mail já cadastrado."
        if request.is_json:
            return jsonify({"erro": msg}), 400
        flash(msg, "error")
        return redirect(url_for("cadastro_form"))

    senha_hash = generate_password_hash(senha_raw)
    cursor.execute("""
        INSERT INTO usuarios
          (nome,email,senha,nacionalidade,genero,maior14)
        VALUES (%s,%s,%s,%s,%s,%s)
    """, (nome,email,senha_hash,nacionalidade, genero, maior14))
    conn.commit()
    cursor.close(); conn.close()

    sucesso = "Cadastro realizado com sucesso! Faça login."
    if request.is_json:
        return jsonify({"mensagem": sucesso}), 201
    flash(sucesso, "success")
    return redirect(url_for("login_form"))


@auth_bp.route("/login", methods=["POST"])
def login():
    dados     = request.get_json(silent=True) or request.form
    email     = dados.get("email","").strip()
    senha_raw = dados.get("senha","").strip()

    if not email or not senha_raw:
        msg = "E-mail e senha são obrigatórios."
        if request.is_json:
            return jsonify({"erro": msg}), 400
        flash(msg, "error")
        return redirect(url_for("login_form"))

    conn   = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT id, nome, senha FROM usuarios WHERE email = %s", (email,))
    row = cursor.fetchone()
    cursor.close(); conn.close()

    if not row or not check_password_hash(row[2], senha_raw):
        msg = "Credenciais inválidas."
        if request.is_json:
            return jsonify({"erro": msg}), 401
        flash(msg, "error")
        return redirect(url_for("login_form"))

    session.clear()
    session["user_id"]   = row[0]
    session["user_nome"] = row[1]

    sucesso = "Login realizado com sucesso!"
    if request.is_json:
        return jsonify({"mensagem": sucesso, "user":{"id":row[0],"nome":row[1]}}), 200
    flash(sucesso, "success")
    return redirect(url_for("tutorial"))
