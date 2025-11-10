# nuevo archivo
from django.core.management.base import BaseCommand
from django.db import connections, DEFAULT_DB_ALIAS, OperationalError

class Command(BaseCommand):
    help = "Verifica la conexión a la base de datos configurada (intentará SELECT VERSION())."

    def handle(self, *args, **options):
        db = DEFAULT_DB_ALIAS
        self.stdout.write(f"Probando conexión a la base de datos ('{db}')...")
        try:
            conn = connections[db]
            conn.ensure_connection()
            with conn.cursor() as cursor:
                cursor.execute("SELECT VERSION()")
                version = cursor.fetchone()[0]
            self.stdout.write(self.style.SUCCESS(f"Conexión establecida. Versión del servidor DB: {version}"))
        except OperationalError as e:
            self.stdout.write(self.style.ERROR(f"Error de conexión a la DB: {e}"))
            self.stdout.write("Revisa: host/puerto, firewall, usuario/host en MySQL (GRANT), y que MySQL escuche en la IP externa (bind-address).")
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Error inesperado: {e}"))
