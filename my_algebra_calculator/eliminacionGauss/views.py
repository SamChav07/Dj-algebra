# eliminacionGauss/views.py

from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from .models import Elim_Gauss
from .forms import ElimGaussForm  # Asegúrate de importar tu formulario correctamente
import json

def main_view(request):
    return render(request, 'main.html')

@require_POST  # Asegura que solo se acepten solicitudes POST para esta vista
def all_gauss_view(request):
    form = ElimGaussForm(request.POST)  # Utiliza el formulario para manejar los datos

    if form.is_valid():
        matriz_datos = form.cleaned_data['EG_matriz']  # Obtiene los datos limpios del formulario
        eg_table_id = form.cleaned_data['EG_tabla_id']

        try:
            # Guardar la matriz completa en la tabla Elim_Gauss
            elim_gauss_instance = Elim_Gauss.objects.create(
                EG_matriz=json.loads(matriz_datos),  # Asegúrate de que los datos sean válidos JSON
                EG_tabla_id=eg_table_id,
            )

            # Realizar la eliminación gaussiana utilizando la matriz almacenada
            resultado = eliminacion_gaussiana(elim_gauss_instance.EG_matriz)

            # Actualiza el resultado en la base de datos
            elim_gauss_instance.EG_resultado = resultado
            elim_gauss_instance.save()

            return render(request, 'all_Gauss.html', {'resultado': resultado})

        except (ValueError, json.JSONDecodeError) as e:
            return render(request, 'error.html', {'error': str(e)})

    return render(request, 'all_Gauss.html', {'form': form})

def op_comb_view(request):
    return render(request, 'Op_comb.html')

def mult_flcl_view(request):
    return render(request, 'mult_FlCl.html')