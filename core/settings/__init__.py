from decouple import config  # pyright: ignore[reportMissingTypeStubs]

from core.settings.base import *

# ruff: noqa: F403
from core.settings.i18n import *
from core.settings.installed_apps import *
from core.settings.logging import *
from core.settings.messages import *
from core.settings.middlewares import *
from core.settings.rest_framework import *
from core.settings.templates import *

ENVIRONMENT = config("DJANGO_ENV", default="local")
if ENVIRONMENT == "production":  # pragma: no cover
    from .production import *
else:
    from .local import *
