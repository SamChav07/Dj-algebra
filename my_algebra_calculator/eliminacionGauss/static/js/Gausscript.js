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
        event.preventDefault(); // Evitar el envío tradicional del formulario

        try {
            // Obtener los datos de las entradas de filas y columnas
            const filas = parseInt(document.getElementById('id_filas').value);
            const columnas = parseInt(document.getElementById('id_columnas').value);

            // Convertir los inputs de la matriz en un formato JSON
            const matriz = obtenerMatriz();

            // Obtener el ID de la tabla desde el formulario
            const egTablaId = document.querySelector('input[name="eg_table_id"]').value; // Referenciar el input oculto

            // Crear un objeto con todos los datos a enviar
            const datosAEnviar = {
                EG_tabla_id: egTablaId,
                ecuaciones: filas,
                incognitas: columnas,
                EG_matriz: JSON.stringify(matriz), // Convertir la matriz a string JSON
            };

            const formData = new URLSearchParams(datosAEnviar); // Formatear los datos para enviar

            const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value; // Obtener el token CSRF

            // Enviar los datos al servidor usando Fetch API
            const response = await fetch(resolverForm.action, { // Usar la acción del formulario
                method: 'POST',
                body: formData,
                headers: {
                    'X-Requested-With': 'XMLHttpRequest', // Indicar que es una petición AJAX
                    'X-CSRFToken': csrftoken // Incluir el token CSRF para seguridad
                }
            });

            const data = await response.json(); // Parsear la respuesta JSON

            // Manejar la respuesta del servidor
            if (data.status === 'success') {
                alert('Datos guardados exitosamente');
                document.getElementById('resultText').textContent = data.resultados; // Mostrar resultados
            } else {
                alert(data.message); // Mostrar mensaje de error
            }
        } catch (error) {
            console.error('Error:', error);
            alert('Ocurrió un error al enviar los datos.');
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