from django.core.exceptions import PermissionDenied
from documentos.models import PerfilUsuario

EVENTOS_RESTRINGIDOS = {
    "Actualización del documento",
    "Suspensión del documento",
    "Eliminación del documento",
    "Reactivación del documento",
    "Solicitud de Creación de Medición o Actividad"
}

def restringir_eventos(view_func):
    """
    Decorador para restringir ciertos eventos a administradores y editores.
    """
    def wrapper(request, *args, **kwargs):
        # Obtener el usuario y su perfil
        usuario = request.user
        perfil = PerfilUsuario.objects.get(user=usuario)

        # Si el usuario no es admin ni editor y está intentando hacer un evento restringido, bloquearlo
        if request.method == "POST":
            tipo_evento = request.POST.get("tipo_evento")
            if tipo_evento in EVENTOS_RESTRINGIDOS and perfil.rol not in ["ADMIN", "EDITOR"]:
                raise PermissionDenied("⚠️ No tienes permisos para realizar este evento.")

        return view_func(request, *args, **kwargs)
    return wrapper
