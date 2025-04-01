from flask import Blueprint, render_template

lugares_bp = Blueprint('lugares', __name__)

@lugares_bp.route("/lugares")
def listar_lugares():
    return "Lugares funcionando!"
