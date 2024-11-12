document.addEventListener('DOMContentLoaded', () => {
    const createMatrixInputsBtn = document.getElementById('createMatrixInputs');
    const matrixInputsContainer = document.getElementById('matrixInputsContainer');
    const indepTermsContainer = document.getElementById('indepTermsContainer');
    const resolveBtn = document.getElementById('resolveBtn');
    const resolverForm = document.getElementById('resolverForm');

    createMatrixInputsBtn.addEventListener('click', () => {
        const size = parseInt(document.getElementById('id_tamMtrx').value);

        matrixInputsContainer.innerHTML = '';
        indepTermsContainer.innerHTML = '';

        // Crear la tabla para la matriz
        const matrixTable = document.createElement('table');
        matrixTable.className = 'table table-bordered'; // Clases de Bootstrap para el estilo

        // Crear la fila de encabezados para la matriz
        const matrixHeaderRow = document.createElement('tr');
        for (let i = 0; i < size; i++) {
            const th = document.createElement('th');
            th.textContent = `Columna ${i + 1}`; // Encabezado "Columna N"
            th.style.textAlign = 'center';  // Centrar el texto
            matrixHeaderRow.appendChild(th);
        }
        matrixTable.appendChild(matrixHeaderRow);

        // Crear las filas para los componentes de la matriz
        for (let i = 0; i < size; i++) {
            const row = document.createElement('tr');
            for (let j = 0; j < size; j++) {
                const cell = document.createElement('td');
                const input = document.createElement('input');
                input.type = 'number';
                input.className = 'form-control';
                input.placeholder = `(${i + 1}, ${j + 1})`; // Dentro de la celda, "Componente N"
                input.dataset.rowIndex = i;
                input.dataset.columnIndex = j;
                cell.appendChild(input);
                row.appendChild(cell);
            }
            matrixTable.appendChild(row);
        }

        matrixInputsContainer.appendChild(matrixTable);

        // Crear la tabla de términos independientes (sin fila de encabezado)
        const termsTable = document.createElement('table');
        termsTable.className = 'table table-bordered'; // Clases de Bootstrap para el estilo

        // Crear una sola fila para los términos independientes
        const termsRow = document.createElement('tr');
        for (let i = 0; i < size; i++) {
            const cell = document.createElement('td');
            const input = document.createElement('input');
            input.type = 'number';
            input.className = 'form-control';
            input.placeholder = `Término ${i + 1}`; // Dentro de la celda, "Término N"
            input.dataset.termIndex = i;
            cell.appendChild(input);
            termsRow.appendChild(cell);
        }
        termsTable.appendChild(termsRow);

        indepTermsContainer.appendChild(termsTable);

        resolveBtn.classList.remove('d-none'); // Mostrar el botón de "Resolver"
    });

    resolverForm.addEventListener('submit', async function (event) {
        event.preventDefault(); // Evitar el envío tradicional del formulario

        try {
            // Obtener la matriz
            const size = parseInt(document.getElementById('id_tamMtrx').value);
            const matrix = [];
            for (let i = 0; i < size; i++) {
                const row = [];
                for (let j = 0; j < size; j++) {
                    const input = document.querySelector(`input[data-row-index='${i}'][data-column-index='${j}']`);
                    const value = parseFloat(input.value) || 0;
                    row.push(value);
                }
                matrix.push(row);
            }

            // Obtener los términos independientes
            const terms = [];
            for (let i = 0; i < size; i++) {
                const input = document.querySelector(`input[data-term-index='${i}']`);
                const value = parseFloat(input.value) || 0;
                terms.push(value);
            }

            if (!matrix.length || !terms.length) {
                alert('Por favor, completa la matriz y los términos independientes antes de enviar.');
                return;
            }

            // Preparar los datos para enviar
            const datosAEnviar = {
                cramer_Matrx: JSON.stringify(matrix),
                cramer_TermsIndp: JSON.stringify(terms)
            };

            const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;

            // Enviar los datos al servidor usando Fetch
            const response = await fetch(resolverForm.action, {
                method: 'POST',
                body: JSON.stringify(datosAEnviar),
                headers: {
                    'Content-Type': 'application/json',
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
            } else {
                console.error('Error del servidor:', data.message);
                alert(`Error: ${data.message}`);
            }
        } catch (error) {
            console.error('Error:', error);
            alert('Ocurrió un error al enviar los datos.');
        }
    });
});
