// VOY A PONER AQUÍ EL CODIGO PARA LA CONFIGURACION
// cambio de modo oscuro a modo claro
/*
document.addEventListener("DOMContentLoaded", function () { // espera a que el documento esté cargado
    const themeToggle = document.getElementById("toggle-theme"); // obtiene el botón de cambio de tema

    const currentTheme = localStorage.getItem("theme") || "dark"; // obtiene el tema actual del almacenamiento local (la variable theme) en caso de que no exista la guarda como "dark"
    document.documentElement.setAttribute("data-theme", currentTheme); // establece el tema actual en el atributo de datos del documento

     updateButtonIcon(currentTheme); // Cambiar icono del botón según el tema

     themeToggle.addEventListener("click", function () { // espera a que se haga clic en el botón de cambio de tema
        let newTheme = document.documentElement.getAttribute("data-theme") === "dark" ? "light" : "dark"; // obtiene el tema actual y lo cambia al opuesto
        document.documentElement.setAttribute("data-theme", newTheme); // establece el nuevo tema en el atributo de datos del documento
        localStorage.setItem("theme", newTheme); // guarda el nuevo tema en el almacenamiento local
        updateButtonIcon(newTheme);
    });

    function updateButtonIcon(theme) {
        themeToggle.textContent = theme === "dark" ? "☀️ Modo Claro" : "🌙 Modo Oscuro";
    }
});
*/
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
/*
document.addEventListener("DOMContentLoaded", function () {
    const themeSelect = document.getElementById("theme-select");

    // Aplicar el tema guardado al cargar la página
    const savedTheme = localStorage.getItem("theme") || "dark";
    document.documentElement.setAttribute("data-theme", savedTheme);
    themeSelect.value = savedTheme;

    // Cambiar el tema al seleccionar una opción
    themeSelect.addEventListener("change", function () {
        const selectedTheme = this.value;
        localStorage.setItem("theme", selectedTheme);
        document.documentElement.setAttribute("data-theme", selectedTheme);
    });
});
*/