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
 * @param {string} msg - Mensaje a enviar
 */
function enviar_prompt(msg) {
    // 1. Deshabilitar el input mientras se procesa
    const promptInput = document.getElementById('prompt');
    const sendButton = document.querySelector('.send-btn');
    const micBtn = document.getElementById('mic-btn');
    const esNuevoChat = document.querySelector('.welcome-container') !== null;

    micBtn.disabled = true;
    promptInput.disabled = true;
    sendButton.disabled = true;
    
    // 2. Mostrar el mensaje temporal del usuario
    const mensajeTemporal = mostrarMensajeTemporal(msg);
    const indicadorPensando = mostrarIndicadorPensando();
    // JUANMA CODIGO si es un chat nuevo, reinicia la página
    if (esNuevoChat) {
        const welcome = document.querySelector('.welcome-container');
        welcome.remove();
        moverChatAbajo();
        console.log("AYUDAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA");
    }
    // 3. Limpiar el campo de texto
    promptInput.value = '';
    
    // 4. Enviar al servidor y esperar respuesta
    makePostRequest({ prompt: msg, contestar: 0 }).then(() => {
        // No necesitamos eliminar el mensaje temporal explícitamente 
        // porque updatePageContent reemplazará todo el contenido del body
        
        // 5. Re-habilitar el input (aunque en realidad se recreará con pagecontent
        // geContent)
        promptInput.disabled = false;
        sendButton.disabled = false;
        micBtn.disabled = false;
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

// Me cansé de hacer codigo bonito, se viene juanmacodigo

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