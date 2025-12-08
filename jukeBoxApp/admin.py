from django.contrib import admin
from .models import Pais, EstiloMusical, Banda, Cancion, Favorito
from .models import Valoracion, Sugerencia

# Register your models here.

# admin.site.register(Pais)
# admin.site.register(EstiloMusical)
# admin.site.register(Banda)
# admin.site.register(Cancion)
# admin.site.register(Valoracion)
# admin.site.register(Sugerencia)

class SoloLecturaAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        if request.user.groups.filter(name="RevisorAnalista").exists():
            return False
        return super().has_add_permission(request)

    def has_change_permission(self, request, obj=None):
        if request.user.groups.filter(name="RevisorAnalista").exists():
            return False
        return super().has_change_permission(request, obj)

    def has_delete_permission(self, request, obj=None):
        if request.user.groups.filter(name="RevisorAnalista").exists():
            return False
        return super().has_delete_permission(request, obj)

@admin.register(Pais)
class PaisAdmin(SoloLecturaAdmin):
    list_display = ("nombre",)

@admin.register(EstiloMusical)
class EstiloMusicalAdmin(SoloLecturaAdmin):
    list_display = ("nombre",)

@admin.register(Banda)
class BandaAdmin(SoloLecturaAdmin):
    list_display = ("nombre", "pais_origen", "anio_formacion")
    search_fields = ("nombre",)

@admin.register(Cancion)
class CancionAdmin(SoloLecturaAdmin):
    list_display = ("titulo", "banda", "anio_publicacion")


@admin.register(Favorito)
class FavoritoAdmin(admin.ModelAdmin):
    list_display = ("user", "banda", "creado")
    list_filter = ("creado", "user")
    search_fields = ("user__username", "banda__nombre")
    readonly_fields = ("creado",)
    autocomplete_fields = ["banda"]
    
    def has_add_permission(self, request):
        # Los usuarios normales no pueden añadir favoritos desde el admin
        # Solo staff/superusers
        return request.user.is_staff or request.user.is_superuser
