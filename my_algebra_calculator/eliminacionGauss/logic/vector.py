

class Vector:
    """Clase para representar y operar con vectores de tamaño variable."""

    def __init__(self, componentes):
        # Verifica que las componentes sean una lista o tupla de números (enteros o flotantes).
        if not isinstance(componentes, (list, tuple)) or not all(isinstance(x, (int, float)) for x in componentes):
            raise ValueError("Las componentes deben ser una lista o tupla de números.")
        self.componentes = list(componentes)  # Almacena los componentes del vector.

    def __str__(self):
        # Devuelve una representación en cadena de caracteres del vector.
        return f"Vector({self.componentes})"

    def __add__(self, otro):
        # Suma dos vectores usando el método estático suma_escalada.
        if not isinstance(otro, Vector):
            raise ValueError("El operando debe ser un Vector.")
        return Vector.suma_escalada([self, otro], [1, 1])

    def __sub__(self, otro):
        # Resta dos vectores usando el método estático suma_escalada con un escalar negativo para el segundo vector.
        if not isinstance(otro, Vector):
            raise ValueError("El operando debe ser un Vector.")
        return Vector.suma_escalada([self, otro], [1, -1])

    def __mul__(self, escalar):
        # Multiplica el vector por un escalar (número), aplicando el escalar a cada componente.
        if not isinstance(escalar, (int, float)):
            raise ValueError("El escalar debe ser un número.")
        producto = [escalar * x for x in self.componentes]
        return Vector(producto)

    def __rmul__(self, escalar):
        # Facilita la multiplicación del vector por un escalar desde el lado izquierdo.
        return self.__mul__(escalar)

    def producto_punto(self, otro_vector):
        # Calcula el producto punto (escalar) entre dos vectores, multiplicando componentes correspondientes y sumando los resultados.
        if not isinstance(otro_vector, Vector):
            raise ValueError("El operando debe ser un Vector.")
        if len(self.componentes) != len(otro_vector.componentes):
            raise ValueError("Los vectores deben tener la misma longitud.")
        producto = sum(f * c for f, c in zip(self.componentes, otro_vector.componentes))
        return producto

    def formato_resultado(self, otro_vector, resultado):
        vector_fila_str = f"Vector Fila: {self.componentes}"
        vector_columna_str = f"Vector Columna: {otro_vector.componentes}"
        ecuacion_str = " + ".join([f"{f} * {c}" for f, c in zip(self.componentes, otro_vector.componentes)])
        resultado_str = f"Resultado: {resultado:.2f}"

        # Formatear el texto final
        resultado_texto = (
            f"Producto Escalar:\n\n"
            f"{vector_fila_str}\n\n"
            f"{vector_columna_str}\n\n"
            f"{ecuacion_str} = {resultado_str}"
        )
        return resultado_texto
    
    @staticmethod
    def suma_escalada(lista_vectores, lista_escalars):
        # Suma una lista de vectores, cada uno escalado por un valor correspondiente de lista_escalars.
        if len(lista_vectores) != len(lista_escalars):
            raise ValueError("La cantidad de vectores debe coincidir con la cantidad de escalares.")
        
        longitud = len(lista_vectores[0].componentes)
        for vector in lista_vectores:
            if len(vector.componentes) != longitud:
                raise ValueError("Todos los vectores deben tener la misma longitud.")
        
        suma = [0] * longitud
        operation_steps = []  # To store the operation steps for display

        for vector, escalar in zip(lista_vectores, lista_escalars):
            suma = [s + (escalar * v) for s, v in zip(suma, vector.componentes)]
            # Format operation details
            formatted_vector = f"[{', '.join(map(str, vector.componentes))}]"
            operation_steps.append(f"{escalar} * {formatted_vector}")

        # Construct equation in a readable format
        equation = " + ".join(operation_steps)
        result_vector = Vector(suma)

        return result_vector, equation

