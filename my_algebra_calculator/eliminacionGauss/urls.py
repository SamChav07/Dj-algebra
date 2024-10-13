from django.urls import path
from .views import *

urlpatterns = [
    path('', main_view, name='main'),  # Vista principal
    path('all_gauss/', escalonar_view, name='escalonar_view'),  # Vista para Método Escalonado
    path('get-existing-ids/', get_existing_ids, name='get_existing_ids'),
    path('escalonar/process/', escalonar_process, name='escalonar_process'),  # Vista para POST
    path('combinarVectores/', combinarVectores_view, name='combinarVectores_view'),  # Vista para Operaciones Combinadas de Vectores
    path('combinarVectores/process/', combinarVectores_process, name='combinarVectores_process'),  # Vista para POST
    path('filaXvector/', filaXvector_view, name='filaXvector_view'),  # Vista para Multiplicación Vector Fila x Columna
]
