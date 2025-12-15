from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (
    CategoriaProductoViewSet,
    ProductoViewSet,
    TipoServicioViewSet,
    ServicioViewSet,
    AppointmentViewSet,
)

router = DefaultRouter()
router.register(r"categorias", CategoriaProductoViewSet, basename="categoria")
router.register(r"productos", ProductoViewSet, basename="producto")
router.register(r"tipos-servicio", TipoServicioViewSet, basename="tipo-servicio")
router.register(r"servicios", ServicioViewSet, basename="servicio")
router.register(r"citas", AppointmentViewSet, basename="cita")

urlpatterns = [
    path("", include(router.urls)),
]
