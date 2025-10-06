from django.db import models
from .choices import UNIDAD_MEDIDA

class CategoriaProducto(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()

    def __str__(self):
        return self.nombre

class Producto(models.Model):
    nombre = models.CharField(max_length=100)
    categoria = models.ForeignKey(CategoriaProducto, on_delete=models.CASCADE)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    descripcion = models.TextField()
    stock = models.PositiveIntegerField()
    unidad_medida = models.CharField(max_length=20, choices=UNIDAD_MEDIDA, default='unidad')

    def __str__(self):
        return self.nombre
