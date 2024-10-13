class Vector:
    """Clase para representar y operar con vectores de tamaño variable."""

    def __init__(self, componentes):
        if not isinstance(componentes, (list, tuple)) or not all(isinstance(x, (int, float)) for x in componentes):
            raise ValueError("Las componentes deben ser una lista o tupla de números.")
        self.componentes = list(componentes)

    def __str__(self):
        return f"Vector({self.componentes})"

    def __add__(self, otro):
        if not isinstance(otro, Vector):
            raise ValueError("El operando debe ser un Vector.")
        return Vector.suma_escalada([self, otro], [1, 1])

    def __sub__(self, otro):
        if not isinstance(otro, Vector):
            raise ValueError("El operando debe ser un Vector.")
        return Vector.suma_escalada([self, otro], [1, -1])

    def __mul__(self, escalar):
        if not isinstance(escalar, (int, float)):
            raise ValueError("El escalar debe ser un número.")
        producto = [escalar * x for x in self.componentes]
        return Vector(producto)

    def __rmul__(self, escalar):
        return self.__mul__(escalar)

    def producto_punto(self, otro):
        if not isinstance(otro, Vector):
            raise ValueError("El operando debe ser un Vector.")
        if len(self.componentes) != len(otro.componentes):
            raise ValueError("Los vectores deben tener la misma longitud.")
        return sum(a * b for a, b in zip(self.componentes, otro.componentes))
    
    @staticmethod
    def suma_escalada(lista_vectores, lista_escalars):
        if len(lista_vectores) != len(lista_escalars):
            raise ValueError("La cantidad de vectores debe coincidir con la cantidad de escalares.")
        longitud = len(lista_vectores[0].componentes)
        for vector in lista_vectores:
            if len(vector.componentes) != longitud:
                raise ValueError("Todos los vectores deben tener la misma longitud.")
        suma = [0] * longitud
        for vector, escalar in zip(lista_vectores, lista_escalars):
            suma = [s + (escalar * v) for s, v in zip(suma, vector.componentes)]
        return Vector(suma)
    
    @staticmethod
    def crear_vector_desde_entrada(componentes):
        try:
            componentes_float = [float(x) for x in componentes]
            return Vector(componentes_float)
        except ValueError:
            raise ValueError("Todos los componentes deben ser números.")