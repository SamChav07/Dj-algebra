from django.urls import path
from .views import *

urlpatterns = [
    path('', main_view, name='main'),  # Vista principal
    #1
    path('all_gauss/', escalonar_view, name='escalonar_view'),  # Vista para Método Escalonado
    path('get-existing-ids/', get_existing_ids, name='get_existing_ids'),
    path('escalonar/process/', escalonar_process, name='escalonar_process'),  # Vista para POST
    #2
    path('combinarVectores/', combinarVectores_view, name='combinarVectores_view'),  # Vista para Operaciones Combinadas de Vectores
    path('get_existing_idsVector/', get_existing_idsVector, name='get_existing_idsVector'),
    path('combinarVectores/process/', combinarVectores_process, name='combinarVectores_process'),  # Vista para POST
    #3
    path('filaXvector/', filaXvector_view, name='filaXvector_view'),  # Vista para Multiplicación Vector Fila x Columna
    path('get_existing_idsfXv/', get_existing_idsfXv, name='get_existing_idsfXv'),
    path('filaXvector/process/', filaXvector_process, name='filaXvector_process'),  # Vista para POST
    #4
    path('propMxV/', propMxV_view, name='propMxV_view'),  
    path('get_existing_ids_pMxV/', get_existing_ids_pMxV, name='get_existing_ids_pMxV'),
    path('propMxV/process/', propMxV_process, name='propMxV_process'),  # Vista para POST
    #5
    path('smMrx/', smMrx_view, name='smMrx_view'),  
    path('get_existing_ids_smMrx/', get_existing_ids_smMrx, name='get_existing_ids_smMrx'),
    path('smMrx/process/', smMrx_process, name='smMrx_process'),  # Vista para POST
    #6
    path('trnsMtx/', trnsMtx_view, name='trnsMtx_view'),  # Vista para cargar el formulario de transposición
    path('get_existing_ids_trnsMtx/', get_existing_ids_trnsMtx, name='get_existing_ids_trnsMtx'),  # Vista para obtener los IDs existentes
    path('trnsMtx/process/', trnsMtx_process, name='trnsMtx_process'),  # Vista para procesar la transposición de la matriz
    #7
    path('multMtrX/', multMtrX_view, name='multMtrX_view'),  # Vista para cargar el formulario de transposición
    path('get_existing_ids_multMtrX/', get_existing_ids_multMtrX, name='get_existing_ids_multMtrX'),  # Vista para obtener los IDs existentes
    path('multMtrX/process/', multMtrX_process, name='multMtrX_process'),  # Vista para procesar la transposición de la matriz
]