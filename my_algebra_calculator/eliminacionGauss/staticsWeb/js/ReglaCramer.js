document.addEventListener('DOMContentLoaded', function () {
    const createMatrixInputs = document.getElementById('createMatrixInputs');
    const matrixInputsContainer = document.getElementById('matrixInputsContainer');
    const resolveBtn = document.getElementById('resolveBtn');
    const resolverForm = document.getElementById('resolverForm');

    // Event listener for creating the matrix inputs
    createMatrixInputs.addEventListener('click', function () {
        const tamMtrx = parseInt(document.getElementById('id_tamMtrx').value);
        
        // Validate input
        if (isNaN(tamMtrx) || tamMtrx <= 0) {
            alert('Por favor, ingresa un tamaño válido para la matriz (mayor que 0).');
            return;
        }

        // Clear previous matrix inputs
        matrixInputsContainer.innerHTML = '';

        // Create and display the inputs for the matrix and independent terms
        crearEntradasMatriz(tamMtrx);

        // Show the "Resolve" button
        resolveBtn.style.display = 'block';
    });

    // Event listener for form submission
    resolverForm.addEventListener('submit', async function (event) {
        event.preventDefault(); // Prevent traditional form submission

        try {
            // Convert matrix and independent terms inputs to JSON format
            const matriz = obtenerMatriz();
            const termsIndp = obtenerTerminosIndependientes();

            // Log the matrix and terms being sent for debugging
            console.log('Matriz:', matriz);
            console.log('Términos Independientes:', termsIndp);

            // Prepare data to send
            const datosAEnviar = {
                cramer_Matrx: matriz,  // Send the matrix as a list of lists
                cramer_TermsIndp: termsIndp // Send the independent terms as a list
            };

            // Check if the matrix is valid
            if (matriz.length === 0 || termsIndp.length === 0) {
                alert('La matriz o los términos independientes no son válidos.');
                return; // Exit the function if the matrix or terms are invalid
            }

            const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value; // Get CSRF token

            // Send data to the server using Fetch API
            const response = await fetch(resolverForm.action, {
                method: 'POST',
                body: JSON.stringify(datosAEnviar), // Send the data as JSON string
                headers: {
                    'Content-Type': 'application/json', // Ensure content type is JSON
                    'X-Requested-With': 'XMLHttpRequest',
                    'X-CSRFToken': csrftoken
                }
            });

            const data = await response.json(); // Parse JSON response

            // Handle server response
            if (data.status === 'success') {
                alert('Cálculo realizado exitosamente');
                document.getElementById('resultText').textContent = JSON.stringify(data.resultados, null, 2); // Display results
            } else {
                let errorMessage = data.message;
                if (data.errors) {
                    errorMessage += '\nErrores específicos:\n' + data.errors.join('\n');
                }
                alert(errorMessage); // Show detailed error message
            }
        } catch (error) {
            console.error('Error:', error);
            alert('Ocurrió un error al enviar los datos.');
        }
    });

    // Function to create inputs for the matrix and independent terms
    function crearEntradasMatriz(tamMtrx) {
        const table = document.createElement('table');
        table.className = 'table table-bordered';

        // Create matrix rows and columns
        for (let i = 0; i < tamMtrx; i++) {
            const row = document.createElement('tr');

            for (let j = 0; j < tamMtrx + 1; j++) { // Matrix columns + 1 for the results column
                const cell = document.createElement('td');
                const input = document.createElement('input');

                input.type = 'number';
                input.className = 'form-control';
                if (j < tamMtrx) {
                    // For matrix values (first n columns)
                    input.placeholder = `(${i + 1}, ${j + 1})`;
                    input.name = `valor_${i + 1}_${j + 1}`;
                } else {
                    // For result values (last column)
                    input.placeholder = `Resultado ${i + 1}`;
                    input.name = `result_${i + 1}`;
                }

                cell.appendChild(input);
                row.appendChild(cell);
            }

            table.appendChild(row);
        }

        matrixInputsContainer.appendChild(table);
    }

    // Function to obtain the matrix as a two-dimensional array
    function obtenerMatriz() {
        const tamMtrx = parseInt(document.getElementById('id_tamMtrx').value);
        const matriz = [];

        for (let i = 0; i < tamMtrx; i++) {
            const fila = [];
            for (let j = 0; j < tamMtrx; j++) { // Only matrix coefficients (not the independent terms)
                const input = document.querySelector(`input[name='valor_${i + 1}_${j + 1}']`);
                const valor = parseFloat(input.value);
                if (isNaN(valor)) {
                    alert(`El valor en la posición (${i + 1}, ${j + 1}) no es un número válido.`);
                    return []; // Return an empty array to indicate error
                }
                fila.push(valor);
            }
            matriz.push(fila);
        }

        return matriz;
    }

    // Function to obtain the independent terms as an array
    function obtenerTerminosIndependientes() {
        const tamMtrx = parseInt(document.getElementById('id_tamMtrx').value);
        const termsIndp = [];

        for (let i = 0; i < tamMtrx; i++) {
            const input = document.querySelector(`input[name='result_${i + 1}']`);
            const valor = parseFloat(input.value);
            if (isNaN(valor)) {
                alert(`El valor del resultado en la posición ${i + 1} no es un número válido.`);
                return []; // Return an empty array to indicate error
            }
            termsIndp.push(valor);
        }

        return termsIndp;
    }
});