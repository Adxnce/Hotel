from django.urls import path
from django.views.generic import RedirectView
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
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
    
    # Rutas del carrito de compras
    path('carrito/', login_required(views.ver_carrito), name='ver_carrito'),
    path('agregar-al-carrito/<int:habitacion_id>/', login_required(views.agregar_al_carrito), name='agregar_al_carrito'),
    path('eliminar-del-carrito/<int:reserva_id>/', login_required(views.eliminar_del_carrito), name='eliminar_del_carrito'),
    path('procesar-pago/', login_required(views.procesar_pago), name='procesar_pago'),
    path('mis-reservas/', login_required(views.mis_reservas), name='mis_reservas'),
    path('recibo/<int:reserva_id>/', login_required(views.ver_recibo), name='ver_recibo'),
]