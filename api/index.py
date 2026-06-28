import os
import sys
from pathlib import Path

# Ensure the megaone app package is importable
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(BASE_DIR / "megaone"))

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.vercel")

from django.core.wsgi import get_wsgi_application

application = get_wsgi_application()
app = application
