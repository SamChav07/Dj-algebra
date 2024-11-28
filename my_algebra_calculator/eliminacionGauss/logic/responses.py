from .logic.vector import Vector

class Responses:
    def __init__(self, vectores_json, escalares_json):
        self.vectores = [Vector(vector) for vector in vectores_json]
        self.escalars = escalares_json

    def opeCombinadas(self):
        # Calculate the scaled sum of vectors
        resultado = Vector.suma_escalada(self.lista_vectores, self.lista_escalars)

        # Format operation details
        operation_steps = []
        for escalar, vector in zip(self.lista_escalars, self.lista_vectores):
            formatted_vector = f"[{', '.join(map(str, vector.componentes))}]"
            operation_steps.append(f"{escalar} * {formatted_vector}")

        # Construct equation and result in a readable format
        equation = " + ".join(operation_steps)
        result_str = f"[{', '.join(f'{x:.2f}' for x in resultado.componentes)}]"
        styled_response = f"{equation} = {result_str}"
        
        # Return styled response for display in the view
        return styled_response, resultado.componentes
