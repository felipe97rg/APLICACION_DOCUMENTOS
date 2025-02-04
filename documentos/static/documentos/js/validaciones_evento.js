document.addEventListener("DOMContentLoaded", function () {
    console.log("✅ validaciones_evento.js cargado correctamente");

    var tipoEventoSelect = document.getElementById("id_tipo_evento");
    var eventoForm = document.getElementById("eventoForm");

    var estadoActual = window.estadoActual;
    var versionActual = window.versionActual;
    var estadoVersion = window.estadoVersion;
    var revisado = window.revisado === "true";
    var aprobado = window.aprobado === "true";
    var comentariosPendientes = window.comentariosPendientes === "true";
    var usuarioRol = window.usuarioRol;  // Rol del usuario
    var numeroVersion = parseInt(window.numeroVersion) || 0;

    var existeVersionPreliminar = window.existeVersionPreliminar === "true"; // Variable enviada desde Django

    function obtenerEventosRestringidos() {
        let restricciones = [];

        // 🚫 1. Si no existe la "Creación de Versión Preliminar", **bloqueamos todos los eventos**
        if (!existeVersionPreliminar) {
            restricciones = [
                "Creación de Versión Interna Superada",
                "Creación de Versión Interdisciplinaria",
                "Creación de Versión Interdisciplinaria Superada",
                "Creación de Versión Final",
                "Creación de Versión Final Superada",
                "Solicitud de Revisión",
                "Solicitud de Corrección",
                "Solicitud de Superación de Numero de Versión Interna",
                "Solicitud de Superación a Versión Interdisciplinaria",
                "Solicitud de Superación de Numero de Versión Interdisciplinaria",
                "Solicitud de Superación a Versión Final",
                "Solicitud de Superación de Numero de Versión Final",
                "Documento Revisado por Ingeniería",
                "Documento Aprobado por Calidad",
                "Actualización del documento",
                "Suspensión del documento",
                "Eliminación del documento"
            ];
        }

        return restricciones;
    }

    function filtrarEventos() {
        let restricciones = obtenerEventosRestringidos();

        for (let i = 0; i < tipoEventoSelect.options.length; i++) {
            let opcion = tipoEventoSelect.options[i];
            if (restricciones.includes(opcion.value)) {
                opcion.disabled = true;
                opcion.style.display = "none"; // Ocultar completamente en la interfaz
            } else {
                opcion.disabled = false;
                opcion.style.display = "block";
            }
        }
    }

    tipoEventoSelect.addEventListener("change", function () {
        let restricciones = obtenerEventosRestringidos();
        let eventoSeleccionado = tipoEventoSelect.value;

        if (restricciones.includes(eventoSeleccionado)) {
            alert("⚠️ No puedes seleccionar este evento antes de la 'Creación de Versión Preliminar'.");
            tipoEventoSelect.value = "";
        }
    });

    eventoForm.addEventListener("submit", function (event) {
        let eventoSeleccionado = tipoEventoSelect.value;
        let restricciones = obtenerEventosRestringidos();

        if (restricciones.includes(eventoSeleccionado)) {
            event.preventDefault();
            alert("❌ No puedes registrar este evento. Verifica las restricciones.");
        }
    });

    filtrarEventos();
});
