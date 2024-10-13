from django.contrib import admin
from .models import Elim_Gauss

# Register your models here.
class EG_admin(admin.ModelAdmin):
    list_display = ('id',)  # Asegúrate de que sea una tupla, incluso con un solo elemento

admin.site.register(Elim_Gauss, EG_admin)