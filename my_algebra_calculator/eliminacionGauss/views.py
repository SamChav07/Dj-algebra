# eliminacionGauss/views.py

from django.shortcuts import render
from django.http import JsonResponse
from .models import Elim_Gauss
from .forms import ElimGaussForm
from django.views.decorators.http import require_POST
import json
from .logic.matriz import Matriz  # Importa la clase Matriz desde logica/matriz.py

def main_view(request):
    return render(request, 'main.html')

def all_gauss_view(request):
    form = ElimGaussForm()  # Crear un nuevo formulario
    return render(request, 'all_Gauss.html', {'form': form})  # Renderizar la plantilla con el formulario

@require_POST
def all_gauss_process(request):
    form = ElimGaussForm(request.POST)  # Utiliza el formulario para manejar los datos

    if form.is_valid():
        eg_table_id = form.cleaned_data['EG_tabla_id']
        matriz_datos = form.cleaned_data['EG_matriz']  # Obtiene los datos limpios del formulario

        try:
            # Guardar la matriz completa en la tabla Elim_Gauss
            elim_gauss_instance = Elim_Gauss.objects.create(
                EG_matriz=json.loads(matriz_datos),  # Asegúrate de que los datos sean válidos JSON
                EG_tabla_id=eg_table_id,
            )

            # Llamar a la clase Matriz y realizar la eliminación gaussiana
            matriz = Matriz(eg_table_id)  # Inicializa la clase con el ID de la tabla
            resultado = matriz.eliminacion_gaussiana()  # Realiza la eliminación gaussiana

            # Actualiza el resultado en la base de datos
            elim_gauss_instance.EG_resultado = resultado
            elim_gauss_instance.save()

            return JsonResponse({'status': 'success', 'resultados': resultado})

        except (ValueError, json.JSONDecodeError) as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)

 