// Función para renderizar markdown en todos los mensajes
function renderMarkdown() {
    console.log("Iniciando renderizado de markdown");
    
    // Inicializar mermaid
    if (typeof mermaid !== 'undefined') {
        mermaid.initialize({
            startOnLoad: true,
            theme: document.documentElement.getAttribute('data-theme') === 'dark' ? 'dark' : 'default'
        });
    }
    
    // Selecciona todos los mensajes de la IA
    document.querySelectorAll('.AiMessage .message-bubble').forEach(element => {
        // Obtiene el contenido actual
        const markdownText = element.textContent.trim();
        
        // Solo renderizar si hay contenido y no es un elemento de carga
        if (markdownText && !element.querySelector('.loading-dots')) {
            // Renderiza el markdown a HTML
            element.innerHTML = marked.parse(markdownText);
            
            // Buscar diagramas Mermaid y renderizarlos
            if (typeof mermaid !== 'undefined') {
                element.querySelectorAll('pre code.language-mermaid').forEach(codeBlock => {
                    const preElement = codeBlock.parentElement;
                    const mermaidDiv = document.createElement('div');
                    mermaidDiv.classList.add('mermaid');
                    mermaidDiv.innerHTML = codeBlock.textContent;
                    preElement.parentNode.replaceChild(mermaidDiv, preElement);
                });
                
                try {
                    mermaid.init(undefined, document.querySelectorAll('.mermaid'));
                } catch (error) {
                    console.error("Error al renderizar Mermaid:", error);
                }
            }
            
            console.log("Mensaje renderizado");
        }
    });
}

// Función para inicializar marked y renderizar
function initMarkdownRendering() {
    console.log("Inicializando renderizador de markdown");
    if (typeof marked !== 'undefined') {
        // Configuración de marked
        marked.setOptions({
            breaks: true,       // Interpretar saltos de línea como <br>
            gfm: true,          // GitHub Flavored Markdown
            headerIds: false    // No generar IDs para los encabezados
        });
        
        renderMarkdown();
    } else {
        console.error("Error: La biblioteca marked no está cargada");
    }
}

// Ejecutar al cargar la página
document.addEventListener('DOMContentLoaded', initMarkdownRendering);

// Función para optimizar la visualización de markdown en móviles
function optimizeMarkdownForMobile() {
    const isMobile = window.innerWidth <= 768;
    
    if (isMobile) {
        // Ajustar las tablas para scroll horizontal
        document.querySelectorAll('table').forEach(table => {
            table.style.display = 'block';
            table.style.overflowX = 'auto';
            table.style.width = '100%';
        });
        
        // Ajustar los bloques de código
        document.querySelectorAll('pre').forEach(pre => {
            pre.style.whiteSpace = 'pre-wrap';
            pre.style.wordBreak = 'break-word';
            pre.style.maxWidth = '100%';
        });
        
        // Ajustar imágenes
        document.querySelectorAll('img').forEach(img => {
            img.style.maxWidth = '100%';
            img.style.height = 'auto';
        });
    }
}

// Ejecutar después de renderizar markdown
if (typeof mermaid !== 'undefined') {
    mermaid.init(undefined, document.querySelectorAll('.language-mermaid'));
    optimizeMarkdownForMobile();
}

// Observar cambios en el contenido del chat para aplicar optimizaciones
const chatObserver = new MutationObserver(mutations => {
    mutations.forEach(mutation => {
        if (mutation.addedNodes.length) {
            optimizeMarkdownForMobile();
        }
    });
});

// Iniciar observación del contenedor de chat
document.addEventListener('DOMContentLoaded', () => {
    const chatContainer = document.querySelector('.chat-container');
    if (chatContainer) {
        chatObserver.observe(chatContainer, { childList: true, subtree: true });
    }
    
    // También aplicar al cargar la página
    optimizeMarkdownForMobile();
});