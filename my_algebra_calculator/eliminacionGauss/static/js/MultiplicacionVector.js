document.getElementById('createTablesBtn').addEventListener('click', function() {
    const dimension = parseInt(document.getElementById('vectorDimension').value);
    const tablesContainer = document.getElementById('tablesContainer');
    const resolveButton = document.getElementById('resolveBtn');

    // Limpiar el contenedor antes de crear nuevas tablas
    tablesContainer.innerHTML = '';

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
    
    // Encabezado de columna
    const th = document.createElement('th');
    th.textContent = 'Vector 1';
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

        cell.appendChild(input); // Añadir input a la celda
        rowData.appendChild(cell); // Añadir celda a la fila
    }

    rowTable.appendChild(rowData); // Añadir fila a la tabla
    tablesContainer.appendChild(rowTable); // Añadir tabla al contenedor

    
   // Crear tabla vertical (vector columna)
    const colTable = document.createElement('table');
    colTable.className = 'table table-bordered'; // Clases de Bootstrap para estilo

   // Crear encabezado
    const colHeader = document.createElement('tr');

    const thCol = document.createElement('th');
    thCol.textContent = 'Vector 2'; // Encabezado de columna
    colHeader.appendChild(thCol);

    colTable.appendChild(colHeader);

   // Crear filas con inputs
    for (let i = 0; i < dimension; i++) {
        const row = document.createElement('tr');

       // No se añade encabezado para cada fila, solo se añade un campo de entrada
        const cell = document.createElement('td');

        const inputCol = document.createElement('input');
        inputCol.type = 'number';
        inputCol.className = 'form-control';
        inputCol.placeholder = `Valor ${i + 1}`; // Placeholder opcional

       cell.appendChild(inputCol); // Añadir input a la celda
       row.appendChild(cell); // Añadir celda a la fila

       colTable.appendChild(row); // Añadir fila a la tabla
    }

   tablesContainer.appendChild(colTable); // Añadir tabla al contenedor

   // Mostrar el botón "Resolver"
   resolveButton.classList.remove('d-none'); // Eliminar clase d-none para mostrar el botón
});
