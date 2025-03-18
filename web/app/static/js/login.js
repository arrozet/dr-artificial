// Constantes para configuración
const API_ENDPOINT = '/login';
const HEADERS = {
    'Content-Type': 'application/json'
};

/**
 * Función para realizar peticiones POST de login al servidor
 * @param {Object} data - Datos a enviar al servidor (email, password, remember)
 * @returns {Promise} - Promesa con la respuesta del servidor
 */
async function Request_Login(data) {
    try {
        const response = await fetch(API_ENDPOINT, {
            method: 'POST',
            headers: HEADERS,
            body: JSON.stringify(data)
        });
        
        // Convertir la respuesta a JSON
        const responseData = await response.json();
        
        // Devolver tanto la respuesta como los datos para manejarlos
        return {
            ok: response.ok,
            status: response.status,
            data: responseData
        };
    } catch (error) {
        console.error('Error en la petición de login:', error);
        return {
            ok: false,
            status: 500,
            data: { message: 'Error de conexión con el servidor' }
        };
    }
}

// Script para manejo del formulario de inicio de sesión
document.addEventListener('DOMContentLoaded', function() {
    const loginForm = document.getElementById('login-form');
    
    // Si no existe el formulario de login en esta página, salir
    if (!loginForm) return;
    
    const email = document.getElementById('email');
    const password = document.getElementById('password');
    const successMessage = document.getElementById('success-message');
    const loginError = document.getElementById('login-error');
    
    // Mostrar errores
    function showError(input, message) {
        const errorElement = document.getElementById(`${input.id}-error`);
        if (errorElement) {
            errorElement.textContent = message;
            errorElement.style.display = 'block';
            input.style.borderColor = '#e74c3c';
        }
    }
    
    // Ocultar errores
    function hideError(input) {
        const errorElement = document.getElementById(`${input.id}-error`);
        if (errorElement) {
            errorElement.style.display = 'none';
            input.style.borderColor = '#ddd';
        }
    }
    
    // Mostrar mensaje de error general
    function showLoginError(message) {
        if (loginError) {
            loginError.textContent = message;
            loginError.style.display = 'block';
        }
    }
    
    // Ocultar mensaje de error general
    function hideLoginError() {
        if (loginError) {
            loginError.style.display = 'none';
        }
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
    loginForm.addEventListener('submit', async function(e) {
        e.preventDefault();
        
        const isEmailValid = validateEmail();
        const isPasswordValid = validatePassword();
        
        if (isEmailValid && isPasswordValid) {
            // Ocultar cualquier error previo
            hideLoginError();
            
            // Deshabilitar botón para prevenir múltiples envíos
            const submitButton = loginForm.querySelector('button[type="submit"]');
            if (submitButton) submitButton.disabled = true;
            
            // Enviar datos al servidor
            const response = await Request_Login({
                email: email.value,
                password: password.value,
                remember: document.getElementById('remember')?.checked || false
            });
            
            // Re-habilitar el botón
            if (submitButton) submitButton.disabled = false;
            
            // Procesar respuesta
            if (response.ok) {
                // Mostrar mensaje de éxito
                if (successMessage) successMessage.style.display = 'block';
                
                // Redirigir a la página principal después de un breve delay
                setTimeout(function() {
                    window.location.href = '/';
                }, 150);
            } else {
                // Mostrar mensaje de error del servidor
                const errorMsg = response.data?.message || 'Error al iniciar sesión. Por favor, intenta nuevamente.';
                showLoginError(errorMsg);
                
                // Ocultar mensaje de éxito si estaba visible
                if (successMessage) successMessage.style.display = 'none';
            }
        }
    });
    
    // Validar en tiempo real
    if (email) email.addEventListener('input', validateEmail);
    if (password) password.addEventListener('input', validatePassword);
});

// Scripts Registro de Usuarios
document.addEventListener('DOMContentLoaded', function() {
    const signupForm = document.getElementById('signup-form');
    
    // Si no existe el formulario de registro en esta página, salir
    if (!signupForm) return;
    
    // Resto del código de registro...
    // (mantengo el código existente para el registro)
});