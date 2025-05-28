from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import db

class Usuario(db.Model, UserMixin):
    """Modelo para los usuarios del sistema (clientes y administradores)"""
    __tablename__ = 'usuarios'
    
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    telefono = db.Column(db.String(20))
    rol_id = db.Column(db.Integer, db.ForeignKey('roles.id'), nullable=False)
    creado_en = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relación con la tabla reservas (un usuario puede tener muchas reservas)
    reservas = db.relationship('Reserva', backref='cliente', lazy='dynamic')
    
    @property
    def password(self):
        """Evita que la contraseña sea accesible directamente"""
        raise AttributeError('La contraseña no es un atributo legible')
    
    @password.setter
    def password(self, password):
        """Establece la contraseña hasheada"""
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        """Verifica la contraseña contra el hash almacenado"""
        return check_password_hash(self.password_hash, password)
    
    def __repr__(self):
        return f'<Usuario {self.email}>'
    
    def is_admin(self):
        """Verifica si el usuario tiene rol de administrador"""
        from app.models.role import Role
        admin_role = Role.query.filter_by(nombre='admin').first()
        return self.rol_id == admin_role.id if admin_role else False
