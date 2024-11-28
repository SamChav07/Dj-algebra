document.addEventListener('DOMContentLoaded', function () {
    const createMatrixBtn = document.getElementById('createMatrixInputs');
    const matrixContainer = document.getElementById('matrixInputsContainer');
    const validateBtn = document.getElementById('validateMatricesBtn');
    const resolveBtn = document.getElementById('resolveBtn');
    const resolverForm = document.getElementById('resolverForm');
    const resultText = document.getElementById('resultText');
    const numMatricesInput = document.getElementById('id_numMatrices');

    createMatrixBtn.addEventListener('click', function () {
        const numMatrices = parseInt(numMatricesInput.value);
        matrixContainer.innerHTML = ''; // Limpiar matrices previas

        for (let i = 0; i < numMatrices; i++) {
            const matrixDiv = document.createElement('div');
            matrixDiv.className = 'matrix-inputs mb-4';
            matrixDiv.innerHTML = `
                <h5>Matriz ${i + 1}</h5>
                <div class="mb-3">
                    <label for="id_filas_${i}" class="form-label">Filas:</label>
                    <input type="number" id="id_filas_${i}" name="filas_${i}" class="form-control" placeholder="Número de filas" min="1" required>
                </div>
                <div class="mb-3">
                    <label for="id_columnas_${i}" class="form-label">Columnas:</label>
                    <input type="number" id="id_columnas_${i}" name="columnas_${i}" class="form-control" placeholder="Número de columnas" min="1" required>
                </div>
            `;
            matrixContainer.appendChild(matrixDiv);
        }

        validateBtn.style.display = 'inline-block';
    });

    validateBtn.addEventListener('click', function () {
        const matrices = [];
        const numMatrices = parseInt(numMatricesInput.value);

        for (let i = 0; i < numMatrices; i++) {
            const filas = parseInt(document.getElementById(`id_filas_${i}`).value);
            const columnas = parseInt(document.getElementById(`id_columnas_${i}`).value);
            matrices.push({ filas, columnas });
        }

        let canMultiply = true;
        for (let i = 0; i < matrices.length - 1; i++) {
            if (matrices[i].columnas !== matrices[i + 1].filas) {
                canMultiply = false;
                break;
            }
        }

        if (canMultiply) {
            alert("Las matrices se pueden multiplicar.");
            generateMatrixTables(matrices);
            resolveBtn.style.display = 'block';
        } else {
            alert("Error: El número de columnas de una matriz debe ser igual al número de filas de la siguiente.");
        }
    });

    function generateMatrixTables(matrices) {
        matrixContainer.innerHTML = '';

        matrices.forEach((matrix, index) => {
            const matrixTableDiv = document.createElement('div');
            matrixTableDiv.className = 'mb-4';
            matrixTableDiv.innerHTML = `
                <h5>Valores de Matriz ${index + 1}</h5>
                <input type="hidden" id="id_filas_${index}" value="${matrix.filas}">
                <input type="hidden" id="id_columnas_${index}" value="${matrix.columnas}">
            `;

            const table = document.createElement('table');
            table.className = 'table table-bordered';

            for (let i = 0; i < matrix.filas; i++) {
                const row = document.createElement('tr');
                for (let j = 0; j < matrix.columnas; j++) {
                    const cell = document.createElement('td');
                    cell.innerHTML = `<input type="number" name="matriz_${index}_${i}_${j}" class="form-control" required>`;
                    row.appendChild(cell);
                }
                table.appendChild(row);
            }

            matrixTableDiv.appendChild(table);
            matrixContainer.appendChild(matrixTableDiv);
        });
    }

    resolverForm.addEventListener('submit', async function (event) {
        event.preventDefault();
        const matrices = gatherMatrices();

        if (!matrices) {
            alert("Error al recolectar las matrices.");
            return;
        }

        try {
            const result = multiplyMatricesWithSteps(matrices);
            resultText.innerHTML = `<pre>${result.steps}</pre>`;
            resultText.innerHTML += `<h5>Resultado final:</h5><pre>${result.finalMatrix}</pre>`;
        } catch (error) {
            alert(error.message);
        }
    });

    function gatherMatrices() {
        const matrices = [];
        const numMatrices = parseInt(numMatricesInput.value);

        console.log("Número de matrices:", numMatrices);

        for (let matrixIndex = 0; matrixIndex < numMatrices; matrixIndex++) {
            const filasInput = document.getElementById(`id_filas_${matrixIndex}`);
            const columnasInput = document.getElementById(`id_columnas_${matrixIndex}`);

            if (!filasInput || !columnasInput) {
                console.error(`Error: Elementos id_filas_${matrixIndex} o id_columnas_${matrixIndex} no encontrados.`);
                return null;
            }

            const filas = parseInt(filasInput.value);
            const columnas = parseInt(columnasInput.value);

            console.log(`Matriz ${matrixIndex + 1} - Filas: ${filas}, Columnas: ${columnas}`);

            const matriz = [];
            for (let i = 0; i < filas; i++) {
                const fila = [];
                for (let j = 0; j < columnas; j++) {
                    const input = document.querySelector(`input[name='matriz_${matrixIndex}_${i}_${j}']`);
                    fila.push(parseFloat(input?.value) || 0);
                }
                matriz.push(fila);
            }
            matrices.push(matriz);
        }
        return matrices;
    }

    function multiplyMatricesWithSteps(matrices) {
        let result = matrices[0];
        let steps = "Proceso de Multiplicación de Matrices:\n\n";

        for (let m = 1; m < matrices.length; m++) {
            const matrixB = matrices[m];
            const newResult = [];
            for (let i = 0; i < result.length; i++) {
                const newRow = [];
                for (let j = 0; j < matrixB[0].length; j++) {
                    let sum = 0;
                    let detailOperation = [];
                    for (let k = 0; k < matrixB.length; k++) {
                        sum += result[i][k] * matrixB[k][j];
                        detailOperation.push(`${result[i][k]} * ${matrixB[k][j]}`);
                    }
                    newRow.push(sum);
                    steps += `Elemento (${i + 1}, ${j + 1}): ${detailOperation.join(" + ")} = ${sum}\n`;
                }
                newResult.push(newRow);
            }
            result = newResult;
            steps += `\nPaso ${m}: Resultado parcial después de multiplicar con Matriz ${m + 1}\n${formatMatrix(result)}\n\n`;
        }

        return {
            steps: steps,
            finalMatrix: formatMatrix(result),
        };
    }

    function formatMatrix(matrix) {
        return matrix.map(row => row.join("\t")).join("\n");
    }
});