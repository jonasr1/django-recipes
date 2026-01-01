from django.contrib import admin
from django.contrib.contenttypes.admin import GenericStackedInline

from recipes.models import Category, Recipe
from tag.models import Tag


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):  # pyright: ignore[reportMissingTypeArgument]
    ...


class TagInline(GenericStackedInline):
    model = Tag
    fields = ("name",)
    extra = 1


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):  # pyright: ignore[reportMissingTypeArgument]
    list_display = ("id", "title", "created_at", "is_published", "author")
    list_display_links = ("title",)
    search_fields = ("id", "title", "description", "slug", "preparation_steps")
    list_filter = ("category", "author", "is_published", "preparation_steps_is_html")
    list_per_page = 10
    list_editable = ("is_published",)
    ordering = ("-id",)
    prepopulated_fields = {"slug": ("title",)}  # noqa: RUF012
    inlines = (TagInline,)
