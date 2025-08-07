from django.db.models import Q
from django.http import HttpRequest, HttpResponse
from django.http.response import Http404
from django.shortcuts import get_list_or_404, get_object_or_404, render

from recipes.models import Recipe
from recipes.utils.pagination import make_pagination


def home(request: HttpRequest) -> HttpResponse:
    recipes = Recipe.objects.filter(is_published=True).order_by("-id")
    page_obj, pagination_range = make_pagination(request, recipes, 9)
    return render(
        request,
        "recipes/pages/home.html",
        context={"recipes": page_obj, "pagination_range": pagination_range},
    )


def category(request: HttpRequest, category_id: int) -> HttpResponse:
    recipes = get_list_or_404(
        Recipe.objects.filter(is_published=True, category__id=category_id).order_by(
            "-id"
        )
    )
    category_obj = recipes[0].category
    title = f"{category_obj.name if category_obj else 'Unknown'}"
    page_obj, pagination_range = make_pagination(request, recipes, 9)

    return render(
        request, "recipes/pages/category.html",
        context={
            "recipes": page_obj, "title": f"{title} - Category ",
            "pagination_range": pagination_range,
        },
    )


def recipe(request: HttpRequest, pk: int) -> HttpResponse:
    recipe_obj = get_object_or_404(Recipe, pk=pk, is_published=True)
    return render(
        request,
        "recipes/pages/recipe-view.html",
        context={"recipe": recipe_obj, "is_detail_page": True},
    )


def search(request: HttpRequest) -> HttpResponse:
    search_term = request.GET.get("q", "").strip()
    if not search_term:
        raise Http404
    recipes = Recipe.objects.filter(
        Q(
            Q(title__icontains=search_term) | Q(description__icontains=search_term),
            is_published=True,
        )
    ).order_by("-id")
    page_obj, pagination_range = make_pagination(request, recipes, 9)

    return render(
        request,
        "recipes/pages/search.html",
        context={
            "page_title": f"Search for '{search_term}'",
            "search_term": search_term,
            "recipes": page_obj,
            "pagination_range": pagination_range,
            "additional_url_query": f"&q={search_term}"
        },
    )
