/**
 * Script para manejar la interfaz responsive en dispositivos móviles
 */
document.addEventListener('DOMContentLoaded', function() {
    const mobileToggle = document.getElementById('mobile-toggle');
    const sidebar = document.querySelector('.sidebar');
    const isMobile = window.innerWidth <= 768;
    
    // Mostrar el botón de toggle solo en móvil
    if (isMobile) {
        mobileToggle.style.display = 'block';
    }
    
    // Función para alternar la sidebar en móvil
    mobileToggle.addEventListener('click', function() {
        sidebar.classList.toggle('expanded');
        // Cambiar el icono según el estado
        mobileToggle.textContent = sidebar.classList.contains('expanded') ? '✕' : '☰';
    });
    
    // Cerrar sidebar al seleccionar un chat (solo en móvil)
    const chatItems = document.querySelectorAll('.chat-item');
    if (isMobile) {
        chatItems.forEach(item => {
            item.addEventListener('click', function() {
                sidebar.classList.remove('expanded');
                mobileToggle.textContent = '☰';
            });
        });
    }
    
    // Ajustar visualización de código y markdown
    function optimizeMarkdownDisplay() {
        // Ajustar dimensiones de bloques de código
        document.querySelectorAll('.message-bubble pre').forEach(codeBlock => {
            codeBlock.style.maxWidth = '100%';
            codeBlock.style.overflowX = 'auto';
        });
        
        // Ajustar tablas
        document.querySelectorAll('.message-bubble table').forEach(table => {
            table.style.display = 'block';
            table.style.overflowX = 'auto';
            table.style.width = '100%';
        });
        
        // Ajustar imágenes
        document.querySelectorAll('.message-bubble img').forEach(img => {
            img.style.maxWidth = '100%';
            img.style.height = 'auto';
        });
    }
    
    // Optimizar markdown cuando se cargue la página
    optimizeMarkdownDisplay();
    
    // Optimizar markdown cuando se agregue nuevo contenido
    const chatContainer = document.querySelector('.chat-container');
    if (chatContainer) {
        const observer = new MutationObserver(function(mutations) {
            mutations.forEach(function(mutation) {
                if (mutation.addedNodes.length > 0) {
                    optimizeMarkdownDisplay();
                }
            });
        });
        
        observer.observe(chatContainer, { childList: true, subtree: true });
    }
    
    // Ajustar altura en cambios de orientación
    window.addEventListener('resize', function() {
        const newIsMobile = window.innerWidth <= 768;
        
        if (newIsMobile !== isMobile) {
            location.reload(); // Recargar para aplicar los cambios de layout
        }
    });
});