from django import forms
from django.contrib.auth.forms import AuthenticationForm
from .models import Evento

class LoginForm(AuthenticationForm):
    username = forms.CharField(
        label="Correo Electrónico",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese su correo'})
    )
    password = forms.CharField(
        label="Contraseña",
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese su contraseña'})
    )


class EventoForm(forms.ModelForm):
    class Meta:
        model = Evento
        fields = [
            "estado_actual",
            "etapa_actual",
            "version_actual",
            "numero_version",
            "estado_version",
            "ruta_actual",  # Editable
            "tipo_evento",  # Editable
            "usuario_interesado_1",  # Editable
            "usuario_interesado_2",  # Editable
            "usuario_interesado_3",  # Editable
        ]
        widgets = {
            "estado_actual": forms.TextInput(attrs={"class": "form-control", "readonly": "readonly"}),
            "etapa_actual": forms.TextInput(attrs={"class": "form-control", "readonly": "readonly"}),
            "version_actual": forms.TextInput(attrs={"class": "form-control", "readonly": "readonly"}),
            "numero_version": forms.NumberInput(attrs={"class": "form-control", "readonly": "readonly"}),
            "estado_version": forms.TextInput(attrs={"class": "form-control", "readonly": "readonly"}),

            "ruta_actual": forms.TextInput(attrs={"class": "form-control"}),  # Editable
            "tipo_evento": forms.TextInput(attrs={"class": "form-control"}),  # Editable
            "usuario_interesado_1": forms.Select(attrs={"class": "form-control"}),  # Editable
            "usuario_interesado_2": forms.Select(attrs={"class": "form-control"}),  # Editable
            "usuario_interesado_3": forms.Select(attrs={"class": "form-control"}),  # Editable
        }
