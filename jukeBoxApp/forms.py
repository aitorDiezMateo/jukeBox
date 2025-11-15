from django import forms
from .models import Valoracion, Sugerencia


class ValoracionForm(forms.ModelForm):
    class Meta:
        model = Valoracion
        fields = ['puntuacion', 'comentario']
        widgets = {
            'puntuacion': forms.RadioSelect(choices=Valoracion.RATING_CHOICES),
            'comentario': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Deja tu comentario...'}),
        }


class SugerenciaForm(forms.ModelForm):
    class Meta:
        model = Sugerencia
        fields = ['titulo', 'artista', 'enlace', 'comentario']
        widgets = {
            'titulo': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Título de la canción'}),
            'artista': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Artista (opcional)'}),
            'enlace': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'Enlace a la canción (YouTube, Spotify...)'}),
            'comentario': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Explica por qué sugerir esta canción...'}),
        }
