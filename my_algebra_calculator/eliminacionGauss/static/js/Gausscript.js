document.addEventListener('DOMContentLoaded', function () {

    const createMatrixBtn = document.getElementById('createMatrixBtn');
    const resolverForm = document.getElementById('resolverForm');
    const matrixContainer = document.getElementById('matrixContainer');

    createMatrixBtn.addEventListener('click', function() {
        const ecuaciones = parseInt(document.getElementById('ecuaciones').value);
        const incognitas = parseInt(document.getElementById('incognitas').value);

        // Limpiar el contenedor de la matriz previo
        matrixContainer.innerHTML = '';

        // Validar entradas
        if (!validarEntradas(ecuaciones, incognitas)) return;

        // Establecer valores ocultos para filas y columnas
        document.getElementById('filasInput').value = ecuaciones;
        document.getElementById('columnasInput').value = incognitas;

        // Crear y mostrar la matriz
        crearMatriz(ecuaciones, incognitas);
        resolverForm.style.display = 'block'; // Mostrar formulario
    });

    resolverForm.addEventListener('submit', async function(event) {
        event.preventDefault();

        try {
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
                document.querySelector('.result-container p').innerText = data.resultados;
            } else {
                alert(data.message);
            }
        } catch (error) {
            console.error('Error:', error);
        }
    });

    // Función para validar las entradas
    function validarEntradas(ecuaciones, incognitas) {
        if (isNaN(ecuaciones) || ecuaciones <= 0) {
            alert('Por favor, ingresa un número válido de ecuaciones (mayor que 0).');
            return false;
        }
        if (isNaN(incognitas) || incognitas <= 0) {
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
});
