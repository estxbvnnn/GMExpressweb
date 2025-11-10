from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Servicio, TipoServicio
from .forms import ServicioForm, TipoServicioForm
from django.contrib import messages

# Dashboard de gestión (solo staff)
staff_required = user_passes_test(lambda u: u.is_active and (u.is_staff or u.is_superuser))

@staff_required
def manage_index(request):
    total = Servicio.objects.count()
    tipos = TipoServicio.objects.count()
    recientes = Servicio.objects.order_by("-id")[:6]
    return render(request, "servicios/manage.html", {
        "total": total,
        "tipos": tipos,
        "recientes": recientes,
    })

def servicio_list(request):
    # Mostrar solo servicios cuyo estado sea 'activo'
    qs = Servicio.objects.filter(estado="activo").order_by("tipo__nombre", "nombre")
    return render(request, "servicios/list.html", {"servicios": qs})

def servicio_detail(request, pk):
    # Evitar 404 crudo: redirigir al listado con mensaje si no existe
    try:
        s = Servicio.objects.get(pk=pk)
    except Servicio.DoesNotExist:
        messages.error(request, "Servicio no encontrado.")
        return redirect("servicios:list")
    return render(request, "servicios/detail.html", {"servicio": s})

# mutaciones restringidas a staff/superuser
@staff_required
def servicio_create(request):
    if request.method == "POST":
        form = ServicioForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Servicio creado.")
            return redirect("servicios:list")
    else:
        form = ServicioForm()
    return render(request, "servicios/form.html", {"form": form, "action": "Crear"})

@staff_required
def servicio_update(request, pk):
    # manejar caso "no existe" de manera amigable
    try:
        s = Servicio.objects.get(pk=pk)
    except Servicio.DoesNotExist:
        messages.error(request, "Servicio no encontrado.")
        return redirect("servicios:manage")
    if request.method == "POST":
        form = ServicioForm(request.POST, instance=s)
        if form.is_valid():
            form.save()
            messages.success(request, "Servicio actualizado.")
            return redirect("servicios:detail", pk=s.pk)
    else:
        form = ServicioForm(instance=s)
    return render(request, "servicios/form.html", {"form": form, "action": "Editar"})

@staff_required
def servicio_delete(request, pk):
    s = get_object_or_404(Servicio, pk=pk)
    if request.method == "POST":
        s.delete()
        messages.success(request, "Servicio eliminado.")
        return redirect("servicios:list")
    return render(request, "servicios/form.html", {"confirm_delete": True, "obj": s, "action": "Eliminar"})

# Tipos
def tipo_list(request):
    qs = TipoServicio.objects.all().order_by("nombre")
    return render(request, "servicios/tipo_list.html", {"tipos": qs})

@staff_required
def tipo_create(request):
    if request.method == "POST":
        form = TipoServicioForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Tipo de servicio creado.")
            return redirect("servicios:tipo_list")
    else:
        form = TipoServicioForm()
    return render(request, "servicios/tipo_form.html", {"form": form, "action": "Crear tipo"})

# ---- Nuevas vistas para TipoServicio ----
def tipo_detail(request, pk):
    t = get_object_or_404(TipoServicio, pk=pk)
    return render(request, "servicios/tipo_detail.html", {"tipo": t})

@staff_required
def tipo_update(request, pk):
    t = get_object_or_404(TipoServicio, pk=pk)
    if request.method == "POST":
        form = TipoServicioForm(request.POST, instance=t)
        if form.is_valid():
            form.save()
            messages.success(request, "Tipo de servicio actualizado.")
            return redirect("servicios:tipo_list")
    else:
        form = TipoServicioForm(instance=t)
    return render(request, "servicios/tipo_form.html", {"form": form, "action": "Editar tipo"})

@staff_required
def tipo_delete(request, pk):
    t = get_object_or_404(TipoServicio, pk=pk)
    if request.method == "POST":
        t.delete()
        messages.success(request, "Tipo de servicio eliminado.")
        return redirect("servicios:tipo_list")
    # confirmación mínima (usa mismo form template)
    return render(request, "servicios/tipo_form.html", {"confirm_delete": True, "obj": t, "action": "Eliminar tipo"})
