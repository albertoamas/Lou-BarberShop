/**
 * Common JavaScript Functions - Lou Barbershop
 * Funciones reutilizables y utilitarios compartidos entre páginas
 */

/**
 * Función utilitaria para verificar si un elemento está en el viewport
 * @param {HTMLElement} element - Elemento a verificar
 * @returns {boolean} - True si está visible en el viewport
 */
function isInViewport(element) {
    const rect = element.getBoundingClientRect();
    return (
        rect.top <= (window.innerHeight || document.documentElement.clientHeight) &&
        rect.bottom >= 0
    );
}

/**
 * Inicializar animaciones de entrada fadeInUp
 * @param {string} selector - Selector CSS de elementos a animar
 */
function initializeFadeInAnimations(selector = '.animate-fadeInUp') {
    const animatedElements = document.querySelectorAll(selector);
    
    // Activar animación para elementos visibles
    function checkAnimations() {
        animatedElements.forEach(element => {
            if (isInViewport(element)) {
                element.style.opacity = '1';
                element.style.transform = 'translateY(0)';
                
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
        element.style.transform = 'translateY(30px)';
        element.style.transition = 'all 0.6s ease';
        
        const delay = element.getAttribute('data-delay');
        if (delay) {
            element.style.animationDelay = delay + 's';
        }
    });
    
    // Comprobar animaciones al cargar y al hacer scroll
    checkAnimations();
    window.addEventListener('scroll', checkAnimations);
}

/**
 * Mejorar accesibilidad de enlaces externos
 */
function improveExternalLinksAccessibility() {
    const externalLinks = document.querySelectorAll('a[target="_blank"]');
    
    externalLinks.forEach(link => {
        // Añadir texto de screen reader para enlaces externos
        const srText = document.createElement('span');
        srText.className = 'sr-only';
        srText.textContent = ' (se abre en nueva pestaña)';
        link.appendChild(srText);
        
        // Añadir rel="noopener noreferrer" por seguridad
        if (!link.getAttribute('rel')) {
            link.setAttribute('rel', 'noopener noreferrer');
        }
    });
}

/**
 * Mejorar navegación por teclado en dropdowns
 */
function improveDropdownKeyboardNavigation() {
    const dropdowns = document.querySelectorAll('.dropdown');
    
    dropdowns.forEach(dropdown => {
        const toggle = dropdown.querySelector('.dropdown-toggle');
        const menu = dropdown.querySelector('.dropdown-menu');
        const items = menu?.querySelectorAll('.dropdown-item');
        
        if (!toggle || !menu || !items) return;
        
        toggle.addEventListener('keydown', function(e) {
            if (e.key === 'ArrowDown') {
                e.preventDefault();
                menu.classList.add('show');
                items[0]?.focus();
            }
        });
        
        items.forEach((item, index) => {
            item.addEventListener('keydown', function(e) {
                switch (e.key) {
                    case 'ArrowDown':
                        e.preventDefault();
                        const nextItem = items[index + 1] || items[0];
                        nextItem.focus();
                        break;
                    case 'ArrowUp':
                        e.preventDefault();
                        const prevItem = items[index - 1] || items[items.length - 1];
                        prevItem.focus();
                        break;
                    case 'Escape':
                        e.preventDefault();
                        menu.classList.remove('show');
                        toggle.focus();
                        break;
                }
            });
        });
    });
}

/**
 * Validación de formularios con retroalimentación accesible
 * @param {HTMLFormElement} form - Formulario a validar
 */
function enhanceFormAccessibility(form) {
    if (!form) return;
    
    const inputs = form.querySelectorAll('input, select, textarea');
    
    inputs.forEach(input => {
        // Añadir aria-invalid inicialmente como false
        input.setAttribute('aria-invalid', 'false');
        
        // Validación en tiempo real
        input.addEventListener('blur', function() {
            const isValid = input.checkValidity();
            input.setAttribute('aria-invalid', !isValid);
            
            // Mostrar/ocultar mensajes de error
            const errorMsg = input.parentNode.querySelector('.invalid-feedback');
            if (errorMsg) {
                if (!isValid) {
                    errorMsg.setAttribute('role', 'alert');
                    errorMsg.style.display = 'block';
                } else {
                    errorMsg.style.display = 'none';
                }
            }
        });
    });
}

/**
 * Inicializar todas las mejoras de accesibilidad y funcionalidades comunes
 */
function initializeCommonFeatures() {
    // Mejorar accesibilidad
    improveExternalLinksAccessibility();
    improveDropdownKeyboardNavigation();
    
    // Mejorar todos los formularios de la página
    const forms = document.querySelectorAll('form');
    forms.forEach(form => enhanceFormAccessibility(form));
    
    // Inicializar animaciones comunes
    initializeFadeInAnimations();
}

// Auto-inicializar cuando el DOM esté listo
document.addEventListener('DOMContentLoaded', initializeCommonFeatures);

// Exportar funciones para uso en otros archivos
window.LouBarbershop = {
    isInViewport,
    initializeFadeInAnimations,
    improveExternalLinksAccessibility,
    improveDropdownKeyboardNavigation,
    enhanceFormAccessibility,
    initializeCommonFeatures
};
