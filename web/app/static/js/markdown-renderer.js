// Función para renderizar markdown en todos los mensajes
function renderMarkdown() {
    console.log("Iniciando renderizado de markdown");
    // Selecciona todos los mensajes de la IA
    document.querySelectorAll('.AiMessage .message-bubble').forEach(element => {
        // Obtiene el contenido actual
        const markdownText = element.textContent.trim();
        
        // Solo renderizar si hay contenido y no es un elemento de carga
        if (markdownText && !element.querySelector('.loading-dots')) {
            // Renderiza el markdown a HTML
            element.innerHTML = marked.parse(markdownText);
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