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


def obtener_documentos(request, subproyecto_id):
    documentos = Documento.objects.filter(subproyecto_id=subproyecto_id).values(
        'id', 'nombre', 'estado', 'version_actual'
    )
    return JsonResponse(list(documentos), safe=False)



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
    
    # Obtener eventos previos registrados para el documento
    eventos_previos = set(Evento.objects.filter(documento=documento).values_list("tipo_evento", flat=True))

    # 🚨 1. No se puede registrar ningún evento antes de la "Solicitud de Creación de Versión Preliminar"
    EVENTOS_PERMITIDOS_ANTES = {
        "Solicitud de Creación de Versión Preliminar",
        "Solicitud de Creación de Medición o Actividad",
        "Suspensión del documento",
        "Eliminación del documento",
    }

    if tipo_evento != "Solicitud de Creación de Versión Preliminar" and "Solicitud de Creación de Versión Preliminar" not in eventos_previos:
        if tipo_evento not in EVENTOS_PERMITIDOS_ANTES:
            return "❌ No puedes registrar este evento antes de realizar la 'Solicitud de Creación de Versión Preliminar'."
    
    # 🚨 2. No permitir duplicación de "Solicitud de Creación de Versión Preliminar"
    if tipo_evento == "Solicitud de Creación de Versión Preliminar" and "Solicitud de Creación de Versión Preliminar" in eventos_previos:
        return "⚠️ No se puede registrar otra 'Solicitud de Creación de Versión Preliminar' para este documento."

    # 🚨 3. No permitir aprobar un documento ya aprobado
    if tipo_evento == "Documento Aprobado por Calidad" and documento.aprobado:
        return "⚠️ Este documento ya ha sido aprobado por calidad y no puede aprobarse nuevamente."

    # 🚨 4. No permitir revisar un documento ya revisado
    if tipo_evento == "Documento Aprobado por Ingeniería" and documento.revisado:
        return "⚠️ Este documento ya ha sido revisado y no puede revisarse nuevamente."

    # 🚨 5. No permitir ciertos eventos sin revisión y aprobación
    if tipo_evento in {"Solicitud de Superación de Numero Versión", "Solicitud de Creación de Versión Preliminar Superada"}:
        if not documento.revisado or not documento.aprobado:
            return "⚠️ No puedes realizar este evento sin que el documento haya sido revisado y aprobado previamente."

    # 🚨 6. Validación de superación de número de versión
    if tipo_evento == "Solicitud de Superación de Numero Versión":
        # Última solicitud de superación previa
        ultima_solicitud = Evento.objects.filter(documento=documento, tipo_evento="Solicitud de Superación de Numero Versión").order_by("-fecha_creacion_evento").first()

        # No se puede superar la versión sin una solicitud previa
        if not ultima_solicitud:
            return "⚠️ No puedes superar la versión sin haber realizado una solicitud previa."

        # Verificar si ya se realizó una superación después de la última solicitud
        ultima_superacion = Evento.objects.filter(documento=documento, tipo_evento="Solicitud de Creación de Versión Preliminar Superada").order_by("-fecha_creacion_evento").first()

        if ultima_superacion and ultima_superacion.fecha_creacion_evento > ultima_solicitud.fecha_creacion_evento:
            return "⚠️ No puedes realizar otra superación sin una nueva solicitud previa."

    # 🚨 7. Restringir eventos en documentos con estados específicos
    if documento.estado_version == "ENVIO" and tipo_evento != "Solicitud de Cancelación de Envió de documento al cliente":
        return "⚠️ Solo puedes solicitar la 'Cancelación de Envío' en documentos con estado 'ENVIO'."

    if documento.estado_actual in ["SUSPENDIDO", "ELIMINADO"] and tipo_evento != "Reactivación del documento":
        return f"⚠️ Solo puedes reactivar documentos que están en estado '{documento.estado_actual.lower()}'"

    return None  # ✅ Si no hay errores, el evento es válido.




@restringir_eventos
@login_required
def registrar_evento(request, documento_id):
    """Vista para registrar un evento en un documento"""
    documento = get_object_or_404(Documento, id=documento_id)

    # **Definir descripciones de eventos**
    descripciones_eventos = {

        "Solicitud de Creación de Versión Preliminar": "Solicitud de creación de una versión preliminar del documento.",
        "Solicitud de Revisión": "Solicitud de revisión del documento.",
        "Solicitud de Corrección por Ingeniería": "Solicitud de corrección del documento por parte de ingeniería.",
        "Documento Aprobado por Ingeniería": "Documento aprobado por ingeniería.",
        "Solicitud de Aprobación por Calidad y Coordinación": "Solicitud de aprobación del documento por calidad y coordinación.",
        "Solicitud de Corrección por Calidad": "Solicitud de corrección del documento por calidad.",
        "Documento Aprobado por Calidad": "Documento aprobado por calidad.",
        "Solicitud de Corrección por Coordinación": "Solicitud de corrección del documento por coordinación.",  
        "Solicitud de Superación de Numero Versión": "Solicitud de superación de número de versión.",
        "Solicitud de Creación de Versión Preliminar Superada": "Solicitud de creación de una versión preliminar superada.",
        "Solicitud de Creación de Versión Interdisciplinaria Superada": "Solicitud de creación de una versión interdisciplinaria superada.",
        "Solicitud de Superación de Versión": "Solicitud de superación de versión.",
        "Solicitud de Creación de Versión Interdisciplinaria": "Solicitud de creación de una versión interdisciplinaria.",
        "Solicitud de Creación de Versión Final": "Solicitud de creación de una versión final.",
        "Solicitud de Envió de documento al cliente": "Solicitud de envío del documento al cliente.",
        "Solicitud de Cancelación de Envió de documento al cliente": "Solicitud de cancelación de envío del documento al cliente.",
        "Actualización del documento": "Actualización del documento.",
        "Suspensión del documento": "Suspensión del documento.",
        "Eliminación del documento": "Eliminación del documento.",
        "Reactivación del documento": "Reactivación del documento.",
        "Solicitud de Creación de Medición o Actividad": "Solicitud de creación de una medición o actividad.",
        "Solicitud de Revisión de Medición o Actividad": "Solicitud de revisión de una medición o actividad.",
        "Creación de Informe de Medición o Actividad": "Creación de un informe de medición o actividad.",
              
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

            # **Evento 1: Solicitud de Creación de Versión Preliminar**
            if evento.tipo_evento == "Solicitud de Creación de Versión Preliminar":
                documento.version_actual = "A"
                documento.numero_version = 1
                documento.ruta_actual = request.POST.get("ruta_actual", documento.ruta_actual)
                documento.revisado = False  # Reiniciar variable de revisado
                documento.aprobado = False  # Reiniciar variable de aprobado
                documento.etapa_actual = "PRELIMINAR"
                documento.estado_version = "CREACIÓN"
            
            # **Evento 2: Solicitud de Revisión**
            elif evento.tipo_evento == "Solicitud de Revisión":
                documento.ruta_actual = request.POST.get("ruta_actual", documento.ruta_actual)
                documento.estado_version = "REVISIÓN"

            # ** Evento 3: Solicitud de Corrección por Ingeniería**
            elif evento.tipo_evento == "Solicitud de Corrección por Ingeniería":
                documento.revisado = False  # Reiniciar variable de revisado
                documento.ruta_actual = request.POST.get("ruta_actual", documento.ruta_actual)
            
            # ** Evento 4: Documento Aprobado por Ingenieria**
            elif evento.tipo_evento == "Documento Aprobado por Ingeniería":
                documento.revisado = True  # Se marca como revisado por ingeniería
                documento.ruta_actual = request.POST.get("ruta_actual", documento.ruta_actual)

            # ** Evento 5: Solicitud de Aprobación por Calidad y Coordinación**
            elif evento.tipo_evento == "Solicitud de Aprobación por Calidad y Coordinación":
                documento.ruta_actual = request.POST.get("ruta_actual", documento.ruta_actual)

            # ** Evento 6: Solicitud de Corrección por Calidad**
            elif evento.tipo_evento == "Solicitud de Corrección por Calidad":
                documento.ruta_actual = request.POST.get("ruta_actual", documento.ruta_actual)

            # ** Evento 7: Documento Aprobado por Calidad**
            elif evento.tipo_evento == "Documento Aprobado por Calidad":
                documento.aprobado = True
                documento.ruta_actual = request.POST.get("ruta_actual", documento.ruta_actual)

            
            # ** Evento 8: Solicitud de Correción por Coordinación**
            elif evento.tipo_evento == "Solicitud de Corrección por Coordinación":
                documento.ruta_actual = request.POST.get("ruta_actual", documento.ruta_actual)
                documento.revisado = False  # Reiniciar variable de revisado
                documento.aprobado = False  # Reiniciar variable de aprobado

            # ** Evento 9: Solicitud de Superación de Versión Preliminar**
            elif evento.tipo_evento == "Solicitud de Superación de Numero Versión":
                documento.ruta_actual = request.POST.get("ruta_actual", documento.ruta_actual)

            # ** Evento 10: Solicitud de Creación de Versión Preliminar Superada**
            elif evento.tipo_evento == "Solicitud de Creación de Versión Preliminar Superada":    
                documento.revisado = False  # Reiniciar variable de revisado
                documento.aprobado = False  # Reiniciar variable de aprobado
                documento.estado_version = "CREACIÓN"  # Reiniciar variable de estado de versión
                documento.numero_version = (documento.numero_version or 0) + 1  # Incrementa el número de versión

            
            # ** Evento 11: Solicitud de Creación de Versión Interdisciplinaria Superada**
            elif evento.tipo_evento == "Solicitud de Creación de Versión Interdisciplinaria Superada":    
                documento.revisado = False  # Reiniciar variable de revisado
                documento.aprobado = False  # Reiniciar variable de aprobado
                documento.estado_version = "CREACIÓN"  # Reiniciar variable de estado de versión
                documento.numero_version = (documento.numero_version or 0) + 1  # Incrementa el número de versión


            # ** Evento 12: Solicitud de Superación de Versión"
            elif evento.tipo_evento == "Solicitud de Superación de Versión":
                documento.ruta_actual = request.POST.get("ruta_actual", documento.ruta_actual)

            # ** Evento 13: Solicitud de Creación de Versión Interdisciplinaria**
            elif evento.tipo_evento == "Solicitud de Creación de Versión Interdisciplinaria":
                documento.revisado = False  # Reiniciar variable de revisado
                documento.aprobado = False  # Reiniciar variable de aprobado
                documento.estado_version = "CREACIÓN"  # Reiniciar variable de estado de versión
                documento.etapa_actual = "INTERDISCIPLINARIA" # Cambia la etapa a "INTERDISCIPLINARIA"
                documento.version_actual = "B"  # Cambia la versión a "B":
                documento.numero_version = 1  # Reinicia el número de versión
                documento.ruta_actual = request.POST.get("ruta_actual", documento.ruta_actual)

            # ** Evento 14: Solicitud de Creación de Versión Final**
            elif evento.tipo_evento == "Solicitud de Creación de Versión Final":
                documento.revisado = False
                documento.aprobado = False
                documento.estado_version = "CREACIÓN"
                documento.etapa_actual = "FINAL"
                documento.version_actual = "0"
                documento.numero_version = None
                documento.ruta_actual = request.POST.get("ruta_actual", documento.ruta_actual)



            # ** Envento 15: Solicitud de Envio de documento al cliente**
            elif evento.tipo_evento == "Solicitud de Envió de documento al cliente":
                documento.estado_version = "ENVIO"
                documento.ruta_actual = request.POST.get("ruta_actual", documento.ruta_actual)
            
            # **Evento 16: Solicitud de Cancelacion de Envio de documento al cliente**
            elif evento.tipo_evento == "Solicitud de Cancelación de Envió de documento al cliente":
                documento.estado_version = "REVISIÓN"
                documento.ruta_actual = request.POST.get("ruta_actual", documento.ruta_actual)

            ############## Creacion de mediciones ##############

            # **Evento 17: Solicitud de Creación de Medición o Actividad**
            elif evento.tipo_evento == "Solicitud de Creación de Medición o Actividad":
                documento.ruta_actual = request.POST.get("ruta_actual", documento.ruta_actual)
                documento.etapa_actual = "MEDICION"
            
            # **Evento 18: Solicitud de Revisión de Medición o Actividad**
            elif evento.tipo_evento == "Solicitud de Revisión de Medición o Actividad":
                documento.ruta_actual = request.POST.get("ruta_actual", documento.ruta_actual)
            
            # **Evento 19: Creación de Informe de Medición o Actividad**
            elif evento.tipo_evento == "Creación de Informe de Medición o Actividad":
                documento.ruta_actual = request.POST.get("ruta_actual", documento.ruta_actual)

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