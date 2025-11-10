from django.contrib import admin
from .models import CategoriaProducto, Producto

@admin.register(CategoriaProducto)
class CategoriaProductoAdmin(admin.ModelAdmin):
    list_display = ("nombre", "descripcion")
    search_fields = ("nombre",)

@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ("nombre", "categoria", "precio", "stock", "unidad_medida")
    list_filter = ("categoria", "unidad_medida")
    search_fields = ("nombre", "descripcion")
    list_display_links = ("nombre",)
    ordering = ("categoria", "nombre")
