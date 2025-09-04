from django.urls import path
from . import views

app_name = "catalogo"

urlpatterns = [
    path("", views.index, name="index"),
    path("acerca/", views.about, name="about"),
    path("categoria/<slug:slug>/", views.categoria, name="categoria"),
    path("categoria/<slug:cat_slug>/producto/<slug:prod_slug>/", views.producto, name="producto"),
]
