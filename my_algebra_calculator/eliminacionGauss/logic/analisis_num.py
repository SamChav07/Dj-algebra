import re
import sympy as sp
from sympy import lambdify, symbols, sympify

class AnNumerico:
    """
    Clase orientada al análisis numérico, que implementa métodos como la bisección.
    """

    def __init__(self, Lfunction):
        # Verifica si la función es válida
        if not Lfunction:
            raise ValueError("La función no puede ser None o vacía.")
        if not isinstance(Lfunction, str):
            raise ValueError("La función debe ser proporcionada como una cadena de texto.")
        
        self.Lfunction = Lfunction

    def run_bisection(self):
        try:
            # Prepara la expresión matemática
            func_text = self.prepare_expression(self.Lfunction)
            x = symbols('x')
            func = lambdify(x, sympify(func_text), 'math')  # Crea una función numérica a partir de la expresión simbólica
            
            # Valores de a, b, y tolerancia (simulados en este caso)
            a = float(input("Ingrese el valor de a: "))
            b = float(input("Ingrese el valor de b: "))
            tol = float(input("Ingrese la tolerancia: "))

            # Llama al método de bisección
            result = self.bisection(func, a, b, tol)
            print(result)  # Aquí lo mostramos en consola, pero puedes cambiarlo a una interfaz gráfica si lo deseas
        except Exception as e:
            raise ValueError(f"Error en la entrada: {e}")

    def prepare_expression(self, expr):
        """
        Prepara una expresión para ser evaluada, corrigiendo la sintaxis.
        """
        expr = re.sub(r'(\d)([a-zA-Z(])', r'\1*\2', expr)  # Añade multiplicación implícita entre números y variables
        expr = expr.replace('^', '**')  # Cambia la notación de potencia de ^ a **
        return expr

    def bisection(self, func, a, b, tol):
        """
        Método de bisección para encontrar la raíz de una función.
        """
        steps = ""
        
        # Verifica si el intervalo es válido
        if func(a) * func(b) >= 0:
            raise ValueError("El intervalo no es válido para el método de bisección.")

        iter_count = 0
        while (b - a) / 2.0 > tol:
            iter_count += 1
            c = (a + b) / 2.0
            steps += f"Iteración {iter_count}: a = {a}, b = {b}, c = {c}, f(c) = {func(c)}\n"

            if abs(func(c)) < tol:
                steps += f"Raíz aproximada encontrada en x = {c}\n"
                return steps

            if func(a) * func(c) < 0:
                b = c
            else:
                a = c

        steps += f"Raíz aproximada encontrada en x = {(a + b) / 2.0}\n"
        return steps