from django.shortcuts import render

from django.http import HttpRequest, HttpResponse


def home(request: HttpRequest) -> HttpResponse:
    return render(request, 'recipes/home.html')


def contato(request: HttpRequest) -> HttpResponse:
    return HttpResponse('contato')


def sobre(request: HttpRequest) -> HttpResponse:
    return HttpResponse('sobre')
