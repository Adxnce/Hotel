document.addEventListener('DOMContentLoaded', function() {
    // Obtener elementos del DOM
    const abrirCarrito = document.getElementById('abrir-carrito');
    const contadorCarrito = document.getElementById('contador-carrito');
    
    // Verificar si los elementos existen
    if (abrirCarrito) {
        // Agregar evento de clic al ícono del carrito
        abrirCarrito.addEventListener('click', function(e) {
            e.preventDefault();
            // Redirigir a la página del carrito
            window.location.href = '/carrito/';
        });
    }

    // Función para actualizar el contador del carrito
    function actualizarContadorCarrito() {
        // Obtener el carrito del localStorage o inicializarlo como array vacío
        const carrito = JSON.parse(localStorage.getItem('carrito')) || [];
        // Actualizar el contador
        if (contadorCarrito) {
            contadorCarrito.textContent = carrito.length;
            contadorCarrito.style.display = carrito.length > 0 ? 'block' : 'none';
        }
    }

    // Actualizar el contador al cargar la página
    actualizarContadorCarrito();

    // Agregar evento de clic a los botones de "Agregar al carrito"
    document.querySelectorAll('.btn-reservar').forEach(boton => {
        boton.addEventListener('click', function(e) {
            e.preventDefault();
            
            // Obtener datos de la habitación
            const habitacionId = this.dataset.habitacionId;
            const habitacionTipo = this.dataset.habitacionTipo || 'Habitación Estándar';
            const habitacionPrecio = parseFloat(this.dataset.habitacionPrecio) || 0;
            const fechaEntrada = document.getElementById('fecha_entrada').value;
            const fechaSalida = document.getElementById('fecha_salida').value;
            const cantidadPersonas = document.getElementById('cantidad_personas').value || 1;
            
            // Validar fechas
            if (!fechaEntrada || !fechaSalida) {
                alert('Por favor, selecciona las fechas de entrada y salida.');
                return;
            }
            
            // Crear objeto de reserva
            const reserva = {
                id: Date.now(), // ID único
                habitacion_id: habitacionId,
                tipo: habitacionTipo,
                precio: habitacionPrecio,
                fecha_entrada: fechaEntrada,
                fecha_salida: fechaSalida,
                cantidad_personas: cantidadPersonas,
                estado: 'pendiente'
            };
            
            // Obtener carrito actual o inicializar
            let carrito = JSON.parse(localStorage.getItem('carrito')) || [];
            
            // Agregar reserva al carrito
            carrito.push(reserva);
            
            // Guardar en localStorage
            localStorage.setItem('carrito', JSON.stringify(carrito));
            
            // Actualizar contador
            actualizarContadorCarrito();
            
            // Mostrar mensaje de éxito
            alert('Habitación agregada al carrito correctamente.');
            
            // Redirigir al carrito
            window.location.href = '/carrito/';
        });
    });
});
