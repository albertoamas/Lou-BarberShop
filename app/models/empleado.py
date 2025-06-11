from app import db

class Empleado(db.Model):
    """Modelo para los empleados (barberos) de la barbería"""
    __tablename__ = 'empleados'
    
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    especialidad = db.Column(db.String(100))
    telefono = db.Column(db.String(20))
    correo = db.Column(db.String(120))
    
    # Relación con la tabla reservas (un empleado puede tener muchas reservas)
    reservas = db.relationship('Reserva', backref='empleado', lazy='dynamic')
    
    # Relación con la tabla horarios no disponibles
    horarios_no_disponibles = db.relationship('HorarioNoDisponible', backref='empleado', lazy='dynamic')
    
    def __repr__(self):
        return f'<Empleado {self.nombre}>'
