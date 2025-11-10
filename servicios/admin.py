from django.contrib import admin
from .models import TipoServicio, Servicio

@admin.register(TipoServicio)
class TipoServicioAdmin(admin.ModelAdmin):
    list_display = ("nombre", "descripcion")
    search_fields = ("nombre",)

@admin.register(Servicio)
class ServicioAdmin(admin.ModelAdmin):
    list_display = ("nombre", "tipo", "precio", "estado")
    list_filter = ("tipo", "estado")
    search_fields = ("nombre", "descripcion")
    list_display_links = ("nombre",)
    ordering = ("-tipo", "nombre")
