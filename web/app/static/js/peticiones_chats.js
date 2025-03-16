// Constantes para configuración
const API_ENDPOINT = '/';
const HEADERS = {
    'Content-Type': 'application/json'
};

/**
 * Función genérica para realizar peticiones POST al servidor
 * @param {Object} data - Datos a enviar al servidor
 * @returns {Promise} - Promesa con la respuesta del servidor
 */
async function makePostRequest(data) {
    try {
        const response = await fetch(API_ENDPOINT, {
            method: 'POST',
            headers: HEADERS,
            body: JSON.stringify(data)
        });
        const htmlContent = await response.text();
        updatePageContent(htmlContent);
    } catch (error) {
        console.error('Error en la petición:', error);
    }
}

/**
 * Actualiza el contenido de la página y reinicializa componentes
 * @param {string} htmlContent - Contenido HTML a insertar
 */
function updatePageContent(htmlContent) {
    document.body.innerHTML = htmlContent;
    iniciar();
    if (typeof initMarkdownRendering === 'function') {
        initMarkdownRendering();
    }
}

/**
 * Crea un nuevo chat
 */
function crearNuevoChat() {
    console.log('Se ha pulsado el botón de crear un nuevo chat');
    makePostRequest({ chat_id: 0 }).then(() => {
        moverChatCentro();
    }   );
}

/**
 * Borra un chat específico
 * @param {number} id - ID del chat a borrar
 */
function borrarChat(id) {
    console.log(`El usuario ha decidido borrar el chat con ID=${id}`);
    makePostRequest({ borrar_chat_id: id });
}

/**
 * Cambia al chat seleccionado
 * @param {number} id - ID del chat al que cambiar
 */
function cambiarChat(id) {
    console.log(`Cambiar chat a ${id}`);
    makePostRequest({ chat_id: id }).then(() => {
        moverChatAbajo();
    });
}

/**
 * Valida que el prompt no esté vacío antes de enviarlo
 */
function validarPrompt() {
    const prompt = document.getElementById('prompt').value.trim();
    if (prompt === '') {
        alert('El prompt no puede estar vacío.');
        return;
    }
    enviar_prompt(prompt);
}

/**
 * Envía un prompt al servidor
 * @param {string} msg - Mensaje a enviar
 */
function enviar_prompt(msg) {
    // Petición para que el servidor añade el mensaje del usuario al chat
    makePostRequest({ prompt: msg, contestar: 0 }).then(() => {
        moverChatAbajo();
    });

    /*
    // Petición para que el servidor conteste con la IA
    makePostRequest({ prompt: msg, contestar: 1 }).then(() => {
        moverChatAbajo();
    }   );

    */
}