# APP/app/__init__.py

from flask import Flask
from app.config import app_config
from flask_bootstrap import Bootstrap
from flask_migrate import Migrate
from .Extensions import db, login_manager
from .Pages import bp as pages_blueprint  # Đổi tên biến để rõ ràng hơn

def create_app(config_name):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(app_config[config_name])
    app.config.from_pyfile('config.py')
    Bootstrap(app)
    db.init_app(app)
    migrate = Migrate(app, db)
    
    # Cấu hình login manager
    login_manager.init_app(app)
    login_manager.login_message = "You must be logged in to access this page."
    login_manager.login_view = "auth.login"

    # Import blueprints
    from app.admin import admin as admin_blueprint
    from app.auth import auth as auth_blueprint
    from app.home import home as home_blueprint

    # Đăng ký các blueprint
    app.register_blueprint(admin_blueprint, url_prefix='/admin')
    app.register_blueprint(auth_blueprint, url_prefix='/auth')
    app.register_blueprint(home_blueprint, url_prefix='/home')
    app.register_blueprint(pages_blueprint)
    
    return app
