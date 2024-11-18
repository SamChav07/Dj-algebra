@require_POST
def RglCramer_process(request):
    logger.debug(f"Request POST data: {request.POST}")

    # Obtener los datos de la matriz desde el POST
    matriz_datos = request.POST.get('cramer_Matrx')

    if not matriz_datos:
        logger.error("cramer_Matrx not provided")
        return JsonResponse({'status': 'error', 'message': 'cramer_Matrx no proporcionado.'}, status=400)

    try:
        # Cargar los datos JSON de la matriz
        matriz_json = json.loads(matriz_datos)

        # Verificar que la matriz sea una lista de listas
        if not isinstance(matriz_json, list) or not all(isinstance(row, list) for row in matriz_json):
            raise ValueError("La matriz debe ser una lista de listas.")

        if not matriz_json:
            raise ValueError("No se proporcionaron matrices.")

        matriz = Matriz(matriz_json)

        soluciones, pasos_detallados = matriz.cramer(paso_a_paso=True)

        cramer_instance = RglCramer.objects.create(
            cramer_Matrx = matriz_json,
            cramer_resultado = soluciones,
            cramer_ecuaciones = pasos_detallados
        )

        logger.info("Cramer operation completed successfully.")
        
        return JsonResponse({'status': 'success', 'resultados': {'resultados': resultados}})

    except (ValueError, json.JSONDecodeError) as e:
        logger.error(f"Error al procesar los datos JSON: {str(e)}")
        return JsonResponse({'status': 'error', 'message': str(e)}, status=400)