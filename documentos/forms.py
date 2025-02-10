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

        # Eventos de Creación de Documento
        ("Solicitud de Creación de Versión Preliminar", "Solicitud de Creación de Versión Preliminar"),
        ("Solicitud de Revisión", "Solicitud de Revisión"),
        ("Solicitud de Corrección por Ingeniería", "Solicitud de Corrección por Ingeniería"),
        ("Documento Aprobado por Ingeniería", "Documento Aprobado por Ingeniería"),
        ("Solicitud de Aprobación por Calidad y Coordinación", "Solicitud de Aprobación por Calidad y Coordinación"),
        ("Solicitud de Corrección por Calidad", "Solicitud de Corrección por Calidad"),
        ("Documento Aprobado por Calidad", "Documento Aprobado por Calidad"),
        ("Solicitud de Corrección por Coordinación", "Solicitud de Corrección por Coordinación"),
        ("Solicitud de Superación de Numero Versión", "Solicitud de Superación de Numero Versión"),
        ("Solicitud de Creación de Versión Preliminar Superada", "Solicitud de Creación de Versión Preliminar Superada"),
        ("Solicitud de Creación de Versión Interdisciplinaria Superada", "Solicitud de Creación de Versión Interdisciplinaria Superada"),
        ("Solicitud de Superación de Versión", "Solicitud de Superación de Versión"),
        ("Solicitud de Creación de Versión Interdisciplinaria", "Solicitud de Creación de Versión Interdisciplinaria"),
        ("Solicitud de Creación de Versión Final", "Solicitud de Creación de Versión Final"),
        ("Solicitud de Envió de Documento al Cliente", "Solicitud de Envió de Documento al Cliente"),
        ("Solicitud de Cancelación de Envió de Documento al Cliente", "Solicitud de Cancelación de Envió de Documento al Cliente"),
        ("Actualización del Documento", "Actualización del Documento"),
        ("Suspensión del Documento", "Suspensión del Documento"),
        ("Eliminación del Documento", "Eliminación del Documento"),
        ("Reactivación del Documento", "Reactivación del Documento"),
        ("Solicitud de Creación de Medición o Actividad", "Solicitud de Creación de Medición o Actividad"),
        ("Solicitud de Revisión de Medición o Actividad", "Solicitud de Revisión de Medición o Actividad"),
        ("Creación de Informe de Medición o Actividad", "Creación de Informe de Medición o Actividad"),
        
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

