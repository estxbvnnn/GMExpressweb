from django.core.management.base import BaseCommand
from django.core.mail import send_mail, EmailMessage, get_connection
from django.conf import settings
import smtplib
import ssl
import traceback

class Command(BaseCommand):
    help = "Envía un correo de prueba. Uso: python manage.py sendtestemail --to you@example.com [--host HOST --port PORT --tls --ssl --user USER --password PASS --from FROM]"

    def add_arguments(self, parser):
        parser.add_argument("--to", required=True, help="Email destinatario")
        parser.add_argument("--host", help="SMTP host (ej: smtp.gmail.com)")
        parser.add_argument("--port", type=int, help="SMTP port (ej: 587)")
        parser.add_argument("--tls", action="store_true", help="Usar STARTTLS")
        parser.add_argument("--ssl", action="store_true", help="Usar SSL")
        parser.add_argument("--user", help="SMTP username")
        parser.add_argument("--password", help="SMTP password")
        parser.add_argument("--from", dest="from_email", help="From header (ej: 'GM Express <no-reply@...>')")
        parser.add_argument("--backend", help="Backend Django (ej: smtp)")

    def handle(self, *args, **options):
        to = options["to"]
        subject = "Correo de prueba - GM Express"
        message = "Este es un correo de prueba enviado desde el proyecto GMExpressweb usando la configuración SMTP."
        # valores: prioridad CLI -> settings
        host = options.get("host") or getattr(settings, "EMAIL_HOST", None)
        port = options.get("port") or getattr(settings, "EMAIL_PORT", None)
        use_tls = options.get("tls") or getattr(settings, "EMAIL_USE_TLS", False)
        use_ssl = options.get("ssl") or getattr(settings, "EMAIL_USE_SSL", False)
        user = options.get("user") or getattr(settings, "EMAIL_HOST_USER", "")
        password = options.get("password") or getattr(settings, "EMAIL_HOST_PASSWORD", "")
        from_email = options.get("from_email") or getattr(settings, "DEFAULT_FROM_EMAIL", "no-reply@example.com")
        backend_opt = options.get("backend") or os_backend_name(getattr(settings, "EMAIL_BACKEND", None))

        # Mostrar configuración (útil para diagnóstico)
        self.stdout.write("Configuración efectiva usada:")
        self.stdout.write(f"  backend flag = {backend_opt}")
        self.stdout.write(f"  host = {host}")
        self.stdout.write(f"  port = {port}")
        self.stdout.write(f"  use_tls = {use_tls}")
        self.stdout.write(f"  use_ssl = {use_ssl}")
        self.stdout.write(f"  user = {user}")
        self.stdout.write(f"  from = {from_email}")

        # Probar conexión SMTP directa si hay host/port
        if host and port:
            try:
                self.stdout.write("Probando conexión SMTP directa...")
                if use_ssl:
                    context = ssl.create_default_context()
                    with smtplib.SMTP_SSL(host, port, timeout=15, context=context) as smtp:
                        if user:
                            smtp.login(user, password)
                else:
                    with smtplib.SMTP(host, port, timeout=15) as smtp:
                        smtp.ehlo()
                        if use_tls:
                            smtp.starttls()
                            smtp.ehlo()
                        if user:
                            smtp.login(user, password)
                self.stdout.write(self.style.SUCCESS("Conexión SMTP / login OK"))
            except Exception as e:
                self.stdout.write(self.style.ERROR("Falló la conexión SMTP o autenticación:"))
                self.stdout.write(self.style.ERROR(str(e)))
                self.stdout.write(self.style.ERROR("Traza completa:"))
                self.stdout.write(traceback.format_exc())
                self.stdout.write(self.style.WARNING("Verifica: HOST/PORT, TLS/SSL, USER, PASSWORD (App Password si Gmail), y firewall/ISP."))
                return
        else:
            self.stdout.write(self.style.WARNING("No hay HOST/PORT definido; se usará la configuración de Django (puede ser console backend)."))

        # Intentar enviar el correo usando Django, creando una conexión con los parámetros (si corresponde)
        try:
            # Determinar backend path
            backend_path = "django.core.mail.backends.smtp.EmailBackend" if backend_opt == "smtp" else getattr(settings, "EMAIL_BACKEND", "django.core.mail.backends.console.EmailBackend")
            # Crear conexión con parámetros efectivos (si SMTP)
            conn_kwargs = {}
            if backend_path.endswith("smtp.EmailBackend"):
                conn_kwargs = {
                    "host": host,
                    "port": port,
                    "username": user,
                    "password": password,
                    "use_tls": use_tls,
                    "use_ssl": use_ssl,
                }
            connection = get_connection(backend=backend_path, **{k: v for k, v in conn_kwargs.items() if v not in (None, "")})
            email = EmailMessage(subject, message, from_email, [to], connection=connection)
            email.send(fail_silently=False)
            self.stdout.write(self.style.SUCCESS(f"Correo de prueba enviado a {to}"))
            self.stdout.write(self.style.SUCCESS("Revisa bandeja y SPAM."))
        except Exception as e:
            self.stdout.write(self.style.ERROR("Error enviando correo via Django:"))
            self.stdout.write(self.style.ERROR(str(e)))
            self.stdout.write(self.style.ERROR("Traza completa:"))
            self.stdout.write(traceback.format_exc())
            self.stdout.write(self.style.WARNING("Si usas Gmail: usa App Password y asegúrate que DEFAULT_FROM_EMAIL coincida con la cuenta autenticada."))


def os_backend_name(backend_setting):
    """
    Normaliza el nombre de backend para CLI (acepta 'smtp' o la ruta completa).
    """
    if not backend_setting:
        return None
    if "smtp" in str(backend_setting).lower():
        return "smtp"
    return backend_setting
