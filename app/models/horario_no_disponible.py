from app import db

class HorarioNoDisponible(db.Model):
    """Modelo para los horarios no disponibles (días bloqueados) de empleados"""
    __tablename__ = 'horarios_no_disponibles'
    
    id = db.Column(db.Integer, primary_key=True)
    fecha = db.Column(db.Date, nullable=False)
    motivo = db.Column(db.String(200))
    empleado_id = db.Column(db.Integer, db.ForeignKey('empleados.id'), nullable=False)
    
    def __repr__(self):
        return f'<HorarioNoDisponible {self.fecha} - Empleado {self.empleado_id}>'
