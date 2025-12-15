from django.contrib.auth import get_user_model
from rest_framework import serializers

from productos.models import CategoriaProducto, Producto
from servicios.models import TipoServicio, Servicio
from citas.models import Appointment

User = get_user_model()


class CategoriaProductoSerializer(serializers.ModelSerializer):
    class Meta:
        model = CategoriaProducto
        fields = ["id", "nombre", "descripcion"]


class ProductoSerializer(serializers.ModelSerializer):
    categoria_nombre = serializers.CharField(source="categoria.nombre", read_only=True)

    class Meta:
        model = Producto
        fields = [
            "id",
            "nombre",
            "categoria",
            "categoria_nombre",
            "precio",
            "descripcion",
            "stock",
            "unidad_medida",
        ]


class TipoServicioSerializer(serializers.ModelSerializer):
    class Meta:
        model = TipoServicio
        fields = ["id", "nombre", "descripcion"]


class ServicioSerializer(serializers.ModelSerializer):
    tipo_nombre = serializers.CharField(source="tipo.nombre", read_only=True)

    class Meta:
        model = Servicio
        fields = [
            "id",
            "nombre",
            "tipo",
            "tipo_nombre",
            "precio",
            "descripcion",
            "estado",
        ]


class AppointmentSerializer(serializers.ModelSerializer):
    user_id = serializers.PrimaryKeyRelatedField(source="user", read_only=True)
    user_email = serializers.EmailField(source="user.email", read_only=True)
    end_time = serializers.DateTimeField(read_only=True)

    class Meta:
        model = Appointment
        fields = [
            "id",
            "user_id",
            "user_email",
            "scheduled_at",
            "duration_minutes",
            "subject",
            "notes",
            "status",
            "created_at",
            "end_time",
        ]
        read_only_fields = ("id", "created_at", "end_time", "user_id", "user_email")

    def create(self, validated_data):
        request = self.context.get("request")
        if request and hasattr(request, "user"):
            validated_data["user"] = request.user
        return super().create(validated_data)
