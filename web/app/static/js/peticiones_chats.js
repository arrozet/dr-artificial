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
 * @param {string} msg - Cadena de caracteres que se corresponde con el prompt del usuario
 */
function enviar_prompt(msg) {

    // Elementos del DOM
    const promptInput = document.getElementById('prompt');
    const sendButton = document.querySelector('.send-btn');
    const micBtn = document.getElementById('mic-btn');
    const esNuevoChat = document.querySelector('.welcome-container') !== null;

    // 1. Deshabilitar el input para evitar envíos múltiples
    micBtn.disabled = true;
    promptInput.disabled = true;
    sendButton.disabled = true;
    
    // 2. Mostrar el mensaje temporal del usuario
    const mensajeTemporal = mostrarMensajeTemporal(msg);
    const indicadorPensando = mostrarIndicadorPensando();

    // Si el usuario está creando un nuevo chat con este PROMPT, 
    if (esNuevoChat) {
        const recommendedMessages = document.querySelector('.recommended-messages');
        if (recommendedMessages) {
            recommendedMessages.remove();
        }
        moverChatAbajo();
        document.querySelector('.welcome-container').remove();
    }
    // 3. Limpiar el campo de texto
    promptInput.value = '';
    
    // 4. Enviar al servidor y esperar respuesta
    makePostRequest({ prompt: msg, contestar: 0 }).then(() => {
        
        // 5. Re-habilitar el input (aunque en realidad se recreará con pagecontent
        promptInput.disabled = false;
        sendButton.disabled = false;
        micBtn.disabled = false;
        document.getElementById("prompt").focus();  // Mantener el foco en el input-text

    }).catch(error => {
        console.error('Error:', error);
        // En caso de error, eliminar el mensaje temporal y re-habilitar input
        if (mensajeTemporal && mensajeTemporal.parentNode) {
            mensajeTemporal.parentNode.removeChild(mensajeTemporal);
        }
        if (indicadorPensando && indicadorPensando.parentNode) {
            indicadorPensando.parentNode.removeChild(indicadorPensando);
        }
        promptInput.disabled = false;
        sendButton.disabled = false;
        micBtn.disabled = false;
    });
}


/**
 * Función que devuelve el HTML, que compone el mensaje del PROMPT del usuario mientras se carga la respuesta de la IA
 * Este mensaje es meramente temporal, desaparecerá cuando la IA responda, ya que el controlador recargará el HTML de index-body
 * 
 * @param {*} mensaje Es una cadena de caracteres, que se corresponde con el prompt del usuario
 * @returns HTML del PROMPT
 */
function mostrarMensajeTemporal(mensaje) {
    const chatContainer = document.querySelector('.chat-container');
    
    // Crear elemento para el mensaje temporal
    const mensajeTemp = document.createElement('div');
    mensajeTemp.className = 'UserMessage temp-message';
    mensajeTemp.id = 'mensaje-temporal';
    
    mensajeTemp.innerHTML = `
        <div class="message-content">
            <div class="message-bubble">
                ${mensaje}
            </div>
        </div>
        <div class="avatar avatarUser">U</div>
    `;
    
    // Añadir al contenedor de chat
    chatContainer.appendChild(mensajeTemp);
    
    // Hacer scroll hasta abajo para mostrar el nuevo mensaje
    chatContainer.scrollTop = chatContainer.scrollHeight;
    
    return mensajeTemp;
}

/**
 * Función que devuelve el HTML, que compone el indicador de pensando de la IA
 * Devuelve un indicador que quiere indicar que la IA está calculando la respuesta
 * 
 * @returns HTML del indicador de pensando
 */
function mostrarIndicadorPensando() {
    const chatContainer = document.querySelector('.chat-container');
    
    // Crear elemento para el indicador de pensando
    const pensandoDiv = document.createElement('div');
    pensandoDiv.className = 'AiMessage';
    pensandoDiv.id = 'ia-pensando';
    
    pensandoDiv.innerHTML = `
    <div class="avatar">
        <img src="/static/images/joselito_end.png" alt="AI" class="avatar-icon">
    </div>
    <div class="message-content">
        <div class="message-bubble">
            <div class="pensando-indicador">
                <div class="pensando-punto"></div>
                <div class="pensando-punto"></div>
                <div class="pensando-punto"></div>
            </div>
        </div>
    </div>
`;
    
    // Añadir al contenedor de chat
    chatContainer.appendChild(pensandoDiv);
    
    // Hacer scroll hasta abajo para mostrar el indicador
    chatContainer.scrollTop = chatContainer.scrollHeight;
    
    return pensandoDiv;
}