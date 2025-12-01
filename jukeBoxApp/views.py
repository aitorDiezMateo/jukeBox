from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.http import JsonResponse
from django.views.generic import TemplateView, ListView, DetailView, FormView, View
from .models import Banda, EstiloMusical, Pais, Cancion, Valoracion, Sugerencia
from .forms import ValoracionForm, SugerenciaForm

# Create your views here.

class IndexView(TemplateView):
    template_name = 'jukeBoxApp/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Obtener una banda por país
        paises = Pais.objects.all()
        bandas_destacadas = []
        for pais in paises:
            banda = Banda.objects.filter(pais_origen=pais).first()
            if banda:
                bandas_destacadas.append(banda)

        context['bandas_destacadas'] = bandas_destacadas
        return context

class BandaListView(ListView):
    model = Banda
    template_name = 'jukeBoxApp/banda_lista.html'
    context_object_name = 'bandas'
    
    def get_queryset(self):
        # Render only the first page of bands on initial load (max 6)
        return Banda.objects.all()[:6]

class BandaDetailView(DetailView):
    model = Banda
    template_name = 'jukeBoxApp/banda_detalle.html'
    context_object_name = 'banda'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['canciones'] = self.object.canciones.all()[:3]  # Obtener las 3 canciones de la banda
        return context

class EstiloListView(ListView):
    model = EstiloMusical
    template_name = 'jukeBoxApp/estilo_lista.html'
    context_object_name = 'estilos'

class EstiloDetailView(DetailView):
    model = EstiloMusical
    template_name = 'jukeBoxApp/estilo_detalle.html'
    context_object_name = 'estilo'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['estilos_relacionados'] = EstiloMusical.objects.exclude(pk=self.object.pk)[:5]

        # Obtener bandas que tienen este estilo
        bandas_con_estilo = self.object.banda_set.all()

        # Obtener canciones de estas bandas de forma aleatoria
        context['canciones'] = Cancion.objects.filter(banda__in=bandas_con_estilo).order_by('?')[:3]
        return context

class PaisListView(ListView):
    model = Pais
    template_name = 'jukeBoxApp/pais_lista.html'
    context_object_name = 'paises'

class PaisDetailView(DetailView):
    model = Pais
    template_name = 'jukeBoxApp/pais_detalle.html'
    context_object_name = 'pais'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['paises_relacionados'] = Pais.objects.exclude(pk=self.object.pk)[:5]

        # Obtener bandas de este país
        bandas_del_pais = self.object.banda_set.all()

        # Obtener canciones de estas bandas de forma aleatoria
        context['canciones'] = Cancion.objects.filter(banda__in=bandas_del_pais).order_by('?')[:3]
        return context

class FavoritosView(TemplateView):
    template_name = 'jukeBoxApp/favoritos.html'
    # La página de favoritos se maneja completamente con JavaScript y localStorage
    # Esta vista solo renderiza la plantilla


class CancionDetailView(DetailView):
    model = Cancion
    template_name = 'jukeBoxApp/cancion_detalle.html'
    context_object_name = 'cancion'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['valoraciones'] = self.object.valoraciones.order_by('-creado')

        # Calcular media de puntuaciones
        puntuaciones = self.object.valoraciones.all().values_list('puntuacion', flat=True)
        promedio = None
        if puntuaciones:
            promedio = round(sum(puntuaciones) / len(puntuaciones), 2)
        context['promedio'] = promedio
        context['form'] = ValoracionForm()
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = ValoracionForm(request.POST)
        if form.is_valid():
            valor = form.save(commit=False)
            valor.cancion = self.object
            valor.save()
            return redirect('cancion_detalle', pk=self.object.pk)

        context = self.get_context_data()
        context['form'] = form
        return self.render_to_response(context)


class SugerirCancionView(FormView):
    template_name = 'jukeBoxApp/sugerir_cancion.html'
    form_class = SugerenciaForm
    success_url = '/sugerir/'  # This will redirect to the same page

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

class ApiCancionesFavoritosView(View):
    # API para obtener canciones de bandas favoritas

    def get(self, request):
        ids = request.GET.get('ids', '')

        if not ids:
            return JsonResponse({'canciones': []})

        try:
            # Convertir IDs a lista de enteros
            banda_ids = [int(id.strip()) for id in ids.split(',') if id.strip()]

            # Obtener canciones de esas bandas
            canciones = Cancion.objects.filter(
                banda__id__in=banda_ids,
                archivo_audio__isnull=False
            ).select_related('banda')[:50]  # Límite de 50 canciones

            # Convertir a formato JSON
            canciones_data = []
            for cancion in canciones:
                canciones_data.append({
                    'titulo': cancion.titulo,
                    'banda': cancion.banda.nombre,
                    'imagen': cancion.banda.imagen.url if cancion.banda.imagen else '',
                    'archivo': cancion.archivo_audio.url if cancion.archivo_audio else '',
                    'duracion': '3:45'  # Podrías calcular esto del archivo
                })

            return JsonResponse(canciones_data, safe=False)

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)


class ApiBandasView(View):
    """API que devuelve bandas paginadas en JSON para infinite scroll."""
    def get(self, request):
        try:
            page = int(request.GET.get('page', 1))
            page_size = int(request.GET.get('page_size', 6))
        except ValueError:
            return JsonResponse({'bands': [], 'has_more': False})

        filter_q = request.GET.get('filter', '')

        qs = Banda.objects.select_related('pais_origen').all().order_by('nombre')
        if filter_q and filter_q != '*':
            if filter_q == 'number':
                qs = qs.filter(nombre__regex=r'^[0-9]')
            else:
                qs = qs.filter(nombre__istartswith=filter_q)

        # Simple pagination
        start = (page - 1) * page_size
        end = start + page_size
        total = qs.count()
        items = qs[start:end]

        bands = []
        for b in items:
            rel_url = reverse('banda_detalle', args=[b.id])
            bands.append({
                'id': b.id,
                'nombre': b.nombre,
                'pais': b.pais_origen.nombre if b.pais_origen else '',
                'imagen': b.imagen.url if b.imagen else '',
                'url': rel_url
            })

        has_more = end < total

        return JsonResponse({'bands': bands, 'has_more': has_more})
