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
    "unfold",
    "unfold.contrib.forms",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "rest_framework",
    "saglik",
    "icerik",
    "iletisim",
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
        "DIRS": [BASE_DIR / "templates"],
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

from ortak.depolama import storages_ayari  # noqa: E402

STORAGES = storages_ayari(os.environ)

REST_FRAMEWORK = {
    "DEFAULT_RENDERER_CLASSES": ["rest_framework.renderers.JSONRenderer"],
    "DEFAULT_PARSER_CLASSES": ["rest_framework.parsers.JSONParser"],
    "DEFAULT_AUTHENTICATION_CLASSES": [],
    "DEFAULT_PERMISSION_CLASSES": ["rest_framework.permissions.AllowAny"],
    "UNAUTHENTICATED_USER": None,
}

# E-posta bildirimi: EMAIL_HOST boşsa gönderilmez, mesajlar yalnız panelde durur.
EMAIL_HOST = ortam("EMAIL_HOST")
EMAIL_PORT = int(ortam("EMAIL_PORT", "587"))
EMAIL_HOST_USER = ortam("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = ortam("EMAIL_HOST_PASSWORD")
EMAIL_USE_TLS = ortam_bool("EMAIL_USE_TLS", True)
EMAIL_TIMEOUT = 8
DEFAULT_FROM_EMAIL = ortam("DEFAULT_FROM_EMAIL") or EMAIL_HOST_USER or "noreply@localhost"

from django.urls import reverse_lazy  # noqa: E402


def _baglanti(ad):
    return reverse_lazy(f"admin:{ad}")


UNFOLD = {
    "SITE_TITLE": "Eskilder Yönetim",
    "SITE_HEADER": "Eskilder Yönetim",
    "SITE_SUBHEADER": "Site içeriği",
    "SITE_SYMBOL": "volunteer_activism",
    "SITE_URL": SITE_URL,
    "SHOW_HISTORY": True,
    "SHOW_VIEW_ON_SITE": False,
    "DASHBOARD_CALLBACK": "icerik.views_yonetim.ozet",
    "COLORS": {
        "primary": {
            "50": "oklch(97% .02 160)", "100": "oklch(94% .04 160)", "200": "oklch(88% .07 160)",
            "300": "oklch(78% .09 160)", "400": "oklch(66% .1 160)", "500": "oklch(55% .1 160)",
            "600": "oklch(46% .09 160)", "700": "oklch(39% .08 160)", "800": "oklch(32% .06 160)",
            "900": "oklch(27% .05 160)", "950": "oklch(20% .04 160)",
        },
    },
    "SIDEBAR": {
        "show_search": False,
        "show_all_applications": False,
        "navigation": [
            {
                "title": "İçerik",
                "items": [
                    {"title": "Ana Sayfa (özet)", "icon": "dashboard", "link": reverse_lazy("admin:index")},
                    {"title": "Duyurular", "icon": "campaign", "link": _baglanti("icerik_duyuru_changelist")},
                    {"title": "Etkinlikler & Buluşmalar", "icon": "event", "link": _baglanti("icerik_etkinlik_changelist")},
                    {"title": "Destekçiler", "icon": "handshake", "link": _baglanti("icerik_destekci_changelist")},
                    {"title": "Gelen Mesajlar", "icon": "mail", "link": _baglanti("iletisim_iletisimmesaji_changelist"),
                     "badge": "icerik.views_yonetim.okunmamis_mesaj_rozeti"},
                ],
            },
            {
                "title": "Sayfa bilgileri",
                "items": [
                    {"title": "Etki Rakamları", "icon": "monitoring", "link": _baglanti("icerik_etkirakami_changelist")},
                    {"title": "Yönetim Kurulu", "icon": "groups", "link": _baglanti("icerik_yonetimkuruluuyesi_changelist")},
                    {"title": "Belgeler", "icon": "description", "link": _baglanti("icerik_dokuman_changelist")},
                    {"title": "Site Ayarları", "icon": "settings", "link": _baglanti("icerik_siteayarlari_changelist")},
                ],
            },
            {
                "title": "Sistem",
                "items": [
                    {"title": "Kullanıcılar", "icon": "person", "link": _baglanti("auth_user_changelist"),
                     "permission": "icerik.views_yonetim.sadece_super"},
                    {"title": "Gruplar", "icon": "admin_panel_settings", "link": _baglanti("auth_group_changelist"),
                     "permission": "icerik.views_yonetim.sadece_super"},
                ],
            },
        ],
    },
}
