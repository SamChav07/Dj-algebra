# eliminacionGauss/models.py

from django.db import models

#Modelo del metodo escalonado
class Elim_Gauss(models.Model):
    EG_matriz = models.JSONField()  #Guarda la matriz completa 
    EG_resultado = models.JSONField(null=True, blank=True)  # Resultado de la eliminación gaussiana
    EG_ecuaciones = models.TextField(null=True, blank=True)  # Guarda los procedimientos
    def __str__(self):
        return f"Elim_Gauss {self.id}"

#Modelo del metodo operaciones combinadas de vectores
class Ope_combinadas(models.Model):
    OpV_vectores = models.JSONField() #vectores
    OpV_escalares = models.JSONField()# Escalares en funcion a n OpV_NmVectores
    OpV_resultado = models.JSONField()
    OpV_ecuaciones = models.TextField()
    def __str__(self):
        return f"Ope_combinadas {self.id}"

#Modelo del metodo multiplicacion vector fila x columna
class MultiFxC(models.Model):
    Mfc_Fila = models.JSONField()  
    Mfc_Column = models.JSONField()
    Mfc_resultado = models.JSONField()
    Mfc_ecuaciones = models.TextField()
    def __str__(self):
        return f"MultiFxC {self.id}"