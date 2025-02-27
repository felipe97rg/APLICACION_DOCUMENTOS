document.addEventListener("DOMContentLoaded", function () {
    fetch("/dashboard/datos_graficas/")
        .then(response => response.json())
        .then(data => {
            console.log("Datos recibidos:", data);

            // Extraer datos para la primera gráfica
            const proyectos = data.subproyectos_por_proyecto.map(item => item.proyecto__nombre);
            const subproyectos = data.subproyectos_por_proyecto.map(item => item.total);

            // Encontrar el valor máximo
            const maxSubproyecto = Math.max(...subproyectos);

            // Generar colores: gris claro para todas, azul #28348A para la más alta
            const colors1 = subproyectos.map(value =>
                value === maxSubproyecto ? 'rgba(40, 52, 138, 0.9)' : 'rgba(200, 200, 200, 0.7)'
            );

            new Chart(document.getElementById('grafica1'), {
                type: 'bar',
                data: {
                    labels: proyectos,
                    datasets: [{
                        label: 'Cantidad de Subproyectos',
                        data: subproyectos,
                        backgroundColor: colors1,
                        borderColor: colors1.map(color => color.replace('0.9', '1')),
                        borderWidth: 1,
                        borderRadius: 10  // 🔹 Esquinas redondeadas
                    }]
                },
                options: {
                    responsive: true,
                    plugins: {
                        legend: { display: false }  // 🔹 Oculta la leyenda
                    },
                    scales: {
                        x: {
                            grid: { display: false },  // 🔹 Oculta líneas en eje X
                            ticks: { color: 'black' }
                        },
                        y: {
                            grid: { display: false },  // 🔹 Oculta líneas en eje Y
                            ticks: { display: false }  // 🔹 Oculta números en eje Y
                        }
                    }
                }
            });

            // Extraer datos para la segunda gráfica
            const subproyectos2 = data.documentos_por_subproyecto.map(item => item.subproyecto__nombre);
            const documentos = data.documentos_por_subproyecto.map(item => item.total);

            // Encontrar el valor máximo
            const maxDocumentos = Math.max(...documentos);

            // Generar colores: gris claro para todas, azul #28348A para la más alta
            const colors2 = documentos.map(value =>
                value === maxDocumentos ? 'rgba(40, 52, 138, 0.9)' : 'rgba(200, 200, 200, 0.7)'
            );

            new Chart(document.getElementById('grafica2'), {
                type: 'bar',
                data: {
                    labels: subproyectos2,
                    datasets: [{
                        label: 'Cantidad de Documentos',
                        data: documentos,
                        backgroundColor: colors2,
                        borderColor: colors2.map(color => color.replace('0.9', '1')),
                        borderWidth: 1,
                        borderRadius: 10  // 🔹 Esquinas redondeadas
                    }]
                },
                options: {
                    responsive: true,
                    plugins: {
                        legend: { display: false }  // 🔹 Oculta la leyenda
                    },
                    scales: {
                        x: {
                            grid: { display: false },  // 🔹 Oculta líneas en eje X
                            ticks: { color: 'black' }
                        },
                        y: {
                            grid: { display: false },  // 🔹 Oculta líneas en eje Y
                            ticks: { display: false }  // 🔹 Oculta números en eje Y
                        }
                    }
                }
            });
        })
        .catch(error => console.error("Error al obtener los datos:", error));
});
