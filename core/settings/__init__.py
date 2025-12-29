from decouple import config  # pyright: ignore[reportMissingTypeStubs]

ENVIRONMENT = config("DJANGO_ENV", default="local")
if ENVIRONMENT == "production":
    from .production import *  # noqa
else:
    from .local import *  # noqa
