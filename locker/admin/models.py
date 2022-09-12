from locker import db, login_manager
from flask_login import UserMixin

# Login manager
@login_manager.user_loader
def user_loader(user_id):
    return User.query.get(user_id)

# Tabela de Users
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(50),unique=False, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(180),unique=False, nullable=False)
    
    def __repr__(self):
        return '<User %r>' % self.nome

db.create_all()