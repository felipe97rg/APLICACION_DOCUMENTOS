import os
import sys
import django

# Asegurar que el script corre desde la raíz del proyecto
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Configurar el entorno de Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "aplicacion_documentos.settings")
django.setup()

from documentos.models import Proyecto, Subproyecto, Documento


# Borrar datos previos para evitar duplicados
Proyecto.objects.all().delete()
Subproyecto.objects.all().delete()
Documento.objects.all().delete()

# Crear proyectos
proyecto1 = Proyecto.objects.create(nombre="CEN-178")

# Crear subproyectos
subproyecto1 = Subproyecto.objects.create(nombre="SP 33", proyecto=proyecto1)


# Crear varios documentos para el mismo subproyecto
documentos_subproyecto1 = [
    {
        "codigo": "GPK-COL-LL34-LL34-ELE-EQM-308", 
        "nombre": "ESQUEMA GENERAL MANDO REMOTO RECONECTADORES CONEXIÓN PEL-GPK", 
        "fecha_creacion" : "2024-11-12"
    },

    {
        "codigo": "GPK-COL-LL34-LL34-ELE-LIS-327", 
        "nombre": "LISTADO DE SEÑALES - TABLERO MANDO REMOTO", 
        "fecha_creacion" : "2024-11-12"
    },


    {
        "codigo": "GPK-COL-LL34-LL34-ELE-HD-317", 
        "nombre": "HOJAS DE DATOS - TABLERO MANDO REMOTO", 
        "fecha_creacion" : "2024-11-12"
    },

    {
        "codigo": "GPK-COL-LL34-LL34-ELE-PPT-336", 
        "nombre": "DESCRIPCIÓN GENERAL Y FILOSOFÍA DE CONTROL - TABLERO MANDO REMOTO", 
        "fecha_creacion" : "2024-11-12"
    },

    {
        "codigo": "GPK-COL-LL34-TGN-ELE-DIA-316", 
        "nombre": "DIAGRAMA UNIFILAR DETALLADO TABLERO DE MANDO REMOTO RECONECTADORES CONEXIÓN PEL-TIGANA", 
        "fecha_creacion" : "2024-13-12"
    },

    {
        "codigo": "GPK-COL-LL34-TGN-ELE-PLT-349", 
        "nombre": "PLANO DE DISPOSICIÓN DE TABLERO Y CANALIZACIONES ELÉCTRICAS TIGANA - TABLERO MANDO REMOTO", 
        "fecha_creacion" : "2024-16-12"
    },

    {
        "codigo": "GPK-COL-LL34-TGN-ELE-TAB-304", 
        "nombre": "TABLA DE CONEXIONADO TIGANA - TABLERO MANDO REMOTO", 
        "fecha_creacion" : "2024-16-12"
    },

    {
        "codigo": "GPK-COL-LL34-JAC-ELE-DIA-343", 
        "nombre": "DIAGRAMA UNIFILAR DETALLADO TABLERO DE MANDO REMOTO RECONECTADORES CONEXIÓN PEL-JACANA", 
        "fecha_creacion" : "2024-13-12"
    },

    {
        "codigo": "GPK-COL-LL34-JAC-ELE-PLT-396", 
        "nombre": "PLANO DE DISPOSICIÓN DE TABLERO Y CANALIZACIONES ELÉCTRICAS JACANA - TABLERO MANDO REMOTO", 
        "fecha_creacion" : "2024-16-12"
    },

    {
        "codigo": "GPK-COL-LL34-JAC-ELE-TAB-310", 
        "nombre": "TABLA DE CONEXIONADO JACANA - TABLERO MANDO REMOTO", 
        "fecha_creacion" : "2024-18-12"
    }
]

for doc in documentos_subproyecto1:
    Documento.objects.create(
        codigo=doc["codigo"],
        nombre=doc["nombre"],
        subproyecto=subproyecto1,  # Todos asociados al mismo Subproyecto 1
        fecha_creacion = doc["fecha_creacion"],
        estado_actual="VIGENTE",
        etapa_actual="PRELIMINAR",
    )




print("✅ Base de datos poblada con éxito.")