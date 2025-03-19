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
    iniciarToggleSidebar();

    // Registrar eventos de cambio de orientación
    window.addEventListener('resize', manejarCambioOrientacion);
    window.addEventListener('orientationchange', manejarCambioOrientacion);
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

/**
 * Función para inicializar el toggle del sidebar
 */

function iniciarToggleSidebar() {
    const toggleBtn = document.getElementById('toggle-sidebar');
    const sidebar = document.querySelector('.sidebar');
    const main = document.querySelector('.main');
    const welcomeContainer = document.querySelector('.welcome-container');
    const inputContainer = document.querySelector('.input-container');
    const themeToggleBtn = document.getElementById('toggle-theme');
    const recommendedMessages = document.querySelector('.recommended-messages');
    
    if (toggleBtn && sidebar && main) {
        // Ocultar automáticamente en pantallas muy pequeñas al iniciar
        const ocultarEnPantallasPequeñas = window.innerWidth <= 480;
        
        // Recuperar el estado guardado de la barra lateral o usar el valor predeterminado
        const sidebarHidden = localStorage.getItem('sidebarHidden') === 'true' || 
                             (ocultarEnPantallasPequeñas && localStorage.getItem('sidebarHidden') === null);
                             
        if (sidebarHidden) {
            sidebar.classList.add('sidebar-hidden');
            main.classList.add('main-expanded');
            if (welcomeContainer) {
                welcomeContainer.classList.add('welcome-shifted');
                // En móvil, cuando la sidebar está oculta, mostrar welcome container
                if (esMobilVertical()) {
                    welcomeContainer.classList.remove('welcome-hidden-mobile');
                }
            }
            
            // En móviles en modo vertical, MOSTRAR input y botón de tema (cuando sidebar está oculta)
            if (esMobilVertical() && inputContainer && themeToggleBtn) {
                inputContainer.classList.remove('input-hidden-mobile');
                themeToggleBtn.classList.remove('theme-button-hidden-mobile');
                
                // Mostrar también los mensajes recomendados
                if (recommendedMessages) {
                    recommendedMessages.classList.remove('recommended-messages-hidden-mobile');
                }
            }
        } else {
            // Si la sidebar es visible, en móviles ocultar input y botón de tema
            if (esMobilVertical() && inputContainer && themeToggleBtn) {
                inputContainer.classList.add('input-hidden-mobile');
                themeToggleBtn.classList.add('theme-button-hidden-mobile');
                
                // Y también ocultar welcome container si existe
                if (welcomeContainer) {
                    welcomeContainer.classList.add('welcome-hidden-mobile');
                }
                
                // Ocultar los mensajes recomendados
                if (recommendedMessages) {
                    recommendedMessages.classList.add('recommended-messages-hidden-mobile');
                }
            }
        }
        
        toggleBtn.addEventListener('click', function() {
            sidebar.classList.toggle('sidebar-hidden');
            main.classList.toggle('main-expanded');
            
            // También ajustar el contenedor de bienvenida si existe
            if (welcomeContainer) {
                welcomeContainer.classList.toggle('welcome-shifted');
                
                // En móvil, ocultar/mostrar completamente el welcome container
                if (esMobilVertical()) {
                    const isSidebarHidden = sidebar.classList.contains('sidebar-hidden');
                    if (isSidebarHidden) {
                        // Si la sidebar está oculta, mostrar welcome container
                        welcomeContainer.classList.remove('welcome-hidden-mobile');
                    } else {
                        // Si la sidebar está visible, ocultar welcome container
                        welcomeContainer.classList.add('welcome-hidden-mobile');
                    }
                }
            }
            
            // En móviles en modo vertical, mostrar/ocultar input y botón de tema
            if (esMobilVertical() && inputContainer && themeToggleBtn) {
                const isSidebarHidden = sidebar.classList.contains('sidebar-hidden');
                if (isSidebarHidden) {
                    inputContainer.classList.remove('input-hidden-mobile');
                    themeToggleBtn.classList.remove('theme-button-hidden-mobile');
                    
                    // También mostrar mensajes recomendados
                    if (recommendedMessages) {
                        recommendedMessages.classList.remove('recommended-messages-hidden-mobile');
                    }
                } else {
                    inputContainer.classList.add('input-hidden-mobile');
                    themeToggleBtn.classList.add('theme-button-hidden-mobile');
                    
                    // Y ocultar mensajes recomendados
                    if (recommendedMessages) {
                        recommendedMessages.classList.add('recommended-messages-hidden-mobile');
                    }
                }
            }
            
            // Guardar el estado de la barra lateral en localStorage
            const isSidebarHidden = sidebar.classList.contains('sidebar-hidden');
            localStorage.setItem('sidebarHidden', isSidebarHidden);
        });
    }
}

/**
 * Función para manejar la orientación del dispositivo
 */
function manejarCambioOrientacion() {
    const sidebar = document.querySelector('.sidebar');
    const main = document.querySelector('.main');
    const welcomeContainer = document.querySelector('.welcome-container');
    const inputContainer = document.querySelector('.input-container');
    const themeToggleBtn = document.getElementById('toggle-theme');
    const recommendedMessages = document.querySelector('.recommended-messages');
    
    // En dispositivos pequeños en modo vertical (portrait), ocultar la barra lateral
    if (window.innerWidth <= 480 && window.innerHeight > window.innerWidth) {
        sidebar.classList.add('sidebar-hidden');
        main.classList.add('main-expanded');
        
        if (welcomeContainer) {
            welcomeContainer.classList.add('welcome-shifted');
            welcomeContainer.classList.remove('welcome-hidden-mobile'); // Mostrar welcome container cuando sidebar está oculta
        }
        
        // Cuando la sidebar está oculta, MOSTRAR input y tema en móvil
        if (inputContainer && themeToggleBtn) {
            inputContainer.classList.remove('input-hidden-mobile');
            themeToggleBtn.classList.remove('theme-button-hidden-mobile');
        }
        
        // También mostrar mensajes recomendados
        if (recommendedMessages) {
            recommendedMessages.classList.remove('recommended-messages-hidden-mobile');
        }
        
        localStorage.setItem('sidebarHidden', 'true');
    } else if (window.innerWidth > 768) {
        // En pantallas grandes, mostrar todo
        if (inputContainer && themeToggleBtn) {
            inputContainer.classList.remove('input-hidden-mobile');
            themeToggleBtn.classList.remove('theme-button-hidden-mobile');
        }
        
        // Y mostrar también el welcome container si existe
        if (welcomeContainer) {
            welcomeContainer.classList.remove('welcome-hidden-mobile');
        }
        
        // Y mostrar mensajes recomendados
        if (recommendedMessages) {
            recommendedMessages.classList.remove('recommended-messages-hidden-mobile');
        }
    }
}
function esMobilVertical() {
    return window.innerWidth <= 768 && window.innerHeight > window.innerWidth;
}

/**
 * Inserta el texto de la recomendación en el textarea y enfoca el cursor
 * @param {string} text - El texto de la recomendación a insertar
 */
function insertarRecomendacion(text) {
    const textarea = document.getElementById('prompt');
    textarea.value = text;
    textarea.focus();
    
    // Opcional: desplazar el cursor al final del texto
    textarea.setSelectionRange(text.length, text.length);
    
    // Efecto visual para indicar que se ha seleccionado
    textarea.classList.add('textarea-highlight');
    setTimeout(() => {
        textarea.classList.remove('textarea-highlight');
    }, 300);
}