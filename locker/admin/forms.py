from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, DecimalField, SubmitField, BooleanField
from wtforms import SubmitField, BooleanField, TextAreaField, IntegerField
from wtforms import validators, ValidationError
from .models import User

# Form para Registar Utilizador
class RegisterUser(FlaskForm):
    nome = StringField('Nome', [validators.Length(min = 3, max = 20), validators.DataRequired()])
    email = StringField('Email', [validators.Email(), validators.DataRequired()])
    password = PasswordField('Password', [validators.DataRequired(), 
        validators.EqualTo('password_2', message='Passwords devem ser iguais')])
    password_2 = PasswordField('Repetir Password')

    def validate_email(self, field): # Verificar se email encontra-se registado
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Email já se encontra registado.')

# Editar User Form
class EditarUser(FlaskForm):
    nome = StringField('Nome', [validators.Length(min = 3, max = 20)])
    email = StringField('Email', [validators.DataRequired()])
    password = PasswordField('Password', [validators.EqualTo('password_2', message='Passwords devem ser iguais')])
    password_2 = PasswordField('Repetir Password')


# Form para Login
class LoginUser(FlaskForm):
    email = StringField('Email', [validators.Email(), validators.DataRequired()])
    password = PasswordField('Password', [validators.DataRequired()])