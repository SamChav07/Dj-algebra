import re
import json
import sympy as sp
from sympy import lambdify, symbols, sympify


class AnNumerico:
    """
    Clase orientada al análisis numérico, que implementa métodos como la bisección.
    """

    def __init__(self, bi_funcion_data):
        """
        Inicializa la clase con los datos JSON de la función y el intervalo.
        :param bi_funcion_data: JSON anidado con la función y parámetros como string o diccionario.
        """
        # Si es un string JSON, deserializarlo
        if isinstance(bi_funcion_data, str):
            bi_funcion_data = json.loads(bi_funcion_data)

        # Verificar que se proporcionen las claves necesarias
        if not bi_funcion_data.get("bi_funcion") or not bi_funcion_data.get("bi_AB"):
            raise ValueError("El JSON debe contener 'bi_funcion' y 'bi_AB'.")

        self.func_text = bi_funcion_data["bi_funcion"]  # Función matemática como texto
        self.bi_AB_data = json.loads(bi_funcion_data["bi_AB"])  # Intervalo y tolerancia como diccionario

        # Extraer los parámetros del intervalo y tolerancia
        self.a = float(self.bi_AB_data.get("a"))
        self.b = float(self.bi_AB_data.get("b"))
        self.tolerance = float(self.bi_AB_data.get("tolerance"))

        # Verifica si la función es válida
        if not self.func_text:
            raise ValueError("La función no puede ser None o vacía.")
        if not isinstance(self.func_text, str):
            raise ValueError("La función debe ser proporcionada como una cadena de texto.")

    def run_bisection(self):
        """
        Ejecuta el método de bisección usando los datos proporcionados.
        """
        try:
            # Prepara la expresión matemática
            func_text = self.prepare_expression(self.func_text)
            x = symbols('x')
            func = lambdify(x, sympify(func_text), 'math')  # Crea una función numérica a partir de la expresión simbólica

            # Llama al método de bisección con los parámetros inicializados
            steps, solution = self.bisection(func, self.a, self.b, self.tolerance)

            # Retorna los resultados (pasos y la raíz aproximada)
            return {'solucion': solution, 'iteraciones': steps}
        except Exception as e:
            raise ValueError(f"Error en la ejecución de bisección: {e}")

    def prepare_expression(self, expr):
        """
        Prepara una expresión para ser evaluada, corrigiendo la sintaxis.
        :param expr: Cadena de texto de la función matemática.
        :return: Cadena de texto corregida.
        """
        expr = re.sub(r'(\d)([a-zA-Z(])', r'\1*\2', expr)  # Añade multiplicación implícita entre números y variables
        expr = expr.replace('^', '**')  # Cambia la notación de potencia de ^ a **
        return expr

    def bisection(self, func, a, b, tol):
        """
        Método de bisección para encontrar la raíz de una función.
        :param func: Función matemática evaluable.
        :param a: Extremo izquierdo del intervalo.
        :param b: Extremo derecho del intervalo.
        :param tol: Tolerancia deseada para el resultado.
        :return: Pasos del cálculo y la raíz aproximada.
        """
        steps = []
        solution = None

        # Verifica si el intervalo es válido
        if func(a) * func(b) >= 0:
            raise ValueError("El intervalo no es válido para el método de bisección.")

        iter_count = 0
        while (b - a) / 2.0 > tol:
            iter_count += 1
            c = (a + b) / 2.0
            steps.append(f"Iteración {iter_count}: a = {a}, b = {b}, c = {c}, f(c) = {func(c)}")

            if abs(func(c)) < tol:
                solution = c
                break

            if func(a) * func(c) < 0:
                b = c
            else:
                a = c

        # Solo se calcula la raíz, pero no se agrega al resultado de las iteraciones
        if solution is None:
            solution = (a + b) / 2.0
        # Solo se devuelve el resultado de las iteraciones
        return steps, solution