from django.contrib import admin

from tag.models import Tag


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):  # pyright: ignore[reportMissingTypeArgument]
    list_display = ("id", "name", "slug")
    list_display_links = ("id", "slug")
    search_fields = ("id", "name", "slug")
    list_editable = ("name",)
    list_per_page = 10
    list_editable = ("name",)
    ordering = ("-id",)
    prepopulated_fields = {"slug": ["name"]}  # noqa: RUF012
