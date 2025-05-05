# backend/controllers/oauth.py

import os
from flask import Blueprint, redirect, url_for, session
from authlib.integrations.flask_client import OAuth
from backend.utils.db import conectar

oauth_bp = Blueprint('oauth', __name__)
oauth    = OAuth()

# Registra o Google via OpenID Connect discovery
oauth.register(
    name='google',
    client_id=os.getenv("GOOGLE_CLIENT_ID"),
    client_secret=os.getenv("GOOGLE_CLIENT_SECRET"),
    server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
    client_kwargs={'scope': 'openid email profile'}
)

@oauth_bp.route('/auth/google')
def login_google():
    redirect_uri = url_for('oauth.auth_callback', _external=True)
    return oauth.google.authorize_redirect(redirect_uri)

@oauth_bp.route('/auth/google/callback')
def auth_callback():
    # 1) troca código por token
    token = oauth.google.authorize_access_token()
    # 2) busca dados do usuário
    user_info = oauth.google.userinfo()  

    # 3) deriva nacionalidade a partir do locale (ex: 'pt-BR' → 'br')
    locale        = user_info.get('locale', '')
    nacionalidade = locale.split('-')[-1].lower() if '-' in locale else locale.lower()
    # 4) valores padrão para gender e maior14
    genero  = 'outro'
    maior14 = True

    # 5) busca ou cria usuário no banco
    conn = conectar()
    cur  = conn.cursor()
    cur.execute(
        "SELECT id, nome FROM usuarios WHERE email = %s",
        (user_info['email'],)
    )
    row = cur.fetchone()

    if row:
        user_id, nome = row
    else:
        cur.execute(
            """
            INSERT INTO usuarios
              (nome, email, senha, nacionalidade, genero, maior14)
            VALUES (%s,%s,%s,%s,%s,%s)
            RETURNING id
            """,
            (
                user_info['name'],
                user_info['email'],
                '',             # senha vazia para social login
                nacionalidade,  # derivada do locale
                genero,         # padrão 'outro'
                maior14         # assume maior de 14 anos
            )
        )
        user_id = cur.fetchone()[0]
        conn.commit()

    cur.close()
    conn.close()

    # 6) grava na sessão e redireciona
    session.clear()
    session['user_id']   = user_id
    session['user_nome'] = user_info['name']
    return redirect(url_for('tutorial'))
