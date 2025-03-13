function crearNuevoChat(){
    console.log("Se ha pulsado el botón de crear un nuevo chat")

    //const params = new URLSearchParams();
    const peticion ={
        new_chat_name: "Nuevo Chat"
    }
    fetch("/", {
        method: "POST", // Método POST
        headers: {
            "Content-Type": "application/json" // Enviar como JSON
        },
        body: JSON.stringify(peticion)
    })
    .then(response => response.json()) // Asumimos que el servidor responderá con JSON
    .then(data => {
        console.log("Respuesta del servidor:", data);
        alert("Respuesta: " + data.respuesta); // Muestra la respuesta del servidor
    })
    .catch(error => {
        console.error("Error en la petición:", error);
    });

    console.log("Creando nuevo chat");
}

function cambiarChat(id) {
    console.log("Cambiar chat a " + id);

    //const params = new URLSearchParams();
    const peticion ={
        chat_id: id
    }
    fetch("/", {
        method: "POST", // Método POST
        headers: {
            "Content-Type": "application/json" // Enviar como JSON
        },
        body: JSON.stringify(peticion)
    })
    .then(response => response.json()) // Asumimos que el servidor responderá con JSON
    .then(data => {
        console.log("Respuesta del servidor:", data);
        alert("Respuesta: " + data.respuesta); // Muestra la respuesta del servidor
    })
    .catch(error => {
        console.error("Error en la petición:", error);
    });
}


function validarPrompt() {
    const prompt = document.getElementById("prompt").value.trim();
        
        if (prompt === "") {
            alert("El prompt no puede estar vacío.");
            
        }else{
            enviar_prompt(prompt);
        }
}

function enviar_prompt(msg) {

        // Crear el objeto con los datos a enviar
        const peticion = {
            prompt: msg
        };

        fetch("/", {
            method: "POST",  // Método POST
            headers: {
                "Content-Type": "application/json"  // Especifica que enviamos JSON
            },
            body: JSON.stringify(datosAEnviar)  // Convertir el objeto a JSON
        })
        .then(response => response.json())  // Asumimos que el servidor responde con JSON
        .then(data => {
            console.log("Respuesta del servidor:", data);
            alert("Respuesta del servidor: " + data.respuesta);
        })
        .catch(error => {
            console.error("Error en la petición:", error);
        });
}
