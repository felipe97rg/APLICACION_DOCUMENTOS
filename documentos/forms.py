from django import forms
from django.contrib.auth.forms import AuthenticationForm
from .models import Evento, Documento, User,  HorasHombre, Proyecto, Subproyecto
from documentos import models
from decimal import Decimal  # <-- AÑADE ESTA LÍNEA



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
        ("Selecciona el tipo de evento","Selecciona el tipo de evento"),
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

        ("Solicitud de Creación de Código", "Solicitud de Creación de Código"),

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

    correos_adicionales = forms.CharField(
        required=False, 
        widget=forms.TextInput(attrs={"placeholder": "Correos adicionales separados por comas"})
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
            "correos_adicionales"
        ]
        widgets = {
            "estado_actual": forms.TextInput(attrs={"class": "form-control", "readonly": "readonly"}),
            "etapa_actual": forms.TextInput(attrs={"class": "form-control", "readonly": "readonly"}),
            "version_actual": forms.TextInput(attrs={"class": "form-control", "readonly": "readonly"}),
            "numero_version": forms.NumberInput(attrs={"class": "form-control", "readonly": "readonly"}),
            "estado_version": forms.TextInput(attrs={"class": "form-control", "readonly": "readonly"}),
            "ruta_actual": forms.TextInput(attrs={"class": "form-control"}),
            "descripcion": forms.Textarea(attrs={"class": "form-control", "readonly": "readonly"}),  # No editable
            "usuario_interesado_1":forms.Select(attrs={"class": "form-control"}),
            "usuario_interesado_2": forms.Select(attrs={"class": "form-control"}),
            "usuario_interesado_3": forms.Select(attrs={"class": "form-control"}),
            "correos_adicionales": forms.TextInput(attrs={"class": "form-control"})
        }

# --- INICIO DE CAMBIOS ---

# 1. Definimos las opciones para el tipo de actividad.
#    Puedes modificar esta lista según tus necesidades.
ACTIVIDAD_CHOICES = [
    ('', 'Seleccione una actividad...'), # Opción por defecto
    ('Documentación', 'Documentación'),
    ('Reunión', 'Reunión'),
    ('Diseño', 'Diseño'),
    ('Capacitación', 'Capacitación'),
    ("Visita a Campo", "Visita a Campo"),
]

# 2. Generamos dinámicamente las opciones para las horas.
#    Aquí creamos una lista de 0.5 a 10.0 horas. Puedes ajustar el rango(1, 21) si necesitas más.
HORAS_CHOICES = [
    ('', 'Seleccione las horas...') # Opción por defecto
] + [(Decimal(f'{i/2:.1f}'), f'{i/2:.1f} horas') for i in range(1, 21)] # Genera de 0.5 a 10.0


# 3. Modificamos tu clase HorasHombreForm
class HorasHombreForm(forms.ModelForm):
    # Sobrescribimos los campos del modelo para convertirlos en listas desplegables.
    # Esto tiene prioridad sobre lo que se define en la clase Meta.

    tipo_actividad = forms.ChoiceField(
        choices=ACTIVIDAD_CHOICES,
        label="Tipo de Actividad",
        widget=forms.Select(attrs={'class': 'form-select'}) # 'form-select' es la clase de Bootstrap 5 para <select>
    )

    cantidad_horas = forms.TypedChoiceField(
        choices=HORAS_CHOICES,
        coerce=Decimal, # Asegura que el valor se guarde como un número (Decimal), no como texto.
        label="Cantidad de Horas",
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    # Mantenemos tus campos existentes que ya funcionaban bien.
    proyecto = forms.ModelChoiceField(queryset=Proyecto.objects.all(), required=False, label="Proyecto", widget=forms.Select(attrs={'class': 'form-select'}))
    subproyecto = forms.ModelChoiceField(queryset=Subproyecto.objects.all(), required=False, label="Subproyecto", widget=forms.Select(attrs={'class': 'form-select'}))
    documento = forms.ModelChoiceField(queryset=Documento.objects.all(), required=False, label="Documento", widget=forms.Select(attrs={'class': 'form-select'}))

    class Meta:
        model = HorasHombre
        # El orden aquí define el orden en que aparecerán los campos en el formulario.
        fields = ['proyecto', 'subproyecto', 'documento', 'tipo_actividad', 'fecha', 'cantidad_horas']
        
        # Ya no necesitamos definir 'tipo_actividad' ni 'cantidad_horas' aquí,
        # pero mantenemos el widget para el campo de fecha.
        widgets = {
            'fecha': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        }

# --- FIN DE CAMBIOS ---

#Proyectos obligatorios y busquedaro en horas hombre