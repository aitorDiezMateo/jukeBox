from django.core.management.base import BaseCommand
from jukeBoxApp.models import Pais

class Command(BaseCommand):
    help = 'Asigna automáticamente las imágenes a los países basándose en los archivos en media/pais/'

    def handle(self, *args, **kwargs):
        # Mapeo de nombres de archivo a nombres de países
        mapeo_imagenes = {
            'argentina.png': 'Argentina',
            'españa.png': 'España',
            'jamaica.png': 'Jamaica',
            'reino_unido.png': 'Reino Unido',
            'suecia.png': 'Suecia',
            'usa.png': 'Estados Unidos',
            'puertoRico.jpg': 'Puerto Rico',
        }

        paises_actualizados = 0
        paises_no_encontrados = []

        for archivo, nombre_pais in mapeo_imagenes.items():
            try:
                # Buscar el país (case-insensitive)
                pais = Pais.objects.filter(nombre__iexact=nombre_pais).first()
                
                if pais:
                    # Asignar la imagen
                    pais.imagen = f'pais/{archivo}'
                    pais.save()
                    paises_actualizados += 1
                    self.stdout.write(
                        self.style.SUCCESS(f'✓ Imagen asignada a "{pais.nombre}": {archivo}')
                    )
                else:
                    paises_no_encontrados.append(nombre_pais)
                    self.stdout.write(
                        self.style.WARNING(f'⚠ País no encontrado: "{nombre_pais}"')
                    )
            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(f'✗ Error al procesar "{nombre_pais}": {str(e)}')
                )

        # Resumen
        self.stdout.write('\n' + '='*50)
        self.stdout.write(self.style.SUCCESS(f'\nPaíses actualizados: {paises_actualizados}'))
        if paises_no_encontrados:
            self.stdout.write(self.style.WARNING(f'Países no encontrados: {len(paises_no_encontrados)}'))
            for pais in paises_no_encontrados:
                self.stdout.write(f'  - {pais}')
