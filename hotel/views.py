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

