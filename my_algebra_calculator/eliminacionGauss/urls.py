from django.urls import path
from .views import main_view, all_gauss_view, op_comb_view, mult_flcl_view

urlpatterns = [
    path('', main_view, name='main'),  # Vista principal
    path('all_gauss/', all_gauss_view, name='all_gauss_view'),  # Vista para Método Escalonado
    path('op_comb/', op_comb_view, name='op_comb_view'),  # Vista para Operaciones Combinadas de Vectores
    path('mult_flcl/', mult_flcl_view, name='mult_flcl_view'),  # Vista para Multiplicación Vector Fila x Columna
]
