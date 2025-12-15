from django.shortcuts import render, Http404, redirect
from django.urls import reverse
from .models import CATALOGOS
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from .forms import RegisterForm
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.conf import settings
from citas.models import Appointment
from django.utils import timezone
from django.contrib import messages
from io import StringIO
from django.core.management import call_command

def index(request):
    contexto = {"categorias": CATALOGOS, "empresa": empresa_info()}
    return render(request, "index.html", contexto)

def categoria(request, slug):
    categoria = next((c for c in CATALOGOS if c["slug"] == slug), None)
    if not categoria:
        raise Http404("Categoría no encontrada")
    contexto = {"categoria": categoria, "empresa": empresa_info()}
    return render(request, "categoria.html", contexto)

def producto(request, cat_slug, prod_slug):
    categoria = next((c for c in CATALOGOS if c["slug"] == cat_slug), None)
    if not categoria:
        raise Http404("Categoría no encontrada")
    producto = next((p for p in categoria["productos"] if p["slug"] == prod_slug), None)
    if not producto:
        raise Http404("Producto no encontrado")
    if producto.get("slug") == "almuerzo-tradicional" and not producto.get("imagen"):
        producto["imagen"] = "templates/almuerzotradicional.png"
    contexto = {"categoria": categoria, "producto": producto, "empresa": empresa_info()}
    return render(request, "producto.html", contexto)

def about(request):
    contexto = {"empresa": empresa_info()}
    return render(request, "about.html", contexto)

# --- Nuevas vistas de autenticación ---

def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            # crear usuario
            user = User.objects.create_user(
                username=data["email"],
                email=data["email"],
                password=data["password1"],
                first_name=data["first_name"],
                last_name=data["last_name"],
            )
            user.is_active = True
            user.save()

            # Enviar correo de bienvenida (si falla no impide el registro)
            try:
                subject = "Bienvenido a GM Express"
                message = (
                    f"Hola {user.first_name},\n\n"
                    "Gracias por registrarte en GM Express.\n\n"
                    "Puedes iniciar sesión en: http://127.0.0.1:8000/login/\n\n"
                    "Saludos,\nGM Express"
                )
                send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [user.email], fail_silently=False)
            except Exception:
                pass

            messages.success(request, "Cuenta creada correctamente. Bienvenido/a.")

            # Iniciar sesión automático tras registro
            user = authenticate(request, username=data["email"], password=data["password1"])
            if user:
                login(request, user)
                return redirect("catalogo:profile")
            return redirect("catalogo:login")
        else:
            # mostrar mensaje de error general para que SweetAlert lo muestre
            errors = form.errors.as_json()
            messages.error(request, "Corrige los errores del formulario antes de continuar.")
    else:
        form = RegisterForm()
    return render(request, "register.html", {"form": form, "empresa": empresa_info()})

def login_view(request):
    error = None
    if request.method == "POST":
        email = request.POST.get("email", "").strip()
        password = request.POST.get("password", "")
        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)
            return redirect("catalogo:profile")
        error = "Correo o contraseña incorrectos."
    return render(request, "login.html", {"error": error, "empresa": empresa_info()})

def logout_view(request):
    logout(request)
    # redirige a la URL absoluta usando el host de la petición (evita redirigir a localhost)
    absolute_index = request.build_absolute_uri(reverse("catalogo:index"))
    return redirect(absolute_index)

@login_required
def profile(request):
    # obtener próximas 5 citas del usuario
    upcoming_qs = Appointment.objects.filter(user=request.user, scheduled_at__gt=timezone.now()).order_by("scheduled_at")[:5]
    contexto = {
        "usuario": request.user,
        "empresa": empresa_info(),
        "upcoming": upcoming_qs,
        "upcoming_count": upcoming_qs.count(),
    }
    return render(request, "profile.html", contexto)

@user_passes_test(lambda u: u.is_active and (u.is_staff or u.is_superuser))
def import_catalog_to_db(request):
    buf = StringIO()
    try:
        call_command("import_catalog", stdout=buf)
        messages.success(request, f"Catálogo importado. Resultado:\n{buf.getvalue()}")
    except Exception as e:
        messages.error(request, f"Error al importar catálogo: {e}")
    return redirect("catalogo:index")

def empresa_info():
    return {
        "nombre": "GM Express",
        "historia": "GM Express nace para ofrecer soluciones alimentarias eficientes y de calidad en instituciones y eventos.",
        "mision": "Entregar alimentos saludables y servicios profesionales que faciliten la alimentación institucional y de eventos.",
        "vision": "Ser referente en gestión alimentaria en colegios, universidades y eventos en Chile.",
        "valores": ["Calidad", "Responsabilidad", "Sostenibilidad", "Compromiso"],
        "contactos": {"telefono": "+56 9 7615 9518", "email": "ventas@gmexpress.cl", "direccion": "Gerónimo Méndez 1851, Barrio Industrial, Coquimbo"},
        "redes": {
            "facebook": "https://www.facebook.com/GMEXPRESSCL",
            "instagram": "https://www.instagram.com/gmexpress_cl/?hl=es",
            "twitter": "#"
        },
    }
