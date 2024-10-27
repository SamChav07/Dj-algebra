// ../js/PropMxV.js - Producto Matriz por Vector y Propiedad
document.addEventListener('DOMContentLoaded', function () {
    const createMatrixBtn = document.getElementById('createMatrixBtn');
    const matrixContainer = document.getElementById('matrixContainer');
    const resolveBtn = document.getElementById('resolveBtn');
    const resolverForm = document.getElementById('resolverForm');

    // Evento para crear la matriz y los vectores
    createMatrixBtn.addEventListener('click', function () {
        const filas = parseInt(document.getElementById('id_filas').value);
        const columnas = parseInt(document.getElementById('id_columnas').value);
        
        matrixContainer.innerHTML = '';  // Limpiar el contenedor

        if (validarEntradas(filas, columnas)) {
            crearMatriz(filas, columnas);
            crearVector('vectorU', columnas, 'Vector U');  // Crear vector en función de las columnas
            crearVector('vectorV', columnas, 'Vector V');  // Crear vector en función de las columnas
            resolveBtn.style.display = 'block';  // Mostrar el botón "Resolver"
        }
    });

    resolverForm.addEventListener('submit', async function (event) {
        event.preventDefault();
        try {
            const matriz = obtenerMatriz();
            const vectorU = obtenerVector('vectorU');
            const vectorV = obtenerVector('vectorV');
            const formData = new URLSearchParams({
                EG_matriz: JSON.stringify(matriz),
                EG_vectorU: JSON.stringify(vectorU),
                EG_vectorV: JSON.stringify(vectorV),
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

    function validarEntradas(filas, columnas) {
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

    function crearMatriz(filas, columnas) {
        const table = document.createElement('table');
        table.className = 'table table-bordered';
        for (let i = 0; i < filas; i++) {
            const row = document.createElement('tr');
            for (let j = 0; j < columnas; j++) {
                const cell = document.createElement('td');
                const input = document.createElement('input');
                input.type = 'number';
                input.className = 'form-control';
                input.placeholder = `(${i + 1}, ${j + 1})`;
                input.name = `matriz_${i}_${j}`;
                cell.appendChild(input);
                row.appendChild(cell);
            }
            table.appendChild(row);
        }
        matrixContainer.appendChild(table);
    }

    function crearVector(vectorName, columnas, headerText) {
        const vectorContainer = document.createElement('div');
        const table = document.createElement('table');
        table.className = 'table table-bordered';
        const rowHeader = document.createElement('tr');
        const th = document.createElement('th');
        th.textContent = headerText;
        rowHeader.appendChild(th);
        table.appendChild(rowHeader);

        for (let i = 0; i < columnas; i++) {  // Usar el número de columnas para el tamaño del vector
            const row = document.createElement('tr');
            const cell = document.createElement('td');
            const input = document.createElement('input');
            input.type = 'number';
            input.className = 'form-control';
            input.placeholder = `Componente ${i + 1}`;
            input.name = `${vectorName}_${i}`;
            cell.appendChild(input);
            row.appendChild(cell);
            table.appendChild(row);
        }

        vectorContainer.appendChild(table);
        matrixContainer.appendChild(vectorContainer);
    }

    function obtenerMatriz() {
        const filas = parseInt(document.getElementById('id_filas').value);
        const columnas = parseInt(document.getElementById('id_columnas').value);
        const matriz = [];
        for (let i = 0; i < filas; i++) {
            const fila = [];
            for (let j = 0; j < columnas; j++) {
                const input = document.querySelector(`input[name='matriz_${i}_${j}']`);
                fila.push(parseFloat(input.value) || 0);
            }
            matriz.push(fila);
        }
        return matriz;
    }

    function obtenerVector(vectorName) {
        return Array.from(document.querySelectorAll(`input[name^=${vectorName}]`)).map(input => parseFloat(input.value) || 0);
    }
});