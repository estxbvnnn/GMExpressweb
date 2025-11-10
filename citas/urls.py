from django.urls import path
from . import views

app_name = "citas"

urlpatterns = [
    path("", views.appointment_list, name="list"),
    path("crear/", views.appointment_create, name="create"),
    path("<int:pk>/", views.appointment_detail, name="detail"),
    path("<int:pk>/editar/", views.appointment_update, name="update"),
    path("<int:pk>/eliminar/", views.appointment_delete, name="delete"),

    # Dashboard de gestión (staff web UI)
    path("manage/", views.appointment_manage, name="manage"),
    path("manage/<int:pk>/action/", views.appointment_manage_action, name="manage_action"),
]
