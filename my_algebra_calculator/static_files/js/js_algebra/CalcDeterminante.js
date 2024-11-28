document.addEventListener('DOMContentLoaded', function () {
    const createMatrixInputsBtn = document.getElementById('createMatrixInputs');
    const matrixInputsContainer = document.getElementById('matrixInputsContainer');
    const resolveBtn = document.getElementById('resolveBtn');
    const resolverForm = document.getElementById('resolverForm');
    const resultText = document.getElementById('resultText'); // Contenedor de resultados

    // Event listener para crear las entradas de la matriz
    createMatrixInputsBtn.addEventListener('click', function () {
        const size = parseInt(document.getElementById('id_tamMtrx').value);

        // Validar el tamaño ingresado
        if (!validarTamaño(size)) return;

        // Crear entradas para la matriz
        crearEntradasMatriz(size);

        // Mostrar el botón de "Resolver"
        resolveBtn.style.display = 'block';
    });

    // Event listener para enviar el formulario
    resolverForm.addEventListener('submit', async function (event) {
        event.preventDefault();

        try {
            // Obtener matriz
            const matriz = obtenerMatriz();
            if (matriz.length === 0) return;

            // Preparar datos para enviar
            const datosAEnviar = {
                cldt_Matrx: JSON.stringify(matriz) // Convertir matriz a JSON
            };

            const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;

            // Enviar datos al servidor usando Fetch
            const response = await fetch(resolverForm.action, {
                method: 'POST',
                body: new URLSearchParams(datosAEnviar),
                headers: {
                    'X-Requested-With': 'XMLHttpRequest',
                    'X-CSRFToken': csrftoken
                }
            });

            const data = await response.json();

            // Manejar la respuesta del servidor
            if (data.status === 'success') {
                alert('Cálculo exitoso.');
                console.log('Resultado:', data.resultado);
                console.log('Pasos:', data.pasos);

                // Mostrar los resultados en el contenedor
                resultText.innerHTML = `
                    <strong>Determinante:</strong> ${data.resultado.toFixed(2)}<br>
                    <strong>Pasos:</strong><br><pre>${data.pasos}</pre>
                `;
            } else {
                alert(`Error: ${data.message}`);
                resultText.innerHTML = `Error: ${data.message}`;
            }
        } catch (error) {
            console.error('Error:', error);
            alert('Ocurrió un error al enviar los datos.');
            resultText.innerHTML = 'Ocurrió un error al procesar la solicitud.';
        }
    });

    // Validar tamaño de la matriz
    function validarTamaño(size) {
        if (isNaN(size) || size <= 0) {
            alert('Por favor, ingresa un tamaño válido de matriz (mayor que 0).');
            return false;
        }
        return true;
    }

    // Crear entradas para una matriz cuadrada
    function crearEntradasMatriz(size) {
        matrixInputsContainer.innerHTML = ''; // Limpiar contenedor previo

        const matrixDiv = document.createElement('div');
        matrixDiv.className = 'mb-4';

        const title = document.createElement('h5');
        title.textContent = `Matriz de tamaño ${size} x ${size}`;
        matrixDiv.appendChild(title);

        const table = document.createElement('table');
        table.className = 'table table-bordered';

        for (let i = 0; i < size; i++) {
            const row = document.createElement('tr');

            for (let j = 0; j < size; j++) {
                const cell = document.createElement('td');
                const input = document.createElement('input');

                input.type = 'number';
                input.className = 'form-control';
                input.name = `matrix_${i}_${j}`;
                input.placeholder = `(${i + 1}, ${j + 1})`;

                cell.appendChild(input);
                row.appendChild(cell);
            }
            table.appendChild(row);
        }
        matrixDiv.appendChild(table);
        matrixInputsContainer.appendChild(matrixDiv);
    }

    // Obtener la matriz como un arreglo bidimensional
    function obtenerMatriz() {
        const size = parseInt(document.getElementById('id_tamMtrx').value);
        const matriz = [];

        for (let i = 0; i < size; i++) {
            const row = [];
            for (let j = 0; j < size; j++) {
                const input = document.querySelector(`input[name='matrix_${i}_${j}']`);
                const value = parseFloat(input.value);

                if (isNaN(value)) {
                    alert(`El valor en la posición (${i + 1}, ${j + 1}) no es válido.`);
                    return []; // Retornar matriz vacía para indicar error
                }
                row.push(value);
            }
            matriz.push(row);
        }
        return matriz;
    }
});
