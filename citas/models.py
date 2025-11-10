from django.db import models
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.utils.timezone import is_naive, make_aware
from datetime import timedelta

User = get_user_model()

class Appointment(models.Model):
    STATUS_CHOICES = [
        ("scheduled", "Programada"),
        ("confirmed", "Confirmada"),
        ("cancelled", "Cancelada"),
        ("completed", "Completada"),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="appointments")
    scheduled_at = models.DateTimeField()
    duration_minutes = models.PositiveIntegerField(default=60)  # duración en minutos
    subject = models.CharField(max_length=150)
    notes = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="scheduled")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["scheduled_at"]
        # unique_together = ("user", "scheduled_at")  # removed to allow overlapping control in clean()

    # Cambiado a property para facilitar el uso en templates
    @property
    def end_time(self):
        return self.scheduled_at + timedelta(minutes=self.duration_minutes)

    def clean(self):
        # Normalizar scheduled_at si es naive (usar timezone actual)
        if self.scheduled_at and is_naive(self.scheduled_at):
            try:
                self.scheduled_at = make_aware(self.scheduled_at, timezone.get_current_timezone())
            except Exception:
                # si falla awareness, dejar como está y seguir (las validaciones posteriores detectarán problemas)
                pass

        # Validaciones básicas de campos
        if not self.subject or not self.subject.strip():
            raise ValidationError("El asunto de la cita no puede estar vacío.")
        if len(self.subject.strip()) > 150:
            raise ValidationError("El asunto es demasiado largo (máx. 150 caracteres).")
        if self.duration_minutes is None or self.duration_minutes <= 0:
            raise ValidationError("La duración debe ser un valor positivo en minutos.")
        if self.notes and len(self.notes) > 2000:
            raise ValidationError("Las notas son demasiado largas (máx. 2000 caracteres).")

        # Validaciones de fecha/tiempo
        now = timezone.now()

        # Si no hay scheduled_at definido, salir de validaciones dependientes de la fecha
        if not self.scheduled_at:
            super().clean()
            return

        if self.scheduled_at <= now:
            raise ValidationError("No se puede agendar una cita en el pasado.")

        # Aviso mínimo: al menos 1 hora antes
        min_notice = now + timedelta(hours=1)
        if self.scheduled_at < min_notice:
            raise ValidationError("Debe agendar con al menos 1 hora de anticipación.")

        # Horario de atención (08:00 - 20:00, hora local)
        sch_local = self.scheduled_at.astimezone(timezone.get_current_timezone())
        start_hour = 8
        end_hour = 20
        if not (start_hour <= sch_local.hour < end_hour):
            raise ValidationError(f"Las citas solo pueden agendarse entre las {start_hour}:00 y las {end_hour}:00.")

        # Evitar solapamientos con otras citas del mismo usuario
        user = getattr(self, "user", None)
        if user:
            qs = Appointment.objects.filter(user=user).exclude(pk=self.pk)
            for other in qs:
                other_start = other.scheduled_at
                other_end = other.end_time
                this_start = self.scheduled_at
                this_end = self.end_time
                # overlap if start < other_end and other_start < end
                if (this_start < other_end) and (other_start < this_end):
                    raise ValidationError("Esta cita solapa con otra cita existente. Elimina o re-programa la otra cita primero.")

            # Evitar duplicados exactos (mismo usuario, misma fecha/hora, misma duración y mismo asunto)
            dup_qs = qs.filter(
                scheduled_at=self.scheduled_at,
                duration_minutes=self.duration_minutes,
                subject__iexact=self.subject.strip()
            )
            if dup_qs.exists():
                raise ValidationError("Ya existe una cita idéntica para esta fecha/hora. Evita crear duplicados.")

        super().clean()

    def __str__(self):
        return f"{self.subject} @ {self.scheduled_at} ({self.user})"
