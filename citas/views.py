from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Appointment
from .forms import AppointmentForm
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.urls import reverse
from django.utils import timezone

@login_required
def appointment_list(request):
    qs = Appointment.objects.filter(user=request.user).order_by("scheduled_at")
    return render(request, "citas/list.html", {"appointments": qs})

@login_required
def appointment_create(request):
    if request.method == "POST":
        form = AppointmentForm(request.POST)
        if form.is_valid():
            ap = form.save(commit=False)
            ap.user = request.user
            try:
                ap.full_clean()
                ap.save()
                # enviar notificación
                try:
                    subject = f"Cita programada: {ap.subject}"
                    message = f"Hola {request.user.get_full_name() or request.user.username},\n\nTu cita '{ap.subject}' fue programada para {ap.scheduled_at} (duración {ap.duration_minutes} min).\n\nVer: {request.build_absolute_uri(reverse('citas:detail', args=[ap.pk]))}"
                    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [request.user.email], fail_silently=True)
                except Exception:
                    pass
                messages.success(request, "Cita creada correctamente.")
                return redirect("citas:list")
            except Exception as e:
                form.add_error(None, e)
    else:
        form = AppointmentForm()
    return render(request, "citas/form.html", {"form": form, "action": "Crear"})

@login_required
def appointment_update(request, pk):
    ap = get_object_or_404(Appointment, pk=pk, user=request.user)
    if request.method == "POST":
        form = AppointmentForm(request.POST, instance=ap)
        if form.is_valid():
            ap = form.save(commit=False)
            try:
                ap.full_clean()
                ap.save()
                try:
                    subject = f"Cita actualizada: {ap.subject}"
                    message = f"Tu cita '{ap.subject}' fue actualizada. Nueva fecha: {ap.scheduled_at} (duración {ap.duration_minutes} min).\n\nVer: {request.build_absolute_uri(reverse('citas:detail', args=[ap.pk]))}"
                    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [request.user.email], fail_silently=True)
                except Exception:
                    pass
                messages.success(request, "Cita actualizada.")
                return redirect("citas:list")
            except Exception as e:
                form.add_error(None, e)
    else:
        form = AppointmentForm(instance=ap)
    return render(request, "citas/form.html", {"form": form, "action": "Editar"})

@login_required
def appointment_delete(request, pk):
    ap = get_object_or_404(Appointment, pk=pk, user=request.user)
    if request.method == "POST":
        subject = f"Cita cancelada: {ap.subject}"
        message = f"Tu cita '{ap.subject}' programada para {ap.scheduled_at} fue cancelada."
        ap.delete()
        try:
            send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [request.user.email], fail_silently=True)
        except Exception:
            pass
        messages.success(request, "Cita eliminada.")
        return redirect("citas:list")
    return render(request, "citas/confirm_delete.html", {"appointment": ap})

@login_required
def appointment_detail(request, pk):
    ap = get_object_or_404(Appointment, pk=pk, user=request.user)
    return render(request, "citas/detail.html", {"appointment": ap})

# Dashboard de gestión (solo staff)
staff_required = user_passes_test(lambda u: u.is_active and u.is_staff)

@staff_required
def appointment_manage(request):
    qs = Appointment.objects.order_by("-scheduled_at")
    return render(request, "citas/manage.html", {"appointments": qs})

@staff_required
def appointment_manage_action(request, pk):
    ap = get_object_or_404(Appointment, pk=pk)
    if request.method == "POST":
        action = request.POST.get("action")
        if action == "confirm":
            ap.status = "confirmed"
            ap.save()
            messages.success(request, "Cita marcada como Confirmada.")
        elif action == "cancel":
            ap.status = "cancelled"
            ap.save()
            messages.success(request, "Cita marcada como Cancelada.")
        elif action == "delete":
            ap.delete()
            messages.success(request, "Cita eliminada.")
        else:
            messages.error(request, "Acción desconocida.")
    return redirect("citas:manage")
