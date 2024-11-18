document.addEventListener('DOMContentLoaded', function () {
    const createMatrixInputsBtn = document.getElementById('createMatrixInputs');
    const matrixInputsContainer = document.getElementById('matrixInputsContainer');
    const resolveBtn = document.getElementById('resolveBtn');
    const resolverForm = document.getElementById('resolverForm');

    // Evento para crear las entradas de la matriz
    createMatrixInputsBtn.addEventListener('click', function () {
        const tamMtrx = parseInt(document.getElementById('id_tamMtrx').value);

        if (isNaN(tamMtrx) || tamMtrx <= 0) {
            alert('Por favor, ingresa un tamaño válido para la matriz (mayor que 0).');
            return;
        }

        // Limpiar el contenedor previo
        matrixInputsContainer.innerHTML = '';

        // Crear las entradas de la matriz
        crearInputsDeMatriz(tamMtrx);

        // Mostrar el botón de "Guardar y Resolver"
        resolveBtn.style.display = 'block';
    });

    // Enviar datos al backend
    resolverForm.addEventListener('submit', async function (event) {
        event.preventDefault();

        try {
            const matriz = obtenerMatriz();

            if (matriz.length === 0) {
                alert('La matriz está vacía o no es válida.');
                return;
            }

            const datosAEnviar = {
                lu_mtrx: JSON.stringify(matriz)
            };

            console.log('Datos a Enviar:', datosAEnviar);

            const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;

            const response = await fetch(resolverForm.action, {
                method: 'POST',
                body: new URLSearchParams(datosAEnviar),
                headers: {
                    'X-Requested-With': 'XMLHttpRequest',
                    'X-CSRFToken': csrftoken
                }
            });

            const data = await response.json();

            if (data.status === 'success') {
                mostrarResultados(data.resultados);
            } else {
                let errorMessage = data.message;
                if (data.errors) {
                    errorMessage += '\nErrores específicos:\n' + data.errors.join('\n');
                }
                alert(errorMessage);
            }
        } catch (error) {
            console.error('Error:', error);
            alert('Ocurrió un error al enviar los datos.');
        }
    });

    // Función para crear inputs para la matriz
    function crearInputsDeMatriz(tamMtrx) {
        const table = document.createElement('table');
        table.className = 'table table-bordered';

        for (let i = 0; i < tamMtrx; i++) {
            const row = document.createElement('tr');

            for (let j = 0; j < tamMtrx + 1; j++) {
                const cell = document.createElement('td');
                const input = document.createElement('input');
                input.type = 'number';
                input.className = 'form-control';

                if (j < tamMtrx) {
                    input.placeholder = `(${i + 1}, ${j + 1})`;
                    input.name = `valor_${i + 1}_${j + 1}`;
                } else {
                    input.placeholder = `b${i + 1}`;
                    input.name = `b_${i + 1}`;
                }

                cell.appendChild(input);
                row.appendChild(cell);
            }

            table.appendChild(row);
        }

        matrixInputsContainer.appendChild(table);
    }

    // Obtener datos de la matriz desde los inputs
    function obtenerMatriz() {
        const tamMtrx = parseInt(document.getElementById('id_tamMtrx').value);
        const matriz = [];

        for (let i = 0; i < tamMtrx; i++) {
            const fila = [];
            for (let j = 0; j < tamMtrx; j++) {
                const input = document.querySelector(`input[name='valor_${i + 1}_${j + 1}']`);
                const valor = parseFloat(input.value);

                if (isNaN(valor)) {
                    alert(`El valor en la posición (${i + 1}, ${j + 1}) no es un número válido.`);
                    return [];
                }

                fila.push(valor);
            }

            const inputB = document.querySelector(`input[name='b_${i + 1}']`);
            const valorB = parseFloat(inputB.value);

            if (isNaN(valorB)) {
                alert(`El valor del término independiente b${i + 1} no es válido.`);
                return [];
            }

            fila.push(valorB);
            matriz.push(fila);
        }
        return matriz;
    }

    // Función para mostrar los resultados en la página
    function mostrarResultados(resultados) {
        // Mostrar los resultados directamente en las pestañas
        mostrarMatrizL(resultados.L);
        mostrarMatrizU(resultados.U);
        mostrarSolucion(resultados.solucion);
        mostrarPasosFactorizacion(resultados.pasos_factorizacion);
        mostrarPasosResolucion(resultados.pasos_resolucion);
    }

    // Funciones para mostrar cada resultado en las pestañas correspondientes
    function mostrarMatrizL(matrizL) {
        document.getElementById('resultTextL').innerHTML = `<h4>Matriz L:</h4>${formatearMatriz(matrizL)}`;
        activateTab('tabL');
    }

    function mostrarMatrizU(matrizU) {
        document.getElementById('resultTextU').innerHTML = `<h4>Matriz U:</h4>${formatearMatriz(matrizU)}`;
        activateTab('tabU');
    }

    function mostrarSolucion(solucion) {
        document.getElementById('resultTextSolucion').innerHTML = `<h4>Solución:</h4>${formatearVector(solucion)}`;
        activateTab('tabSolucion');
    }

    function mostrarPasosFactorizacion(pasos) {
        document.getElementById('resultTextPasosF').innerHTML = `<h4>Pasos de Factorización:</h4><pre>${pasos}</pre>`;
        activateTab('tabPasosF');
    }

    function mostrarPasosResolucion(pasos) {
        document.getElementById('resultTextPasosR').innerHTML = `<h4>Pasos de Resolución:</h4><pre>${pasos}</pre>`;
        activateTab('tabPasosR');
    }

    // Función para activar una pestaña específica
    function activateTab(tabId) {
        const tabElement = new bootstrap.Tab(document.querySelector(`a[href="#${tabId}"]`));
        tabElement.show();
    }

    // Función para formatear una matriz como tabla
    function formatearMatriz(matriz) {
        let html = '<table class="table table-bordered">';
        matriz.forEach(fila => {
            html += '<tr>';
            fila.forEach(valor => {
                html += `<td>${valor.toFixed(2)}</td>`;
            });
            html += '</tr>';
        });
        html += '</table>';
        return html;
    }

    // Función para formatear un vector como lista
    function formatearVector(vector) {
        return `<ul>${vector.map(valor => `<li>${valor.toFixed(2)}</li>`).join('')}</ul>`;
    }
});