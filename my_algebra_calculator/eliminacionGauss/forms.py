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

    def clean_pMxV_matrix(self):
        """Método para validar el campo pMxV_matrix."""
        matrix = self.cleaned_data.get('pMxV_matrix')
        try:
            json.loads(matrix)
        except (ValueError, TypeError):
            raise forms.ValidationError("El formato de la matriz no es válido. Debe ser un JSON.")
        return matrix

    def clean_pMxV_vectorU(self):
        """Método para validar el campo pMxV_vectorU."""
        vector_u = self.cleaned_data.get('pMxV_vectorU')
        try:
            json.loads(vector_u)
        except (ValueError, TypeError):
            raise forms.ValidationError("El formato del vector U no es válido. Debe ser un JSON.")
        return vector_u

    def clean_pMxV_vectorV(self):
        """Método para validar el campo pMxV_vectorV."""
        vector_v = self.cleaned_data.get('pMxV_vectorV')
        try:
            json.loads(vector_v)
        except (ValueError, TypeError):
            raise forms.ValidationError("El formato del vector V no es válido. Debe ser un JSON.")
        return vector_v

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

    def clean_sMrx_matrxS(self):
        """Método para validar el campo sMrx_matrxS."""
        matrices = self.cleaned_data.get('sMrx_matrxS')
        try:
            matrix_list = json.loads(matrices)
            if not isinstance(matrix_list, list):
                raise forms.ValidationError("El formato de las matrices no es válido. Debe ser un JSON que contenga una lista de matrices.")
            for matrix in matrix_list:
                if not isinstance(matrix, list):
                    raise forms.ValidationError("Cada matriz debe ser una lista.")
        except (ValueError, TypeError):
            raise forms.ValidationError("El formato de las matrices no es válido. Debe ser un JSON.")
        return matrices

    def clean_sMrx_escalares(self):
        """Método para validar el campo sMrx_escalares."""
        escalares = self.cleaned_data.get('sMrx_escalares')
        try:
            escalar_list = json.loads(escalares)
            if not isinstance(escalar_list, list):
                raise forms.ValidationError("El formato de los escalares no es válido. Debe ser un JSON que contenga una lista de escalares.")
        except (ValueError, TypeError):
            raise forms.ValidationError("El formato de los escalares no es válido. Debe ser un JSON.")
        return escalares