from django.apps import AppConfig


class RecipesConfig(AppConfig):
    DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
    name = "recipes"

    def ready(self) -> None:
        import recipes.signals  # noqa: F401
