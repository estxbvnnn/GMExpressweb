from django.urls import path
from . import views

app_name = "productos"

urlpatterns = [
    path("", views.product_list, name="list"),
    path("crear/", views.product_create, name="create"),
    path("<int:pk>/", views.product_detail, name="detail"),
    path("<int:pk>/editar/", views.product_update, name="update"),
    path("<int:pk>/eliminar/", views.product_delete, name="delete"),

    # categorías (básico)
    path("categorias/", views.categoria_list, name="categoria_list"),
    path("categorias/crear/", views.categoria_create, name="categoria_create"),
    path("categorias/<int:pk>/", views.categoria_detail, name="categoria_detail"),      # detalle público
    path("categorias/<int:pk>/editar/", views.categoria_update, name="categoria_update"), # editar (staff)
    path("categorias/<int:pk>/eliminar/", views.categoria_delete, name="categoria_delete"),# eliminar (staff)

    # Dashboard de gestión (no Django admin)
    path("manage/", views.manage_index, name="manage"),

    # Rutas para carrito, checkout e historial
    path("carrito/", views.cart_view, name="cart"),
    path("carrito/checkout/", views.cart_checkout, name="cart_checkout"),
    path("<int:pk>/add-to-cart/", views.cart_add, name="add_to_cart"),
    path("historial/", views.purchase_history, name="history"),
]
