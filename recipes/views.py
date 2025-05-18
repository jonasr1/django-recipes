from django.shortcuts import render

from django.http import HttpRequest, HttpResponse


def home(request: HttpRequest) -> HttpResponse:
    return render(request, 'recipes/pages/home.html', context={
        'name': 'Jonas'
    })


def recipe(request: HttpRequest, id: int) -> HttpResponse:
    return render(request, 'recipes/pages/recipe-view.html', context={
        'name': 'Jonas'
    })
