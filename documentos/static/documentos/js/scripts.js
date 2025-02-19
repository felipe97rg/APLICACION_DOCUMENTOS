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

$(document).ready(function() {
    $(".btn-close").click(function() {
        $(this).closest(".alert").fadeOut(300, function() {
            $(this).remove();
        });
    });
});


$(document).ready(function() {
    // Ocultar automáticamente las alertas después de 5 segundos
    setTimeout(function() {
        $(".alert").fadeOut(500, function() {
            $(this).remove();
        });
    }, 5000);
});

$(document).ready(function () {
    $("#toggleUploadForm").click(function (e) {
        e.preventDefault();
        $("#uploadFormContainer").toggle();
    });
});


document.addEventListener("DOMContentLoaded", function () {
    console.log("El script de mostrar formulario está cargado.");

    const toggleButton = document.getElementById("toggleUploadForm");
    const uploadForm = document.getElementById("uploadFormContainer");

    if (toggleButton && uploadForm) {
        toggleButton.addEventListener("click", function (event) {
            event.preventDefault();
            if (uploadForm.style.display === "none" || uploadForm.style.display === "") {
                uploadForm.style.display = "block";
            } else {
                uploadForm.style.display = "none";
            }
        });
    } else {
        console.log("Error: No se encontraron los elementos necesarios.");
    }
});

$(document).ready(function() {
    $("#documento").change(function() {
        var documento_id = $(this).val();
        if (documento_id) {
            $("#evento-link").removeClass("d-none").attr("href", "/documento/" + documento_id + "/evento/");
            
            // Obtener los detalles del documento y restricciones de eventos
            $.get("/api/documento/" + documento_id + "/detalle/", function(data) {
                $("#estado_actual").text(data.estado_actual || "N/A");
                $("#etapa_actual").text(data.etapa_actual || "N/A");
                $("#version_actual").text(data.version_actual || "N/A");
                $("#numero_version").text(data.numero_version || "N/A");
                $("#estado_version").text(data.estado_version || "N/A");
                $("#ruta_actual").text(data.ruta_actual || "N/A");
                $("#revisado").text(data.revisado ? "Sí" : "No");
                $("#aprobado").text(data.aprobado ? "Sí" : "No");

                // Filtrar eventos en el select
                var eventosRestringidos = data.eventos_restringidos || [];
                $("#id_tipo_evento option").each(function() {
                    var evento = $(this).val();
                    if (eventosRestringidos.includes(evento)) {
                        $(this).prop("disabled", true).css("color", "gray"); // Deshabilitar opción
                    } else {
                        $(this).prop("disabled", false).css("color", "black");
                    }
                });

                // Guardar restricciones en el select para futura validación
                $("#id_tipo_evento").data("eventos-restringidos", eventosRestringidos);

                $("#documento-detalle").removeClass("d-none");
            });
        } else {
            $("#documento-detalle").addClass("d-none");
            $("#evento-link").addClass("d-none");
        }
    });
});
