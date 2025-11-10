from django import forms
from .models import Appointment
from django.utils import timezone

class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ["scheduled_at", "duration_minutes", "subject", "notes"]
        widgets = {
            "scheduled_at": forms.DateTimeInput(attrs={"type": "datetime-local", "class": "form-control"}),
            "duration_minutes": forms.NumberInput(attrs={"class": "form-control", "min": 30, "max": 240}),
            "subject": forms.TextInput(attrs={"class": "form-control", "maxlength": 150}),
            "notes": forms.Textarea(attrs={"class": "form-control", "rows": 3, "maxlength": 2000}),
        }

    def clean_scheduled_at(self):
        dt = self.cleaned_data.get("scheduled_at")
        if dt and dt <= timezone.now():
            raise forms.ValidationError("La fecha y hora deben ser en el futuro.")
        return dt

    def clean_duration_minutes(self):
        d = self.cleaned_data.get("duration_minutes")
        if d is None:
            return d
        if d < 30 or d > 240:
            raise forms.ValidationError("La duración debe estar entre 30 y 240 minutos.")
        return d

    def clean_subject(self):
        s = (self.cleaned_data.get("subject") or "").strip()
        if not s:
            raise forms.ValidationError("El asunto no puede estar vacío.")
        if len(s) > 150:
            raise forms.ValidationError("El asunto es demasiado largo (máx. 150 caracteres).")
        return s

    def clean_notes(self):
        n = self.cleaned_data.get("notes") or ""
        if len(n) > 2000:
            raise forms.ValidationError("Las notas son demasiado largas (máx. 2000 caracteres).")
        return n
