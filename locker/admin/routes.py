from flask import Blueprint, render_template, flash, redirect, url_for, request, session
from flask_login import login_required, current_user, logout_user, login_user
from locker import app, db, bcrypt
from .forms import RegisterUser, EditarUser, LoginUser
from .models import User

admin = Blueprint('admin', __name__)


#################### * Helpers * ####################

# Flash errors
def flash_erros(erros):
    print(erros)
    for key, values in erros:
        for value in values:
            flash(f'{value}', "danger")


#################### * Utilizadores * ####################

# Lista de Utilizadores
@admin.route('/')
@login_required
def utilizadores():
    title = "Lista de Utilizadores Autorizados"
    users = User.query.all()
    return render_template('/admin/users.html', title = title, users = users)

# Registar Route
@admin.route('/adicionar', methods = ['POST', 'GET'])
def registar():
    title = "Registar Utilizador"
    form = RegisterUser()

    if form.validate_on_submit():
        hash_password = bcrypt.generate_password_hash(form.password.data)
        novo_user = User(
            nome = form.nome.data,
            email = form.email.data,
            password = hash_password
        )
        db.session.add(novo_user)
        db.session.commit()

        flash(f"{form.nome.data} adicionado aos utilizadores!", "success")
        return redirect(url_for('admin.utilizadores'))
    return render_template('/admin/registar.html', form = form, title = title)


# Editar utilizador
@admin.route('/editar/<int:id>', methods = ['POST', 'GET'])
@login_required
def editar(id):
    user = User.query.get_or_404(id)
    title = f"Editar Perfil de {user.nome}"
    form = EditarUser()
    
    if user and form.validate_on_submit():
        user.nome = form.nome.data
        user.email = form.email.data
        user.password = bcrypt.generate_password_hash(form.password.data)
        db.session.commit()

        flash(f"Utilizador {form.nome.data} atualizado com sucesso!", "success")
        return redirect(url_for('admin.utilizadores'))
    else: # Caso erro ao adicionar user 
        flash_erros(form.errors.items())

    return render_template('/admin/editar.html',user = user, title = title, form = form) 

# Apagar Utilizador
@admin.route('/apagar-user/<int:id>', methods = ["POST"])
@login_required
def apagar(id):
    user = User.query.get_or_404(id)
    if user and user.id != current_user.id:
        db.session.delete(user)
        db.session.commit()
        flash("Utilizador removido com sucesso", "success")
        return redirect(url_for('admin.utilizadores'))
    return redirect(url_for('admin.utilizadores'))
    

#################### * Session Manager * ####################

# Login Utilizador
@admin.route('/login', methods = ['POST', 'GET'])
def login():
    title = "Login | Tek4Door"
    form = LoginUser()
    if form.validate_on_submit():
        user = User.query.filter_by(email = form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            flash(f'Bem-Vindo {user.nome}', 'success')
            next = request.args.get('next')
            return redirect(next or url_for('home.landing'))
        else:
            flash_erros(form.errors.items())
            return redirect(url_for("admin.login"))
    return render_template('/admin/login.html', title = title, form = form)

# Logout
@admin.route('/logout')
@login_required
def logout():
    logout_user()
    flash("Sessão terminada com sucesso", "success")
    return redirect(url_for("admin.login"))