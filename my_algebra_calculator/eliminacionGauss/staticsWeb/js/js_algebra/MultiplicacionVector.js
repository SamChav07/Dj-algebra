document.addEventListener('DOMContentLoaded', function () {
    const createTablesBtn = document.getElementById('createTablesBtn');
    const resolveBtn = document.getElementById('resolveBtn');
    const resolverForm = document.getElementById('resolverForm');
    const tablesContainerFila = document.getElementById('tablesContainerFila');
    const tablesContainerColumn = document.getElementById('tablesContainerColumn');

    // Listener para crear las tablas de entrada
    createTablesBtn.addEventListener('click', function () {
        const vectorDimension = parseInt(document.getElementById('vectorDimension').value);

        // Limpiar tablas anteriores
        tablesContainerFila.innerHTML = '';
        tablesContainerColumn.innerHTML = '';

        // Validar la dimensión del vector
        if (isNaN(vectorDimension) || vectorDimension <= 0) {
            alert('Por favor, ingresa una dimensión válida para el vector.');
            return;
        }

        // Crear las tablas de entrada para fila y columna
        createVectorTable(tablesContainerFila, 'Fila', vectorDimension);
        createVectorTable(tablesContainerColumn, 'Column', vectorDimension);

        // Mostrar botón "Guardar y Resolver"
        resolveBtn.classList.remove('d-none');
    });

    // Función para crear una tabla de entrada para el vector
    function createVectorTable(container, type, dimension) {
        const table = document.createElement('table');
        table.className = 'table table-bordered';

        const row = document.createElement('tr');
        for (let i = 0; i < dimension; i++) {
            const cell = document.createElement('td');
            const input = document.createElement('input');
            input.type = 'number';
            input.className = 'form-control';
            input.placeholder = `(${type} ${i + 1})`;
            input.name = `${type.toLowerCase()}_${i + 1}`;
            cell.appendChild(input);
            row.appendChild(cell);
        }
        table.appendChild(row);
        container.appendChild(table);
    }

    // Event listener for form submission
    resolverForm.addEventListener('submit', async function (event) {
        event.preventDefault(); // Prevent traditional form submission

        try {
            const vectorFila = getVectorValues('Fila');
            const vectorColumna = getVectorValues('Column');

            // Validate that the vectors are the same size
            if (vectorFila.length !== vectorColumna.length) {
                alert('Los vectores de fila y columna deben tener la misma dimensión.');
                return;
            }

            // Prepare data to send to the server
            const datosAEnviar = {
                rowVector: JSON.stringify(vectorFila),
                colVector: JSON.stringify(vectorColumna)
            };

            // Get CSRF token
            const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;

            // Send data to the server using Fetch
            const response = await fetch(resolverForm.action, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': csrftoken,
                    'Content-Type': 'application/x-www-form-urlencoded',
                    'X-Requested-With': 'XMLHttpRequest'
                },
                body: new URLSearchParams(datosAEnviar)
            });

            const data = await response.json(); // Parse JSON response

            // Handle server response
            if (data.status === 'success') {
                alert('Multiplicación de vectores realizada exitosamente.');

                // Display results in the result container
                const resultText = document.getElementById('resultText');
                resultText.innerHTML = `
                    ${data.resultados.replace(/\n/g, '<br>')}
                `; // Show formatted results

            } else {
                let errorMessage = data.message;
                if (data.errors) {
                    errorMessage += '\nErrores específicos:\n' + data.errors.join('\n');
                }
                alert(errorMessage); // Show detailed error message
            }
        } catch (error) {
            console.error('Error al enviar los datos:', error);
            alert('Ocurrió un error al procesar la solicitud.');
        }
    });

    // Función para obtener valores del vector de entrada
    function getVectorValues(type) {
        const inputs = document.querySelectorAll(`input[name^="${type.toLowerCase()}_"]`);
        const values = [];
        for (const input of inputs) {
            const value = parseFloat(input.value);
            if (isNaN(value)) {
                alert(`Por favor, ingresa un valor numérico válido en el vector de ${type}.`);
                return [];
            }
            values.push(value);
        }
        return values;
    }
});