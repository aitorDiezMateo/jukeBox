from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('bandas/', views.banda_lista, name='banda_lista'),
    path('banda/<int:pk>/', views.banda_detalle, name='banda_detalle'),
    path('estilos/', views.estilo_lista, name='estilo_lista'),
    path('estilo/<int:pk>/', views.estilo_detalle, name='estilo_detalle'),
    path('paises/', views.pais_lista, name='pais_lista'),
    path('cancion/<int:pk>/', views.cancion_detalle, name='cancion_detalle'),
    path('sugerir/', views.sugerir_cancion, name='sugerir_cancion'),
    path('pais/<int:pk>/', views.pais_detalle, name='pais_detalle'),
    path('favoritos/', views.favoritos, name='favoritos'),
    path('api/canciones-favoritos/', views.api_canciones_favoritos, name='api_canciones_favoritos'),
]
