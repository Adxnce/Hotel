from django.http import JsonResponse, HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.http import JsonResponse
from django.urls import reverse
import json
from datetime import datetime
from django.utils import timezone
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.db import transaction
from .forms import ReservaForm
from .models import Habitacion, Reserva
from datetime import datetime, timedelta
from django.contrib import messages


def login_redirect(request):
    """Redirige al usuario a la página de login."""
    return redirect('login')

# Create your views here.

def home_view(request):
    # Si el usuario no está autenticado, redirigir al login
    if not request.user.is_authenticated:
        return redirect(f'/login/?next={request.path}')
    
    # Obtener todas las habitaciones disponibles
    habitaciones = Habitacion.objects.all()
    
    # Inicializar el formulario de reserva
    form = ReservaForm()
    
    # Obtener las fechas para el datepicker
    hoy = timezone.now().date()
    fecha_min_entrada = hoy.strftime('%Y-%m-%d')
    fecha_min_salida = (hoy + timezone.timedelta(days=1)).strftime('%Y-%m-%d')
    
    # Configurar el contexto
    context = {
        'form': form,
        'habitaciones': habitaciones,
        'fecha_min_entrada': fecha_min_entrada,
        'fecha_min_salida': fecha_min_salida,
        'user': request.user,
        'STATIC_URL': '/static/',
    }
    
    # Manejar solicitudes POST
    if request.method == 'POST':
        form = ReservaForm(request.POST)
        if form.is_valid():
            try:
                # Crear la reserva
                reserva = form.save(commit=False)
                reserva.cliente = request.user
                reserva.estado = 'PENDIENTE'  # Estado inicial
                reserva.save()
                
                messages.success(request, '¡Habitación agregada al carrito correctamente!')
                return redirect('ver_carrito')
            except Exception as e:
                messages.error(request, f'Error al procesar la reserva: {str(e)}')
        else:
            # Si el formulario no es válido, mostrar errores
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'Error en {field}: {error}')
    
    return render(request, 'hotel/index.html', context)


def login_view(request):
    """
    Autentica al usuario usando Django y crea la sesión.
    El formulario envía 'email' y 'password'. Como el username se guarda igual al email,
    autenticamos con username=email.
    """
    # Si el usuario ya está autenticado, redirigir al home
    if request.user.is_authenticated:
        return redirect('home')
    
    next_url = request.GET.get('next', '')
    
    if request.method == 'POST':
        # Manejar solicitudes AJAX
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            username = request.POST.get('email')
            password = request.POST.get('password')
            user = authenticate(request, username=username, password=password)
            
            if user is not None:
                login(request, user)
                redirect_url = next_url if next_url else '/home/'
                return JsonResponse({
                    'message': 'Inicio de sesión exitoso', 
                    'redirect': redirect_url
                }, status=200)
            else:
                return JsonResponse({
                    'error': 'Credenciales inválidas. Inténtalo de nuevo.'
                }, status=401)
        else:
            # Manejar envío de formulario tradicional
            username = request.POST.get('email')
            password = request.POST.get('password')
            user = authenticate(request, username=username, password=password)
            
            if user is not None:
                login(request, user)
                return redirect(next_url if next_url else 'home')
            else:
                messages.error(request, 'Credenciales inválidas. Inténtalo de nuevo.')
                return redirect(f'/login/?next={next_url}' if next_url else 'login')

    # GET - Mostrar formulario de login
    context = {'next': next_url}
    return render(request, 'hotel/login.html', context)


def logout_view(request):
    """Cierra la sesión y redirige a la página de login."""
    logout(request)
    messages.info(request, 'Has cerrado sesión correctamente.')
    return redirect('login')

def register_view(request):
    """
    Gestiona el registro de un nuevo usuario.
    Crea el usuario y su perfil asociado con el número de teléfono.
    """
    if request.method == 'POST':
        # 1. Recuperamos los datos del formulario
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        password = request.POST.get('password')

        # 2. Realizamos las validaciones
        if not all([first_name, last_name, email, phone, password]):
            return JsonResponse({'error': 'Todos los campos son obligatorios.'}, status=400)

        if len(password) < 8:
            return JsonResponse({'error': 'La contraseña debe tener al menos 8 caracteres.'}, status=400)

        if '@' not in email or '.' not in email.split('@')[-1]:
            return JsonResponse({'error': 'El correo electrónico no es válido.'}, status=400)
        
        if User.objects.filter(email=email).exists():
            return JsonResponse({'error': 'Este correo electrónico ya está en uso.'}, status=400)

        phone_cleaned = ''.join(filter(str.isdigit, phone))
        if not (8 <= len(phone_cleaned) <= 15):
            return JsonResponse({'error': 'El teléfono debe tener entre 8 y 15 dígitos.'}, status=400)

        # 3. Creamos el usuario y guardamos el teléfono en su perfil
        try:
            # Creamos el usuario con los datos básicos
            user = User.objects.create_user(
                username=email, 
                email=email, 
                password=password, 
                first_name=first_name, 
                last_name=last_name
            )
            
            # Ahora le asignamos el teléfono y lo guardamos.
            user.profile.phone = phone_cleaned
            user.profile.save()

            print(f"Usuario '{user.username}' registrado con teléfono '{user.profile.phone}'.")

            return JsonResponse({'message': 'Registro exitoso. Ahora puedes iniciar sesión.'}, status=201)

        except Exception as e:
            print(f"Error al crear el usuario: {e}")
            return JsonResponse({'error': 'Ocurrió un error inesperado durante el registro.'}, status=500)

    # Si el método es GET, solo mostramos el formulario
    return render(request, 'hotel/register.html')

# Vistas para el carrito de compras

@login_required
def ver_carrito(request):
    """Muestra el carrito de compras del usuario actual."""
    # Obtener las reservas pendientes del usuario
    reservas = Reserva.objects.filter(
        cliente=request.user,
        estado='PENDIENTE'
    ).select_related('habitacion')
    
    # Calcular el total del carrito
    total_carrito = sum(reserva.monto_total for reserva in reservas if reserva.monto_total)
    
    context = {
        'reservas': reservas,
        'total_carrito': total_carrito,
    }
    return render(request, 'hotel/carrito.html', context)

@login_required
@require_POST
def agregar_al_carrito(request, habitacion_id):
    """Agrega una habitación al carrito de compras."""
    habitacion = get_object_or_404(Habitacion, pk=habitacion_id)
    
    # Obtener fechas del formulario
    fecha_entrada = request.POST.get('fecha_entrada')
    fecha_salida = request.POST.get('fecha_salida')
    cantidad_personas = int(request.POST.get('cantidad_personas', 1))
    
    try:
        fecha_entrada = datetime.strptime(fecha_entrada, '%Y-%m-%d').date()
        fecha_salida = datetime.strptime(fecha_salida, '%Y-%m-%d').date()
        
        # Validar fechas
        hoy = timezone.now().date()
        if fecha_entrada < hoy:
            messages.error(request, 'La fecha de entrada no puede ser anterior a hoy.')
            return redirect('home')
            
        if fecha_salida <= fecha_entrada:
            messages.error(request, 'La fecha de salida debe ser posterior a la fecha de entrada.')
            return redirect('home')
            
        # Verificar disponibilidad (simplificado)
        # En una implementación real, deberías verificar las fechas de reserva existentes
        
        # Crear la reserva en estado PENDIENTE
        reserva = Reserva(
            cliente=request.user,
            habitacion=habitacion,
            fecha_entrada=fecha_entrada,
            fecha_salida=fecha_salida,
            cantidad_personas=cantidad_personas,
            estado='PENDIENTE',
            monto_total=0  # Se calculará al guardar
        )
        reserva.save()  # Esto activará el cálculo del monto_total
        
        messages.success(request, 'Habitación agregada al carrito correctamente.')
        return redirect('ver_carrito')
        
    except ValueError as e:
        messages.error(request, 'Formato de fecha inválido.')
        return redirect('home')
    except Exception as e:
        messages.error(request, f'Error al agregar al carrito: {str(e)}')
        return redirect('home')

@login_required
def eliminar_del_carrito(request, reserva_id):
    """Elimina una reserva del carrito de compras."""
    reserva = get_object_or_404(Reserva, pk=reserva_id, cliente=request.user, estado='PENDIENTE')
    reserva.delete()
    return redirect('ver_carrito')

@login_required
def procesar_pago(request):
    """Procesa el pago de las reservas en el carrito."""
    if request.method == 'POST':
        try:
            # Obtener datos del formulario
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                data = json.loads(request.body)
                carrito_data = json.loads(data.get('carrito_data', '[]'))
                metodo_pago = data.get('metodo_pago', 'EFECTIVO')
                is_ajax = True
            else:
                carrito_data = json.loads(request.POST.get('carrito_data', '[]'))
                metodo_pago = request.POST.get('metodo_pago', 'EFECTIVO')
                is_ajax = False
            
            if not carrito_data:
                if is_ajax:
                    return JsonResponse({'error': 'No hay reservas para procesar.'}, status=400)
                messages.error(request, 'No hay reservas para procesar.')
                return redirect('ver_carrito')
            
            reservas_creadas = []
            
            with transaction.atomic():
                for item in carrito_data:
                    # Obtener el ID de la habitación
                    habitacion_id = item.get('habitacion_id') or item.get('id')
                    if not habitacion_id:
                        raise Exception('No se proporcionó un ID de habitación válido')
                    
                    # Buscar la habitación (manejar tanto string como enteros)
                    try:
                        # Primero intentar convertir a entero
                        habitacion_id_int = int(habitacion_id)
                        habitacion = Habitacion.objects.get(habitacion_id=habitacion_id_int)
                    except (ValueError, Habitacion.DoesNotExist):
                        # Si falla, intentar con el ID como string
                        try:
                            habitacion = Habitacion.objects.get(habitacion_id=str(habitacion_id))
                        except Habitacion.DoesNotExist:
                            # Si aún falla, intentar con el primer registro disponible
                            habitacion = Habitacion.objects.first()
                            if not habitacion:
                                raise Exception('No hay habitaciones disponibles en el sistema')
                    
                    # Obtener fechas
                    fecha_entrada = datetime.strptime(item.get('fecha_entrada'), '%Y-%m-%d').date()
                    fecha_salida = datetime.strptime(item.get('fecha_salida'), '%Y-%m-%d').date()
                    
                    # Calcular estadía
                    noches = max(1, (fecha_salida - fecha_entrada).days)
                    
                    # Obtener el precio del ítem del carrito o usar un valor por defecto
                    precio_noche = float(item.get('precio', 0))  # Usar el precio del carrito o 0 si no está definido
                    if precio_noche <= 0:
                        # Si no hay precio en el carrito, usar un valor por defecto basado en el tipo de habitación
                        if habitacion.tipo.lower() == 'sencilla':
                            precio_noche = 50.0
                        elif habitacion.tipo.lower() == 'doble':
                            precio_noche = 80.0
                        elif habitacion.tipo.lower() == 'suite':
                            precio_noche = 120.0
                        else:
                            precio_noche = 60.0  # Precio por defecto
                    
                    # Crear la reserva
                    reserva = Reserva(
                        cliente=request.user,
                        habitacion=habitacion,
                        fecha_entrada=fecha_entrada,
                        fecha_salida=fecha_salida,
                        cantidad_personas=item.get('cantidad_personas', 1),
                        monto_total=precio_noche * noches,
                        estado='CONFIRMADA',
                        metodo_pago=metodo_pago,
                        fecha_creacion=timezone.now()
                    )
                    reserva.save()
                    reservas_creadas.append(reserva)
            
            # Limpiar el carrito
            if 'carrito' in request.session:
                del request.session['carrito']
            
            # Redirigir a la página de recibo
            if is_ajax:
                return JsonResponse({
                    'status': 'success',
                    'reserva_id': reservas_creadas[0].reserva_id,
                    'redirect_url': reverse('ver_recibo', args=[reservas_creadas[0].reserva_id])
                })
            
            return redirect('ver_recibo', reserva_id=reservas_creadas[0].reserva_id)
            
        except Exception as e:
            error_msg = f'Error al procesar el pago: {str(e)}'
            if is_ajax:
                return JsonResponse({'error': error_msg}, status=500)
            messages.error(request, error_msg)
            return redirect('ver_carrito')
    
    return redirect('ver_carrito')

@login_required
def ver_recibo(request, reserva_id):
    """Muestra el recibo de la reserva confirmada."""
    reserva = get_object_or_404(Reserva, reserva_id=reserva_id, cliente=request.user)
    
    # Calcular estadísticas adicionales
    noches = (reserva.fecha_salida - reserva.fecha_entrada).days
    if noches < 1:
        noches = 1
    
    context = {
        'reserva': reserva,
        'noches': noches,
        'fecha_actual': timezone.now(),
    }
    
    return render(request, 'hotel/recibo.html', context)

@login_required
def mis_reservas(request):
    """Muestra el historial de reservas del usuario."""
    reservas = Reserva.objects.filter(
        cliente=request.user
    ).exclude(estado='PENDIENTE').order_by('-fecha_creacion')
    
    return render(request, 'hotel/mis_reservas.html', {
        'reservas': reservas,
    })