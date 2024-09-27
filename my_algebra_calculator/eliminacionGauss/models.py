from django.db import models

from django.db import models

class EG_Table(models.Model):
    tb_filas = models.IntegerField()
    tb_columnas = models.IntegerField()

class Elim_Gauss(models.Model):
    EG_tabla = models.ForeignKey(EG_Table, on_delete=models.CASCADE, related_name='elim_gauss')
    EG_ecuaciones = models.IntegerField()  # Número de filas
    EG_incognitas = models.IntegerField()  # Número de columnas
    EG_fila = models.IntegerField()  # Fila del valor
    EG_columna = models.IntegerField()  # Columna del valor
    EG_valor = models.FloatField()  # Valor individual

    class Meta:
        unique_together = ('EG_tabla' ,'EG_fila', 'EG_columna')  # Asegura que no haya duplicados para la misma celda en la matriz

    def __str__(self):
        return f"({self.EG_fila}, {self.EG_columna}): {self.EG_valor}"  # Formato deseado

class Ope_combinadas(models.Model):
    OpV_NmVectores = models.IntegerField()# Columnas X
    OpV_DmVectores = models.IntegerField()# Filas Y
    OpV_valor = models.FloatField()
    class Meta:
        unique_together = ('OpV_NmVectores', 'OpV_DmVectores')
    def __str__(self):
        return f"({self.OpV_NmVectores}, {self.OpV_DmVectores}): {self.OpV_valor}"

class MltFC_horizontal(models.Model):
    MfcX_NmVectorX = models.IntegerField()
    MfcX_NmVectorY = models.IntegerField()
    MfcX_valor = models.FloatField()
    class Meta:
        unique_together = ('MfcX_NmVectorX', 'MfcX_NmVectorY')
    def __str__(self):
        return f"({self.MfcX_NmVectorX}, {self.MfcX_NmVectorY}): {self.MfcX_valor}"

class MltFC_vertical(models.Model):
    MfcY_NmVectorX = models.IntegerField()
    MfcY_NmVectorY = models.IntegerField()
    MfcY_valor = models.FloatField()
    class Meta:
        unique_together = ('MfcY_NmVectorX', 'MfcY_NmVectorY')
    def __str__(self):
        return f"({self.MfcX_NmVectorX}, {self.MfcX_NmVectorY}): {self.MfcX_valor}"