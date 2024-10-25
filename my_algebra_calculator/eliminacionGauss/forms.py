# eliminacionGauss/forms.py

from django import forms
from .models import *

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

    def clean_EG_matriz(self):
        """Método para validar el campo EG_matriz."""
        matriz = self.cleaned_data.get('EG_matriz')
        try:
            # Validar si la matriz es un JSON válido
            import json
            json.loads(matriz)
        except (ValueError, TypeError):
            raise forms.ValidationError("El formato de la matriz no es válido. Debe ser un JSON.")
        return matriz

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

    def clean_OpV_vectores(self):
        """Método para validar el campo OpV_vectores."""
        vectores = self.cleaned_data.get('OpV_vectores')
        try:
            import json
            json.loads(vectores)
        except (ValueError, TypeError):
            raise forms.ValidationError("El formato de los vectores no es válido. Debe ser un JSON.")
        return vectores

    def clean_OpV_escalares(self):
        """Método para validar el campo OpV_escalares."""
        escalares = self.cleaned_data.get('OpV_escalares')
        try:
            import json
            json.loads(escalares)
        except (ValueError, TypeError):
            raise forms.ValidationError("El formato de los escalares no es válido. Debe ser un JSON.")
        return escalares

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

    def clean_Mfc_Fila(self):
        """Método para validar el campo Mfc_Fila."""
        fila = self.cleaned_data.get('Mfc_Fila')
        try:
            import json
            json.loads(fila)
        except (ValueError, TypeError):
            raise forms.ValidationError("El formato de la fila no es válido. Debe ser un JSON.")
        return fila

    def clean_Mfc_Column(self):
        """Método para validar el campo Mfc_Column."""
        columna = self.cleaned_data.get('Mfc_Column')
        try:
            import json
            json.loads(columna)
        except (ValueError, TypeError):
            raise forms.ValidationError("El formato de la columna no es válido. Debe ser un JSON.")
        return columna