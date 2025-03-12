



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
        body: JSON.stringify({ chat_id: id })  // Se envía el chat_id como un objeto JSON
    })
    .then(response => response.json())  // Asumiendo que Flask devuelve un JSON
    .then(data => {
        console.log("Respuesta del servidor:", data);

        // Aquí puedes hacer algo con la respuesta del servidor, como actualizar los mensajes en la interfaz
        const mensajes = data.mensajes_nuevo_chat;
        // Llamada para actualizar el DOM con los mensajes recibidos (esto depende de cómo quieras mostrar los mensajes)
    })
    .catch(error => {
        console.error("Error en la petición:", error);
    });
}

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