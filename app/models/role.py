from app import db

class Role(db.Model):
    """Modelo para los roles de usuario en el sistema"""
    __tablename__ = 'roles'
    
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), unique=True, nullable=False)
    
    # Relación con la tabla usuarios (un rol puede tener muchos usuarios)
    usuarios = db.relationship('Usuario', backref='role', lazy='dynamic')
    
    def __repr__(self):
        return f'<Role {self.nombre}>'
