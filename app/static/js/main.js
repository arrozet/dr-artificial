document.addEventListener("DOMContentLoaded", () => {
    const chatBox = document.getElementById("chat-box");
    const userInput = document.getElementById("user-input");
    const sendBtn = document.getElementById("send-btn");

    function appendMessage(text, sender) {
        const messageDiv = document.createElement("div");
        messageDiv.classList.add("message", sender);
        messageDiv.textContent = text;
        chatBox.appendChild(messageDiv);
        chatBox.scrollTop = chatBox.scrollHeight;
    }

    sendBtn.addEventListener("click", () => {
        const message = userInput.value.trim();
        if (message) {
            appendMessage(message, "user");
            userInput.value = "";
            setTimeout(() => {
                appendMessage("Respuesta automática del bot.", "bot");
            }, 1000);
        }
    });

    userInput.addEventListener("keypress", (event) => {
        if (event.key === "Enter") {
            sendBtn.click();
        }
    });
});
