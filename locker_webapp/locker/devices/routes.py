from flask import Blueprint, request, url_for, redirect, render_template, flash
from locker import app, db
from flask_login import login_required

from .models import Devices, Autorizados
from .forms import NovoDispositivoForm, DispositivoAutorizadoForm

import requests

devices = Blueprint('devices', __name__)


#################### * Helpers * ####################

# Flash errors
def flash_erros(erros):
    print(erros)
    for key, values in erros:
        for value in values:
            flash(f'{value}', "danger")


############# * Dispositivos Autorizados * ##############

# Adicionar Dispositivo
@devices.route("/adicionar-dispositivo-autorizado")
@login_required
def adicionar_autorizado():
    title = "Adicionar Dispositivo Autorizado"
    form = DispositivoAutorizadoForm()
    return render_template('dispositivos/devices/adicionar_autorizados.html', title = title,
        form = form)


#################### * Dispositivos * ####################

# Lista de dispositivos
@devices.route("/")
@login_required
def landing():
    title = "Lista de Dispostivos Conectados"
    devices = Devices.query.all()
    return render_template('dispositivos/devices/devices.html', title = title, 
        devices = devices)

# Conectar novo dispositivo
@devices.route("/adicionar-dispositivo", methods = ['POST', 'GET'])
@login_required
def conectar_dispositivo():
    title = "Adicionar Novo Dispositivo"
    form = NovoDispositivoForm()
    if form.validate_on_submit():
        nome_disp = form.nome.data
        pin_rasp = form.pin.data
        device = Devices.query.filter_by(pin = pin_rasp).first()
        if device: # Verificar se algum dispositivo possui o pin a ser utilizado
            flash(f"Pino a ser utilizado por {device.nome}", "danger")
            return redirect(url_for('devices.conectar_dispositivo'))
        device_add = Devices(nome = nome_disp, pin = pin_rasp, estado = False)
        db.session.add(device_add)
        db.session.commit()
        flash(f"Dispositivo {nome_disp} no pino {pin_rasp} adicionado com sucesso", "success")
        return redirect(url_for("devices.landing"))
    return render_template("dispositivos/devices/adicionar_device.html", title = title, form = form)

# Editar Device
@devices.route('/editar-dispositivo/<int:id>', methods = ['POST', 'GET'])
@login_required
def editar_dispositivo(id):
    form = NovoDispositivoForm()
    device = Devices.query.get_or_404(id)
    title = f"Editar Dispositivo {device.nome}"
    if form.validate_on_submit():
        device.nome = form.nome.data
        device.pin = form.pin.data
        db.session.commit()
        flash(f"{device.nome} atualizado com sucesso!", "success")
        return redirect(url_for('devices.landing'))
    return render_template('dispositivos/devices/editar-device.html', device = device,
        title = title, form = form)    

# Apagar Dispositivo
@devices.route("/apagar-dispositivo/<int:id>", methods = ['POST'])
@login_required
def apagar_dispositivo(id):
    disp = Devices.query.get_or_404(id)
    if disp:
        db.session.delete(disp)
        db.session.commit()
        flash("Dispositivo removido do servidor.","success")
        return redirect(url_for('devices.landing'))


#################### * Interaçoes c/ Devices * ####################

@devices.route("/toggle-device/<int:id>", methods = ['POST'])
def toggle(id):
    device = Devices.query.get_or_404(id)
    if request.method == "POST":
        endpoint = f"http://127.0.0.1:5000/device_patch/{device.pin}"
        status = not device.estado
        r = requests.patch(endpoint, {'status': status})
        if r.status_code == 200:
            if status: flash(f"{device.nome} acionado com sucesso!", "success")
            if not status: flash(f"{device.nome} desacionado com sucesso!", "success")
        else:
            flash("Algo errado aconteceu durante envio do comando", "danger")
        return redirect(url_for('devices.landing'))