from django.http import JsonResponse, HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect
import json
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.contrib import messages
from django.utils import timezone
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import ReservaForm
from .models import Habitacion, Reserva
from datetime import datetime

def login_redirect(request):
    """Redirige al usuario a la página de login."""
    return redirect('login')

# Create your views here.

def home_view(request):
    # Si el usuario no está autenticado, redirigir al login
    if not request.user.is_authenticated:
        return redirect(f'/login/?next={request.path}')
        
    habitaciones = Habitacion.objects.all()
    
    if request.method == 'POST':
        form = ReservaForm(request.POST)
        if form.is_valid():
            reserva = form.save(commit=False)
            if request.user.is_authenticated:
                reserva.cliente = request.user
                reserva.save()
                messages.success(request, '¡Reserva realizada con éxito!')
                return redirect('home')
            else:
                messages.warning(request, 'Debes iniciar sesión para realizar una reserva')
                return redirect(f'/login/?next={request.path}')
    else:
        form = ReservaForm()
    
    # Obtener las fechas para el datepicker
    hoy = timezone.now().date()
    fecha_min_entrada = hoy.strftime('%Y-%m-%d')
    fecha_min_salida = (hoy + timezone.timedelta(days=1)).strftime('%Y-%m-%d')
    
    from django.conf import settings
    
    context = {
        'form': form,
        'habitaciones': habitaciones,
        'fecha_min_entrada': fecha_min_entrada,
        'fecha_min_salida': fecha_min_salida,
        'user': request.user,
        'STATIC_URL': settings.STATIC_URL,
    }
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