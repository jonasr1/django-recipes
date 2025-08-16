from django.http.request import HttpRequest
from django.http.response import Http404, HttpResponse
from django.shortcuts import redirect, render

from authors.forms import RegisterForm


def register_view(request: HttpRequest) -> HttpResponse:
    register_form_data = request.session.get("register_form_data", None)
    form = RegisterForm(register_form_data)
    return render(request, "authors/pages/register_view.html", {"form": form})

def register_create(request: HttpRequest) -> HttpResponse:
    if not request.POST:
        raise Http404
    POST = request.POST
    request.session["register_form_data"] = POST
    form = RegisterForm(POST)
    return redirect("authors:register")
