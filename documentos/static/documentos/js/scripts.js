$(document).ready(function () {
    // ✅ Manejo de la selección de proyectos
    $("#proyecto").change(function () {
        var proyecto_id = $(this).val();
        if (proyecto_id) {
            $.get(`/api/subproyectos/${proyecto_id}/`, function (data) {
                actualizarSelect("#subproyecto", data, "Selecciona un subproyecto");
                $("#subproyecto").prop("disabled", false);
            });
        } else {
            resetSelects();
        }
    });

    // ✅ Manejo de la selección de subproyectos
    $("#subproyecto").change(function () {
        var subproyecto_id = $(this).val();
        if (subproyecto_id) {
            $.get(`/api/documentos/${subproyecto_id}/`, function (data) {
                actualizarSelect("#documento", data, "Selecciona un documento");
                $("#documento").prop("disabled", false);
            });
        } else {
            resetDocumento();
        }
    });

    // ✅ Manejo de la selección de documentos
    $("#documento").change(function () {
        var documento_id = $(this).val();
        if (documento_id) {
            $("#evento-link").removeClass("d-none").attr("href", `/documento/${documento_id}/evento/`);

            // Obtener detalles y eventos del documento en paralelo
            $.when(
                $.get(`/api/documento/${documento_id}/detalle/`),
                $.get(`/api/documento/${documento_id}/eventos/`)
            ).done(function (detalleRes, eventosRes) {
                actualizarDetallesDocumento(detalleRes[0]);
                actualizarHistorialEventos(eventosRes[0]);
                actualizarBarraProgreso();
            });
        } else {
            resetDocumento();
        }
    });

    // ✅ Función para actualizar un select con nuevos datos
    function actualizarSelect(selector, data, placeholder) {
        $(selector).empty().append(`<option value="">${placeholder}</option>`);
        $.each(data, function (index, item) {
            $(selector).append(new Option(item.nombre, item.id));
        });
    }

    // ✅ Función para resetear los selects cuando no hay selección
    function resetSelects() {
        $("#subproyecto").empty().append('<option value="">Selecciona un subproyecto</option>').prop("disabled", true);
        resetDocumento();
    }

    // ✅ Función para resetear el documento cuando no hay selección
    function resetDocumento() {
        $("#documento").empty().append('<option value="">Selecciona un documento</option>').prop("disabled", true);
        $("#evento-link").addClass("d-none");
        $("#documento-detalle, #eventos-documento").addClass("d-none");
    }

    // ✅ Función para actualizar los detalles del documento
    function actualizarDetallesDocumento(data) {
        $("#nombre").text(data.nombre || "N/A");
        $("#codigo").text(data.codigo || "N/A");
        $("#estado_actual").text(data.estado_actual || "N/A");
        $("#etapa_actual").text(data.etapa_actual || "N/A");
        $("#version_actual").text(data.version_actual || "N/A");
        $("#numero_version").text(data.numero_version || "N/A");
        $("#ruta_actual").text(data.ruta_actual || "N/A");
        $("#revisado").text(data.revisado ? "Sí" : "No");
        $("#aprobado").text(data.aprobado ? "Sí" : "No");

        $("#documento-detalle").removeClass("d-none");
    }

    // ✅ Función para actualizar la línea de tiempo de eventos
    function actualizarHistorialEventos(eventos) {
        var timelineContainer = $("#timeline-container");
        timelineContainer.empty();

        if (eventos.length === 0) {
            timelineContainer.append('<p class="text-center">No hay eventos registrados.</p>');
        } else {
            eventos.sort((a, b) => new Date(b.fecha) - new Date(a.fecha)); // Ordenar de más reciente a más antiguo

            $.each(eventos, function (index, evento) {
                var lado = index % 2 === 0 ? "left" : "right";
                var destinatario1 = evento.usuario_interesado_1 || "No asignado";
                var destinatario2 = evento.usuario_interesado_2 || "No asignado";
                var destinatario3 = evento.usuario_interesado_3 || "No asignado";

                var tarjeta = `
                    <div class="timeline-item ${lado}">
                        <div class="timeline-content">
                            <h5>${evento.tipo_evento}</h5>
                            <p><strong>Fecha:</strong> ${evento.fecha}</p>
                            <p><strong>Remitente:</strong> ${evento.usuario}</p>
                            <p><strong>Destinatario 1:</strong> ${destinatario1}</p>
                            <p><strong>Destinatario 2:</strong> ${destinatario2}</p>
                            <p><strong>Destinatario 3:</strong> ${destinatario3}</p>
                            <p><strong>Estado:</strong> ${evento.estado_actual}</p>
                            <p><strong>Versión:</strong> ${evento.version_actual}</p>
                            <p><strong>Número de Versión:</strong> ${evento.numero_version || "No disponible"}</p>
                            <p><strong>Descripción:</strong> ${evento.descripcion}</p>
                            <p><strong>Comentarios:</strong> ${evento.comentarios || "Sin comentarios"}</p>
                            <p><strong>Ruta del Documento:</strong> ${evento.ruta_actual}</p>
                        </div>
                    </div>
                `;
                timelineContainer.append(tarjeta);
            });
        }

        $("#eventos-documento").removeClass("d-none");
    }

    // ✅ Función para actualizar la barra de progreso de etapas
    function actualizarBarraProgreso() {
        let etapaProgreso = $("#progreso-etapas");
        let etapaActual = $("#etapa_actual").text().trim().toUpperCase();
        let etapas = {
            "PRELIMINAR": "etapa-preliminar",
            "INTERDISCIPLINARIA": "etapa-interdisciplinaria",
            "FINAL": "etapa-final"
        };

        etapaProgreso.addClass("d-none"); // Ocultar por defecto

        if (etapaActual in etapas) {
            $(".etapa-box").removeClass("active");
            $("#" + etapas[etapaActual]).addClass("active");
            etapaProgreso.removeClass("d-none");
        }
    }
    
    // ✅ Cerrar alertas automáticamente
    setTimeout(function () {
        $(".alert").fadeOut(500, function () {
            $(this).remove();
        });
    }, 5000);
});
