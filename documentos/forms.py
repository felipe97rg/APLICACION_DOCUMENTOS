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
        ("Solicitud de de Creación de Versión Preliminar", "Solicitud de Creación de Versión Preliminar"),
        ("Solicitud de Revisión", "Solicitud de Revisión"),
        ("Solicitud de Corrección Preliminar", "Solicitud de Corrección Preliminar"),
        ("Documento Revisado por Ingeniería", "Documento Revisado por Ingeniería"),
        ("Documento Aprobado por Calidad", "Documento Aprobado por Calidad"),
        ("Solicitud de Superación Versión Interna", "Solicitud de Superación de Versión Interna"),
        ("Solicitud de Creación de Versión Interna Superada", "Solicitud de Creación de Versión Interna Superada"),
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

