// Script principal para Lou Barbershop

// Función para ejecutar cuando el DOM esté cargado
document.addEventListener('DOMContentLoaded', function() {
    console.log('Lou Barbershop - Aplicación cargada');
    
    // Inicializar componentes de Bootstrap
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
});
