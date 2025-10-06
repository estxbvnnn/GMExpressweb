from django.contrib import admin
from .models import TipoServicio, Servicio

@admin.register(TipoServicio)
class TipoServicioAdmin(admin.ModelAdmin):
    list_display = ("nombre", "descripcion")
    search_fields = ("nombre",)

@admin.register(Servicio)
class ServicioAdmin(admin.ModelAdmin):
    list_display = ("nombre", "tipo", "precio", "estado", "activo")
    list_filter = ("tipo", "estado", "activo")
    search_fields = ("nombre", "descripcion")
