from locker import db

"""
    DEVICES: Modelo responsavel por armazenar o estado dos GPIOs
        - Nome: Nome do dispositivo;
        - Pin: Número do GPIO
        - Codigo: Código da porta + gsm
        - Estado: True, False -> Ligado, Desligado
    ---
    Controladores: Modelo responsavel por armazenar informacao usada na API
        - Nome: Nome do controlador
        - Access_name: Nome a ser validado
        - key: Código de acesso
"""

class Devices(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    nome = db.Column(db.String(50),unique = True, nullable = False)
    device_id = db.Column(db.String(10), unique = True, nullable = False)
    pin = db.Column(db.Integer, unique = True, nullable = False)
    codigo = db.Column(db.String(10), unique = True, nullable = False)
    estado = db.Column(db.Boolean, nullable = False)

class Controladores(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    nome = db.Column(db.String(50), nullable = False, unique = True)
    access_name = db.Column(db.String(20), nullable = False, unique = True)
    key = db.Column(db.String(180), nullable = False, unique = False)

class Atualizar(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    atualizar = db.Column(db.Integer, nullable = False, unique = False)

db.create_all()