# pyright: reportConstantRedefinition=false
from core.settings.base import *  # noqa: F403
from core.settings.base import BASE_DIR
from core.settings.installed_apps import INSTALLED_APPS
from core.settings.middlewares import MIDDLEWARE

DEBUG = True

MIDDLEWARE.insert(
    MIDDLEWARE.index("django.middleware.common.CommonMiddleware") + 1,
    "debug_toolbar.middleware.DebugToolbarMiddleware",
)
INSTALLED_APPS += ["debug_toolbar"]

STATICFILES_DIRS = [
    BASE_DIR / "base_static",
]

# Database
# https://docs.djangoproject.com/en/5.2/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    },
}

# Local storage (filesystem)
STORAGES = {
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
    },
    "staticfiles": {
        "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage",
    },
}

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

# Django Debug Toolbar
INTERNAL_IPS = ["127.0.0.1", "localhost"]
# Note: Docker users may need SHOW_TOOLBAR_CALLBACK=show_toolbar_with_docker
