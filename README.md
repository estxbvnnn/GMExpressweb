GMExpressweb - Resumen
----------------------
Proyecto Django para gestión de catálogo, productos/servicios y citas.

Instalación rápida
- Crear/activar virtualenv
- pip install -r requirements.txt
- python manage.py migrate
- python manage.py createtestuser
- python manage.py runserver

Credenciales de prueba
- admin / admin1

Reglas de negocio implementadas (citas)
- No se puede agendar una cita en el pasado (validación en modelo y formulario).
- No se permiten duplicados exactos (mismo usuario + misma fecha/hora) (unique_together).
- CRUD de citas protegido: solo usuarios autenticados pueden crear/editar/ver/eliminar sus propias citas.

Cómo probar recuperación de contraseña y envíos
- Configurar variables de entorno SMTP (ver readme.dm) o usar console email backend.
- Crear usuario de prueba y usar /password_reset/ para el flujo.
