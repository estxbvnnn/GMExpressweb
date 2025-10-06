from django.db import models
from .choices import ESTADO_SERVICIO

class TipoServicio(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()

    def __str__(self):
        return self.nombre

class Servicio(models.Model):
    nombre = models.CharField(max_length=100)
    tipo = models.ForeignKey(TipoServicio, on_delete=models.CASCADE)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    descripcion = models.TextField()
    estado = models.CharField(max_length=20, choices=ESTADO_SERVICIO, default='activo')
    activo = models.BooleanField(default=True)

    def __str__(self):
        return self.nombre
