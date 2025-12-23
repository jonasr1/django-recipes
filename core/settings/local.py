from .base import *  # noqa: F403
from .base import BASE_DIR

DEBUG = True
ALLOWED_HOSTS = ["*"]

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
