# eliminacionGauss/views.py

import logging
import json
from django.shortcuts import render
from django.http import JsonResponse
from .models import Elim_Gauss, Ope_combinadas, MultiFxC, PropMxV, SmMrx
from .forms import ElimGaussForm, CombVectorForm, MultiFxCForm, PropMxVForm, SmMrxForm
from django.views.decorators.http import require_POST
from .logic.matriz import Matriz
from .logic.vector import Vector
from .logic.matrizxvector import MxV

# Configure logging
logger = logging.getLogger(__name__)

def main_view(request):
    return render(request, 'main.html')

# Vista para la eliminación de Gauss
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

    # Check for EG_matriz presence
    matriz_datos = request.POST.get('EG_matriz')
    if not matriz_datos:
        logger.error("EG_matriz not provided.")
        return JsonResponse({'status': 'error', 'message': 'EG_matriz no proporcionado.'}, status=400)

    # Create a form instance with the POST data
    form = ElimGaussForm(request.POST)

    if form.is_valid():
        try:
            # Validate and parse the matrix data
            matriz_json = json.loads(matriz_datos)

            # Ensure matriz_json is a list of lists (matrix structure)
            if not isinstance(matriz_json, list) or not all(isinstance(row, list) for row in matriz_json):
                raise ValueError("La matriz debe ser una lista de listas.")

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
    errors = [f"{field}: {error}" for field, error_list in form.errors.items() for error in error_list]

    logger.warning("Form validation failed: %s", errors)
    return JsonResponse({'status': 'error', 'message': 'Formulario no válido.', 'errors': errors}, status=400)

#vista_CombinaciondeVectores
def combinarVectores_view(request):
    """Renderiza la plantilla combinarVectores.html con el formulario."""
    form = CombVectorForm()  # Suponiendo que tienes un formulario en Django
    return render(request, 'combinarVectores.html', {'form': form})

def get_existing_idsVector(request):
    """Devuelve una respuesta JSON con los IDs existentes de las operaciones de vectores."""
    ids = list(Ope_combinadas.objects.values_list('id', flat=True))
    return JsonResponse({'ids': ids})

@require_POST
def combinarVectores_process(request):
    logger.debug(f"Datos POST recibidos: {request.POST}")
    vectores_datos = request.POST.get('OpV_vectores')
    escalares_datos = request.POST.get('OpV_escalares')

    if not vectores_datos or not escalares_datos:
        logger.error("OpV_vectores o OpV_escalares no proporcionados.")
        return JsonResponse({'status': 'error', 'message': 'OpV_vectores o OpV_escalares no proporcionados.'}, status=400)

    try:
        vectores_json = json.loads(vectores_datos)
        escalares_json = json.loads(escalares_datos)

        if len(vectores_json) != len(escalares_json):
            raise ValueError("La cantidad de vectores debe coincidir con la cantidad de escalares.")

        lista_vectores = [Vector(vector) for vector in vectores_json]
        resultado_vector = Vector.suma_escalada(lista_vectores, escalares_json)

        ope_combinadas_instance = Ope_combinadas.objects.create(
            OpV_vectores=vectores_json,
            OpV_escalares=escalares_json,
            OpV_resultado=resultado_vector.componentes,
            OpV_ecuaciones=' + '.join([f"{escalar} * {vector}" for escalar, vector in zip(escalares_json, vectores_json)])
        )

        logger.info("Combinación de vectores completada exitosamente.")
        return JsonResponse({'status': 'success', 'resultados': resultado_vector.componentes})

    except (ValueError, json.JSONDecodeError) as e:
        logger.error(f"Error al procesar los datos: {str(e)}")
        return JsonResponse({'status': 'error', 'message': str(e)}, status=400)

#vista_filaXvector
def filaXvector_view(request):
    form = MultiFxCForm()
    return render(request, 'filaXvector.html', {'form': form})

def get_existing_idsfXv(request):
    ids = list(MultiFxC.objects.values_list('id', flat=True))
    return JsonResponse({'ids': ids})

@require_POST
def filaXvector_process(request):
    logger.debug(f"Datos POST recibidos: {request.POST}")

    fila_datos = request.POST.get('Mfc_Fila')
    columna_datos = request.POST.get('Mfc_Column')

    if not fila_datos or not columna_datos:
        logger.error("Mfc_Fila o Mfc_Column no proporcionados.")
        return JsonResponse({'status': 'error', 'message': 'Mfc_Fila o Mfc_Column no proporcionados.'}, status=400)

    try:
        fila_json = json.loads(fila_datos)
        columna_json = json.loads(columna_datos)

        if len(fila_json) != len(columna_json):
            raise ValueError("El número de elementos en los vectores de fila y columna debe coincidir.")

        vector_fila = Vector(fila_json)
        vector_columna = Vector(columna_json)

        resultado = vector_fila.multiplicar_por_vector(vector_columna)

        # Crear instancia en la base de datos
        multi_fxc_instance = MultiFxC.objects.create(
            Mfc_Fila=fila_json,
            Mfc_Column=columna_json,
            Mfc_resultado=resultado.componentes,
            Mfc_ecuaciones=' * '.join([f"{f} * {c}" for f, c in zip(fila_json, columna_json)])
        )

        logger.info("Multiplicación de vectores completada exitosamente.")
        return JsonResponse({'status': 'success', 'resultados': resultado.componentes})

    except (ValueError, json.JSONDecodeError) as e:
        logger.error(f"Error al procesar los datos: {str(e)}")
        return JsonResponse({'status': 'error', 'message': str(e)}, status=400)

def propMxV_view(request):
    form = PropMxVForm()
    return render(request, 'propMxV.html', {'form': form})

def get_existing_ids_pMxV(request):
    ids = list(PropMxV.objects.values_list('id', flat=True))
    return JsonResponse({'ids': ids})

@require_POST
def propMxV_process(request):
    logger.debug("Datos POST recibidos en propMxV_process: %s", request.POST)

    matrix_data = request.POST.get('EG_matriz')
    vectorU_data = request.POST.get('EG_vectorU')
    vectorV_data = request.POST.get('EG_vectorV')

    if not all([matrix_data, vectorU_data, vectorV_data]):
        logger.error("Datos faltantes: EG_matriz, EG_vectorU o EG_vectorV no proporcionados.")
        return JsonResponse({'status': 'error', 'message': 'Se requieren todos los campos: matriz, vector U y vector V.'}, status=400)

    try:
        matrix_json = json.loads(matrix_data)
        vectorU_json = json.loads(vectorU_data)
        vectorV_json = json.loads(vectorV_data)

        # Validar dimensiones
        # Asegurarse de que la cantidad de columnas de la matriz coincide con la longitud de los vectores
        num_columnas = len(matrix_json[0]) if matrix_json else 0  # Obtener la cantidad de columnas de la matriz

        if len(vectorU_json) != num_columnas:
            return JsonResponse({'status': 'error', 'message': f'El tamaño del vector U debe coincidir con la cantidad de columnas de la matriz ({num_columnas}).'}, status=400)
        
        if len(vectorV_json) != num_columnas:
            return JsonResponse({'status': 'error', 'message': f'El tamaño del vector V debe coincidir con la cantidad de columnas de la matriz ({num_columnas}).'}, status=400)

        # Crear instancia del modelo PropMxV
        prop_mxv_instance = PropMxV.objects.create(
            pMxV_matrix=matrix_json,
            pMxV_vectorU=vectorU_json,
            pMxV_vectorV=vectorV_json
        )

        # Procesar matriz y vectores usando MxV
        mxv = MxV(prop_mxv_instance.id)
        resultado_texto = mxv.formatear_resultado()

        # Guardar resultado en la instancia del modelo
        prop_mxv_instance.pMxV_resultado = resultado_texto
        prop_mxv_instance.save()

        logger.info("Procesamiento completado.")
        return JsonResponse({'status': 'success', 'resultado': resultado_texto})

    except (ValueError, json.JSONDecodeError) as e:
        logger.error(f"Error al procesar los datos JSON: {str(e)}")
        return JsonResponse({'status': 'error', 'message': str(e)}, status=400)

def smMrx_view(request):
    """Renderiza el formulario para la suma de matrices."""
    form = SmMrxForm()
    return render(request, 'sumaMatrx.html', {'form': form})

def get_existing_ids_smMrx(request):
    """Devuelve los IDs existentes en la tabla SmMrx."""
    ids = list(SmMrx.objects.values_list('id', flat=True))
    return JsonResponse({'ids': ids})

@require_POST
def smMrx_process(request):
    logger.debug("Datos POST recibidos en smMrx_process: %s", request.POST)

    matrices_data = request.POST.get('sMrx_matrxS')
    escalares_data = request.POST.get('sMrx_escalares')

    if not matrices_data or not escalares_data:
        logger.error("Datos faltantes: sMrx_matrxS o sMrx_escalares no proporcionados.")
        return JsonResponse({'status': 'error', 'message': 'Se requieren todos los campos: matrices y escalares.'}, status=400)

    try:
        matrices_json = json.loads(matrices_data)
        escalares_json = json.loads(escalares_data)

        logger.debug("Matrices recibidas: %s", matrices_json)
        logger.debug("Escalares recibidos: %s", escalares_json)

        if not isinstance(matrices_json, list) or not all(isinstance(matrix, list) for matrix in matrices_json):
            raise ValueError("El formato de las matrices no es válido.")

        if not isinstance(escalares_json, list):
            raise ValueError("El formato de los escalares no es válido.")

        if not matrices_json:
            raise ValueError("No se proporcionaron matrices.")

        num_filas = len(matrices_json)
        num_columnas = len(matrices_json[0]) if num_filas > 0 else 0

        for matrix in matrices_json:
            if len(matrix) != num_columnas:
                raise ValueError("Todas las matrices deben tener el mismo número de columnas.")

        if len(escalares_json) != num_filas:
            raise ValueError("El número de escalares debe coincidir con el número de matrices.")

        sm_mrx_instance = SmMrx.objects.create(
            sMrx_matrxS=matrices_json,
            sMrx_escalares=escalares_json
        )

        logger.debug("Instancia creada: %s", sm_mrx_instance)

        matriz_instance = Matriz(sm_mrx_instance.id)
        resultado_texto = matriz_instance.suma_matrices()

        sm_mrx_instance.sMrx_resultado = resultado_texto
        sm_mrx_instance.save()

        logger.info("Procesamiento completado.")
        return JsonResponse({'status': 'success', 'resultado': resultado_texto})

    except (ValueError, json.JSONDecodeError) as e:
        logger.error(f"Error al procesar los datos JSON: {str(e)}")
        return JsonResponse({'status': 'error', 'message': str(e)}, status=400)