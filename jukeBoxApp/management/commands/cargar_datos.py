from django.core.management.base import BaseCommand
from jukeBoxApp.models import Pais, EstiloMusical, Banda


class Command(BaseCommand):
    help = 'Carga datos de ejemplo en la base de datos'

    def handle(self, *args, **options):
        # Primero borramos datos existentes
        self.stdout.write('Borrando datos existentes...')
        Banda.objects.all().delete()
        EstiloMusical.objects.all().delete()
        Pais.objects.all().delete()

        # Crear países
        self.stdout.write('Creando países...')
        espana = Pais.objects.create(nombre="España", codigo="ESP")
        uk = Pais.objects.create(nombre="Reino Unido", codigo="GBR")
        usa = Pais.objects.create(nombre="Estados Unidos", codigo="USA")
        suecia = Pais.objects.create(nombre="Suecia", codigo="SWE")
        argentina = Pais.objects.create(nombre="Argentina", codigo="ARG")
        jamaica = Pais.objects.create(nombre="Jamaica", codigo="JAM")

        # Crear estilos musicales
        self.stdout.write('Creando estilos musicales...')
        rock = EstiloMusical.objects.create(
            nombre="Rock",
            descripcion="Género musical nacido en los años 50, caracterizado por el uso de guitarras eléctricas y ritmos potentes."
        )
        pop = EstiloMusical.objects.create(
            nombre="Pop",
            descripcion="Música popular orientada al consumo masivo, con melodías pegadizas y estructuras simples."
        )
        punk = EstiloMusical.objects.create(
            nombre="Punk",
            descripcion="Movimiento musical de los 70 caracterizado por su actitud rebelde y canciones cortas y directas."
        )
        heavy = EstiloMusical.objects.create(
            nombre="Heavy Metal",
            descripcion="Género derivado del rock con sonidos más duros, guitarras distorsionadas y temáticas oscuras."
        )
        reggae = EstiloMusical.objects.create(
            nombre="Reggae",
            descripcion="Género musical originario de Jamaica, con ritmo relajado y mensaje social."
        )
        indie = EstiloMusical.objects.create(
            nombre="Indie",
            descripcion="Música independiente con sonido alternativo y producción fuera de grandes sellos."
        )

        # Crear bandas de España
        self.stdout.write('Creando bandas españolas...')
        heroes = Banda.objects.create(
            nombre="Héroes del Silencio",
            pais_origen=espana,
            anio_formacion=1984,
            descripcion="Banda de rock español originaria de Zaragoza, una de las más exitosas en lengua española."
        )
        heroes.estilos.add(rock)

        dover = Banda.objects.create(
            nombre="Dover",
            pais_origen=espana,
            anio_formacion=1992,
            descripcion="Banda madrileña de rock alternativo liderada por Amparo Llanos."
        )
        dover.estilos.add(rock, indie)

        # Crear bandas del Reino Unido
        self.stdout.write('Creando bandas británicas...')
        beatles = Banda.objects.create(
            nombre="The Beatles",
            pais_origen=uk,
            anio_formacion=1960,
            descripcion="La banda más influyente de la historia, revolucionó la música popular en los años 60."
        )
        beatles.estilos.add(rock, pop)

        queen = Banda.objects.create(
            nombre="Queen",
            pais_origen=uk,
            anio_formacion=1970,
            descripcion="Legendaria banda liderada por Freddie Mercury, conocida por su teatralidad y versatilidad."
        )
        queen.estilos.add(rock)

        clash = Banda.objects.create(
            nombre="The Clash",
            pais_origen=uk,
            anio_formacion=1976,
            descripcion="Una de las bandas más importantes del movimiento punk británico."
        )
        clash.estilos.add(punk, rock)

        # Crear bandas de Estados Unidos
        self.stdout.write('Creando bandas estadounidenses...')
        metallica = Banda.objects.create(
            nombre="Metallica",
            pais_origen=usa,
            anio_formacion=1981,
            descripcion="Pioneros del thrash metal, una de las bandas de heavy metal más exitosas de la historia."
        )
        metallica.estilos.add(heavy, rock)

        nirvana = Banda.objects.create(
            nombre="Nirvana",
            pais_origen=usa,
            anio_formacion=1987,
            descripcion="Banda liderada por Kurt Cobain, revolucionó el rock alternativo con el movimiento grunge."
        )
        nirvana.estilos.add(rock, punk)

        ramones = Banda.objects.create(
            nombre="Ramones",
            pais_origen=usa,
            anio_formacion=1974,
            descripcion="Pioneros del punk rock, influyeron en toda la escena musical underground."
        )
        ramones.estilos.add(punk, rock)

        # Crear bandas de Suecia
        self.stdout.write('Creando bandas suecas...')
        abba = Banda.objects.create(
            nombre="ABBA",
            pais_origen=suecia,
            anio_formacion=1972,
            descripcion="Grupo sueco de pop que dominó las listas mundiales en los años 70."
        )
        abba.estilos.add(pop)

        ghost = Banda.objects.create(
            nombre="Ghost",
            pais_origen=suecia,
            anio_formacion=2006,
            descripcion="Banda de heavy metal con estética teatral y temática ocultista."
        )
        ghost.estilos.add(heavy, rock)

        # Crear bandas de Argentina
        self.stdout.write('Creando bandas argentinas...')
        soda = Banda.objects.create(
            nombre="Soda Stereo",
            pais_origen=argentina,
            anio_formacion=1982,
            descripcion="Una de las bandas más influyentes del rock en español, liderada por Gustavo Cerati."
        )
        soda.estilos.add(rock, pop)

        divididos = Banda.objects.create(
            nombre="Divididos",
            pais_origen=argentina,
            anio_formacion=1988,
            descripcion="Banda argentina de rock liderada por Ricardo Mollo."
        )
        divididos.estilos.add(rock)

        # Crear bandas de Jamaica
        self.stdout.write('Creando bandas jamaicanas...')
        marley = Banda.objects.create(
            nombre="Bob Marley and The Wailers",
            pais_origen=jamaica,
            anio_formacion=1963,
            descripcion="La banda más importante de reggae, liderada por Bob Marley, llevó el reggae a nivel mundial."
        )
        marley.estilos.add(reggae)

        self.stdout.write(self.style.SUCCESS('\n¡Datos cargados exitosamente!'))
        self.stdout.write(f'Países: {Pais.objects.count()}')
        self.stdout.write(f'Estilos: {EstiloMusical.objects.count()}')
        self.stdout.write(f'Bandas: {Banda.objects.count()}')
