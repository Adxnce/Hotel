// Variables globales
let carrito = [];
let total = 0;

// Elementos del DOM
const contenedorCarrito = document.getElementById('items-carrito');
const totalElemento = document.getElementById('total');
const botonVaciar = document.getElementById('vaciar-carrito');
const botonesAgregar = document.querySelectorAll('.btn-agregar');
const contadorCarrito = document.getElementById('contador-carrito');
const carritoLateral = document.getElementById('carrito-lateral');
const overlay = document.getElementById('overlay');
const abrirCarrito = document.getElementById('abrir-carrito');
const cerrarCarrito = document.getElementById('cerrar-carrito');
const botonFinalizarCompra = document.getElementById('finalizar-compra');

// Event Listeners
document.addEventListener('DOMContentLoaded', () => {
    // Cargar carrito desde localStorage si existe
    if (localStorage.getItem('carrito')) {
        carrito = JSON.parse(localStorage.getItem('carrito')) || [];
        actualizarCarrito();
    }

    // Evento para los botones de agregar al carrito
    botonesAgregar.forEach(boton => {
        boton.addEventListener('click', agregarAlCarrito);
    });

    // Evento para el botón de vaciar carrito
    if (botonVaciar) {
        botonVaciar.addEventListener('click', vaciarCarrito);
    }

    // Eventos para abrir/cerrar carrito
    if (abrirCarrito) {
        abrirCarrito.addEventListener('click', () => {
            carritoLateral.classList.add('activo');
            overlay.style.display = 'block';
            document.body.style.overflow = 'hidden';
        });
    }

    if (cerrarCarrito) {
        cerrarCarrito.addEventListener('click', cerrarCarritoSidebar);
    }

    if (overlay) {
        overlay.addEventListener('click', cerrarCarritoSidebar);
    }

    // Evento para finalizar compra
    if (botonFinalizarCompra) {
        botonFinalizarCompra.addEventListener('click', finalizarCompra);
    }
});

// Funciones
function agregarAlCarrito(e) {
    e.preventDefault();
    const boton = e.currentTarget;
    const habitacion = boton.closest('.habitacion');
    const tipo = habitacion.getAttribute('data-tipo');
    const precio = parseFloat(habitacion.getAttribute('data-precio'));
    const nombre = habitacion.querySelector('h3').textContent;
    
    // Verificar si el producto ya está en el carrito
    const itemExistente = carrito.find(item => item.tipo === tipo);
    
    if (itemExistente) {
        // Si ya existe, incrementar la cantidad
        itemExistente.cantidad++;
        itemExistente.subtotal = itemExistente.precio * itemExistente.cantidad;
    } else {
        // Si no existe, agregarlo al carrito
        carrito.push({
            tipo: tipo,
            nombre: nombre,
            precio: precio,
            cantidad: 1,
            subtotal: precio
        });
    }
    
    actualizarCarrito();
    guardarCarritoEnLocalStorage();
    mostrarNotificacion(`Habitación agregada al carrito`);
    
    // Mostrar el carrito después de agregar un ítem
    if (carritoLateral) {
        carritoLateral.classList.add('activo');
        overlay.style.display = 'block';
        document.body.style.overflow = 'hidden';
    }
}

function eliminarDelCarrito(tipo) {
    const itemIndex = carrito.findIndex(item => item.tipo === tipo);
    if (itemIndex > -1) {
        if (carrito[itemIndex].cantidad > 1) {
            // Si hay más de uno, disminuir la cantidad
            carrito[itemIndex].cantidad--;
            carrito[itemIndex].subtotal = carrito[itemIndex].precio * carrito[itemIndex].cantidad;
        } else {
            // Si solo hay uno, eliminarlo del carrito
            carrito.splice(itemIndex, 1);
        }
        actualizarCarrito();
        guardarCarritoEnLocalStorage();
        mostrarNotificacion('Habitación actualizada en el carrito');
    }
}

function actualizarCarrito() {
    // Limpiar el contenedor del carrito
    contenedorCarrito.innerHTML = '';
    
    // Si el carrito está vacío, mostrar mensaje
    if (carrito.length === 0) {
        contenedorCarrito.innerHTML = '<p class="carrito-vacio">El carrito está vacío</p>';
        total = 0;
        if (contadorCarrito) contadorCarrito.textContent = '0';
    } else {
        // Mostrar cada ítem del carrito
        carrito.forEach(item => {
            const elementoItem = document.createElement('div');
            elementoItem.classList.add('item-carrito');
            elementoItem.innerHTML = `
                <div class="item-info">
                    <h4>${item.nombre}</h4>
                    <div class="item-precio">$${item.precio.toFixed(2)} c/u</div>
                    <div class="item-cantidad">
                        <button class="disminuir" data-tipo="${item.tipo}">-</button>
                        <span>${item.cantidad}</span>
                        <button class="aumentar" data-tipo="${item.tipo}">+</button>
                    </div>
                </div>
                <div class="item-acciones">
                    <div class="item-subtotal">$${item.subtotal.toFixed(2)}</div>
                    <button class="eliminar-item" data-tipo="${item.tipo}"><i class="fas fa-trash"></i></button>
                </div>
            `;
            contenedorCarrito.appendChild(elementoItem);
        });
        
        // Calcular el total
        total = carrito.reduce((acc, item) => acc + item.subtotal, 0);
        
        // Actualizar contador del carrito
        const totalItems = carrito.reduce((acc, item) => acc + item.cantidad, 0);
        if (contadorCarrito) contadorCarrito.textContent = totalItems;
        
        // Agregar eventos a los botones
        document.querySelectorAll('.disminuir').forEach(boton => {
            boton.addEventListener('click', (e) => {
                const tipo = e.target.getAttribute('data-tipo');
                eliminarDelCarrito(tipo);
            });
        });
        
        document.querySelectorAll('.aumentar').forEach(boton => {
            boton.addEventListener('click', (e) => {
                const tipo = e.target.getAttribute('data-tipo');
                const item = carrito.find(item => item.tipo === tipo);
                if (item) {
                    item.cantidad++;
                    item.subtotal = item.precio * item.cantidad;
                    actualizarCarrito();
                    guardarCarritoEnLocalStorage();
                }
            });
        });
        
        document.querySelectorAll('.eliminar-item').forEach(boton => {
            boton.addEventListener('click', (e) => {
                const tipo = e.target.closest('button').getAttribute('data-tipo');
                carrito = carrito.filter(item => item.tipo !== tipo);
                actualizarCarrito();
                guardarCarritoEnLocalStorage();
                mostrarNotificacion('Habitación eliminada del carrito');
            });
        });
    }
    
    // Actualizar el total
    if (totalElemento) totalElemento.textContent = total.toFixed(2);
}

function vaciarCarrito() {
    if (confirm('¿Estás seguro de que deseas vaciar el carrito?')) {
        carrito = [];
        actualizarCarrito();
        guardarCarritoEnLocalStorage();
        mostrarNotificacion('Carrito vaciado');
    }
}

function cerrarCarritoSidebar() {
    carritoLateral.classList.remove('activo');
    overlay.style.display = 'none';
    document.body.style.overflow = 'auto';
}

function finalizarCompra() {
    if (carrito.length === 0) {
        mostrarNotificacion('El carrito está vacío');
        return;
    }
    
    // Aquí podrías redirigir a una página de pago o mostrar un formulario
    alert('¡Gracias por tu reserva! Pronto nos pondremos en contacto contigo para confirmar los detalles.');
    
    // Vaciar el carrito después de la compra
    carrito = [];
    actualizarCarrito();
    guardarCarritoEnLocalStorage();
    cerrarCarritoSidebar();
}

function guardarCarritoEnLocalStorage() {
    localStorage.setItem('carrito', JSON.stringify(carrito));
}

function mostrarNotificacion(mensaje) {
    // Crear notificación
    const notificacion = document.createElement('div');
    notificacion.classList.add('notificacion');
    notificacion.textContent = mensaje;
    
    // Agregar al documento
    document.body.appendChild(notificacion);
    
    // Mostrar con animación
    setTimeout(() => {
        notificacion.classList.add('mostrar');
    }, 10);
    
    // Ocultar después de 3 segundos
    setTimeout(() => {
        notificacion.classList.remove('mostrar');
        // Eliminar después de la animación
        setTimeout(() => {
            document.body.removeChild(notificacion);
        }, 300);
    }, 3000);
}
