document.addEventListener('DOMContentLoaded', function () {
    const createVectorTableBtn = document.getElementById('createVectorTableBtn');
    const vectorTableContainer = document.getElementById('vectorTableContainer');
    const scalarTableContainer = document.getElementById('scalarTableContainer');
    const resolveButton = document.getElementById('resolveBtn');
    const inputVector = document.getElementById('OpV_vectores');
    const inputEscalar = document.getElementById('OpV_escalares');
    const resolverForm = document.getElementById('resolverForm');

    // Event listener for creating the tables
    createVectorTableBtn.addEventListener('click', function () {
        const numVectores = parseInt(document.getElementById('numVectores').value);
        const dimVectores = parseInt(document.getElementById('dimVectores').value);

        // Clear previous tables
        vectorTableContainer.innerHTML = '';
        scalarTableContainer.innerHTML = '';

        // Validate inputs
        if (isNaN(numVectores) || numVectores <= 0) {
            alert('Por favor, ingresa un número válido de vectores (mayor que 0).');
            return;
        }

        if (isNaN(dimVectores) || dimVectores <= 0) {
            alert('Por favor, ingresa un número válido para la dimensión (mayor que 0).');
            return;
        }

        // Create the table for vectors
        const vectorTable = document.createElement('table');
        vectorTable.className = 'table table-bordered'; // Bootstrap classes for styling

        // Create header row for vectors
        const vectorHeaderRow = document.createElement('tr');
        for (let i = 0; i < numVectores; i++) {
            const th = document.createElement('th');
            th.textContent = `Vector ${i + 1}`;
            vectorHeaderRow.appendChild(th);
        }
        vectorTable.appendChild(vectorHeaderRow);

        // Create rows for vector components
        for (let i = 0; i < dimVectores; i++) {
            const row = document.createElement('tr');
            for (let j = 0; j < numVectores; j++) {
                const cell = document.createElement('td');
                const input = document.createElement('input');
                input.type = 'number';
                input.className = 'form-control';
                input.placeholder = `Componente ${i + 1}`;
                input.dataset.vectorIndex = j; 
                input.dataset.componentIndex = i; 
                cell.appendChild(input); 
                row.appendChild(cell);
            }
            vectorTable.appendChild(row);
        }

        vectorTableContainer.appendChild(vectorTable); 

        // Create the table for scalars
        const scalarTable = document.createElement('table');
        scalarTable.className = 'table table-bordered'; // Bootstrap classes for styling

        // Create header row for scalars
        const scalarHeaderRow = document.createElement('tr');
        for (let j = 0; j < numVectores; j++) {
            const th = document.createElement('th');
            th.textContent = `Escalar ${j + 1}`;
            scalarHeaderRow.appendChild(th);
        }
        scalarTable.appendChild(scalarHeaderRow);

        // Create scalar input row
        const rowEscalars = document.createElement('tr');
        for (let j = 0; j < numVectores; j++) {
            const cell = document.createElement('td');
            const input = document.createElement('input');
            input.type = 'number';
            input.className = 'form-control';
            input.placeholder = `Escalar ${j + 1}`;
            input.dataset.vectorIndex = j;
            input.dataset.isScalar = true;
            cell.appendChild(input);
            rowEscalars.appendChild(cell);
        }
        scalarTable.appendChild(rowEscalars);
        scalarTableContainer.appendChild(scalarTable);

        // Show the "Resolve" button after creating the tables
        resolveButton.classList.remove('d-none');

        // Handle the action of the "Resolve" button
        resolveButton.onclick = function () {
            const vectores = [];
            const escalares = [];

            // Get the components of the vectors
            for (let j = 0; j < numVectores; j++) {
                const components = [];
                for (let i = 0; i < dimVectores; i++) {
                    const input = document.querySelector(`input[data-vector-index="${j}"][data-component-index="${i}"]`);
                    components.push(parseFloat(input.value) || 0); // Use 0 if no value is present
                }
                vectores.push(components);
            }

            // Get the scalars
            for (let j = 0; j < numVectores; j++) {
                const inputScalar = document.querySelector(`input[data-vector-index="${j}"][data-is-scalar]`);
                escalares.push(parseFloat(inputScalar.value) || 0); // Use 0 if no value is present
            }

            // Convert to JSON and assign to form fields
            inputVector.value = JSON.stringify(vectores);
            inputEscalar.value = JSON.stringify(escalares);

            // Submit the form
            resolverForm.submit(); // Submit the form directly
        };
    });
});