from django.contrib import admin
from .models import Appointment

@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ("subject", "user", "scheduled_at", "end_time", "status", "created_at")
    list_filter = ("status", "user", "scheduled_at")
    search_fields = ("subject", "notes", "user__email")
    date_hierarchy = "scheduled_at"
    ordering = ("-scheduled_at",)
    readonly_fields = ("created_at",)
    actions = ("mark_confirmed", "mark_cancelled")

    def end_time(self, obj):
        return obj.end_time
    end_time.short_description = "Fin"

    @admin.action(description="Marcar seleccionadas como Confirmadas")
    def mark_confirmed(self, request, queryset):
        updated = queryset.update(status="confirmed")
        self.message_user(request, f"{updated} cita(s) marcadas como Confirmada(s).")

    @admin.action(description="Marcar seleccionadas como Canceladas")
    def mark_cancelled(self, request, queryset):
        updated = queryset.update(status="cancelled")
        self.message_user(request, f"{updated} cita(s) marcadas como Cancelada(s).")
