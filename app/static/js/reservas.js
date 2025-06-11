/**
 * Funciones JavaScript para la selección dinámica de fechas y horas en reservas
 */

// Inicialización cuando el DOM está listo
document.addEventListener('DOMContentLoaded', function() {    // Inicializar selección de fecha si existe
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
    
    // Nuevas funciones para la página mejorada
    initServiceCardInteraction();
    initFormEnhancements();
    initProgressStep();
    addScrollAnimations();
    initNewBookingPageFeatures();
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
    }    // Evento para cuando cambia la fecha
    fechaInput.addEventListener('change', function() {
        // Usar una fecha local sin problemas de timezone
        const fechaSeleccionada = new Date(this.value + 'T00:00:00');
        
        // Validar que no sea domingo (0 es domingo, 6 es sábado)
        if (fechaSeleccionada.getDay() === 0) {
            // Limpiar el valor y mostrar error en el formulario
            this.value = '';
            
            // Buscar la sección del formulario y mostrar el error
            const formSection = this.closest('.form-section');
            if (formSection) {
                const errorMessage = formSection.querySelector('.error-message');
                if (errorMessage) {
                    errorMessage.innerHTML = '<i class="fas fa-exclamation-circle"></i> La barbería está cerrada los domingos';
                    errorMessage.style.display = 'block';
                }
                this.classList.add('error');
            }
            return;
        }
        
        // Si la fecha es válida, remover errores
        const formSection = this.closest('.form-section');
        if (formSection) {
            const errorMessage = formSection.querySelector('.error-message');
            if (errorMessage) {
                errorMessage.style.display = 'none';
            }
            this.classList.remove('error');
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
    // Obtener los elementos necesarios    const servicioSelect = document.getElementById('servicio_id');
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

// ==================== FUNCIONES PARA LA NUEVA PÁGINA DE AGENDA TU CITA ====================

/**
 * Funciones para mejorar la interactividad de la página de reservas
 */

/**
 * Inicializa la interacción con las tarjetas de servicios
 */
function initServiceCardInteraction() {
    const serviceCards = document.querySelectorAll('.service-card-modern');
    const servicioSelect = document.getElementById('servicio_id');
    
    if (!serviceCards.length || !servicioSelect) return;
    
    // Agregar event listeners a las tarjetas
    serviceCards.forEach(card => {
        card.addEventListener('click', function() {
            const serviceId = this.getAttribute('data-service-id');
            
            // Remover selección anterior
            serviceCards.forEach(c => c.classList.remove('selected'));
            
            // Agregar selección a la tarjeta actual
            this.classList.add('selected');
            
            // Actualizar el select
            servicioSelect.value = serviceId;
            
            // Animar la tarjeta seleccionada
            this.style.transform = 'scale(1.02)';
            setTimeout(() => {
                this.style.transform = '';
            }, 200);
            
            // Actualizar el progreso
            updateProgressStep(2);
        });
    });
    
    // Sincronizar selección inicial si hay valor en el select
    if (servicioSelect.value) {
        const selectedCard = document.querySelector(`[data-service-id="${servicioSelect.value}"]`);
        if (selectedCard) {
            selectedCard.classList.add('selected');
        }
    }
    
    // Evento para cuando cambia el select directamente
    servicioSelect.addEventListener('change', function() {
        serviceCards.forEach(c => c.classList.remove('selected'));
        
        const selectedCard = document.querySelector(`[data-service-id="${this.value}"]`);
        if (selectedCard) {
            selectedCard.classList.add('selected');
        }
    });
}

/**
 * Mejoras en el formulario
 */
function initFormEnhancements() {
    const form = document.querySelector('.appointment-form');
    const inputs = form?.querySelectorAll('input, select');
    
    if (!form || !inputs.length) return;
    
    // Agregar efectos de focus a los inputs
    inputs.forEach(input => {
        // Efecto de onda al hacer focus
        input.addEventListener('focus', function() {
            this.parentElement.classList.add('focused');
            
            // Crear efecto de onda
            createRippleEffect(this);
        });
        
        input.addEventListener('blur', function() {
            this.parentElement.classList.remove('focused');
        });
        
        // Validación en tiempo real
        input.addEventListener('input', function() {
            validateField(this);
        });
    });
    
    // Validación al enviar el formulario
    form.addEventListener('submit', function(e) {
        const isValid = validateForm();
        if (!isValid) {
            e.preventDefault();
            showValidationErrors();
        } else {
            // Mostrar loading en el botón
            const submitBtn = this.querySelector('.submit-btn');
            if (submitBtn) {
                submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin me-2"></i>Procesando...';
                submitBtn.disabled = true;
            }
        }
    });
}

/**
 * Crea un efecto de onda en el elemento
 */
function createRippleEffect(element) {
    const ripple = document.createElement('span');
    ripple.classList.add('ripple');
    
    const rect = element.getBoundingClientRect();
    const size = Math.max(rect.width, rect.height);
    
    ripple.style.width = ripple.style.height = size + 'px';
    ripple.style.left = (rect.width / 2 - size / 2) + 'px';
    ripple.style.top = (rect.height / 2 - size / 2) + 'px';
    
    element.style.position = 'relative';
    element.appendChild(ripple);
    
    setTimeout(() => {
        ripple.remove();
    }, 1000);
}

/**
 * Valida un campo individual
 */
function validateField(field) {
    const value = field.value.trim();
    const fieldName = field.name;
    
    // Remover clases de validación previas
    field.classList.remove('is-valid', 'is-invalid');
    
    let isValid = true;
    
    switch (fieldName) {
        case 'servicio_id':
            isValid = value !== '';
            break;
        case 'fecha':
            isValid = value !== '' && new Date(value) >= new Date().setHours(0,0,0,0);
            break;
    }
    
    // Agregar clase de validación
    field.classList.add(isValid ? 'is-valid' : 'is-invalid');
    
    return isValid;
}

/**
 * Valida todo el formulario
 */
function validateForm() {
    const form = document.querySelector('.appointment-form');
    const requiredFields = form.querySelectorAll('[required]');
    
    let isValid = true;
    
    requiredFields.forEach(field => {
        if (!validateField(field)) {
            isValid = false;
        }
    });
    
    return isValid;
}

/**
 * Muestra errores de validación
 */
function showValidationErrors() {
    const invalidFields = document.querySelectorAll('.is-invalid');
    
    if (invalidFields.length > 0) {
        // Scroll al primer campo inválido
        invalidFields[0].scrollIntoView({ 
            behavior: 'smooth', 
            block: 'center' 
        });
        
        // Mostrar notificación
        showNotification('Por favor, completa todos los campos requeridos', 'error');
    }
}

/**
 * Actualiza el paso del progreso
 */
function updateProgressStep(step) {
    const steps = document.querySelectorAll('.step');
    
    steps.forEach((stepElement, index) => {
        if (index < step) {
            stepElement.classList.add('active');
        } else {
            stepElement.classList.remove('active');
        }
    });
}

/**
 * Inicializa el progreso inicial
 */
function initProgressStep() {
    const servicioSelect = document.getElementById('servicio_id');
    const fechaInput = document.querySelector('.custom-date');
    
    // Verificar qué campos están completados
    if (servicioSelect?.value) {
        updateProgressStep(2);
    }
    
    if (fechaInput?.value) {
        updateProgressStep(3);
    }
    
    // Eventos para actualizar el progreso
    servicioSelect?.addEventListener('change', () => {
        if (servicioSelect.value) {
            updateProgressStep(2);
        }
    });
    
    fechaInput?.addEventListener('change', () => {
        if (fechaInput.value) {
            updateProgressStep(3);
        }
    });
}

/**
 * Añade animaciones al hacer scroll
 */
function addScrollAnimations() {
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };
    
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                // Agregar animación sin crear nuevos contextos de apilamiento
                entry.target.style.opacity = '1';
                entry.target.style.transform = 'translateY(0)';
                entry.target.style.transition = 'all 0.6s ease-out';
                observer.unobserve(entry.target);
            }
        });
    }, observerOptions);
    
    // Observar elementos para animar (evitar conflictos con navbar)
    const elementsToAnimate = document.querySelectorAll(
        '.appointment-form-card, .services-panel, .service-card-modern'
    );
    
    elementsToAnimate.forEach(el => {
        // Configurar estado inicial sin afectar z-index
        el.style.opacity = '0';
        el.style.transform = 'translateY(30px)'; // Reducir desplazamiento
        el.style.transition = 'none'; // Prevenir transiciones iniciales
        observer.observe(el);
    });
}

/**
 * Muestra notificaciones al usuario
 */
function showNotification(message, type = 'info') {
    // Crear elemento de notificación
    const notification = document.createElement('div');
    notification.className = `notification notification-${type}`;
    notification.innerHTML = `
        <div class="notification-content">
            <i class="fas fa-${type === 'error' ? 'exclamation-circle' : 'info-circle'} me-2"></i>
            <span>${message}</span>
        </div>
        <button class="notification-close" onclick="this.parentElement.remove()">
            <i class="fas fa-times"></i>
        </button>
    `;
      // Estilos inline para la notificación
    notification.style.cssText = `
        position: fixed;
        top: 80px;
        right: 20px;
        padding: 1rem 1.5rem;
        border-radius: 10px;
        color: white;
        z-index: 9998;
        display: flex;
        align-items: center;
        justify-content: space-between;
        min-width: 300px;
        animation: slideIn 0.3s ease-out;
        background: ${type === 'error' ? '#dc3545' : '#17a2b8'};
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
    `;
    
    document.body.appendChild(notification);
    
    // Auto-remover después de 5 segundos
    setTimeout(() => {
        if (notification.parentElement) {
            notification.style.animation = 'slideOut 0.3s ease-in';
            setTimeout(() => notification.remove(), 300);
        }
    }, 5000);
}

// Estilos CSS adicionales para las notificaciones y efectos
const additionalStyles = `
@keyframes slideIn {
    from { transform: translateX(100%); opacity: 0; }
    to { transform: translateX(0); opacity: 1; }
}

@keyframes slideOut {
    from { transform: translateX(0); opacity: 1; }
    to { transform: translateX(100%); opacity: 0; }
}

.ripple {
    position: absolute;
    border-radius: 50%;
    background: rgba(255, 255, 255, 0.6);
    transform: scale(0);
    animation: ripple-animation 1s linear;
    pointer-events: none;
}

@keyframes ripple-animation {
    to {
        transform: scale(4);
        opacity: 0;
    }
}

.notification-close {
    background: none;
    border: none;
    color: white;
    cursor: pointer;
    padding: 0;
    margin-left: 1rem;
    opacity: 0.8;
}

.notification-close:hover {
    opacity: 1;
}

.form-control.is-valid {
    border-color: #28a745;
    box-shadow: 0 0 0 0.2rem rgba(40, 167, 69, 0.25);
}

.form-control.is-invalid {
    border-color: #dc3545;
    box-shadow: 0 0 0 0.2rem rgba(220, 53, 69, 0.25);
}

.form-select.is-valid {
    border-color: #28a745;
    box-shadow: 0 0 0 0.2rem rgba(40, 167, 69, 0.25);
}

.form-select.is-invalid {
    border-color: #dc3545;
    box-shadow: 0 0 0 0.2rem rgba(220, 53, 69, 0.25);
}
`;

// Agregar estilos adicionales al documento
if (!document.getElementById('appointment-additional-styles')) {
    const style = document.createElement('style');
    style.id = 'appointment-additional-styles';
    style.textContent = additionalStyles;
    document.head.appendChild(style);
}

// ==================== FUNCIONES PARA NUEVA PÁGINA AGENDA TU CITA ====================

/**
 * Inicializa la interacción de selección de servicios en el showcase
 */
function initServiceShowcaseInteraction() {
    const serviceItems = document.querySelectorAll('.service-showcase-item');
    const servicioSelect = document.getElementById('servicio_selector');
    
    if (serviceItems.length > 0 && servicioSelect) {
        serviceItems.forEach(item => {
            item.addEventListener('click', function() {
                // Remover selección previa
                serviceItems.forEach(i => i.classList.remove('selected'));
                
                // Seleccionar item actual
                this.classList.add('selected');
                
                // Actualizar el select
                const serviceValue = this.dataset.serviceValue;
                if (serviceValue) {
                    servicioSelect.value = serviceValue;
                    
                    // Disparar evento change
                    const changeEvent = new Event('change', { bubbles: true });
                    servicioSelect.dispatchEvent(changeEvent);
                    
                    // Animación de éxito
                    this.style.transform = 'scale(1.02)';
                    setTimeout(() => {
                        this.style.transform = '';
                    }, 200);
                }
            });
            
            // Efecto hover mejorado
            item.addEventListener('mouseenter', function() {
                if (!this.classList.contains('selected')) {
                    this.style.transform = 'translateX(8px) scale(1.01)';
                }
            });
            
            item.addEventListener('mouseleave', function() {
                if (!this.classList.contains('selected')) {
                    this.style.transform = '';
                }
            });
        });
        
        // Sincronizar selección inicial si ya hay un valor
        if (servicioSelect.value) {
            const selectedItem = document.querySelector(`[data-service-value="${servicioSelect.value}"]`);
            if (selectedItem) {
                selectedItem.classList.add('selected');
            }
        }
        
        // Escuchar cambios en el select para sincronizar showcase
        servicioSelect.addEventListener('change', function() {
            serviceItems.forEach(item => {
                item.classList.remove('selected');
                if (item.dataset.serviceValue === this.value) {
                    item.classList.add('selected');
                }
            });
        });
    }
}

/**
 * Mejoras en el formulario moderno
 */
function initModernFormEnhancements() {
    // Mejorar inputs con animaciones
    const modernInputs = document.querySelectorAll('.modern-select, .modern-date');
    
    modernInputs.forEach(input => {
        // Efecto focus mejorado
        input.addEventListener('focus', function() {
            this.parentElement.classList.add('focused');
        });
        
        input.addEventListener('blur', function() {
            this.parentElement.classList.remove('focused');
        });
        
        // Validación en tiempo real
        input.addEventListener('input', function() {
            validateInput(this);
        });
        
        // Efecto de escritura
        input.addEventListener('keydown', function() {
            this.style.transform = 'scale(1.01)';
            setTimeout(() => {
                this.style.transform = '';
            }, 100);
        });
    });
    
    // Mejorar botón de envío
    const submitBtn = document.querySelector('.btn-modern-primary');
    if (submitBtn) {
        submitBtn.addEventListener('click', function(e) {
            // Validar antes de enviar
            if (!validateForm()) {
                e.preventDefault();
                return false;
            }
            
            // Animación de envío
            this.style.transform = 'scale(0.95)';
            this.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Procesando...';
            
            setTimeout(() => {
                this.style.transform = '';
            }, 150);
        });
        
        // Efecto hover mejorado
        submitBtn.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-4px) scale(1.02)';
        });
        
        submitBtn.addEventListener('mouseleave', function() {
            this.style.transform = '';
        });
    }
}

/**
 * Validar input individual
 */
function validateInput(input) {
    const formSection = input.closest('.form-section');
    const errorMessage = formSection.querySelector('.error-message');
    
    // Remover errores previos
    input.classList.remove('error');
    if (errorMessage) {
        errorMessage.style.display = 'none';
    }
    
    let isValid = true;
    let message = '';
    
    if (input.classList.contains('modern-select')) {
        if (!input.value || input.value === '') {
            isValid = false;
            message = 'Por favor selecciona un servicio';
        }
    }
      if (input.classList.contains('modern-date')) {
        if (!input.value) {
            isValid = false;
            message = 'Por favor selecciona una fecha';
        } else {
            // Usar fecha local sin problemas de timezone
            const selectedDate = new Date(input.value + 'T00:00:00');
            const today = new Date();
            today.setHours(0, 0, 0, 0);
            
            if (selectedDate < today) {
                isValid = false;
                message = 'La fecha no puede ser anterior a hoy';
            }
            
            // Validar que no sea domingo
            if (selectedDate.getDay() === 0) {
                isValid = false;
                message = 'La barbería está cerrada los domingos';
            }
        }
    }
    
    if (!isValid) {
        input.classList.add('error');
        showErrorMessage(formSection, message);
    }
    
    return isValid;
}

/**
 * Mostrar mensaje de error
 */
function showErrorMessage(formSection, message) {
    let errorDiv = formSection.querySelector('.error-message');
    
    if (!errorDiv) {
        errorDiv = document.createElement('div');
        errorDiv.className = 'error-message';
        errorDiv.innerHTML = '<i class="fas fa-exclamation-circle"></i><span></span>';
        formSection.appendChild(errorDiv);
    }
    
    errorDiv.querySelector('span').textContent = message;
    errorDiv.style.display = 'flex';
    
    // Animación de aparición
    errorDiv.style.opacity = '0';
    errorDiv.style.transform = 'translateY(-10px)';
    
    setTimeout(() => {
        errorDiv.style.transition = 'all 0.3s ease';
        errorDiv.style.opacity = '1';
        errorDiv.style.transform = 'translateY(0)';
    }, 10);
}

/**
 * Validar formulario completo
 */
function validateForm() {
    const servicioSelect = document.getElementById('servicio_selector');
    const fechaInput = document.querySelector('.modern-date');
    
    let isValid = true;
    
    if (servicioSelect) {
        isValid = validateInput(servicioSelect) && isValid;
    }
    
    if (fechaInput) {
        isValid = validateInput(fechaInput) && isValid;
    }
    
    return isValid;
}

/**
 * Animaciones al hacer scroll
 */
function initScrollAnimations() {
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };
    
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('animate-in');
            }
        });
    }, observerOptions);
    
    // Observar elementos que se van a animar
    const animateElements = document.querySelectorAll('.info-panel, .service-showcase-item, .info-item');
    animateElements.forEach(el => {
        observer.observe(el);
    });
}

/**
 * Efectos en paneles de información
 */
function initInfoPanelsEffects() {
    const infoPanels = document.querySelectorAll('.info-panel');
    
    infoPanels.forEach(panel => {
        panel.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-8px) scale(1.02)';
        });
        
        panel.addEventListener('mouseleave', function() {
            this.style.transform = '';
        });
    });
}

/**
 * Inicializar todas las funciones del nuevo diseño
 */
function initNewBookingPageFeatures() {
    initServiceShowcaseInteraction();
    initModernFormEnhancements();
    initInfoPanelsEffects();
    initScrollAnimations();
    
    // Agregar clase CSS para animaciones
    const style = document.createElement('style');
    style.textContent = `
        .error {
            border-color: #dc3545 !important;
            box-shadow: 0 0 0 4px rgba(220, 53, 69, 0.1) !important;
        }
        
        .focused {
            transform: scale(1.02);
        }
        
        .animate-in {
            animation: slideInUp 0.6s ease forwards;
        }
        
        @keyframes slideInUp {
            from {
                opacity: 0;
                transform: translateY(30px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }
        
        .info-panel, .service-showcase-item, .info-item {
            opacity: 0;
            transform: translateY(30px);
            transition: all 0.3s ease;
        }
    `;
    document.head.appendChild(style);
}
