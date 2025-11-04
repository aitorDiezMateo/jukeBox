from django.core.management.base import BaseCommand
from jukeBoxApp.models import EstiloMusical

class Command(BaseCommand):
    help = 'Asigna automáticamente las imágenes a los estilos musicales basándose en los archivos en media/estilos/'

    def handle(self, *args, **kwargs):
        # Mapeo de nombres de archivo a nombres de estilos
        mapeo_imagenes = {
            'heavy_metal.png': 'Heavy Metal',
            'indie_music.jpg': 'Indie',
            'pop_music.jpg': 'Pop',
            'punk.png': 'Punk',
            'reggae.png': 'Reggae',
            'rock.png': 'Rock',
        }

        estilos_actualizados = 0
        estilos_no_encontrados = []

        for archivo, nombre_estilo in mapeo_imagenes.items():
            try:
                # Buscar el estilo (case-insensitive)
                estilo = EstiloMusical.objects.filter(nombre__iexact=nombre_estilo).first()
                
                if estilo:
                    # Asignar la imagen
                    estilo.imagen = f'estilos/{archivo}'
                    estilo.save()
                    estilos_actualizados += 1
                    self.stdout.write(
                        self.style.SUCCESS(f'✓ Imagen asignada a "{estilo.nombre}": {archivo}')
                    )
                else:
                    estilos_no_encontrados.append(nombre_estilo)
                    self.stdout.write(
                        self.style.WARNING(f'⚠ Estilo no encontrado: "{nombre_estilo}"')
                    )
            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(f'✗ Error al procesar "{nombre_estilo}": {str(e)}')
                )

        # Resumen
        self.stdout.write('\n' + '='*50)
        self.stdout.write(self.style.SUCCESS(f'\nEstilos actualizados: {estilos_actualizados}'))
        if estilos_no_encontrados:
            self.stdout.write(self.style.WARNING(f'Estilos no encontrados: {len(estilos_no_encontrados)}'))
            for estilo in estilos_no_encontrados:
                self.stdout.write(f'  - {estilo}')
