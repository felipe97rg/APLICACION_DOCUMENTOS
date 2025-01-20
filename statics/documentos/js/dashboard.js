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

                        var tarjeta = `
                            <div class="timeline-item ${lado}">
                                <div class="timeline-content">
                                    <h5>${evento.tipo_evento}</h5>
                                    <p><strong>Usuario:</strong> ${evento.usuario}</p>
                                    <p><strong>Fecha:</strong> ${evento.fecha}</p>
                                    <p><strong>Estado:</strong> ${evento.estado_actual}</p>
                                    <p><strong>Versión:</strong> ${evento.version_actual}</p>
                                    <a href="${evento.ruta_actual}" target="_blank">📄 Ver Documento</a>
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
