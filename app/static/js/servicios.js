/**
 * Services Page JavaScript - Lou Barbershop
 * Funciones para animaciones y efectos visuales de la página de servicios
 */

document.addEventListener('DOMContentLoaded', function() {
    initializeServicesAnimations();
});

/**
 * Inicializar animaciones de la página de servicios
 */
function initializeServicesAnimations() {
    const animatedElements = document.querySelectorAll('.animate-fadeInUp');
    
    // Función para verificar si un elemento está en el viewport
    function isInViewport(element) {
        const rect = element.getBoundingClientRect();
        return (
            rect.top <= (window.innerHeight || document.documentElement.clientHeight) &&
            rect.bottom >= 0
        );
    }
    
    // Activar animación para elementos visibles
    function checkAnimations() {
        animatedElements.forEach(element => {
            if (isInViewport(element)) {
                element.style.opacity = '1';
                const delay = element.getAttribute('data-delay');
                if (delay) {
                    element.style.animationDelay = delay + 's';
                }
            }
        });
    }
    
    // Inicializar todos los elementos como invisibles
    animatedElements.forEach(element => {
        element.style.opacity = '0';
        const delay = element.getAttribute('data-delay');
        if (delay) {
            element.style.animationDelay = delay + 's';
        }
    });
    
    // Comprobar animaciones al cargar y al hacer scroll
    checkAnimations();
    window.addEventListener('scroll', checkAnimations);
}
