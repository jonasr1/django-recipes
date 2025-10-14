from typing import TYPE_CHECKING, cast

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http.request import HttpRequest
from django.http.response import Http404, HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse

from authors.forms import AuthorRecipeForm, LoginForm, RegisterForm
from recipes.models import Recipe

if TYPE_CHECKING:
    from django.contrib.auth.models import User


def register_view(request: HttpRequest) -> HttpResponse:
    register_form_data = request.session.get("register_form_data", None)
    form = RegisterForm(register_form_data)
    return render(request, "authors/pages/register_view.html", {
        "form": form, "form_action": reverse("authors:register_create"),
    })


def register_create(request: HttpRequest) -> HttpResponseRedirect:
    if not request.POST:
        raise Http404
    post_data = request.POST
    request.session["register_form_data"] = post_data
    form = RegisterForm(post_data)
    if form.is_valid():
        user: User = form.save(commit=False)
        raw_password: str = form.cleaned_data["password"]
        user.set_password(raw_password)
        user.save()
        messages.success(request, "Your user is created, please log in.")
        del request.session["register_form_data"]
        return redirect(reverse("authors:login"))
    return redirect(reverse("authors:register"))


def login_view(request: HttpRequest) -> HttpResponse:
    form = LoginForm()
    return render(request, "authors/pages/login.html", {
        "form": form, "form_action": reverse("authors:login_create"),
    })


def login_create(request: HttpRequest) -> HttpResponseRedirect:
    if not request.POST:
        raise Http404
    form = LoginForm(request.POST)
    if form.is_valid():
        authenticated_user = authenticate(
            username=form.cleaned_data.get("username", ""),
            password=form.cleaned_data.get("password", ""),
        )
        if authenticated_user is not None:
            messages.success(request, "You are logged in.")
            login(request, authenticated_user)
        else:
            messages.error(request, "Invalid credentials")
    else:
        messages.error(request, "Invalid username or password")
    return redirect(reverse("authors:dashboard"))


@login_required(login_url="authors:login", redirect_field_name="next")
def logout_view(request: HttpRequest) -> HttpResponseRedirect:
    if not request.POST:
        messages.error(request, "Invalid logout request")
        return redirect(reverse("authors:login"))
    messages.success(request, "Logged out successfully")
    logout(request)
    return redirect(reverse("authors:login"))


@login_required(login_url="authors:login", redirect_field_name="next")
def dashboard(request: HttpRequest) -> HttpResponse:
    user: User = cast("User", request.user)
    recipes = Recipe.objects.filter(is_published=False, author=user)
    return render(request, "authors/pages/dashboard.html", context={"recipes": recipes})


@login_required(login_url="authors:login", redirect_field_name="next")
def dashboard_recipe_edit(request: HttpRequest, recipe_id: int) -> HttpResponse:
    user: User = cast("User", request.user)
    recipe = Recipe.objects.filter(
        is_published=False, author=user, pk=recipe_id,
    ).first()
    if not recipe:
        raise Http404
    form = AuthorRecipeForm(
        data=request.POST or None, instance=recipe, files=request.FILES or None,
    )
    if form.is_valid():
        recipe: Recipe = form.save(commit=False)
        recipe.author = cast("User", request.user)
        recipe.preparation_steps_is_html = False
        recipe.is_published = False
        recipe.save()
        messages.success(request, "Your recipe has been saved successfully!")
        redirect(reverse("authors:dashboard_recipe_edit", args=(recipe_id,)))
    return render(
        request, "authors/pages/dashboard_recipe.html", context={"form": form},
    )
