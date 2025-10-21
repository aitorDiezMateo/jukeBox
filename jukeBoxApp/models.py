from django.db import models

# Create your models here.

class Pais(models.Model):
    nombre = models.CharField(max_length=100)
    codigo = models.CharField(max_length=3)
    
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
    
    def __str__(self):
        return self.nombre
