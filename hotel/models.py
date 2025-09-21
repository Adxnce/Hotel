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
    ESTADOS_RESERVA = [
        ('PENDIENTE', 'Pendiente de pago'),
        ('CONFIRMADA', 'Confirmada'),
        ('CANCELADA', 'Cancelada'),
        ('COMPLETADA', 'Completada'),
    ]
    
    METODOS_PAGO = [
        ('EFECTIVO', 'Efectivo'),
        ('TARJETA', 'Tarjeta de Crédito/Débito'),
        ('TRANSFERENCIA', 'Transferencia Bancaria'),
    ]
    
    reserva_id = models.AutoField(primary_key=True, verbose_name="ID de Reserva")
    cliente = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reservas')
    habitacion = models.ForeignKey(Habitacion, on_delete=models.CASCADE, related_name='reservas')
    fecha_creacion = models.DateTimeField(verbose_name="Fecha de Creación", null=True, blank=True)
    fecha_entrada = models.DateField(verbose_name="Fecha de Entrada")
    fecha_salida = models.DateField(verbose_name="Fecha de Salida")
    cantidad_personas = models.PositiveIntegerField(verbose_name="Cantidad de Personas")
    estado = models.CharField(max_length=20, choices=ESTADOS_RESERVA, default='PENDIENTE', verbose_name="Estado")
    metodo_pago = models.CharField(max_length=20, choices=METODOS_PAGO, null=True, blank=True, verbose_name="Método de Pago")
    monto_total = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="Monto Total")
    observaciones = models.TextField(blank=True, null=True, verbose_name="Observaciones")
    
    class Meta:
        verbose_name = "Reserva"
        verbose_name_plural = "Reservas"
        ordering = ['-fecha_creacion']
        constraints = [
            models.CheckConstraint(
                check=models.Q(fecha_salida__gt=models.F('fecha_entrada')),
                name='fecha_salida_mayor_entrada',
                violation_error_message='La fecha de salida debe ser posterior a la fecha de entrada.'
            ),
            models.CheckConstraint(
                check=models.Q(cantidad_personas__gt=0),
                name='cantidad_personas_positiva',
                violation_error_message='La cantidad de personas debe ser mayor a cero.'
            )
        ]

    def __str__(self):
        return f"Reserva {self.reserva_id} - {self.cliente.get_full_name() or self.cliente.username}"
        
    def calcular_duracion_estadia(self):
        """Calcula la duración de la estadía en días."""
        return (self.fecha_salida - self.fecha_entrada).days
    
    def calcular_monto_total(self):
        """
        Calcula el monto total de la reserva basado en el precio de la habitación
        y la duración de la estadía.
        Este método debe ser implementado cuando se defina el modelo de precios.
        """
        # Por ahora, retornamos un valor fijo o 0
        return 0
    
    def esta_activa(self):
        """Verifica si la reserva está activa (entre las fechas de entrada y salida)."""
        from django.utils import timezone
        hoy = timezone.now().date()
        return self.fecha_entrada <= hoy < self.fecha_salida
    
    def save(self, *args, **kwargs):
        # Establecer la fecha de creación si es una nueva reserva
        if not self.reserva_id:
            from django.utils import timezone
            self.fecha_creacion = timezone.now()
            
        # Calcular el monto total antes de guardar
        if not self.monto_total:
            self.monto_total = self.calcular_monto_total()
            
        super().save(*args, **kwargs)