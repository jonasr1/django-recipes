from core.settings.base import *  # noqa: F403
from core.settings.base import BASE_DIR, MIDDLEWARE

DEBUG = True  # pyright: ignore[reportConstantRedefinition]

MIDDLEWARE.insert(
    MIDDLEWARE.index("django.middleware.common.CommonMiddleware") + 1,
    "debug_toolbar.middleware.DebugToolbarMiddleware",
)

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
