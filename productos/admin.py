from django.contrib import admin
from .models import CategoriaProducto, Producto, Compra, CompraItem

class UsingDefaultMixin:
    using = "default"

    def get_queryset(self, request):
        return super().get_queryset(request).using(self.using)

    def save_model(self, request, obj, form, change):
        obj.save(using=self.using)

    def delete_model(self, request, obj):
        obj.delete(using=self.using)

    def save_related(self, request, form, formsets, change):
        for formset in formsets:
            formset.save(using=self.using)

@admin.register(CategoriaProducto)
class CategoriaProductoAdmin(UsingDefaultMixin, admin.ModelAdmin):
    list_display = ("nombre", "descripcion")
    search_fields = ("nombre",)

@admin.register(Producto)
class ProductoAdmin(UsingDefaultMixin, admin.ModelAdmin):
    list_display = ("nombre", "categoria", "precio", "stock", "unidad_medida")
    list_filter = ("categoria", "unidad_medida")
    search_fields = ("nombre", "descripcion")
    list_display_links = ("nombre",)
    ordering = ("categoria", "nombre")

@admin.register(Compra)
class CompraAdmin(UsingDefaultMixin, admin.ModelAdmin):
    list_display = ("id", "usuario", "total", "creada_en")
    date_hierarchy = "creada_en"
    search_fields = ("usuario__email",)

@admin.register(CompraItem)
class CompraItemAdmin(UsingDefaultMixin, admin.ModelAdmin):
    list_display = ("compra", "producto", "cantidad", "precio_unitario")
    search_fields = ("producto__nombre",)
