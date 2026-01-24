from functools import cached_property
from typing import Any, Final

from decouple import config  # pyright: ignore[reportMissingTypeStubs]
from django.db.models import Q
from django.db.models.aggregates import Count
from django.db.models.query import QuerySet
from django.forms.models import model_to_dict
from django.http import HttpResponse
from django.http.request import HttpRequest
from django.http.response import Http404, HttpResponseBase, JsonResponse
from django.shortcuts import render
from django.utils import translation
from django.utils.http import urlencode
from django.utils.translation import gettext as _
from django.views.generic import DetailView, ListView

from recipes.models import Recipe
from tag.models import Tag
from utils.pagination import make_pagination

PER_PAGE: Final[int] = config("PER_PAGE", default=6, cast=int)


def theory(request: HttpRequest, *args, **kwargs) -> HttpResponse:
    recipes = Recipe.objects.values("id", "title")
    number_of_recipes = recipes.aggregate(Count("id"))
    context = {"recipes": recipes, "number_of_recipes": number_of_recipes["id__count"]}
    return render(request, "recipes/pages/theory.html", context=context)


class RecipeListViewBase(ListView):  # pyright: ignore[reportMissingTypeArgument]
    model = Recipe
    context_object_name = "recipes"
    ordering = ("-id",)

    def get_queryset(self, *args, **kwargs) -> QuerySet[Recipe]:
        return (
            super()
            .get_queryset(*args, **kwargs)
            .filter(is_published=True)
            .select_related("author", "category")
            .prefetch_related("tags", "author__profile")
        )

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        page_obj, pagination_range = make_pagination(
            self.request, context.get("recipes"), PER_PAGE,  # type: ignore
        )
        html_language = translation.get_language()
        context.update({
            "recipes": page_obj,
            "pagination_range": pagination_range,
            "html_language": html_language,
        })
        return context


class RecipeApiMixin:
    """
    Mixin to share serialization logic between API views.

    This mixin provides a method to serialize Recipe model instances into
    dictionary format suitable for API responses. It handles date formatting,
    cover image URL generation, and removes unwanted fields from the output.

    Methods:
        serialize_recipe(recipe): Converts a Recipe instance to a serialized
            dictionary with formatted dates, absolute cover image URLs, and
            filtered fields.
    """

    def serialize_recipe(self, recipe: Recipe) -> dict[str, Any]:
        recipe_dict = model_to_dict(recipe)
        recipe_dict["created_at"] = recipe.created_at.isoformat()
        recipe_dict["updated_at"] = recipe.updated_at.isoformat()
        if recipe.cover:
            recipe_dict["cover"] = self.request.build_absolute_uri(recipe.cover.url)
        else:
            recipe_dict["cover"] = ""
        recipe_dict.pop("is_published", None)
        return recipe_dict

    def get_serialized_list(self, context: dict[str, Any]) -> list[dict[str, Any]]:
        page_obj = context.get("recipes")
        if page_obj and hasattr(page_obj, "object_list"):
            return [self.serialize_recipe(recipe) for recipe in page_obj.object_list]
        return []


class RecipeListViewHome(RecipeListViewBase):
    template_name = "recipes/pages/home.html"


class RecipeListViewHomeApi(RecipeApiMixin, RecipeListViewBase):
    def render_to_response(self, context, **response_kwargs) -> JsonResponse:  # noqa: ANN001
        return JsonResponse(data={"recipes": self.get_serialized_list(context)})


class RecipeListViewCategory(RecipeListViewBase):
    template_name = "recipes/pages/category.html"

    def get_queryset(self, *args, **kwargs) -> QuerySet[Recipe]:
        category_id = self.kwargs.get("category_id")
        qs = (super().get_queryset(*args, **kwargs))
        qs = qs.filter(is_published=True, category__id=category_id)
        if not qs.exists():
            msg = "No recipes found in this category"
            raise Http404(msg)
        return qs

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        recipes = context["recipes"]
        if not recipes:
            context["title"] = _("Unknown Category")
            return context
        category_obj = recipes[0].category
        category_name = category_obj.name if category_obj else "Unknown"
        context["title"] = f"{category_name} - {_("Category")}"
        context["category_name"] = category_name
        return context


class RecipeListViewCategoryApi(RecipeApiMixin, RecipeListViewCategory):
    def render_to_response(self, context, **response_kwargs) -> JsonResponse:  # noqa: ANN001
        return JsonResponse(
            data={
                "recipes": self.get_serialized_list(context),
                "category_name": context.get("category_name", ""),
            },
        )


class RecipeListViewSearch(RecipeListViewBase):
    template_name = "recipes/pages/search.html"

    @cached_property
    def search_term(self) -> str:
        return (self.request.GET.get("q") or "").strip()

    def get_queryset(self, *args, **kwargs) -> QuerySet[Recipe]:
        search_term = self.search_term
        if not search_term:
            raise Http404
        qs = super().get_queryset()
        return qs.filter(
            Q(title__icontains=search_term) | Q(description__icontains=search_term),
            is_published=True,
        )

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        search_term = self.search_term
        additional_query = urlencode({"q": search_term})
        context.update({
            "page_title": f"Search for '{search_term}'",
            "search_term": search_term,
            "additional_url_query": f"&{additional_query}",
        })
        return context


class RecipeListViewTag(RecipeListViewBase):
    template_name = "recipes/pages/tag.html"

    def get_queryset(self, *args, **kwargs) -> QuerySet[Recipe]:
        qs = super().get_queryset()
        return qs.filter(tags__slug=self.kwargs.get("slug", ""))

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        tag = Tag.objects.filter(slug=self.kwargs.get("slug", "")).first()
        page_title = "No recipes found" if not tag else f"{tag} - Tag |"
        context.update({"page_title": page_title})
        return context


class RecipeListViewSearchApi(RecipeApiMixin, RecipeListViewSearch):
    def dispatch(self, request: HttpRequest, *args, **kwargs) -> HttpResponseBase:
        # We check the search term BEFORE any other logic
        if not self.search_term:
            return JsonResponse(
                data={"error": "Search term 'q' is required."}, status=400,
            )
        return super().dispatch(request, *args, **kwargs)

    def render_to_response(self, context, **response_kwargs) -> JsonResponse:  # noqa: ANN001
        return JsonResponse(
            {"recipes": self.get_serialized_list(context), "search_term": self.search_term},  # noqa: E501
        )


class RecipeDetail(DetailView):  # pyright: ignore[reportMissingTypeArgument]
    model = Recipe
    context_object_name = "recipe"
    template_name = "recipes/pages/recipe-view.html"

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["is_detail_page"] = True
        return context

    def get_queryset(self) -> QuerySet[Recipe]:
        qs = super().get_queryset()
        return qs.filter(is_published=True)


class RecipeDetailApi(RecipeApiMixin, RecipeDetail):
    def render_to_response(self, context, **response_kwargs) -> JsonResponse:  # noqa: ANN001
        recipe_data = self.serialize_recipe(self.object)
        return JsonResponse({"recipe": recipe_data})
