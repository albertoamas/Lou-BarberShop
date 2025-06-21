/**
 * Home Page JavaScript - Lou Barbershop
 * Funciones para animaciones, efectos visuales y interactividad de la página principal
 */

document.addEventListener('DOMContentLoaded', function() {
    initializeAnimations();
    initializeParallaxEffects();
    initializeCounters();
});

/**
 * Inicializar animaciones de entrada
 */
function initializeAnimations() {
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
                element.style.transform = 'translateY(0)';
            }
        });
    }
    
    // Inicializar todos los elementos como invisibles
    animatedElements.forEach(element => {
        element.style.opacity = '0';
        element.style.transform = 'translateY(30px)';
        element.style.transition = 'all 0.6s ease';
    });
    
    // Comprobar animaciones al cargar y al hacer scroll
    checkAnimations();
    window.addEventListener('scroll', checkAnimations);
}

/**
 * Efectos parallax para decoraciones
 */
function initializeParallaxEffects() {
    window.addEventListener('scroll', function() {
        const scrolled = window.pageYOffset;
        const parallaxElements = document.querySelectorAll('.hero-decoration-1, .hero-decoration-2');
        
        parallaxElements.forEach(element => {
            const speed = element.classList.contains('hero-decoration-1') ? 0.5 : 0.3;
            element.style.transform = `translateY(${scrolled * speed}px)`;
        });
    });
}

/**
 * Contador animado para estadísticas
 */
function initializeCounters() {
    function animateCounters() {
        const counters = document.querySelectorAll('.stat-number-home');
        
        counters.forEach(counter => {
            const target = parseInt(counter.textContent.replace(/\D/g, ''));
            const duration = 2000;
            const step = target / (duration / 16);
            let current = 0;
            
            const timer = setInterval(() => {
                current += step;
                if (current >= target) {
                    current = target;
                    clearInterval(timer);
                }
                
                if (counter.textContent.includes('%')) {
                    counter.textContent = Math.floor(current) + '%';
                } else if (counter.textContent.includes('+')) {
                    counter.textContent = Math.floor(current) + '+';
                } else {
                    counter.textContent = Math.floor(current);
                }
            }, 16);
        });
    }
    
    // Función para verificar si un elemento está en el viewport
    function isInViewport(element) {
        const rect = element.getBoundingClientRect();
        return (
            rect.top <= (window.innerHeight || document.documentElement.clientHeight) &&
            rect.bottom >= 0
        );
    }
    
    // Iniciar contador cuando la sección sea visible
    const heroSection = document.querySelector('.home-hero');
    if (heroSection && isInViewport(heroSection)) {
        setTimeout(animateCounters, 1000);
    }
    
    window.addEventListener('scroll', function() {
        if (heroSection && isInViewport(heroSection)) {
            setTimeout(animateCounters, 1000);
        }
    });
}
