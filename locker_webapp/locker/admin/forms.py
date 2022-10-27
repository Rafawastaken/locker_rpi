from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, DecimalField, SubmitField, BooleanField
from wtforms import SubmitField, BooleanField, TextAreaField, IntegerField
from wtforms import validators, ValidationError
from .models import User

# Form para Registar Utilizador
class RegisterUser(FlaskForm):
    nome = StringField('Nome', [validators.Length(min = 4, max = 20), validators.DataRequired()])
    email = StringField('Email', [validators.Email(), validators.DataRequired()])
    contacto = StringField('Contacto', [validators.DataRequired()])
    password = PasswordField('Password', [validators.DataRequired(), 
        validators.EqualTo('password_2', message='Passwords devem ser iguais')])
    password_2 = PasswordField('Repetir Password')
    submit = SubmitField('Adicionar')

# Editar User Form
class EditarUser(FlaskForm):
    nome = StringField('Nome', [validators.Length(min = 3, max = 20)])
    email = StringField('Email', [validators.DataRequired()])
    contacto = StringField('Contacto', [validators.DataRequired()])
    password = PasswordField('Password', [validators.EqualTo('password_2', message='Passwords devem ser iguais')])
    password_2 = PasswordField('Repetir Password')

# Login Form - Loginpip 
class LoginUser(FlaskForm):
    email = StringField('Email', [validators.Email(), validators.DataRequired()])
    password = PasswordField('Password', [validators.DataRequired()])
    submit = SubmitField("Entrar")
