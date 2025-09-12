from django.http import JsonResponse
from django.shortcuts import render
import json
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User

# Create your views here.

def home_view(request):
    return render(request, 'hotel/home.html')


def login_view(request):
    # Usuario mock
    user_mock = {
        'username': 'admin',
        'password': 'password123'
    }

    if request.method == 'POST':
        
        # Recuperamos los datos del formulario enviado por .ajax
        username = request.POST.get('username')
        password = request.POST.get('password')

        if username == user_mock['username'] and password == user_mock['password']:
            
            # Si las credenciales son correctas, enviamos un JSON de éxito
            return JsonResponse({'message': 'Inicio de sesión exitoso'}, status=200)
        else:
            
            # Si son incorrectas, error
            return JsonResponse({'error': 'Credenciales inválidas. Inténtalo de nuevo.'}, status=401)
    
    # Si el método es GET, simplemente renderizamos la página de login
    return render(request, 'hotel/login.html')

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