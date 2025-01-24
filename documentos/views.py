from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import LoginForm, EventoForm
from .models import Proyecto, Subproyecto, Documento, Evento
from django.http import JsonResponse
from django.conf import settings
from django.core.mail import send_mail, EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags



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
def dashboard_view(request):
    """ Muestra el Dashboard con la lista de proyectos """
    proyectos = Proyecto.objects.all()
    return render(request, "documentos/dashboard.html", {"proyectos": proyectos})

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
def registrar_evento(request, documento_id):
    """Vista para registrar un evento en un documento"""
    documento = get_object_or_404(Documento, id=documento_id)

    # Mensajes predeterminados según el tipo de evento
    descripciones_eventos = {
        "SOLICITUD DE REVISIÓN PRELIMINAR": "Se ha creado la versión A del documento y se solicita la revisión preliminar de este para su primera evaluación.",
        "SOLICITUD DE CORRECCIÓN PRELIMINAR": "Se ha solicitado la corrección preliminar del documento.",
        "DOCUMENTO REVISADO": "El documento ha sido revisado por ingeniería.",
        "DOCUMENTO APROBADO": "El documento ha sido aprobado por calidad.",
        "SOLICITUD DE SUBIR VERSIÓN INTERNA": "Se ha solicitado subir el número de versión interna del documento.",
        "SOLICITUD DE REVISIÓN EN SUPERACIÓN DE VERSIÓN INTERNA": "Se ha creado la versión nueva del documento y se solicita la revisión de este para su  evaluación.",
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

            # **Evento 1: SOLICITUD DE REVISIÓN PRELIMINAR**
            if evento.tipo_evento == "SOLICITUD DE REVISIÓN PRELIMINAR":
                documento.version_actual = "A"
                documento.numero_version = 1

            # **Evento 2: SOLICITUD DE CORRECCIÓN PRELIMINAR**
            elif evento.tipo_evento == "SOLICITUD DE CORRECCIÓN PRELIMINAR":
                documento.estado_version = "CORRECCIÓN"
                documento.ruta_actual = request.POST.get("ruta_actual", documento.ruta_actual)

            # **Evento 3: DOCUMENTO REVISADO**
            elif evento.tipo_evento == "DOCUMENTO REVISADO":
                documento.revisado = True  # Se marca como revisado

            # **Evento 4: DOCUMENTO APROBADO**
            elif evento.tipo_evento == "DOCUMENTO APROBADO":
                documento.aprobado = True  # Se marca como aprobado

            # **Evento 5: SOLICITUD DE SUBIR VERSIÓN INTERNA**
            elif evento.tipo_evento == "SOLICITUD DE SUBIR VERSIÓN INTERNA":
                documento.revisado = False  # Reiniciar variable de revisado
                documento.aprobado = False  # Reiniciar variable de aprobado

            # **Evento 6: SOLICITUD DE REVISIÓN EN SUPERACIÓN DE VERSIÓN INTERNA**
            elif evento.tipo_evento == "SOLICITUD DE REVISIÓN EN SUPERACIÓN DE VERSIÓN INTERNA":
                documento.version_actual = "A"  # Mantiene la versión en "A"
                documento.numero_version = (documento.numero_version or 0) + 1  # Incrementa el número de versión

            documento.save()
            evento.save()

            # **Enviar correo si hay destinatarios**
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

            messages.success(request, "✅ Evento registrado con éxito y correo enviado.")
            return redirect("dashboard")

    else:
        form = EventoForm(initial={
            "estado_actual": documento.estado_actual,
            "etapa_actual": documento.etapa_actual,
            "version_actual": documento.version_actual,
            "numero_version": documento.numero_version,
            "estado_version": documento.estado_version,
            "ruta_actual": documento.ruta_actual,
            "descripcion": descripciones_eventos.get("SOLICITUD DE REVISIÓN PRELIMINAR", "Descripción no disponible"),
        })

    return render(request, "documentos/registrar_evento.html", {"form": form, "documento": documento, "usuario": request.user})
