from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from app.config import Config

# Inicializar las extensiones
db = SQLAlchemy()
migrate = Migrate()

def create_app(config_class=Config):
    """Crear y configurar la aplicación Flask"""
    app = Flask(__name__)
    app.config.from_object(config_class)
      # Inicializar extensiones con la app
    db.init_app(app)
    migrate.init_app(app, db)
      # Inicializar Flask-Login
    from app.auth import login_manager
    login_manager.init_app(app)
    
    # Importar modelos para asegurar que Flask-Migrate los reconozca
    from app.models import Role, Usuario, Servicio, Empleado, Reserva, HorarioNoDisponible
    
    # Registrar blueprints
    from app.routes.main import main_bp
    app.register_blueprint(main_bp)
    
    # Registrar blueprint de autenticación
    from app.routes.auth import auth_bp
    app.register_blueprint(auth_bp)
    
    # Registrar blueprint de reservas
    from app.routes.reservas import reservas_bp
    app.register_blueprint(reservas_bp)
    
    # Registrar blueprint de admin
    from app.routes.admin import admin_bp
    app.register_blueprint(admin_bp)
    
    # Registrar blueprint de API
    from app.routes.api import api_bp
    app.register_blueprint(api_bp, url_prefix='/api')
    
    # Registrar comandos CLI personalizados
    from app.cli import register_commands
    register_commands(app)
    
    @app.route('/test')
    def test_route():
        return {'message': 'La aplicación está funcionando correctamente'}
    
    return app
