document.getElementById('createVectorTableBtn').addEventListener('click', function() {
    const numVectores = parseInt(document.getElementById('numVectores').value);
    const dimVectores = parseInt(document.getElementById('dimVectores').value);
    const vectorTableContainer = document.getElementById('vectorTableContainer');
    const resolveButton = document.getElementById('resolveBtn');

    // Limpiar el contenedor antes de crear una nueva tabla
    vectorTableContainer.innerHTML = '';

    // Validar las entradas
    if (isNaN(numVectores) || numVectores <= 0) {
        alert('Por favor, ingresa un número válido de vectores (mayor que 0).');
        return;
    }

    if (isNaN(dimVectores) || dimVectores <= 0) {
        alert('Por favor, ingresa un número válido para la dimensión (mayor que 0).');
        return;
    }

    // Crear la tabla
    const table = document.createElement('table');
    table.className = 'table table-bordered'; // Clases de Bootstrap para estilo

    // Crear encabezado
    const headerRow = document.createElement('tr');
    
    // Encabezado de columnas
    for (let i = 0; i < numVectores; i++) {
        const th = document.createElement('th');
        th.textContent = `Vector ${i + 1}`;
        headerRow.appendChild(th);
    }
    
    table.appendChild(headerRow);

    // Crear filas para componentes
    for (let i = 0; i <= dimVectores; i++) { // Añadir fila extra para "Escalar"
        const row = document.createElement('tr');

        for (let j = 0; j < numVectores; j++) {
            const cell = document.createElement('td');

            if (i === dimVectores) { // Última fila para "Escalar"
                const input = document.createElement('input');
                input.type = 'number';
                input.className = 'form-control';
                input.placeholder = `Escalar ${j + 1}`; // Placeholder opcional
                cell.appendChild(input); // Añadir input a la celda
            } else {
                const input = document.createElement('input');
                input.type = 'number';
                input.className = 'form-control';
                input.placeholder = `Componente ${i + 1}`;
                cell.appendChild(input); // Añadir input a la celda
            }

            row.appendChild(cell); // Añadir celda a la fila
        }

        table.appendChild(row); // Añadir fila a la tabla
    }

    vectorTableContainer.appendChild(table); // Añadir tabla al contenedor

    // Mostrar el botón "Resolver"
    resolveButton.classList.remove('d-none'); // Eliminar clase d-none para mostrar el botón
});
