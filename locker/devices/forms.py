from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField, BooleanField
from wtforms import validators, ValidationError

class NovoDispositivoForm(FlaskForm):
    nome = StringField('Nome', [validators.Length(min = 3, max = 20), validators.DataRequired()])
    pin = IntegerField('Número do Pino', [validators.DataRequired()])
    