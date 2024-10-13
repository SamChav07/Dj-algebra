# eliminacionGauss/views.py

import logging
from django.shortcuts import render
from django.http import JsonResponse
from .models import *
from .forms import *
from django.views.decorators.http import require_POST
import json
from .logic import *

# Configure logging
logger = logging.getLogger(__name__)

def main_view(request):
    return render(request, 'main.html')

def escalonar_view(request):
    form = ElimGaussForm()  
    return render(request, 'escalonar.html', {'form': form})  

def get_existing_ids(request):
    ids = list(Elim_Gauss.objects.values_list('id', flat=True))
    return JsonResponse({'ids': ids})

@require_POST
def escalonar_process(request):
    # Log incoming POST data
    logger.debug(f"Request POST data: {request.POST}")

    # Create a form instance with the POST data
    form = ElimGaussForm(request.POST)

    # Check for EG_matriz presence
    matriz_datos = request.POST.get('EG_matriz')
    if not matriz_datos:
        logger.error("EG_matriz not provided.")
        return JsonResponse({'status': 'error', 'message': 'EG_matriz no proporcionado.'}, status=400)

    if form.is_valid():
        try:
            # Validate and parse the matrix data
            matriz_json = json.loads(matriz_datos)
            if not isinstance(matriz_json, list):
                raise ValueError("La matriz debe ser una lista.")

            # Save the matrix in the Elim_Gauss table
            elim_gauss_instance = Elim_Gauss.objects.create(
                EG_matriz=matriz_json,
            )

            # Call the Matriz class and perform Gaussian elimination using the id
            matriz = Matriz(elim_gauss_instance.id)  # Use the newly created instance's id
            resultado = matriz.eliminacion_gaussiana()

            # Update the result in the database
            elim_gauss_instance.EG_resultado = resultado
            elim_gauss_instance.save()

            logger.info("Gaussian elimination completed successfully.")
            return JsonResponse({'status': 'success', 'resultados': resultado})

        except (ValueError, json.JSONDecodeError) as e:
            logger.error(f"Error processing matrix data: {str(e)}")
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)

    # If the form is not valid, return specific errors
    errors = []
    for field, error_list in form.errors.items():
        for error in error_list:
            errors.append(f"{field}: {error}")

    logger.warning("Form validation failed: %s", errors)
    return JsonResponse({'status': 'error', 'message': 'Formulario no válido.', 'errors': errors}, status=400)

def combinarVectores_view(request):
    form = CombVectorForm()
    return render(request, 'combinarVectores.html', {'form': form})

def get_existing_idsVector(request):
    ids = list(Ope_combinadas.objects.values_list('id', flat=True))
    return JsonResponse({'ids': ids})

@require_POST
def combinarVectores_process(request):
    logger.debug(f"Request POST data: {request.POST}")

    vectores_datos = request.POST.get('OpV_vectores')
    escalares_datos = request.POST.get('OpV_escalares')

    # Verificar si se proporcionaron los datos de vectores y escalares
    if not vectores_datos or not escalares_datos:
        logger.error("OpV_vectores or OpV_escalares not provided.")
        return JsonResponse({'status': 'error', 'message': 'OpV_vectores o OpV_escalares no proporcionados.'}, status=400)

    try:
        # Cargar datos de JSON
        vectores_json = json.loads(vectores_datos)
        escalares_json = json.loads(escalares_datos)

        # Crear instancias de Vector
        vectores = [Vector(vector) for vector in vectores_json]
        escalares = [float(escalar) for escalar in escalares_json]

        # Validar que la cantidad de vectores y escalares coincida
        if len(vectores) != len(escalares):
            raise ValueError("La cantidad de vectores debe coincidir con la cantidad de escalares.")

        # Validar que todos los vectores tengan la misma longitud
        longitud = len(vectores[0].componentes)
        for vector in vectores:
            if len(vector.componentes) != longitud:
                raise ValueError("Todos los vectores deben tener la misma longitud.")

        # Realizar operaciones con los vectores
        resultado_vector = Vector.suma_escalada(vectores, escalares)

        # Crear y guardar una instancia de Ope_combinadas
        ope_combinadas_instance = Ope_combinadas.objects.create(
            OpV_vectores=vectores_json,
            OpV_escalares=escalares_json,
            OpV_resultado=resultado_vector.componentes,  # Guarda el resultado de la operación
            OpV_ecuaciones=' '.join([f"{escalar} * {vector}" for escalar, vector in zip(escalares, vectores)])  # Crear la ecuación
        )

        logger.info("Combinación de vectores completada exitosamente.")
        return JsonResponse({'status': 'success', 'resultados': resultado_vector.componentes})

    except (ValueError, json.JSONDecodeError) as e:
        logger.error(f"Error procesando datos: {str(e)}")
        return JsonResponse({'status': 'error', 'message': str(e)}, status=400)

def filaXvector_view(request):
    return render(request, 'filaXvector.html')