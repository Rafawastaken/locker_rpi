from flask import Blueprint, request, url_for, redirect, render_template, flash
from locker import app, db

from .models import Devices, Raspberry
from .forms import NovoDispositivoForm

devices = Blueprint('devices', __name__)


#################### * Helpers * ####################

# Flash errors
def flash_erros(erros):
    print(erros)
    for key, values in erros:
        for value in values:
            flash(f'{value}', "danger")


#################### * Utilizadores * ####################

# Lista de dispositivos
@devices.route("/")
def landing():
    title = "Lista de Dispostivos Conectados"
    return render_template('devices/devices.html', title = title)

# Conectar novo dispositivo
@devices.route("/adicionar-dispositivo", methods = ['POST', 'GET'])
def conectar_dispositivo():
    title = "Adicionar Novo Dispositivo"
    form = NovoDispositivoForm()
    return render_template("devices/adicionar_device.html", title = title, form = form)