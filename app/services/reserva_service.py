from datetime import datetime, time, timedelta
from app import db
from app.models.reserva import Reserva
from app.models.servicio import Servicio
from app.models.empleado import Empleado
from app.models.horario_no_disponible import HorarioNoDisponible

class ReservaService:
    """Servicio para gestionar las reservas y disponibilidad"""
    
    @staticmethod
    def get_horas_disponibles(fecha, servicio_id, empleado_id=None):
        """
        Obtiene las horas disponibles para una fecha, servicio y empleado específicos
        
        Args:
            fecha: La fecha para la que se buscan horas disponibles
            servicio_id: ID del servicio seleccionado
            empleado_id: ID del empleado (opcional)
            
        Returns:
            Una lista de horas disponibles en formato HH:MM
        """
        # Obtener duración del servicio
        servicio = Servicio.query.get(servicio_id)
        if not servicio:
            return []
        
        duracion_servicio = servicio.duracion  # en minutos
        
        # Definir horario de atención
        hora_apertura = time(9, 0)  # 9:00 AM
        hora_cierre = time(19, 0)  # 7:00 PM
        
        # Generar todas las horas posibles cada 30 minutos
        horas_posibles = []
        hora_actual = time(9, 0)
        
        while hora_actual < hora_cierre:
            # Verificar que la reserva completa termine antes del cierre
            hora_fin = (datetime.combine(datetime.today(), hora_actual) + 
                      timedelta(minutes=duracion_servicio)).time()
            
            if hora_fin <= hora_cierre:
                horas_posibles.append(hora_actual.strftime('%H:%M'))
            
            # Sumar 30 minutos
            hora_datetime = datetime.combine(datetime.today(), hora_actual)
            hora_datetime = hora_datetime + timedelta(minutes=30)
            hora_actual = hora_datetime.time()
        
        # Filtrar horas ocupadas por reservas existentes
        horas_ocupadas = set()
        
        # Consulta base para reservas existentes
        query = Reserva.query.filter(Reserva.fecha == fecha, 
                                    Reserva.estado.in_(['pendiente', 'confirmada']))
        
        # Si se especificó un empleado, filtrar por él
        if empleado_id:
            query = query.filter(Reserva.empleado_id == empleado_id)
            
            # También verificar si el empleado tiene horarios no disponibles
            horarios_bloqueados = HorarioNoDisponible.query.filter(
                HorarioNoDisponible.empleado_id == empleado_id,
                HorarioNoDisponible.fecha == fecha
            ).all()
            
            if horarios_bloqueados:
                # Si hay días bloqueados para este empleado, no hay horas disponibles
                return []
        
        # Obtener todas las reservas para la fecha y empleados seleccionados
        reservas = query.all()
        
        # Marcar las horas que se solapan con reservas existentes
        for reserva in reservas:
            # Obtener duración del servicio de la reserva
            duracion_reserva = reserva.servicio.duracion
            
            # Calcular la hora de fin de la reserva
            inicio_reserva = datetime.combine(fecha, reserva.hora)
            fin_reserva = inicio_reserva + timedelta(minutes=duracion_reserva)
            
            # Marcar como ocupadas todas las horas que caen dentro de la reserva
            for hora in horas_posibles:
                hora_dt = datetime.strptime(hora, '%H:%M').time()
                hora_dt = datetime.combine(fecha, hora_dt)
                
                # Si la hora cae dentro del período de la reserva existente
                if inicio_reserva <= hora_dt < fin_reserva:
                    horas_ocupadas.add(hora)
                
                # Si el servicio seleccionado no cabría antes del inicio de la reserva
                if hora_dt <= inicio_reserva and hora_dt + timedelta(minutes=duracion_servicio) > inicio_reserva:
                    horas_ocupadas.add(hora)
        
        # Devolver las horas disponibles
        return [hora for hora in horas_posibles if hora not in horas_ocupadas]
    
    @staticmethod
    def get_disponibilidad_empleados(fecha, servicio_id):
        """
        Obtiene la disponibilidad de todos los empleados para una fecha y servicio
        
        Args:
            fecha: La fecha para la que se busca disponibilidad
            servicio_id: ID del servicio seleccionado
            
        Returns:
            Un diccionario con empleado_id como clave y lista de horas disponibles como valor
        """
        empleados = Empleado.query.all()
        disponibilidad = {}
        
        for empleado in empleados:
            horas = ReservaService.get_horas_disponibles(fecha, servicio_id, empleado.id)
            if horas:
                disponibilidad[empleado.id] = {
                    'nombre': empleado.nombre,
                    'especialidad': empleado.especialidad,
                    'horas': horas
                }
        
        return disponibilidad
    
    @staticmethod
    def crear_reserva(cliente_id, servicio_id, empleado_id, fecha, hora):
        """
        Crea una nueva reserva
        
        Args:
            cliente_id: ID del cliente
            servicio_id: ID del servicio
            empleado_id: ID del empleado
            fecha: Fecha de la reserva
            hora: Hora de la reserva (string en formato HH:MM)
            
        Returns:
            La reserva creada o None si hubo un error
        """
        try:
            # Convertir hora string a objeto time
            hora_obj = datetime.strptime(hora, '%H:%M').time()
            
            # Crear nueva reserva
            reserva = Reserva(
                cliente_id=cliente_id,
                servicio_id=servicio_id,
                empleado_id=empleado_id,
                fecha=fecha,
                hora=hora_obj,
                estado='pendiente'
            )
            
            db.session.add(reserva)
            db.session.commit()
            
            return reserva
        except Exception as e:
            db.session.rollback()
            print(f"Error al crear reserva: {e}")
            return None
    
    @staticmethod
    def cancelar_reserva(reserva_id, motivo=None):
        """
        Cancela una reserva existente
        
        Args:
            reserva_id: ID de la reserva a cancelar
            motivo: Motivo de cancelación (opcional)
            
        Returns:
            True si la operación fue exitosa, False en caso contrario
        """
        try:
            reserva = Reserva.query.get(reserva_id)
            if not reserva:
                return False
            
            reserva.estado = 'cancelada'
            # Si se proporcionó un motivo, podríamos agregarlo a la reserva
            # Por ahora no hay un campo para esto en el modelo
            
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            print(f"Error al cancelar reserva: {e}")
            return False
