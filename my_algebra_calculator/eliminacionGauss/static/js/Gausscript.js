document.addEventListener('DOMContentLoaded', function () {
    const createMatrixBtn = document.getElementById('createMatrixBtn');
    const resolverForm = document.getElementById('resolverForm');
    const matrixContainer = document.getElementById('matrixContainer');
    const resolveBtn = document.getElementById('resolveBtn');

    createMatrixBtn.addEventListener('click', function () {
        const filas = parseInt(document.getElementById('id_filas').value);
        const columnas = parseInt(document.getElementById('id_columnas').value);

        // Limpiar el contenedor de la matriz previo
        matrixContainer.innerHTML = '';

        // Validar entradas
        if (!validarEntradas(filas, columnas)) return;

        // Crear y mostrar la matriz
        crearMatriz(filas, columnas);

        // Mostrar el botón "Resolver"
        resolveBtn.style.display = 'block';
    });

    resolverForm.addEventListener('submit', async function (event) {
        event.preventDefault();

        try {
            // Convertir los inputs de la matriz en un formato JSON
            const matriz = obtenerMatriz();

            // Llenar el campo oculto del textarea con la matriz en formato JSON
            document.querySelector('textarea[name="matriz"]').value = JSON.stringify(matriz);

            const formData = new FormData(this);
            const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;

            const response = await fetch(this.action, {
                method: 'POST',
                body: formData,
                headers: {
                    'X-Requested-With': 'XMLHttpRequest',
                    'X-CSRFToken': csrftoken
                }
            });

            const data = await response.json();

            if (data.status === 'success') {
                alert('Datos guardados exitosamente');
                document.getElementById('resultText').textContent = data.resultados; // Mostrar resultados
            } else {
                alert(data.message);
            }
        } catch (error) {
            console.error('Error:', error);
        }
    });

    // Función para validar las entradas
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

    // Función para crear la tabla de la matriz
    function crearMatriz(filas, columnas) {
        const table = document.createElement('table');
        table.className = 'table table-bordered'; // Clases de Bootstrap para estilo

        for (let i = 0; i < filas; i++) {
            const row = document.createElement('tr'); // Crear fila

            for (let j = 0; j < columnas; j++) {
                const cell = document.createElement('td'); // Crear celda
                const input = document.createElement('input'); // Crear input

                input.type = 'number';
                input.className = 'form-control'; // Estilo de Bootstrap
                input.placeholder = `(${i + 1}, ${j + 1})`; // Placeholder
                input.name = `valor_${i + 1}_${j + 1}`; // Nombre del input

                cell.appendChild(input); // Insertar input en la celda
                row.appendChild(cell); // Insertar celda en la fila
            }

            table.appendChild(row); // Insertar fila en la tabla
        }

        matrixContainer.appendChild(table); // Añadir la tabla al contenedor
    }

    // Función para obtener la matriz como un array bidimensional
    function obtenerMatriz() {
        const filas = parseInt(document.getElementById('id_filas').value);
        const columnas = parseInt(document.getElementById('id_columnas').value);
        const matriz = [];

        for (let i = 0; i < filas; i++) {
            const fila = [];
            for (let j = 0; j < columnas; j++) {
                const input = document.querySelector(`input[name="valor_${i + 1}_${j + 1}"]`);
                fila.push(parseFloat(input.value) || 0); // Agregar el valor o 0 si está vacío
            }
            matriz.push(fila);
        }

        return matriz;
    }
});
