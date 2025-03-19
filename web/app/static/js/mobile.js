/**
 * Script para manejar la interfaz responsive en dispositivos móviles
 */
document.addEventListener('DOMContentLoaded', function() {
    const mobileToggle = document.getElementById('mobile-toggle');
    const sidebar = document.querySelector('.sidebar');
    const body = document.body;
    
    // Crear un overlay para cerrar al hacer clic fuera
    const overlay = document.createElement('div');
    overlay.className = 'sidebar-overlay';
    body.appendChild(overlay);
    
    // Función para mostrar/ocultar sidebar
    function toggleSidebar() {
        sidebar.classList.toggle('expanded');
        
        if (sidebar.classList.contains('expanded')) {
            overlay.classList.add('active');
            mobileToggle.innerHTML = '✕';
        } else {
            overlay.classList.remove('active');
            mobileToggle.innerHTML = '☰';
        }
    }
    
    // Event listener para el botón
    mobileToggle.addEventListener('click', toggleSidebar);
    
    // Cerrar sidebar al hacer clic en overlay
    overlay.addEventListener('click', function() {
        sidebar.classList.remove('expanded');
        overlay.classList.remove('active');
        mobileToggle.innerHTML = '☰';
    });
    
    // Cerrar sidebar al seleccionar un chat
    const chatItems = document.querySelectorAll('.chat-item');
    chatItems.forEach(item => {
        item.addEventListener('click', function() {
            if (window.innerWidth <= 768) {
                sidebar.classList.remove('expanded');
                overlay.classList.remove('active');
                mobileToggle.innerHTML = '☰';
            }
        });
    });
    
    // Optimizar visualización de contenido markdown
    function optimizeMarkdownContent() {
        const messageElements = document.querySelectorAll('.message-bubble');
        
        messageElements.forEach(element => {
            // Ajustar tablas
            const tables = element.querySelectorAll('table');
            tables.forEach(table => {
                table.style.display = 'block';
                table.style.overflowX = 'auto';
                table.style.maxWidth = '100%';
            });
            
            // Ajustar bloques de código
            const codeBlocks = element.querySelectorAll('pre, code');
            codeBlocks.forEach(block => {
                block.style.whiteSpace = 'pre-wrap';
                block.style.wordBreak = 'break-word';
                block.style.maxWidth = '100%';
                block.style.overflowX = 'auto';
            });
            
            // Ajustar imágenes
            const images = element.querySelectorAll('img');
            images.forEach(img => {
                img.style.maxWidth = '100%';
                img.style.height = 'auto';
            });
        });
    }
    
    // Ejecutar optimización al cargar
    optimizeMarkdownContent();
    
    // Observar cambios en el chat-container para aplicar optimizaciones
    const chatContainer = document.querySelector('.chat-container');
    if (chatContainer) {
        const observer = new MutationObserver(mutations => {
            optimizeMarkdownContent();
        });
        
        observer.observe(chatContainer, { 
            childList: true, 
            subtree: true 
        });
    }
});