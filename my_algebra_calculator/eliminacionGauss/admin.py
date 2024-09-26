from django.contrib import admin
from .models import *

# Register your models here.
class EG_admin(admin.ModelAdmin):
    list_display = ('EG_fila', 'EG_columna', 'EG_valor',)
admin.site.register(Elim_Gauss, EG_admin)