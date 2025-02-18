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

        ("Creación de Versión Preliminar", "Creación de Versión Preliminar"),
        ("Creación de Versión Interna Superada", "Creación de Versión Interna Superada"),

        ("Creación de Versión Interdisciplinaria", "Creación de Versión Interdisciplinaria"),
        ("Creación de Versión Interdisciplinaria Superada", "Creación de Versión Interdisciplinaria Superada"),

        ("Creación de Versión Final", "Creación de Versión Final"),
        ("Creación de Versión Final Superada", "Creación de Versión Final Superada"),

        # Eventos de Solicitudes de Documento
        ("Solicitud de Revisión", "Solicitud de Revisión"),
        ("Solicitud de Corrección por Calidad", "Solicitud de Corrección por Calidad"),
        ("Solicitud de Corrección por Ingeniería", "Solicitud de Corrección por Ingeniería"),
        ("Solicitud de Envio de documento al cliente", "Solicitud de Envio de documento al cliente"),
        ("Solicitud de Cancelación de Envio de documento al cliente", "Solicitud de Cancelación de Envio de documento al cliente"),

        ("Solicitud de Superación de Numero de Versión Interna", "Solicitud de Superación de Numero de Versión Interna"),

        ("Solicitud de Superación a Versión Interdisciplinaria", "Solicitud de Superación a Versión Interdisciplinaria"),
        ("Solicitud de Superación de Numero de Versión Interdisciplinaria", "Solicitud de Superación de Numero de Versión Interdisciplinaria"),

        ("Solicitud de Superación a Versión Final", "Solicitud de Superación a Versión Final"),
        ("Solicitud de Superación de Numero de Versión Final", "Solicitud de Superación de Numero de Versión Final"),

        # Eventos de creacion de Mediciones y Actividades
        
        ("Solicitud de Creación de Medición o Actividad", "Solicitud de Creación de Medición o Actividad"),
        ("Solicitud de Revisión de Medición o Actividad", "Solicitud de Revisión de Medición o Actividad"),
        ("Creación de Informe de Medición o Actividad", "Creación de Informe de Medición o Actividad"),


        # Eventos de Revisión y Aprobación de Documento
        ("Documento Aprobado por Ingeniería", "Documento Aprobado por Ingeniería"),
        ("Documento Aprobado por Calidad", "Documento Aprobado por Calidad"),

        # Eventos de Modificacion de estado del Documento
        ("Actualización del documento", "Actualización del documento"),
        ("Suspensión del documento", "Suspensión del documento"),
        ("Eliminación del documento", "Eliminación del documento"),
        ("Reactivación del documento", "Reactivación del documento"),
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

