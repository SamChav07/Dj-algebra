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
            
            return JsonResponse({'status': 'success', 'resultados': {'resultados': resultados}})

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