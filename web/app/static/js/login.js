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
            switch (response.status) {
                case 200:
                    // Inicio de sesión exitoso
                    if (successMessage) successMessage.style.display = 'block';
                    
                    // Guardar información en localStorage si es necesario
                    if (document.getElementById('remember')?.checked) {
                        localStorage.setItem('userEmail', email.value);
                        // No guardar contraseña por seguridad
                    }
                    
                    // Redirigir a la página principal
                    setTimeout(function() {
                        window.location.href = '/';
                    }, 800);
                    break;
                    
                case 401:
                    // Credenciales incompletas
                    showLoginError('Por favor complete todos los campos correctamente');
                    
                    // Resaltar los campos problemáticos
                    if (response.data.message.includes('contraseña')) {
                        showError(password, 'La contraseña no puede estar vacía');
                    }
                    if (response.data.message.includes('correo')) {
                        showError(email, 'El correo electrónico no puede estar vacío');
                    }
                    break;
                    
                case 403:
                    // Credenciales incorrectas
                    showLoginError('Correo electrónico o contraseña incorrectos');
                    
                    // Efecto de shake en el formulario para indicar error
                    loginForm.classList.add('shake');
                    setTimeout(() => loginForm.classList.remove('shake'), 500);
                    
                    // Limpiar el campo de contraseña
                    password.value = '';
                    break;
                    
                case 429:
                    // Demasiados intentos
                showLoginError('Demasiados intentos de inicio de sesión. Por favor, intente más tarde.');
                
                // Deshabilitar el formulario temporalmente
                const fields = loginForm.querySelectorAll('input, button');
                fields.forEach(field => field.disabled = true);
                
                // Habilitar después de un tiempo
                setTimeout(() => {
                    fields.forEach(field => field.disabled = false);
                    hideLoginError();
                }, 30000); // 30 segundos
                break;
                
            case 500:
                // Error del servidor
                showLoginError('Error del servidor. Por favor, intente más tarde.');
                console.error('Error del servidor:', response.data);
                break;
                
            default:
                // Otros errores
                showLoginError(response.data?.message || 'Error desconocido. Por favor, intente más tarde.');
                console.warn('Respuesta no manejada:', response);
                break;
            }


            // Ocultar mensaje de éxito si hubo error
            if (response.status !== 200 && successMessage) {
                successMessage.style.display = 'none';
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