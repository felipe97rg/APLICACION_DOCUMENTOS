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
    TIPO_EVENTO_CHOICES = [
    ("SOLICITUD DE REVISIÓN PRELIMINAR", "Solicitud de Revisión Preliminar"),
    ("SOLICITUD DE CORRECCIÓN PRELIMINAR", "Solicitud de Corrección Preliminar"),
    ("DOCUMENTO REVISADO", "Documento Revisado por Ingeniería"),
    ("DOCUMENTO APROBADO", "Documento aprobado por Calidad"),
]


    tipo_evento = forms.ChoiceField(
        choices=TIPO_EVENTO_CHOICES,
        widget=forms.Select(attrs={"class": "form-control"}),
        label="Tipo de Evento"
    )

    comentarios = forms.CharField(
        widget=forms.Textarea(attrs={"class": "form-control", "placeholder": "Añadir comentarios..."}),
        required=True,  # Ahora es obligatorio
        label="Comentarios"
    )

    class Meta:
        model = Evento
        fields = [
            "estado_actual",
            "etapa_actual",
            "version_actual",
            "numero_version",
            "estado_version",
            "ruta_actual",
            "tipo_evento",
            "descripcion",  # Este campo sigue siendo de solo lectura
            "comentarios",  # Ahora es obligatorio
            "usuario_interesado_1",
            "usuario_interesado_2",
            "usuario_interesado_3",
        ]
        widgets = {
            "estado_actual": forms.TextInput(attrs={"class": "form-control", "readonly": "readonly"}),
            "etapa_actual": forms.TextInput(attrs={"class": "form-control", "readonly": "readonly"}),
            "version_actual": forms.TextInput(attrs={"class": "form-control", "readonly": "readonly"}),
            "numero_version": forms.NumberInput(attrs={"class": "form-control", "readonly": "readonly"}),
            "estado_version": forms.TextInput(attrs={"class": "form-control", "readonly": "readonly"}),
            "ruta_actual": forms.TextInput(attrs={"class": "form-control"}),
            "descripcion": forms.Textarea(attrs={"class": "form-control", "readonly": "readonly"}),  # No editable
            "usuario_interesado_1": forms.Select(attrs={"class": "form-control"}),
            "usuario_interesado_2": forms.Select(attrs={"class": "form-control"}),
            "usuario_interesado_3": forms.Select(attrs={"class": "form-control"}),
        }

