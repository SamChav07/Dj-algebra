document.addEventListener('DOMContentLoaded', () => {
    const createTablesBtn = document.getElementById('createTablesBtn');
    const tablesContainerFila = document.getElementById('tablesContainerFila');
    const tablesContainerColumn = document.getElementById('tablesContainerColumn');
    const inputRowVector = document.getElementById('Mfc_Fila');
    const inputColVector = document.getElementById('Mfc_Column');
    const submitBtn = document.getElementById('resolveBtn');
    const resolverForm = document.getElementById('resolverForm');
    const resultText = document.getElementById('resultText');

    // Evento para crear tablas de vectores
    createTablesBtn.addEventListener('click', function() {
        const dimension = parseInt(document.getElementById('vectorDimension').value);
        
        // Limpiar los contenedores antes de crear nuevas tablas
        tablesContainerFila.innerHTML = '';  
        tablesContainerColumn.innerHTML = ''; 

        // Validar la entrada
        if (isNaN(dimension) || dimension <= 0) {
            alert('Por favor, ingresa una dimensión válida (mayor que 0).');
            return;
        }

        // Crear tabla horizontal (vector fila)
        const rowTable = document.createElement('table');
        rowTable.className = 'table table-bordered'; // Clases de Bootstrap para estilo

        // Crear encabezado
        const rowHeader = document.createElement('tr');
        const th = document.createElement('th');
        th.textContent = 'Vector 1'; // Encabezado de fila
        rowHeader.appendChild(th);
        rowTable.appendChild(rowHeader);

        // Crear fila con inputs
        const rowData = document.createElement('tr');
        for (let i = 0; i < dimension; i++) {
            const cell = document.createElement('td');
            const input = document.createElement('input');
            input.type = 'number';
            input.className = 'form-control';
            input.placeholder = `Valor ${i + 1}`; // Placeholder opcional
            input.setAttribute('data-row-index', i); // Añadir atributo para identificar los inputs
            cell.appendChild(input); // Añadir input a la celda
            rowData.appendChild(cell); // Añadir celda a la fila
        }
        rowTable.appendChild(rowData); // Añadir fila a la tabla
        tablesContainerFila.appendChild(rowTable); // Añadir tabla al contenedor

        // Crear tabla vertical (vector columna)
        const colTable = document.createElement('table');
        colTable.className = 'table table-bordered'; // Clases de Bootstrap para estilo
        const colHeader = document.createElement('tr');
        const thCol = document.createElement('th');
        thCol.textContent = 'Vector 2'; // Encabezado de columna
        colHeader.appendChild(thCol);
        colTable.appendChild(colHeader);

        // Crear filas con inputs
        for (let i = 0; i < dimension; i++) {
            const row = document.createElement('tr');
            const cell = document.createElement('td');
            const inputCol = document.createElement('input');
            inputCol.type = 'number';
            inputCol.className = 'form-control';
            inputCol.placeholder = `Valor ${i + 1}`; // Placeholder opcional
            inputCol.setAttribute('data-col-index', i); // Añadir atributo para identificar los inputs
            cell.appendChild(inputCol); // Añadir input a la celda
            row.appendChild(cell); // Añadir celda a la fila
            colTable.appendChild(row); // Añadir fila a la tabla
        }
        tablesContainerColumn.appendChild(colTable); // Añadir tabla al contenedor

        // Mostrar el botón "Resolver"
        submitBtn.classList.remove('d-none'); // Eliminar clase d-none para mostrar el botón
    });

    // Función para obtener los datos de los vectores
    const getVectorData = (dataIndex) => {
        return Array.from(document.querySelectorAll(`input[data-${dataIndex}]`))
            .map(input => parseFloat(input.value) || 0);
    };

    // Evento para el envío del formulario
    resolverForm.addEventListener('submit', async (event) => {
        event.preventDefault(); // Evitar la sumisión tradicional del formulario

        const rowVector = getVectorData('row-index'); // Datos de la fila
        const colVector = getVectorData('col-index'); // Datos de la columna

        if (!rowVector.length || !colVector.length) {
            alert('Por favor, completa ambos vectores antes de enviar.');
            return;
        }

        inputRowVector.value = JSON.stringify(rowVector);
        inputColVector.value = JSON.stringify(colVector);

        const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
        try {
            const response = await fetch(resolverForm.action, {
                method: 'POST',
                body: new FormData(resolverForm),
                headers: {
                    'X-Requested-With': 'XMLHttpRequest',
                    'X-CSRFToken': csrftoken
                }
            });

            const data = await response.json();
            if (data.status === 'success') {
                resultText.textContent = data.resultados.join(', ');
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
});