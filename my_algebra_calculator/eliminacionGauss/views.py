from django.shortcuts import render
from django.http import JsonResponse
from .models import * #importa todos los modelos Elim_Gauss - Ope_combinadas 
                                        # MltFC_horizontal - MltFC_vertical
from .logic.matriz import Matriz
#Se puede intentar acceder a un objeto que no existe_Se usa un bloque try-except para manejar el DoesNotExist

def main_view(request):
    return render(request, 'main.html')

def all_gauss_view(request):
    if request.method == 'POST':
        # Recoger las filas y columnas desde el formulario
        filas = int(request.POST.get('filas'))
        columnas = int(request.POST.get('columnas'))

        instances_gaussianas = []
        
        # Recoger los valores ingresados por el usuario y crear instancias de Elim_Gauss
        for i in range(1, filas + 1):
            for j in range(1, columnas + 1):
                valor = request.POST.get(f'valor_{i}_{j}')  
                
                if valor:  
                    try:
                        valor_float = float(valor)  
                        
                        # Crear y guardar instancia en la base de datos
                        instance_gaussiana = Elim_Gauss.objects.create(
                            EG_NmEcuaciones=i,
                            EG_NmIncognitas=j,
                            EG_valor=valor_float
                        )
                        instances_gaussianas.append(instance_gaussiana)

                    except ValueError:
                        return JsonResponse({'status': 'error', 'message': 'Valor no válido'})

        # Verifica si hay instancias para evitar errores
        if not instances_gaussianas:
            return JsonResponse({'status': 'error', 'message': 'No se han proporcionado datos válidos.'})

        # Crear una instancia de Matriz usando las instancias recogidas (Asegúrate de implementar esta clase)
        matriz_objeto = Matriz(instances_gaussianas)
        
        # Supongo que esta función ya existe
        resultados_gaussianos = matriz_objeto.eliminacion_gaussiana()

        return JsonResponse({'status': 'success', 'resultados': resultados_gaussianos})  

    return render(request, 'all_Gauss.html')

def op_comb_view(request):
    return render(request, 'Op_comb.html')

def mult_flcl_view(request):
    return render(request, 'mult_FlCl.html')