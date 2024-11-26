{% load static %}

<!DOCTYPE html>
<html lang="en" data-bs-theme="dark">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>CalcX</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-QWTKZyjpPEjISv5WaRU9OFeRpok6YctnYmDr5pNlyT2bRjXh0JMhjY6hW+ALEwIH" crossorigin="anonymous"> 
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.10.5/font/bootstrap-icons.css">
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js" integrity="sha384-YvpcrYf0tY3lHB60NNkmXc5s9fDVZLESaAA55NDzOxhy9GkcIdslK1eN7N6jIeHz" crossorigin="anonymous"></script>
    <script src="//cdn.jsdelivr.net/npm/@popperjs/core@2.9.2/dist/umd/popper.min.js"></script>
    <script src="{% static "js/js_analisis/Biseccion.js" %}" defer></script>

    <script src="//cdnjs.cloudflare.com/ajax/libs/mathjax/3.2.0/es5/tex-mml-chtml.js"></script>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet">
    <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>

    <style>
        .result-container {
            background-color: #ffffff;
            padding: 20px;
            border-radius: 5px;
            height: 100%;
        }
        .matrix-container {
            margin-top: 20px;
        }
        .matrix {
            display: grid;
            gap: 5px;
            margin-top: 10px;
        }
        .cell {
            border: 1px solid #007bff;
            padding: 10px;
            text-align: center;
            background-color: #1f1f1f;
            color: #ffffff;
        }
        footer {
            margin-top: 40px;
        }

        #iterationInput {
            width: 200px;
        }

        /* Estilo para el cuadro de resultados */
        #resultBox {
            min-height: 100px;
            background-color: #f7f7f7;
            border: 1px solid #ccc;
            padding: 20px;
            border-radius: 5px;
            margin-bottom: 20px;
        }

        #coordinates {
            margin-top: 10px;
            font-size: 1.2rem;
        }

        .chart-container {
            position: relative;
            height: 400px;
            width: 100%;
        }        

        #chart {
            width: 100%;
            height: 400px;
        }        
    </style>
</head>
<body class="d-flex flex-column min-vh-100">
    
    <header class="text-center my-4">
        <nav class="navbar bg-body-tertiary d-flex justify-content-between">
            <div class="container-fluid d-flex align-items-center">
                <a class="navbar-brand" href="main.html">
                    <img src="{% static "assets/calcXlogo.svg" %}" alt="Logo de calcX" style="width: 100%; height: 100px;">
                </a>
                <form class="d-flex align-items-center">
                    <button class="btn btn-primary me-2" type="button" onclick="window.location.href='{% url "mainAlgebra_view" %}'">Inicio</button>
                    <button class="btn btn-primary me-2" type="button" onclick="window.location.href='aboUs.html'">About Us</button>                
                </form>
            </div>
        </nav>
    </header>

    <main class="container mt-4 flex-grow-1">
        <h1 class="text-center mb-4">Método de Bisección</h1>
    
        <div class="row">
            <div class="col-md-6">
                <form id="bisectionForm" method="post" action="{% url 'biSeccion_process' %}">
                    {% csrf_token %}
        
                    <!-- Entrada de la función -->
                    <div class="mb-3">
                        <label for="id_functionInput" class="form-label">Función f(x):</label>
                        <input type="text" id="id_functionInput" name="function" class="form-control" placeholder="Ingrese la función en términos de x (e.g., x**2 - 4)" required>
                    </div>
        
                    <!-- Vista renderizada de la función -->
                    <div id="renderedFunctionView" class="border p-3 bg-light text-center mb-3 position-relative" style="min-height: 100px;">
                        Aquí se renderizará la función ingresada.
                        <i class="bi bi-calculator position-absolute bottom-0 end-0 me-2" id="toggleButtons" style="cursor: pointer; color: blue; font-size: 24px;"></i>
                    </div>
    
                    <!-- Contenedor para los botones -->
                    <div id="functionButtons" class="d-none mt-2"></div>
        
                    <!-- Entrada de valores a, b y tolerancia -->
                    <div class="mb-3">
                        <label for="inputA" class="form-label">Valor de a:</label>
                        <input type="number" id="inputA" name="a" class="form-control" placeholder="Inicio del intervalo" required>
                    </div>
        
                    <div class="mb-3">
                        <label for="inputB" class="form-label">Valor de b:</label>
                        <input type="number" id="inputB" name="b" class="form-control" placeholder="Fin del intervalo" required>
                    </div>
        
                    <div class="mb-3">
                        <label for="inputTolerance" class="form-label">Tolerancia:</label>
                        <input type="number" id="inputTolerance" name="tolerance" class="form-control" placeholder="Ingrese la tolerancia" step="any" required>
                    </div>
        
                    <!-- Botón para calcular -->
                    <div class="text-center">
                        <button type="submit" class="btn btn-primary w-100">Calcular Raíz</button>
                    </div>
                </form>
            </div>
    
            <div class="col-md-6 d-flex justify-content-center align-items-start" style="background-color: #f8f9fa; height: 100%;">
                <div class="container">
                    <h2 class="mb-3">Gráfica de Función</h2>
                    <input type="text" id="functionInput" class="form-control mb-3" placeholder="Ingresa la función (e.g., x**3 + 2*x)">
        
                    <!-- Contenedor del gráfico -->
                    <div class="chart-container mt-4">
                        <div id="chart"></div>
                    </div>
                    <div id="coordinates" class="mt-3">Haz clic en el gráfico para ver las coordenadas.</div>
                </div>
            </div>

        </div>
    
        <div class="row mt-4">
            <div class="col-md-12">
                <!-- Cuadro de Resultados -->
                <div id="resultBox">
                    <h2 class="text-center">Resultados</h2>
        
                    <!-- Botones para mostrar resultados -->
                    <div id='resultText' style='margin-bottom: 20px;'></div>
        
                    <!-- Pestañas -->
                    <ul class="nav nav-tabs justify-content-center mb-3" id="resultTabs">
                        <li class="nav-item">
                            <a class="nav-link active" data-bs-toggle="tab" href="#tabS">Solución</a>
                        </li>
                        <li class="nav-item">
                            <a class="nav-link" data-bs-toggle="tab" href="#tabI">Iteraciones</a>
                        </li>
                    </ul>
        
                    <!-- Contenido de las Pestañas -->
                    <div class="tab-content mt-3">
                        <div id="tabS" class="tab-pane fade show active">
                            <!-- Aquí se mostrará la Solución -->
                            <pre id='resultTextS'>Aquí aparecerá la solución.</pre>
                        </div>
                        <div id="tabI" class="tab-pane fade">
                            <!-- Icono de lupa para desplegar la búsqueda de iteración -->
                            <div class="input-group mb-3">
                                <span class="input-group-text" id="searchIcon" style="cursor: pointer;">
                                    <i class="bi bi-search"></i>
                                </span>
                                <input type="number" id="iterationInput" class="form-control" placeholder="Ingresa el número de iteración" aria-label="Número de iteración" aria-describedby="searchIcon" style="display: none;" onchange="showSpecificIteration()">
                            </div>
            
                            <!-- Aquí se mostrarán las iteraciones -->
                            <pre id='resultTextIter'>Aquí aparecerán las iteraciones.</pre>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </main>    

    <!-- Footer -->
    <footer class='text-center py-4 bg-body-tertiary'>
        <p>&copy; 2024 My Algebra Calculator</p>
    </footer>
    <script>
        function plotGraph() {
            const functionInput = document.getElementById('functionInput').value;
            if (!functionInput) {
                Plotly.newPlot('chart', [], {});
                return;
            }
    
            const xValues = [];
            const yValues = [];
            const step = 0.1; // Incremento de x
            const range = 10; // Rango de -10 a 10
    
            for (let x = -range; x <= range; x += step) {
                xValues.push(x);
                try {
                    const y = eval(functionInput.replace(/x/g, `(${x})`).replace(/\^/g, "**"));
                    yValues.push(y);
                } catch (e) {
                    Plotly.newPlot('chart', [], {});
                    return;
                }
            }
    
            const data = [{
                x: xValues,
                y: yValues,
                type: 'scatter',
                mode: 'lines',
                line: { color: 'rgba(75, 192, 192, 1)', width: 2 },
                name: `y = ${functionInput}`
            }];
    
            const layout = {
                title: 'Gráfica de Función con Coordenadas',
                xaxis: {
                    title: 'x',
                    zeroline: true,
                    showgrid: true,
                    gridcolor: '#444',
                    tickfont: { color: '#ffffff' },
                },
                yaxis: {
                    title: 'y',
                    zeroline: true,
                    showgrid: true,
                    gridcolor: '#444',
                    tickfont: { color: '#ffffff' },
                },
                plot_bgcolor: '#1e1e1e',
                paper_bgcolor: '#2c2c2c',
                showlegend: true
            };
    
            Plotly.newPlot('chart', data, layout);
    
            document.getElementById('chart').on('plotly_click', function(data) {
                const point = data.points[0];
                const xValue = point.x.toFixed(2);
                const yValue = point.y.toFixed(2);
                document.getElementById('coordinates').innerText = `(${xValue}, ${yValue})`;
            });
        }
    
        document.getElementById('functionInput').addEventListener('input', plotGraph);
    </script>    

</body>
</html>

#858281 

#7a7877 
<p style="color:  #cbc7c7 ;">Aquí se renderizará la función ingresada.</p>