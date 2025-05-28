from flask import Blueprint, jsonify

# Crear un Blueprint para las rutas de la API
api_bp = Blueprint('api', __name__)

@api_bp.route('/status')
def status():
    """Ruta para verificar el estado de la API"""
    return jsonify({
        'status': 'success',
        'message': 'API funcionando correctamente'
    })

# En futuros pasos, aquí se agregarán más rutas para la API
