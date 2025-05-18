from django.shortcuts import render
from django.http import HttpRequest, HttpResponse

from recipes.utils.recipes.factory import make_recipe


def home(request: HttpRequest) -> HttpResponse:
    return render(request, 'recipes/pages/home.html', context={
        'recipes': [make_recipe() for _ in range(10)]
    })


def recipe(request: HttpRequest, id: int) -> HttpResponse:
    return render(request, 'recipes/pages/recipe-view.html', context={
        'recipe': make_recipe(), 'is_detail_page': True
    })
