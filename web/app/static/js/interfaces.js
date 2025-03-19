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