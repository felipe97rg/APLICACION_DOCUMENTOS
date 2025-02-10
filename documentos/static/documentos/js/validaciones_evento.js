document.addEventListener("DOMContentLoaded", function () {
    const selectEvento = document.getElementById("id_tipo_evento");

    // 📌 Diccionario de clasificación manual para cada tipo de evento
    const clasificacionEventos = {
        "Solicitud de Creación de Versión Preliminar": "solicitudes",
        "Solicitud de Revisión": "solicitudes",
        "Solicitud de Corrección por Ingeniería": "solicitudes",
        "Solicitud de Aprobación por Calidad y Coordinación": "solicitudes",
        "Solicitud de Corrección por Calidad": "solicitudes",
        "Solicitud de Corrección por Coordinación": "solicitudes",
        "Solicitud de Superación de Numero Versión": "solicitudes",
        "Solicitud de Creación de Versión Preliminar Superada": "solicitudes",
        "Solicitud de Creación de Versión Interdisciplinaria Superada": "solicitudes",
        "Solicitud de Creación de Versión Interdisciplinaria": "solicitudes",
        "Solicitud de Creación de Versión Final": "solicitudes",
        "Solicitud de Envió de Documento al Cliente": "solicitudes",
        "Solicitud de Cancelación de Envió de Documento al Cliente": "solicitudes",
        
        "Solicitud de Creación de Medición o Actividad": "mediciones",
        "Solicitud de Revisión de Medición o Actividad": "mediciones",
        "Creación de Informe de Medición o Actividad" : "mediciones",
        
        "Documento Aprobado por Ingeniería": "aprobaciones",
        "Documento Aprobado por Calidad": "aprobaciones"
    };

    function aplicarColores() {
        for (const option of selectEvento.options) {
            if (option.value === "") continue; // Evitar aplicar estilo a la opción de "Seleccionar"

            const categoria = clasificacionEventos[option.textContent] || "otras";

            // Eliminar clases previas
            option.classList.remove("opcion-solicitudes", "opcion-aprobaciones", "opcion-mediciones", "opcion-otras");

            // Asignar la clase según la categoría
            if (categoria === "solicitudes") {
                option.classList.add("opcion-solicitudes");
            } else if (categoria === "aprobaciones") {
                option.classList.add("opcion-aprobaciones");
            } else if (categoria === "mediciones") {
                option.classList.add("opcion-mediciones");
            } else {
                option.classList.add("opcion-otras");
            }
        }
    }

    // Aplicar los colores al cargar la página
    aplicarColores();

    // Si hay algún cambio en el select, vuelve a aplicar colores
    selectEvento.addEventListener("change", aplicarColores);
});
