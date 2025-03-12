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

    console.log("Cambiar chat a " + id);

    // Enviar petición a Flask
    fetch('/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ chat_id: id })
    })
    .then(response => response.json())
    .then(data => {
        console.log("Respuesta del servidor:", data);
    })
    .catch(error => {
        console.error("Error en la petición:", error);
    });
}