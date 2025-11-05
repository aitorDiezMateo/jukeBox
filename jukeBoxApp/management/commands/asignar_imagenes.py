from django.core.management.base import BaseCommand
from jukeBoxApp.models import Banda
import os
from django.conf import settings

class Command(BaseCommand):
    help = 'Asigna automáticamente las imágenes a las bandas basándose en los archivos en media/bandas/'

    def handle(self, *args, **kwargs):
        # Mapeo de nombres de archivo a nombres de bandas
        mapeo_imagenes = {
            'abba.png': 'ABBA',
            'BobMarley.jpg': 'Bob Marley and The Wailers',
            'divididos.png': 'Divididos',
            'dover.png': 'Dover',
            'ghost.png': 'Ghost',
            'heroesDelSilencio.png': 'Héroes del Silencio',
            'metallica.png': 'Metallica',
            'nirvana.png': 'Nirvana',
            'queen.png': 'Queen',
            'ramones.png': 'Ramones',
            'sondaStereo.png': 'Soda Stereo',
            'TheBeatles.png': 'The Beatles',
            'theClash.png': 'The Clash',
            'badBunny.jpg': 'Bad Bunny',
        }

        bandas_actualizadas = 0
        bandas_no_encontradas = []

        for archivo, nombre_banda in mapeo_imagenes.items():
            try:
                # Buscar la banda (case-insensitive)
                banda = Banda.objects.filter(nombre__iexact=nombre_banda).first()
                
                if banda:
                    # Asignar la imagen
                    banda.imagen = f'bandas/{archivo}'
                    banda.save()
                    bandas_actualizadas += 1
                    self.stdout.write(
                        self.style.SUCCESS(f'✓ Imagen asignada a "{banda.nombre}": {archivo}')
                    )
                else:
                    bandas_no_encontradas.append(nombre_banda)
                    self.stdout.write(
                        self.style.WARNING(f'⚠ Banda no encontrada: "{nombre_banda}"')
                    )
            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(f'✗ Error al procesar "{nombre_banda}": {str(e)}')
                )

        # Resumen
        self.stdout.write('\n' + '='*50)
        self.stdout.write(self.style.SUCCESS(f'\nBandas actualizadas: {bandas_actualizadas}'))
        if bandas_no_encontradas:
            self.stdout.write(self.style.WARNING(f'Bandas no encontradas: {len(bandas_no_encontradas)}'))
            for banda in bandas_no_encontradas:
                self.stdout.write(f'  - {banda}')
