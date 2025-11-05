from django.core.management.base import BaseCommand
from jukeBoxApp.models import Banda, Cancion
import os
from django.conf import settings

class Command(BaseCommand):
    help = 'Carga las canciones en la base de datos según el archivo canciones.md'

    def handle(self, *args, **kwargs):
        # Mapeo de canciones por banda
        canciones_data = {
            'Bob Marley and The Wailers': [
                ('Three Little Birds', 1977, 'BobMarley_ThreeLittleBirds.mp3'),
                ('Could You Be Loved', 1980, 'BobMarley_CouldYouBeLoved.mp3'),
                ('Is This Love', 1978, 'BobMarley_IsThisLove.mp3'),
            ],
            'Divididos': [
                ('Vivo Aca', 2003, 'Divididos_VivoAca.mp3'),
                ('Que ves', 1993, 'Divididos_QueVes.mp3'),
                ('Guanuqueando', 1993, 'Divididos_Guanuqueando.mp3'),
            ],
            'Soda Stereo': [
                ('De Música ligera', 1990, 'SodaStereo_DeMúsicaLigera.mp3'),
                ('Cuando Pase el Temblor', 1985, 'SodaStereo_CuandoPaseElTemblor.mp3'),
                ('Trátame Suavemente', 1984, 'SodaStereo_TrátameSuavemente.mp3'),
            ],
            'Ghost': [
                ('Lachryma', 2015, 'Ghost_Lachryma.mp3'),
                ('Mary On A Cross', 2019, 'Ghost_MaryOnACross.mp3'),
                ('Square Hammer', 2016, 'Ghost_SquareHammer.mp3'),
            ],
            'ABBA': [
                ('Dancing Queen', 1976, 'ABBA_DancingQueen.mp3'),
                ('Gimme Gimme Gimme (A Man After Midnight)', 1979, 'ABBA_GimmeGimmeGimme.mp3'),
                ('Mamma Mia', 1975, 'ABBA_MammaMia.mp3'),
            ],
            'Ramones': [
                ('I Wanna Be Sedated', 1978, 'Ramones_IWannaBeSedated.mp3'),
                ('Pet Sematary', 1989, 'Ramones_PetSematary.mp3'),
                ('Poison Heart', 1992, 'Ramones_PoisonHeart.mp3'),
            ],
            'Nirvana': [
                ('Smells Like Teen Spirit', 1991, 'Nirvana_SmellsLikeTeenSpirit.mp3'),
                ('Come As You Are', 1991, 'Nirvana_ComeAsYouAre.mp3'),
                ('Something In The Way', 1991, 'Nirvana_SomethingInTheWay.mp3'),
            ],
            'Metallica': [
                ('Enter Sandman', 1991, 'Metallica_EnterSandman.mp3'),
                ('Nothing Else Matters', 1991, 'Metallica_NothingElseMatters.mp3'),
                ('Whiskey In The Jar', 1998, 'Metallica_WhiskeyintheJar.mp3'),
            ],
            'The Clash': [
                ('London Calling', 1979, 'TheClash_LondonCalling.mp3'),
                ('Should I Stay or Should I Go', 1982, 'TheClash_ShouldIStayOrShouldIGo.mp3'),
                ('Rock The Casbah', 1982, 'TheClash_RockTheCasbah.mp3'),
            ],
            'Queen': [
                ('Bohemian Rhapsody', 1975, 'Queen_BohemianRhapsody.mp3'),
                ('Another one bites the dust', 1980, 'Queen_AnotherOneBitesTheDust.mp3'),
                ("Don't Stop Me Now", 1979, 'Queen_DontStopMeNow.mp3'),
            ],
            'The Beatles': [
                ('Here Comes the Sun', 1969, 'Beatles_hereComesTheSun.mp3'),
                ('Let It Be', 1970, 'Beatles_LetItBe.mp3'),
                ('Come Together', 1969, 'Beatles_comeTogether.mp3'),
            ],
            'Dover': [
                ('Serenade', 1997, 'DOVER_Serenade.mp3'),
                ('Devil Came to Me', 1997, 'DOVER_DevilCameToMe.mp3'),
                ('King George', 1997, 'DOVER_KingGeorge.mp3'),
            ],
            'Héroes del Silencio': [
                ('Entre Dos Tierras', 1990, 'HeroesDelSilencio_entreDosTierras.mp3'),
                ('Maldito Duende', 1989, 'HeroesDelSilencio_MalditoDuende.mp3'),
                ('La Sirena Varada', 1993, 'HeroesDelSilencio_LaSirenaVarada.mp3'),
            ],
            'Bad Bunny': [
                ('Baile Inolvidable', 2020, 'BadBunny_BaileInolvidable.mp3'),
                ('Dakiti', 2020, 'BadBunny_Dakiti.mp3'),
                ('La Santa', 2020, 'BadBunny_LaSanta.mp3'),
            ],
        }

        canciones_creadas = 0
        canciones_actualizadas = 0
        bandas_no_encontradas = []

        for nombre_banda, canciones in canciones_data.items():
            try:
                # Buscar la banda
                banda = Banda.objects.filter(nombre__iexact=nombre_banda).first()
                
                if not banda:
                    bandas_no_encontradas.append(nombre_banda)
                    self.stdout.write(
                        self.style.WARNING(f'⚠ Banda no encontrada: "{nombre_banda}"')
                    )
                    continue

                # Crear las canciones
                for titulo, anio, archivo in canciones:
                    cancion, created = Cancion.objects.get_or_create(
                        titulo=titulo,
                        banda=banda,
                        defaults={
                            'anio_publicacion': anio,
                            'archivo_audio': f'canciones/{archivo}'
                        }
                    )
                    
                    if created:
                        canciones_creadas += 1
                        self.stdout.write(
                            self.style.SUCCESS(f'✓ Canción creada: "{titulo}" - {banda.nombre} ({anio})')
                        )
                    else:
                        # Actualizar si ya existe
                        cancion.anio_publicacion = anio
                        cancion.archivo_audio = f'canciones/{archivo}'
                        cancion.save()
                        canciones_actualizadas += 1
                        self.stdout.write(
                            self.style.WARNING(f'↻ Canción actualizada: "{titulo}" - {banda.nombre}')
                        )

            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(f'✗ Error al procesar "{nombre_banda}": {str(e)}')
                )

        # Resumen
        self.stdout.write('\n' + '='*50)
        self.stdout.write(self.style.SUCCESS(f'\nCanciones creadas: {canciones_creadas}'))
        self.stdout.write(self.style.WARNING(f'Canciones actualizadas: {canciones_actualizadas}'))
        if bandas_no_encontradas:
            self.stdout.write(self.style.WARNING(f'Bandas no encontradas: {len(bandas_no_encontradas)}'))
            for banda in bandas_no_encontradas:
                self.stdout.write(f'  - {banda}')
        
        self.stdout.write(f'\nTotal de canciones en BD: {Cancion.objects.count()}')
