# eliminacionGauss/models.py

from django.db import models

class Elim_Gauss(models.Model):
    EG_matriz = models.JSONField()  # Asegúrate de que esta línea esté presente
    EG_tabla_id = models.CharField(max_length=100)  # ID de la tabla relacionada
    EG_resultado = models.JSONField(null=True, blank=True)  # Resultado de la eliminación gaussiana
    EG_ecuaciones = models.TextField(null=True, blank=True)  # Asegúrate de que esta línea esté presente

    def __str__(self):
        return f"Elim_Gauss {self.id} - Tabla ID: {self.EG_tabla_id}"

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