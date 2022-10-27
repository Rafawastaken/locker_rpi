from locker import db
from datetime import datetime as dt

class LogsAtividade(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    utilizador = db.Column(db.String, unique = False, nullable = False) # Quem efetuou o pedido
    dispositivo = db.Column(db.String, unique = False, nullable = False) # Porta que foi direcionado o pedido
    origem = db.Column(db.String, unique = False, nullable = False) # Onde foi emitido o pedido (Servidor, Keypad, GSM)
    data = db.Column(db.String, unique = False, default = dt.now().strftime("%d-%m-%Y %H:%M:%S")) # Timestamp

    def __repr__(self):
        return f"<Registo {self.target}_{self.data}>"

db.create_all()
