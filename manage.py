#!/usr/bin/env python
import os
import sys
from pathlib import Path

# Añadir la carpeta raíz del proyecto al sys.path para que pueda importarse el paquete 'web'
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

def main():
    # Usar los settings que están dentro de GMExpressweb/GMExpress/settings.py
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "GMExpressweb.GMExpress.settings")
    try:
        from django.core.management import execute_from_command_line
    except ImportError:
        raise
    execute_from_command_line(sys.argv)

main()
