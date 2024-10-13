# eliminacionGauss/forms.py

from django import forms
from .models import *

class ElimGaussForm(forms.ModelForm):
    class Meta:
        model = Elim_Gauss
        fields = ['EG_matriz']  # Elimina el campo EG_tabla_id
        widgets = {
            'EG_matriz': forms.Textarea(attrs={'rows': 10, 'cols': 40}),
        }
        labels = {
            'EG_matriz': 'Matriz (en formato JSON)',
        }

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