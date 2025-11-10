Instrucciones rápidas para ejecutar GMExpressweb

- Instalar Django 
  pip install "django==4.2.*"

- Migraciones y datos
  python manage.py migrate

Ejecutar servidor
- Ejecuta:
  "python manage.py runserver"
  http://127.0.0.1:8000

Instalación recomendada (Windows / macOS / Linux)

1) Crear y activar un entorno virtual (opcional pero recomendado)
- Windows (PowerShell):
  python -m venv .venv
  .\.venv\Scripts\Activate.ps1
- Windows (cmd):
  python -m venv .venv
  .\.venv\Scripts\activate
- macOS / Linux:
  python3 -m venv .venv
  source .venv/bin/activate

2) Instalar dependencias desde requirements.txt
  pip install -r requirements.txt

3) Alternativa nativa para MySQL (opcional)
- Si prefieres mysqlclient en lugar de PyMySQL, instala:
  pip install mysqlclient
  (En Windows puede requerir Visual C++ Build Tools o un wheel precompilado.)

4) Verificar conexión y migraciones
  python manage.py migrate
  python manage.py runserver

Solución si recibes "pip: El término 'pip' no se reconoce"

- Opción rápida (usar el pip asociado al intérprete Python):
  python -m pip install -r requirements.txt
  # o en sistemas con la utilidad py:
  py -m pip install -r requirements.txt

- Si usas un entorno virtual (recomendado):
  # PowerShell
  python -m venv .venv
  .\.venv\Scripts\Activate.ps1
  pip install -r requirements.txt

  # CMD
  python -m venv .venv
  .\.venv\Scripts\activate
  pip install -r requirements.txt

- Si sigues sin tener pip disponible:
  - Asegúrate de haber marcado "Add Python to PATH" al instalar Python, o reinstala Python y habilita esa opción.
  - Como alternativa usa la ruta completa al ejecutable python: C:\Path\To\Python\python.exe -m pip install -r requirements.txt

Credenciales de prueba (puedes crear tu propio usuario en /registro/):
- Usuario de ejemplo (crear manualmente si prefieres):
  correo: prueba@example.com
  contraseña: Prueba123$

- Cuenta adicional solicitada (creada por el comando createtestuser):
  correo: gcawsesteban@gmail.com
  contraseña: tebyowor123

Prueba rápida:
1) Ejecuta el servidor: python manage.py runserver
2) Abre /registro/ para crear un usuario.
3) Inicia sesión en /login/ y visita /perfil/ (vista protegida).

Notas:
- Asegúrate que el servidor MySQL en 52.54.52.32 esté accesible y que el usuario gm_admin tenga permisos remotos.
- Si usas PyMySQL, el proyecto ya incluye la instrucción para registrarlo como MySQLdb (ver __init__.py del paquete de settings).

Hecho por:
Esteban Ardiles
Carlos Villarroel

Enviar correos (SMTP) — instrucciones rápidas

Por defecto el proyecto usa el backend de consola (EMAIL_BACKEND por defecto) para desarrollo; los correos generados por Django se muestran en la salida de la terminal.

Para enviar correos reales via SMTP configura variables de entorno antes de ejecutar el servidor. Ejemplo (PowerShell):

$env:DJANGO_EMAIL_BACKEND = "smtp"
$env:EMAIL_HOST = "smtp.gmail.com"
$env:EMAIL_PORT = "587"
$env:EMAIL_USE_TLS = "True"
$env:EMAIL_HOST_USER = "tu_email@example.com"
$env:EMAIL_HOST_PASSWORD = "tu_contraseña_o_app_password"
$env:DEFAULT_FROM_EMAIL = "GM Express <no-reply@tudominio.cl>"

En Linux/macOS (bash):

export DJANGO_EMAIL_BACKEND=smtp
export EMAIL_HOST=smtp.gmail.com
export EMAIL_PORT=587
export EMAIL_USE_TLS=True
export EMAIL_HOST_USER=tu_email@example.com
export EMAIL_HOST_PASSWORD=tu_contraseña_o_app_password
export DEFAULT_FROM_EMAIL="GM Express <no-reply@tudominio.cl>"

No pongas credenciales en el repositorio. Para Gmail usa un App Password si tienes verificación en dos pasos.

Crear usuario de prueba

1) Activa tu entorno virtual y asegúrate de haber corrido migraciones:
   python -m pip install -r requirements.txt
   python manage.py migrate

2) Crear el usuario de prueba (prueba@example.com / Prueba123$):
   python manage.py createtestuser

3) Probar restablecimiento de contraseña:
   - Si usas el backend de consola, ejecuta:
       python manage.py runserver
     Luego en la interfaz web ve a /password_reset/ y envía el correo; el enlace aparecerá en la terminal.
   - Si configuraste SMTP correctamente, recibirás el correo en la bandeja del usuario.

Pruebas
1) Activa el entorno virtual e instala dependencias: python -m pip install -r requirements.txt
2) Corre migraciones: python manage.py migrate
3) Crea usuario de prueba (opcional): python manage.py createtestuser
4) Ejecuta el servidor: python manage.py runserver
5) Regístrate en /registro/ y verifica que:
   - Si usas console backend, el correo se mostrará en la consola donde corre runserver.
   - Si configuraste SMTP correctamente, el correo llegará a la bandeja del usuario.

Nota:
- Para Gmail: si tienes verificación en dos pasos, crea un App Password y úsalo en EMAIL_HOST_PASSWORD.
- Asegúrate de no subir credenciales al repositorio; usa variables de entorno.

Configuración rápida de SMTP (local, no almacenar en el repo)

PowerShell (ejecuta en la misma sesión antes de arrancar runserver):
$env:DJANGO_EMAIL_BACKEND = "smtp"
$env:EMAIL_HOST = "smtp.gmail.com"
$env:EMAIL_PORT = "587"
$env:EMAIL_USE_TLS = "True"
$env:EMAIL_HOST_USER = "estebanardiles333@gmail.com"
$env:EMAIL_HOST_PASSWORD = "T3bysinho12$"
$env:DEFAULT_FROM_EMAIL = "GM Express <estebanardiles333@gmail.com>"

Bash / macOS / Linux:
export DJANGO_EMAIL_BACKEND=smtp
export EMAIL_HOST=smtp.gmail.com
export EMAIL_PORT=587
export EMAIL_USE_TLS=True
export EMAIL_HOST_USER=estebanardiles333@gmail.com
export EMAIL_HOST_PASSWORD='T3bysinho12$'
export DEFAULT_FROM_EMAIL="GM Express <estebanardiles333@gmail.com>"

Notas:
- Gmail suele requerir un App Password si tienes verificación en dos pasos. Si usas Gmail y no tienes App Password, revisa esta guía y crea un App Password y usa ese valor en EMAIL_HOST_PASSWORD.
- Estas variables son locales: no las comites al repositorio. Para producción usa un sistema seguro (vault, secret manager o variables del entorno del servidor).
- Tras exportar/establecer las variables, ejecuta:
  python manage.py runserver
  y prueba registro o /password_reset/; los correos se enviarán por SMTP.

Nota:
- Estas cuentas se crean localmente con:
  python manage.py createtestuser
- No subas credenciales reales al repositorio; usa variables de entorno para SMTP y secretos.

Probar envío real (SMTP) sin usar la salida de la terminal

1) Establece las variables de entorno (PowerShell ejemplo):
$env:DJANGO_EMAIL_BACKEND = "smtp"
$env:EMAIL_HOST = "smtp.gmail.com"
$env:EMAIL_PORT = "587"
$env:EMAIL_USE_TLS = "True"
$env:EMAIL_HOST_USER = "tu_email@gmail.com"
$env:EMAIL_HOST_PASSWORD = "TU_APP_PASSWORD"
$env:DEFAULT_FROM_EMAIL = "GM Express <tu_email@gmail.com>"

2) En la misma sesión, arranca el servidor o simplemente prueba con el comando de gestión:
   python manage.py sendtestemail --to tu_email_destino@example.com

   - Si el comando responde "Correo de prueba enviado a ..." y recibes el email en la bandeja (revisa spam), la configuración SMTP funciona.
   - Si falla, revisa el error mostrado y comprueba: credenciales, App Password (Gmail), puerto/TLS, firewall.

Notas:
- Gmail requiere App Password si tienes verificación en dos pasos; no uses la contraseña de cuenta normal.
- No guardes credenciales en el repositorio. Usa variables de entorno o un gestor de secretos.
