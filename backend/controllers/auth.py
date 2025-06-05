import logging
from flask import Blueprint, request, jsonify, session, redirect, url_for, flash, render_template, current_app
from flask_mail import Message
from itsdangerous import URLSafeTimedSerializer, SignatureExpired, BadSignature
from email_validator import validate_email, EmailNotValidError
from werkzeug.security import generate_password_hash, check_password_hash
from backend.utils.db import conectar
from backend.controllers.tutorial import user_done

auth_bp = Blueprint('auth', __name__)
logger = logging.getLogger(__name__)

def _error_response(message, status=400):
    if request.is_json:
        return jsonify({"erro": message}), status
    flash(message, "error")
    return redirect(url_for("login_form"))

def get_serializer():
    secret_key = current_app.config['SECRET_KEY']
    return URLSafeTimedSerializer(secret_key)

@auth_bp.route("/cadastro", methods=["POST"])
def cadastro():
    dados = request.get_json(silent=True) or request.form
    nome = dados.get("nome", "").strip()
    email = dados.get("email", "").strip().lower()
    senha_raw = dados.get("senha", "").strip()
    nacional = dados.get("nacionalidade", "").strip()
    genero = dados.get("genero", "").strip()
    maior14 = bool(dados.get("maior14"))

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
    cur = conn.cursor()
    cur.execute("SELECT id FROM usuarios WHERE email = %s", (email,))
    if cur.fetchone():
        cur.close()
        conn.close()
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
    cur.close()
    conn.close()

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
        cur = conn.cursor()
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
            cur.close()
            conn.close()
        except:
            pass

    if not row or not check_password_hash(row[2], senha):
        return _error_response("Credenciais inválidas.", 401)

    session.clear()
    session["user_id"] = row[0]
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
    if tutorial_already_done:
        return redirect(url_for("home"))
    else:
        return redirect(url_for("tutorial.index"))

@auth_bp.route("/esqueci-senha", methods=["GET"])
def esqueci_senha():
    return render_template("auth/forgot_password.html")

@auth_bp.route("/esqueci-senha", methods=["POST"])
def esqueci_senha_post():
    email = request.form.get("email").strip().lower()
    try:
        valid = validate_email(email)
        email = valid.email.lower()
    except EmailNotValidError:
        flash("E-mail inválido.", "error")
        return redirect(url_for("auth.esqueci_senha"))

    conn = conectar()
    cur = conn.cursor()
    cur.execute("SELECT id, nome FROM usuarios WHERE email = %s;", (email,))
    usuario = cur.fetchone()
    cur.close()
    conn.close()

    if not usuario:
        flash("Este e-mail não está cadastrado.", "error")
        return redirect(url_for("auth.esqueci_senha"))

    user_id, nome = usuario
    serializer = get_serializer()
    token = serializer.dumps(email, salt="recuperar-senha")
    reset_link = url_for("auth.resetar_senha", token=token, _external=True)

    assunto = "[Égua do Guia] Recuperação de senha"
    corpo = render_template("auth/email_recovery.html", nome=nome, reset_link=reset_link)
    msg = Message(subject=assunto, recipients=[email], html=corpo)
    try:
        current_app.extensions["mail"].send(msg)
        flash("Enviamos um link de recuperação para o seu e-mail. Verifique sua caixa de entrada.", "success")
    except Exception as e:
        flash(f"Erro ao enviar e-mail: {e}", "error")

    return redirect(url_for("login_form"))

@auth_bp.route("/resetar-senha/<token>", methods=["GET"])
def resetar_senha(token):
    serializer = get_serializer()
    try:
        email = serializer.loads(token, salt="recuperar-senha", max_age=3600)
    except SignatureExpired:
        flash("O link expirou. Por favor, solicite um novo e-mail.", "warning")
        return redirect(url_for("auth.esqueci_senha"))
    except BadSignature:
        flash("Link inválido ou corrompido.", "error")
        return redirect(url_for("auth.esqueci_senha"))

    return render_template("auth/reset_password.html", token=token)

@auth_bp.route("/resetar-senha/<token>", methods=["POST"])
def resetar_senha_post(token):
    senha_nova = request.form.get("senha", "").strip()
    senha_confirmacao = request.form.get("senha_confirmacao", "").strip()

    if senha_nova != senha_confirmacao:
        flash("As senhas não conferem.", "error")
        return redirect(url_for("auth.resetar_senha", token=token))

    serializer = get_serializer()
    try:
        email = serializer.loads(token, salt="recuperar-senha", max_age=3600)
    except SignatureExpired:
        flash("O link expirou. Por favor, solicite um novo e-mail.", "warning")
        return redirect(url_for("auth.esqueci_senha"))
    except BadSignature:
        flash("Link inválido ou corrompido.", "error")
        return redirect(url_for("auth.esqueci_senha"))

    hash_password = generate_password_hash(senha_nova)
    conn = conectar()
    cur = conn.cursor()
    cur.execute("UPDATE usuarios SET senha = %s WHERE email = %s;", (hash_password, email))
    conn.commit()
    cur.close()
    conn.close()

    flash("Sua senha foi redefinida com sucesso! Faça login novamente.", "success")
    return redirect(url_for("login_form"))
