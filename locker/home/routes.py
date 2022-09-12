from flask import Blueprint, render_template, flash, redirect, url_for, request
from flask_login import login_required, current_user, logout_user, login_user

from locker import app, db

home = Blueprint('home', __name__)


#################### * Helpers * ####################

# Flash errors
def flash_erros(erros):
    print(erros)
    for key, values in erros:
        for value in values:
            flash(f'{value}', "danger")


#################### * Standard Pages * ####################

# Landing Page 
@home.route('/')
@login_required
def landing():
    title = "Lista de Utilizadores Autorizados"
    return render_template('/home/landing.html', title = title)


