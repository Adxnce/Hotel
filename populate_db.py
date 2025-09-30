import os
import django
from datetime import datetime, timedelta

# Configurar el entorno de Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'app_hotelera.settings')
django.setup()

from hotel.models import Hotel, Habitacion

def create_sample_data():
    """
    Crea datos de ejemplo para el hotel solo si no existen.
    Utiliza get_or_create para evitar duplicados.
    """
    
    # Verificar si ya existen datos
    if Hotel.objects.exists():
        print("✓ Los datos ya existen en la base de datos.")
        print(f"  - Hoteles registrados: {Hotel.objects.count()}")
        print(f"  - Habitaciones registradas: {Habitacion.objects.count()}")
        return
    
    print("🏨 Creando datos de ejemplo para el hotel...")
    
    # Crear un hotel de ejemplo
    hotel, created = Hotel.objects.get_or_create(
        nombre='Hotel Premium',
        defaults={
            'direccion': 'Calle Principal #123, Ciudad',
            'categoria': '5 estrellas'
        }
    )
    
    if created:
        print(f"✓ Hotel creado: {hotel.nombre}")
    else:
        print(f"✓ Hotel ya existía: {hotel.nombre}")
    
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
    habitaciones_creadas = 0
    for i, tipo_data in enumerate(tipos_habitaciones, 1):
        habitacion, created = Habitacion.objects.get_or_create(
            hotel=hotel,
            tipo=tipo_data['tipo'],
            defaults={
                'capacidad': tipo_data['capacidad'],
                'descripcion': tipo_data['descripcion']
            }
        )
        
        if created:
            habitaciones_creadas += 1
            print(f"✓ Habitación creada: {habitacion.tipo}")
        else:
            print(f"✓ Habitación ya existía: {habitacion.tipo}")
    
    print(f"\n🎉 Proceso completado:")
    print(f"  - Habitaciones nuevas creadas: {habitaciones_creadas}")
    print(f"  - Total de habitaciones: {Habitacion.objects.count()}")

def check_database_status():
    """
    Verifica el estado actual de la base de datos.
    """
    print("\n📊 Estado actual de la base de datos:")
    print(f"  - Hoteles: {Hotel.objects.count()}")
    print(f"  - Habitaciones: {Habitacion.objects.count()}")
    
    if Hotel.objects.exists():
        for hotel in Hotel.objects.all():
            print(f"    🏨 {hotel.nombre} ({hotel.categoria})")
            habitaciones = hotel.habitacion_set.all()
            for hab in habitaciones:
                print(f"      🛏️  {hab.tipo} (Capacidad: {hab.capacidad})")

if __name__ == '__main__':
    try:
        print("🚀 Iniciando script de población de datos...")
        create_sample_data()
        check_database_status()
    except Exception as e:
        print(f"❌ Error al ejecutar el script: {e}")
        print("Asegúrate de que:")
        print("  1. La base de datos PostgreSQL esté funcionando")
        print("  2. Las credenciales sean correctas")
        print("  3. La base de datos 'HotelDatabase' exista")
