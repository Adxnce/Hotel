import os
import django
from datetime import datetime, timedelta

# Configurar el entorno de Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'app_hotelera.settings')
django.setup()

from hotel.models import Hotel, Habitacion

def create_sample_data():
    # Crear un hotel de ejemplo
    hotel, created = Hotel.objects.get_or_create(
        nombre='Hotel Premium',
        direccion='Calle Principal #123, Ciudad',
        categoria='5 estrellas'
    )
    
    # Tipos de habitaciones
    tipos_habitaciones = [
        {
            'tipo': 'Habitación Estándar',
            'capacidad': 2,
            'descripcion': 'Cómoda habitación con cama matrimonial o dos camas individuales, baño privado y TV.'
        },
        {
            'tipo': 'Habitación Deluxe',
            'capacidad': 3,
            'descripcion': 'Amplia habitación con cama king size, sofá cama, minibar y vista a la ciudad.'
        },
        {
            'tipo': 'Suite Ejecutiva',
            'capacidad': 4,
            'descripcion': 'Lujosa suite con sala de estar separada, jacuzzi y vista panorámica.'
        },
        {
            'tipo': 'Habitación Familiar',
            'capacidad': 5,
            'descripcion': 'Espaciosa habitación con dos habitaciones conectadas, ideal para familias.'
        },
        {
            'tipo': 'Suite Presidencial',
            'capacidad': 2,
            'descripcion': 'Nuestra suite más exclusiva con sala de estar, comedor, jacuzzi y servicio de mayordomo.'
        }
    ]
    
    # Crear las habitaciones
    for i, tipo in enumerate(tipos_habitaciones, 1):
        Habitacion.objects.get_or_create(
            hotel=hotel,
            tipo=tipo['tipo'],
            capacidad=tipo['capacidad'],
            descripcion=tipo['descripcion']
        )
    
    print("¡Datos de ejemplo creados exitosamente!")

if __name__ == '__main__':
    create_sample_data()
