from django.db import models
from django.contrib.auth.models import User  # Usamos el modelo de usuario de Django

# Create your models here.
class Proyecto(models.Model):
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre


class Subproyecto(models.Model):
    nombre = models.CharField(max_length=100)
    proyecto = models.ForeignKey(Proyecto, on_delete=models.CASCADE)

    def __str__(self):
        return self.nombre

class Documento(models.Model):
    id = models.AutoField(primary_key=True)  # ID autoincremental
    codigo = models.CharField(max_length=100, unique=True)  # Código único del documento
    nombre = models.CharField(max_length=200)  # Nombre del documento
    subproyecto = models.ForeignKey(Subproyecto, on_delete=models.CASCADE)  # Relación con un proyecto
    fecha_creacion = models.DateTimeField(auto_now_add=True)  # Fecha de creación automática
    estado_actual = models.CharField(max_length=50, default="VIGENTE")  # Estado actual por defecto
    etapa_actual = models.CharField(max_length=50, null=True, blank=True)  # Etapa actual
    version_actual = models.CharField(max_length=50, null=True, blank=True)  # Versión actual
    numero_version = models.IntegerField(null=True, blank=True)  # Número de la versión
    estado_version = models.CharField(max_length=50, null=True, blank=True)  # Estado de la versión
    ruta_actual = models.CharField(max_length=255, null=True, blank=True)  # Ruta actual del documento

        # Nuevas columnas booleanas
    revisado = models.BooleanField(default=False)  # Indica si el documento ha sido revisado
    aprobado = models.BooleanField(default=False)  # Indica si el documento ha sido aprobado


    def __str__(self):
        return f"{self.codigo} - {self.nombre}"
    
class Evento(models.Model):
    documento = models.ForeignKey(Documento, on_delete=models.CASCADE)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name="usuario_evento")
    usuario_interesado_1 = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="usuario_interesado_1")
    usuario_interesado_2 = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="usuario_interesado_2")
    usuario_interesado_3 = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="usuario_interesado_3")
    fecha_creacion_evento = models.DateTimeField(auto_now_add=True)
    
    estado_actual = models.CharField(max_length=50, null=True, blank=True)
    etapa_actual = models.CharField(max_length=50, null=True, blank=True)
    version_actual = models.CharField(max_length=50, null=True, blank=True)
    numero_version = models.IntegerField(null=True, blank=True)
    estado_version = models.CharField(max_length=50, null=True, blank=True)
    ruta_actual = models.CharField(max_length=255, null=True, blank=True)
    
    tipo_evento = models.CharField(max_length=100)
    descripcion = models.TextField(null=True, blank=True)  # Mensaje predeterminado para cada evento
    comentarios = models.TextField(null=True, blank=True)  # Comentarios adicionales del usuario

    def __str__(self):
        return f"Evento {self.tipo_evento} - Documento: {self.documento.codigo}"
