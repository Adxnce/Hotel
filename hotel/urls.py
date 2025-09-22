from django.urls import path
from django.views.generic import RedirectView
from django.contrib.auth.decorators import login_required
from hotel import views

urlpatterns = [
    # Ruta raíz redirige a login
    path('', views.login_redirect, name='root_redirect'),
    
    # Rutas de autenticación
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
    
    # Ruta protegida que requiere autenticación
    path('home/', login_required(views.home_view), name='home'),
]