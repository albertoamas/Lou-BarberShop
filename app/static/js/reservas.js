/**
 * Funciones JavaScript para la selección dinámica de fechas y horas en reservas
 */

// Inicialización cuando el DOM está listo
document.addEventListener('DOMContentLoaded', function() {
    // Inicializar selección de fecha si existe
    const fechaInput = document.getElementById('fecha');
    if (fechaInput) {
        initFechaInput(fechaInput);
    }
    
    // Inicializar selección de servicio si existe
    const servicioSelect = document.getElementById('servicio_id');
    if (servicioSelect) {
        initServicioSelect(servicioSelect);
    }
    
    // Inicializar selección de empleado si existe
    const empleadoSelect = document.getElementById('empleado_id');
    if (empleadoSelect) {
        initEmpleadoSelect(empleadoSelect);
    }
});

/**
 * Inicializa el input de fecha con validaciones
 */
function initFechaInput(fechaInput) {
    // Establecer fecha mínima (hoy)
    const hoy = new Date();
    const yyyy = hoy.getFullYear();
    const mm = String(hoy.getMonth() + 1).padStart(2, '0');
    const dd = String(hoy.getDate()).padStart(2, '0');
    const fechaMinima = `${yyyy}-${mm}-${dd}`;
    
    fechaInput.min = fechaMinima;
    
    // Si no hay fecha seleccionada, establecer hoy como valor por defecto
    if (!fechaInput.value) {
        fechaInput.value = fechaMinima;
    }
    
    // Evento para cuando cambia la fecha
    fechaInput.addEventListener('change', function() {
        const fechaSeleccionada = new Date(this.value);
        
        // Validar que no sea domingo (0 es domingo, 6 es sábado)
        if (fechaSeleccionada.getDay() === 0) {
            alert('Lo sentimos, la barbería está cerrada los domingos. Por favor selecciona otro día.');
            // Establecer como fecha mínima o dejar en blanco
            this.value = '';
        }
        
        // Si estamos en la página de selección de hora, actualizar horas disponibles
        actualizarHorasDisponibles();
    });
}

/**
 * Inicializa el select de servicio
 */
function initServicioSelect(servicioSelect) {
    servicioSelect.addEventListener('change', function() {
        // Si estamos en la página de selección de hora, actualizar horas disponibles
        actualizarHorasDisponibles();
    });
}

/**
 * Inicializa el select de empleado
 */
function initEmpleadoSelect(empleadoSelect) {
    empleadoSelect.addEventListener('change', function() {
        // Si estamos en la página de selección de hora, actualizar horas disponibles
        actualizarHorasDisponibles();
    });
}

/**
 * Actualiza las horas disponibles usando la API
 */
function actualizarHorasDisponibles() {
    // Obtener los elementos necesarios
    const servicioSelect = document.getElementById('servicio_id');
    const empleadoSelect = document.getElementById('empleado_id');
    const fechaInput = document.getElementById('fecha');
    const horaSelect = document.getElementById('hora');
    
    // Si no están todos los elementos, no hacer nada
    if (!servicioSelect || !fechaInput || !horaSelect) {
        return;
    }
    
    // Obtener valores seleccionados
    const servicioId = servicioSelect.value;
    const empleadoId = empleadoSelect ? empleadoSelect.value : '';
    const fecha = fechaInput.value;
    
    // Validar que haya valores
    if (!servicioId || !fecha) {
        return;
    }
    
    // Construir URL para la API
    let apiUrl = `/reservas/api/horas-disponibles?servicio_id=${servicioId}&fecha=${fecha}`;
    if (empleadoId) {
        apiUrl += `&empleado_id=${empleadoId}`;
    }
    
    // Hacer la petición AJAX
    fetch(apiUrl)
        .then(response => response.json())
        .then(data => {
            // Limpiar opciones actuales
            horaSelect.innerHTML = '';
            
            // Si hay error, mostrar una opción con el mensaje
            if (data.error) {
                const option = document.createElement('option');
                option.textContent = data.error;
                option.disabled = true;
                horaSelect.appendChild(option);
                return;
            }
            
            // Si no hay horas disponibles
            if (!data.horas || data.horas.length === 0) {
                const option = document.createElement('option');
                option.textContent = 'No hay horarios disponibles';
                option.disabled = true;
                horaSelect.appendChild(option);
                return;
            }
            
            // Agregar las horas disponibles
            data.horas.forEach(hora => {
                const option = document.createElement('option');
                option.value = hora;
                option.textContent = hora;
                horaSelect.appendChild(option);
            });
            
            // Habilitar el select
            horaSelect.disabled = false;
        })
        .catch(error => {
            console.error('Error al obtener horas disponibles:', error);
            
            // Mostrar mensaje de error
            horaSelect.innerHTML = '';
            const option = document.createElement('option');
            option.textContent = 'Error al cargar horarios';
            option.disabled = true;
            horaSelect.appendChild(option);
        });
}
