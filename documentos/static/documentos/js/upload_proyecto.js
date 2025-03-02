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