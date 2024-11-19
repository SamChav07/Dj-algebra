// Espera a que el DOM se cargue completamente
document.addEventListener("DOMContentLoaded", function () {
    const functionInput = document.getElementById("functionInput");
    const renderedFunctionView = document.getElementById("renderedFunctionView");
    const toggleButtons = document.getElementById("toggleButtons");
    const functionButtons = document.getElementById("functionButtons");

    // Configuración de los botones matemáticos
    const buttonsConfig = [
        // Primera fila
        ['+', '+'], ['-', '-'], ['×', '\\times '], ['÷', '\\div '],
        // Segunda fila
        ['xˣ', 'x^{'], ['√', '\\sqrt{'], ['ln', '\\ln('], ['log₁₀', '\\log_{10}('],
        ['logₐ', '\\log_{'], ['sin', '\\sin('], ['cos', '\\cos('], ['tan', '\\tan('],
        // Tercera fila
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

        // Si el texto termina con "{" (como en x^{ o sqrt{), agregamos automáticamente el cierre "}"
        const newValue =
            currentValue.slice(0, cursorPosition) +
            text +
            (text.endsWith('{') ? '}' : '') +
            currentValue.slice(cursorPosition);

        functionInput.value = newValue;

        // Si se agrega un "{" automáticamente, posicionamos el cursor dentro de las llaves
        if (text.endsWith('{')) {
            functionInput.selectionStart = functionInput.selectionEnd = cursorPosition + text.length;
        } else {
            functionInput.selectionStart = functionInput.selectionEnd = cursorPosition + text.length;
        }

        // Dispara un evento de entrada para actualizar la vista renderizada
        