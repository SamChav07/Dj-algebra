document.addEventListener('DOMContentLoaded', function () {
    const createMatrixBtn = document.getElementById('createMatrixBtn');
    const matrixContainer = document.getElementById('matrixContainer');
    const resolveBtn = document.getElementById('resolveBtn');
    const resolverForm = document.getElementById('resolverForm');

    // Crear la matriz cuando se hace clic en "Crear Matriz"
    createMatrixBtn.addEventListener('click', function () {
        const filas = parseInt(document.getElementById('id_filas').value);
        const columnas = parseInt(document.getElementById('id_columnas').value);

        // Limpiar la matriz anterior, si existe
        matrixContainer.innerHTML = '';

        // Validar entradas
        if (!validarEntradas(filas, columnas)) return;

        // Crear y mostrar la matriz en el DOM
        crearMatriz(filas, columnas);

        // Mostrar el botón "Resolver"
        resolveBtn.style.display = 'block';
    });

    // Manejar el envío del formulario
    resolverForm.addEventListener('submit', async function (event) {
        event.preventDefault(); // Prevenir el envío tradicional del formulario

        try {
            // Obtener la matriz en formato de array bidimensional
            const matriz = obtenerMatriz();

            if (matriz.length === 0) return; // Si la matriz está vacía debido a un error de validación.

            // Preparar los datos para enviar al backend
            const datosAEnviar = {
                trMx_Matriz: JSON.stringify(matriz), // Convertir matriz a JSON
            };

            const formData = new URLSearchParams(datosAEnviar); // Formatear datos para enviar
            const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value; // Obtener token CSRF

            // Enviar los datos al servidor
            const response = await fetch(resolverForm.action, {
                method: 'POST',
                body: formData,
                headers: {
                    'X-Requested-With': 'XMLHttpRequest',
                    'X-CSRFToken': csrftoken
                }
            });

            const data = await response.json(); // Parsear la respuesta JSON
            console.log(data); // Log the response to check its structure

            // Manejar la respuesta del servidor
            if (data.status === 'success') {
                alert('Transposición completada exitosamente');
                console.log('Resultados:', data.resultados); // Log the resultados

                // Check if resultados is an array
                if (Array.isArray(data.resultados)) {
                    mostrarResultados(data.resultados); // Call a function to display the results in a table
                } else {
                    console.error('El resultado no es un array:', data.resultados);
                    alert('El resultado no es válido.');
                }
            } else {
                alert(data.message || 'Ocurrió un error en el servidor.');
            }
        } catch (error) {
            console.error('Error:', error);
            alert('Ocurrió un error al enviar los datos.');
        }
    });

    // Validar las entradas de filas y columnas
    function validarEntradas(filas, columnas) {
        if (isNaN(filas) || filas <= 0) {
            alert('Por favor, ingresa un número válido de filas (mayor que 0).');
            return false;
        }
        if (isNaN(columnas) || columnas <= 0) {
            alert('Por favor, ingresa un número válido de columnas (mayor que 0).');
            return false;
        }
        return true;
    }

    // Crear una tabla de matriz en el contenedor
    function crearMatriz(filas, columnas) {
        const table = document.createElement('table');
        table.className = 'table table-bordered';

        for (let i = 0; i < filas; i++) {
            const row = document.createElement('tr');

            for (let j = 0; j < columnas; j++) {
                const cell = document.createElement('td');
                const input = document.createElement('input');

                input.type = 'number';
                input.className = 'form-control';
                input.placeholder = `(${i + 1}, ${j + 1})`;
                input.name = `valor_${i + 1}_${j + 1}`;
                input.required = true; // Ensure input is required

                cell.appendChild(input);
                row.appendChild(cell);
            }

            table.appendChild(row);
        }

        matrixContainer.appendChild(table);
    }

    // Obtener la matriz como array bidimensional
    function obtenerMatriz() {
        const filas = parseInt(document.getElementById('id_filas').value);
        const columnas = parseInt(document.getElementById('id_columnas').value);
        const matriz = [];

        for (let i = 0; i < filas; i++) {
            const fila = [];
            for (let j = 0; j < columnas; j++) {
                const input = document.querySelector(`input[name='valor_${i + 1}_${j + 1}']`);
                const valor = parseFloat(input.value);
                if (isNaN(valor)) {
                    alert(`El valor en la posición (${i + 1}, ${j + 1}) no es un número válido.`);
                    return [];  // Retornar un array vacío para indicar error
                }
                fila.push(valor);
            }
            matriz.push(fila);
        }

        return matriz;
    }

    // Function to display the results in a card
    function mostrarResultados(resultados) {
        const resultTextElement = document.getElementById('resultText');
        resultTextElement.innerHTML = ''; // Clear previous results

        // Create a Bootstrap card
        const card = document.createElement('div');
        card.className = 'card mt-4';
        
        const cardHeader = document.createElement('div');
        cardHeader.className = 'card-header';
        cardHeader.textContent = 'Resultados de la Transposición';

        const cardBody = document.createElement('div');
        cardBody.className = 'card-body';

        if (resultados.length > 0) {
            const table = document.createElement('table');
            table.className = 'table table-bordered table-striped table-hover'; // Added Bootstrap classes for styling

            resultados.forEach(row => {
                const tr = document.createElement('tr');
                row.forEach(value => {
                    const td = document.createElement('td');
                    td.textContent = value; // Insert the value
                    tr.appendChild(td);
                });
                table.appendChild(tr);
            });

            cardBody.appendChild(table); // Append the table to the card body
        } else {
            cardBody.textContent = 'No hay resultados para mostrar.';
        }

        card.appendChild(cardHeader);
        card.appendChild(cardBody);
        resultTextElement.appendChild(card); // Append the card to the resultText
    }
});