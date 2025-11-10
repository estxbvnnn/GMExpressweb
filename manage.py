import os
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent 
sys.path.insert(0, str(PROJECT_ROOT))

def main():
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "GMExpress.settings")
    try:
        from django.core.management import execute_from_command_line
    except ImportError:
        raise
    execute_from_command_line(sys.argv)

main()
