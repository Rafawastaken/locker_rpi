from flask import Blueprint, request, url_for, redirect, render_template, flash
from locker import app, db
from flask_login import login_required

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
@login_required
def landing():
    title = "Lista de Dispostivos Conectados"
    devices = Devices.query.all()
    return render_template('devices/devices.html', title = title, 
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
    return render_template("devices/adicionar_device.html", title = title, form = form)

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
    return render_template('devices/editar-device.html', device = device,
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
