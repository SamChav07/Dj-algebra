document.addEventListener("DOMContentLoaded", function () {
    const functionInput = document.getElementById("id_functionInput");
    const renderedFunctionView = document.getElementById("renderedFunctionView");
    const toggleButtons = document.getElementById("toggleButtons");
    const functionButtons = document.getElementById("functionButtons");
    const bisectionForm = document.getElementById('nRaphsonForm');

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

    function obtenerDatosFormulario() {
        const funcion = functionInput.value.trim();
        const a = parseFloat(document.getElementById("inputA").value);

        if (!funcion) {
            alert('La función no puede estar vacía.');
            return null;
        }

        if (isNaN(a)) {
            alert('Por favor, ingrese valores válidos para a, b y tolerancia.');
            return null;
        }

        // Crear la estructura de datos en el formato esperado
        const new_funcion = JSON.stringify({
            new_funcion: funcion,
            new_xCero: a,
        });

        return { new_funcion };
    }

    
});