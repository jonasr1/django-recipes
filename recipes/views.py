from functools import cached_property
from typing import Any, Final

from decouple import config
from django.db.models import Q
from django.db.models.query import QuerySet
from django.http.response import Http404
from django.utils.http import urlencode
from django.views.generic import DetailView, ListView

from recipes.models import Recipe
from utils.pagination import make_pagination

PER_PAGE: Final[int] = config("PER_PAGE", default=6)


class RecipeListViewBase(ListView):
    model = Recipe
    context_object_name = "recipes"
    ordering = ("-id")

    def get_queryset(self, *args, **kwargs) -> QuerySet[Recipe]:
        qs = super().get_queryset(*args, **kwargs)
        return qs.filter(is_published=True)

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        page_obj, pagination_range = make_pagination(
            self.request, context.get("recipes"), PER_PAGE,
        )
        context.update({"recipes": page_obj, "pagination_range": pagination_range})
        return context


class RecipeListViewHome(RecipeListViewBase):
    template_name = "recipes/pages/home.html"


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
            context["title"] = "Unknown Category"
            return context
        category_obj = recipes[0].category
        category_name = category_obj.name if category_obj else "Desconhecido"
        context["title"] = f"{category_name} - Category"
        return context


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
        context.update(
            {
                "page_title": f"Search for '{search_term}'",
                "search_term": search_term,
                "additional_url_query": f"&{additional_query}",
            },
        )
        return context


class RecipeDetail(DetailView):
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
