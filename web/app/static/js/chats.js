function crearNuevoChat(){
    console.log("Se ha pulsado el botón de crear un nuevo chat")

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
    .then(response => response.text()) // Asumimos que el servidor responderá con JSON
    .then(data => {
        document.body.innerHTML = data;  // Actualizar toda la página con el HTML devuelto
        // location.reload(); // esto puede ser que vaya tambien
            iniciarMicrófono();
            iniciarModoOscuro();
    })
    .catch(error => {
        console.error("Error en la petición:", error);
    });

    console.log("Creando nuevo chat");
}

function borrarChat(id){
    console.log("El usuario ha decidido borrar el chat cond ID= " + id);

    const peticion ={
        borrar_chat_id: id
    }
    fetch("/", {
        method: "POST", // Método POST
        headers: {
            "Content-Type": "application/json" // Enviar como JSON
        },
        body: JSON.stringify(peticion)
    })
    .then(response => response.text()) // Asumimos que el servidor responderá con JSON
    .then(data => {
        document.body.innerHTML = data;  // Actualizar toda la página con el HTML devuelto
    })
    .catch(error => {
        console.error("Error en la petición:", error);
    });

    console.log("Chat borrado");
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
    .then(response => response.text()) // Asumimos que el servidor responderá con JSON
    .then(data => {
        document.body.innerHTML = data;  // Actualizar toda la página con el HTML devuelto
            iniciarMicrófono();
            iniciarModoOscuro();
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
            body: JSON.stringify(peticion)  // Convertir el objeto a JSON
        })
        .then(response => response.text())  // Asumimos que el servidor responde con JSON
        .then(data => {
            document.body.innerHTML = data;  // Actualizar toda la página con el HTML devuelto
            iniciarMicrófono();
            iniciarModoOscuro();
        })
        .catch(error => {
            console.error("Error en la petición:", error);
        });
}
