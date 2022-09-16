from flask import Flask
from flask_sqlalchemy import SQLAlchemy # Base de Dados
from flask_migrate import Migrate # Migrações
from flask_bcrypt import Bcrypt # Criptografia
from flask_login import LoginManager # Login
from flask_restful import Api # Api
import os

############# * Geral * ############# 

# Consts
DB_NAME = "database.db"
BASEDIR = os.path.abspath(os.path.dirname(__file__))
DATABASE_PATH = f"{BASEDIR}/database/{DB_NAME}"

# Create app
app =  Flask(__name__)

# Configs
app.config['SECRET_KEY'] = "randompass12333333"
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DATABASE_PATH}'

# Base de Dados
db = SQLAlchemy(app)

# Migrações Base de Dados
migrate = Migrate(app, db)

# Encriptar Dados
bcrypt = Bcrypt(app)

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
from .api.api import api_bp

# Api
api = Api(api_bp) 

############# * Paths * ############# 
app.register_blueprint(home, url_prefix = '/') # Landing page
app.register_blueprint(admin, url_prefix = '/utilizadores') # Admin, landing
app.register_blueprint(devices, url_prefix = '/dispositivos') # Admin, landing
app.register_blueprint(api_bp)

############# * Models Api * #############
from .api.api import GetDeviceStatus, PatchDeviceStatus

############# * API Endpoints * #############
api.add_resource(GetDeviceStatus, "/devices_status")
api.add_resource(PatchDeviceStatus, "/device_patch/<int:device_pin>")