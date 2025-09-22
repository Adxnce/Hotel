$(document).ready(function() {
    // Verificar si hay mensajes de Django para mostrar
    {% if messages %}
        {% for message in messages %}
            $('#error-message').text('{{ message }}').removeClass('d-none');
        {% endfor %}
    {% endif %}
    
    $('#login-form').on('submit', function(event) {
        // Evitamos que el formulario se envíe de la manera tradicional
        event.preventDefault();
        
        // Ocultar mensajes de error previos
        $('#error-message').addClass('d-none');

        // Obtenemos el token CSRF del input oculto en el formulario
        var csrfToken = $('input[name="csrfmiddlewaretoken"]').val();

        // Mostrar indicador de carga
        var submitBtn = $(this).find('button[type="submit"]');
        var originalBtnText = submitBtn.html();
        submitBtn.prop('disabled', true).html('<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span> Iniciando sesión...');

        // Hacemos la petición AJAX
        $.ajax({
            type: 'POST',
            url: '/login/',
            data: $(this).serialize(),
            headers: {
                'X-Requested-With': 'XMLHttpRequest',
                'X-CSRFToken': csrfToken
            },
            dataType: 'json',
            success: function(response) {
                // Si la respuesta del servidor contiene un 'redirect', redirigir
                if (response.redirect) {
                    window.location.href = response.redirect;
                } else if (response.message) {
                    // Redirección por defecto si no se especifica en la respuesta
                    window.location.href = '/home/';
                }
            },
            error: function(xhr, status, error) {
                // Restaurar botón
                submitBtn.prop('disabled', false).html(originalBtnText);
                
                // Mostrar mensaje de error
                var errorMessage = 'Error desconocido. Inténtalo de nuevo.';
                if (xhr.responseJSON && xhr.responseJSON.error) {
                    errorMessage = xhr.responseJSON.error;
                } else if (xhr.status === 0) {
                    errorMessage = 'No se pudo conectar con el servidor. Verifica tu conexión a internet.';
                } else if (xhr.status === 403) {
                    errorMessage = 'Acceso denegado. No tienes permiso para acceder a esta página.';
                } else if (xhr.status === 500) {
                    errorMessage = 'Error interno del servidor. Por favor, inténtalo más tarde.';
                }
                
                // Mostrar el error en el div que añadimos al HTML
                $('#error-message').text(errorMessage).removeClass('d-none');
                
                // Hacer scroll al mensaje de error
                $('html, body').animate({
                    scrollTop: $('#error-message').offset().top - 50
                }, 500);
                
                // Limpiar solo el campo de la contraseña por conveniencia del usuario
                $('#password').val('');
            }
        });
    });
});
