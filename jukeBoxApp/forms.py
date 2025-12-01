from django import forms
from .models import Valoracion, Sugerencia, Banda


class ValoracionForm(forms.ModelForm):
    class Meta:
        model = Valoracion
        fields = ['puntuacion', 'comentario']
        widgets = {
            'puntuacion': forms.RadioSelect(choices=Valoracion.RATING_CHOICES),
            'comentario': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Deja tu comentario...'}),
        }


class SugerenciaForm(forms.ModelForm):
    # Campo personalizado para seleccionar artista existente o "Otro"
    ARTISTA_CHOICES = [('', '-- Seleccionar artista --')] + \
                     [(banda.nombre, banda.nombre) for banda in Banda.objects.all().order_by('nombre')] + \
                     [('otro', 'Otro artista')]

    artista_selector = forms.ChoiceField(
        choices=ARTISTA_CHOICES,
        required=False,
        widget=forms.Select(attrs={
            'class': 'form-control',
            'id': 'id_artista_selector'
        }),
        label="Artista"
    )

    # Campo adicional para escribir el nombre del artista cuando se selecciona "Otro"
    artista_otro = forms.CharField(
        required=False,
        max_length=200,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Nombre del artista',
            'id': 'id_artista_otro'
        }),
        label=""
    )

    class Meta:
        model = Sugerencia
        fields = ['titulo', 'enlace', 'comentario']
        # Nota: artista_selector y artista_otro son campos adicionales no basados en modelo

    def save(self, commit=True):
        instance = super().save(commit=False)
        # El campo artista ya fue establecido en clean()
        instance.artista = self.cleaned_data.get('artista', '')
        if commit:
            instance.save()
        return instance

    def clean(self):
        cleaned_data = super().clean()
        artista_selector = cleaned_data.get('artista_selector')
        artista_otro = cleaned_data.get('artista_otro')

        if artista_selector == 'otro':
            if not artista_otro:
                raise forms.ValidationError("Debes especificar el nombre del artista.")
            cleaned_data['artista'] = artista_otro
        else:
            cleaned_data['artista'] = artista_selector

        return cleaned_data
