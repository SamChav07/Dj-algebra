// ../js/SumMatrx.js - Suma de Matrices y Escalares
document.addEventListener('DOMContentLoaded', function () {
    const createMatrixBtn = document.getElementById('createMatrixBtn');
    const matrixContainer = document.getElementById('matrixContainer');
    const resolveBtn = document.getElementById('resolveBtn');
    const resolverForm = document.getElementById('resolverForm');

    // Evento para crear las matrices y los escalares
    createMatrixBtn.addEventListener('click', function () {
        const numMatrices = parseInt(document.getElementById('id_numMatrices').value);
        const filas = parseInt(document.getElementById('id_filas').value);
        const columnas = parseInt(document.getElementById('id_columnas').value);
        
        matrixContainer.innerHTML = '';  // Limpiar el contenedor

        if (validarEntradas(numMatrices, filas, columnas)) {
            for (let i = 0; i < numMatrices; i++) {
                crearMatriz(i, filas, columnas);
            }
            crearEscalareColumnas(numMatrices);
            resolveBtn.style.display = 'block';  // Mostrar el botón "Resolver"
        }
    });

    resolverForm.addEventListener('submit', async function (event) {
        event.preventDefault();
        try {
            const matrices = obtenerMatrices();
            const escalares = obtenerEscalares();

            const formData = new URLSearchParams({
                sMrx_matrxS: JSON.stringify(matrices),
                sMrx_escalares: JSON.stringify(escalares),
            });
            
            console.log("Datos enviados:", formData.toString());  // Comprobación de datos antes de enviar
    
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
            if (response.ok) {
                document.getElementById('resultText').textContent = data.resultado;
            } else {
                console.error("Error de respuesta:", data.message);
                alert(data.message || 'Error al procesar la solicitud.');
            }
        } catch (error) {
            console.error('Error:', error);
            alert('Ocurrió un error al enviar los datos.');
        }
    });

    function validarEntradas(numMatrices, filas, columnas) {
        if (isNaN(numMatrices) || numMatrices <= 0) {
            alert('Por favor, ingresa un número válido de matrices.');
            return false;
        }
        if (isNaN(filas) || filas <= 0) {
            alert('Por favor, ingresa un número válido de filas.');
            return false;
        }
        if (isNaN(columnas) || columnas <= 0) {
            alert('Por favor, ingresa un número válido de columnas.');
            return false;
        }
        return true;
    }

    function crearMatriz(matrixIndex, filas, columnas) {
        const matrixDiv = document.createElement('div');
        const table = document.createElement('table');
        table.className = 'table table-bordered mt-3';
        const caption = document.createElement('caption');
        caption.textContent = `Matriz ${matrixIndex + 1}`;
        table.appendChild(caption);

        for (let i = 0; i < filas; i++) {
            const row = document.createElement('tr');
            for (let j = 0; j < columnas; j++) {
                const cell = document.createElement('td');
                const input = document.createElement('input');
                input.type = 'number';
                input.className = 'form-control';
                input.placeholder = `(${i + 1}, ${j + 1})`;
                input.name = `matriz_${matrixIndex}_${i}_${j}`;
                cell.appendChild(input);
                row.appendChild(cell);
            }
            table.appendChild(row);
        }
        
        matrixDiv.appendChild(table);
        matrixContainer.appendChild(matrixDiv);
    }

    function crearEscalareColumnas(numMatrices) {
        const escalarTable = document.createElement('table');
        escalarTable.className = 'table table-bordered mt-3';
        const headerRow = document.createElement('tr');
        const th1 = document.createElement('th');
        th1.textContent = 'Escalar';
        headerRow.appendChild(th1);
        escalarTable.appendChild(headerRow);

        for (let i = 0; i < numMatrices; i++) {
            const row = document.createElement('tr');
            const cell = document.createElement('td');
            const input = document.createElement('input');
            input.type = 'number';
            input.className = 'form-control';
            input.placeholder = `Escalar de Matriz ${i + 1}`;
            input.name = `escalar_${i}`;
            cell.appendChild(input);
            row.appendChild(cell);
            escalarTable.appendChild(row);
        }

        matrixContainer.appendChild(escalarTable);
    }

    function obtenerMatrices() {
        const filas = parseInt(document.getElementById('id_filas').value);
        const columnas = parseInt(document.getElementById('id_columnas').value);
        const matrices = [];
        const numMatrices = parseInt(document.getElementById('id_numMatrices').value);

        for (let matrixIndex = 0; matrixIndex < numMatrices; matrixIndex++) {
            const matriz = [];
            for (let i = 0; i < filas; i++) {
                const fila = [];
                for (let j = 0; j < columnas; j++) {
                    const input = document.querySelector(`input[name='matriz_${matrixIndex}_${i}_${j}']`);
                    fila.push(parseFloat(input.value) || 0);
                }
                matriz.push(fila);
            }
            matrices.push(matriz);
        }
        return matrices;
    }

    function obtenerEscalares() {
        const escalarInputs = matrixContainer.querySelectorAll('input[name^="escalar_"]');
        return Array.from(escalarInputs).map(input => parseFloat(input.value) || 0);
    }
});