# backend/controllers/auth.py

import logging
from flask import (
    Blueprint, request, jsonify, session,
    redirect, url_for, flash, render_template
)
from email_validator import validate_email, EmailNotValidError
from backend.utils.db import conectar
from werkzeug.security import generate_password_hash, check_password_hash
from backend.controllers.tutorial import user_done  # helper import

auth_bp = Blueprint('auth', __name__)
logger = logging.getLogger(__name__)

def _error_response(message, status=400):
    """Retorna JSON ou flash+redirect conforme o Content-Type."""
    if request.is_json:
        return jsonify({"erro": message}), status
    flash(message, "error")
    return redirect(url_for("login_form"))

@auth_bp.route("/cadastro", methods=["POST"])
def cadastro():
    dados      = request.get_json(silent=True) or request.form
    nome       = dados.get("nome",     "").strip()
    email      = dados.get("email",    "").strip().lower()
    senha_raw  = dados.get("senha",    "").strip()
    nacional   = dados.get("nacionalidade", "").strip()
    genero     = dados.get("genero",   "").strip()
    maior14    = bool(dados.get("maior14"))
 
    if not all([nome, email, senha_raw, nacional, genero, maior14]):
        msg = "Todos os campos são obrigatórios e você deve ter mais de 14 anos."
        if request.is_json:
            return jsonify({"erro": msg}), 400
        flash(msg, "error")
        return redirect(url_for("cadastro_form"))

    try:
        valid = validate_email(email)
        email = valid.email.lower()
    except EmailNotValidError:
        msg = "E-mail inválido."
        if request.is_json:
            return jsonify({"erro": msg}), 400
        flash(msg, "error")
        return redirect(url_for("cadastro_form"))

    if len(senha_raw) < 6:
        msg = "Senha deve ter ao menos 6 caracteres."
        if request.is_json:
            return jsonify({"erro": msg}), 400
        flash(msg, "error")
        return redirect(url_for("cadastro_form"))

    conn = conectar()
    cur  = conn.cursor()
    cur.execute("SELECT id FROM usuarios WHERE email = %s", (email,))
    if cur.fetchone():
        cur.close(); conn.close()
        msg = "E-mail já cadastrado."
        if request.is_json:
            return jsonify({"erro": msg}), 400
        flash(msg, "error")
        return redirect(url_for("cadastro_form"))

    senha_hash = generate_password_hash(senha_raw)
    cur.execute("""
        INSERT INTO usuarios
          (nome, email, senha, nacionalidade, genero, maior14)
        VALUES (%s, %s, %s, %s, %s, %s)
    """, (nome, email, senha_hash, nacional, genero, maior14))
    conn.commit()
    cur.close(); conn.close()

    sucesso = "Cadastro realizado com sucesso! Faça login."
    if request.is_json:
        return jsonify({"mensagem": sucesso}), 201
    flash(sucesso, "success")
    return redirect(url_for("login_form"))


@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json(silent=True) or request.form
    email = (data.get("email") or "").strip().lower()
    senha = (data.get("senha") or "").strip()

    if not email:
        return _error_response("E-mail é obrigatório.")
    if not senha:
        return _error_response("Senha é obrigatória.")
    try:
        valid = validate_email(email)
        email = valid.email.lower()
    except EmailNotValidError:
        return _error_response("E-mail inválido.")

    if len(senha) < 6:
        return _error_response("Senha deve ter ao menos 6 caracteres.")

    try:
        conn = conectar()
        cur  = conn.cursor()
        cur.execute(
            "SELECT id, nome, senha, tutorial_done FROM usuarios WHERE email = %s",
            (email,)
        )
        row = cur.fetchone()
    except Exception:
        logger.exception("Erro ao buscar usuário para login")
        return _error_response("Erro interno ao processar login.", 500)
    finally:
        try:
            cur.close(); conn.close()
        except:
            pass

    if not row or not check_password_hash(row[2], senha):
        return _error_response("Credenciais inválidas.", 401)

    session.clear()
    session["user_id"]   = row[0]
    session["user_nome"] = row[1]

    tutorial_already_done = bool(row[3])
    success_msg = "Login realizado com sucesso!"

    if request.is_json:
        return jsonify({
            "mensagem": success_msg,
            "user": {"id": row[0], "nome": row[1]},
            "tutorial_done": tutorial_already_done
        }), 200

    flash(success_msg, "success")
    # **AQUI** usamos o endpoint 'home', que já existe
    if tutorial_already_done:
        return redirect(url_for("home"))
    else:
        return redirect(url_for("tutorial.index"))
