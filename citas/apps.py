from pathlib import Path
from django.apps import AppConfig

class CitasConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "citas"
    verbose_name = "Gestión de Citas"
    path = Path(__file__).resolve().parent
