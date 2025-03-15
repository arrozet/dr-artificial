

// FUNCION DE MODO OSUCRO Y MODO CLARO
document.addEventListener("DOMContentLoaded", function () {
    iniciar();
});

function iniciar(){
    iniciarMicrófono();
    iniciarModoOscuro();
    iniciarEventoEnter();
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
// FUNCION PARA MICROFONO NO FUNCIONA LA HE COPIADO Y PEGADO A PRISAS DE CLAUDE
/*
document.addEventListener('DOMContentLoaded', function() {
    const micButton = document.getElementById('mic-btn');
    const textarea = document.getElementById('prompt');
    
    // Verificar si el navegador soporta la API de reconocimiento de voz
    if ('webkitSpeechRecognition' in window || 'SpeechRecognition' in window) {
        // Inicializar el reconocimiento de voz
        const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
        const recognition = new SpeechRecognition();
        
        // Configurar opciones
        recognition.lang = 'es-ES'; // Idioma español
        recognition.continuous = false; // No continúa escuchando después de terminar
        recognition.interimResults = false; // Solo regresa resultados finales
        
        let isListening = false;
        
        // Evento al hacer clic en el botón de micrófono
        micButton.addEventListener('click', function() {
            if (isListening) {
                // Detener el reconocimiento
                recognition.stop();
                micButton.classList.remove('active');
            } else {
                // Iniciar el reconocimiento
                recognition.start();
                micButton.classList.add('active');
            }
            isListening = !isListening;
        });
        
        // Evento cuando se reconoce la voz
        recognition.onresult = function(event) {
            const transcript = event.results[0][0].transcript;
            // Añadir el texto reconocido al área de texto
            textarea.value += transcript;
        };
        
        // Eventos para manejar el inicio y fin del reconocimiento
        recognition.onstart = function() {
            isListening = true;
            micButton.classList.add('active');
        };
        
        recognition.onend = function() {
            isListening = false;
            micButton.classList.remove('active');
        };
        
        recognition.onerror = function(event) {
            console.error('Error en reconocimiento de voz:', event.error);
            isListening = false;
            micButton.classList.remove('active');
        };
    } else {
        // Ocultar el botón si no hay soporte
        micButton.style.display = 'none';
        console.warn('Tu navegador no soporta reconocimiento de voz');
    }
});
*/