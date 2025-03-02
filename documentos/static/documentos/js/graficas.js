document.addEventListener("DOMContentLoaded", function () {
    fetch("/dashboard/datos_graficas/")
        .then(response => response.json())
        .then(data => {
            console.log("Datos recibidos:", data);

            // Extraer datos para la primera gráfica
            const proyectos = data.subproyectos_por_proyecto.map(item => item.proyecto__nombre);
            const subproyectos = data.subproyectos_por_proyecto.map(item => item.total);

            // Encontrar el valor máximo y su índice
            const maxSubproyecto = Math.max(...subproyectos);
            const maxIndex1 = subproyectos.indexOf(maxSubproyecto);

            // Generar colores: gris claro para todas, azul #28348A para la más alta
            const colors1 = subproyectos.map((value, index) =>
                index === maxIndex1 ? 'rgb(40,52,138)' : 'rgba(200, 200, 200, 0.7)'
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
                        borderRadius: 10
                    }]
                },
                options: {
                    responsive: true,
                    plugins: {
                        legend: { display: false },
                        tooltip: {
                            enabled: true
                        },
                        datalabels: {
                            display: true,
                            color: 'black',
                            font: { weight: 'bold', size: 14 },
                            align: 'top',
                            formatter: (value, ctx) => {
                                return ctx.dataIndex === maxIndex1 ? value : ''; // Solo mostrar en la barra más alta
                            }
                        }
                    },
                    scales: {
                        x: {
                            grid: { display: false },
                            ticks: { color: 'black' }
                        },
                        y: {
                            grid: { display: false, color: '#ddd' },
                            ticks: { display: true, color: 'black' }
                        }
                    }
                }
            });

            // Extraer datos para la segunda gráfica
            const subproyectos2 = data.documentos_por_subproyecto.map(item => item.subproyecto__nombre);
            const documentos = data.documentos_por_subproyecto.map(item => item.total);

            // Encontrar el valor máximo y su índice
            const maxDocumentos = Math.max(...documentos);
            const maxIndex2 = documentos.indexOf(maxDocumentos);

            // Generar colores: gris claro para todas, azul #28348A para la más alta
            const colors2 = documentos.map((value, index) =>
                index === maxIndex2 ? 'rgb(40,52,138)' : 'rgba(200, 200, 200, 0.7)'
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
                        borderRadius: 10
                    }]
                },
                options: {
                    responsive: true,
                    plugins: {
                        legend: { display: false },
                        tooltip: {
                            enabled: true
                        },
                        datalabels: {
                            display: true,
                            color: 'white',
                            font: { weight: 'bold', size: 14 },
                            align: 'top',
                            formatter: (value, ctx) => {
                                return ctx.dataIndex === maxIndex2 ? value : ''; // Solo mostrar en la barra más alta
                            }
                        }
                    },
                    scales: {
                        x: {
                            grid: { display: false },
                            ticks: { color: 'black' }
                        },
                        y: {
                            grid: { display: false, color: '#ddd' },
                            ticks: { display: true, color: 'black' }
                        }
                    }
                }
            });
        })
        .catch(error => console.error("Error al obtener los datos:", error));
});
