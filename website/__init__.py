
from flask import Flask
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from config import Config
from flask_wtf import CSRFProtect

db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = 'main.login'
login_manager.login_message_category = 'info'
# csrf = CSRFProtect()
migrate = Migrate()
DB_NAME = "database.db"


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    app.config['SECRET_KEY'] = 'fdghdfgfdg'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['WTF_CSRF_ENABLED'] = True
    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)

    # csrf.init_app(app)
    migrate.init_app(app, db)

    from website.routes import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from website.models import User



    return app
