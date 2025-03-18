/**
 * Función genérica para realizar peticiones POST al servidor
 * @param {Object} data - Datos a enviar al servidor
 * @returns {Promise} - Promesa con la respuesta del servidor
 */
async function Request_Login(data) {
    try {
        const response = await fetch(API_ENDPOINT, {
            method: 'POST',
            headers: HEADERS,
            body: JSON.stringify(data)
        });

        log.console('OKEY: Respuesta del servidor:', response);

    } catch (error) {
        console.error('Error en la petición:', error);
    }
}

// Sripts Inicio de Sesión

document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('login-form');
    const email = document.getElementById('email');
    const password = document.getElementById('password');
    const successMessage = document.getElementById('success-message');
    
    // Mostrar errores
    function showError(input, message) {
        const errorElement = document.getElementById(`${input.id}-error`);
        errorElement.textContent = message;
        errorElement.style.display = 'block';
        input.style.borderColor = '#e74c3c';
    }
    
    // Ocultar errores
    function hideError(input) {
        const errorElement = document.getElementById(`${input.id}-error`);
        errorElement.style.display = 'none';
        input.style.borderColor = '#ddd';
    }
    
    // Validar email
    function validateEmail() {
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        if (!emailRegex.test(email.value)) {
            showError(email, 'Por favor, ingresa un correo electrónico válido');
            return false;
        }
        hideError(email);
        return true;
    }
    
    // Validar contraseña
    function validatePassword() {
        if (password.value.trim() === '') {
            showError(password, 'Por favor, ingresa tu contraseña');
            return false;
        }
        hideError(password);
        return true;
    }
    
    // Validar formulario al enviar
    form.addEventListener('submit', function(e) {
        e.preventDefault();
        
        const isEmailValid = validateEmail();
        const isPasswordValid = validatePassword();
        
        if (isEmailValid && isPasswordValid) {
            // Aquí podrías enviar los datos a un servidor para autenticación
            console.log('Intento de inicio de sesión');
            console.log({
                email: email.value,
                password: password.value,
                remember: document.getElementById('remember').checked       // Esto no se como mirarlo
            });
            
            Request_Login({
                email: email.value,
                password: password.value,
                remember: document.getElementById('remember').checked}
            )

            // Mostrar mensaje de éxito
            successMessage.style.display = 'block';
            
            // Simular redirección a página principal después de 2 segundos
            setTimeout(function() {
                // Aquí se redireccionaría a la página principal
                // window.location.href = 'dashboard.html';
                alert('Redireccionando a la página principal...');
            }, 2000);
        }
    });
    
    // Validar en tiempo real
    email.addEventListener('input', validateEmail);
    password.addEventListener('input', validatePassword);
});

// Scripts Registro de Usuarios
document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('signup-form');
    const username = document.getElementById('username');
    const email = document.getElementById('email');
    const password = document.getElementById('password');
    const confirmPassword = document.getElementById('confirm-password');
    const successMessage = document.getElementById('success-message');
    
    // Mostrar errores
    function showError(input, message) {
        const errorElement = document.getElementById(`${input.id}-error`);
        errorElement.textContent = message;
        errorElement.style.display = 'block';
        input.style.borderColor = '#e74c3c';
    }
    
    // Ocultar errores
    function hideError(input) {
        const errorElement = document.getElementById(`${input.id}-error`);
        errorElement.style.display = 'none';
        input.style.borderColor = '#ddd';
    }
    
    // Validar nombre de usuario
    function validateUsername() {
        if (username.value.length < 4) {
            showError(username, 'El nombre de usuario debe tener al menos 4 caracteres');
            return false;
        }
        hideError(username);
        return true;
    }
    
    // Validar email
    function validateEmail() {
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        if (!emailRegex.test(email.value)) {
            showError(email, 'Por favor, ingresa un correo electrónico válido');
            return false;
        }
        hideError(email);
        return true;
    }
    
    // Validar contraseña
    function validatePassword() {
        const passwordRegex = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[a-zA-Z\d]{8,}$/;
        if (!passwordRegex.test(password.value)) {
            showError(password, 'La contraseña debe tener al menos 8 caracteres, incluir una letra mayúscula, una minúscula y un número');
            return false;
        }
        hideError(password);
        return true;
    }
    
    // Validar confirmación de contraseña
    function validateConfirmPassword() {
        if (password.value !== confirmPassword.value) {
            showError(confirmPassword, 'Las contraseñas no coinciden');
            return false;
        }
        hideError(confirmPassword);
        return true;
    }
    
    // Validar formulario al enviar
    form.addEventListener('submit', function(e) {
        e.preventDefault();
        
        const isUsernameValid = validateUsername();
        const isEmailValid = validateEmail();
        const isPasswordValid = validatePassword();
        const isConfirmPasswordValid = validateConfirmPassword();
        
        if (isUsernameValid && isEmailValid && isPasswordValid && isConfirmPasswordValid) {
            // Aquí podrías enviar los datos a un servidor
            console.log('Formulario enviado con éxito');
            console.log({
                username: username.value,
                email: email.value,
                password: password.value
            });
            
            // Mostrar mensaje de éxito
            successMessage.style.display = 'block';
            
            // Limpiar formulario
            form.reset();
            
            // Redirigir a la página de inicio de sesión después de 3 segundos
            setTimeout(function() {
                // Aquí se redireccionaría a la página de login
                // window.location.href = 'login.html';
                alert('Redireccionando a la página de login...');
            }, 3000);
        }
    });
    
    // Validar en tiempo real
    username.addEventListener('input', validateUsername);
    email.addEventListener('input', validateEmail);
    password.addEventListener('input', validatePassword);
    confirmPassword.addEventListener('input', validateConfirmPassword);
});