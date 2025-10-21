from django.shortcuts import render, get_object_or_404
from .models import Banda, EstiloMusical, Pais

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
    return render(request, 'jukeBoxApp/banda_detalle.html', {'banda': banda})

def estilo_lista(request):
    estilos = EstiloMusical.objects.all()
    return render(request, 'jukeBoxApp/estilo_lista.html', {'estilos': estilos})

def estilo_detalle(request, pk):
    estilo = get_object_or_404(EstiloMusical, pk=pk)
    return render(request, 'jukeBoxApp/estilo_detalle.html', {'estilo': estilo})

def pais_lista(request):
    paises = Pais.objects.all()
    return render(request, 'jukeBoxApp/pais_lista.html', {'paises': paises})

def pais_detalle(request, pk):
    pais = get_object_or_404(Pais, pk=pk)
    return render(request, 'jukeBoxApp/pais_detalle.html', {'pais': pais})
