from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import LoginForm, EventoForm
from .models import Proyecto, Subproyecto, Documento, Evento
from django.http import JsonResponse



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
def registrar_evento(request, documento_id):
    """ Vista para registrar un evento en un documento """
    documento = get_object_or_404(Documento, id=documento_id)

    if request.method == "POST":
        form = EventoForm(request.POST)
        if form.is_valid():
            evento = form.save(commit=False)
            evento.documento = documento
            evento.usuario = request.user  # Usuario autenticado
            evento.estado_actual = documento.estado_actual
            evento.etapa_actual = documento.etapa_actual
            evento.version_actual = documento.version_actual
            evento.numero_version = documento.numero_version
            evento.estado_version = documento.estado_version
            evento.save()
            messages.success(request, "✅ Evento registrado con éxito.")
            return redirect("dashboard")  # Redirigir al dashboard
    else:
        # Prellenar el formulario con los datos del documento
        form = EventoForm(initial={
            "estado_actual": documento.estado_actual,
            "etapa_actual": documento.etapa_actual,
            "version_actual": documento.version_actual,
            "numero_version": documento.numero_version,
            "estado_version": documento.estado_version,
            "ruta_actual": documento.ruta_actual,  # Editable
        })

    return render(request, "documentos/registrar_evento.html", {"form": form, "documento": documento, "usuario": request.user})

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
            "tipo_evento": evento.tipo_evento,
            "fecha": evento.fecha_creacion_evento.strftime("%Y-%m-%d %H:%M"),
            "estado_actual": evento.estado_actual,
            "version_actual": evento.version_actual,
            "ruta_actual": evento.ruta_actual,


        }
        for evento in eventos
    ]

    return JsonResponse(data, safe=False)