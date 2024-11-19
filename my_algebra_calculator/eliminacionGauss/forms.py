# eliminacionGauss/forms.py

from django import forms
from .models import *
import json

#Forms01
class ElimGaussForm(forms.ModelForm):
    class Meta:
        model = Elim_Gauss
        fields = ['EG_matriz']
        widgets = {
            'EG_matriz': forms.Textarea(attrs={'rows': 10, 'cols': 40}),
        }
        labels = {
            'EG_matriz': 'Matriz (en formato JSON)',
        }

#Forms02
class CombVectorForm(forms.ModelForm):
    class Meta:
        model = Ope_combinadas
        fields = ['OpV_vectores', 'OpV_escalares']
        widgets = {
            'OpV_vectores': forms.Textarea(attrs={'rows': 10, 'cols': 40}),
            'OpV_escalares': forms.Textarea(attrs={'rows': 5, 'cols': 40}),
        }
        labels = {
            'OpV_vectores': 'Vectores (en formato JSON)',
            'OpV_escalares': 'Escalares (en formato JSON)',
        }

#Forms03
class MultiFxCForm(forms.ModelForm):
    class Meta:
        model = MultiFxC
        fields = ['Mfc_Fila', 'Mfc_Column']
        widgets = {
            'Mfc_Fila': forms.Textarea(attrs={'rows': 5, 'cols': 40}),
            'Mfc_Column': forms.Textarea(attrs={'rows': 5, 'cols': 40}),
        }
        labels = {
            'Mfc_Fila': 'Fila (en formato JSON)',
            'Mfc_Column': 'Columna (en formato JSON)',
        }

#Forms04
class PropMxVForm(forms.ModelForm):
    class Meta:
        model = PropMxV
        fields = ('pMxV_matrix', 'pMxV_vectorU', 'pMxV_vectorV')
        widgets = {
            'pMxV_matrix': forms.Textarea(attrs={'rows': 5, 'cols': 40}),
            'pMxV_vectorU': forms.Textarea(attrs={'rows': 5, 'cols': 40}),
            'pMxV_vectorV': forms.Textarea(attrs={'rows': 5, 'cols': 40}),
        }
        labels = {
            'pMxV_matrix': 'Matriz (en formato JSON)',
            'pMxV_vectorU': 'VectorU (en formato JSON)',
            'pMxV_vectorV': 'VectorV (en formato JSON)',
        }

#Forms05
class SmMrxForm(forms.ModelForm):
    class Meta:
        model = SmMrx
        fields = ('sMrx_matrxS', 'sMrx_escalares')
        widgets = {
            'sMrx_matrxS': forms.Textarea(attrs={'rows': 10, 'cols': 40}),
            'sMrx_escalares': forms.Textarea(attrs={'rows': 5, 'cols': 40}),
        }
        labels = {
            'sMrx_matrxS': 'Matrices (en formato JSON)',
            'sMrx_escalares': 'Escalares (en formato JSON)',
        }

#Forms06
class TrnsMtxForm(forms.ModelForm):
    class Meta:
        model = TrnsMtx
        fields = ['trMx_Matriz']
        widgets = {
            'trMx_Matriz': forms.Textarea(attrs={'rows': 10, 'cols': 40}),
        }
        labels = {
            'trMx_Matriz': 'Matriz (en formato JSON)',
        }

#Forms07
class MultMtrXForm(forms.ModelForm):
    class Meta:
        model = multMtrX
        fields = ['mMrx_Matrx']  # Include fields you want in the form
        widgets = {
            'mMrx_Matrx': forms.Textarea(attrs={'rows': 10, 'cols': 40, 'placeholder': 'Ejemplo: [[1, 2], [3, 4]]'}),
        }
        labels = {
            'mMrx_Matrx': 'Matriz (en formato JSON)',
        }

#Forms08
class ClcDetermForm(forms.ModelForm):
    class Meta:
        model = ClcDeterm
        fields = ['cldt_Matrx']
        widgets = {
            'cldt_Matrx': forms.Textarea(attrs={'rows': 10, 'cols': 40, 'placeholder': 'Ejemplo: [[1, 2], [3, 4]]'}),
        }
        labels = {
            'cldt_Matrx': 'Matriz (en formato JSON)',
        }

#Forms09
class InvMtrxForm(forms.ModelForm):
    class Meta:
        model = InvMtrx
        fields = ['inmx_Matrx']
        widgets = {
            'inmx_Matrx': forms.Textarea(attrs={'rows': 10, 'cols': 40, 'placeholder': 'Ejemplo: [[1, 2], [3, 4]]'}),
        }
        labels = {
            'inmx_Matrx': 'Matriz (en formato JSON)',
        }

#Forms10
class RglCramerForm(forms.ModelForm):
    class Meta:
        model = RglCramer
        fields = ['cramer_Matrx']
        widgets = {
            'cramer_Matrx': forms.Textarea(attrs={'rows': 10, 'cols': 40, 'placeholder': 'Ejemplo: [[1, 2], [3, 4]]'}),
        }
        labels = {
            'cramer_Matrx': 'Matriz (en formato JSON)',
        }

#Forms11
class factLUForm(forms.ModelForm):
    class Meta:
        model = factLU
        fields = ['lu_mtrx']
        widgets = {
            'lu_mtrx': forms.Textarea(attrs={'rows': 10, 'cols': 40, 'placeholder': 'Ejemplo: [[1, 2], [3, 4]]'}),        
        }
        labels = {
            'lu_mtrx': 'Matriz (en formato JSON)',
        }

#Forms12
class biSeccionForm(forms.ModelForm):
    class Meta:
        model = biSeccion
        fields = ['bi_funcion'] 
        widgets = {
            'bi_funcion': forms.Textarea(attrs={'rows': 10, 'cols': 40, 'placeholder': 'Ejemplo: x^2 - 4'}),        
        }
        labels = {
            'bi_funcion': 'bi_funcion (en formato Text)',
        }