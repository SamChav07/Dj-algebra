document.addEventListener('DOMContentLoaded', function () {
    const createMatrixInputs = document.getElementById('createMatrixInputs');
    const matrixInputsContainer = document.getElementById('matrixInputsContainer');
    const resolveBtn = document.getElementById('resolveBtn');
    const resolverForm = document.getElementById('resolverForm');

    // Crear inputs para la matriz LU y vector b
    createMatrixInputs.addEventListener('click', function () {
        const tamMtrx = parseInt(document.getElementById('id_tamMtrx').value);

        // Validar el tamaño ingresado
        if (isNaN(tamMtrx) || tamMtrx <= 0) {
            alert('Por favor, ingresa un tamaño válido para la matriz (mayor que 0).');
            return;
        }

        // Limpiar inputs previos
        matrixInputsContainer.innerHTML = '';

        // Crear tabla para la matriz y el vector
        crearEntradasLU(tamMtrx);

        // Mostrar botón de resolver
        resolveBtn.style.display = 'block';
    });

    resolverForm.addEventListener('submit', async function (event) {
        event.preventDefault();
    
        try {
            const matriz = obtenerMatrizLU();
            const vectorB = obtenerVectorB();
    
            if (matriz.length === 0 || vectorB.length === 0) {
                alert('La matriz o el vector independiente no son válidos.');
                return;
            }
    
            const datosAEnviar = {
                lu_mtrx: matriz,
                lu_b: vectorB, // Asegúrate de que este campo sea opcional si decides no usarlo
            };
    
            const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    
            const response = await fetch(resolverForm.action, {
                method: 'POST',
                body: JSON.stringify(datosAEnviar),
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrftoken,
                },
            });
    
            const data = await response.json();
    
            if (data.status === 'success') {
                alert('Datos guardados correctamente.');
                document.getElementById('resultText').textContent = JSON.stringify(data.resultados, null, 2);
            } else {
                alert(data.message || 'Error al procesar los datos.');
            }
        } catch (error) {
            console.error('Error:', error);
            alert('Ocurrió un error al enviar los datos.');
        }
    });    

    // Crear entradas para la matriz y vector b
    function crearEntradasLU(tamMtrx) {
        const table = document.createElement('table');
        table.className = 'table table-bordered';

        for (let i = 0; i < tamMtrx; i++) {
            const row = document.createElement('tr');

            for (let j = 0; j < tamMtrx + 1; j++) {
                const cell = document.createElement('td');
                const input = document.createElement('input');
                input.type = 'number';
                input.className = 'form-control';

                if (j < tamMtrx) {
                    input.placeholder = `(${i + 1}, ${j + 1})`;
                    input.name = `valor_${i + 1}_${j + 1}`;
                } else {
                    input.placeholder = `b${i + 1}`;
                    input.name = `b_${i + 1}`;
                }

                cell.appendChild(input);
                row.appendChild(cell);
            }

            table.appendChild(row);
        }

        matrixInputsContainer.appendChild(table);
    }

    // Obtener matriz LU
    function obtenerMatrizLU() {
        const tamMtrx = parseInt(document.getElementById('id_tamMtrx').value);
        const matriz = [];

        for (let i = 0; i < tamMtrx; i++) {
            const fila = [];
            for (let j = 0; j < tamMtrx; j++) {
                const input = document.querySelector(`input[name='valor_${i + 1}_${j + 1}']`);
                const valor = parseFloat(input.value);

                if (isNaN(valor)) {
                    alert(`El valor en la posición (${i + 1}, ${j + 1}) no es un número válido.`);
                    return [];
                }

                fila.push(valor);
            }
            matriz.push(fila);
        }

        return matriz;
    }

    // Obtener vector b
    function obtenerVectorB() {
        const tamMtrx = parseInt(document.getElementById('id_tamMtrx').value);
        const vectorB = [];

        for (let i = 0; i < tamMtrx; i++) {
            const input = document.querySelector(`input[name='b_${i + 1}']`);
            const valor = parseFloat(input.value);

            if (isNaN(valor)) {
                alert(`El valor en b${i + 1} no es un número válido.`);
                return [];
            }

            vectorB.push(valor);
        }

        return vectorB;
    }
});