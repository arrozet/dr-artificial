document.addEventListener("DOMContentLoaded", function () {
    iniciar();
});

/**
 *  Inicializa todas las funciones
 */
function iniciar(){
    iniciarMicrófono();
    iniciarModoOscuro();
    iniciarEventoEnter();
    cargarChatNuevo();
    mostrarChatAbajo();
}

/**
 * Función que controla la posición del input-container. Dependiendo de la existencia de un mensaje
 * con el id "nuevo-chat-mensaje" se centra o se deja abajo.
 * 
 * Esto es así, ya que este mensaje solo saldrá cuando nos encontremos en un chat nuevo.
 */
function cargarChatNuevo(){
    const mensajeVacio = document.getElementById('nuevo-chat-mensaje');

    if (mensajeVacio) {     // Si está el mensaje, el chat es vacío
        console.log("Estamos ante un chat nuevo");
        moverChatCentro();
    }else{
        console.log("Bajamos el chat");
        moverChatAbajo();
    }
}

/**
 * Función que musestra el chat por el último mensaje, es directamente
 */
function mostrarChatAbajo() {
    const chatContainer = document.querySelector('.chat-container');
    const lastMessage = chatContainer.lastElementChild;

    if (lastMessage) {
        // Calculamos la altura total del contenido
        const scrollHeight = chatContainer.scrollHeight;
        const clientHeight = chatContainer.clientHeight;
        
        // Hacemos scroll hasta el final
        chatContainer.scrollTop = scrollHeight - clientHeight;
        
        // Aseguramos que el scroll se realiza incluso después de que el contenido se haya renderizado
        setTimeout(() => {
            chatContainer.scrollTop = chatContainer.scrollHeight - chatContainer.clientHeight;
        }, 0);
    }
}


/**
 *  Función que mueve el input-container al centro 
 */ 
function moverChatCentro() {
    const inputContainer = document.querySelector('.input-container');
    inputContainer.classList.add('centered');  // Aplica la clase que lo centra
  }
  
/**
 * Función que mueve el input-container al final para mostrar los mensajes más recientes.
 */
function moverChatAbajo() {
    const inputContainer = document.querySelector('.input-container');
    inputContainer.classList.remove('centered');  // Elimina la clase que lo centra
}




function iniciarMicrófono() {
    const micBtn = document.getElementById("mic-btn");
    console.log("Micrófono encontrado después del cambio de chat:", micBtn);
    const textArea = document.getElementById("prompt");
    console.log("textareaaaaaaaaaaaa :", textArea);

    if (!("webkitSpeechRecognition" in window) && !("SpeechRecognition" in window)) {
        alert("Tu navegador no soporta reconocimiento de voz.");
        return;
    }

    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    const recognition = new SpeechRecognition();

    recognition.continuous = false; // Solo una frase a la vez
    recognition.lang = "es-ES";
    recognition.interimResults = false;

    recognition.onresult = function (event) {
        const transcript = event.results[0][0].transcript;
        textArea.value += transcript; // Agregar el texto al textarea
    };

    recognition.onerror = function (event) {
        console.error("Error en el reconocimiento de voz:", event.error);
    };

    // Cuando el reconocimiento se detiene, quitar el color del botón
    recognition.onend = function () {
        micBtn.classList.remove("active");
    };

    micBtn.addEventListener("click", function () {
        if (micBtn.classList.contains("active")) {
            recognition.stop(); // Si ya está activo, detenerlo
        } else {
            micBtn.classList.add("active");
            recognition.start(); // Si está inactivo, iniciarlo
        }
    });
    console.log("He terminao vale");
}

function iniciarModoOscuro(){
    const themeToggle = document.getElementById("toggle-theme");
    const themeIcon = document.getElementById("theme-icon"); // Obtiene la imagen dentro del botón

    const currentTheme = localStorage.getItem("theme") || "dark";
    document.documentElement.setAttribute("data-theme", currentTheme);

    updateButtonIcon(currentTheme); // Cambiar icono del botón según el tema

    themeToggle.addEventListener("click", function () {
        let newTheme = document.documentElement.getAttribute("data-theme") === "dark" ? "light" : "dark";
        document.documentElement.setAttribute("data-theme", newTheme);
        localStorage.setItem("theme", newTheme);
        updateButtonIcon(newTheme);
    });

    function updateButtonIcon(theme) {
        const themeIcon = document.getElementById("theme-icon");
        themeIcon.src = theme === "dark" ? "/static/images/sun.png" : "/static/images/moon.png";
    }
}

function iniciarEventoEnter() {
    const promptInput = document.getElementById("prompt");

    if (promptInput) {
        promptInput.addEventListener("keydown", function(event) {
            if (event.key === "Enter" && !event.shiftKey) {
                event.preventDefault(); // Evita el salto de línea
                validarPrompt(); // Llama a la función del botón
            }
        });
    }
}
