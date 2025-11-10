from django.contrib import admin
from .models import Appointment

@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ("subject", "user", "scheduled_at", "created_at")
    list_filter = ("scheduled_at",)
    search_fields = ("subject", "notes", "user__email")
