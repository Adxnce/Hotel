from django import forms
from .models import Reserva
from django.forms import DateInput

class ReservaForm(forms.ModelForm):
    class Meta:
        model = Reserva
        fields = ['habitacion', 'fecha_entrada', 'fecha_salida', 'cantidad_personas']
        widgets = {
            'fecha_entrada': DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'fecha_salida': DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Asegurarse de que todos los campos tengan la clase form-control para estilos de Bootstrap
        for field_name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})
