from django.db import models

# Create your models here.

class Pais(models.Model):
    nombre = models.CharField(max_length=100)
    codigo = models.CharField(max_length=3)
    imagen = models.ImageField(upload_to='pais/', blank=True, null=True)
    
    def __str__(self):
        return self.nombre

class EstiloMusical(models.Model):
    nombre = models.CharField(max_length=50)
    descripcion = models.TextField()
    
    def __str__(self):
        return self.nombre

class Banda(models.Model):
    nombre = models.CharField(max_length=200)
    pais_origen = models.ForeignKey(Pais, on_delete=models.CASCADE)
    estilos = models.ManyToManyField(EstiloMusical)
    anio_formacion = models.IntegerField()
    descripcion = models.TextField()
    imagen = models.ImageField(upload_to='bandas/', blank=True, null=True)
    
    def __str__(self):
        return self.nombre

class Cancion(models.Model):
    titulo = models.CharField(max_length=200)
    banda = models.ForeignKey(Banda, on_delete=models.CASCADE, related_name='canciones')
    anio_publicacion = models.IntegerField()
    archivo_audio = models.FileField(upload_to='canciones/', blank=True, null=True)
    
    def __str__(self):
        return f"{self.titulo} - {self.banda.nombre}"
    
    class Meta:
        verbose_name = "Canción"
        verbose_name_plural = "Canciones"
        ordering = ['anio_publicacion']
