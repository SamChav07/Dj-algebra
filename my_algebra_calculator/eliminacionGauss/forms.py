# eliminacionGauss/forms.py

from django import forms
from .models import Elim_Gauss

class ElimGaussForm(forms.ModelForm):
    class Meta:
        model = Elim_Gauss
        fields = ['EG_matriz', 'EG_tabla_id']
        widgets = {
            'EG_matriz': forms.Textarea(attrs={'rows': 10, 'cols': 40}),
        }
        labels = {
            'EG_matriz': 'Matriz (en formato JSON)',
            'EG_tabla_id': 'ID de la Tabla',
        }
