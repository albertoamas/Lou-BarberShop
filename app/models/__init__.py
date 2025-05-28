# Este archivo permite que la carpeta models sea reconocida como un paquete Python
# Importar todos los modelos para que Flask-Migrate los detecte
from app.models.role import Role
from app.models.usuario import Usuario
from app.models.servicio import Servicio
from app.models.empleado import Empleado
from app.models.reserva import Reserva
from app.models.horario_no_disponible import HorarioNoDisponible

# Exportar los modelos para que estén disponibles al importar el paquete
__all__ = ['Role', 'Usuario', 'Servicio', 'Empleado', 'Reserva', 'HorarioNoDisponible']
