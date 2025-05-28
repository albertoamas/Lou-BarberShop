from app import db
from datetime import datetime

class Reserva(db.Model):
    """Modelo para las reservas de citas en la barbería"""
    __tablename__ = 'reservas'
    
    id = db.Column(db.Integer, primary_key=True)
    cliente_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
    servicio_id = db.Column(db.Integer, db.ForeignKey('servicios.id'), nullable=False)
    empleado_id = db.Column(db.Integer, db.ForeignKey('empleados.id'), nullable=False)
    fecha = db.Column(db.Date, nullable=False)
    hora = db.Column(db.Time, nullable=False)
    estado = db.Column(db.String(20), default='pendiente')  # pendiente, confirmada, cancelada, completada
    creada_en = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<Reserva {self.id} - {self.fecha} {self.hora}>'
    
    @property
    def fecha_hora(self):
        """Retorna la fecha y hora combinadas como un objeto datetime"""
        return datetime.combine(self.fecha, self.hora)
    
    def get_duration(self):
        """Obtiene la duración de la reserva en minutos"""
        return self.servicio.duracion if self.servicio else 0
    
    def cancel(self):
        """Cancela una reserva"""
        self.estado = 'cancelada'
        return True
    
    def confirm(self):
        """Confirma una reserva"""
        self.estado = 'confirmada'
        return True
    
    def complete(self):
        """Marca una reserva como completada"""
        self.estado = 'completada'
        return True
