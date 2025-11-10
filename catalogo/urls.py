from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy
from .forms import LoginForm   # <-- nuevo import

app_name = "catalogo"

urlpatterns = [
    path("", views.index, name="index"),
    path("acerca/", views.about, name="about"),
    path("categoria/<slug:slug>/", views.categoria, name="categoria"),
    path("categoria/<slug:cat_slug>/producto/<slug:prod_slug>/", views.producto, name="producto"),
    # autenticación
    path("registro/", views.register, name="register"),

    # usar LoginView integrado con formulario personalizado para añadir clases/widgets
    path("login/", auth_views.LoginView.as_view(template_name="login.html", authentication_form=LoginForm), name="login"),
    # usar LogoutView integrado
    path("logout/", auth_views.LogoutView.as_view(next_page=reverse_lazy("catalogo:index")), name="logout"),

    path("perfil/", views.profile, name="profile"),

    # password reset (usar templates/registration/*.html)
    path(
        "password_reset/",
        auth_views.PasswordResetView.as_view(
            template_name="registration/password_reset_form.html",
            success_url=reverse_lazy("catalogo:password_reset_done"),
        ),
        name="password_reset",
    ),
    path(
        "password_reset/done/",
        auth_views.PasswordResetDoneView.as_view(template_name="registration/password_reset_done.html"),
        name="password_reset_done",
    ),
    path(
        "reset/<uidb64>/<token>/",
        auth_views.PasswordResetConfirmView.as_view(
            template_name="registration/password_reset_confirm.html",
            success_url=reverse_lazy("catalogo:password_reset_complete"),
        ),
        name="password_reset_confirm",
    ),
    path(
        "reset/done/",
        auth_views.PasswordResetCompleteView.as_view(template_name="registration/password_reset_complete.html"),
        name="password_reset_complete",
    ),
]
