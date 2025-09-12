from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


# Create your models here.

# Extiende el modelo User para agregar un campo de teléfono
class Profile(models.Model):
    # Se crea una relación uno-a-uno. Cada Usuario tiene un solo Perfil.
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=15, blank=True, null=True, verbose_name="Teléfono")
    
    def __str__(self):
        return self.user.username

@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    """
    Crea un perfil para el usuario si es un nuevo usuario.
    Actualiza el perfil si el usuario ya existe.
    """
    if created:
        # Si el usuario acaba de ser creado, creamos su perfil asociado.
        Profile.objects.create(user=instance)
    # Guardamos el perfil para asegurar que esté sincronizado.
    instance.profile.save()

# Crea un modelo Hotel que tenga hotel_id, nombre, direccion, categoria.
class Hotel(models.Model):
    hotel_id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    direccion = models.CharField(max_length=200)
    categoria = models.CharField(max_length=50)

    def __str__(self):
        return self.nombre

# Crea un modelo Habitacion que tenga habitacion_id, hotel (relacionado con Hotel), tipo, capacidad, descripcion.
class Habitacion(models.Model):
    habitacion_id = models.AutoField(primary_key=True)
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE)
    tipo = models.CharField(max_length=50)
    capacidad = models.IntegerField()
    descripcion = models.TextField(blank=True)

    def __str__(self):
        return f"Habitación {self.habitacion_id} - {self.tipo}"

#Crea un modelo Reserva que tenga reserva_id autoincrementable, cliente_id (relacionado con User), habitacion_id (relacionado con Habitacion), fecha_entrada, fecha_salida, cantidad_personas.
class Reserva(models.Model):
    reserva_id = models.AutoField(primary_key=True)
    cliente = models.ForeignKey(User, on_delete=models.CASCADE)
    habitacion = models.ForeignKey(Habitacion, on_delete=models.CASCADE)
    fecha_entrada = models.DateField()
    fecha_salida = models.DateField()
    cantidad_personas = models.IntegerField()

    def __str__(self):
        return f"Reserva {self.reserva_id} - {self.cliente.username}"