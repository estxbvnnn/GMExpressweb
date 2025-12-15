# Register PyMySQL as MySQLdb fallback
try:
    import pymysql
    pymysql.install_as_MySQLdb()
except Exception:
    # If PyMySQL is not installed, mysqlclient may be used instead.
    pass
