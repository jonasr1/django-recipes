from django.http.request import HttpRequest
from django.http.response import HttpResponse
from django.shortcuts import render


def register_view(request: HttpRequest) -> HttpResponse:
    return render(request, "authors/pages/register_view.html")
