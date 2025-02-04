from django.contrib import admin
from .models import PerfilUsuario, Proyecto, Subproyecto, Documento, Evento

class DocumentoAdmin(admin.ModelAdmin):
    list_display = ("codigo", "nombre", "estado_actual", "version_actual", "revisado", "aprobado")  # Mostrar estos campos en la lista
    list_filter = ("estado_actual", "revisado", "aprobado")  # Agregar filtros en la barra lateral
    search_fields = ("codigo", "nombre")  # Permitir búsqueda por código o nombre

# Registrar los modelos en Django Admin
admin.site.register(Proyecto)
admin.site.register(Subproyecto)
admin.site.register(Documento, DocumentoAdmin)  # Usamos DocumentoAdmin para mejorar la vista
admin.site.register(Evento)
admin.site.register(PerfilUsuario)
