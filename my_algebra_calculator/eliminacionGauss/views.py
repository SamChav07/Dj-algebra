# eliminacionGauss/views.py

import logging
from django.shortcuts import render
from django.http import JsonResponse
from .models import *
from .forms import ElimGaussForm
from django.views.decorators.http import require_POST
import json
from .logic.matriz import Matriz  

# Configure logging
logger = logging.getLogger(__name__)

def main_view(request):
    return render(request, 'main.html')

def all_gauss_view(request):
    form = ElimGaussForm()  
    return render(request, 'all_Gauss.html', {'form': form})  

def get_existing_ids(request):
    ids = list(Elim_Gauss.objects.values_list('EG_tabla_id', flat=True))
    return JsonResponse({'ids': ids})

@require_POST
def all_gauss_process(request):
    # Log incoming POST data
    logger.debug(f"Request POST data: {request.POST}")

    # Retrieve EG_tabla_id from the POST data
    eg_table_id = request.POST.get('EG_tabla_id')
    
    # Check if EG_tabla_id is provided
    if not eg_table_id:
        logger.error("EG_tabla_id not provided.")
        return JsonResponse({'status': 'error', 'message': 'EG_tabla_id no proporcionado.'}, status=400)

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
                EG_tabla_id=eg_table_id,
            )

            # Call the Matriz class and perform Gaussian elimination
            matriz = Matriz(eg_table_id)
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

def op_comb_view(request):
    return render(request, 'Op_comb.html')

def mult_flcl_view(request):
    return render(request, 'mult_FlCl.html')