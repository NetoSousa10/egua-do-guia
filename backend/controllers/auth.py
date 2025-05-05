# backend/controllers/auth.py

import os
from flask import (
    Blueprint, request, jsonify, session,
    redirect, url_for, flash, render_template
)
from email_validator import validate_email, EmailNotValidError
from backend.utils.db import conectar
from werkzeug.security import generate_password_hash, check_password_hash

auth_bp = Blueprint('auth', __name__)

@auth_bp.route("/cadastro", methods=["POST"])
def cadastro():
    dados      = request.get_json(silent=True) or request.form
    nome       = dados.get("nome",     "").strip()
    email      = dados.get("email",    "").strip()
    senha_raw  = dados.get("senha",    "").strip()
    nacional   = dados.get("nacionalidade", "").strip()
    genero     = dados.get("genero",   "").strip()
    maior14    = bool(dados.get("maior14"))

    # 1) campos obrigatórios
    if not all([nome, email, senha_raw, nacional, genero, maior14]):
        msg = "Todos os campos são obrigatórios e você deve ter mais de 14 anos."
        if request.is_json:
            return jsonify({"erro": msg}), 400
        flash(msg, "error")
        return redirect(url_for("cadastro_form"))

    # 2) validação de formato de e-mail usando email-validator
    try:
        valid = validate_email(email)
        email = valid.email
    except EmailNotValidError:
        msg = "E-mail inválido."
        if request.is_json:
            return jsonify({"erro": msg}), 400
        flash(msg, "error")
        return redirect(url_for("cadastro_form"))

    # 3) senha mínima
    if len(senha_raw) < 6:
        msg = "Senha deve ter ao menos 6 caracteres."
        if request.is_json:
            return jsonify({"erro": msg}), 400
        flash(msg, "error")
        return redirect(url_for("cadastro_form"))

    # 4) verifica duplicidade
    conn = conectar()
    cur  = conn.cursor()
    cur.execute("SELECT id FROM usuarios WHERE email = %s", (email,))
    if cur.fetchone():
        cur.close()
        conn.close()
        msg = "E-mail já cadastrado."
        if request.is_json:
            return jsonify({"erro": msg}), 400
        flash(msg, "error")
        return redirect(url_for("cadastro_form"))

    # 5) insere novo usuário
    senha_hash = generate_password_hash(senha_raw)
    cur.execute("""
        INSERT INTO usuarios
          (nome, email, senha, nacionalidade, genero, maior14)
        VALUES (%s, %s, %s, %s, %s, %s)
    """, (nome, email, senha_hash, nacional, genero, maior14))
    conn.commit()
    cur.close()
    conn.close()

    sucesso = "Cadastro realizado com sucesso! Faça login."
    if request.is_json:
        return jsonify({"mensagem": sucesso}), 201
    flash(sucesso, "success")
    return redirect(url_for("login_form"))


@auth_bp.route("/login", methods=["POST"])
def login():
    dados     = request.get_json(silent=True) or request.form
    email     = dados.get("email", "").strip()
    senha_raw = dados.get("senha", "").strip()

    # 1) campos obrigatórios
    if not email or not senha_raw:
        msg = "E-mail e senha são obrigatórios."
        if request.is_json:
            return jsonify({"erro": msg}), 400
        flash(msg, "error")
        return redirect(url_for("login_form"))

    # 2) validação de formato de e-mail usando email-validator
    try:
        valid = validate_email(email)
        email = valid.email
    except EmailNotValidError:
        msg = "E-mail inválido."
        if request.is_json:
            return jsonify({"erro": msg}), 400
        flash(msg, "error")
        return redirect(url_for("login_form"))

    # 3) senha mínima
    if len(senha_raw) < 6:
        msg = "Senha deve ter ao menos 6 caracteres."
        if request.is_json:
            return jsonify({"erro": msg}), 400
        flash(msg, "error")
        return redirect(url_for("login_form"))

    # 4) busca usuário no DB
    conn = conectar()
    cur  = conn.cursor()
    cur.execute("SELECT id, nome, senha FROM usuarios WHERE email = %s", (email,))
    row = cur.fetchone()
    cur.close()
    conn.close()

    # 5) valida credenciais
    if not row or not check_password_hash(row[2], senha_raw):
        msg = "Credenciais inválidas."
        if request.is_json:
            return jsonify({"erro": msg}), 401
        flash(msg, "error")
        return redirect(url_for("login_form"))

    # 6) sucesso: inicia sessão
    session.clear()
    session["user_id"]   = row[0]
    session["user_nome"] = row[1]

    sucesso = "Login realizado com sucesso!"
    if request.is_json:
        return jsonify({"mensagem": sucesso, "user": {"id": row[0], "nome": row[1]}}), 200
    flash(sucesso, "success")
    return redirect(url_for("tutorial"))


@auth_bp.route('/auth/complete-profile', methods=['GET', 'POST'])
def complete_profile():
    user_id = session.get('user_id')
    if not user_id:
        flash("Faça login para completar seu perfil.", "error")
        return redirect(url_for('login_form'))

    if request.method == 'POST':
        nacional = request.form.get('nacionalidade', '').strip()
        genero   = request.form.get('genero', '').strip()

        # validação simples
        if not nacional or not genero:
            flash("Selecione nacionalidade e gênero.", "error")
            return redirect(url_for('auth.complete_profile'))

        # atualiza no banco
        conn = conectar()
        cur  = conn.cursor()
        cur.execute("""
            UPDATE usuarios
               SET nacionalidade = %s,
                   genero        = %s
             WHERE id = %s
        """, (nacional, genero, user_id))
        conn.commit()
        cur.close()
        conn.close()

        flash("Perfil atualizado com sucesso!", "success")
        return redirect(url_for("tutorial"))

    # GET: renderiza o form
    return render_template('login/complete_profile.html')
