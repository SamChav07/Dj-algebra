# eliminacionGauss/forms.py

from django import forms
from .models import Matriz

class MatrizForm(forms.ModelForm):
    class Meta:
        model = Matriz
        fields = ['matriz']
