from flask import Blueprint, render_template
from app.models.servicio import Servicio

# Crear blueprint para servicios
servicios_bp = Blueprint('servicios', __name__, url_prefix='/servicios')

@servicios_bp.route('/')
def index():
    """Página principal de servicios - Muestra catálogo de servicios disponibles"""
    servicios = Servicio.query.all()
    return render_template('servicios/index.html', 
                         title='Nuestros Servicios', 
                         servicios=servicios)
