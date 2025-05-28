from flask_migrate import Migrate
from app import create_app, db

# Crear la aplicación Flask
app = create_app()

# Inicializar Flask-Migrate
migrate = Migrate(app, db)

# Importar modelos para asegurar que Flask-Migrate los reconozca
from app.models import Role, Usuario, Servicio, Empleado, Reserva, HorarioNoDisponible

if __name__ == '__main__':
    app.run(debug=True)
