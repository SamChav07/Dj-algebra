# eliminacionGauss/views.py

import logging
import json
from django.shortcuts import render
from django.http import JsonResponse
from .models import Elim_Gauss, Ope_combinadas, MultiFxC, PropMxV, SmMrx, TrnsMtx, multMtrX, ClcDeterm, InvMtrx, RglCramer, factLU, biSeccion, nRaphson
from .forms import ElimGaussForm, CombVectorForm, MultiFxCForm, PropMxVForm, SmMrxForm, TrnsMtxForm, MultMtrXForm, ClcDetermForm, InvMtrxForm, RglCramerForm, factLUForm, biSeccionForm, nRaphsonForm
from django.views.decorators.http import require_POST
from .logic.matriz import Matriz
from .logic.vector import Vector
from .logic.matrizxvector import MxV
from .logic.analisis_num import AnNumerico

import numpy as np

# Configure logging
logger = logging.getLogger(__name__)

def main_view(request):
    return render(request, 'main/main.html')

def mainAlgebra_view(request):
    return render(request, 'main/mainAlgebraLineal.html')

def mainNumAnalisis_view(request):
    return render(request, 'main/mainNumericoAnalisis.html')

def aboutU_view(request):
    return render(request, 'services/aboUs.html')

def product_view(request):
    return render(request, 'services/product.html')

#1 Vista para la eliminación de Gauss
def escalonar_view(request):
    form = ElimGaussForm()  
    return render(request, 'algebraLn/escalonar.html', {'form': form})  

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
            if not isinstance(matriz_json, list) or not all(isinstance(i, list) for i in matriz_json):
                raise ValueError("La matriz debe ser una lista de listas.")

            # Create an instance of Matriz directly with the matrix data
            matriz = Matriz(matriz_json)  # No need for the ID now
            resultado = matriz.eliminacion_gaussiana()  # Perform Gaussian elimination

            logger.info("Gaussian elimination completed successfully.")
            return JsonResponse({'status': 'success', 'resultados': resultado})

        except json.JSONDecodeError:
            logger.error("EG_matriz no es un JSON válido.")
            return JsonResponse({'status': 'error', 'message': 'EG_matriz no es un JSON válido.'}, status=400)
        except ValueError as e:
            logger.error(f"Error processing matrix data: {str(e)}")
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)

    # If the form is not valid, return specific errors
    errors = []
    for field, error_list in form.errors.items():
        for error in error_list:
            errors.append(f"{field}: {error}")

    logger.warning("Form validation failed: %s", errors)
    return JsonResponse({'status': 'error', 'message': 'Formulario no válido.', 'errors': errors}, status=400)

#2 Vista_CombinaciondeVectores
def combinarVectores_view(request):
    """Renderiza la plantilla combinarVectores.html con el formulario."""
    form = CombVectorForm()  # Suponiendo que tienes un formulario en Django
    return render(request, 'algebraLn/combinarVectores.html', {'form': form})

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
        resultado_vector, equation = Vector.suma_escalada(lista_vectores, escalares_json)

        ope_combinadas_instance = Ope_combinadas.objects.create(
            OpV_vectores=vectores_json,
            OpV_escalares=escalares_json,
            OpV_resultado=resultado_vector.componentes,
            OpV_ecuaciones=equation  # Use the formatted equation string
        )

        logger.info("Combinación de vectores completada exitosamente.")
        result_str = f"[{', '.join(f'{x:.2f}' for x in resultado_vector.componentes)}]"
        styled_response = f"{equation} = {result_str}"

        return JsonResponse({'status': 'success', 'resultados': resultado_vector.componentes, 'ecuacion': styled_response})

    except (ValueError, json.JSONDecodeError) as e:
        logger.error(f"Error al procesar los datos: {str(e)}")
        return JsonResponse({'status': 'error', 'message': str(e)}, status=400)

#3 vista_filaXvector
def filaXvector_view(request):
    form = MultiFxCForm()
    return render(request, 'algebraLn/filaXvector.html', {'form': form})

def get_existing_idsfXv(request):
    ids = list(MultiFxC.objects.values_list('id', flat=True))
    return JsonResponse({'ids': ids})

@require_POST
def filaXvector_process(request):
    logger.debug(f"Datos POST recibidos: {request.POST}")

    fila_datos = request.POST.get('rowVector')
    columna_datos = request.POST.get('colVector')

    if not fila_datos or not columna_datos:
        logger.error("rowVector o colVector no proporcionados.")
        return JsonResponse({'status': 'error', 'message': 'rowVector o colVector no proporcionados.'}, status=400)

    try:
        fila_json = json.loads(fila_datos)
        columna_json = json.loads(columna_datos)

        if len(fila_json) != len(columna_json):
            raise ValueError("El número de elementos en los vectores de fila y columna debe coincidir.")

        vector_fila = Vector(fila_json)
        vector_columna = Vector(columna_json)

        # Realizar el producto punto
        resultado = vector_fila.producto_punto(vector_columna)

        # Formatear el resultado
        resultado_texto = vector_fila.formato_resultado(vector_columna, resultado)

        # Guardar instancia en la base de datos
        multi_fxc_instance = MultiFxC.objects.create(
            Mfc_Fila=fila_json,
            Mfc_Column=columna_json,
            Mfc_resultado=resultado,
            Mfc_ecuaciones=' + '.join([f"{f} * {c}" for f, c in zip(fila_json, columna_json)])
        )

        logger.info("Multiplicación de vectores completada exitosamente.")
        return JsonResponse({'status': 'success', 'resultados': resultado_texto})

    except (ValueError, json.JSONDecodeError) as e:
        logger.error(f"Error al procesar los datos: {str(e)}")
        return JsonResponse({'status': 'error', 'message': str(e)}, status=400)

def propMxV_view(request):
    form = PropMxVForm()
    return render(request, 'algebraLn/propMxV.html', {'form': form})

def get_existing_ids_pMxV(request):
    ids = list(PropMxV.objects.values_list('id', flat=True))
    return JsonResponse({'ids': ids})

#4 
@require_POST
def propMxV_process(request):
    logger.debug("Datos POST recibidos en propMxV_process: %s", request.POST)

    matrix_data = request.POST.get('pMxV_matrix')
    vectorU_data = request.POST.get('pMxV_vectorU')
    vectorV_data = request.POST.get('pMxV_vectorV')

    if not all([matrix_data, vectorU_data, vectorV_data]):
        logger.error("Datos faltantes: pMxV_matrix, pMxV_vectorU o EG_vectpMxV_vectorVorV no proporcionados.")
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

#5
def smMrx_view(request):
    """Renderiza el formulario para la suma de matrices."""
    form = SmMrxForm()
    return render(request, 'algebraLn/sumaMatrx.html', {'form': form})

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

#6
def trnsMtx_view(request):
    form = TrnsMtxForm()
    return render(request, 'algebraLn/trnsMtrx.html', {'form': form})

# 2. Vista para obtener los IDs existentes
def get_existing_ids_trnsMtx(request):
    """Devuelve una respuesta JSON con los IDs existentes de las operaciones de transposición de matrices."""
    ids = list(TrnsMtx.objects.values_list('id', flat=True))
    return JsonResponse({'ids': ids})

# 3. Vista para procesar la transposición de la matriz
@require_POST
def trnsMtx_process(request):
    # Log de los datos recibidos en POST
    logger.debug(f"Request POST data: {request.POST}")

    # Instancia del formulario con los datos POST
    form = TrnsMtxForm(request.POST)

    # Verificar la presencia de la matriz en los datos POST
    matriz_datos = request.POST.get('trMx_Matriz')
    if not matriz_datos:
        logger.error("trMx_Matriz no proporcionado.")
        return JsonResponse({'status': 'error', 'message': 'trMx_Matriz no proporcionado.'}, status=400)

    if form.is_valid():
        try:
            # Validar y parsear los datos de la matriz
            matriz_json = json.loads(matriz_datos)
            if not isinstance(matriz_json, list) or not all(isinstance(i, list) for i in matriz_json):
                raise ValueError("La matriz debe ser una lista de listas.")

            # Crear la instancia de Matriz y calcular la transposición
            matriz = Matriz(matriz_json)  # Crear la matriz usando los datos JSON
            matriz_transpuesta = matriz.calcular_transpuesta()  # Obtener la matriz transpuesta

            # Guardar la matriz original en el modelo TrnsMtx
            trns_mtx_instance = TrnsMtx.objects.create(
                trMx_Matriz=matriz_json,
                trMx_resultado=matriz_transpuesta  # Guardar el resultado transpuesto
            )

            logger.info("Transposición de la matriz completada exitosamente.")
            return JsonResponse({'status': 'success', 'resultados': matriz_transpuesta})

        except json.JSONDecodeError:
            logger.error("trMx_Matriz no es un JSON válido.")
            return JsonResponse({'status': 'error', 'message': 'trMx_Matriz no es un JSON válido.'}, status=400)
        except ValueError as e:
            logger.error(f"Error al procesar los datos de la matriz: {str(e)}")
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)

    # Si el formulario no es válido, devolver errores específicos
    errors = []
    for field, error_list in form.errors.items():
        for error in error_list:
            errors.append(f"{field}: {error}")

    logger.warning("Falló la validación del formulario: %s", errors)
    return JsonResponse({'status': 'error', 'message': 'Formulario no válido.', 'errors': errors}, status=400)

#7
def multMtrX_view(request):
    form = MultMtrXForm()
    return render(request, 'algebraLn/multMtrX.html', {'form': form})

def get_existing_ids_multMtrX(request):
    """Devuelve los IDs existentes en la tabla MultMtrX."""
    ids = list(MultMtrX.objects.values_list('id', flat=True))
    return JsonResponse({'ids': ids})

@require_POST
def multMtrX_process(request):
    """Procesa la multiplicación de matrices."""
    logger.debug("Datos POST recibidos en multMtrX_process: %s", request.POST)

    matrices_data = request.POST.get('mMrx_Matrx')

    if not matrices_data:
        logger.error("Datos faltantes: mMrx_Matrx no proporcionado.")
        return JsonResponse({'status': 'error', 'message': 'Se requieren los datos de matrices.'}, status=400)

    try:
        matrices_json = json.loads(matrices_data)

        # Validaciones de estructura de datos
        if not isinstance(matrices_json, list) or not all(isinstance(matrix, list) for matrix in matrices_json):
            raise ValueError("El formato de las matrices no es válido.")
        
        if not matrices_json:
            raise ValueError("No se proporcionaron matrices.")

        # Crear instancias de Matriz a partir de los datos recibidos
        matrices = [Matriz(len(matrix), matrix) for matrix in matrices_json]
        resultado = matrices[0]
        pasos = "Proceso de Multiplicación de Matrices:\n\n"

        # Multiplicar matrices en secuencia y documentar el proceso
        for i in range(1, len(matrices)):
            resultado, ecuacion_paso = resultado.multiplicar_por(matrices[i])
            pasos += f"Paso {i}: Resultado parcial después de multiplicar con Matriz {i + 1}\n{ecuacion_paso}\n\n"

        # Guardar resultado y pasos en la base de datos
        mult_mtrx_instance = multMtrX.objects.create(
            mMrx_Matrx=matrices_json,
            mMrx_resultado=resultado.matriz,
            mMrx_ecuaciones=pasos
        )

        logger.info("Procesamiento completado con éxito.")
        return JsonResponse({'status': 'success', 'resultado': resultado.matriz, 'pasos': pasos})

    except (ValueError, json.JSONDecodeError) as e:
        logger.error(f"Error al procesar los datos JSON: {str(e)}")
        return JsonResponse({'status': 'error', 'message': str(e)}, status=400)

#8
def clcDeterm_view(request):
    form = ClcDetermForm()
    return render(request, 'algebraLn/calcDeterminante.html', {'form': form})

# View para obtener los IDs existentes
def get_existing_ids_clcDeterm(request):
    """Devuelve los IDs existentes en la tabla ClcDeterm."""
    ids = list(ClcDeterm.objects.values_list('id', flat=True))
    return JsonResponse({'ids': ids})

# View para procesar el cálculo del determinante
@require_POST
def clcDeterm_process(request):
    """Procesa el cálculo de determinantes."""
    logger.debug("Datos POST recibidos en clc_determ_process: %s", request.POST)

    matrices_data = request.POST.get('cldt_Matrx')

    if not matrices_data:
        logger.error("Datos faltantes: cldt_Matrx no proporcionado.")
        return JsonResponse({'status': 'error', 'message': 'Se requieren los datos de matrices.'}, status=400)

    try:
        matrices_json = json.loads(matrices_data)

        # Validaciones de estructura de datos
        if not isinstance(matrices_json, list) or not all(isinstance(row, list) for row in matrices_json):
            raise ValueError("El formato de la matriz no es válido.")
        
        if not matrices_json:
            raise ValueError("No se proporcionaron matrices.")

        # Crear una instancia de la clase Matriz solo con la matriz
        matriz = Matriz(matrices_json)  # Solo pasamos la matriz como argumento

        # Calcular determinante con pasos detallados
        determinante, pasos = matriz.calcular_determinante(paso_a_paso=True)

        # Guardar resultado y pasos en la base de datos
        clc_determ_instance = ClcDeterm.objects.create(
            cldt_Matrx=matrices_json,
            cldt_resultado=determinante,
            cldt_ecuaciones=pasos
        )

        logger.info("Procesamiento completado con éxito.")
        return JsonResponse({
            'status': 'success',
            'resultado': determinante,
            'pasos': pasos
        })

    except (ValueError, json.JSONDecodeError) as e:
        logger.error(f"Error al procesar los datos JSON: {str(e)}")
        return JsonResponse({'status': 'error', 'message': str(e)}, status=400)

#9
def invMtrx_view(request):
    form = InvMtrxForm()
    return render(request, 'algebraLn/inversaMatriz.html', {'form': form})

# Vista para obtener los IDs existentes de las matrices invertidas
def get_existing_ids_invMtrx(request):
    """Devuelve los IDs existentes en la tabla InvMtrx."""
    ids = list(InvMtrx.objects.values_list('id', flat=True))
    return JsonResponse({'ids': ids})

# Vista para procesar el cálculo de la inversa
@require_POST
def invMtrx_process(request):
    """Procesa el cálculo de la inversa de una matriz."""
    logger.debug("Datos POST recibidos en inv_mtrx_process: %s", request.body)

    try:
        # Parsear los datos JSON recibidos
        data = json.loads(request.body.decode('utf-8'))

        # Obtener la matriz desde el JSON
        matrices_json = data.get('cldt_Matrx', None)

        if not matrices_json:
            logger.error("Datos faltantes: cldt_Matrx no proporcionado.")
            return JsonResponse({'status': 'error', 'message': 'Se requieren los datos de matrices.'}, status=400)

        # Validaciones de estructura de datos
        if not isinstance(matrices_json, list) or not all(isinstance(row, list) for row in matrices_json):
            raise ValueError("El formato de la matriz no es válido.")
        
        if not matrices_json:
            raise ValueError("No se proporcionaron matrices.")

        # Crear una instancia de la clase Matriz solo con la matriz
        matriz = Matriz(matrices_json)  # Solo pasamos la matriz como argumento

        # Calcular la inversa con pasos detallados
        inversa, pasos = matriz.calcular_inversa(paso_a_paso=True)

        # Guardar resultado y pasos en la base de datos
        inv_mtrx_instance = InvMtrx.objects.create(
            inmx_Matrx=matrices_json,
            inmx_resultado=inversa,
            inmx_ecuaciones=pasos
        )

        logger.info("Procesamiento completado con éxito.")
        return JsonResponse({
            'status': 'success',
            'resultado': inversa,
            'pasos': pasos
        })

    except (ValueError, json.JSONDecodeError) as e:
        logger.error(f"Error al procesar los datos JSON: {str(e)}")
        return JsonResponse({'status': 'error', 'message': str(e)}, status=400)

def RglCramer_view(request):
    # Crear una instancia del formulario
    form = RglCramerForm()
    return render(request, 'algebraLn/reglaCramer.html', {'form': form})

def get_existing_ids_RglCramer(request):
    """Devuelve los IDs existentes en la tabla RglCramer."""
    # Obtener los IDs de las matrices ya calculadas
    ids = list(RglCramer.objects.values_list('id', flat=True))
    return JsonResponse({'ids': ids})

@require_POST
def RglCramer_process(request):
    logger.debug(f"Request POST data: {request.POST}")

    form = RglCramerForm(request.POST)

    # Obtener los datos de la matriz desde el POST
    matriz_datos = request.POST.get('cramer_Matrx')
    if not matriz_datos:
        logger.error("cramer_Matrx not provided")
        return JsonResponse({'status': 'error', 'message': 'cramer_Matrx no proporcionado.'}, status=400)

    if form.is_valid():
        try:
            # Cargar los datos JSON de la matriz
            matriz_json = json.loads(matriz_datos)
            # Verificar que la matriz sea una lista de listas
            if not isinstance(matriz_json, list) or not all(isinstance(row, list) for row in matriz_json):
                raise ValueError("La matriz debe ser una lista de listas.")

            # Separar matriz A y vector b
            matriz_a = [row[:-1] for row in matriz_json]  # Todos los elementos excepto el último de cada fila
            resultado = [row[-1] for row in matriz_json]   # Último elemento de cada fila

            # Verificar dimensiones
            if not all(len(row) == len(matriz_a) + 1 for row in matriz_json):
                    raise ValueError("Las dimensiones de la matriz no son válidas. Asegúrate de que sea n x (n+1).")

            # Crear objeto Matriz y resolver con la regla de Cramer
            matriz = Matriz(matriz_a)
            soluciones, pasos_detallados = matriz.cramer(resultado ,paso_a_paso=True)

            logger.info("Cramer operation completed successfully.")

            resultados = {
                'solucion': soluciones,
                'pasos_detallados': pasos_detallados,
            }
            
            return JsonResponse({'status': 'success', 'resultados': resultados})

        except json.JSONDecodeError:
            logger.error("cramer_Matrx no es un JSON válido.")
            return JsonResponse({'status': 'error', 'message': 'cramer_Matrx no es un JSON válido.'}, status=400)
        except ValueError as e:
            logger.error(f"Error processing matrix data: {str(e)}")
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
        except Exception as e:
            logger.error(f"Error Inesperado: {str(e)}")
            return JsonResponse({'status': 'error', 'message': f"Error inesperado: {str(e)}"}, status=500)

    # Manejo de errores de formulario
    errors = []
    for field, error_list in form.errors.items():
        for error in error_list:
            errors.append(f"{field}: {error}")

    logger.warning("Form validation failed: %s", errors)
    return JsonResponse({'status': 'error', 'message': 'Formulario no válido.', 'errors': errors}, status=400)

def factLU_view(request):
    """Renderiza la página con el formulario de factorización LU."""
    form = factLUForm()
    return render(request, 'algebraLn/factorizacionLU.html', {'form': form})

# 2. Vista para obtener los IDs existentes en la tabla factLU
def get_existing_ids_factLU(request):
    """Devuelve los IDs existentes en la tabla factLU."""
    ids = list(factLU.objects.values_list('id', flat=True))
    return JsonResponse({'ids': ids})

@require_POST
def factLU_process(request):
    logger.debug(f"Request POST data: {request.POST}")

    form = factLUForm(request.POST)

    matriz_datos = request.POST.get('lu_mtrx')
    if not matriz_datos:
        logger.error("lu_mtrx not provided")
        return JsonResponse({'status': 'error', 'message': 'lu_mtrx no proporcionado.'}, status=400)

    if form.is_valid():
        try:
            # Convertir datos de matriz de JSON a lista
            matriz_json = json.loads(matriz_datos)
            if not isinstance(matriz_json, list) or not all(isinstance(row, list) for row in matriz_json):
                raise ValueError("La matriz debe ser una lista de listas.")

            # Separar matriz A y vector b
            matriz_a = [row[:-1] for row in matriz_json]  # Todos los elementos excepto el último de cada fila
            vector_b = [row[-1] for row in matriz_json]   # Último elemento de cada fila

            # Validar dimensiones
            if not all(len(row) == len(matriz_a) + 1 for row in matriz_json):
                raise ValueError("Las dimensiones de la matriz no son válidas. Asegúrate de que sea n x (n+1).")

            # Resolver factorización LU
            matriz = Matriz(matriz_a)  # Crear instancia de clase Matriz con A
            L, U, pasos_lu = matriz.factorizacion_lu(paso_a_paso=True)  # Factorización LU con pasos
            solucion, pasos_resolucion = matriz.resolver_lu(vector_b, paso_a_paso=True)  # Resolver Ax = b

            logger.info("LU operation completed successfully.")

            # Preparar respuesta JSON
            resultados = {
                'L': L.matriz,  # Convertir matriz L a lista
                'U': U.matriz,  # Convertir matriz U a lista
                'solucion': solucion,
                'pasos_factorizacion': pasos_lu,
                'pasos_resolucion': pasos_resolucion,
            }
            return JsonResponse({'status': 'success', 'resultados': resultados})

        except json.JSONDecodeError:
            logger.error("lu_mtrx no es un JSON válido.")
            return JsonResponse({'status': 'error', 'message': 'lu_mtrx no es un JSON válido.'}, status=400)
        except ValueError as e:
            logger.error(f"Error processing matrix data: {str(e)}")
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
        except Exception as e:
            logger.error(f"Unexpected error: {str(e)}")
            return JsonResponse({'status': 'error', 'message': f"Error inesperado: {str(e)}"}, status=500)

    # Manejo de errores de formulario
    errors = []
    for field, error_list in form.errors.items():
        for error in error_list:
            errors.append(f"{field}: {error}")

    logger.warning("Form validation failed: %s", errors)
    return JsonResponse({'status': 'error', 'message': 'Formulario no válido.', 'errors': errors}, status=400)

def bi_view(request):
    form = biSeccionForm()
    return render(request, 'analisisNm/biseccion.html',  {'form': form})

def get_existing_ids_bi(request):
    ids = list(biSeccion.objects.values_list('id', flat=True))
    return JsonResponse({'ids': ids})

@require_POST
def biSeccion_process(request):
    logger.debug(f"Request POST data: {request.body.decode('utf-8')}")

    try:
        # Intentar cargar los datos como JSON
        data = json.loads(request.body)

        # Verificar que el JSON contiene las claves necesarias
        bi_funcion_data = data.get("bi_funcion")
        if not bi_funcion_data:
            logger.error("El campo 'bi_funcion' no se encuentra en el cuerpo de la solicitud.")
            return JsonResponse({'status': 'error', 'message': "El campo 'bi_funcion' es obligatorio."}, status=400)

        # Validar que `bi_funcion` contiene `bi_funcion` y `bi_AB`
        bi_funcion_json = json.loads(bi_funcion_data)  # Convertir el string JSON en diccionario
        if "bi_funcion" not in bi_funcion_json or "bi_AB" not in bi_funcion_json:
            logger.error("Faltan claves obligatorias en el JSON de 'bi_funcion'.")
            return JsonResponse({'status': 'error', 'message': "El JSON debe contener 'bi_funcion' y 'bi_AB'."}, status=400)

        # Guardar el dato en el modelo
        registro = biSeccion.objects.create(
            bi_funcion=bi_funcion_json,
            bi_resultado=None  # Inicialmente vacío
        )
        logger.info(f"Registro creado exitosamente con ID: {registro.id}")

        # Procesar los datos con AnNumerico
        an_num = AnNumerico(bi_funcion_json)
        resultado = an_num.run_bisection()

        # Actualizar el resultado en el modelo
        registro.bi_resultado = {"pasos": resultado['iteraciones'], "solucion": resultado['solucion']}
        registro.save()
        logger.info(f"Resultado almacenado para el registro ID: {registro.id}")

        # Responder con los resultados separados
        return JsonResponse({
            'status': 'success',
            'message': f"Registro procesado exitosamente con ID: {registro.id}",
            'resultados': {
                'solucion': resultado['solucion'],
                'iteraciones': resultado['iteraciones']
            }
        })

    except json.JSONDecodeError:
        logger.error("El cuerpo de la solicitud no contiene un JSON válido.")
        return JsonResponse({'status': 'error', 'message': 'Formato JSON inválido en el cuerpo de la solicitud.'}, status=400)
    except ValueError as e:
        logger.error(f"Error en los datos de bi_funcion: {str(e)}")
        return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
    except Exception as e:
        logger.error(f"Error inesperado: {str(e)}")
        return JsonResponse({'status': 'error', 'message': f"Error inesperado: {str(e)}"}, status=500)

def generate_plot_data(request):
    function = request.GET.get('function', '')
    if not function:
        return JsonResponse({'error': 'No se proporcionó ninguna función.'})
    
    try:
        # Generar valores de x e y
        x = np.linspace(-10, 10, 500)  # 500 puntos en el rango [-10, 10]
        y = [eval(function.replace('x', str(value))) for value in x]

        return JsonResponse({
            'x': x.tolist(),
            'y': y,
            'function': function
        })
    except Exception as e:
        return JsonResponse({'error': f'Error al evaluar la función: {str(e)}'})

def newRaphson_view(request):
    form = nRaphsonForm()  
    return render(request, 'analisisNm/newRaphson.html', {'form': form})  