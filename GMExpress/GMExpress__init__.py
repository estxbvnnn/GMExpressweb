# Registrar PyMySQL para que actúe como MySQLdb (si instalaste PyMySQL)
try:
    import pymysql
    pymysql.install_as_MySQLdb()
except Exception:
    # Si PyMySQL no está instalado, la instalación con mysqlclient seguirá funcionando.
    pass