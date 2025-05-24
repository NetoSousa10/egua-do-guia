# backend/controllers/tutorial.py

from flask import Blueprint, session, redirect, url_for, render_template, jsonify
from backend.utils.db import conectar
from backend.controllers.profile import login_required

tutorial_bp = Blueprint('tutorial', __name__, url_prefix='/tutorial')

def user_done(user_id):
    """
    Retorna True se o usuário já completou o tutorial.
    """
    conn = conectar()
    cur  = conn.cursor()
    cur.execute(
        "SELECT tutorial_done FROM usuarios WHERE id = %s",
        (user_id,)
    )
    row = cur.fetchone()
    cur.close()
    conn.close()
    return bool(row and row[0])

@tutorial_bp.route('/', methods=['GET'])
@login_required
def index():
    # Sempre leva à etapa 1
    return redirect(url_for('tutorial.etapa', step=1))

@tutorial_bp.route('/etapa<int:step>', methods=['GET'])
@login_required
def etapa(step):
    user_id = session['user_id']

    # Se já concluiu, redireciona direto para a home
    if user_done(user_id):
        # Substitua 'menu.menu_home' pelo endpoint correto da sua home
        return redirect(url_for('menu.menu_home'))

    # Senão, renderiza a etapa apropriada
    if step == 1:
        return render_template('tutorial/tutorial_etapa1.html')
    return render_template(f'tutorial/tutorial_etapa{step}.html')

@tutorial_bp.route('/complete', methods=['POST'])
@login_required
def complete():
    user_id = session['user_id']
    conn    = conectar()
    cur     = conn.cursor()

    # Busca estado atual e saldo
    cur.execute(
        "SELECT tutorial_done, coins FROM usuarios WHERE id = %s",
        (user_id,)
    )
    row = cur.fetchone()
    if not row:
        cur.close()
        conn.close()
        return jsonify({'error': 'Usuário não encontrado'}), 404

    done, balance = row

    # Se já ganhou, retorna sem conceder de novo
    if done:
        cur.close()
        conn.close()
        return jsonify({'new_balance': balance, 'granted': 0})

    # Concede 20 moedas e marca tutorial como feito
    new_balance = balance + 20
    cur.execute("""
        UPDATE usuarios
           SET coins = %s,
               tutorial_done = TRUE
         WHERE id = %s
    """, (new_balance, user_id))
    conn.commit()
    cur.close()
    conn.close()

    return jsonify({'new_balance': new_balance, 'granted': 20})

@tutorial_bp.route('/reward', methods=['GET'])
@login_required
def reward():
    user_id = session['user_id']

    # Se ainda não completou, volta para o início do tutorial
    if not user_done(user_id):
        return redirect(url_for('tutorial.index'))

    # Caso contrário, exibe a tela de recompensa
    return render_template('tutorial/reward.html')
