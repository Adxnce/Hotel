$(document).ready(function() {



    $('#register-form').on('submit', function(event) {
        // Evitamos que el formulario se envíe de la manera tradicional
        event.preventDefault();
    
        // Obtenemos el token CSRF del input oculto en el formulario
        var csrfToken = $('input[name="csrfmiddlewaretoken"]').val();


        
        // Hacemos la petición AJAX
        $.ajax({
            type: 'POST',
            url: '/register/',
            data: $(this).serialize(),
            beforeSend: function(xhr) {
                xhr.setRequestHeader('X-CSRFToken', csrfToken);
            },
            success: function(response) {
                // Si la respuesta es exitosa, redirigimos o mostramos un mensaje
                alert("Registro exitoso. Ahora puedes iniciar sesión.");
            },
            error: function(xhr) {
                // Si hay un error, mostramos el mensaje correspondiente
                var errorMessage = xhr.responseJSON ? xhr.responseJSON.error : "Error en el registro. Inténtalo de nuevo.";
                $('#error-message').text(errorMessage).removeClass('d-none');
            }
        });
    });
});