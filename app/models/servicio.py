from app import db

class Servicio(db.Model):
    """Modelo para los servicios ofrecidos por la barbería"""
    __tablename__ = 'servicios'
    
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    duracion = db.Column(db.Integer, nullable=False)  # Duración en minutos
    precio = db.Column(db.Float, nullable=False)
    
    # Relación con la tabla reservas (un servicio puede tener muchas reservas)
    reservas = db.relationship('Reserva', backref='servicio', lazy='dynamic')
    
    def __repr__(self):
        return f'<Servicio {self.nombre}>'
