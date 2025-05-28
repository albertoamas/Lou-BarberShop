from flask_wtf import FlaskForm
from wtforms import SelectField, DateField, TimeField, HiddenField, SubmitField, StringField
from wtforms.validators import DataRequired, ValidationError
from datetime import datetime, time, timedelta
from app.models.servicio import Servicio
from app.models.empleado import Empleado
from app.models.reserva import Reserva
from app.models.horario_no_disponible import HorarioNoDisponible

class ReservaForm(FlaskForm):
    """Formulario para crear una nueva reserva"""
    servicio_id = SelectField('Servicio', validators=[DataRequired()], coerce=int)
    empleado_id = SelectField('Barbero', validators=[DataRequired()], coerce=int)
    fecha = DateField('Fecha', validators=[DataRequired()], format='%Y-%m-%d')
    hora = SelectField('Hora', validators=[DataRequired()], coerce=str)
    submit = SubmitField('Confirmar Reserva')

    def __init__(self, *args, **kwargs):
        super(ReservaForm, self).__init__(*args, **kwargs)
        
        # Cargar opciones de servicios
        self.servicio_id.choices = [(s.id, f"{s.nombre} - ${s.precio:.2f} ({s.duracion} min)") 
                               for s in Servicio.query.order_by(Servicio.nombre).all()]
        
        # Cargar opciones de empleados
        self.empleado_id.choices = [(e.id, f"{e.nombre} - {e.especialidad}") 
                               for e in Empleado.query.order_by(Empleado.nombre).all()]
        
        # Generar horas disponibles (9:00 AM a 7:00 PM, cada 30 minutos)
        horas_disponibles = []
        hora_actual = time(9, 0)  # 9:00 AM
        hora_final = time(19, 0)  # 7:00 PM
        
        while hora_actual < hora_final:
            hora_str = hora_actual.strftime('%H:%M')
            horas_disponibles.append((hora_str, hora_str))
            
            # Sumar 30 minutos
            hora_datetime = datetime.combine(datetime.today(), hora_actual)
            hora_datetime = hora_datetime + timedelta(minutes=30)
            hora_actual = hora_datetime.time()
        
        self.hora.choices = horas_disponibles
    
    def validate_fecha(self, fecha):
        """Validar que la fecha no sea en el pasado y no sea domingo"""
        hoy = datetime.now().date()
        if fecha.data < hoy:
            raise ValidationError('No puedes reservar para una fecha pasada.')
        
        if fecha.data.weekday() == 6:  # domingo
            raise ValidationError('La barbería está cerrada los domingos.')
    
    def validate_hora(self, hora):
        """Validar que la hora esté dentro del horario de atención"""
        hora_seleccionada = datetime.strptime(hora.data, '%H:%M').time()
        hora_apertura = time(9, 0)  # 9:00 AM
        hora_cierre = time(19, 0)  # 7:00 PM
        
        if hora_seleccionada < hora_apertura or hora_seleccionada >= hora_cierre:
            raise ValidationError('El horario de atención es de 9:00 AM a 7:00 PM.')


class BuscarDisponibilidadForm(FlaskForm):
    """Formulario para buscar disponibilidad de citas"""
    servicio_id = SelectField('Servicio', validators=[DataRequired()], coerce=int)
    fecha = DateField('Fecha', validators=[DataRequired()], format='%Y-%m-%d')
    submit = SubmitField('Buscar Disponibilidad')
    
    def __init__(self, *args, **kwargs):
        super(BuscarDisponibilidadForm, self).__init__(*args, **kwargs)
        
        # Cargar opciones de servicios
        self.servicio_id.choices = [(s.id, f"{s.nombre} - ${s.precio:.2f} ({s.duracion} min)") 
                               for s in Servicio.query.order_by(Servicio.nombre).all()]
    
    def validate_fecha(self, fecha):
        """Validar que la fecha no sea en el pasado y no sea domingo"""
        hoy = datetime.now().date()
        if fecha.data < hoy:
            raise ValidationError('No puedes reservar para una fecha pasada.')
        
        if fecha.data.weekday() == 6:  # domingo
            raise ValidationError('La barbería está cerrada los domingos.')


class CancelarReservaForm(FlaskForm):
    """Formulario para cancelar una reserva"""
    reserva_id = HiddenField('ID de Reserva', validators=[DataRequired()])
    motivo = StringField('Motivo de Cancelación')
    submit = SubmitField('Cancelar Reserva')
