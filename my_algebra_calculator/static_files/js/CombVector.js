document.addEventListener('DOMContentLoaded', () => {
    const createVectorTableBtn = document.getElementById('createVectorTableBtn');
    const vectorTableContainer = document.getElementById('vectorTableContainer');
    const scalarTableContainer = document.getElementById('scalarTableContainer');
    const inputVector = document.getElementById('OpV_vectores');
    const inputEscalar = document.getElementById('OpV_escalares');
    const submitAllBtn = document.getElementById('resolveBtn');
    const resolverForm = document.getElementById('resolverForm');
    const resultText = document.getElementById('resultText');

    createVectorTableBtn.addEventListener('click', () => {
        const numVectores = parseInt(document.getElementById('numVectores').value);
        const dimVectores = parseInt(document.getElementById('dimVectores').value);

        vectorTableContainer.innerHTML = '';
        scalarTableContainer.innerHTML = '';

        // Create the table for vectors
        const vectorTable = document.createElement('table');
        vectorTable.className = 'table table-bordered'; // Bootstrap classes for styling

        // Create header row for vectors
        const vectorHeaderRow = document.createElement('tr');
        for (let i = 0; i < numVectores; i++) {
            const th = document.createElement('th');
            th.textContent = `Vector ${i + 1}`; // Encabezado "Vector N"
            th.style.textAlign = 'center';  // Centrar el texto
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
                input.placeholder = `Componente ${i + 1}`; // Dentro de la celda, "Componente N"
                input.dataset.vectorIndex = j;
                input.dataset.componentIndex = i;
                cell.appendChild(input);
                row.appendChild(cell);
            }
            vectorTable.appendChild(row);
        }

        vectorTableContainer.appendChild(vectorTable);

        // Create the table for scalars (without header row)
        const scalarTable = document.createElement('table');
        scalarTable.className = 'table table-bordered'; // Bootstrap classes for styling

        // Create rows for scalar values
        const scalarRow = document.createElement('tr');
        for (let j = 0; j < numVectores; j++) {
            const cell = document.createElement('td');
            const input = document.createElement('input');
            input.type = 'number';
            input.className = 'form-control';
            input.placeholder = `Escalar ${j + 1}`; // Dentro de la celda, "Escalar N"
            input.dataset.escalarIndex = j;
            cell.appendChild(input);
            scalarRow.appendChild(cell);
        }
        scalarTable.appendChild(scalarRow);

        scalarTableContainer.appendChild(scalarTable);
        submitAllBtn.classList.remove('d-none');
    });

    submitAllBtn.addEventListener('click', (e) => {
        e.preventDefault();  // Prevent form from submitting normally
        const vectores = Array.from(document.querySelectorAll('input[data-vector-index]'))
            .reduce((acc, input) => {
                const vectorIndex = input.dataset.vectorIndex;
                acc[vectorIndex] = acc[vectorIndex] || [];
                acc[vectorIndex].push(parseFloat(input.value) || 0);
                return acc;
            }, []);

        const escalares = Array.from(document.querySelectorAll('input[data-escalar-index]'))
            .map(input => parseFloat(input.value) || 0);

        if (!vectores.length || !escalares.length) {
            alert('Por favor, completa los vectores y escalares antes de enviar.');
            return;
        }

        inputVector.value = JSON.stringify(vectores);
        inputEscalar.value = JSON.stringify(escalares);

        // Make AJAX request
        const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
        fetch(resolverForm.action, {
            method: 'POST',
            body: new FormData(resolverForm),
            headers: {
                'X-Requested-With': 'XMLHttpRequest',
                'X-CSRFToken': csrftoken
            }
        })
        .then(response => response.json())
        .then(data => {
            if (data.status === 'success') {
                resultText.textContent = data.resultados.join(', ');  // Update results in the HTML
            } else {
                let errorMessage = data.message;
                if (data.errors) {
                    errorMessage += '\nErrores específicos:\n' + data.errors.join('\n');
                }
                alert(errorMessage);
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('Ocurrió un error al enviar los datos.');
        });
    });

    resolverForm.addEventListener('submit', async (event) => {
        event.preventDefault();
        try {
            const idsResponse = await fetch('/get-existing-ids/');
            const idsData = await idsResponse.json();
            console.log('Existing IDs:', idsData.ids);

            const formData = new FormData(resolverForm);
            formData.append('OpV_vectores', inputVector.value);
            formData.append('OpV_escalares', inputEscalar.value);
            const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;

            const response = await fetch(resolverForm.action, {
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