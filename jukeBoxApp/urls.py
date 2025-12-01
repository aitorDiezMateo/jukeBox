from django.urls import path
from . import views

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('bandas/', views.BandaListView.as_view(), name='banda_lista'),
    path('banda/<int:pk>/', views.BandaDetailView.as_view(), name='banda_detalle'),
    path('estilos/', views.EstiloListView.as_view(), name='estilo_lista'),
    path('estilo/<int:pk>/', views.EstiloDetailView.as_view(), name='estilo_detalle'),
    path('paises/', views.PaisListView.as_view(), name='pais_lista'),
    path('cancion/<int:pk>/', views.CancionDetailView.as_view(), name='cancion_detalle'),
    path('sugerir/', views.SugerirCancionView.as_view(), name='sugerir_cancion'),
    path('pais/<int:pk>/', views.PaisDetailView.as_view(), name='pais_detalle'),
    path('favoritos/', views.FavoritosView.as_view(), name='favoritos'),
    path('api/canciones-favoritos/', views.ApiCancionesFavoritosView.as_view(), name='api_canciones_favoritos'),
    path('api/bandas/', views.ApiBandasView.as_view(), name='api_bandas'),
]
