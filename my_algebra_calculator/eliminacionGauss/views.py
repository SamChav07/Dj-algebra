from django.shortcuts import render
from django.http import JsonResponse
from eliminacionGauss.models import * #importa todos los modelos Elim_Gauss - Ope_combinadas 
                                        # MltFC_horizontal - MltFC_vertical
from eliminacionGauss.logic.matriz import Matriz
from eliminacionGauss.forms import MatrixForm
#Se puede intentar acceder a un objeto que no existe_Se usa un bloque try-except para manejar el DoesNotExist

def main_view(request):
    return render(request, 'main.html')

def resolver_matriz_view(request):
    if request.method == 'POST':
        # Supongamos que recibes la matriz desde un formulario o desde otro proceso
        matriz_datos = request.POST.get('matriz')  # Esto puede variar según cómo obtienes los datos
        eg_table_id = request.POST.get('eg_table_id')

        # Guardar cada valor en la tabla Elim_Gauss
        for fila_idx, fila in enumerate(matriz_datos):
            for col_idx, valor in enumerate(fila):
                Elim_Gauss.objects.create(
                    EG_tabla_id=eg_table_id,
                    EG_fila=fila_idx + 1,  # Ajustar a índice base 1
                    EG_columna=col_idx + 1,
                    EG_valor=valor
                )

        # Luego de guardar, llamamos a la clase Matriz para resolver el sistema
        try:
            matriz = Matriz(eg_table_id)  # Crea la instancia con el ID de la tabla
            resultado = matriz.eliminacion_gaussiana()  # Resuelve la matriz
            return render(request, 'all_Gauss.html', {'resultado': resultado})

        except ValueError as e:
            # Si hay un error, mostramos un mensaje
            return render(request, 'error.html', {'error': str(e)})

    # Si no es una petición POST, redirige a otro lado
    return render(request, 'all_Gauss.html', {'form': form})

def op_comb_view(request):
    return render(request, 'Op_comb.html')

def mult_flcl_view(request):
    return render(request, 'mult_FlCl.html')