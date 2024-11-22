document.addEventListener("DOMContentLoaded", function () {
    const functionInput = document.getElementById("id_functionInput");
    const renderedFunctionView = document.getElementById("renderedFunctionView");
    const toggleButtons = document.getElementById("toggleButtons");
    const functionButtons = document.getElementById("functionButtons");
    const bisectionForm = document.getElementById('bisectionForm');

    // Configuración de los botones matemáticos
    const buttonsConfig = [
        ['+', '+'], ['-', '-'], ['×', '\\times '], ['÷', '\\div '],
        ['xˣ', 'x^{'], ['√', '\\sqrt{'], ['ln', '\\ln('], ['log₁₀', '\\log_{10}('],
        ['logₐ', '\\log_{'], ['sin', '\\sin('], ['cos', '\\cos('], ['tan', '\\tan('],
        ['sinh', '\\sinh('], ['cosh', '\\cosh('], ['tanh', '\\tanh('], ['arcsin', '\\arcsin('],
        ['arccos', '\\arccos('], ['arctan', '\\arctan('], ['cot', '\\cot('], ['sec', '\\sec('],
        ['csc', '\\csc('], ['(', '('], [')', ')'], ['π', '\\pi '], ['e', 'e']
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
            (text.endsWith('{') ? '}' : '') +
            currentValue.slice(cursorPosition);

        functionInput.value = newValue;

        if (text.endsWith('{')) {
            functionInput.selectionStart = functionInput.selectionEnd = cursorPosition + text.length;
        } else {
            functionInput.selectionStart = functionInput.selectionEnd = cursorPosition + text.length;
        }

        // Dispara un evento de entrada para actualizar la vista renderizada
        functionInput.dispatchEvent(new Event("input"));
    }

    // Escucha los cambios en el campo de entrada
    functionInput.addEventListener("input", function () {
        const functionText = functionInput.value;

        // Renderiza la función usando MathJax
        renderedFunctionView.innerHTML = `
            Aquí se renderizará la función ingresada: 
            <div id="math-output" style="font-size: 28px; color: black; padding: 20px;">\\( ${functionText} \\)</div>
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

    // Función para mostrar los resultados en la página
    function mostrarResultados(resultados) {
        // Aquí puedes implementar cómo mostrar los resultados devueltos por el servidor.
        alert(`Resultado de la raíz: ${resultados.calc_Raiz}`); // Ejemplo simple

        // Puedes agregar más lógica aquí para mostrar matrices o pasos.
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
                mostrarResultados(data.resultado); // Muestra resultados en la interfaz
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
});