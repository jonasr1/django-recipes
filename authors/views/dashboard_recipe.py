from typing import TYPE_CHECKING, cast

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http.request import HttpRequest
from django.http.response import Http404, HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views import View

from authors.forms.recipe_form import AuthorRecipeForm
from recipes.models import Recipe

if TYPE_CHECKING:
    from django.contrib.auth.models import User


@method_decorator(
    login_required(login_url="authors:login", redirect_field_name="next"),
    name="dispatch",
)
class DashboardRecipe(View):
    def get_recipe(self, recipe_id: int | None = None) -> Recipe:
        recipe = None
        user: User = cast("User", self.request.user)
        if recipe_id is not None:
            recipe = Recipe.objects.filter(
                is_published=False,
                author=user,
                pk=recipe_id,
            ).first()
            if not recipe:
                raise Http404
        return recipe

    def render_recipe(self, form: AuthorRecipeForm) -> HttpResponse:
        return render(
            self.request, "authors/pages/dashboard_recipe.html", context={"form": form},
        )

    def get(self, request: HttpRequest, recipe_id: int | None = None) -> HttpResponse:
        if recipe_id:
            recipe = self.get_recipe(recipe_id)
            form = AuthorRecipeForm(instance=recipe)
            return self.render_recipe(form)
        form = AuthorRecipeForm()
        return self.render_recipe(form)

    def post(self, request: HttpRequest, recipe_id: int | None = None) -> HttpResponse:
        recipe = self.get_recipe(recipe_id)
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
            return redirect(reverse("authors:dashboard_edit_recipe", args=(recipe.id,)))
        return self.render_recipe(recipe)


class DashboardRecipeDelete(DashboardRecipe):
    def post(self, *args, **kwargs) -> HttpResponse:  # noqa: ANN002, ANN003
        recipe = self.get_recipe(self.request.POST.get("id"))
        recipe.delete()
        messages.success(self.request, "Deleted successfully.")
        return redirect(reverse("authors:dashboard"))
