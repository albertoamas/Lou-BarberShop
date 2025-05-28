from flask_login import LoginManager
from app.models.usuario import Usuario

login_manager = LoginManager()
login_manager.login_view = 'auth.login'  # Ruta a la que redirigir si se requiere inicio de sesión
login_manager.login_message = 'Por favor inicie sesión para acceder a esta página.'
login_manager.login_message_category = 'info'

@login_manager.user_loader
def load_user(user_id):
    """Carga el usuario desde la base de datos por su ID"""
    return Usuario.query.get(int(user_id))
