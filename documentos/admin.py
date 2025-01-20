from django.contrib import admin
from .models import Proyecto, Subproyecto, Documento

# Registrar los modelos en Django Admin
admin.site.register(Proyecto)
admin.site.register(Subproyecto)
admin.site.register(Documento)
