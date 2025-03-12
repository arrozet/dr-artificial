document.addEventListener("DOMContentLoaded", function() {
    const textarea = document.querySelector("textarea");
    const sendBtn = document.querySelector(".send-btn");
    const chatContainer = document.querySelector(".chat-container");
    
    // Adjust textarea height based on content
    textarea.addEventListener("input", function() {
        textarea.style.height = "auto";
        textarea.style.height = (textarea.scrollHeight) + "px";
        
        // Enable/disable send button
        sendBtn.disabled = textarea.value.trim() === "";
    });

    // Send message
    sendBtn.addEventListener("click", function() {
        if (textarea.value.trim() === "") return;
        
        // Create user message
        const userMsg = document.createElement("div");
        userMsg.className = "message";
        userMsg.innerHTML = `
            <div class="avatar user">U</div>
            <div class="message-content">
                <div class="message-bubble">${textarea.value.replace(/\n/g, "<br>")}</div>
            </div>`;
        chatContainer.appendChild(userMsg);
        
        // Create assistant message (simulated response)
        setTimeout(() => {
            const assistantMsg = document.createElement("div");
            assistantMsg.className = "message";
            assistantMsg.innerHTML = `
                <div class="avatar">AI</div>
                <div class="message-content">
                    <div class="message-bubble">Estoy procesando tu mensaje: "${textarea.value}"<br><br>Este es un ejemplo de respuesta simulada del asistente de IA. En una implementación real, esto se conectaría a un modelo de lenguaje como GPT o Claude para generar respuestas.</div>
                </div>
            `;
            chatContainer.appendChild(assistantMsg);
            
            // Scroll to bottom
            chatContainer.scrollTop = chatContainer.scrollHeight;
        }, 500);

// Clear input
textarea.value = "";
textarea.style.height = "auto";
sendBtn.disabled = true;

// Scroll to bottom
chatContainer.scrollTop = chatContainer.scrollHeight;
});

});

// FUNCION DE MODO OSUCRO Y MODO CLARO
document.addEventListener("DOMContentLoaded", function () { 
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
});

function validarPrompt() {
    var prompt = document.getElementById("prompt").value.trim();
        
        if (prompt === "") {
            alert("El prompt no puede estar vacío.");
            
            return false;
        }
        return true;
}

// FUNCIONES PARA CAMBIAR DE CHAT

function cambiarChat(id) {
    // Oculta todos los chats
    document.querySelectorAll('.chat').forEach(chat => chat.style.display = 'none');
    
    // Muestra el chat seleccionado
    document.getElementById('chat' + id).style.display = 'block';

    // Guarda en la URL el chat actual
    window.location.hash = 'chat' + id;
}

// Detectar cambios en la URL
window.addEventListener("hashchange", () => {
    let chatId = window.location.hash.replace("#", "");
    if (chatId) {
        cambiarChat(chatId.replace("chat", ""));
    }
});

// Cargar el chat correcto al abrir la página
window.onload = () => {
    if (window.location.hash) {
        let chatId = window.location.hash.replace("#chat", "");
        cambiarChat(chatId);
    }
};

sessionStorage.setItem("chatActivo", id);


