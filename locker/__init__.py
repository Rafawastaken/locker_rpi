from flask import Flask
from flask_sqlalchemy import SQLAlchemy # Base de Dados
from flask_migrate import Migrate # Migrações
from flask_login import LoginManager # Gestor de Sessões

############# * Geral * ############# 

# Create app
app =  Flask(__name__)

# Base de Dados
db = SQLAlchemy(app)

# Configs
from . import config

# Iniciar Base de Dados
db.init_app(app)

# Migrações Base de Dados
migrate = Migrate(app, db)

# Encriptar Dados
# bcrypt = Bcrypt(app)

# Gestor de Sessões
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "admin.login"
login_manager.login_message_category = 'danger'
login_manager.needs_refresh_message_category ='danger'
login_manager.login_message = u'Necessário efetuar login para visualizar a página solicitada'

############# * Routes * ############# 

from .home.routes import home
from .admin.routes import admin


############# * Paths * ############# 
app.register_blueprint(home, url_prefix = '/') # Landing page
app.register_blueprint(admin, url_prefix = '/utilizadores') # Admin, landing