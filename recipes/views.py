from django.http import HttpRequest, HttpResponse
from django.http.response import Http404
from django.shortcuts import get_list_or_404, get_object_or_404, render

from recipes.models import Recipe


def home(request: HttpRequest) -> HttpResponse:
    recipes = Recipe.objects.filter(is_published=True).order_by("-id")
    return render(
        request, "recipes/pages/home.html", context={"recipes": recipes}
    )


def category(request: HttpRequest, category_id: int) -> HttpResponse:
    recipes = get_list_or_404(
        Recipe.objects.filter(is_published=True, category__id=category_id)
        .order_by("-id")
    )
    category_obj = recipes[0].category
    title = f"{category_obj.name if category_obj else 'Unknown'}"
    return render(request, "recipes/pages/category.html", context={
        "recipes": recipes, "title": f"{title} - Category "
        }
    )


def recipe(request: HttpRequest, pk: int) -> HttpResponse:
    recipe_obj = get_object_or_404(Recipe, pk=pk, is_published=True)
    return render(request, "recipes/pages/recipe-view.html", context={
        "recipe": recipe_obj, "is_detail_page": True
        }
    )

def search(request: HttpRequest) -> HttpResponse:
    search_term = request.GET.get("q", "").strip()
    if not search_term:
        raise Http404
    return render(request, "recipes/pages/search.html", context={
            "page_title": f"Search for '{search_term}'", "search_term": search_term,
        },
    )
