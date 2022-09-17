from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField, BooleanField, PasswordField
from wtforms import validators, ValidationError

class AdicionarDispositivoForm(FlaskForm):
    nome = StringField('Nome', [validators.Length(min = 3, max = 20), validators.DataRequired()])
    pin = IntegerField('Número do Pino', [validators.DataRequired()])
    
class AdicionarControladorForm(FlaskForm):
    nome = StringField('Nome', [validators.Length(min = 3, max = 20), validators.DataRequired()])
    access_code = PasswordField('Password', [validators.DataRequired(), 
        validators.EqualTo('access_code_2', message='Códigos de acesso devem ser iguais')])
    access_code_2 = PasswordField('Repetir Password')