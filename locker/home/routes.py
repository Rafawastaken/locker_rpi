from flask import Blueprint, render_template, flash, redirect, url_for, request
from flask_login import login_required
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
    title = "Tek 4 Door | Servidor de Domótica"
    return render_template('/home/landing.html', title = title)

