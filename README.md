GMExpressweb - Resumen
----------------------
Proyecto Django para gestión de catálogo, productos/servicios y citas.

Instalación rápida
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
