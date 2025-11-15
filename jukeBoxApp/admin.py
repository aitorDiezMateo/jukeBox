from django.contrib import admin
from .models import Pais, EstiloMusical, Banda, Cancion
from .models import Valoracion, Sugerencia

# Register your models here.

admin.site.register(Pais)
admin.site.register(EstiloMusical)
admin.site.register(Banda)
admin.site.register(Cancion)
admin.site.register(Valoracion)
admin.site.register(Sugerencia)
