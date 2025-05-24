# backend/controllers/store.py

import os
from flask import Blueprint, render_template, session, request, jsonify, url_for
from backend.utils.db import conectar
from backend.controllers.profile import login_required  # conforme seu setup atual

store_bp = Blueprint('store', __name__, url_prefix='/store')

@store_bp.route('/balance', methods=['GET'])
@login_required
def get_balance():
    """Retorna o saldo atual do usuário."""
    user_id = session['user_id']
    conn = conectar(); cur = conn.cursor()
    cur.execute("SELECT coins FROM usuarios WHERE id = %s", (user_id,))
    row = cur.fetchone()
    cur.close(); conn.close()
    return jsonify({'coins': row[0] if row else 0})

@store_bp.route('/categories', methods=['GET'])
def get_categories():
    """Lista as categorias disponíveis na loja com o caminho correto das imagens."""
    cats = [
        {'slug': 'roupas', 'name': 'Roupas', 'img': url_for('static', filename='assets/img/roupas.png')},
        {'slug': 'avatar','name': 'Avatar','img': url_for('static', filename='assets/img/avatar.png')},
        {'slug': 'cupons','name': 'Cupons','img': url_for('static', filename='assets/img/cupons.png')},
        {'slug': 'temas', 'name': 'Temas', 'img': url_for('static', filename='assets/img/temas.png')},
    ]
    return jsonify(cats)

@store_bp.route('/items/<category>', methods=['GET'])
def get_items(category):
    """Busca todos os itens de uma categoria."""
    conn = conectar(); cur = conn.cursor()
    cur.execute("""
        SELECT id, name, price, img_url
          FROM store_items
         WHERE category = %s
         ORDER BY id
    """, (category,))
    cols = [d.name for d in cur.description]
    items = [dict(zip(cols, row)) for row in cur.fetchall()]
    cur.close(); conn.close()
    return jsonify(items)

@store_bp.route('/purchase', methods=['POST'])
@login_required
def purchase():
    """Compra um item: debita coins e registra posse em user_items."""
    user_id = session['user_id']
    item_id = request.json.get('item_id')

    conn = conectar(); cur = conn.cursor()
    # 1) preço do item
    cur.execute("SELECT price FROM store_items WHERE id = %s", (item_id,))
    row = cur.fetchone()
    if not row:
        cur.close(); conn.close()
        return jsonify({'error': 'Item não encontrado'}), 404
    price = row[0]

    # 2) saldo do usuário
    cur.execute("SELECT coins FROM usuarios WHERE id = %s FOR UPDATE", (user_id,))
    balance = cur.fetchone()[0]
    if balance < price:
        cur.close(); conn.close()
        return jsonify({'error': 'Saldo insuficiente'}), 400

    # 3) debita e registra posse
    new_balance = balance - price
    cur.execute("UPDATE usuarios SET coins = %s WHERE id = %s", (new_balance, user_id))
    cur.execute("INSERT INTO user_items (user_id, item_id) VALUES (%s, %s)", (user_id, item_id))

    conn.commit(); cur.close(); conn.close()
    return jsonify({'new_balance': new_balance})

@store_bp.route('/grant_coins', methods=['POST'])
@login_required
def grant_coins():
    """
    Concede coins ao usuário (compra simulada).
    Espera JSON: { "amount": 50 }
    """
    try:
        user_id = session['user_id']
        amount = request.json.get('amount', 0)

        conn = conectar(); cur = conn.cursor()
        # bloqueia a linha do usuário
        cur.execute("SELECT coins FROM usuarios WHERE id = %s FOR UPDATE", (user_id,))
        row = cur.fetchone()
        if row is None:
            raise ValueError(f"Usuário {user_id} não encontrado")

        balance = row[0]
        new_balance = balance + amount

        cur.execute("UPDATE usuarios SET coins = %s WHERE id = %s", (new_balance, user_id))
        conn.commit(); cur.close(); conn.close()

        return jsonify({'new_balance': new_balance})

    except Exception as e:
        # retorna o erro para debugging
        return jsonify({'error': str(e)}), 500

@store_bp.route('/inventory', methods=['GET'])
@login_required
def get_inventory():
    """Retorna todos os itens que o usuário já comprou."""
    user_id = session['user_id']
    conn = conectar(); cur = conn.cursor()
    cur.execute("""
        SELECT ui.id      AS user_item_id,
               si.id      AS item_id,
               si.category,
               si.name,
               si.img_url,
               ui.equipped
          FROM user_items ui
    INNER JOIN store_items si ON si.id = ui.item_id
         WHERE ui.user_id = %s
      ORDER BY ui.acquired_at
    """, (user_id,))
    cols = [d.name for d in cur.description]
    inv = [dict(zip(cols, row)) for row in cur.fetchall()]
    cur.close(); conn.close()
    return jsonify(inv)

@store_bp.route('/opcoes/<category>', methods=['GET'])
def page_category(category):
    """Renders the HTML container for a given category."""
    if category not in ('roupas','avatar','cupons','temas'):
        return "Categoria não existe", 404
    return render_template(f'opcoes/{category}.html')
