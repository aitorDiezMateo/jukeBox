from django.contrib import admin
from .models import Pais, EstiloMusical, Banda, Cancion

# Register your models here.

admin.site.register(Pais)
admin.site.register(EstiloMusical)
admin.site.register(Banda)
admin.site.register(Cancion)
