from django.core.management.base import BaseCommand
from django.contrib.auth.models import User

class Command(BaseCommand):
    help = "Crea usuarios de prueba si no existen."

    def handle(self, *args, **options):
        users = [
            ("prueba@example.com", "Prueba123$"),
            ("gcawsesteban@gmail.com", "tebyowor123"),
        ]
        for email, password in users:
            if User.objects.filter(username=email).exists():
                self.stdout.write(self.style.WARNING(f"Usuario {email} ya existe."))
                continue
            user = User.objects.create_user(
                username=email,
                email=email,
                password=password,
                first_name="Prueba" if email.startswith("prueba") else "Esteban",
                last_name="Usuario" if email.startswith("prueba") else "Cuenta",
            )
            user.is_active = True
            user.save()
            self.stdout.write(self.style.SUCCESS(f"Usuario creado: {email} / {password}"))
