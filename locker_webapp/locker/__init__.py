from ast import Add
from flask import Flask
from flask_sqlalchemy import SQLAlchemy # Base de Dados
from flask_migrate import Migrate # Migrações
from flask_bcrypt import Bcrypt # Criptografia
from flask_login import LoginManager # Login
from flask_restful import Api # Api
from flask_httpauth import HTTPBasicAuth #  Auth
import os

############# * Geral * ############# 

# Consts
DB_NAME = "database.db"
BASEDIR = os.path.abspath(os.path.dirname(__file__))
DATABASE_PATH = f"{BASEDIR}/database/{DB_NAME}"

# Create app
app =  Flask(__name__)

with app.app_context():
    # Configs
    app.config['SECRET_KEY'] = "randompass12333333"
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DATABASE_PATH}'

    # Base de Dados
    db = SQLAlchemy(app)

    # Migrações Base de Dados
    migrate = Migrate(app, db)

    # Encriptar Dados
    bcrypt = Bcrypt(app)

    # Api Auth
    auth = HTTPBasicAuth()

    # Login Manager
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'admin.login'
    login_manager.login_message_category = 'danger'
    login_manager.needs_refresh_message_category ='danger'
    login_manager.login_message = u'Necessário efetuar login para visualizar esta página'


    ############# * Routes * ############# 

    from .home.routes import home
    from .admin.routes import admin
    from .devices.routes import devices
    from .logs.routes import logs
    from .api.api import api_bp

    # Api
    api = Api(api_bp) 

    ############# * Paths * ############# 
    app.register_blueprint(home, url_prefix = '/') # Landing page
    app.register_blueprint(admin, url_prefix = '/utilizadores') # Admin, landing
    app.register_blueprint(devices, url_prefix = '/dispositivos') # Admin, landing
    app.register_blueprint(logs, url_prefix = "/registos") # Registos de abertura de porta
    app.register_blueprint(api_bp) # Api blueprint

    ############# * Models Api * #############
    from .api.api import Status, PatchDeviceStatus, AddLog, GetCreds, AtualizarConfig

    ############# * API Endpoints * #############
    api.add_resource(Status, "/status") # Estadp de dispositivos
    api.add_resource(PatchDeviceStatus, "/device-patch/<string:device_id>") # Alterar estado de dispositivo
    api.add_resource(AddLog, "/registos/adicionar") # Adicionar logs
    api.add_resource(GetCreds, "/config") # Get config
    api.add_resource(AtualizarConfig, "/update-status-config")

