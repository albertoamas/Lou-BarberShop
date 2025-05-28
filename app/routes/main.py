from flask import Blueprint, render_template

# Crear un Blueprint para las rutas principales
main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    """Ruta de la página principal"""
    return render_template('index.html', title='Lou Barbershop - Inicio')

@main_bp.route('/about')
def about():
    """Ruta de la página acerca de nosotros"""
    return render_template('about.html', title='Lou Barbershop - Acerca de')
