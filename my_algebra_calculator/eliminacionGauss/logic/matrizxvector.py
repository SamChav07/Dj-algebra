from eliminacionGauss.models import PropMxV

class MxV:
    def __init__(self, prop_mxv_id):
        try:
            entrada = PropMxV.objects.get(id=prop_mxv_id)
            self.matriz = entrada.pMxV_matrix
            self.vectores = [entrada.pMxV_vectorU, entrada.pMxV_vectorV]
        except PropMxV.DoesNotExist:
            raise ValueError("No hay entradas en la base de datos para este ID.")
        except Exception as e:
            raise ValueError(f"Error al obtener la matriz y vectores: {str(e)}")

    def sumar_vectores(self):
        if len(self.vectores) != 2:
            raise ValueError("Se requieren exactamente 2 vectores para sumar.")

        u = self.vectores[0]
        v = self.vectores[1]

        return [u[i] + v[i] for i in range(len(u))]

    def multiplicar_matriz_por_vector(self, vector):
        filas = len(self.matriz)
        columnas = len(self.matriz[0])

        if columnas != len(vector):
            raise ValueError("El número de columnas de la matriz debe coincidir con el tamaño del vector")

        resultado = [0] * filas
        for i in range(filas):
            suma = 0
            for j in range(columnas):
                suma += self.matriz[i][j] * vector[j]
            resultado[i] = suma

        return resultado

    def aplicar_propiedad(self):
        if len(self.vectores) != 2:
            raise ValueError("Se requieren exactamente 2 vectores para aplicar la propiedad.")

        u = self.vectores[0]
        v = self.vectores[1]

        Au = self.multiplicar_matriz_por_vector(u)
        Av = self.multiplicar_matriz_por_vector(v)

        u_plus_v = self.sumar_vectores()
        A_u_plus_v = self.multiplicar_matriz_por_vector(u_plus_v)

        return Au, Av, A_u_plus_v

    def formatear_matriz(self, matriz):
        return "\n".join("  ".join(f"{valor:.2f}" for valor in fila) for fila in matriz)

    def formatear_vector(self, vector):
        return "  ".join(f"{valor:.2f}" for valor in vector)

    def formatear_resultado(self):
        Au, Av, A_u_plus_v = self.aplicar_propiedad()
        u, v = self.vectores
        u_plus_v = self.sumar_vectores()
        Au_plus_Av = [Au[i] + Av[i] for i in range(len(Au))]

        # Crear texto detallado de los resultados
        resultado_texto = f"Matriz A:\n{self.formatear_matriz(self.matriz)}\n\n"
        resultado_texto += f"Vector u:\n{self.formatear_vector(u)}\n\n"
        resultado_texto += f"Vector v:\n{self.formatear_vector(v)}\n\n"
        resultado_texto += f"u + v:\n{self.formatear_vector(u_plus_v)}\n\n"

        # Pasos para calcular Au
        resultado_texto += "Pasos para calcular Au:\n"
        for i in range(len(Au)):
            pasos_Au = " + ".join([f"{self.matriz[i][j]}*{u[j]}" for j in range(len(u))])
            resultado_texto += f"A[{i + 1}]u = {pasos_Au} = {Au[i]:.2f}\n"

        # Pasos para calcular Av
        resultado_texto += "\nPasos para calcular Av:\n"
        for i in range(len(Av)):
            pasos_Av = " + ".join([f"{self.matriz[i][j]}*{v[j]}" for j in range(len(v))])
            resultado_texto += f"A[{i + 1}]v = {pasos_Av} = {Av[i]:.2f}\n"

        # Pasos para calcular A(u + v)
        resultado_texto += "\nPasos para calcular A(u + v):\n"
        for i in range(len(A_u_plus_v)):
            pasos_A_u_v = " + ".join([f"{self.matriz[i][j]}*{u_plus_v[j]}" for j in range(len(u_plus_v))])
            resultado_texto += f"A[{i + 1}](u + v) = {pasos_A_u_v} = {A_u_plus_v[i]:.2f}\n"

        # Resultados finales
        resultado_texto += f"\nAu:\n{self.formatear_vector(Au)}\n"
        resultado_texto += f"Av:\n{self.formatear_vector(Av)}\n"
        resultado_texto += f"Au + Av:\n{self.formatear_vector(Au_plus_Av)}\n"
        resultado_texto += f"A(u + v):\n{self.formatear_vector(A_u_plus_v)}\n"

        # Conclusión
        conclusion = "A(U + V) = AU + AV" if A_u_plus_v == Au_plus_Av else "A(U + V) != AU + AV"
        resultado_texto += f"\nConclusión:\n{conclusion}\n"

        return resultado_texto
