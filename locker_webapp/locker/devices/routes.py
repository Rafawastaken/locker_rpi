from flask import Blueprint, request, url_for, redirect, render_template, flash
from locker import app, db, bcrypt
from flask_login import login_required

from .models import Devices, Controladores, Atualizar
from .forms import AdicionarDispositivoForm, AdicionarControladorForm

devices = Blueprint('devices', __name__)


#################### * Helpers * ####################

# Flash errors
def flash_erros(erros):
    print(erros)
    for key, values in erros:
        for value in values:
            flash(f'{value}', "danger")


def atualizar_config_db():
    try:
        atualizar = Atualizar.query.first()
        if atualizar:
            atualizar.atualizar = True
        else:
            atualizar = Atualizar(atualizar = True)
            db.session.add(atualizar)
        db.session.commit()
        return True
    except:
        return False



#################### * Controladores * ####################

# Lista de Controladores
@devices.route('/controladores')
@login_required
def controladores():
    title = "Lista de Controladores"
    controladores = Controladores.query.all()
    return render_template('dispositivos/controladores/controladores.html',
        title = title, controladores = controladores)

# Adicionar Controlador
@devices.route("/adicionar-controlador", methods = ['POST', 'GET'])
@login_required
def adicionar_controlador():
    title = "Adicionar Controlador"
    form = AdicionarControladorForm()
    if form.validate_on_submit():
        # Match data 
        nome = form.nome.data
        codigo =  bcrypt.generate_password_hash(form.access_code.data)
        access_name = form.access_name.data
       
        # Adicionar novo controlador
        novo_controlador = Controladores(nome = nome, key = codigo, access_name = access_name)
        db.session.add(novo_controlador)
        db.session.commit()

        flash(f"{nome} adicionado com sucesso!", "success")
        return redirect(url_for('devices.controladores'))
    else:
        flash_erros(form.errors.items())
    return render_template('dispositivos/controladores/adicionar_controlador.html',
        title = title, form = form)

# Editar Controlador
@devices.route('/editar-controlador/<int:id>', methods = ['POST', 'GET'])
@login_required
def editar_controlador(id):
    title = "Editar Controlador"
    controlador = Controladores.query.get_or_404(id)
    form = AdicionarControladorForm()
    if form.validate_on_submit():
        controlador.nome = form.nome.data
        controlador.access_name = form.access_name.data
        controlador.key = bcrypt.generate_password_hash(form.access_code.data)
        db.session.commit()

        # Atualizar
        atualizar_config_db()

        flash(f"Controlador {form.nome.data} editar com sucesso!", "success")
        return redirect(url_for('devices.controladores'))
    else: 
        flash_erros(form.errors.items())
    return render_template('dispositivos/controladores/editar_controlador.html',
        title = title, controlador = controlador, form = form)

# Apagar Controlador
@devices.route('/apagar-controlador/<int:id>', methods = ['POST'])
@login_required
def apagar_controlador(id):
    controlador = Controladores.query.get_or_404(id)
    if not controlador:
        flash("Impossível apagar o controlador requisitado...", "danger")
        return redirect(url_for('devices.controladores'))
    db.session.delete(controlador)
    db.session.commit()

    # Atualizar
    atualizar_config_db()

    flash(f"Controlador {controlador.nome} removido com sucesso!", "success")
    return redirect(url_for('devices.controladores'))

#################### * Dispositivos * ####################

# Lista de dispositivos
@devices.route("/")
@login_required
def dispositivos():
    title = "Lista de Dispostivos Conectados"
    devices = Devices.query.all()
    return render_template('dispositivos/devices/devices.html', title = title, 
        devices = devices)

# Conectar novo dispositivo
@devices.route("/adicionar-dispositivo", methods = ['POST', 'GET'])
@login_required
def conectar_dispositivo():
    title = "Adicionar Novo Dispositivo"
    form = AdicionarDispositivoForm()
    if form.validate_on_submit():
        # Dados form
        nome_disp = form.nome.data
        device_id = form.device_id.data
        pin_rasp = form.pin.data
        codigo = form.codigo.data

        # Verificar se algum dispositivo possui o pin a ser utilizado
        if Devices.query.filter_by(pin = pin_rasp).first(): 
            flash(f"Pino a ser utilizado", "danger")
            return redirect(url_for('devices.conectar_dispositivo'))

        # Verificar se algum dispositivo possui o id a ser utilizado
        if Devices.query.filter_by(device_id =  device_id).first():
            flash(f"ID de dispositivo a ser utilizado", "danger")
            return redirect(url_for('devices.consectar_dispositivo'))

        # Adicionar dispositivo a base de dados
        device_add = Devices(nome = nome_disp, device_id = device_id, pin = pin_rasp, codigo = codigo, estado = False)
        db.session.add(device_add)
        db.session.commit()

        # Atualizar 
        atualizar_config_db()

        # Notificar e finalizar
        flash(f"Dispositivo {nome_disp} no pino {pin_rasp} adicionado com sucesso", "success")
        return redirect(url_for("devices.dispositivos"))
    else: 
        flash_erros(form.errors.items())
    return render_template("dispositivos/devices/adicionar_device.html", title = title, form = form)

# Editar Device
@devices.route('/editar-dispositivo/<int:id>', methods = ['POST', 'GET'])
@login_required
def editar_dispositivo(id):
    # Filtrar dispositivo 
    device = Devices.query.get_or_404(id)
    
    title = f"Editar Dispositivo {device.nome}"
    form = AdicionarDispositivoForm()


    if form.validate_on_submit():
        # Atribuir valores atualizados
        device.nome = form.nome.data
        device.pin = form.pin.data
        device.codigo = form.codigo.data
        device.device_id = form.device_id.data

        # Guarda a base de dados
        db.session.commit()

        # Atualizar
        atualizar_config_db()

        # Notificar e finalizar
        flash(f"{device.nome} atualizado com sucesso!", "success")
        return redirect(url_for('devices.dispositivos'))

    return render_template('dispositivos/devices/editar-device.html', device = device,
        title = title, form = form)    

# Apagar Dispositivo
@devices.route("/apagar-dispositivo/<int:id>", methods = ['POST'])
@login_required
def apagar_dispositivo(id):
    # Filtrar dispositivo
    device = Devices.query.get_or_404(id)

    # Se dispositivo nao encontrado
    if not device:
        flash("Impossível apagar o dispositivo requisitado ", "danger")
        return redirect(url_for("devices.dispositivos"))

    # Remover dispositivo da base de dados
    db.session.delete(device)
    db.session.commit()

    # Atualizar
    atualizar_config_db()
    
    # Notificar e finalizar
    flash("Dispositivo removido do servidor.","success")
    return redirect(url_for('devices.dispositivos'))


#################### * Interaçoes c/ Devices * ####################

@devices.route("/toggle-device/<int:id>", methods = ['POST'])
@login_required
def toggle(id):
    device = Devices.query.get_or_404(id)
    if request.method == "POST":
        device.estado = not device.estado
        db.session.commit()
        if device.estado: flash(f"{device.nome} acionado com sucesso!", "success")
        if not device.estado: flash(f"{device.nome} desacionado com sucesso!", "success")
    return redirect(url_for('devices.dispositivos'))


#################### * Atualizar config * ####################
@devices.route('/atualizar-config', methods = ['POST'])
def atualizar_config():
    if atualizar_config_db():
        flash("Pedido para atualizar exectutado com sucesso", "success")
    else:
        flash("Ocorreu um erro ao executar o pedido de atualização das configurações", "danger")
    return redirect(request.referrer)
