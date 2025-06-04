from app import db
from app.models import Role, Usuario, Servicio, Empleado

def init_db():
    """Inicializar la base de datos con datos básicos"""
    # Crear roles si no existen
    if Role.query.count() == 0:
        roles = [
            Role(nombre='admin'),
            Role(nombre='cliente')
        ]
        db.session.add_all(roles)
        db.session.commit()
        print("Roles creados correctamente")
    
    # Crear usuario administrador si no existe
    admin_role = Role.query.filter_by(nombre='admin').first()
    if admin_role and not Usuario.query.filter_by(email='admin@loubarbershop.com').first():
        admin = Usuario(
            nombre='Administrador',
            email='admin@loubarbershop.com',
            telefono='123456789',
            rol_id=admin_role.id
        )
        admin.password = 'admin123'  # Se hasheará automáticamente
        db.session.add(admin)
        db.session.commit()
        print("Usuario administrador creado correctamente")
      # Crear servicios de ejemplo si no existen
    if Servicio.query.count() == 0:
        servicios = [            Servicio(
                nombre='Corte de cabello',
                descripcion='Corte de cabello profesional adaptado a tu estilo, incluyendo lavado y secado.',
                duracion=45,
                precio=50.00
            ),Servicio(
                nombre='Barba',
                descripcion='Arreglo y perfilado profesional de barba con productos de calidad.',
                duracion=30,
                precio=40.00
            ),
            Servicio(
                nombre='Corte y perfilado de cejas',
                descripcion='Diseño y perfilado de cejas para un look impecable.',
                duracion=20,
                precio=60.00
            ),
            Servicio(
                nombre='Corte y barba',
                descripcion='Servicio combinado de corte de cabello y arreglo de barba.',
                duracion=60,
                precio=70.00
            ),
            Servicio(
                nombre='Servicio completo (corte, barba, cejas)',
                descripcion='Paquete completo que incluye corte de cabello, arreglo de barba y perfilado de cejas.',
                duracion=90,
                precio=80.00
            )
        ]
        db.session.add_all(servicios)
        db.session.commit()
        print("Servicios creados correctamente")
    
    # Crear empleados de ejemplo si no existen
    if Empleado.query.count() == 0:
        empleados = [
            Empleado(nombre='Carlos Rodríguez', especialidad='Cortes Modernos'),
            Empleado(nombre='Javier Méndez', especialidad='Barbas y Afeitados'),
            Empleado(nombre='Miguel Ángel', especialidad='Tratamientos Capilares')
        ]
        db.session.add_all(empleados)
        db.session.commit()
        print("Empleados creados correctamente")
    
    print("Base de datos inicializada correctamente")
