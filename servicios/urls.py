from django.urls import path
from . import views

app_name = "servicios"

urlpatterns = [
    path("", views.servicio_list, name="list"),
    path("crear/", views.servicio_create, name="create"),
    path("<int:pk>/", views.servicio_detail, name="detail"),
    path("<int:pk>/editar/", views.servicio_update, name="update"),
    path("<int:pk>/eliminar/", views.servicio_delete, name="delete"),

    # tipos
    path("tipos/", views.tipo_list, name="tipo_list"),
    path("tipos/crear/", views.tipo_create, name="tipo_create"),
    path("tipos/<int:pk>/", views.tipo_detail, name="tipo_detail"),        # <-- agregado
    path("tipos/<int:pk>/editar/", views.tipo_update, name="tipo_update"),  # <-- agregado
    path("tipos/<int:pk>/eliminar/", views.tipo_delete, name="tipo_delete"),# <-- agregado

    # Dashboard de gestión (no Django admin)
    path("manage/", views.manage_index, name="manage"),
]
