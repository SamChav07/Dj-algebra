document.addEventListener('DOMContentLoaded', function () {
    const createMatrixBtn = document.getElementById('createMatrixBtn');
    const matrixContainer = document.getElementById('matrixContainer');
    const resolveBtn = document.getElementById('resolveBtn');
    const resolverForm = document.getElementById('resolverForm');

    createMatrixBtn.addEventListener('click', function () {
        const filas = parseInt(document.getElementById('id_filas').value);
        const columnas = parseInt(document.getElementById('id_columnas').value);

        // Clear previous matrix container
        matrixContainer.innerHTML = '';

        // Validate inputs and create matrix if valid
        if (validarEntradas(filas, columnas)) {
            crearMatriz(filas, columnas + 1); // Agregar 1 para la columna adicional
            resolveBtn.style.display = 'block'; // Show the "Resolve" button
        }
    });

    resolverForm.addEventListener('submit', async function (event) {
        event.preventDefault(); // Prevent traditional form submission

        try {
            const matriz = obtenerMatriz();
            const formData = new URLSearchParams({
                EG_matriz: JSON.stringify(matriz) // Convert matrix to JSON string
            });

            const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;

            // Send data to the server using Fetch API
            const response = await fetch(resolverForm.action, {
                method: 'POST',
                body: formData,
                headers: {
                    'X-Requested-With': 'XMLHttpRequest',
                    'X-CSRFToken': csrftoken
                }
            });

            const data = await response.json(); // Parse JSON response

            // Handle server response
            if (data.status === 'success') {
                alert('Datos guardados exitosamente');
                document.getElementById('resultText').textContent = data.resultados;
            } else {
                alert(data.message); // Show detailed error message
            }
        } catch (error) {
            console.error('Error:', error);
            alert('Ocurrió un error al enviar los datos.');
        }
    });

    function validarEntradas(filas, columnas) {
        if (isNaN(filas) || filas <= 0) {
            alert('Por favor, ingresa un número válido de ecuaciones (mayor que 0).');
            return false;
        }
        if (isNaN(columnas) || columnas <= 0) {
            alert('Por favor, ingresa un número válido de incógnitas (mayor que 0).');
            return false;
        }
        return true;
    }

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
                cell.appendChild(input);
                row.appendChild(cell);
            }
            table.appendChild(row);
        }
        matrixContainer.appendChild(table);
    }

    function obtenerMatriz() {
        const filas = parseInt(document.getElementById('id_filas').value);
        const columnas = parseInt(document.getElementById('id_columnas').value) + 1; // Incluye columna adicional
        const matriz = [];

        for (let i = 0; i < filas; i++) {
            const fila = [];
            for (let j = 0; j < columnas; j++) {
                const input = document.querySelector(`input[name='valor_${i + 1}_${j + 1}']`);
                fila.push(parseFloat(input.value) || 0);
            }
            matriz.push(fila);
        }
        return matriz;
    }
});