$(document).ready(function() {
    
    
    $('#login-form').on('submit', function(event) {
        // Evitamos que el formulario se envíe de la manera tradicional
        event.preventDefault();

        // Obtenemos el token CSRF del input oculto en el formulario
        var csrfToken = $('input[name="csrfmiddlewaretoken"]').val();

        // Hacemos la petición AJAX
        $.ajax({
            type: 'POST',
            url: '',
            data: $(this).serialize(),
            
            // CAMBIO CLAVE: Añadimos el token CSRF a los encabezados de la petición
            beforeSend: function(xhr) {
                xhr.setRequestHeader('X-CSRFToken', csrfToken);
            },

            success: function(response) {
                // Si la respuesta del servidor contiene un 'message', la autenticación fue exitosa
                if (response.message) {
                    // Redirigimos al home
                    window.location.href = '/home/';
                }
            },
            error: function(xhr, status, error) {
                // Si hay un error (ej. 401 Unauthorized), mostramos el mensaje del servidor
                var errorMessage = 'Error desconocido. Inténtalo de nuevo.';
                if (xhr.responseJSON && xhr.responseJSON.error) {
                    errorMessage = xhr.responseJSON.error;
                }
                
                // Mostramos el error en el div que añadimos al HTML
                $('#error-message').text(errorMessage).removeClass('d-none');
                
                // Limpiamos solo el campo de la contraseña por conveniencia del usuario
                $('#password').val('');
            }
        });
    });
});
