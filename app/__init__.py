from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
import os

db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')

    db.init_app(app)
    migrate.init_app(app, db)

    # Configuración para las rutas de subida de archivos
    app.config['UPLOAD_FOLDER'] = 'app/static/uploads'

    # Asegúrate de que la carpeta de subida exista
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])

    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'main.login'

    @login_manager.user_loader
    def load_user(user_id):
        from app.models import User  # Importar el modelo User aquí
        return User.query.get(int(user_id))  # Asegúrate de que el modelo User esté correctamente definido

    # Import and register blueprints
    from app.routes import main
    app.register_blueprint(main)

    return app
