from pathlib import Path
from django.apps import AppConfig

class CatalogoConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "catalogo"
    verbose_name = "Catálogo GM Express"
    path = Path(__file__).resolve().parent
