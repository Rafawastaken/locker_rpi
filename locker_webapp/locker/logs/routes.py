from flask import Blueprint, flash, render_template, redirect, url_for, request
from flask_login import current_user, login_required
from .models import LogsAtividade
from locker import app, db

import random

logs = Blueprint('logs', __name__)


#################### * Helpers * ####################

# Flash errors
def flash_erros(erros):
    print(erros)
    for key, values in erros:
        for value in values:
            flash(f'{value}', "danger")

def adicionar_atividade_sample():
    for x in range(50):
        entry = LogsAtividade(
            utilizador = current_user.nome,
            dispositivo = f"Porta {random.randint(1,4)}",
            origem = "Servidor"
        )

        db.session.add(entry)
    db.session.commit()


#################### * Registo * ####################

# Visualizar registo de atividade
@logs.route('/registos-atividade')
@login_required
def registo_atividade():
    title = "Registos de atividade"
    page = request.args.get('page', 1, type = int)
    logs = LogsAtividade.query.order_by(LogsAtividade.id.desc())
    logs = logs.paginate(page = page, per_page = 40)

    return render_template('logs/logs.html', title = title, logs = logs)
