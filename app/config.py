import os
from dotenv import load_dotenv

# Cargar variables de entorno desde el archivo .env
load_dotenv()

class Config:
    """Configuración base de la aplicación Flask"""
    # Configuración de la base de datos
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'postgresql://postgres:password@localhost:5432/lou_barbershop'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Clave secreta para la seguridad de la aplicación
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'clave-secreta-predeterminada'
    
    # Otras configuraciones
    DEBUG = os.environ.get('FLASK_ENV') == 'development'
    
class DevelopmentConfig(Config):
    """Configuración para entorno de desarrollo"""
    DEBUG = True
    
class ProductionConfig(Config):
    """Configuración para entorno de producción"""
    DEBUG = False
