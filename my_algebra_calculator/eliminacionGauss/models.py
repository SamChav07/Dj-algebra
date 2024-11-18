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
    OpV_resultado = models.JSONField(null=True, blank=True)
    OpV_ecuaciones = models.TextField(null=True, blank=True)
    def __str__(self):
        return f"Ope_combinadas {self.id}"

#Modelo del metodo multiplicacion vector fila x columna
class MultiFxC(models.Model):
    Mfc_Fila = models.JSONField()  
    Mfc_Column = models.JSONField()
    Mfc_resultado = models.JSONField(null=True, blank=True)
    Mfc_ecuaciones = models.TextField(null=True, blank=True)
    def __str__(self):
        return f"MultiFxC {self.id}"

#Modelo del metodo Producto Matriz por Vector y Propiedad
class PropMxV(models.Model):
    pMxV_matrix = models.JSONField()
    pMxV_vectorU = models.JSONField()
    pMxV_vectorV = models.JSONField()
    pMxV_resultado = models.JSONField(null=True, blank=True)
    pMxV_ecuaciones = models.TextField(null=True, blank=True)
    def __str__(self):
        return f"PropMxV {self.id}"

#Modelo del metodo Suma de matrices
class SmMrx(models.Model):
    sMrx_matrxS = models.JSONField()
    sMrx_escalares = models.JSONField()
    sMrx_resultado = models.JSONField(null=True, blank=True)
    sMrx_ecuaciones = models.JSONField(null=True, blank=True)
    def __str__(self):
        return f"SmMrx {self.id}"

#Transposicion de Matrices 
class TrnsMtx(models.Model):
    trMx_Matriz = models.JSONField()  #Guarda la matriz completa 
    trMx_resultado = models.JSONField(null=True, blank=True)  # Resultado de la eliminación gaussiana
    trMx_ecuaciones = models.TextField(null=True, blank=True)  # Guarda los procedimientos
    def __str__(self):
        return f"TrnsMtx {self.id}"

#Multiplicacion de matrices
class multMtrX(models.Model):
    mMrx_Matrx = models.JSONField()
    mMrx_resultado = models.JSONField(null=True, blank=True) 
    mMrx_ecuaciones = models.TextField(null=True, blank=True)
    def __str__(self):
        return f"multMtrX {self.id}"

#Calculo de Determinantes 
class ClcDeterm(models.Model):
    cldt_Matrx = models.JSONField()
    cldt_resultado = models.JSONField(null=True, blank=True) 
    cldt_ecuaciones = models.TextField(null=True, blank=True)
    def __str__(self):
        return f"clcDeterm {self.id}"

#Calculo de Inversa de una matriz 
class InvMtrx(models.Model):
    inmx_Matrx = models.JSONField()
    inmx_resultado = models.JSONField(null=True, blank=True) 
    inmx_ecuaciones = models.TextField(null=True, blank=True)
    def __str__(self):
        return f"InvMtrx {self.id}"

#Calculo Sistema con Regla de Cramer
class RglCramer(models.Model):
    cramer_Matrx = models.JSONField()
    cramer_TermsIndp = models.JSONField()
    cramer_resultado = models.JSONField(null=True, blank=True) 
    cramer_ecuaciones = models.TextField(null=True, blank=True)
    def __str__(self):
        return f"RglCramer {self.id}"

class factLU(models.Model):
    lu_mtrx = models.JSONField()
    lu_resultado = models.JSONField(null=True, blank=True) 
    lu_ecuaciones = models.JSONField(null=True, blank=True) 
    def __str__(self):
        return f"self.factLU {self.id}"