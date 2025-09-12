from django.http import JsonResponse
from django.shortcuts import render
import json

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

    if request.method == 'POST':
        # Recuperamos los datos del formulario enviado por .ajax
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        password = request.POST.get('password')

        print(first_name, last_name, email, phone, password)

        # Validamos todos los campos
        if not all([first_name, last_name, email, phone, password]):
            return JsonResponse({'error': 'Todos los campos son obligatorios.'}, status=400)

        # Validamos que la contraseña tenga al menos 8 caracteres
        if len(password) < 8:
            return JsonResponse({'error': 'La contraseña debe tener al menos 8 caracteres.'}, status=400)

        # Validamos que el email tenga un formato básico
        if '@' not in email or '.' not in email.split('@')[-1]:
            return JsonResponse({'error': 'El correo electrónico no es válido.'}, status=400)

        # Validamos que el teléfono tenga solo números y tenga entre 8 y 15 dígitos. Si tiene un +, lo borramos
        phone = phone.replace(' ', '').replace('-', '').replace('(', '').replace(')', '')
        if phone.startswith('+'):
            phone = phone[1:]
        if not phone.isdigit() or not (8 <= len(phone) <= 15):
            return JsonResponse({'error': 'El teléfono debe tener entre 8 y 15 dígitos y solo contener números.'}, status=400)

        # Si todas las validaciones pasan, simulamos el registro exitoso
        return JsonResponse({'message': 'Registro exitoso. Ahora puedes iniciar sesión.'}, status=200)

    

    return render(request, 'hotel/register.html')
