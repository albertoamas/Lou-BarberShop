from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_required, current_user
from datetime import datetime
from app import db
from app.forms import ReservaForm, BuscarDisponibilidadForm, CancelarReservaForm
from app.models.servicio import Servicio
from app.models.empleado import Empleado
from app.models.reserva import Reserva
from app.services.reserva_service import ReservaService

# Crear blueprint para reservas
reservas_bp = Blueprint('reservas', __name__, url_prefix='/reservas')

@reservas_bp.route('/')
def index():
    """Página principal de reservas - Muestra servicios disponibles"""
    servicios = Servicio.query.all()
    return render_template('reservas/index.html', title='Nuestros Servicios', servicios=servicios)

@reservas_bp.route('/nueva', methods=['GET', 'POST'])
@login_required
def nueva_reserva():
    """Formulario para crear una nueva reserva"""
    form = BuscarDisponibilidadForm()
    
    if form.validate_on_submit():
        servicio_id = form.servicio_id.data
        fecha = form.fecha.data
        
        # Redirigir a la página de selección de hora y empleado
        return redirect(url_for('reservas.seleccionar_hora', 
                              servicio_id=servicio_id,
                              fecha=fecha.strftime('%Y-%m-%d')))
    
    return render_template('reservas/nueva_reserva.html', 
                         title='Nueva Reserva', 
                         form=form)

@reservas_bp.route('/seleccionar-hora')
@login_required
def seleccionar_hora():
    """Página para seleccionar hora y empleado"""
    servicio_id = request.args.get('servicio_id', type=int)
    fecha_str = request.args.get('fecha')
    
    if not servicio_id or not fecha_str:
        flash('Parámetros inválidos', 'danger')
        return redirect(url_for('reservas.nueva_reserva'))
    
    try:
        fecha = datetime.strptime(fecha_str, '%Y-%m-%d').date()
    except ValueError:
        flash('Formato de fecha inválido', 'danger')
        return redirect(url_for('reservas.nueva_reserva'))
    
    # Obtener el servicio
    servicio = Servicio.query.get_or_404(servicio_id)
    
    # Obtener disponibilidad de empleados
    disponibilidad = ReservaService.get_disponibilidad_empleados(fecha, servicio_id)
    
    if not disponibilidad:
        flash('No hay horarios disponibles para la fecha seleccionada', 'warning')
        return redirect(url_for('reservas.nueva_reserva'))
    
    return render_template('reservas/seleccionar_hora.html',
                         title='Seleccionar Hora',
                         servicio=servicio,
                         fecha=fecha,
                         fecha_str=fecha_str,
                         disponibilidad=disponibilidad)

@reservas_bp.route('/confirmar', methods=['GET', 'POST'])
@login_required
def confirmar_reserva():
    """Página para confirmar los detalles de la reserva"""
    # Si se llega por GET, obtener parámetros
    if request.method == 'GET':
        servicio_id = request.args.get('servicio_id', type=int)
        empleado_id = request.args.get('empleado_id', type=int)
        fecha_str = request.args.get('fecha')
        hora = request.args.get('hora')
        
        if not all([servicio_id, empleado_id, fecha_str, hora]):
            flash('Parámetros inválidos', 'danger')
            return redirect(url_for('reservas.nueva_reserva'))
        
        try:
            fecha = datetime.strptime(fecha_str, '%Y-%m-%d').date()
        except ValueError:
            flash('Formato de fecha inválido', 'danger')
            return redirect(url_for('reservas.nueva_reserva'))
        
        # Obtener datos para mostrar
        servicio = Servicio.query.get_or_404(servicio_id)
        empleado = Empleado.query.get_or_404(empleado_id)
        
        return render_template('reservas/confirmar_reserva.html',
                             title='Confirmar Reserva',
                             servicio=servicio,
                             empleado=empleado,
                             fecha=fecha,
                             fecha_str=fecha_str,
                             hora=hora)
    
    # Si se llega por POST, procesar la reserva
    elif request.method == 'POST':
        servicio_id = request.form.get('servicio_id', type=int)
        empleado_id = request.form.get('empleado_id', type=int)
        fecha_str = request.form.get('fecha')
        hora = request.form.get('hora')
        
        if not all([servicio_id, empleado_id, fecha_str, hora]):
            flash('Información incompleta', 'danger')
            return redirect(url_for('reservas.nueva_reserva'))
        
        try:
            fecha = datetime.strptime(fecha_str, '%Y-%m-%d').date()
        except ValueError:
            flash('Formato de fecha inválido', 'danger')
            return redirect(url_for('reservas.nueva_reserva'))
        
        # Crear la reserva
        reserva = ReservaService.crear_reserva(
            cliente_id=current_user.id,
            servicio_id=servicio_id,
            empleado_id=empleado_id,
            fecha=fecha,
            hora=hora
        )
        
        if reserva:
            flash('¡Reserva creada exitosamente!', 'success')
            return redirect(url_for('reservas.mis_reservas'))
        else:
            flash('Error al crear la reserva', 'danger')
            return redirect(url_for('reservas.nueva_reserva'))

@reservas_bp.route('/mis-reservas')
@login_required
def mis_reservas():
    """Muestra las reservas del usuario actual con paginación para el historial"""
    # Obtener página actual para el historial
    page = request.args.get('page', 1, type=int)
    per_page = 5  # 5 registros por página
    
    # Obtener reservas activas (pendientes y confirmadas)
    reservas_activas = Reserva.query.filter_by(cliente_id=current_user.id)\
                               .filter(Reserva.estado.in_(['pendiente', 'confirmada']))\
                               .order_by(Reserva.fecha, Reserva.hora).all()
      # Obtener historial de reservas con paginación (completadas y canceladas)
    historial_paginado = Reserva.query.filter_by(cliente_id=current_user.id)\
                                      .filter(Reserva.estado.in_(['completada', 'cancelada']))\
                                      .order_by(Reserva.fecha.desc(), Reserva.hora.desc())\
                                      .paginate(page=page, per_page=per_page, error_out=False)
    
    return render_template('reservas/mis_reservas.html',
                         title='Mis Reservas',
                         reservas_activas=reservas_activas,
                         historial=historial_paginado.items,
                         historial_paginado=historial_paginado)

@reservas_bp.route('/cancelar/<int:reserva_id>', methods=['GET', 'POST'])
@login_required
def cancelar_reserva(reserva_id):
    """Cancela una reserva existente"""
    # Verificar que la reserva exista y pertenezca al usuario
    reserva = Reserva.query.get_or_404(reserva_id)
    
    if reserva.cliente_id != current_user.id and not current_user.is_admin():
        flash('No tienes permiso para cancelar esta reserva', 'danger')
        return redirect(url_for('reservas.mis_reservas'))
      # Verificar que la reserva esté en estado cancelable
    if reserva.estado not in ['pendiente', 'confirmada']:
        flash('Esta reserva no puede ser cancelada', 'warning')
        return redirect(url_for('reservas.mis_reservas'))
    
    form = CancelarReservaForm()
    
    if form.validate_on_submit():
        print(f"Formulario validado correctamente para reserva {reserva_id}")
        if ReservaService.cancelar_reserva(reserva_id, form.motivo.data):
            flash('Reserva cancelada exitosamente', 'success')
        else:
            flash('Error al cancelar la reserva', 'danger')
        
        return redirect(url_for('reservas.mis_reservas'))
    
    # Agregar logs para debugging
    if request.method == 'POST':
        print(f"Formulario POST recibido pero no validado. Errores: {form.errors}")
        flash('Error en el formulario de cancelación', 'danger')
    
    return render_template('reservas/cancelar_reserva.html',
                         title='Cancelar Reserva',
                         reserva=reserva,
                         form=form)

# Rutas para obtener datos vía AJAX
@reservas_bp.route('/api/horas-disponibles')
def api_horas_disponibles():
    """API para obtener horas disponibles"""
    servicio_id = request.args.get('servicio_id', type=int)
    empleado_id = request.args.get('empleado_id', type=int)
    fecha_str = request.args.get('fecha')
    
    if not servicio_id or not fecha_str:
        return jsonify({'error': 'Parámetros inválidos'}), 400
    
    try:
        fecha = datetime.strptime(fecha_str, '%Y-%m-%d').date()
    except ValueError:
        return jsonify({'error': 'Formato de fecha inválido'}), 400
    
    horas = ReservaService.get_horas_disponibles(fecha, servicio_id, empleado_id)
    
    return jsonify({'horas': horas})
