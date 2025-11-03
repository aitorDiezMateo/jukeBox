from django.shortcuts import render, get_object_or_404
from .models import Banda, EstiloMusical, Pais, Cancion

# Create your views here.

def index(request):
    # Obtener una banda por país
    paises = Pais.objects.all()
    bandas_destacadas = []
    for pais in paises:
        banda = Banda.objects.filter(pais_origen=pais).first()
        if banda:
            bandas_destacadas.append(banda)
    
    return render(request, 'jukeBoxApp/index.html', {
        'bandas_destacadas': bandas_destacadas
    })

def banda_lista(request):
    bandas = Banda.objects.all()
    return render(request, 'jukeBoxApp/banda_lista.html', {'bandas': bandas})

def banda_detalle(request, pk):
    banda = get_object_or_404(Banda, pk=pk)
    canciones = banda.canciones.all()[:3]  # Obtener las 3 canciones de la banda
    return render(request, 'jukeBoxApp/banda_detalle.html', {
        'banda': banda,
        'canciones': canciones
    })

def estilo_lista(request):
    estilos = EstiloMusical.objects.all()
    return render(request, 'jukeBoxApp/estilo_lista.html', {'estilos': estilos})

def estilo_detalle(request, pk):
    estilo = get_object_or_404(EstiloMusical, pk=pk)
    estilos_relacionados = EstiloMusical.objects.exclude(pk=pk)[:5]
    
    # Obtener bandas que tienen este estilo
    bandas_con_estilo = estilo.banda_set.all()
    
    # Obtener canciones de estas bandas de forma aleatoria
    canciones = Cancion.objects.filter(banda__in=bandas_con_estilo).order_by('?')[:3]
    
    return render(request, 'jukeBoxApp/estilo_detalle.html', {
        'estilo': estilo,
        'estilos_relacionados': estilos_relacionados,
        'canciones': canciones
    })

def pais_lista(request):
    paises = Pais.objects.all()
    return render(request, 'jukeBoxApp/pais_lista.html', {'paises': paises})

def pais_detalle(request, pk):
    pais = get_object_or_404(Pais, pk=pk)
    paises_relacionados = Pais.objects.exclude(pk=pk)[:5]
    
    # Obtener bandas de este país
    bandas_del_pais = pais.banda_set.all()
    
    # Obtener canciones de estas bandas de forma aleatoria
    canciones = Cancion.objects.filter(banda__in=bandas_del_pais).order_by('?')[:3]
    
    return render(request, 'jukeBoxApp/pais_detalle.html', {
        'pais': pais,
        'paises_relacionados': paises_relacionados,
        'canciones': canciones
    })
