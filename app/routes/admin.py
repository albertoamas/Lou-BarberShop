from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from functools import wraps
from app import db
from app.models.reserva import Reserva
from app.models.servicio import Servicio
from app.models.empleado import Empleado
from app.models.usuario import Usuario
from app.models.horario_no_disponible import HorarioNoDisponible
from datetime import datetime, date

# Crear blueprint para administración
admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

# Decorador para verificar si el usuario es administrador
def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_admin():
            flash('No tienes permiso para acceder a esta página', 'danger')
            return redirect(url_for('main.index'))
        return f(*args, **kwargs)
    return decorated_function

@admin_bp.route('/')
@login_required
@admin_required
def index():
    """Página principal del panel de administración"""
    # Contar reservas pendientes, confirmadas y completadas
    pendientes = Reserva.query.filter_by(estado='pendiente').count()
    confirmadas = Reserva.query.filter_by(estado='confirmada').count()
    completadas = Reserva.query.filter_by(estado='completada').count()
    
    # Contar clientes totales (usuarios con rol de cliente)
    clientes = Usuario.query.filter_by(rol_id=2).count()  # Asumiendo que rol_id=2 es para clientes
    
    # Contar empleados
    empleados = Empleado.query.count()
    
    # Contar servicios
    servicios = Servicio.query.count()
    
    # Obtener reservas para hoy
    hoy = date.today()
    reservas_hoy = Reserva.query.filter(
        Reserva.fecha == hoy,
        Reserva.estado.in_(['pendiente', 'confirmada'])
    ).order_by(Reserva.hora).all()
    
    return render_template('admin/index.html',
                         title='Panel de Administración',
                         pendientes=pendientes,
                         confirmadas=confirmadas,
                         completadas=completadas,
                         clientes=clientes,
                         empleados=empleados,
                         servicios=servicios,
                         reservas_hoy=reservas_hoy)

@admin_bp.route('/reservas')
@login_required
@admin_required
def reservas():
    """Página para gestionar todas las reservas"""
    # Obtener estado de filtro de la URL
    estado = request.args.get('estado', 'todas')
    
    # Consulta base
    query = Reserva.query
    
    # Aplicar filtro por estado
    if estado != 'todas':
        query = query.filter_by(estado=estado)
    
    # Ordenar por fecha y hora
    reservas = query.order_by(Reserva.fecha.desc(), Reserva.hora).all()
    
    return render_template('admin/reservas.html',
                         title='Gestionar Reservas',
                         reservas=reservas,
                         estado_filtro=estado)

@admin_bp.route('/reservas/confirmar/<int:reserva_id>')
@login_required
@admin_required
def confirmar_reserva(reserva_id):
    """Confirma una reserva pendiente"""
    reserva = Reserva.query.get_or_404(reserva_id)
    
    if reserva.estado != 'pendiente':
        flash('Solo se pueden confirmar reservas pendientes', 'warning')
    else:
        reserva.estado = 'confirmada'
        db.session.commit()
        flash('Reserva confirmada exitosamente', 'success')
    
    return redirect(url_for('admin.reservas'))

@admin_bp.route('/reservas/completar/<int:reserva_id>')
@login_required
@admin_required
def completar_reserva(reserva_id):
    """Marca una reserva como completada"""
    reserva = Reserva.query.get_or_404(reserva_id)
    
    if reserva.estado not in ['pendiente', 'confirmada']:
        flash('No se puede marcar como completada esta reserva', 'warning')
    else:
        reserva.estado = 'completada'
        db.session.commit()
        flash('Reserva marcada como completada exitosamente', 'success')
    
    return redirect(url_for('admin.reservas'))

@admin_bp.route('/reservas/cancelar/<int:reserva_id>')
@login_required
@admin_required
def cancelar_reserva(reserva_id):
    """Cancela una reserva"""
    reserva = Reserva.query.get_or_404(reserva_id)
    
    if reserva.estado not in ['pendiente', 'confirmada']:
        flash('No se puede cancelar esta reserva', 'warning')
    else:
        reserva.estado = 'cancelada'
        db.session.commit()
        flash('Reserva cancelada exitosamente', 'success')
    
    return redirect(url_for('admin.reservas'))

@admin_bp.route('/horarios-no-disponibles')
@login_required
@admin_required
def horarios_no_disponibles():
    """Página para gestionar horarios no disponibles"""
    horarios = HorarioNoDisponible.query.order_by(HorarioNoDisponible.fecha).all()
    empleados = Empleado.query.all()
    
    return render_template('admin/horarios_no_disponibles.html',
                         title='Horarios No Disponibles',
                         horarios=horarios,
                         empleados=empleados)

@admin_bp.route('/horarios-no-disponibles/agregar', methods=['POST'])
@login_required
@admin_required
def agregar_horario_no_disponible():
    """Agrega un nuevo horario no disponible"""
    fecha_str = request.form.get('fecha')
    motivo = request.form.get('motivo')
    empleado_id = request.form.get('empleado_id', type=int)
    
    if not fecha_str or not motivo or not empleado_id:
        flash('Todos los campos son obligatorios', 'danger')
        return redirect(url_for('admin.horarios_no_disponibles'))
    
    try:
        fecha = datetime.strptime(fecha_str, '%Y-%m-%d').date()
    except ValueError:
        flash('Formato de fecha inválido', 'danger')
        return redirect(url_for('admin.horarios_no_disponibles'))
    
    # Verificar si ya existe un horario no disponible para esta fecha y empleado
    existente = HorarioNoDisponible.query.filter_by(
        fecha=fecha,
        empleado_id=empleado_id
    ).first()
    
    if existente:
        flash('Ya existe un horario no disponible para esta fecha y empleado', 'warning')
        return redirect(url_for('admin.horarios_no_disponibles'))
    
    # Verificar si hay reservas para esta fecha y empleado
    reservas = Reserva.query.filter(
        Reserva.fecha == fecha,
        Reserva.empleado_id == empleado_id,
        Reserva.estado.in_(['pendiente', 'confirmada'])
    ).all()
    
    if reservas:
        flash('No se puede bloquear esta fecha porque hay reservas programadas', 'warning')
        return redirect(url_for('admin.horarios_no_disponibles'))
    
    # Crear el horario no disponible
    horario = HorarioNoDisponible(
        fecha=fecha,
        motivo=motivo,
        empleado_id=empleado_id
    )
    
    db.session.add(horario)
    db.session.commit()
    
    flash('Horario no disponible agregado exitosamente', 'success')
    return redirect(url_for('admin.horarios_no_disponibles'))

@admin_bp.route('/horarios-no-disponibles/eliminar/<int:horario_id>')
@login_required
@admin_required
def eliminar_horario_no_disponible(horario_id):
    """Elimina un horario no disponible"""
    horario = HorarioNoDisponible.query.get_or_404(horario_id)
    
    db.session.delete(horario)
    db.session.commit()
    
    flash('Horario no disponible eliminado exitosamente', 'success')
    return redirect(url_for('admin.horarios_no_disponibles'))

@admin_bp.route('/servicios')
@login_required
@admin_required
def servicios():
    """Página para gestionar servicios"""
    servicios = Servicio.query.order_by(Servicio.nombre).all()
    
    return render_template('admin/servicios.html',
                         title='Gestionar Servicios',
                         servicios=servicios)

@admin_bp.route('/servicios/agregar', methods=['POST'])
@login_required
@admin_required
def agregar_servicio():
    """Agrega un nuevo servicio"""
    nombre = request.form.get('nombre')
    descripcion = request.form.get('descripcion')
    precio = request.form.get('precio', type=float)
    duracion = request.form.get('duracion', type=int)
    
    if not all([nombre, descripcion, precio, duracion]):
        flash('Todos los campos son obligatorios', 'danger')
        return redirect(url_for('admin.servicios'))
    
    # Crear el servicio
    servicio = Servicio(
        nombre=nombre,
        descripcion=descripcion,
        precio=precio,
        duracion=duracion
    )
    
    db.session.add(servicio)
    db.session.commit()
    
    flash('Servicio agregado exitosamente', 'success')
    return redirect(url_for('admin.servicios'))

@admin_bp.route('/servicios/editar/<int:servicio_id>', methods=['POST'])
@login_required
@admin_required
def editar_servicio(servicio_id):
    """Edita un servicio existente"""
    servicio = Servicio.query.get_or_404(servicio_id)
    
    nombre = request.form.get('nombre')
    descripcion = request.form.get('descripcion')
    precio = request.form.get('precio', type=float)
    duracion = request.form.get('duracion', type=int)
    
    if not all([nombre, descripcion, precio, duracion]):
        flash('Todos los campos son obligatorios', 'danger')
        return redirect(url_for('admin.servicios'))
    
    # Actualizar el servicio
    servicio.nombre = nombre
    servicio.descripcion = descripcion
    servicio.precio = precio
    servicio.duracion = duracion
    
    db.session.commit()
    
    flash('Servicio actualizado exitosamente', 'success')
    return redirect(url_for('admin.servicios'))

@admin_bp.route('/servicios/eliminar/<int:servicio_id>')
@login_required
@admin_required
def eliminar_servicio(servicio_id):
    """Elimina un servicio"""
    servicio = Servicio.query.get_or_404(servicio_id)
    
    # Verificar si hay reservas asociadas a este servicio
    reservas = Reserva.query.filter_by(servicio_id=servicio_id).count()
    
    if reservas > 0:
        flash('No se puede eliminar este servicio porque tiene reservas asociadas', 'warning')
        return redirect(url_for('admin.servicios'))
    
    db.session.delete(servicio)
    db.session.commit()
    
    flash('Servicio eliminado exitosamente', 'success')
    return redirect(url_for('admin.servicios'))

@admin_bp.route('/empleados')
@login_required
@admin_required
def empleados():
    """Página para gestionar empleados"""
    empleados = Empleado.query.order_by(Empleado.nombre).all()
    
    return render_template('admin/empleados.html',
                         title='Gestionar Empleados',
                         empleados=empleados)

@admin_bp.route('/empleados/agregar', methods=['POST'])
@login_required
@admin_required
def agregar_empleado():
    """Agrega un nuevo empleado"""
    nombre = request.form.get('nombre')
    especialidad = request.form.get('especialidad')
    telefono = request.form.get('telefono')
    correo = request.form.get('correo')
    
    if not all([nombre, especialidad]):
        flash('Nombre y especialidad son obligatorios', 'danger')
        return redirect(url_for('admin.empleados'))
    
    # Crear el empleado
    empleado = Empleado(
        nombre=nombre,
        especialidad=especialidad,
        telefono=telefono if telefono else None,
        correo=correo if correo else None
    )
    
    db.session.add(empleado)
    db.session.commit()
    
    flash('Empleado agregado exitosamente', 'success')
    return redirect(url_for('admin.empleados'))

@admin_bp.route('/empleados/editar/<int:empleado_id>', methods=['POST'])
@login_required
@admin_required
def editar_empleado(empleado_id):
    """Edita un empleado existente"""
    empleado = Empleado.query.get_or_404(empleado_id)
    
    nombre = request.form.get('nombre')
    especialidad = request.form.get('especialidad')
    telefono = request.form.get('telefono')
    correo = request.form.get('correo')
    
    if not all([nombre, especialidad]):
        flash('Nombre y especialidad son obligatorios', 'danger')
        return redirect(url_for('admin.empleados'))
    
    # Actualizar el empleado
    empleado.nombre = nombre
    empleado.especialidad = especialidad
    empleado.telefono = telefono if telefono else None
    empleado.correo = correo if correo else None
    
    db.session.commit()
    
    flash('Empleado actualizado exitosamente', 'success')
    return redirect(url_for('admin.empleados'))

@admin_bp.route('/empleados/eliminar/<int:empleado_id>')
@login_required
@admin_required
def eliminar_empleado(empleado_id):
    """Elimina un empleado"""
    empleado = Empleado.query.get_or_404(empleado_id)
    
    # Verificar si el empleado tiene reservas asociadas
    reservas = Reserva.query.filter_by(empleado_id=empleado_id).first()
    if reservas:
        flash('No se puede eliminar el empleado porque tiene reservas asociadas', 'warning')
        return redirect(url_for('admin.empleados'))
    
    db.session.delete(empleado)
    db.session.commit()
    
    flash('Empleado eliminado exitosamente', 'success')
    return redirect(url_for('admin.empleados'))
