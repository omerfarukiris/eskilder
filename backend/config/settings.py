"""Eskilder Django ayarları. Tüm gizli/ortama bağlı değerler ortam değişkenlerinden okunur."""
import os
from pathlib import Path

import dj_database_url

BASE_DIR = Path(__file__).resolve().parent.parent


def ortam(ad, varsayilan=""):
    return os.environ.get(ad, varsayilan)


def ortam_bool(ad, varsayilan=False):
    return ortam(ad, str(varsayilan)).lower() in {"1", "true", "yes", "evet"}


DEBUG = ortam_bool("DEBUG", False)
SECRET_KEY = ortam("SECRET_KEY") or ("yerel-gelistirme-anahtari" if DEBUG or "pytest" in os.sys.modules else "")
if not SECRET_KEY:
    raise RuntimeError("SECRET_KEY ortam değişkeni tanımlı değil.")

ALLOWED_HOSTS = [h.strip() for h in ortam("ALLOWED_HOSTS", "localhost,127.0.0.1,testserver").split(",") if h.strip()]
CSRF_TRUSTED_ORIGINS = [f"https://{h.lstrip('.')}" for h in ALLOWED_HOSTS if h not in {"localhost", "127.0.0.1", "testserver"}]
SITE_URL = ortam("SITE_URL", "http://localhost:5173").rstrip("/")
CRON_SECRET = ortam("CRON_SECRET")

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "rest_framework",
    "saglik",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "config.urls"
WSGI_APPLICATION = "config.wsgi.application"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

# Veritabanı: DATABASE_URL yoksa yerel SQLite. Supabase pooler (transaction mode) için
# kalıcı bağlantı, sunucu tarafı imleç ve prepared statement kapalı.
_db_url = ortam("DATABASE_URL")
if _db_url:
    _db = dj_database_url.parse(_db_url, conn_max_age=0)
    _db["DISABLE_SERVER_SIDE_CURSORS"] = True
    _db.setdefault("OPTIONS", {})["prepare_threshold"] = None
    DATABASES = {"default": _db}
else:
    DATABASES = {"default": {"ENGINE": "django.db.backends.sqlite3", "NAME": BASE_DIR / "db.sqlite3"}}

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

LANGUAGE_CODE = "tr"
TIME_ZONE = "Europe/Istanbul"
USE_I18N = True
USE_TZ = True

STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR.parent / "frontend" / "public" / "static"
MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

if not DEBUG:
    SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
    SESSION_COOKIE_SECURE = ortam_bool("SECURE_COOKIES", True)
    CSRF_COOKIE_SECURE = ortam_bool("SECURE_COOKIES", True)

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {"console": {"class": "logging.StreamHandler"}},
    "root": {"handlers": ["console"], "level": "INFO"},
}
