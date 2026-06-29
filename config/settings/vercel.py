from .base import *  # noqa: F403
from .base import DATABASES
from .base import STORAGES
from .base import env

SECRET_KEY = env("SECRET_KEY", default=env("DJANGO_SECRET_KEY", default="insecure-change-me"))
DEBUG = env.bool("DEBUG", default=False)
ALLOWED_HOSTS = env.list(
    "DJANGO_ALLOWED_HOSTS",
    default=[".vercel.app", ".onrender.com", "localhost", "127.0.0.1"],
)

# Serverless: don't persist database connections across function invocations
DATABASES["default"]["CONN_MAX_AGE"] = 0

# Use whitenoise to serve static files in serverless environment
# It finds files via STATICFILES_DIRS and app static/ dirs without collectstatic
WHITENOISE_USE_FINDERS = True
WHITENOISE_MANIFEST_STRICT = False
WHITENOISE_AUTOREFRESH = True

STORAGES["staticfiles"]["BACKEND"] = "whitenoise.storage.CompressedStaticFilesStorage"

ADMIN_URL = env("DJANGO_ADMIN_URL", default="admin/")

# Security - trust Vercel's proxy headers
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
CSRF_TRUSTED_ORIGINS = env.list(
    "DJANGO_CSRF_TRUSTED_ORIGINS",
    default=["https://*.vercel.app"],
)

# Disable SSL-sensitive settings on Vercel's proxy
SECURE_SSL_REDIRECT = env.bool("DJANGO_SECURE_SSL_REDIRECT", default=False)
SESSION_COOKIE_SECURE = env.bool("DJANGO_SESSION_COOKIE_SECURE", default=False)
CSRF_COOKIE_SECURE = env.bool("DJANGO_CSRF_COOKIE_SECURE", default=False)
