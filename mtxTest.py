# eliminacionGauss/logic/matriz.py

from eliminacionGauss.models import Elim_Gauss

class Matriz:
    """
    Clase que representa una matriz y permite realizar eliminación Gaussiana.
    """

    def __init__(self, matriz):
        # Validar si la matriz es None
        if matriz is None:
            raise ValueError("La matriz no puede ser None.")

        # Validar si la matriz es una lista de listas
        if isinstance(matriz, list) and all(isinstance(i, list) for i in matriz):
            self.matriz = matriz
        
        # Validar si la matriz tiene el formato del método Cramer
        elif isinstance(matriz, dict) and 'cramer_Matrx' in matriz and 'cramer_TermsIndp' in matriz:
            # Extraer la matriz y los términos independientes del diccionario
            matriz_base = matriz['cramer_Matrx']
            terminos_independientes = matriz['cramer_TermsIndp']

            # Validar dimensiones
            if len(matriz_base) != len(terminos_independientes):
                raise ValueError("La cantidad de filas en la matriz debe coincidir con la cantidad de términos independientes.")

            # Construir la matriz ampliada
            self.matriz = [fila + [terminos_independientes[i]] for i, fila in enumerate(matriz_base)]
        
        else:
            raise ValueError("Formato de matriz no reconocido. Debe ser una lista de listas o un diccionario con 'cramer_Matrx' y 'cramer_TermsIndp'.")

    def obtener_matriz(self, entradas):
        """
        Convierte las entradas en formato de lista de listas a una matriz de números flotantes.
        :param entradas: lista de listas con los coeficientes de las ecuaciones.
        :return: matriz convertida a tipo flotante.
        :raises ValueError: Si alguna entrada no puede ser convertida.
        """
        if self.matriz is None:
            raise ValueError("La matriz no puede ser None.")
        return self.matriz

        def factorizacion_lu(self, paso_a_paso=False):
        """
        Realiza la factorización LU de la matriz A (sin pivoteo) mostrando los pasos de manera visual y detallada.
        :param paso_a_paso: si es True, muestra los pasos de la factorización.
        :return: tupla con matrices L y U, y los pasos si paso_a_paso es True.
        """
        n = len(self.matriz)
        L = [[0.0] * n for _ in range(n)]  # Inicializar L como matriz de ceros
        U = [fila[:] for fila in self.matriz]  # Inicializar U como copia de A
        pasos = "" if paso_a_paso else None

        # Función local para formatear matrices en formato de tabla visual
        def formatear_matriz_visual(matriz, nombre_matriz):
            """Formatea una matriz en un string visualmente claro."""
            texto = f"{nombre_matriz} =\n"
            for fila in matriz:
                texto += "| " + "  ".join(f"{valor:.2f}" for valor in fila) + " |\n"
            return texto

        if paso_a_paso:
            pasos += "---- Inicio de la Factorización LU ----\n"
            pasos += formatear_matriz_visual(self.matriz, "A (Matriz original)") + "\n"

        for i in range(n):
            L[i][i] = 1.0  # La diagonal de L es 1

            for j in range(i + 1, n):
                if abs(U[i][i]) < 1e-10:
                    raise ValueError("La factorización LU requiere que los elementos diagonales no sean cero.")

                # Calcular el factor que multiplicará la fila de U
                factor = U[j][i] / U[i][i]
                L[j][i] = factor

                if paso_a_paso:
                    pasos += f"Paso {i + 1}.{j + 1}: Calculamos el factor L[{j + 1}][{i + 1}] = {factor:.2f}\n"

                # Actualizar la fila de U restando el múltiplo correspondiente de la fila pivote
                for k in range(i, n):
                    U[j][k] -= factor * U[i][k]

                if paso_a_paso:
                    pasos += "\nActualizando L y U:\n"
                    pasos += formatear_matriz_visual(L, "L") + "\n"
                    pasos += formatear_matriz_visual(U, "U") + "\n"
                    pasos += "-" * 30 + "\n"  # Separador visual

        return (Matriz(n, L), Matriz(n, U), pasos) if paso_a_paso else (Matriz(n, L), Matriz(n, U))
    
    def resolver_lu(self, b, paso_a_paso=False):
        """
        Resuelve el sistema Ax = b utilizando la factorización LU, mostrando los pasos de manera visual.
        :param b: vector de términos independientes.
        :param paso_a_paso: si es True, muestra los pasos de la resolución.
        :return: solución del sistema.
        """
        n = len(self.matriz)
        L, U, pasos_lu = self.factorizacion_lu(paso_a_paso=True)  # Factorización LU

        # Resolver Ly = b usando sustitución hacia adelante
        y = [0.0] * n
        if paso_a_paso:
            pasos_lu += "\n---- Resolviendo Ly = b ----\n"

        for i in range(n):
            suma = sum(L.matriz[i][j] * y[j] for j in range(i))
            y[i] = (b[i] - suma) / L.matriz[i][i]

            # Descripción visual de cada paso
            if paso_a_paso:
                pasos_lu += f"y[{i + 1}] = (b[{i + 1}] - sum(L[{i + 1}][1..{i}]*y[1..{i}])) / L[{i + 1}][{i + 1}]\n"
                pasos_lu += f"y[{i + 1}] = ({b[i]:.2f} - {suma:.2f}) / {L.matriz[i][i]:.2f} = {y[i]:.2f}\n"

        # Resolver Ux = y usando sustitución hacia atrás
        x = [0.0] * n
        if paso_a_paso:
            pasos_lu += "\n---- Resolviendo Ux = y ----\n"

        for i in range(n - 1, -1, -1):
            suma = sum(U.matriz[i][j] * x[j] for j in range(i + 1, n))
            x[i] = (y[i] - suma) / U.matriz[i][i]

            # Descripción visual de cada paso
            if paso_a_paso:
                pasos_lu += f"x[{i + 1}] = (y[{i + 1}] - sum(U[{i + 1}][{i + 2}..{n}]*x[{i + 2}..{n}])) / U[{i + 1}][{i + 1}]\n"
                pasos_lu += f"x[{i + 1}] = ({y[i]:.2f} - {suma:.2f}) / {U.matriz[i][i]:.2f} = {x[i]:.2f}\n"

        return (x, pasos_lu) if paso_a_paso else x