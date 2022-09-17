from locker import db

"""
    Modelo para armazenar as configurações dos Relés
        id - ID de device
        nome - Nome do device
        pin - Pin number ao qual device esta ligado
        estado - Ligado ou Desligado
"""

class Devices(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    nome = db.Column(db.String(50),unique = True, nullable = False)
    pin = db.Column(db.Integer, unique = True, nullable = False)
    estado = db.Column(db.Boolean, nullable = False)

class Controladores(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    nome = db.Column(db.String(50), nullable = False, unique = True)
    key = db.Column(db.String(180), nullable = False, unique = False)

db.create_all()