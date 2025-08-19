from django.contrib import messages
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
    post_data = request.POST
    request.session["register_form_data"] = post_data
    form = RegisterForm(post_data)
    if form.is_valid():
        form.save()
        messages.success(request, "Your user is created, please log in.")
        del request.session["register_form_data"]
    return redirect("authors:register")
