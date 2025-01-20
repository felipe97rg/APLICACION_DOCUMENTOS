from django.urls import path
from .views import login_view, logout_view, dashboard_view, get_subproyectos, get_documentos, registrar_evento, dashboard_view, get_documento_detalle

urlpatterns = [
    path("login/", login_view, name="login"),
    path("logout/", logout_view, name="logout"),
    path("dashboard/", dashboard_view, name="dashboard"),
    path("api/subproyectos/<int:proyecto_id>/", get_subproyectos, name="get_subproyectos"),
    path("api/documentos/<int:subproyecto_id>/", get_documentos, name="get_documentos"), 
    path("documento/<int:documento_id>/evento/", registrar_evento, name="registrar_evento"),
    path("api/documento/<int:documento_id>/detalle/", get_documento_detalle, name="get_documento_detalle"),
]
