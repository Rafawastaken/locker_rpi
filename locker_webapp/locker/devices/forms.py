from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField, BooleanField, PasswordField
from wtforms import validators, ValidationError

class NovoDispositivoForm(FlaskForm):
    nome = StringField('Nome', [validators.Length(min = 3, max = 20), validators.DataRequired()])
    pin = IntegerField('Número do Pino', [validators.DataRequired()])
    
class DispositivoAutorizadoForm(FlaskForm):
    nome = StringField('Nome', [validators.Length(min = 3, max = 20), validators.DataRequired()])
    access_code = PasswordField('Password', [validators.DataRequired(), 
        validators.EqualTo('password_2', message='Passwords devem ser iguais')])
    access_code_2 = PasswordField('Repetir Password')