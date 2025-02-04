from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from documentos.decorators import restringir_eventos
from django.contrib import messages
from .forms import LoginForm, EventoForm
from .models import Proyecto, Subproyecto, Documento, Evento
from django.http import JsonResponse
from django.conf import settings
from django.core.mail import send_mail, EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
import pandas as pd
from django.core.files.storage import FileSystemStorage


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('dashboard')  # Redirige al dashboard después de iniciar sesión
        else:
            messages.error(request, "Credenciales incorrectas.")
    else:
        form = LoginForm()
    return render(request, 'documentos/login.html', {'form': form})

@login_required
def dashboard_view(request):
    proyectos = Proyecto.objects.all()  # Obtener todos los proyectos
    return render(request, 'documentos/dashboard.html', {'proyectos': proyectos})

@login_required
def get_subproyectos(request, proyecto_id):
    """ Devuelve los subproyectos asociados a un proyecto """
    subproyectos = list(Subproyecto.objects.filter(proyecto_id=proyecto_id).values("id", "nombre"))
    return JsonResponse(subproyectos, safe=False)

@login_required
def get_documentos(request, subproyecto_id):
    """ Devuelve los documentos asociados a un subproyecto """
    documentos = list(Documento.objects.filter(subproyecto_id=subproyecto_id).values("id", "codigo", "nombre"))
    return JsonResponse(documentos, safe=False)

def logout_view(request):
    logout(request)
    messages.success(request, "Has cerrado sesión exitosamente.")
    return redirect('login')  # Redirige a la página de inicio de sesión


@login_required
def get_documento_detalle(request, documento_id):
    """ Devuelve los detalles del documento seleccionado en formato JSON """
    documento = get_object_or_404(Documento, id=documento_id)
    data = {
        "estado_actual": documento.estado_actual,
        "etapa_actual": documento.etapa_actual,
        "version_actual": documento.version_actual,
        "numero_version": documento.numero_version,
        "estado_version": documento.estado_version,
        "ruta_actual": documento.ruta_actual,
        "revisado": documento.revisado,  # Nuevo campo
        "aprobado": documento.aprobado   # Nuevo campo
    }
    return JsonResponse(data)

@login_required
def get_eventos_documento(request, documento_id):
    """ Devuelve los eventos asociados a un documento en formato JSON """
    documento = get_object_or_404(Documento, id=documento_id)
    eventos = Evento.objects.filter(documento=documento).order_by("fecha_creacion_evento")

    data = [
        {
            "id": evento.id,
            "usuario": evento.usuario.username,
            "usuario_interesado_1": evento.usuario_interesado_1.username if evento.usuario_interesado_1 else None,
            "usuario_interesado_2": evento.usuario_interesado_2.username if evento.usuario_interesado_2 else None,
            "usuario_interesado_3": evento.usuario_interesado_3.username if evento.usuario_interesado_3 else None,
            "fecha": evento.fecha_creacion_evento.strftime("%Y-%m-%d %H:%M"),
            "estado_actual": evento.estado_actual,
            "version_actual": evento.version_actual,
            "numero_version": evento.numero_version,
            "estado_version": evento.estado_version,
            "ruta_actual": evento.ruta_actual,
            "tipo_evento": evento.tipo_evento,
            "descripcion": evento.descripcion,
            "comentarios": evento.comentarios,
                    }
        for evento in eventos
    ]

    return JsonResponse(data, safe=False)



@login_required
def upload_proyecto(request):
    if request.method == 'POST' and request.FILES.get('archivo_excel'):
        archivo = request.FILES['archivo_excel']
        fs = FileSystemStorage()
        filename = fs.save(archivo.name, archivo)
        file_path = fs.path(filename)

        try:
            # Leer el archivo Excel
            df = pd.read_excel(file_path, header=None)
            
            # Extraer Proyecto y Subproyecto
            proyecto_nombre = df.iloc[0, 1] if len(df) > 0 else None
            subproyecto_nombre = df.iloc[1, 1] if len(df) > 1 else None
            
            if not proyecto_nombre or not subproyecto_nombre:
                messages.error(request, 'El archivo no contiene información válida de proyecto y subproyecto')
                return redirect('upload_proyecto')
            
            # Verificar y crear Proyecto
            proyecto, _ = Proyecto.objects.get_or_create(nombre=proyecto_nombre)
            
            # Verificar y crear Subproyecto
            subproyecto, _ = Subproyecto.objects.get_or_create(nombre=subproyecto_nombre, proyecto=proyecto)
            
            # Leer documentos desde la fila 4 en adelante
            if len(df) > 3:
                for index, row in df.iloc[3:].iterrows():
                    if pd.notna(row[0]) and pd.notna(row[1]):  # Verifica que las celdas no estén vacías
                        documento_codigo = str(row[0]).strip()
                        documento_nombre = str(row[1]).strip()
                        
                        # Verificar si el documento ya existe antes de crearlo
                        if not Documento.objects.filter(codigo=documento_codigo).exists():
                            Documento.objects.create(
                                codigo=documento_codigo,
                                nombre=documento_nombre,
                                subproyecto=subproyecto
                            )
            
            messages.success(request, 'Archivo procesado exitosamente')
            return redirect('dashboard')  # Redirige al dashboard después del éxito
        except Exception as e:
            messages.error(request, f'Error al procesar el archivo: {str(e)}')
            return redirect('upload_proyecto')
    
    return render(request, 'documentos/upload_proyecto.html')


#**************************************************************************************************************************************#
#**************************************************************************************************************************************#
#**************************************************************************************************************************************#
#**************************************************************************************************************************************#
def validar_evento_permitido(documento, tipo_evento):
    """
    Verifica si el evento es válido para ser registrado en base a reglas de negocio.
    Retorna un mensaje de error si no se permite, o None si es válido.
    """

    # 🚀 Cacheamos consultas para evitar múltiples búsquedas innecesarias en la base de datos
    eventos_previos = Evento.objects.filter(documento=documento).values_list("tipo_evento", flat=True)
    
    # 🚫 Lista de eventos que NO pueden repetirse
    EVENTOS_UNICOS = {
        "Creación de Versión Preliminar",
        "Creacion de Versión Interdisciplinaria",
        "Creación de Versión Final",
        "Solicitud de Creación de Medición o Actividad"
    }

        # 🚨 No permitir eventos únicos duplicados
    if tipo_evento in EVENTOS_UNICOS and tipo_evento in eventos_previos:
        return f"⚠️ No se puede registrar otra '{tipo_evento}' para este documento."


    # 🚨 No se puede registrar ningún evento antes de la "Creación de Versión Preliminar",
    # excepto los permitidos explícitamente
    EVENTOS_PERMITIDOS_ANTES = {
        "Solicitud de Creación de Medición o Actividad",
        "Suspensión del documento",
        "Eliminación del documento",
    }

    if tipo_evento != "Creación de Versión Preliminar" and "Creación de Versión Preliminar" not in eventos_previos:
        if tipo_evento not in EVENTOS_PERMITIDOS_ANTES:
            return "❌ No puedes registrar este evento antes de realizar la 'Creación de Versión Preliminar'."


    # 🚨 Validaciones para eventos que dependen de solicitudes previas
    eventos_requeridos = {
        "Creación de Versión Interna Superada": "Solicitud de Superación de Numero de Versión Interna",
        "Creacion de Versión Interdisciplinaria": "Solicitud de Superación a Versión Interdisciplinaria",
        "Creación de Versión Interdisciplinaria Superada": "Solicitud de Superación de Numero de Versión Interdisciplinaria",
        "Creación de Versión Final": "Solicitud de Superación a Versión Final",
        "Creación de Versión Final Superada": "Solicitud de Superación de Numero de Versión Final",
    }

    if tipo_evento in eventos_requeridos and eventos_requeridos[tipo_evento] not in eventos_previos:
        return f"⚠️ No puedes crear una '{tipo_evento}' sin haber creado antes una '{eventos_requeridos[tipo_evento]}'." 

    # 🚨 No permitir revisar o aprobar si ya fue revisado/aprobado
    if tipo_evento == "Documento Aprobado por Calidad" and documento.aprobado:
        return "⚠️ Este documento ya ha sido aprobado y no puede aprobarse nuevamente."
    
    if tipo_evento == "Documento Revisado por Ingeniería" and documento.revisado:
        return "⚠️ Este documento ya ha sido revisado y no puede revisarse nuevamente."

    # 🚨 No permitir solicitar subir de versión sin ser revisado y aprobado
    eventos_que_requieren_revision = {
        "Solicitud de Superación a Versión Interdisciplinaria",
        "Creacion de Versión Interdisciplinaria",
        "Solicitud de Superación a Versión Final",
        "Creación de Versión Final"
    }
    
    if tipo_evento in eventos_que_requieren_revision and (not documento.revisado or not documento.aprobado):
        return "⚠️ No puedes crear o superar la versión sin que el documento haya sido revisado y aprobado previamente."

    # 🚨 No permitir avanzar sin haber pasado por la versión anterior
    if tipo_evento == "Creacion de Versión Interdisciplinaria" and documento.etapa_actual != "PRELIMINAR":
        return "⚠️ Solo puedes crear una 'Versión Interdisciplinaria' si el documento se encentra en la Versión Preliminar."

    if tipo_evento == "Creación de Versión Final" and documento.etapa_actual != "INTERDISCIPLINARIA":
        return "⚠️ Solo puedes crear una 'Versión Final' si el documento se encuentra en una Versión Interdisciplinaria."

    # 🚨 Validaciones de Envío y Cancelación de Envío
    if tipo_evento == "Solicitud de Envio de documento al cliente" and (not documento.revisado or not documento.aprobado or documento.version_actual == "A"):
        return "⚠️ No puedes solicitar el envío del documento al cliente si no ha sido revisado y aprobado o está en versión A."

    if tipo_evento == "Solicitud de Cancelación de Envio de documento al cliente" and "Solicitud de Envio de documento al cliente" not in eventos_previos:
        return "⚠️ No puedes solicitar la cancelación del envío del documento al cliente si no se ha solicitado el envío."

    # 🚨 No permitir registrar eventos en documentos eliminados o suspendidos, excepto si es Reactivación del documento
    if documento.estado_actual in ["ELIMINADO", "SUSPENDIDO"] and tipo_evento != "Reactivación del documento":
        return f"⚠️ No puedes registrar eventos en un documento que está {documento.estado_actual.lower()}, excepto la 'Reactivación del documento'." 
    
    # No permitir realizar el evento "Solicitud de Creación de Medición o Actividad" si existe una "Creación de Versión Preliminar"
    if tipo_evento == "Solicitud de Creación de Medición o Actividad" and "Creación de Versión Preliminar" in eventos_previos:
        return "⚠️ No puedes solicitar la creación de una medición o actividad si ya se ha creado la versión preliminar."
    
    # 🚨 Restricción de eventos después de "Solicitud de Creación de Medición o Actividad"
    EVENTOS_DESPUES_MEDICION = {
        "Solicitud de Revisión de Medición o Actividad",
        "Creación de Informe de Medición o Actividad",
        "Actualización del documento",
        "Suspensión del documento",
        "Eliminación del documento",
        "Reactivación del documento",
        "Solicitud de Corrección",
        "Solicitud de Revisión",

    }

    if "Solicitud de Creación de Medición o Actividad" in eventos_previos and tipo_evento not in EVENTOS_DESPUES_MEDICION:
        return "⚠️ Después de 'Solicitud de Creación de Medición o Actividad', solo puedes realizar eventos de superación de versión."
    

    return None  # ✅ Si no hay errores, el evento es válido.



@restringir_eventos
@login_required
def registrar_evento(request, documento_id):
    """Vista para registrar un evento en un documento"""
    documento = get_object_or_404(Documento, id=documento_id)

    # **Definir descripciones de eventos**
    descripciones_eventos = {

        # Eventos de Creación de Documento
        "Creación de Versión Preliminar": "Se ha creado la versión A del documento y se solicita la revisión preliminar de este para su primera evaluación.",
        "Creación de Versión Interna Superada": "Se ha creado la versión nueva del documento y se solicita la revisión de este para su evaluación.",

        "Creacion de Versión Interdisciplinaria": "Se ha creado la versión interdisciplinaria del documento y se solicita la revisión de este para su evaluación.",
        "Creación de Versión Interdisciplinaria Superada": "Se ha creado la versión nueva del documento y se solicita la revisión de este para su evaluación.",

        "Creación de Versión Final": "Se ha creado la versión final del documento y se solicita la revisión de este para su evaluación.",
        "Creación de Versión Final Superada": "Se ha creado la versión nueva del documento y se solicita la revisión de este para su evaluación.",

        # Eventos de Solicitudes de Documento
        "Solicitud de Revisión": "Se ha solicitado la revisión del documento.",
        "Solicitud de Corrección": "Se ha solicitado del documento.",
        "Solicitud de Envio de documento al cliente": "Se ha solicitado el envio del documento al cliente.",
        "Solicitud de Cancelación de Envio de documento al cliente": "Se ha solicitado la cancelación del envio del documento al cliente.",

        "Solicitud de Superación de Numero de Versión Interna": "Se ha solicitado subir el número de versión interna del documento.",

        "Solicitud de Superación a Versión Interdisciplinaria": "Se ha solicitado subir de versión interna (A) a Versión interdisciplinaria (B).",
        "Solicitud de Superación de Numero de Versión Interdisciplinaria": "Se ha solicitado subir el número de versión interdisciplinaria del documento.",

        "Solicitud de Superación a Versión Final": "Se ha solicitado subir de versión interdisciplinaria (B) a Version final (0).",
        "Solicitud de Superación de Numero de Versión Final": "Se ha solicitado subir el número de versión final del documento.",

        # Eventos de Documento de Medición o Actividad
        "Solicitud de Creación de Medición o Actividad": "Se ha solicitado la creación de una medición o actividad.",
        "Solicitud de Revisión de Medición o Actividad": "Se ha solicitado la revisión de una medición o actividad.",
        "Creación de Informe de Medición o Actividad": "Se ha creado el documento informe de medición o actividad.",	

        
        # Eventos de Revisión y Aprobación de Documento
        "Documento Revisado por Ingeniería": "El documento ha sido revisado por ingeniería.",
        "Documento Aprobado por Calidad": "El documento ha sido aprobado por calidad.",
        
        # Eventos de Modificacion de estado del Documento
        "Actualización del documento": "Se ha actualizado el documento.",
        "Suspensión del documento": "Se ha suspendido el documento.",
        "Eliminación del documento": "Se ha eliminado el documento.",
        "Reactivación del documento": "Se ha reactivado el documento.",
    }

    if request.method == "POST":
        form = EventoForm(request.POST)
        if form.is_valid():
            evento = form.save(commit=False)
            evento.documento = documento
            evento.usuario = request.user
            evento.estado_actual = documento.estado_actual
            evento.etapa_actual = documento.etapa_actual
            evento.version_actual = documento.version_actual
            evento.numero_version = documento.numero_version
            evento.estado_version = documento.estado_version
            evento.descripcion = descripciones_eventos.get(evento.tipo_evento, "Descripción no disponible")

###############################################     Validaciones de eventos      ################################################
            # 🚨 Verificar si el evento está permitido
            mensaje_error = validar_evento_permitido(documento, evento.tipo_evento)
            if mensaje_error:
                messages.error(request, mensaje_error)
                return redirect("registrar_evento", documento_id=documento.id)


################################################ Fin de Validaciones de eventos ################################################
            
################################################       Lógica de eventos        ################################################

############## Creacion de versiones ##############

            # **Evento 1: Creación de Versión Preliminar**
            if evento.tipo_evento == "Creación de Versión Preliminar":
                documento.version_actual = "A"
                documento.numero_version = 1
                documento.ruta_actual = request.POST.get("ruta_actual", documento.ruta_actual)
                documento.revisado = False  # Reiniciar variable de revisado
                documento.aprobado = False  # Reiniciar variable de aprobado
                documento.etapa_actual = "PRELIMINAR"
                           # **Evento 2: Creación de Versión Interna Superada**
            elif evento.tipo_evento == "Creación de Versión Interna Superada":
                documento.version_actual = "A"  # Mantiene la versión en "A"
                documento.numero_version = (documento.numero_version or 0) + 1  # Incrementa el número de versión
                documento.ruta_actual = request.POST.get("ruta_actual", documento.ruta_actual)                
                documento.revisado = False  # Reiniciar variable de revisado
                documento.aprobado = False  # Reiniciar variable de aprobado


            # **Evento 3: Creación de Versión Interdisciplinaria**
            elif evento.tipo_evento == "Creacion de Versión Interdisciplinaria":
                documento.version_actual = "B"  # Cambia la versión a "B"
                documento.numero_version = 1  # Reinicia el número de versión
                documento.ruta_actual = request.POST.get("ruta_actual", documento.ruta_actual)
                documento.revisado = False  # Reiniciar variable de revisado
                documento.aprobado = False  # Reiniciar variable de aprobado
                documento.etapa_actual = "INTERDISCIPLINARIA" # Cambia la etapa a "INTERDISCIPLINARIA"
            # **Evento 4: Creación de Versión Interdisciplinaria Superada**
            elif evento.tipo_evento == "Creación de Versión Interdisciplinaria Superada":
                documento.version_actual = "B"  # Mantiene la versión en "B"
                documento.numero_version = (documento.numero_version or 0) + 1  # Incrementa el número de versión
                documento.ruta_actual = request.POST.get("ruta_actual", documento.ruta_actual)
                documento.revisado = False  # Reiniciar variable de revisado
                documento.aprobado = False  # Reiniciar variable de aprobado
            
            # **Evento 5: Creación de Versión Final**
            elif evento.tipo_evento == "Creación de Versión Final":
                documento.version_actual = "0" # Cambia la versión a "0"
                documento.numero_version = None  # Reinicia el número de versión a null
                documento.ruta_actual = request.POST.get("ruta_actual", documento.ruta_actual)
                documento.revisado = False  # Reiniciar variable de revisado
                documento.aprobado = False  # Reiniciar variable de aprobado
                documento.etapa_actual = "FINAL" # Cambia la etapa a "FINAL"
            # **Evento 6: Creación de Versión Final Superada**
            elif evento.tipo_evento == "Creación de Versión Final Superada":
                documento.version_actual = (documento.version_actual or 0) + 1  # Incrementa el número de versión
                documento.ruta_actual = request.POST.get("ruta_actual", documento.ruta_actual)
                documento.revisado = False  # Reiniciar variable de revisado
                documento.aprobado = False  # Reiniciar variable de aprobado


############## Solicitudes ##############

            # **Evento 7: Solicitud de Revisión**
            elif evento.tipo_evento == "Solicitud de Revisión":
                documento.ruta_actual = request.POST.get("ruta_actual", documento.ruta_actual)

            # **Evento 8: Solicitud de Corrección Preliminar**
            elif evento.tipo_evento == "Solicitud de Corrección Preliminar":
                documento.estado_version = "CORRECCIÓN"
                documento.ruta_actual = request.POST.get("ruta_actual", documento.ruta_actual)
            
            # **Evento 9: Solicitud de envio de documento al cliente**
            elif evento.tipo_evento == "Solicitud de Envio de documento al cliente":
                documento.estado_actual = "ENVIO"
                documento.ruta_actual = request.POST.get("ruta_actual", documento.ruta_actual)

            # **Evento 10: Solicitud de Cancelacion de Envio de documento al cliente**
            elif evento.tipo_evento == "Solicitud de Cancelación de Envio de documento al cliente":
                documento.estado_actual = "VIGENTE"
                documento.ruta_actual = request.POST.get("ruta_actual", documento.ruta_actual)

            
            # **Evento 9: Solicitud de Superación de numero Versión Interna**
            elif evento.tipo_evento == "Solicitud de Superación de Numero de Versión Interna":
                documento.ruta_actual = request.POST.get("ruta_actual", documento.ruta_actual)


            # ** Evento 10: Solicitud de superación a Versión Interdisciplinaria**
            elif evento.tipo_evento == "Solicitud de Superación a Versión Interdisciplinaria":
                documento.ruta_actual = request.POST.get("ruta_actual", documento.ruta_actual)
            # **Evento 11: Solicitud de Superación de Numero de Versión Interdisciplinaria**
            elif evento.tipo_evento == "Solicitud de Superación de Numero de Versión Interdisciplinaria":
                documento.ruta_actual = request.POST.get("ruta_actual", documento.ruta_actual)


            # **Evento 12: Solicitud de superación a Versión Final**
            elif evento.tipo_evento == "Solicitud de Superación a Versión Final":
                documento.ruta_actual = request.POST.get("ruta_actual", documento.ruta_actual)
            # **Evento 13: Solicitud de Superación de Numero de Versión Final**
            elif evento.tipo_evento == "Solicitud de Superación de Numero de Versión Final":
                documento.ruta_actual = request.POST.get("ruta_actual", documento.ruta_actual)

############## Documento de Medición o Actividad ##############

            # **Evento 14: Solicitud de Creación de Medición o Actividad**
            elif evento.tipo_evento == "Solicitud de Creación de Medición o Actividad":
                documento.ruta_actual = request.POST.get("ruta_actual", documento.ruta_actual)
                documento.estado_actual = "Actividad"
            
            # **Evento 15: Solicitud de Revisión de Medición o Actividad**
            elif evento.tipo_evento == "Solicitud de Revisión de Medición o Actividad":
                documento.ruta_actual = request.POST.get("ruta_actual", documento.ruta_actual)

            # **Evento 16: Creación de Informe de Medición o Actividad**
            elif evento.tipo_evento == "Creación de Informe de Medición o Actividad":
                documento.ruta_actual = request.POST.get("ruta_actual", documento.ruta_actual)

            
############## Revisiones y Aprobaciones ##############

            # **Evento 14: Documento Revisado**
            elif evento.tipo_evento == "Documento Revisado por Ingeniería":
                documento.revisado = True  # Se marca como revisado

            # **Evento 15: Documento Aprobado**
            elif evento.tipo_evento == "Documento Aprobado por Calidad":
                documento.aprobado = True  # Se marca como aprobado

############## Modificaciones de estado ##############

            # **Evento 16: Actualización del documento**
            elif evento.tipo_evento == "Actualización del documento":
                documento.estado_actual = "ACTUALIZADO"
                documento.ruta_actual = request.POST.get("ruta_actual", documento.ruta_actual)
            # **Evento 17: Suspensión del documento**
            elif evento.tipo_evento == "Suspensión del documento":
                documento.estado_actual = "SUSPENDIDO"
                documento.ruta_actual = request.POST.get("ruta_actual", documento.ruta_actual)
            # **Evento 18: Eliminación del documento**
            elif evento.tipo_evento == "Eliminación del documento":
                documento.estado_actual = "ELIMINADO"
                documento.ruta_actual = request.POST.get("ruta_actual", documento.ruta_actual)
            # **Evento 19: Reactivación del documento**
            elif evento.tipo_evento == "Reactivación del documento":
                documento.estado_actual = "VIGENTE"
                documento.ruta_actual = request.POST.get("ruta_actual", documento.ruta_actual)

           
            documento.save()
            evento.save()

            # **📧 Enviar correo si hay destinatarios**
            destinatarios = [
                evento.usuario_interesado_1.email if evento.usuario_interesado_1 else None,
                evento.usuario_interesado_2.email if evento.usuario_interesado_2 else None,
                evento.usuario_interesado_3.email if evento.usuario_interesado_3 else None,
            ]
            destinatarios = [email for email in destinatarios if email]

            if destinatarios:
                subject = f"📄 Nuevo Evento Registrado: {evento.tipo_evento}"
                html_message = render_to_string("documentos/correo_evento.html", {
                    "documento": documento,
                    "evento": evento,
                })
                plain_message = strip_tags(html_message)
                from_email = settings.DEFAULT_FROM_EMAIL

                email = EmailMultiAlternatives(subject, plain_message, from_email, destinatarios)
                email.attach_alternative(html_message, "text/html")
                email.send()

            # ✅ Guardar mensaje de éxito y redirigir al Dashboard
            messages.success(request, f"✅ Evento '{evento.tipo_evento}' se ha registrado con éxito.")
            return redirect("dashboard")  # Aquí redirige con el mensaje

    else:
        form = EventoForm(initial={
            "estado_actual": documento.estado_actual,
            "etapa_actual": documento.etapa_actual,
            "version_actual": documento.version_actual,
            "numero_version": documento.numero_version,
            "estado_version": documento.estado_version,
            "ruta_actual": documento.ruta_actual,
            "descripcion": descripciones_eventos.get("Creación de Versión Preliminar", "Descripción no disponible"),
        })

    return render(request, "documentos/registrar_evento.html", {"form": form, "documento": documento, "usuario": request.user})