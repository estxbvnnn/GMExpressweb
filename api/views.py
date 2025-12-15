from django.db import transaction
from django.db.models import F
from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response

from productos.models import CategoriaProducto, Producto
from servicios.models import TipoServicio, Servicio
from citas.models import Appointment

from .serializers import (
    CategoriaProductoSerializer,
    ProductoSerializer,
    TipoServicioSerializer,
    ServicioSerializer,
    AppointmentSerializer,
)
from .permissions import IsStaffOrReadOnly, IsOwnerOrStaff


class CategoriaProductoViewSet(viewsets.ModelViewSet):
    queryset = CategoriaProducto.objects.all().order_by("nombre")
    serializer_class = CategoriaProductoSerializer
    permission_classes = [IsStaffOrReadOnly]


class ProductoViewSet(viewsets.ModelViewSet):
    queryset = Producto.objects.select_related("categoria").all().order_by("nombre")
    serializer_class = ProductoSerializer
    permission_classes = [IsStaffOrReadOnly]

    def get_permissions(self):
        if getattr(self, "action", None) == "comprar":
            return [permissions.AllowAny()]
        return super().get_permissions()

    @action(detail=True, methods=["post"], url_path="comprar", permission_classes=[permissions.AllowAny])
    def comprar(self, request, pk=None):
        cantidad = request.data.get("cantidad")
        try:
            cantidad = int(cantidad)
        except (TypeError, ValueError):
            return Response({"detail": "Cantidad inválida."}, status=400)
        if cantidad <= 0:
            return Response({"detail": "La cantidad debe ser mayor a 0."}, status=400)

        with transaction.atomic():
            try:
                producto = Producto.objects.select_for_update().get(pk=pk)
            except Producto.DoesNotExist:
                return Response({"detail": "Producto no encontrado."}, status=404)

            if cantidad > producto.stock:
                return Response({"detail": "Stock insuficiente."}, status=400)

            producto.stock = F("stock") - cantidad
            producto.save(update_fields=["stock"])
            producto.refresh_from_db(fields=["stock"])

        return Response(
            {
                "detail": "Compra realizada y stock actualizado.",
                "stock_restante": producto.stock,
            },
            status=200,
        )


class TipoServicioViewSet(viewsets.ModelViewSet):
    queryset = TipoServicio.objects.all().order_by("nombre")
    serializer_class = TipoServicioSerializer
    permission_classes = [IsStaffOrReadOnly]


class ServicioViewSet(viewsets.ModelViewSet):
    queryset = Servicio.objects.select_related("tipo").all().order_by("nombre")
    serializer_class = ServicioSerializer
    permission_classes = [IsStaffOrReadOnly]


class AppointmentViewSet(viewsets.ModelViewSet):
    serializer_class = AppointmentSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrStaff]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff or user.is_superuser:
            return Appointment.objects.select_related("user").all().order_by("-scheduled_at")
        return Appointment.objects.select_related("user").filter(user=user).order_by("-scheduled_at")

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
