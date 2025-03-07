document.addEventListener("DOMContentLoaded", function () {
    fetch("/reporte/datos_graficas/")
        .then(response => response.json())
        .then(data => {
            console.log("Datos recibidos:", data);

            // Función para generar colores consistentes
            function generarColores(dataArray) {
                const maxValor = Math.max(...dataArray);
                return dataArray.map(value =>
                    value === maxValor ? 'rgb(0, 123, 255)' : 'rgba(200, 200, 200, 0.7)'
                );
            }

            // Configuración de ejes sin líneas de fondo
            const opcionesGrafica = {
                responsive: true,
                plugins: { legend: { display: false } },
                scales: {
                    x: {
                        ticks: { color: 'black' },
                        grid: { display: false }  // Elimina líneas de fondo
                    },
                    y: {
                        ticks: { color: 'black' },
                        grid: { display: false }  // Elimina líneas de fondo
                    }
                }
            };

            // ====== Gráfica 1: Subproyectos por Proyecto ======
            const proyectos = data.subproyectos_por_proyecto.map(item => item.proyecto__nombre);
            const subproyectos = data.subproyectos_por_proyecto.map(item => item.total);
            const colors1 = generarColores(subproyectos);

            new Chart(document.getElementById('grafica1'), {
                type: 'bar',
                data: {
                    labels: proyectos,
                    datasets: [{
                        label: 'Cantidad de Subproyectos',
                        data: subproyectos,
                        backgroundColor: colors1,
                        borderColor: colors1,
                        borderWidth: 1,
                        borderRadius: 10
                    }]
                },
                options: opcionesGrafica
            });

            // ====== Gráfica 2: Documentos por Subproyecto ======
            const subproyectos2 = data.documentos_por_subproyecto.map(item => item.subproyecto__nombre);
            const documentos = data.documentos_por_subproyecto.map(item => item.total);
            const colors2 = generarColores(documentos);

            new Chart(document.getElementById('grafica2'), {
                type: 'bar',
                data: {
                    labels: subproyectos2,
                    datasets: [{
                        label: 'Cantidad de Documentos',
                        data: documentos,
                        backgroundColor: colors2,
                        borderColor: colors2,
                        borderWidth: 1,
                        borderRadius: 10
                    }]
                },
                options: opcionesGrafica
            });

            // ====== Gráfica 3: Documentos por Etapa ======
            if (data.documentos_por_etapa.length > 0) {
                const etapas = data.documentos_por_etapa.map(item => item.etapa_actual);
                const cantidadPorEtapa = data.documentos_por_etapa.map(item => item.total);
                const colors3 = generarColores(cantidadPorEtapa);

                new Chart(document.getElementById('grafica3'), {
                    type: 'bar',
                    data: {
                        labels: etapas,
                        datasets: [{
                            label: 'Cantidad de Documentos',
                            data: cantidadPorEtapa,
                            backgroundColor: colors3,
                            borderColor: colors3,
                            borderWidth: 1,
                            borderRadius: 10
                        }]
                    },
                    options: {
                        ...opcionesGrafica,  // Se mantiene la configuración original
                        indexAxis: 'y',  // Asegura que la gráfica sea horizontal
                        scales: {
                            y: {
                                ...opcionesGrafica.scales.x,  // Mantiene la configuración del eje X
                            },
                            x: {
                                ...opcionesGrafica.scales.y,  // Mantiene la configuración del eje Y
                            }
                        }
                    }
                });
            } else {
                console.warn("No hay datos disponibles para la gráfica de documentos por etapa.");
            }
        })
        .catch(error => console.error("Error al obtener los datos:", error));
});


document.addEventListener("DOMContentLoaded", function () {
    fetch("/reporte/datos_graficas/")
        .then(response => response.json())
        .then(data => {
            console.log("Datos recibidos:", data);

            // Función para formatear fechas (YYYY-MM-DD)
            function formatearFecha(fecha) {
                return new Date(fecha).toLocaleDateString("es-ES", {
                    year: "numeric", month: "2-digit", day: "2-digit"
                });
            }

            // 📌 Nueva Gráfica: Eventos registrados por día
            if (data.eventos_por_dia.length > 0) {
                const fechas = data.eventos_por_dia.map(item => formatearFecha(item.fecha));
                const eventosPorDia = data.eventos_por_dia.map(item => item.total);

                new Chart(document.getElementById('grafica4'), {
                    type: 'line',
                    data: {
                        labels: fechas,
                        datasets: [{
                            label: 'Eventos Registrados',
                            data: eventosPorDia,
                            borderColor: 'rgb(0, 123, 255)',
                            backgroundColor: 'rgba(0, 123, 255, 0.3)',
                            borderWidth: 2,
                            fill: true,
                            tension: 0.3,  // Suaviza la línea
                            pointRadius: 5,
                            pointBackgroundColor: 'rgb(0, 123, 255)',
                        }]
                    },
                    options: {
                        responsive: true,
                        plugins: { legend: { display: true } },
                        scales: {
                            x: {
                                ticks: { color: 'black' },
                                grid: { display: false }
                            },
                            y: {
                                ticks: { color: 'black' },
                                grid: { display: false }
                            }
                        }
                    }
                });
            } else {
                console.warn("No hay datos disponibles para la gráfica de eventos por día.");
            }
        })
        .catch(error => console.error("Error al obtener los datos:", error));
});

document.addEventListener("DOMContentLoaded", function () {
    fetch("/reporte/datos_graficas/")
        .then(response => response.json())
        .then(data => {
            console.log("Datos recibidos:", data);

            // 📌 Función para generar colores con la barra más alta en azul
            function generarColores(dataArray) {
                const maxValor = Math.max(...dataArray);
                return dataArray.map(value =>
                    parseFloat(value) === maxValor ? 'rgb(0, 123, 255)' : 'rgba(200, 200, 200, 0.7)'
                );
            }

            // 📌 Configuración de ejes sin líneas de fondo
            const opcionesGrafica = {
                responsive: true,
                plugins: { legend: { display: false } },
                scales: {
                    x: {
                        ticks: { color: 'black' },
                        grid: { display: false }  // Elimina líneas de fondo
                    },
                    y: {
                        ticks: { color: 'black' },
                        grid: { display: false },  // Elimina líneas de fondo
                        min: 0,
                        max: 100, // 📌 Asegura que el eje Y vaya de 0 a 100%
                        ticks: {
                            callback: function(value) {
                                return value + "%"; // 📌 Formato en porcentaje
                            }
                        }
                    }
                }
            };

            // 📌 Nueva Gráfica: Porcentaje de avance por subproyecto
            if (data.avance_por_subproyecto.length > 0) {
                const subproyectos = data.avance_por_subproyecto.map(item => item.subproyecto__nombre);
                const porcentajeAvance = data.avance_por_subproyecto.map(item => parseFloat(item.porcentaje_avance.toFixed(2)));

                // Generar colores con la barra más alta en azul
                const colorsAvance = generarColores(porcentajeAvance);

                new Chart(document.getElementById('grafica5'), {
                    type: 'bar',
                    data: {
                        labels: subproyectos,
                        datasets: [{
                            label: 'Porcentaje de Avance',
                            data: porcentajeAvance,
                            backgroundColor: colorsAvance,
                            borderColor: colorsAvance,
                            borderWidth: 1,
                            borderRadius: 10
                        }]
                    },
                    options: opcionesGrafica
                });
            } else {
                console.warn("No hay datos disponibles para la gráfica de avance por subproyecto.");
            }
        })
        .catch(error => console.error("Error al obtener los datos:", error));
});
