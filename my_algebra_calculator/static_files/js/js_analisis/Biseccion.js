document.addEventListener("DOMContentLoaded", function () {
    const functionInput = document.getElementById("id_functionInput");
    const renderedFunctionView = document.getElementById("renderedFunctionView");
    const toggleButtons = document.getElementById("toggleButtons");
    const functionButtons = document.getElementById("functionButtons");
    const bisectionForm = document.getElementById('bisectionForm');

    // Configuración de los botones matemáticos
    const buttonsConfig = [
        ['+', '+'], ['-', '-'], ['×', '*'], ['÷', '/'],
        ['xˣ', '**'], ['√', 'sqrt('], ['ln', 'ln('], ['log₁₀', 'log10('],
        ['logₐ', 'log('], ['sin', 'sin('], ['cos', 'cos('], ['tan', 'tan('],
        ['sinh', 'sinh('], ['cosh', 'cosh('], ['tanh', 'tanh('], ['arcsin', 'asin('],
        ['arccos', 'acos('], ['arctan', 'atan('], ['cot', 'cot('], ['sec', 'sec('],
        ['csc', 'csc('], ['(', '('], [')', ')'], ['π', 'pi'], ['e', 'E']
    ];

    // Generar dinámicamente los botones del teclado
    functionButtons.innerHTML = ""; // Limpiar cualquier contenido previo
    buttonsConfig.forEach(([label, value]) => {
        const button = document.createElement("button");
        button.textContent = label;
        button.type = "button"; // Se asegura de que no sea un botón de envío
        button.classList.add("btn", "btn-secondary", "m-1");
        button.style.minWidth = "50px";

        // Evento para insertar texto en el input
        button.addEventListener("click", function () {
            insertText(value);
            functionInput.focus(); // Mantiene el foco en el campo de entrada
        });

        functionButtons.appendChild(button);
    });

    // Función para insertar texto en el campo de entrada
    function insertText(text) {
        const cursorPosition = functionInput.selectionStart;
        const currentValue = functionInput.value;

        const newValue =
            currentValue.slice(0, cursorPosition) +
            text +
            currentValue.slice(cursorPosition);

        functionInput.value = newValue;

        functionInput.selectionStart = functionInput.selectionEnd = cursorPosition + text.length;

        // Dispara un evento de entrada para actualizar la vista renderizada
        functionInput.dispatchEvent(new Event("input"));
    }

    // Escucha los cambios en el campo de entrada
    functionInput.addEventListener("input", function () {
        const functionText = functionInput.value;

        // Renderiza la función usando MathJax para que sea legible para el usuario
        renderedFunctionView.innerHTML = `
            Aquí se renderizará la función ingresada: 
            <div id="math-output" style="font-size: 28px; color: black; padding: 20px;">\\( ${functionText.replace(/\*\*/g, '^')} \\)</div>
        `;

        MathJax.typeset();
    });

    // Agregar evento de clic para mostrar/ocultar los botones
    toggleButtons.addEventListener("click", function () {
        functionButtons.classList.toggle("d-none");
    });

    // Función para obtener datos del formulario
    function obtenerDatosFormulario() {
        const funcion = functionInput.value.trim();
        const a = parseFloat(document.getElementById("inputA").value);
        const b = parseFloat(document.getElementById("inputB").value);
        const tolerance = parseFloat(document.getElementById("inputTolerance").value);

        if (!funcion) {
            alert('La función no puede estar vacía.');
            return null;
        }

        if (isNaN(a) || isNaN(b) || isNaN(tolerance)) {
            alert('Por favor, ingrese valores válidos para a, b y tolerancia.');
            return null;
        }

        // Crear la estructura de datos en el formato esperado
        const bi_funcion = JSON.stringify({
            bi_funcion: funcion,
            bi_AB: JSON.stringify({ a, b, tolerance })
        });

        return { bi_funcion };
    }

    // Función para manejar el envío del formulario mediante AJAX
    bisectionForm.addEventListener('submit', async function (event) {
        event.preventDefault(); // Prevenir el envío normal del formulario

        const datosAEnviar = obtenerDatosFormulario();
        if (!datosAEnviar) return; // Si hay un error en la obtención de datos, salir

        console.log('Datos a Enviar:', datosAEnviar);

        const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;

        try {
            const response = await fetch(bisectionForm.action, {
                method: 'POST',
                body: JSON.stringify(datosAEnviar),
                headers: {
                    'Content-Type': 'application/json',
                    'X-Requested-With': 'XMLHttpRequest',
                    'X-CSRFToken': csrftoken
                }
            });

            const data = await response.json();

            if (data.status === 'success') {
                mostrarResultados(data); // Muestra resultados en la interfaz
            } else {
                let errorMessage = data.message;
                if (data.errors) {
                    errorMessage += '\nErrores específicos:\n' + data.errors.join('\n');
                }
                alert(errorMessage);
            }

        } catch (error) {
            alert('Ocurrió un error al enviar los datos.');
            console.error(error);
        }
    });

    // Función para manejar la respuesta del servidor
    function mostrarResultados(data) {
        if (data.status === 'success') {
            const resultados = data.resultados;
            mostrarSolucion(resultados);
            mostrarIteraciones(resultados.iteraciones);
        } else {
            console.error("Error en la respuesta:", data.message);
        }
    }

    function mostrarSolucion(resultados) {
        // Extraer la raíz aproximada y las iteraciones desde el JSON de la respuesta
        const raizAproximada = resultados.solucion;
        const iteraciones = resultados.iteraciones;
        
        // Determinar el número máximo de iteraciones
        const numeroIteraciones = iteraciones.length;  // El número de iteraciones es igual a la longitud del array de iteraciones
    
        // Mostrar la solución y el número de iteraciones
        document.getElementById('resultTextS').innerHTML = `
            <p>${raizAproximada}<br>Número de iteraciones: ${numeroIteraciones}</p>
        `;
        
        // Activar la pestaña de solución
        activateTab('tabS');
    }

    function mostrarIteraciones(iteraciones) {
        const iteracionesContainer = document.getElementById('resultTextIter');

        // Almacenamos todas las iteraciones en un contenedor oculto para hacer la búsqueda
        const allIterationsHtml = iteraciones.map(paso => `<li>${paso}</li>`).join('');
        iteracionesContainer.innerHTML = `<h4>Iteraciones:</h4><ul id="iteracionesList">${allIterationsHtml}</ul>`;

        // Habilitar la búsqueda
        activateTab('tabI');
    }

    // Mostrar el campo de entrada para buscar iteración específica al hacer clic en la lupa
    document.getElementById('searchIcon').addEventListener('click', function() {
        const input = document.getElementById('iterationInput');
        input.style.display = input.style.display === 'none' ? 'block' : 'none';
        input.focus();
    });

    // Función para mostrar la iteración específica ingresada cuando se presione "Enter"
    document.getElementById('iterationInput').addEventListener('keypress', function(event) {
        if (event.key === "Enter") { // Solo se activa cuando se presiona Enter
            showSpecificIteration();
        }
    });

    function showSpecificIteration() {
        const iterationNumber = parseInt(document.getElementById('iterationInput').value, 10);

        if (!isNaN(iterationNumber) && iterationNumber > 0) {
            const iteraciones = document.getElementById('iteracionesList').getElementsByTagName('li');
            const iteration = iteraciones[iterationNumber - 1];  // Iteración ingresada (1-indexed)

            if (iteration) {
                const iterationContent = iteration.textContent.trim();

                // Procesamos el contenido de la iteración para extraer y mostrar los datos
                const iterationDetails = iterationContent.split(", ");
                let formattedMessage = `Iteración ${iterationNumber}:\n`;

                iterationDetails.forEach((detail, index) => {
                    formattedMessage += `${detail}\n`;
                });

                // Mostrar la iteración en una ventana emergente ordenada
                alert(formattedMessage);
            } else {
                alert('Iteración no encontrada.');
            }
        } else {
            alert('Por favor ingrese un número válido de iteración.');
        }
    }

    function activateTab(tabId) {
        const tab = document.querySelector(`a[href="#${tabId}"]`);
        if (tab) tab.click();
    }
});

document.addEventListener("DOMContentLoaded", function () {
    const functionInput = document.getElementById("id_functionInput");
    const renderedFunctionView = document.getElementById("renderedFunctionView");
    const desmosContainer = document.getElementById("desmos-graph");

    // Inicializar Desmos
    const calculator = Desmos.GraphingCalculator(desmosContainer, { expressions: true });

    function mostrarSolucion(resultados) {
        const raizAproximada = resultados.solucion;
        const iteraciones = resultados.iteraciones;

        document.getElementById('resultTextS').innerHTML = `
            <p>Raíz aproximada: ${raizAproximada}<br>
            Número de iteraciones: ${iteraciones.length}</p>
        `;

        // Graficar función en Desmos
        calculator.setExpression({ id: 'graph1', latex: `y=${functionInput.value}` });
        if (!isNaN(raizAproximada)) {
            calculator.setExpression({ id: 'root', latex: `(${raizAproximada}, 0)` });
        }
    }

    function mostrarIteraciones(iteraciones) {
        const iteracionesContainer = document.getElementById('resultTextIter');
        iteracionesContainer.innerHTML = `
            <h4>Iteraciones:</h4>
            <ul id="iteracionesList">
                ${iteraciones.map((iter, idx) => `<li>Iteración ${idx + 1}: ${iter}</li>`).join('')}
            </ul>
        `;
    }

    // Buscar iteración específica
    document.getElementById('searchIcon').addEventListener('click', function () {
        const input = document.getElementById('iterationInput');
        input.style.display = input.style.display === 'none' ? 'block' : 'none';
        input.focus();
    });

    // Mostrar iteración específica
    document.getElementById('iterationInput').addEventListener('change', function () {
        const iteracionNum = parseInt(this.value, 10) - 1;
        const iteraciones = document.querySelectorAll('#iteracionesList li');
        if (iteraciones[iteracionNum]) {
            alert(iteraciones[iteracionNum].textContent);
        } else {
            alert('Iteración no encontrada.');
        }
    });
});

document.getElementById('id_functionInput').addEventListener('input', function() {
    var inputValue = this.value;

    document.getElementById('functionInput').value = inputValue;
})