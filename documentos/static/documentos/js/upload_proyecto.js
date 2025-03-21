function mostrarNombreArchivo() {
    var input = document.getElementById('archivo_excel');
    var fileName = document.getElementById('file-name');

    if (input.files.length > 0) {
        fileName.textContent = "📂 " + input.files[0].name;
        fileName.style.color = "#007bff"; // Cambia el color para resaltar
    } else {
        fileName.textContent = "Haz clic para seleccionar un archivo";
        fileName.style.color = "#6c757d"; // Color gris por defecto
    }
}

document.addEventListener("DOMContentLoaded", function() {
    const proyectoSelect = document.getElementById("proyecto");
    const subproyectoSelect = document.getElementById("subproyecto");

    // Al seleccionar un proyecto, obtener los subproyectos
    proyectoSelect.addEventListener("change", function() {
        const proyectoId = this.value;
        subproyectoSelect.innerHTML = '<option value="">Selecciona un subproyecto...</option>';
        subproyectoSelect.disabled = true;

        if (proyectoId) {
            console.log("Proyecto seleccionado ID:", proyectoId);  // Verifica si el ID llega correctamente
            fetch(`/api/subproyectos/${proyectoId}/`)
                .then(response => response.json())
                .then(data => {
                    console.log("Respuesta de la API:", data);  // Verifica si la API devuelve datos
                    if (data.error) {
                        alert("⚠️ No hay subproyectos disponibles para este proyecto.");
                    } else {
                        data.forEach(subproyecto => {
                            const option = document.createElement("option");
                            option.value = subproyecto.id;
                            option.textContent = subproyecto.nombre;
                            subproyectoSelect.appendChild(option);
                        });
                        subproyectoSelect.disabled = false;
                    }
                })
                .catch(error => {
                    console.error("Error al cargar los subproyectos:", error);
                    alert("❌ Hubo un error al cargar los subproyectos.");
                });
        }
    });
});

document.addEventListener("DOMContentLoaded", function() {
    const proyectoSelect = document.getElementById("proyecto_estado");
    const subproyectoSelect = document.getElementById("subproyecto_estado");
    const documentoSelect = document.getElementById("documento_estado");

    // Al seleccionar un proyecto, obtener los subproyectos
    proyectoSelect.addEventListener("change", function() {
        const proyectoId = this.value;
        subproyectoSelect.innerHTML = '<option value="">Selecciona un subproyecto...</option>';
        subproyectoSelect.disabled = true;
        documentoSelect.innerHTML = '<option value="">Selecciona un documento...</option>';
        documentoSelect.disabled = true;

        if (proyectoId) {
            console.log("Proyecto seleccionado ID:", proyectoId);  // <-- Verifica si el ID llega correctamente

            fetch(`/api/subproyectos/${proyectoId}/`)
                .then(response => response.json())
                .then(data => {
                    console.log("Respuesta de la API:", data);  // <-- Verifica si la API devuelve datos

                    if (data.error) {
                        alert("⚠️ No hay subproyectos disponibles.");
                    } else {
                        data.forEach(subproyecto => {
                            const option = document.createElement("option");
                            option.value = subproyecto.id;
                            option.textContent = subproyecto.nombre;
                            subproyectoSelect.appendChild(option);
                        });
                        subproyectoSelect.disabled = false;
                    }
                })
                .catch(error => {
                    console.error("Error al cargar los subproyectos:", error);
                    alert("❌ Error al cargar los subproyectos.");
                });
        }
    });

    // Al seleccionar un subproyecto, obtener los documentos
    subproyectoSelect.addEventListener("change", function() {
        const subproyectoId = this.value;
        documentoSelect.innerHTML = '<option value="">Selecciona un documento...</option>';
        documentoSelect.disabled = true;

        if (subproyectoId) {
            fetch(`/api/documentos/${subproyectoId}/`)
                .then(response => response.json())
                .then(data => {
                    console.log("Respuesta de la API de documentos:", data);

                    if (data.error) {
                        alert("⚠️ No hay documentos disponibles.");
                    } else {
                        data.forEach(documento => {
                            const option = document.createElement("option");
                            option.value = documento.id;
                            option.textContent = documento.nombre;
                            documentoSelect.appendChild(option);
                        });
                        documentoSelect.disabled = false;
                    }
                })
                .catch(error => {
                    console.error("Error al cargar los documentos:", error);
                    alert("❌ Error al cargar los documentos.");
                });
        }
    });
});

function scrollToSection(sectionId) {
    // Ocultar todas las secciones
    document.getElementById('upload_proyecto_section').classList.add('d-none');
    document.getElementById('upload_documento_section').classList.add('d-none');
    document.getElementById('modificar_estado_section').classList.add('d-none');

    // Mostrar la sección deseada
    let section = document.getElementById(sectionId);
    section.classList.remove('d-none');

    // Hacer scroll a la sección
    section.scrollIntoView({ behavior: "smooth", block: "start" });
}
document.addEventListener("DOMContentLoaded", function() {
    const proyectoSelect = document.getElementById("proyecto_gestion");
    const subproyectoSelect = document.getElementById("subproyecto_gestion");
    const documentoSelect = document.getElementById("documento_gestion");
    const codigoContainer = document.getElementById("codigo-container");
    const codigoInput = document.getElementById("codigo");
    const codigoClienteInput = document.getElementById("codigo_cliente");
    const mensaje = document.getElementById("mensaje");

    // Obtener subproyectos cuando se selecciona un proyecto
    proyectoSelect.addEventListener("change", function() {
        subproyectoSelect.innerHTML = "<option value=''>-- Seleccionar --</option>";
        documentoSelect.innerHTML = "<option value=''>-- Seleccionar --</option>";
        subproyectoSelect.disabled = true;
        documentoSelect.disabled = true;
        codigoContainer.style.display = "none";

        if (this.value) {
            fetch(`/api/subproyectos/${this.value}/`)
                .then(response => response.json())
                .then(data => {
                    data.forEach(subproyecto => {
                        const option = document.createElement("option");
                        option.value = subproyecto.id;
                        option.textContent = subproyecto.nombre;
                        subproyectoSelect.appendChild(option);
                    });
                    subproyectoSelect.disabled = false;
                });
        }
    });

    // Obtener documentos cuando se selecciona un subproyecto
    subproyectoSelect.addEventListener("change", function() {
        documentoSelect.innerHTML = "<option value=''>-- Seleccionar --</option>";
        documentoSelect.disabled = true;
        codigoContainer.style.display = "none";

        if (this.value) {
            fetch(`/api/documentos/${this.value}/`)
                .then(response => response.json())
                .then(data => {
                    data.forEach(documento => {
                        const option = document.createElement("option");
                        option.value = documento.id;
                        option.textContent = documento.nombre;
                        documentoSelect.appendChild(option);
                    });
                    documentoSelect.disabled = false;
                });
        }
    });

    // Mostrar inputs cuando se selecciona un documento
    documentoSelect.addEventListener("change", function() {
        if (this.value) {
            fetch(`/api/documentos/${subproyectoSelect.value}/`)
                .then(response => response.json())
                .then(data => {
                    const documento = data.find(doc => doc.id == documentoSelect.value);
                    if (documento) {
                        codigoInput.value = documento.codigo || "";
                        codigoClienteInput.value = documento.codigo_cliente || "";
                        codigoContainer.style.display = "block";
                    }
                });
        } else {
            codigoContainer.style.display = "none";
        }
    });

    // Enviar formulario con AJAX para actualizar el documento
    document.getElementById("gestionar-documento-form").addEventListener("submit", function(event) {
        event.preventDefault();

        const formData = new FormData(this);
        formData.append("documento_id", documentoSelect.value);

        fetch("{% url 'crear_codigo_documento' %}", {
            method: "POST",
            body: formData,
            headers: {
                "X-CSRFToken": document.querySelector("[name=csrfmiddlewaretoken]").value
            }
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                mensaje.textContent = data.message;
                mensaje.style.display = "block";
                setTimeout(() => mensaje.style.display = "none", 3000);
            }
        });
    });
});