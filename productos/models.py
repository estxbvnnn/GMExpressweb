from django.conf import settings
from django.db import models
from decimal import Decimal
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

class Compra(models.Model):
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="compras")
    total = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal("0.00"))
    creada_en = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Compra #{self.pk} - {self.usuario}"

class CompraItem(models.Model):
    compra = models.ForeignKey(Compra, on_delete=models.CASCADE, related_name="items")
    producto = models.ForeignKey(Producto, on_delete=models.PROTECT)
    cantidad = models.PositiveIntegerField()
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)

    def subtotal(self):
        return self.precio_unitario * self.cantidad
