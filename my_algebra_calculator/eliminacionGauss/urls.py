from django.urls import path
from .views import *

urlpatterns = [
    path('', main_view, name='main'),  # Vista principal
    path('all_gauss/', escalonar_view, name='escalonar_view'),  # Vista para Método Escalonado
    path('get-existing-ids/', get_existing_ids, name='get_existing_ids'),
    path('escalonar/process/', escalonar_process, name='escalonar_process'),  # Vista para POST
    path('combinarVectores/', combinarVectores_view, name='combinarVectores_view'),  # Vista para Operaciones Combinadas de Vectores
    path('get_existing_idsVector/', get_existing_idsVector, name='get_existing_idsVector'),
    path('combinarVectores/process/', combinarVectores_process, name='combinarVectores_process'),  # Vista para POST
    path('filaXvector/', filaXvector_view, name='filaXvector_view'),  # Vista para Multiplicación Vector Fila x Columna
    path('get_existing_idsfXv/', get_existing_idsfXv, name='get_existing_idsfXv'),
    path('filaXvector/process/', filaXvector_process, name='filaXvector_process'),  # Vista para POST
    path('propMxV/', propMxV_view, name='propMxV_view'),  
    path('get_existing_ids_pMxV/', get_existing_ids_pMxV, name='get_existing_ids_pMxV'),
    path('propMxV/process/', propMxV_process, name='propMxV_process'),  # Vista para POST

    path('smMrx/', smMrx_view, name='smMrx_view'),  
    path('get_existing_ids_smMrx/', get_existing_ids_smMrx, name='get_existing_ids_smMrx'),
    path('smMrx/process/', smMrx_process, name='smMrx_process'),  # Vista para POST
]