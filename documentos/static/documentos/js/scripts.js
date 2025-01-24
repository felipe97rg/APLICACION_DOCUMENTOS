$(document).ready(function() {
    $("#proyecto").change(function() {
        var proyecto_id = $(this).val();
        if (proyecto_id) {
            $.get("/api/subproyectos/" + proyecto_id + "/", function(data) {
                $("#subproyecto").empty().append('<option value="">Selecciona un subproyecto</option>');
                $.each(data, function(index, item) {
                    $("#subproyecto").append(new Option(item.nombre, item.id));
                });
                $("#subproyecto").prop("disabled", false);
            });
        } else {
            $("#subproyecto").empty().append('<option value="">Selecciona un subproyecto</option>').prop("disabled", true);
            $("#documento").empty().append('<option value="">Selecciona un documento</option>').prop("disabled", true);
            $("#documento-detalle").addClass("d-none");
            $("#evento-link").addClass("d-none");
        }
    });

    $("#subproyecto").change(function() {
        var subproyecto_id = $(this).val();
        if (subproyecto_id) {
            $.get("/api/documentos/" + subproyecto_id + "/", function(data) {
                $("#documento").empty().append('<option value="">Selecciona un documento</option>');
                $.each(data, function(index, item) {
                    $("#documento").append(new Option(item.nombre, item.id));
                });
                $("#documento").prop("disabled", false);
            });
        } else {
            $("#documento").empty().append('<option value="">Selecciona un documento</option>').prop("disabled", true);
            $("#documento-detalle").addClass("d-none");
            $("#evento-link").addClass("d-none");
        }
    });

    $("#documento").change(function() {
        var documento_id = $(this).val();
        if (documento_id) {
            $("#evento-link").removeClass("d-none").attr("href", "/documento/" + documento_id + "/evento/");
            
            // Obtener los detalles del documento seleccionado
            $.get("/api/documento/" + documento_id + "/detalle/", function(data) {
                $("#estado_actual").text(data.estado_actual || "N/A");
                $("#etapa_actual").text(data.etapa_actual || "N/A");
                $("#version_actual").text(data.version_actual || "N/A");
                $("#numero_version").text(data.numero_version || "N/A");
                $("#estado_version").text(data.estado_version || "N/A");
                $("#ruta_actual").text(data.ruta_actual|| "N/A");
                $("#revisado").text(data.revisado ? "Sí" : "No");
                $("#aprobado").text(data.aprobado ? "Sí" : "No");
                
                $("#documento-detalle").removeClass("d-none");
            });
        } else {
            $("#documento-detalle").addClass("d-none");
            $("#evento-link").addClass("d-none");
        }
    });
});

$(document).ready(function() {
    $("#documento").change(function() {
        var documento_id = $(this).val();
        if (documento_id) {
            $("#evento-link").removeClass("d-none").attr("href", "/documento/" + documento_id + "/evento/");
            
            // Obtener los eventos del documento
            $.get("/api/documento/" + documento_id + "/eventos/", function(eventos) {
                var timelineContainer = $("#timeline-container");
                timelineContainer.empty();

                if (eventos.length === 0) {
                    timelineContainer.append('<p class="text-center">No hay eventos registrados.</p>');
                } else {
                    $.each(eventos, function(index, evento) {
                        var lado = index % 2 === 0 ? "left" : "right"; // Alterna eventos a la izquierda y derecha

                        // Manejar destinatarios vacíos
                        var destinatario1 = evento.usuario_interesado_1 ? evento.usuario_interesado_1 : "No asignado";
                        var destinatario2 = evento.usuario_interesado_2 ? evento.usuario_interesado_2 : "No asignado";
                        var destinatario3 = evento.usuario_interesado_3 ? evento.usuario_interesado_3 : "No asignado";

                        var tarjeta = `
                            <div class="timeline-item ${lado}">
                                <div class="timeline-content">
                                    <h5>${evento.tipo_evento}</h5>
                                    <p><strong>Fecha:</strong> ${evento.fecha}</p>
                                    <p><strong>Remitente:</strong> ${evento.usuario}</p>
                                    <p><strong>Destinatario 1:</strong> ${evento.usuario_interesado_1}</p>
                                    <p><strong>Destinatario 2:</strong> ${evento.usuario_interesado_2}</p>
                                    <p><strong>Destinatario 3:</strong> ${evento.usuario_interesado_3}</p>
                                    <p><strong>Estado:</strong> ${evento.estado_actual}</p>
                                    <p><strong>Versión:</strong> ${evento.version_actual}</p>
                                    <p><strong>Número de Versión:</strong> ${evento.numero_version || "No disponible"}</p>
                                    <p><strong>Estado de la Versión:</strong> ${evento.estado_version || "No disponible"}</p>
                                    <p><strong>Descripción:</strong> ${evento.descripcion}</p>
                                    <p><strong>Comentarios:</strong> ${evento.comentarios ? evento.comentarios : "Sin comentarios"}</p>
                                    <p><strong>Ruta del Documento:</strong> ${evento.ruta_actual}</p>
                                </div>
                            </div>
                        `;

                        timelineContainer.append(tarjeta);
                    });
                }
                
                $("#eventos-documento").removeClass("d-none");
            });
        } else {
            $("#eventos-documento").addClass("d-none");
            $("#evento-link").addClass("d-none");
        }
    });
});